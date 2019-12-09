import numpy as np
import re

def gender_parse(df, gender):
    """Reduces dataframe according to gender parameter"""
    df1 = df[(df['gender'] == gender) | (df['gender'] == "All")]
    return df1

def age_parse(df, age):
    """Reduces dataframe according to age parameter"""
    df = df[(df['min_age'] == None) | (df['min_age'] < age)]
    df = df[(df['max_age'] == None) | (df['max_age'] > age)]

    return df

def country_parse(df, country):

    if country == 'All':
        return df
    else:
        df = df[(df['country'] == country)]
        return df

def paginate(page):
    """Reduces ranked dataframe according to page parameter"""
    end_ind = page * 12
    start_ind = end_ind - 12

    return start_ind, end_ind

def tokenizer(string):
    """Tokenizes an inputted string"""

    tokenized_lst = string.split()
    tokenized_lst = [re.sub(r'[^\w\s]','',i) for i in tokenized_lst]
    tokenized_lst = [i.lower() for i in tokenized_lst]

    return tokenized_lst

