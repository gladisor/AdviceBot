import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import itertools
import pickle

data = pd.read_csv('data.csv')

class Vocab:
    def __init__(self, tokens):
        self.vocab = Counter(tokens)

    @staticmethod
    def tokenize(text):
        return str(text).split()

    def encode(self, tokens):
        return [self.vocab[token] for token in tokens]

data['q_tokens'] = data['question'].apply(Vocab.tokenize)
data['q_len'] = data['q_tokens'].apply(len)

data['c_tokens'] = data['comment'].apply(Vocab.tokenize)
data['c_len'] = data['c_tokens'].apply(len)

cutoff = 200
data = data[data['c_len'] <= cutoff]
data = data[data['q_len'] <= cutoff]

q_tokens = data['q_tokens'].tolist()
c_tokens = data['c_tokens'].tolist()

tokens = itertools.chain(*q_tokens, *c_tokens)

vocab = Vocab(tokens)

data['q_encoded'] = data['q_tokens'].apply(Vocab.encode)

print(data['q_encoded'])
