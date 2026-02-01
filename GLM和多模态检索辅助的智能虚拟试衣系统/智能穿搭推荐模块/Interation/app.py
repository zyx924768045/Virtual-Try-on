from gevent import pywsgi
from flask import Flask
from flask_restful import Resource, Api, reqparse
from transformers import AutoTokenizer, AutoModel
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)
tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
parser = reqparse.RequestParser()
parser.add_argument('inputs', type=str, help='Inputs for chat')
parser.add_argument('history', type=str, action='append', help='Chat history')
class Chat(Resource):
    def post(self):
        args = parser.parse_args()
        inputs = args['inputs']
        history = args['history'] or []
        response, new_history = model.chat(tokenizer, inputs, history)
        return {'response': response, 'new_history': new_history}

api.add_resource(Chat, '/api/chat')
if __name__ == '__main__':
            server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
            server.serve_forever()


