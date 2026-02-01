# coding=utf-8
import keras
import numpy as np
from bilstm_crf_model import BiLstmCrfModel
from crf_layer import CRF
from data_helpers import NerDataProcessor
import tensorflow as tf
max_len = 80
vocab_size = 2410
embedding_dim = 200
lstm_units = 128

if __name__ == '__main__':

    # model.save('./checkpoint/bilstm_crf_model.h5')
    model = tf.keras.models.load_model("./checkpoint/bilstm_crf_model.h5")
    # pred = model.predict("")

    from metrics import *
    y_true, y_pred = [],[]

    for t_oh,p_oh in zip(test_y,pred):
        t_oh = np.argmax(t_oh,axis=1)
        t_oh = [id2tag[i].replace('_','-') for i in t_oh if i!=0]
        p_oh = np.argmax(p_oh,axis=1)
        p_oh = [id2tag[i].replace('_','-') for i in p_oh if i!=0]

        y_true.append(t_oh)
        y_pred.append(p_oh)

    f1 = f1_score(y_true,y_pred,suffix=False)
    p = precision_score(y_true,y_pred,suffix=False)
    r = recall_score(y_true,y_pred,suffix=False)
    acc = accuracy_score(y_true,y_pred)
    print("f1_score: {:.4f}, precision_score: {:.4f}, recall_score: {:.4f}, accuracy_score: {:.4f}".format(f1,p,r,acc))
    print(classification_report(y_true, y_pred, digits=4, suffix=False))