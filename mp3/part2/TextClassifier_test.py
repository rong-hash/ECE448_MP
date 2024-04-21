import math

class TextClassifier(object):
    def __init__(self):
        self.lambda_mixture = 0.5
        self.prior = {}
        self.word_probs = {}
    
    def fit(self, train_set, train_labels):
        label_count = {}
        word_count = {}
        
        # 计算每个类别的频率和每个类别的单词频率
        # Count the frequency of each class and word frequency per class
        for words, label in zip(train_set, train_labels):
            if label not in label_count:
                label_count[label] = 0
                word_count[label] = {}
            label_count[label] += 1
            for word in words:
                if word not in word_count[label]:
                    word_count[label][word] = 0
                word_count[label][word] += 1

        # 计算先验概率和单词概率
        # Calculate prior probabilities and word likelihoods
        total_docs = len(train_set)
        self.prior = {label: count / total_docs for label, count in label_count.items()}
        
        self.word_probs = {}
        for label, words in word_count.items():
            total_count = sum(words.values())
            self.word_probs[label] = {word: (count + 1) / (total_count + len(words))
                                      for word, count in words.items()}  # Laplace smoothing 拉普拉斯平滑(对于没见过的词)

    def predict(self, dev_set, dev_labels):
        results = []
        correct_predictions = 0
        
        for words in dev_set:
            log_probs = {label: math.log(self.prior[label]) for label in self.prior}  # Start with the log of the prior probabilities
            for word in words:
                for label in log_probs:
                    if word in self.word_probs[label]:
                        log_probs[label] += math.log(self.word_probs[label][word])
                    else:
                        # If the word wasn't seen in the training set, ignore or use a very small probability
                        log_probs[label] += math.log(1e-6)
            
            predicted_label = max(log_probs, key=log_probs.get)  # Choose the label with the highest log probability
            results.append(predicted_label)
            if predicted_label == dev_labels[results.index(predicted_label)]:
                correct_predictions += 1
        
        accuracy = correct_predictions / len(dev_set)
        return accuracy, results

