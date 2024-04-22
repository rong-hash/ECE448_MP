import math

class TextClassifier(object):
    def __init__(self):
        self.lambda_mixture = 0.5
        self.prior = {}
        self.word_probs = {}

    
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
        label_count = {}
        word_count  = {}
        # 参数说明
        # label_count [label]         标签钟类
        # 
        #
        # word_count [label][words]   标签下 所有词包中 该单词出现数量!!!
        # {1: {'abbott': 2, 'farnham': 2, 'e': 1, 'limited': 3, 'british': 3, 'coachbuilding': 1, 'business': 9, 'based': 10, 'surrey': 1
        #      'trading': 3, 'name': 2, '1929': 2, 'major': 2, 'part': 2, 'output': 1, 'subcontract': 1, 'motor': 1, 'vehicle': 1, 'manufacturers': 1, ...}...}
        
        
        # 计算每个类别的频率和每个类别的单词频率
        # Count the frequency of each class and word frequency per class
        for words, label in zip(train_set, train_labels):

            # 计算 标签数量
            if label not in label_count:
                label_count[label] = 0
                word_count[label]  = {}
            label_count[label] += 1 # 标签数量 [但是我们只有14个标签！！！！！]


            # 计算 对应标签下 单词数量
            for word in words: 
                # 新单词
                if word not in word_count[label]: # label 1 下 word 1 出现的次数
                    word_count[label][word] = 0
                word_count[label][word] += 1

        # 计算先验概率和单词概率
        # Calculate prior probabilities and word likelihoods
        total_docs = len(train_set) # 长度 (有多少个标签 = 有多少个词包)

        # P(label)       嵌入 计算14个标签出现概率 
        self.prior = {label: count / total_docs for label, count in label_count.items()} 
        
        # P(word|label)  嵌入 计算14个标签下单词出现条件概率 
        self.word_probs = {}
        for label, words in word_count.items():
            total_count = sum(words.values())                                # 某label下 总单词数
            self.word_probs[label] = {word: (count) / (total_count)          # 某label下 某单词出现的概率
                                      for word, count in words.items()} 
            # self.word_probs[label] = {word: (count + 1) / (total_count + len(words))
            #                           for word, count in words.items()}  # Laplace smoothing 拉普拉斯平滑(对于没见过的词)




    # [由训练集搞出来的Fit函数，对测试集进行标签预测]-----------------------------------------------------------------------
    def predict(self, dev_words_set, dev_labels, lambda_mix=0.0):
        
        predicted_label_list = []
        correct_predictions = 0
        
        # # -------------------------------------------------------------------------------------------------------------
        # for words in dev_words_set: # 一组词
            
        #     # 调用本身属性 计算每个标签的概率
        #     label_log_probs = {label: math.log(self.prior[label]) for label in self.prior}  # Start with the log of the prior probabilities

        #     for word in words:
        #         for label in label_log_probs:
                    
        #             # 调用本身性质 P(word|label)
        #             if word in self.word_probs[label]:
        #                 label_log_probs[label] += math.log(self.word_probs[label][word])
                    
        #             # 没见过的单词
        #             else:
        #                 # If the word wasn't seen in the training set, ignore or use a very small probability
        #                 label_log_probs[label] += math.log(1e-6)
            
        # # 计算预测的 Predicted_Label
        # # 用于和 dev_labels 进行比较，计算准确率

        #     # 使用 MAP 进行分类 
        #     predicted_label = max(label_log_probs, key=label_log_probs.get)  # Choose the label with the highest log probability
        #     predicted_label_list.append(predicted_label)

        #     # 计算正确率
        #     if predicted_label == dev_labels[predicted_label_list.index(predicted_label)]:
        #         correct_predictions += 1
        # # -------------------------------------------------------------------------------------------------------------


        # -------------------------------------------------------------------------------------------------------------
        for words in dev_words_set: # 一组词
            
            word_number = self.bag_of_word(words)

            # 调用本身属性 计算每个标签的概率
            # 对数相加 = 内部相乘
            label_log_probs = {label: math.log(self.prior[label]) for label in self.prior}  

            for word in word_number:
                for label in label_log_probs:
                    
                    # 调用本身性质 P(word|label)
                    if word in self.word_probs[label]:
                        label_log_probs[label] += word_number[word] * math.log(self.word_probs[label][word])
                    
                    # 没见过的单词
                    else:
                        label_log_probs[label] += word_number[word] * math.log(1e-6) #这里肯定有问题


            # # -------------------------------------------------------------------------------------------------------------
            # # 调用本身属性 计算每个标签的概率
            # # 对数相加 = 内部相乘
            # for word in words:

            #     # 计算每个 label 下的 P(word1,word2,...wordn|label) 
            #     for label in label_log_probs:
                    
            #         # 调用本身性质 P(word|label)
            #         # 如果见过该单词
            #         if word in self.word_probs[label]:
            #             label_log_probs[label] += math.log(self.word_probs[label][word]) # 累乘 P(word n|label 1)，遇到相同 word n 会累乘
                    
            #         # 如果没见过的单词
            #         else:
            #             # If the word wasn't seen in the training set, ignore or use a very small probability
            #             label_log_probs[label] += math.log(1e-6)
            
        # 计算预测的 Predicted_Label
        # 用于和 dev_labels 进行比较，计算准确率

            # 使用 MAP 进行分类 
            predicted_label = max(label_log_probs, key=label_log_probs.get)  # Choose the label with the highest log probability
            predicted_label_list.append(predicted_label)

            # 计算正确率
            if predicted_label == dev_labels[predicted_label_list.index(predicted_label)]:
                correct_predictions += 1
        # -------------------------------------------------------------------------------------------------------------



        accuracy = correct_predictions / len(dev_words_set)
        return accuracy, predicted_label_list

