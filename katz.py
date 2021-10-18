import numpy as np
no_word_p = 1e-10
def C_(num,N):
    return (num+1) * N[num + 1] / N[num]
def A(num,N):
    return (num + 1) * N[num + 1] / N[1]
def faz(numword12,numword1,gtmax,N):
    if (numword12 >= gtmax):
        return numword12 / numword1
    else:
        return numword12 / numword1 * (C_(numword12, N) / numword12 - A(gtmax, N)) / (1 - A(gtmax, N))

def predicted(word1,word2, CoreDictionary, CoreBiGramTableDictionary,mList,NoBostot,NoBosEostot,N,gtmax = 10):
    numword12 = CoreBiGramTableDictionary.getBiFrequency(word1,word2)
    numword1 = CoreDictionary.getTermFrequency(word1)
    if(numword12 == 0):
        if(CoreDictionary.getTermFrequency(word2)==0 or CoreDictionary.getTermFrequency(word2)==0):
            return no_word_p
        z1sumup = 0
        z1sumdown = 0
        for word in mList :
            tempnumword12 = CoreBiGramTableDictionary.getBiFrequency(word1,word)
            if(tempnumword12 > 0) :
                z1sumup += faz(tempnumword12,numword1,gtmax,N)
                z1sumdown += CoreDictionary.getTermFrequency(word) / NoBostot
        return (1-z1sumup)/(1-z1sumdown) * CoreDictionary.getTermFrequency(word2) / NoBosEostot
    else :
        return faz(numword12,numword1,gtmax,N)


