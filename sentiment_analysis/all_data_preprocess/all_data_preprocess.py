import os
import pandas as pd
import re
import jieba
import time
import random
import threading

re_patten = '[^\u4e00-\u9fa5]+' # 汉字的所有字符
re_patten = '\[.*\]' # 去除[]以及里面的内容
file_path = '../data/news/'


# 获取所有评论和新闻的文本数据,变成一个训练词向量的总文件
def aaa(file_path):

    files = os.listdir(file_path)
    all_data_list = []
    stock_list = []
    for index in range(0, len(files)):
        file_name = files[index]
        print('获取{}信息..'.format(file_name))
        try:
            data = pd.read_csv(file_path + file_name, encoding="utf-8")
            news_list = data['标题'].tolist() # 取文件‘标题’列，将serias 变成list
            stock = [file_name[0:6]] * len(news_list) # 将每条新闻后面带上stcokcode
            all_data_list.extend(news_list) # 不用append。因为append加起来是多个list，用extend，就是合并成一个list
            stock_list.extend(stock)
        except Exception as e:
            print('{} 获取信息失败！原因: {}'.format(file_name, str(e)))

    all_data = pd.DataFrame(all_data_list, columns=['评论和新闻'])
    all_data['stock'] = stock_list
    all_data.to_csv('all_data.csv', encoding='utf-8', index_label='index') # 加index= 0不要行索引
    print('生成全量文件成功！！！')

# 去掉表示表情的文字[xxx]
def bbb(filename, data):
    news_list = data['评论和新闻'].tolist()
    for i in range(0, len(news_list)):
        try:
            news = news_list[i]
            new = re.sub('\[.*\]', '', news)
            # new = re.sub('[^\u4e00-\u9fa5]+', '', news)
            news_list[i] = new
            # print('第{}条数据处理成功'.format(i))
            log_to_txt('./logs/quchong_{}.txt'.format(filename), '第 {} 条数据处理成功！'.format(i))
        except Exception as err:
            # print('第{}条数据处理失败，内容：{}，原因：{}'.format(i, news, err))
            log_to_txt('./logs/quchong_{}.txt'.format(filename), '第 {} 条数据处理失败！原因：{}'.format(i, str(err)))
    data.to_csv(filename + '_data_clear.csv', encoding='utf-8', index=0)
    return data


    # 加载停用词表
def load_stopword():
    stopword_file = './info/stopwords-master/cn_stopwords_khan.txt'
    f_stop = open(stopword_file, encoding='utf-8')  # 自己的中文停用词表
    sw = [line.strip() for line in f_stop]  # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
    f_stop.close()
    return sw


def separate_words(name, data):
    print('Current {} is processing...'.format(name))

    ## 去掉表示表情的文字[xxx]
    clean_data = bbb(name, data)
    # clean_data = pd.read_csv(name+'_data_clear.csv')

    all_data_list_seg = []
    all_data_list = clean_data['评论和新闻'].tolist()

    user_dict = './info/user_dict.txt'  # 自定义的词典
    jieba.load_userdict(user_dict)
    stopwords = load_stopword()
    for i in range(len(all_data_list)):
        try:
            sentence_separated = jieba.cut(all_data_list[i])
            outstr = ''
            for word in sentence_separated:
                if word not in stopwords:
                    if word != '/t':
                        outstr += word
                        outstr += " "

            outstr = re.sub('[^\u4e00-\u9fa5]+', ' ', outstr)
            outstr = outstr.strip()  # 去除两边空格
            all_data_list_seg.append([outstr])
            print('{} ,已完成第 {} 条数据处理'.format(name, i))
        except Exception as e:
            # print('Thread-{}, 第 {} 条数据处理失败！原因：{}'.format(name, i, str(e)))
            log_to_txt('{}_error.txt'.format(name), 'Thread-{}, 第 {} 条数据处理失败！原因：{}'.format(name, i, str(e)))

    # all_data_list_seg = all_data_list_seg(filter(None, all_data_list_seg)) # <有错误!> 分词、去除停用词，特殊字符后，会出现‘’情况，需要过滤
    write_to_file(name+'.txt', all_data_list_seg)
    print("Current  {} 分词及去停用词完成!".format(name))
    # return all_data_list_seg


# # 将分词结果汇总到一个文件中
def collect_data(file_path):
    files = os.listdir(file_path)
    all_data_list = []

    for index in range(0, len(files)):
        file_name = files[index]
        print(file_name)
        df_news = pd.read_table(file_path+file_name, header=None) #DataFrame
        df_news_list = df_news.iloc[:, 0].tolist()
        all_data_list.extend(df_news_list)
    return all_data_list


# 处理后写入文件
def write_to_file(file, data):
    with open(file, 'wb') as fs:
        for i in range(len(data)):
            fs.write(data[i].encode('utf-8'))
            fs.write('\n'.encode("utf-8"))


def log_to_txt(filename, res):
    with open(filename, 'a', newline='') as txtfile:
        txtfile.write(res + '\n')


if __name__ == '__main__':
    # ---------------0----------------
    # aaa(file_path)
    # ---------------1----------------
    # ss = pd.read_csv('all_data.csv', encoding='utf-8')
    # # 对’评论和新闻‘去重
    # print('去重前大小：{}'.format(ss.shape))
    # data = ss.drop_duplicates(subset=['评论和新闻'], keep='first')
    # data = data.reset_index()  # 去重之后，索引未变话，不是连续，需要重置索引
    # print('去重后大小：{}'.format(data.shape))
    # # print('-----------------------------------------')
    # zz = data

    # # zz = zz.dropna(axis=0)  # 将空行删除，不覆盖原来表格，需要重新赋值
    # zz.dropna(axis=0, inplace=True)  # 在原来的表格中删除
    # ---------------3-----------------
    # page = 70000
    # for i in range(1, 21):
    #     t = threading.Thread(target=separate_words, args=('Thread-'+str(i), zz[(i-1)*page: i*page]))
    #     t.start()
    # last = threading.Thread(target=separate_words, args=('Thread-21', zz[page*20:len(zz)+1]))
    # last.start()
    # print('Main Thread')

    # ---------------4---------------------
    file_path = './data/separated_words/2/'
    all_train_data = collect_data(file_path)
    print(all_train_data)
    write_to_file(file_path+'all_data_separated.txt', all_train_data)
    print('collect data is finished!')


