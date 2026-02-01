from flask import Flask, jsonify, request
import clip
import torch
from transformers import BertForSequenceClassification, BertConfig, BertTokenizer
from transformers import CLIPProcessor, CLIPModel
app = Flask(__name__)
text_tokenizer = BertTokenizer.from_pretrained("IDEA-CCNL/Taiyi-CLIP-Roberta-102M-Chinese",trust_remote_code=True)
text_encoder = BertForSequenceClassification.from_pretrained("IDEA-CCNL/Taiyi-CLIP-Roberta-102M-Chinese",trust_remote_code=True).eval()
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32",trust_remote_code=True)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32",trust_remote_code=True)
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = clip.load("ViT-B/32", device)

@app.route('/api/clip', methods=['POST'])
def get_clip_result():
    data = request.json()
    text = data['text']
    image = preprocess(data['image']).unsqueeze(0).to(device)
    text_features = clip_model.text_encoder(clip.text_tokenizer([text]).to(device)).float()
    image_features = clip_model.encode_image(image).float()
    similarity = (100.0 * text_features @ image_features.T).softmax(dim=-1)
    return jsonify({'similarity': similarity.item()})

if __name__ == '__main__':
    app.run(host='0.0.0.0')





