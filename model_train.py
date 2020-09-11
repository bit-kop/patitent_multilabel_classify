# -*- coding: utf-8 -*-
# 训练模型，ALBERT+GRU，ALBERT预训练模型+时序循环神经网络GRU
import json
import os
import numpy as np
from keras.optimizers import Adam
from tqdm import tqdm  # 实时输出处理进度
from keras import Model
from keras.layers import Input,Dense
from keras.layers import Bidirectional,GRU
from att import Attention
from albert_zh.extract_feature import BertVector
import matplotlib.pyplot as plt
from sklearn.preprocessing import MultiLabelBinarizer

cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
train_path = os.path.join(cur_dir, 'data/reduce_data/multi_label_train.txt')
test_path = os.path.join(cur_dir, 'data/reduce_data/multi_label_test.txt')

with open(train_path, 'r', encoding='utf-8') as f:
    train_content = [i.strip() for i in f.readlines()]
with open(test_path, 'r', encoding='utf-8') as f:
    test_content = [i.strip() for i in f.readlines()]

# 获取训练集与测试集的事件类型
movie_genres = []

for line in train_content + test_content:
    genres = line.split('\t', maxsplit=1)[0].split('|')
    print(genres)
    movie_genres.append(genres)

# 利用sklearn中的MultiLabelBinarizer进行多标签编码
mlb = MultiLabelBinarizer()
mlb.fit(movie_genres)
print('一共有%d种事件类型' % len(mlb.classes_))

event_type_path = os.path.join(cur_dir, 'data/event_type.json')
with open(event_type_path, 'w', encoding='utf-8') as h:
    h.write(json.dumps(mlb.classes_.tolist(), ensure_ascii=False, indent=4))

# 对训练集和测试集的数据进行多标签编码
#MultiLabelBinarizer对多标签的编码格式如下：
'''
如果文本所对应的事件类型存在，则将该位置的元素置为1，否则为0。因此，y值为65维的向量，
其中1个或多个为1，是该文本（x值）对应一个或多个事件类型
编码后，y_train的形式为：
[[1,0,0]
[0,1,1]
...    ]
每一行的标签编码为0，1格式，有标1，没有标0
'''
y_train = []
y_test = []
for line in train_content:
    genres = line.split('\t',maxsplit=1)[0].split('|')
    y_train.append(mlb.transform([genres])[0])

for line in test_content:
    genres = line.split('\t',maxsplit=1)[0].split('|')
    y_test.append(mlb.transform([genres])[0])

y_train = np.array(y_train)
y_test = np.array(y_test)

# 利用ALBERT对x值进行编码

bert_model = BertVector(pooling_strategy="NONE", max_seq_len=200)
print('begin encoding')
f = lambda text: bert_model.encode([text])['encodes'][0]

x_train=[]
x_test = []
process_bar = tqdm(train_content)

for ch,line in zip(process_bar,train_content):
    movie_intro = line.split('\t',maxsplit=1)[1]
    x_train.append(f(movie_intro))

process_bar = tqdm(test_content)

for ch,line in zip(process_bar,test_content):
    movie_intro = line.split('\t',maxsplit=1)[1]
    x_test.append(f(movie_intro))

x_train = np.array(x_train)
x_test = np.array(x_test)

print('end encoding')
print(x_train.shape)

# 深度学习模型：
# 模型结构：ALBERT+双向GRU+Attention+FC
inputs = Input(shape=(200, 312, ), name="input")
gru = Bidirectional(GRU(128,dropout=0.2,return_sequences=True),name='bi-gru')(inputs)
attention = Attention(32,name='attention')(gru)
num_class = len(mlb.classes_)
output = Dense(num_class,activation='sigmoid',name='dense')(attention)
model = Model(inputs,output)
# 模型可视化
# from keras.utils import plot_model
# model_plot_path = os.path.join(cur_dir, 'data/multi_label_model.png')
# plot_model(model,to_file=model_plot_path,show_shapes=True)
model.compile(loss='binary_crossentropy',
              optimizer=Adam(),
              metrics=['accuracy'])

history = model.fit(x_train,y_train,validation_data=(x_test,y_test),batch_size=64,epochs=50)

model_save_path = os.path.join(cur_dir, 'model/my_event_type.h5')
model.save(model_save_path)

# 训练结果可视化：
# 绘制loss与accuracy

plt.subplot(2, 1, 1)
epochs = len(history.history['loss'])
plt.plot(range(epochs), history.history['loss'], label='loss')
plt.plot(range(epochs), history.history['val_loss'], label='val_loss')
plt.legend()

plt.subplot(2, 1, 2)
epochs = len(history.history['accuracy'])
plt.plot(range(epochs), history.history['accuracy'], label='acc')
plt.plot(range(epochs), history.history['val_accuracy'], label='val_acc')
plt.legend()
loss_accuracy_path = os.path.join(cur_dir, 'data/方案-1-one-loss_acc.png')
plt.savefig(loss_accuracy_path)
