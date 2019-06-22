#머신러닝에 필요한 모듈 import
from collections import defaultdict
from pandas import read_table
import numpy as np
import math
import re
import nltk
from nltk.corpus import stopwords

#나이브 베이지 모델 
class NaiveBayesClassifier:

    #모델이 생성될 때 처음 시작되는 함수
    def __init__(self, k=0.5):
        self.k = k
        self.word_probs = []

    #학습데이터를 불러오는 np.array로 만드는 함수
    def load_corpus(self, path):
        corpus = read_table(path, sep=',', encoding='utf-8')
        corpus = np.array(corpus)
        return corpus

    def count_words(self, training_set):
        # 학습데이터의 본문(doc), 평점(point)으로 구성
        counts = defaultdict(lambda : [0, 0])
        for doc, point in training_set:
            # 본문이 text일 때만 카운트
            if self.isNumber(doc) is False:
                # 본문을 띄어쓰기 단위로 토크나이징
                # 데이터 전처리 과정 http:// 링크 삭제, 불필요한 단어(be동사, the, with 등) 전부 삭제
                doc = doc.lower()
                doc = re.sub('https?://\S+','',doc)
                words = doc.split()
                words = [w for w in words if not w in stopwords.words('english')]
                for word in words:
                    counts[word][0 if point > 3.5 else 1] += 1
        return counts

    def isNumber(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def word_probabilities(self, counts, total_class0, total_class1, k):
        # 단어의 빈도수를 [단어, p(w|호재), p(w|악재)] 형태로 반환
        return [(w,
                 (class0 + k) / (total_class0 + 2*k),
                 (class1 + k) / (total_class1 + 2*k))
                for w, (class0, class1) in counts.items()]

    def class0_probability(self, word_probs, doc):
        # 별도 토크나이즈 안하고 띄어쓰기로만
        # 데이터 전처리 추가
        docwords = doc.split()
        docwords = [w for w in docwords if not w in stopwords.words('english')]
        # 초기값은 모두 0으로 처리
        log_prob_if_class0 = log_prob_if_class1 = 0.0

        # 모든 단어에 대해 반복
        for word, prob_if_class0, prob_if_class1 in word_probs:
            # 만약 학습을 통해 얻은 word가 나타나면
            # 해당 단어가 나올 log 확률을 더해 줌
            if word in docwords:
                log_prob_if_class0 += math.log(prob_if_class0)
                log_prob_if_class1 += math.log(prob_if_class1)

            # 만약 학습을 통해 얻은 word가 나타나지 않는다면
            # 해당 단어가 나오지 않을 log 확률을 더해 줌
            # 나오지 않을 확률은 log(1-나올 확률)로 계산
            else:
                log_prob_if_class0 += math.log(1.0 - prob_if_class0)
                log_prob_if_class1 += math.log(1.0 - prob_if_class1)

        prob_if_class0 = math.exp(log_prob_if_class0)
        prob_if_class1 = math.exp(log_prob_if_class1)
        return prob_if_class0 / (prob_if_class0 + prob_if_class1)

    def train(self, trainfile_path):
        training_set = self.load_corpus(trainfile_path)

        # 범주0(호재)과 범주1(악재) 문서 수를 세어 줌
        num_class0 = len([1 for _, point in training_set if point > 3.5])
        num_class1 = len(training_set) - num_class0
        
        # train
        word_counts = self.count_words(training_set)
        self.word_probs = self.word_probabilities(word_counts,
                                                  num_class0,
                                                  num_class1,
                                                  self.k)

    def classify(self, doc):
        return self.class0_probability(self.word_probs, doc)

model = NaiveBayesClassifier()
model.train(trainfile_path='test.csv')