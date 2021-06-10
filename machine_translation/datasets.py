import jieba
from utils import *


SOS_token = 0
EOS_token = 1
MAX_LENGTH = 10

class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {
            0: 'SOS', 1: 'EOS'
        }
        self.n_words = 2

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

    def addSentence(self, sentence):
        for word in sentence.split(" "):
            self.addWord(word)


def readLangs(lang1, lang2, path):
    lines = open(path, encoding='utf8').readlines()

    lang1_cls = Lang(lang1)
    lang2_cls = Lang(lang2)

    pairs = []
    for l in lines:
        l = l.split('\t')
        setence1 = normalizeString(l[0])
        setence2 = cht_to_chs(l[1])
        seg_list = jieba.cut(setence2, cut_all=False)
        setence2 = ' '.join(seg_list)

        if len(setence1.split(' ')) > MAX_LENGTH:
            continue
        if len(setence2.split(' ')) > MAX_LENGTH:
            continue

        pairs.append([setence1, setence2])
        lang1_cls.addSentence(setence1)
        lang2_cls.addSentence(setence2)

    return lang1_cls, lang2_cls, pairs


if __name__ == '__main__':

    lang1 = 'en'
    lang2 = 'cn'
    path = 'data/en-cn.txt'
    lang1_cls, lang2_cls, pairs = readLangs(lang1, lang2, path)

    print(len(pairs))
    print(lang1_cls.n_words)
    print(lang1_cls.index2word)

    print(lang2_cls.n_words)
    print(lang2_cls.index2word)
