# -*- coding: utf-8 -*-
"""r/india flair predictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10GfVm2TgVkCZwNHVKylgaNECiffhsDMY
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime
import praw
import tldextract
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle


def setUp(usrnm, passwd, cl_id, cl_sc):
    print('Getting Reddit Data...')
    reddit = praw.Reddit(client_id=cl_id, client_secret=cl_sc, user_agent='reddit_back', username=usrnm, password=passwd)

    return reddit

def extractData(reddit, urls):
    reddit.read_only = True
    topics = { "author":[],
                "body":[],
                "comments":[],
                "comms_num":[],
                "id": [],
                "score":[],
                "title": [],
                "url": [],
                "created":[]}
    print('Collecting Data...')
    for url in urls:
        submission = reddit.submission(url = url)
        topics["title"].append(submission.title)
        topics["score"].append(submission.score)
        topics["id"].append(submission.id)
        topics["url"].append(submission.url)
        topics["comms_num"].append(submission.num_comments)
        topics["created"].append(submission.created)
        topics["body"].append(submission.selftext)
        topics["author"].append(submission.author)
            
        #   Remove comments that are accessed by clicking on More Comments, limit = 0 implies no clicking
        submission.comments.replace_more(limit=0)
        comment = ''
        #   Only using top level comments
        for top_level_comment in submission.comments:
            comment = comment + ' ' + top_level_comment.body
        topics["comments"] = comment

    topics_df = pd.DataFrame(topics)
    #   The created time is in Unix Time, convert it to timestamp before proceding
    print('Done Collecting Data')
    return topics_df

def getDomain(url):
    ext = tldextract.extract(url)
    return ext.domain

def empty_to_nan(text):
    if not text:
        return "nan"
    else:
        return text

def clean_text(text):
    text = BeautifulSoup(text, "html.parser").text
    text = text.lower()
    space_sub = re.compile('[/(){}\[\]\|@,;]')
    remove_bad_sym = re.compile('[^0-9a-z #+_]')
    STOPWORDS = set(stopwords.words('english'))
    text = space_sub.sub(' ', text)
    text = remove_bad_sym.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

def to_str(text):
    return str(text)
def convert2timestamp(created):
    return datetime.datetime.fromtimestamp(created)

def create_dict(urls, test_ans):
    res_dict = {}
    for i in range(len(urls)):
        res_dict[urls[i]] = test_ans[i]
    return res_dict

def get_predictions(urls):

    nltk.download("stopwords")

    dataset_df = pd.read_csv('dataset.csv')
    print(dataset_df.head())

    client_id = '8DYCKFnYAy-VSg'
    client_secret = 'QoM1hKffGS8PHXy7m4sK3EUgNmk'
    username = 'ultramarinebot'
    password = 'DingDong'

    reddit = setUp(username, password, client_id, client_secret)
    
    test_df = extractData(reddit, urls)

    cols_to_string = ['body', 'comments', 'title']

    for col in cols_to_string:
        test_df[col] = test_df[col].apply(empty_to_nan)

    Y_train = dataset_df['flair']
    X_train = dataset_df.drop(['flair', 'id', 'created'], axis = 1)
    test_df = test_df.drop(['id', 'created'], axis = 1)
    print("X_train", X_train.shape)
    print("Y_train", Y_train.shape)
    

    
    # Adding test_df row(s) to X_train
    count_test = test_df.shape[0]
    X_train = X_train.append(test_df, ignore_index=True)


    
    for col in cols_to_string:
        X_train[col] = X_train[col].apply(to_str)
        print(col,"->" ,isinstance(X_train[col][0], str))
        X_train[col] = X_train[col].apply(clean_text)
        X_train['url'] = X_train['url'].apply(getDomain)

    
    # Normalization for comms_num and score
    

    cols_to_normalize = ['comms_num', 'score']
    for col in cols_to_normalize:
        X_train[col] = ((X_train[col] - X_train[col].mean()) / (X_train[col].max() - X_train[col].min()) + 1)/2

    # Remove Duplicates
    X_train = X_train.loc[:,~X_train.columns.duplicated()]

    # Recover test_df
    test_df = X_train.tail(count_test)
    X_train = X_train[:-count_test]
    test_df.reset_index(drop=True, inplace=True)
    #print(test_df)
    #print(X_train.head())

    #X_train = pd.concat([X_train, pd.get_dummies(X_train['url'])], axis=1)
    #X_train = pd.concat([X_train, pd.get_dummies(X_train['author'])], axis=1)
    #print(test_df.columns)
    X_train = X_train.drop(['url', 'author'], axis=1)
    test_df = test_df.drop(['url', 'author'], axis=1)


    corpus = X_train['body'] + X_train['comments'] + X_train['title']
    X_train = X_train.drop(cols_to_string, axis=1)

    corpus_test = test_df['body'] + test_df['comments'] + test_df['title']
    test_df = test_df.drop(cols_to_string, axis=1)

    print('pre sans tfidf done')

    # Preprrocessing

    tfidf_vect = TfidfVectorizer(max_features=10000, stop_words='english', min_df=1, binary=0, use_idf=1, smooth_idf=0, sublinear_tf=1)

    print('crash location, maybe 1')

    tfidf_vect.fit(corpus.values.astype('U'))
    #tfidf_vect_vectors = tfidf_vect.transform(corpus.values.astype('U'))
    #col_tfidf = tfidf_transformer.fit_transform(col_vect)

    #col_tfidf_df = pd.DataFrame(tfidf_vect_vectors.todense(), columns=tfidf_vect.get_feature_names())

    print('crash location, maybe 2')
    #X_train = pd.concat([X_train, col_tfidf_df], axis=1)

    # tfidf of test_df
    tfidf_vect_test = tfidf_vect.transform(corpus_test.values.astype('U'))

    print('crash location, maybe 3')

    col_names = ['tfidf_' + s for s in tfidf_vect.get_feature_names()]
    col_tfidf_test = pd.DataFrame(tfidf_vect_test.todense(), columns=col_names)

    print('col_tfidf_test:   ',col_tfidf_test.shape)

    test_df = pd.concat([test_df, col_tfidf_test], axis=1)

    print('test_df shape:   ',test_df.shape)
    
    print('tfidf done')

    
    rf = pickle.load(open('models/rf_model.sav', 'rb'))
    #catb = pickle.load(open('models/catb_model.sav', 'rb'))

    print('model loaded')

    test_ans = rf.predict(test_df)
    #test_ans = catb.predict(test_df)
    
    print('Done with everything!')

    return create_dict(urls, test_ans)

    """

    
    from sklearn.tree import DecisionTreeClassifier
    dt = DecisionTreeClassifier(random_state=10)
    dt.fit(X_train, Y_train)
    dt.score(X_test_cv, Y_test_cv)

    test_dt = dt.predict(test_df)
    return create_dict(urls, test_dt)

    
    from sklearn.linear_model import SGDClassifier

    sgd = SGDClassifier(loss='hinge', penalty='l2', random_state=10, max_iter=5, tol=None)
    sgd.fit(X_train, Y_train)
    sgd.score(X_test_cv, Y_test_cv)

    from sklearn.naive_bayes import MultinomialNB

    nb = MultinomialNB()
    nb.fit(X_train, Y_train)
    nb.score(X_test_cv, Y_test_cv)

    from sklearn import svm
    svm_rbf = svm.SVC(kernel='rbf', random_state=10).fit(X_train, Y_train)
    svm_rbf.score(X_test_cv, Y_test_cv)

    from sklearn import svm
    svm_linear = svm.SVC(kernel='linear', C=5, gamma='auto',random_state = 10).fit(X_train, Y_train)
    svm_linear.score(X_test_cv, Y_test_cv)



    # Save Model
    import pickle
    pickle.dump(rf, open('rf_model.sav', 'wb'))
    # To load model use: model = pickle.load(open(filename, 'rb'))
    """
