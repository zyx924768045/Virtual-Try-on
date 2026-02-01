import io
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
device="pytorch1.7.1 cuda11.0"
model_path = 'pasta-gan-plusplus\checkpoint\pasta-gan++\ network-snapshot-004408.pkl'
model = tf.keras.models.load_model(model_path,device)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
@app.route('/home', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        try:
            img = Image.open(file).resize((512, 312)).convert("RGB")
            img_array = (np.array(img) / 127.5) - 1.0
            img_array = np.expand_dims(img_array, axis=0)
            generated_image = model.predict(img_array)
            denormalized_image = (generated_image[0] + 1) * 127.5
            output_img = Image.fromarray(np.uint8(denormalized_image))

            response = jsonify({'message': "Image generated successfully!"})
            response.status_code = 200
            response.headers['Content-Type'] = 'image/jpg'

            img_byte_arr = io.BytesIO()
            output_img.save(img_byte_arr, format='JPG')
            img_byte_arr = img_byte_arr.getvalue()

            response.set_data(img_byte_arr)
            return response

        except Exception as e:
            return jsonify({'error': 'Failed to generate image: {}'.format(e)}), 400

    return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
#该API接受POST请求，用户将待生成的图片文件通过文件上传提交，
# 上传的图片不能超过规定的格式和大小，否则会返回错误信息。
# 服务器根据图片生成一张新的图片，并将其作为响应数据返回。
# 服务器使用了PIL库来处理图片，使用TensorFlow Keras库来加载PASTA-GAN++模型。
# 在预测图片时，根据PASTA-GAN++论文中的方法，将待生成的图片缩放为512 x 312像素大小，
# 缩放后的图片经过归一化，再使用模型得到一个生成的图像。最后将生成的图像反归一化，
# 保存为JPG格式的图片数据。
