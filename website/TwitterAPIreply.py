from itertools import count
from pickle import APPEND
from tkinter.tix import TCL_WINDOW_EVENTS
from unittest import result
import tweepy
import pandas as pd
import numpy as np
import re
import MeCab
import csv

def remove_text(text):
        text = re.sub(r'@[A-Za-z0-9]+','',text)
        text = re.sub(r'#','',text)
        text = re.sub(r'https?:\/\/\S+','',text)
        text = re.sub(r'RT[\s]+','',text)
        text = re.sub(r'\n','',text)
        text = re.sub(r':','',text)

        return text

def Twitter(username,searchcount):
    pd.set_option('display.unicode.east_asian_width', True)

    #APIの認証に必要なkey
    CONSUMER_KEY = 'VlTaFaokNGlVpzMT2GZcAGl1g'
    CONSUMER_SECRET = 'MLw5awDlHhZr0MqZl0wzH9U5TdCCnf5fvz3rTWnhimyBUIgYfz'
    ACCESS_TOKEN = '1546527343577288704-OqDrkKzpGtlZnTeCWA04aROaAAZU9S'
    ACCESS_SECRET = 'KAW4zttngehyn6lIXlwhuapleNmMnazJkGvZNj2gn6Ew8'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    search_name = 'to:',username                   
    replies = api.search_tweets(search_name,
        tweet_mode = 'extended',
        result_type='mixed',
        count=searchcount,
        lang = 'ja'
            )

    #データフレームの箱を設定
    df = pd.DataFrame([tweet.full_text for tweet in replies],columns=['Tweets'])

    #いらない文章を削除
    df['Tweets'] = df['Tweets'].apply(remove_text)

    # print(df['Tweets'])
    #APIで集めたデータを形態素解析

    mecab = MeCab.Tagger('-Owakati')
    df1 = []

    for word_tweets in df['Tweets']:
        temp = pd.DataFrame(columns=['word'])
        con = mecab.parse(word_tweets)
        lines = con.split(' ')
        for split_words in lines:
            temp = temp.append({'word':split_words},ignore_index=True)
        df1.append(temp)

    #pandasの最大表示行数の設定を変更　デフォルトは60行
    pd.set_option('display.max_rows', None)

    #全件表示
    # print(df1)

    # 感情値辞書の読み込み
    polar = pd.read_csv('http://www.lr.pi.titech.ac.jp/~takamura/pubs/pn_ja.dic',
                        encoding='shift-jis',
                        names=['word_type_score'],
                        )
    # print(polar)

    # 語と感情値を抽出
    polar['split'] = polar['word_type_score'].str.split(':')
    polar['word'] = polar['split'].str.get(0)
    polar['score'] = polar['split'].str.get(3)

    # dict型に変換
    keys = polar['word'].tolist()
    values = polar['score'].tolist()
    dic = dict(zip(keys, values))

    #辞書表示
    # print(dic)

    result = []
    # 文単位の処理
    for sentence in df1:
        temp = []
        # 語単位の処理
        for word_wakati in sentence['word']:
            word_score = []
            score = dic.get(word_wakati)
            word_score = (word_wakati,score)
            temp.append(word_score)       
        result.append(temp)

    # 文毎にデータフレーム化して表示
    # for i in range(len(result)):
    #     score_df = pd.DataFrame(result[i], columns=['word', 'score'])
    #     print(df['Tweets'][i], '\n', score_df, '\n')

    #平均を集計して表示
    avarage_list = []
    for i in result:
        temp = []
        for j in i:
            if not j[1] is None:
                temp.append(float(j[1]))
        if not len(temp) == 0:
            avarage = (sum(temp) / len(temp))
            avarage_list.append(avarage)
    if not len(avarage_list) == 0:
        avarage_total = (sum(avarage_list) / len(avarage_list))
        return avarage_total
    else:
        pass

    # print('平均はscoreは',avarage_total,'でした')

def negapozi(negapozi_score):
    if -1 <= negapozi_score <= -0.7:
        return '炎上している可能性がかなり高いです'
    if -0.7 <= negapozi_score <= -0.4:
        return '炎上している可能性があります'
    if -0.4 <= negapozi_score <= 0.4:
        return '炎上している確率は低いです'
    if 0.4 <= negapozi_score <= 0.7:
        return '炎上している確率はかなり低いです'
    if 0.7 <= negapozi_score <= 1:
        return '炎上していません'
