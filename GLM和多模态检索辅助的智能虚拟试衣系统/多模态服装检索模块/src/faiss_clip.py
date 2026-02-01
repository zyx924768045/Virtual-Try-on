import  faiss
from functools import  reduce
import  numpy as np
from PIL import Image
import requests
import clip
import torch
from transformers import BertForSequenceClassification, BertConfig, BertTokenizer
from transformers import CLIPProcessor, CLIPModel
import numpy as np


dim = 768
k=4
nlist=1000

def normaliz_vec(vec_list, vectas=None):
    for i in range(len(vec_list)):
        vec = vec_list[i]
        square_sum = reduce(lambda x, y: x+y, map(lambda x: x*x, vec))
        sqrt_square_sum = np.sqrt(square_sum)
        coef = 1/sqrt_square_sum
        vec = list(map(lambda x: x*coef, vectas))
        vec_list[i] = vec
    return vec_list
def add_faiss(index,ids,datas):

    vectors = np.array( datas ).astype('float32') # vectors -> array
    ids = np.array(ids)
    #<ids,vectors>
    index.add_with_ids(ids,vectors)
def add_in_faiss(image_data_list, index=None):

    # 1. init faiss index
    index = faiss.index_factory(dim,"IDMap,Flat,L2norm",faiss.METRIC_INNER_PRODUCT)

    batch_image_data = []
    batch_id_data = []
    for i,data in enumerate(image_data_list):
        id,image = data
        batch_image_data.append(image)
        batch_id_data.append(id)
        if i%100==0:
            print("create index (faiss) ,i = ",i)
            # 2. clip-serving ( batch_image_data -> image vector)
            clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            vectors = processor(images=batch_image_data.raw), return_tensors="pt")
            vectors = normaliz_vec(vectors.tolist())
            add_faiss(index,batch_id_data,vectors) #index_db format:  <id,text vector>
            batch_image_data.clear()
            batch_id_data.clear()
    table_name = "{}_{}".format(task, index.ntotal)
    faiss.write_index(index, "{}.index".format(table_name))
    print(index.ntotal)  # index total_count
def read_index_in_faiss(table_name):
    index = faiss.read_index("{}.index".format(table_name))
    return index
def search_in_faiss(index,query,topK=4):

    # query = 黑色宽松长牛仔裤

    # query -> clip-serving (text vector)
    query = [" ".join( [ word for word in query ])]
    print("bert-serving input: ",query)
    try:
        text_tokenizer = BertTokenizer.from_pretrained("IDEA-CCNL/Taiyi-CLIP-Roberta-102M-Chinese")
        text_encoder = BertForSequenceClassification.from_pretrained("IDEA-CCNL/Taiyi-CLIP-Roberta-102M-Chinese").eval()
        vectors = text_tokenizer(query, return_tensors='pt', padding=True)['input_ids']
        vectors = normaliz_vec(vectors.tolist())
    except:
        print('error: bert-serving disconnect,please check it')
        return [],[]
    # text vector (query)->  faiss ( return search list )

    print("-" * 60)
    try:
        query = np.array(vectors).astype('float32')
        dis,ind = index.search( query,k=topK )

        return dis,ind
    except:
        print("error: faiss service error")
        return [],[]