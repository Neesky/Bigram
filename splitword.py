def get_splitsentence(sentence):
    import jieba.posseg as pseg
    import jieba
    jieba.enable_paddle() #启动paddle模式。 0.40版之后开始支持，早期版本不支持
    words = pseg.cut(sentence,use_paddle=True) #paddle模式
    splitword = ["BOS"]
    for word, flag in words:
        splitword.append(word)
    splitword.append("EOS")
    return splitword