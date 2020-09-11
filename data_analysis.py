# -*- coding: utf-8 -*-
# 训练集与测试集数据分析
# 首先是
import re
from collections import defaultdict  #实现特定目标的容器，defaultdict：字典的子类，为字典查询提供一个默认值
from pprint import pprint  # 打印完整的数据结构
import os

# 爬出来的数据，有的多标签种包含了（），需要正则去除（）中的内容

file_name_list = ['A61C1700', 'A63B520', 'B64C100', 'B82Y3000', 'C02F100', 'D01D100', 'E01B100', 'F03G300', 'F21S902',
                  'H01B100']

for file_name in file_name_list:
    cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
    all_label_path = os.path.join(cur_dir, 'data/'+file_name+'_all_label.txt')
    all_label = open(all_label_path,'r',encoding='utf-8').readlines()
    all_label_regu = [re.sub('\(.*?\)', '', i.strip().split('摘要')[0]) for i in all_label]

    with open(all_label_path,'w',encoding='utf-8') as f:
        for ll in all_label_regu:

            label_list = ll.split(' ')
            label_str = ''
            for label in label_list:
                if label is not '':
                    label_str += label + '|'
            label_str = label_str[:-1]
            f.write(label_str + '\n')
        f.close()






# train_path = os.path.join(cur_dir, 'data/multi-classification-train.txt')
# with open(train_path,'r',encoding='utf-8') as f:
#     content = [i.strip() for i in f.readlines()]
#
# # 每个事件类型的数量统计
# event_type_count_dict = defaultdict(int)
#
# # 多事件类型数量
# multi_event_type_cnt = 0
#
# for line in content:
#     #事件类型
#     event_types = line.split(' ',maxsplit=1)[0]
#     # 如果|在事件类型中，则为多事件类型
#     if '|' in event_types:
#         multi_event_type_cnt+=1
#     # 对应的每个事件类型数量+1
#     for event_type in event_types.split('|'):
#         event_type_count_dict[event_type]+=1
# print('多事件类型的样本共有%d个,占比为%.4f'%(multi_event_type_cnt,multi_event_type_cnt/len(content)))
