import pandas as pd
import re
import jieba
import matplotlib.pyplot as plt

filepath = '../data_train/'
filename = '688001_train.csv'

def load_data(file):
    data = pd.read_csv(file)
    print('加载数据...')
    return data

# 对每行数据进行去非汉字，分词

# 去掉文本中不是汉字的内容
def clean(data, stock):
    # 对’评论和新闻‘去重
    # print('去重前大小：{}'.format(data.shape))
    # # print(data[190:200])
    # data = data.drop_duplicates(subset=['标题'], keep='first')
    # # data = data.reset_index() # 去重之后，索引未变话，不是连续，需要重置索引
    # print('去重后大小：{}'.format(data.shape))
    # # print(data[190:200])
    print('清洗数据...')
    data['stock'] = stock
    news_list = data['标题'].tolist()

    for i in range(0, len(news_list)):
        try:
            news = news_list[i]
            new = re.sub('\[.*\]', '', news) # 去掉表示表情的文字[xxx]
            # new = re.sub('[^\u4e00-\u9fa5]+', '', news)
            news_list[i] = new
            print('第{}条数据处理成功'.format(i))
        except Exception as err:
            print('第{}条数据处理失败，内容：{}，原因：{}'.format(i, news, err))
    return data



def load_stopword():
    stopword_file = '../all_data_preprocess/info/stopwords-master/cn_stopwords_khan.txt'
    f_stop = open(stopword_file, encoding='utf-8')  # 自己的中文停用词表
    sw = [line.strip() for line in f_stop]  # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
    f_stop.close()
    return sw



def separate_words(data, stock):

    data_cleaned = clean(data, stock)

    print('分词...')
    all_data_separated_list = []
    all_data_list = data_cleaned['标题'].tolist()

    user_dict = '../all_data_preprocess/info/user_dict.txt'  # 自定义的词典
    jieba.load_userdict(user_dict)
    stopwords = load_stopword()

    for i in range(len(all_data_list)):
        try:
            sentence_separated_list = jieba.cut(all_data_list[i])
            outstr = ''
            for word in sentence_separated_list:
                if word not in stopwords:
                    if word != '/t':
                        outstr += word
                        outstr += " "
            # outstr = outstr.strip()  # 去除两边空格
            outstr = re.sub('[^\u4e00-\u9fa5]+', ' ', outstr)
            outstr = outstr.strip()  # 去除两边空格
            all_data_separated_list.append(outstr)
            print('第 {} 条数据处理成功！'.format(i))
        except Exception as e:
            # print('Thread-{}, 第 {} 条数据处理失败！原因：{}'.format(name, i, str(e)))
            print('第 {} 条数据处理失败！原因：{}'.format(i, str(e)))
            all_data_separated_list.append([''])
    # print(all_data_separated_list)
    data_cleaned['separated'] = all_data_separated_list
    return data_cleaned


def analyse_word_num(data):
    data_num_train = len(data)  # 数据条数
    word_num = 0  # 总词数
    single_num = []  # 每条数据的长度的大小数组
    ave_num = 0  # 平均每条数据的词数大小

    for i in range(len(data)):
        try:

            sentence = data.iloc[i]['separated']
            single_num.append(len(sentence.split(' ')))
            word_num += len(sentence.split(' '))
        except Exception as ex:
            print('{}，{}出错了！'.format(i, sentence))
    ave_num = word_num / data_num_train
    print('全部数据词总数为：', word_num, '; 每条数据的平均词数为：', ave_num)
    print(single_num)
    plt.hist(single_num, bins=100)
    plt.xlabel('Sequence Length')
    plt.ylabel('Frequency')
    plt.axis([0, 50, 0, 1000])
    plt.show()




if __name__ == '__main__':
    file = filepath + filename

    data = load_data(file)
    data_separated = separate_words(data, '688001')
    print(data_separated)
    data_separated.to_csv(filepath+'separated_'+filename, encoding='utf-8')



    data = load_data(filepath+'separated_'+filename)
    print(type(data['separated']))
    print(len(data['separated']))
    print(data)
    data.dropna(axis=0, subset=['separated'], inplace=True) # 将'separated'为空的行删除
    print(data)
    print(data.iloc[0]['separated'])
    print(data.iloc[0]['separated'].split(' '))
    print(len(data.iloc[0]['separated'].split(' ')))
    analyse_word_num(data)
    # 由图看出 每句话最多20，选择用20维作为句子的维度

