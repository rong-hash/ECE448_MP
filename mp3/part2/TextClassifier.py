# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019

import math
from collections import Counter, defaultdict, OrderedDict # 方便数据处理

class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        self.lambda_mixture = 0.5

        self.label_prob          = {}
        self.word_vocab_types    = 0
        self.word_vocab          = defaultdict(int)                                              # 训练集 单词库

        self.word_count_in_label = OrderedDict((i, defaultdict(int)) for i in range(1, 15))      # 训练集 指定标签下的 单词数量，会出现0
        self.word_prob_in_label  = OrderedDict((i, defaultdict(int)) for i in range(1, 15))      
        

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
        # self.word_count_in_label          标签下 所有词包中 该单词出现数量!!!
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
        if lambda_mix != 0.0:
            return self.predict_extra(x_set, dev_label, lambda_mix)
        predicted_label_list = []
        correct_predictions = 0
    
        # -------------------------------------------------------------------------------------------------------------
        for words in dev_words_set: # 一组词
            
            # 单词数量 词包
            word_count_dev = self.bag_of_word(words)

            # 复制 self 属性 计算每个标签的概率
            # 每次循环会刷新
            # 对数相加 = 内部相乘 (对数比较巧妙)
            # log(P(label))
            label_log_probs = {label: math.log(self.label_prob[label]) for label in self.label_prob}  
            # label_log_probs = {label: 0                               for label in self.label_prob}  # Part 2.4 要求去掉 P(label)

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
                    
                    # 直接在 P(label) 的基础上进行对数相加
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
    def predict_extra(self, x_set, dev_label,lambda_mix):
        accuracy = 0.0

        result = []
        accurate_cnt = 0
        total_dev = len(dev_label)
        lap_sum = len(self.allwords)
                        
        for i in range(total_dev):
            tmp_x = x_set[i]
            tmp_lab = dev_label[i]
            tmp_sum = self.label_log.copy()
            tmp_sum_ec = self.label_log.copy()
            weighted_sum = [0] * 15
            weighted_sum[0] = float("-inf")

            tot1=0.0
            tot2=0.0
            for j in range(1, 15):
                for word in tmp_x:
                    if word not in self.allwords:
                        continue
                    if word in self.word_cnt[j]:
                        tmp_sum[j] += math.log((self.word_cnt[j][word] + 1) / (self.words_label[j] + lap_sum))
                    else:
                        tmp_sum[j] += math.log(1 / (self.words_label[j] + lap_sum))
                
                for k in range(len(tmp_x) - 1):
                    if (tmp_x[k], tmp_x[k+1]) not in self.allbiwords:
                        tmp_sum_ec[j] += math.log(1/100000)
                        continue
                    if tmp_x[k] not in self.bi:
                        tmp_sum_ec[j] += math.log(1/100000)
                        continue
                    if (tmp_x[k], tmp_x[k+1]) in self.word_cnt_ec[j].keys():
                        tmp_sum_ec[j] += math.log((self.word_cnt_ec[j][(tmp_x[k], tmp_x[k+1])] + 1) / (self.word_cnt[j][tmp_x[k]] + self.bi[tmp_x[k]]))
                    else:
                        if tmp_x[k] in self.word_cnt[j]:
                            tmp_sum_ec[j] += math.log(1 / (self.word_cnt[j][tmp_x[k]] + self.bi[tmp_x[k]]))
                        else:
                            tmp_sum_ec[j] += math.log(1 / (self.bi[tmp_x[k]]))

                
                if tmp_x[0] in self.word_cnt[j]:
                    tmp_sum_ec[j] += math.log(self.word_cnt[j][tmp_x[0]] / self.words_label[j] + lap_sum)
                else:
                    tmp_sum_ec[j] += math.log(1 / self.words_label[j] + lap_sum)
                
                tmp_sum[j] = math.exp(tmp_sum[j])
                tmp_sum_ec[j] = math.exp(tmp_sum_ec[j])
                tot1 += tmp_sum[j]
                tot2 += tmp_sum_ec[j]
            
            for j in range(1, 15):
                tmp_sum[j] = tmp_sum[j] / tot1
                tmp_sum_ec[j] = tmp_sum_ec[j] / tot2
                weighted_sum[j] = (1-lambda_mix) * (tmp_sum[j]) + lambda_mix * (tmp_sum_ec[j])
                
            inf_label = weighted_sum.index(max(weighted_sum))
            ec_label = tmp_sum_ec.index(max(tmp_sum_ec))

            result.append(inf_label)
            if inf_label == tmp_lab:
                accurate_cnt += 1

        accuracy = accurate_cnt / total_dev
        #print('lambda is ',lambda_mix, 'accuracy is ',accuracy,'count are ',accurate_cnt, total_dev)
        return accuracy, result
