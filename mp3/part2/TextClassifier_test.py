import math
from collections import Counter, defaultdict, OrderedDict

class TextClassifier(object):
    def __init__(self):
        self.lambda_mixture = 0.5

        self.label_prob          = {}
        self.word_vocab_types    = 0
        self.word_vocab          = defaultdict(int)                                              # 训练集 单词库

        self.word_count_in_label = OrderedDict((i, defaultdict(int)) for i in range(1, 15))      # 训练集 指定标签下的 单词数量，会出现0
        self.word_prob_in_label  = OrderedDict((i, defaultdict(int)) for i in range(1, 15))      #
        

    # 将一堆词，变成统计单词数量的词包
    def bag_of_word(self, words):
        bag = {}
        for word in words:
            if word not in bag:
                bag[word] = 0
            bag[word] += 1
        return bag


    # [根据训练好的数据集，生成标签分配函数]---------------------------------------------------------------------------------------
    def fit(self, train_set, train_labels):
        # 参数说明
        # label_count [label]               标签钟类
        # 
        # label_word_count [label][words]   标签下 所有词包中 该单词出现数量!!!
        # {1: {'abbott': 2, 'farnham': 2, 'e': 1, 'limited': 3, 'british': 3, 'coachbuilding': 1, 'business': 9, 'based': 10, 'surrey': 1
        #      'trading': 3, 'name': 2, '1929': 2, 'major': 2, 'part': 2, 'output': 1, 'subcontract': 1, 'motor': 1, 'vehicle': 1, 'manufacturers': 1, ...}...}
        
        # 计算 标签数量
        label_count = Counter(train_labels)

        # 生成 训练集 word_vocab 单词库
        for words in train_set:
            for word in words:
                self.word_vocab[word] += 1
        self.word_vocab_types = len(self.word_vocab) # 24906

        # 计算 标签下 单词数量，会出现0
        for words, label in zip(train_set, train_labels):
            word_count = Counter(words)
            # 计算 24906 所有词在 class1 中出现的次数 [计算时间需要3-4min]
            # for word in self.word_vocab:
            #     self.word_count_in_label[label][word] += word_count[word]

            # 计算 仅仅在 class1 中出现的次数 [计算时间非常快]
            for word, count in word_count.items():
                self.word_count_in_label[label][word] += count

        # 计算先验概率和单词概率
        # Calculate prior probabilities and word likelihoods
        total_docs = len(train_set) # 长度 (有多少个标签 = 有多少个词包)

        # P(label)       嵌入 计算14个标签出现概率 
        self.label_prob = {label: count / total_docs for label, count in label_count.items()} 
        
        # P(word|label)  嵌入 计算14个标签下单词出现条件概率 
        for label, words in self.word_count_in_label.items():
            total_count = sum(words.values())                                                             # 某label下 总单词数               
            self.word_prob_in_label[label] = {word: (count + 1) / (total_count + self.word_vocab_types)   # 某label下 某单词出现的概率
                                      for word, count in words.items()}                                   # Laplace smoothing 拉普拉斯平滑(对于没见过的词)




    # [由训练集搞出来的Fit函数，对测试集进行标签预测]-----------------------------------------------------------------------
    def predict(self, dev_words_set, dev_labels, lambda_mix=0.0):
        
        predicted_label_list = []
        correct_predictions = 0
    
        # -------------------------------------------------------------------------------------------------------------
        for words in dev_words_set: # 一组词
            
            # 单词数量 词包
            word_count_dev = self.bag_of_word(words)

            # 调用本身属性 计算每个标签的概率
            # 对数相加 = 内部相乘 (对数比较巧妙)
            # log(P(label))
            label_log_probs = {label: math.log(self.label_prob[label]) for label in self.label_prob}  

            # 计算 每个label 有多少单词数 没有出现在 self.word_count_in_label
            word_count_unseen = OrderedDict((i, defaultdict(int)) for i in range(1, 15))

            for label in label_log_probs.keys():
                word_count_unseen[label] = {}
                for word, word_count in word_count_dev.items():
                    if word not in self.word_count_in_label[label]:
                        word_count_unseen[label][word] = word_count

            # 这里存在较大问题!!!!
            # 对 word_count_dev [每种]单词分析
            for word, word_count in word_count_dev.items():
                for label in label_log_probs:

                    # 如果 label 中有该单词
                    if word in self.word_prob_in_label[label]:
                        label_log_probs[label] += word_count_dev[word] * math.log(self.word_prob_in_label[label][word])
                    
                    # 如果 label 中无该单词 [主要是这里的逻辑！！！！！！！]
                    else:                        # label1 中的总单词数                             # 24906 词库总数
                        prob_unseen = (0 + 1) / (sum(self.word_count_in_label[label].values()) + self.word_vocab_types)
                        label_log_probs[label] += word_count_dev[word] * math.log(prob_unseen) 

        # 计算预测的 Predicted_Label
        # 用于和 dev_labels 进行比较，计算准确率

            # 使用 MAP 进行贝叶斯分类 
            predicted_label = max(label_log_probs, key=label_log_probs.get)  
            predicted_label_list.append(predicted_label)

            # 计算正确率
            if predicted_label == dev_labels[predicted_label_list.index(predicted_label)]:
                correct_predictions += 1
        # -------------------------------------------------------------------------------------------------------------



        accuracy = correct_predictions / len(dev_words_set)
        return accuracy, predicted_label_list

