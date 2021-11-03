import os
import pandas as pd
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import gensim
import multiprocessing
import numpy as np


def train_w2v_model(data, outp1, outp2):

    # LineSentence(inp)：应该是把word2vec训练模型的磁盘存储文件（model在内存中总是不踏实）转换成所需要的格式；对应的格式是参考上面的例1。
    # size：是每个词的向量维度；
    # window：是词向量训练时的上下文扫描窗口大小，窗口为5就是考虑前5个词和后5个词；
    # min - count：设置最低频率，默认是5，如果一个词语在文档中出现的次数小于5，那么就会丢弃；
    # workers：是训练的进程数（需要更精准的解释，请指正），默认是当前运行机器的处理器核数。这些参数先记住就可以了。

    model = Word2Vec(LineSentence(data), vector_size=300, window=5, min_count=5, sg=1, hs=0,
                     workers=multiprocessing.cpu_count())
    # Word2Vec()

    # outp1 为输出模型
    model.save(outp1)

    # outp2为原始c版本word2vec的vector格式的模型
    model.wv.save_word2vec_format(outp2, binary=False)

    #保存成npz格式
    # np.save('word2vec.npz')
    print('train_w2v_model is finished')


if __name__ == '__main__':

    # file = '../all_data_preprocess/data/separated_words/2/all_data_separated.txt'
    # all_data_separated = pd.read_table(file, header=None)
    # print(all_data_separated)

    # 训练词向量
    # train_w2v_model(file, 'outModel', 'outVector')
    # 导入模型
    word2vec_model = Word2Vec.load('outModel')

    # 计算相似度
    # word_cos = word2vec_model.wv.similarity('融资', '万元')
    # print(word_cos)


    print(word2vec_model.wv.index_to_key) # 字典
    # print(word2vec_model.wv.key_to_index) # 字典和索引
    # print(word2vec_model.wv['融资'])

    # ss = np.load('outModel.wv.vectors.npy') # 50540*300
    # print(ss.shape)


