from collections import Counter
import numpy as np
import data
import codecs
import splitword
import argparse
import sys
maxnum = 10000



def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--origin_data_file', type=str,
                        help='file where to load data.', default='data.txt')
    parser.add_argument('--modified_data_file', type=str,
                        help='file where to put modified_data.', default='out.txt')
    parser.add_argument('--sentence', type=str,
                        help='Sentence to be predicted.', default='我和我的祖国')
    return parser.parse_args(argv)



def prepared(args):
    data.get_data(args.origin_data_file, args.modified_data_file)
    input_data = codecs.open(args.modified_data_file, 'r', data.get_encoding(args.modified_data_file))
    counter = Counter()  # 词频统计
    read_data_line = input_data.readlines()
    input_data.close()
    for sentence in read_data_line:
        sentence = sentence.split()
        for word in sentence:
            counter[word] += 1
    counter = counter.most_common(maxnum)
    lec = len(counter)

    word2id = {counter[i][0]: i for i in range(lec)}
    id2word = {i: w for w, i in word2id.items()}

    """N-gram建模训练"""
    unigram = np.array([i[1] for i in counter]) / sum(i[1] for i in counter)

    bigram = np.zeros((lec, lec)) + 1

    for sentence in read_data_line:
        sentences = sentence.split()
        sentence = []
        for w in sentences:
            if(w in word2id.keys()):
                sentence.append(word2id[w])
        for i in range(1, len(sentence)):
            bigram[[sentence[i - 1]], [sentence[i]]] += 1
    for i in range(lec):
        bigram[i] /= bigram[i].sum()
    return word2id,id2word,unigram,bigram

def prob(sentence,word2id,unigram,bigram):
    s = [word2id[w] for w in sentence]
    les = len(s)
    if les < 1:
        return 0
    p = unigram[s[0]]
    if les < 2:
        return p
    for i in range(1, les):
        p *= bigram[s[i - 1], s[i]]
    return p


def perm(data):
    if len(data) == 1:  # 和阶乘一样，需要有个结束条件
        return [data]
    r = []
    for i in range(len(data)):
        s = data[:i] + data[i + 1:]  # 去掉第i个元素，进行下一次的递归
        p = perm(s)
        for x in p:
            r.append(data[i:i + 1] + x)  # 一直进行累加
    return r


def max_prob(words,word2id,unigram,bigram):
    pc = perm(words[1:-1])

    for i in range(len(pc)):
        pc[i].insert(0,"BOS")
        pc[i].insert(len(pc[i]),"EOS")
    p, w = max((prob(s,word2id,unigram,bigram), s) for s in pc)
    return p, ''.join(w)
def main(args):
    word2id,id2word,unigram,bigram = prepared(args)
    splitsentence = splitword.get_splitsentence(args.sentence)
    print("待预测语句：",args.sentence)
    print("分词后的语句：",splitsentence)
    bestp,beststr = max_prob(splitsentence,word2id,unigram,bigram)
    print("最佳排列语句：",beststr,",该语句概率为",bestp)
    print("原语句：",args.sentence,",该语句概率为",prob(splitsentence,word2id,unigram,bigram))
if __name__ == '__main__':
	main(parse_arguments(sys.argv[1:]))