from pyhanlp import *
import data
import splitword
import argparse
import katz
import numpy as np
def statistical_single_word(corpus_path, output_path):
    """
    统计语料库中的单个单词的词频
    :param corpus_path: 语料库路径
    :param output_path: 输出保存单个单词词频的路径
    :return:
    """
    # 通过 SafeJClass 取得 HanLP 中的 CorpusLoader 类
    CorpusLoader = SafeJClass('com.hankcs.hanlp.corpus.document.CorpusLoader')
    # 通过 SafeJClass 取得 HanLP 中的 NatureDictionaryMaker 类
    NatureDictionaryMaker = SafeJClass('com.hankcs.hanlp.corpus.dictionary.NatureDictionaryMaker')
    sents = CorpusLoader.convert2SentenceList(corpus_path)
    for sent in sents:
        for word in sent:
            word.setLabel("n")
    maker = NatureDictionaryMaker()  # 创建对象
    maker.compute(sents)  # 处理预料
    maker.saveTxtTo(output_path)  # 保存文件到 output_path 路径下
def get_all(file,whos):
    mList = []
    import codecs
    input_data = codecs.open(file, 'r', data.get_encoding(file))
    for line in input_data.readlines():
        if(whos==0):
            mList.append(line.split()[whos])
        else :
            mList.append(eval(line.split()[whos]))
    input_data.close()
    return mList
def get_prepared(st,ed,in_path = "data.txt",out_path = "Neesky_data"):
    temp_path = "NeeskyMaxtempLPicFca2.txt"
    if os.path.isfile(out_path+".txt")==0 and os.path.isfile(temp_path)==0:
        data.get_data(in_path, temp_path)
    if os.path.isfile(out_path+".txt")==0:
        statistical_single_word(temp_path, out_path)
    HanLP.Config.CoreDictionaryPath =  out_path + ".txt"  # 一元语法模型路径
    HanLP.Config.BiGramDictionaryPath = out_path + ".ngram.txt"  # 二元语法模型路径
    CoreDictionary = LazyLoadingJClass("com.hankcs.hanlp.dictionary.CoreDictionary")  # 加载一元语法模型Java模块
    CoreBiGramTableDictionary = SafeJClass("com.hankcs.hanlp.dictionary.CoreBiGramTableDictionary")  # 加载二元语法模型Java模块
    mList = get_all(out_path+".txt",0)
    mmnumList = get_all(out_path + ".ngram.txt",1)
    NoBostot=0
    NoBosEostot=0
    maxtot = 0
    for word in mList:
        tempnumword = CoreDictionary.getTermFrequency(word)
        maxtot = max(maxtot,tempnumword)
        if(word != st):
            NoBostot += tempnumword
            if(word!=ed):
                NoBosEostot += tempnumword
    N = np.zeros([maxtot+1],dtype=np.int32)
    for num in mmnumList:

        N[num] = N[num] + 1
    if os.path.isfile(temp_path) :
        os.remove(temp_path)
    return CoreDictionary,CoreBiGramTableDictionary,mList,NoBostot,NoBosEostot,N

# temptot = 0
def checkpro(splitsentence,CoreDictionary,CoreBiGramTableDictionary,mList,NoBostot,NoBosEostot,N,type):

    p = 1.0
    for i in range(len(splitsentence)-1):
        if(type == "katz"):
            p = p * katz.predicted(splitsentence[i],splitsentence[i+1], CoreDictionary, CoreBiGramTableDictionary,mList,NoBostot,NoBosEostot,N,gtmax = 10)
        else:
            p = p * (1.0 * (CoreBiGramTableDictionary.getBiFrequency(splitsentence[i], splitsentence[i + 1]) + 1) / (
                        CoreDictionary.getTermFrequency(splitsentence[i]) + 1))
    # global temptot
    # temptot = temptot + 1
    # print(temptot)
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
def max_prob(words,CoreDictionary,CoreBiGramTableDictionary,st,ed,mList,NoBostot,NoBosEostot,N,type):
    pc = perm(words[1:-1])

    for i in range(len(pc)):
        pc[i].insert(0,st)
        pc[i].insert(len(pc[i]),ed)
    # print(len(pc))
    p, w = max((checkpro(s,CoreDictionary,CoreBiGramTableDictionary,mList,NoBostot,NoBosEostot,N,type), s) for s in pc)
    return p, ''.join(w)
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--origin_data_file', type=str,
                        help='file where to load data.', default='data.txt')
    parser.add_argument('--modified_data_file', type=str,
                        help='file where to put modified_data.', default='Neesky_data')
    parser.add_argument('--sentence', type=str,
                        help='Sentence to be predicted.', default='香港各界举行活动喜庆元旦')
    parser.add_argument('--type', type=str,
                        help='Sentence to be predicted.', default='katz')
    return parser.parse_args(argv)
def main(args):
    st = "始##始"
    ed = "末##末"
    type = args.type
    splitsentence = splitword.get_splitsentence(args.sentence, "始##始", "末##末")
    CoreDictionary, CoreBiGramTableDictionary, mList,NoBostot,NoBosEostot,N = get_prepared(st,ed,args.origin_data_file,args.modified_data_file)

    print("待预测语句：",args.sentence)
    print("分词后的语句：",splitsentence)
    bestp,beststr = max_prob(splitsentence, CoreDictionary, CoreBiGramTableDictionary, st, ed,mList,NoBostot,NoBosEostot,N,type)
    print("最佳排列语句：",beststr,",该语句概率为",bestp)
    print("原语句：",args.sentence,",该语句概率为",checkpro(splitsentence, CoreDictionary, CoreBiGramTableDictionary,mList, NoBostot,NoBosEostot,N,type))

if __name__ == '__main__':
	main(parse_arguments(sys.argv[1:]))