# encoding: utf-8
import codecs
import os
import re
import chardet

def get_encoding(file):

    with open(file, 'rb') as f:
        data = f.read()
        if chardet.detect(data)['encoding'] == 'GB2312':
            return 'gbk'
        return chardet.detect(data)['encoding']

def character_tagging(input_file, output_file):
    input_data = codecs.open(input_file, 'r', get_encoding(input_file))
    output_data = codecs.open(output_file, 'w', "utf-8")
    for line in input_data.readlines():
        # 移除字符串的头和尾的空格。strip()方法默认是移除空格的
        word_list = line.strip().split()
        for word in word_list[1:]:
            words = word.split("/")
            word = words[0]
            output_data.write(word + " "),
        output_data.write("\n")
    input_data.close()
    output_data.close()

punc = r"""！？｡＂＃＄％＆＇《》（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥·"""
def Modify(s):
    if s[-1] in (r"[%s]+"%punc):
        s = s[:-1]
    if s[0] in (r"[%s]+" %punc):
        s = s[1:]

    s_modify1 = re.sub(r"[%s]+"%punc, " EOS BOS ", s)   ## r'\w+'为正则表达式，匹配多个英文单词或者数字
    s_modify1="BOS "+s_modify1+" EOS"
    s_modify3 = ""
    s_modify1_list = s_modify1.split()
    flag = 0
    for i in range(len(s_modify1_list)):
        if (s_modify1_list[i] == "BOS" and s_modify1_list[i+1] == "EOS") or  flag :
            if(flag == 0):
                flag = 1
            else :
                flag = 0
        else :
            s_modify3 = s_modify3 + s_modify1_list[i] + " "

    return s_modify3
def NewModify(s):
    if s[-1] in (r"[%s]+"%punc):
        s = s[:-1]
    if s[0] in (r"[%s]+" %punc):
        s = s[1:]

    s_modify1 = re.sub(r"[%s]+"%punc, " ", s)   ## r'\w+'为正则表达式，匹配多个英文单词或者数字
    return s_modify1
def get_data(input_file,output_file):
    temp_file = "NeeskyMaxtempLPicFca.txt"
    character_tagging(input_file, temp_file)

    input_data = codecs.open(temp_file, 'r', get_encoding(temp_file))
    output_data = codecs.open(output_file, 'w', 'utf-8')

    for line in input_data.readlines():
        #output_data.write(Modify(line))
        output_data.write(NewModify(line))
    input_data.close()
    output_data.close()
    os.remove(temp_file)
if __name__ == "__main__":
    get_data("data.txt","out.txt")