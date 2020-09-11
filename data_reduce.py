'''
针对每一个类别，每个样本对应多个类别的情况，缩减每个样本的标签个数最多为3个
（1），对应主分类号为A61C17/00，首先去掉每个样本中开头不是A的标签；
（2），A46B5/00|A46B9/02|A46B11/02|A46B15/00|A61C17/14|A61C17/00，对于多个标签的样本，缩减其标签个数为3个
'''
import os
from collections import defaultdict

# (1)
# 规范多标签中每个标签的格式，如果标签最后有大写字母（N），删除
def step_0(path):
    all_labels = open(path,'r',encoding='utf-8').readlines()

    with open(path,'w',encoding='utf-8') as f:
        for all_label in all_labels:
            all_label = all_label.strip().split('|')
            new_all_label = []
            daxie_list =[chr(i) for i in range(65,91)]
            for ll in all_label:
                if ll[len(ll)-1] in daxie_list:
                    ll = ll[:-1]
                new_all_label.append(ll)
            ss = ''
            for ll in new_all_label:
                ss+=ll+'|'
            ss= ss[:-1]
            f.write(ss+'\n')
    f.close()


def step_1(path1,path2,sym):
    all_labels = open(path1,'r',encoding='utf-8').readlines()
    new_all_labels = []
    with open(path2,'w',encoding='utf-8') as f:
        for line in all_labels:
            new_line = ''
            labels = line.strip().split('|')
            new_labels = []
            for label in labels:
                if (label[0] is not sym):
                    new_labels.append(label)
            labels = list(set(labels).difference(set(new_labels)))
            for label in labels:
                new_line+=label+'|'
            new_line = new_line[:-1]
            f.write(new_line+'\n')
    f.close()
# (2),统计标签出现的频次：
def step_2(path,sym,len_label):
    with open(path, 'r', encoding='utf-8') as f:
        content = [_.strip() for _ in f.readlines()]

# 每个事件类型的数量统计
    event_type_count_dict = defaultdict(int)

    for line in content:
    # 事件类型
        event_types = line

    # 对应的每个事件类型数量加1
        for event_type in event_types.split("|"):
            event_type_count_dict[event_type] += 1
#
# # 输出结果
    sort_labels = sorted(event_type_count_dict.items(),key=lambda x:x[1],reverse=False)
    delete_labels = []
    for sort_label in sort_labels:
        if (int(str(sort_label).split(',')[1].replace(')', '')) < len_label) :
            delete_label = str(sort_label).split(',')[0].replace('(','').replace('\'','')
            # print(delete_label)
            delete_labels.append(delete_label)
    print(len(delete_labels))
    # print(delete_labels)
    new_all_labels = open(path,'r',encoding='utf-8').readlines()

    with open(path, 'w', encoding='utf-8') as f:
        for all_label in new_all_labels:
            # print(all_label)
            all_label = all_label.strip().split('|')
            new_label = []

            for ss in delete_labels:
                if ss in all_label:
                    new_label.append(ss)
            # print(new_label)
            all_label = list(set(all_label).difference(set(new_label)))
            s = ''
            for i in all_label:
                s += i+'|'
            s= s[:-1]
            f.write(s+'\n')
    f.close()
    last_all_label = open(path,'r',encoding='utf-8').readlines()
    count_label = []
    for line in last_all_label:
        n = line.strip().count('|')+1
        count_label.append(n)
    print(max(count_label))

# 第三步，数据进一步处理：
def step_3(path,sym):
    last_all_label = open(path, 'r', encoding='utf-8').readlines()
    with open(path,'w',encoding='utf-8') as f:
        for label in last_all_label:
            label = label.strip()
            label = label.replace('|','')
            f.write(str(label)+'\n')
    f.close()

    all_labels = open(new_all_label_path, 'r', encoding='utf-8').readlines()
    with open(new_all_label_path, 'w', encoding='utf-8') as f:

        for line in all_labels:
            line = line.strip()
            line = insert_label(line,sym)
            f.write(str(line) + '\n')
    f.close()

# 标签中插入分隔符'|'
def insert_label(label,sym):
    new_label = None
    if label.count(sym) == 1:
        new_label = label
    if label.count(sym) == 2:
        index = label.find(sym, 2)
        str_list = list(label)
        str_list.insert(index, '|')
        new_label = ''.join(str_list)
    if label.count(sym) == 3:
        index1 = label.find(sym, 1)
        str_list = list(label)
        str_list.insert(index1, '|')
        new_label = ''.join(str_list)
        index2 = new_label.find(sym, index1 + 2)
        str_list1 = list(new_label)
        str_list1.insert(index2, '|')
        new_label = ''.join(str_list1)
    return new_label

if __name__ == '__main__':
    cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
    all_label_path = os.path.join(cur_dir, 'data/H01B100_all_label.txt')
    new_all_label_path = os.path.join(cur_dir, 'data/reduce_data/H01B100_all_label.txt')
    sym = 'H'
    len_label = 100
    step_0(all_label_path)
    step_1(all_label_path,new_all_label_path,sym)
    step_2(new_all_label_path,sym,len_label)
