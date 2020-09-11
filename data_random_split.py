'''
数据整合与随机切分，构造两个数据集，一是main label+abstract的单标签分类，二是 all label+abstract + abstract 用作多标签分类
按照比例8：2，随机切分为训练集与测试集
'''
import os
import random

file_name_list = ['A61C1700', 'A63B520', 'B64C100', 'B82Y3000', 'C02F100', 'D01D100', 'E01B100', 'F03G300', 'F21S902',
                  'H01B100']

# file_name_list = ['A61C1700', 'A63B520']



# 切分函数，把文件切分为8:2,此处由于爬虫数据本身无规律，没有随机
def split(full_list, shuffle=False, ratio=0.2):
    n_total = len(full_list)
    offset = int(n_total * (1 - ratio))
    if n_total == 0 or offset < 1:
        return [], full_list
    if shuffle:
        random.shuffle(full_list)
    sublist_1 = full_list[:offset]
    sublist_2 = full_list[offset:]
    return sublist_1, sublist_2


# 对每一个类别，进行label与abstract的切分，然后把所有的label与abstract合并
total_one_label_train = []
total_one_label_test = []
total_multi_label_train = []
total_multi_label_test = []
total_abstract_train = []
total_abstract_test = []


cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])

for file_name in file_name_list:
    abstract_path = os.path.join(cur_dir, 'data/'+file_name+'_abstract.txt')
    main_label_path = os.path.join(cur_dir, 'data/'+file_name+'_main_label.txt')
    all_label_path = os.path.join(cur_dir, 'data/reduce_data/'+file_name+'_all_label.txt')

    abstract = open(abstract_path, 'r',encoding='utf-8').readlines()
    main_label = open(main_label_path,'r',encoding='utf-8').readlines()
    all_label = open(all_label_path,'r',encoding='utf-8').readlines()

    train_abstract,test_abstract = split(abstract,shuffle=False, ratio=0.2)
    train_main_label, test_main_label = split(main_label,shuffle=False,ratio=0.2)
    train_all_label,test_all_label = split(all_label,shuffle=False,ratio=0.2)

    total_one_label_train += train_main_label
    total_one_label_test += test_main_label
    total_multi_label_train += train_all_label
    total_multi_label_test += test_all_label
    total_abstract_train += train_abstract
    total_abstract_test += test_abstract


one_label_train_path = os.path.join(cur_dir, 'data/one_label_train.txt')
one_label_test_path = os.path.join(cur_dir, 'data/one_label_test.txt')
multi_label_train_path = os.path.join(cur_dir, 'data/reduce_data/multi_label_train.txt')
multi_label_test_path = os.path.join(cur_dir, 'data/reduce_data/multi_label_test.txt')

with open(one_label_train_path,'w',encoding='utf-8') as f:
    for i in range(len(total_one_label_train)):
        # f.write(total_one_label_train[i].strip()+'\t'+total_abstract_train[i].strip()+'\n')
        f.write(total_one_label_train[i].replace('\n','').strip()+'\t'+total_abstract_train[i].strip() + '\n')
    f.close()

with open(one_label_test_path,'w',encoding='utf-8') as f:
    for i in range(len(total_one_label_test)):
        # f.write(total_one_label_train[i].strip()+'\t'+total_abstract_train[i].strip()+'\n')
        f.write(total_one_label_test[i].replace('\n','').strip()+'\t'+total_abstract_test[i].strip() + '\n')
    f.close()

with open(multi_label_train_path,'w',encoding='utf-8') as f:
    for i in range(len(total_multi_label_train)):
        # f.write(total_one_label_train[i].strip()+'\t'+total_abstract_train[i].strip()+'\n')
        f.write(total_multi_label_train[i].replace('\n','').strip()+'\t'+total_abstract_train[i].strip() + '\n')
    f.close()

with open(multi_label_test_path,'w',encoding='utf-8') as f:
    for i in range(len(total_multi_label_test)):
        # f.write(total_one_label_train[i].strip()+'\t'+total_abstract_train[i].strip()+'\n')
        f.write(total_multi_label_test[i].replace('\n','').strip()+'\t'+total_abstract_test[i].strip() + '\n')
    f.close()














