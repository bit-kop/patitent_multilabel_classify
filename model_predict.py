# -*- coding: utf-8 -*-
import json
import numpy as np
from keras.models import load_model
from att import Attention
from albert_zh.extract_feature import BertVector
import os

cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
model_path = os.path.join(cur_dir, 'model/my_event_type.h5')
load_model = load_model(model_path,custom_objects={'Attention':Attention})

# 预测语句
text = "本发明公开了一种智能跳绳的制作方法及智能跳绳器具。该方法是将计数器、计时器、感应器和提示装置安装在跳绳的其中一个手柄内，计时器采用倒计时方式，开始跳绳时先设定跳绳时间；跳绳开始时，绳子每转动一周触发感应器一次，计数器跳动一个数字，当达到设定时间后，提示装置发出声音，同时切断感应器电源，计数器停止计数计数器停留在设定时间内的跳绳总数。本发明能准确地测定设定时间内跳绳个数。本发明构思新颖，体积小，重量轻，结构紧凑，携带方便，安全可靠，操作简单，容易掌握。"
text = text.replace("\n", "").replace("\r", "").replace("\t", "")

labels = []

bert_model = BertVector(pooling_strategy="NONE", max_seq_len=200)

# 将句子转换成向量
vec = bert_model.encode([text])["encodes"][0]
x_train = np.array([vec])

# 模型预测
predicted = load_model.predict(x_train)[0]

print(predicted)

indices = [i for i in range(len(predicted)) if predicted[i] > 0.1]

for indice in indices:
    print(predicted[indice])

event_json_path = os.path.join(cur_dir, 'data/event_type.json')

with open(event_json_path, "r", encoding="utf-8") as g:
    movie_genres = json.loads(g.read())

print("预测语句: %s" % text)
print("预测事件类型: %s" % "|".join([movie_genres[index] for index in indices]))