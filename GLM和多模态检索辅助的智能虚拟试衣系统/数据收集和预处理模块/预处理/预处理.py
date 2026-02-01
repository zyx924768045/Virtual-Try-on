# -*- coding: utf-8 -*-
"""
Created on Mon May 1 21:16:37 2023
中文穿搭推荐文本对话数据集预处理
@author: LENOVO
"""
import pandas as pd
from pandas import DataFrame
import numpy as np
import re

#1.读取数据
df=pd.read_csv(r"E:\Program Files (x86)\WeChat Files\wxid_buwcc958po4722\FileStorage\File\2023-05\qa11.csv",encoding='gbk')

del df['ID']#删除ID列
print(df.shape)

#2.缺失值处理
#print(df.isnull().any())#经检验，有缺失值
df=df.dropna()

#3.去重复值
print(df.duplicated().any())#结果为true，有重复值
#print(df['QUESTION'].value_counts())
df=df.drop_duplicates(['ANSWER'])
print(df.shape)
print(df.duplicated().any())
#print(df['QUESTION'].value_counts())
#print(df.loc[df['QUESTION']=='黑色短袖怎么搭配裤子'])#检测到部分正文一样但附加信息不同而造成的
                                                    #语义重复，需要对文本处理之后二次去重
#4.文本处理
for i in df.index:
    #4.1去掉回答者信息：用户名、回答时间等
    if "展开全部" in df['ANSWER'][i]:
        if df['ANSWER'][i].split('部',1)[1]:
            df['ANSWER'][i]=df['ANSWER'][i].split('部',1)[1]
    if "关注" in df['ANSWER'][i]:
        df['ANSWER'][i]=df['ANSWER'][i].split('注',1)[1]
    #4.2去掉“评论数、分享、举报”字样
    if "举报" in df['ANSWER'][i]:
        df['ANSWER'][i]=df['ANSWER'][i].rsplit('\n',4)[0]
    #4.3尽可能去掉与回答无关的文本
    if "本回答由提问者推荐" in df['ANSWER'][i]:
        df['ANSWER'][i]=df['ANSWER'][i].split('本回答由提问者推荐',1)[0]
    #4.4去空格
    df['ANSWER'][i]=df['ANSWER'][i].strip()
    #4.5去掉文本中空格,英文标点符号换成中文标点符号
    df['ANSWER'][i]=df['ANSWER'][i].replace(' ','')
    df['ANSWER'][i]=df['ANSWER'][i].replace('?','？')
    df['ANSWER'][i]=df['ANSWER'][i].replace(',','，')
    #4.6"\n"字符串换行符替换成"<br>"html换行符
    df['ANSWER'][i]=re.sub('\n\n|\n','',df['ANSWER'][i])
    #4.7将问题中的空格换成逗号
    df['QUESTION'][i]=df['QUESTION'][i].replace(' ','')
    #4.8删除仅包含时间和问题描述的无意义回答
    if "00:00" in df['ANSWER'][i]:
        df.drop(index=i, inplace=True)
#print(df.head(7))

#5.二次去重
print(df.duplicated().any())#检测到确有重复值
df=df.drop_duplicates(['QUESTION'])
print(df['QUESTION'].value_counts())

#6.dataframe重排索引
df = df.reset_index(drop=True)

#7.输出csv
df.to_csv(r'E:\Program Files (x86)\WeChat Files\wxid_buwcc958po4722\FileStorage\File\2023-05\qa11-cleaned.csv',encoding='gbk')
