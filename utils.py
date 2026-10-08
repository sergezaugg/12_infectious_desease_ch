#--------------------             
# Author : Serge Zaugg
# Description : All functions an UI elements used my the streamlit app
#--------------------

import numpy as np
import pandas as pd 
import plotly.express as px
import streamlit as st
from datetime import date
from datetime import datetime
from streamlit import session_state as ss
import requests
import io
from datetime import datetime, timedelta


@st.cache_data(ttl=86400, show_spinner="Downloading BAG data...")
def download_all_data(a = 1):
    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/data/version'
    r = requests.get(full_query_string, allow_redirects=True)
    data_version = r.json()

    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/files'
    r = requests.get(full_query_string, allow_redirects=True)
    data_file_list = r.json()

    data_file_list =[a for a in data_file_list if "oblig" in a]

    # # temp 
    # data_file_list = data_file_list[0:10]

    n_files = len(data_file_list)

    data_di = {}
    for li_index in range(len(data_file_list)):
        print(li_index)
        data_set_name = data_file_list[li_index]
        print(data_set_name)
        full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/' + data_set_name + '/csv'
        r = requests.get(full_query_string, allow_redirects=True)
        raw_text = r.text
        df = pd.read_csv(io.StringIO(raw_text, newline='\n')  , sep=",")
        data_di[data_set_name] = df
          
    return data_di , data_version, n_files


#---------------------------------
# (2) function for data preparation 

def convert_iso_date_to_datetime(d):
    return(datetime.strptime(d + '-1', "%Y-W%W-%w"))

@st.cache_data
def preprocess_INFLUENZA(df):
    df = df.copy()
    # make a continuous time variable 
    df['date'] = df["temporal"].apply(convert_iso_date_to_datetime)
    # re-code  
    df['agegroup'] = df['agegroup'].replace(to_replace='0 - 4',   value='00-04') # ,   inplace=True)
    df['agegroup'] = df['agegroup'].replace(to_replace='5 - 14',  value='05-14') #,   inplace=True)
    df['agegroup'] = df['agegroup'].replace(to_replace='15 - 29', value='15-29') #,   inplace=True)
    df['agegroup'] = df['agegroup'].replace(to_replace='30 - 64', value='30-64') #,   inplace=True)
    df['agegroup'] = df['agegroup'].replace(to_replace='65+',     value='65+') #,     inplace=True)
    df['agegroup'] = df['agegroup'].replace(to_replace='unknown', value='Unknown') #, inplace=True)
    # df['agegroup'] = df['agegroup'].replace(to_replace='all',     value='All') #,     inplace=True)
    return(df)

# @st.cache_data
# def get_all_oblig(df):
#     df = df[df["type"]  == 'all']
#     df = df[df["valueCategory"]  == 'cases']
#     df = df[df["georegion"] == 'CHFL']
#     df = df[df["agegroup"]  == 'all']
#     df = df[df["sex"]  == 'all']
#     return(df)

# @st.cache_data
# def get_by_cantons_oblig(df):
#     df = df[df["type"]  == 'all']
#     df = df[df["valueCategory"]  == 'cases']
#     df = df[df["georegion"] != 'CHFL']
#     df = df[df["georegion"] != 'CH']
#     df = df[df["georegion"] != 'FL']
#     df = df[df["agegroup"]  == 'all']
#     df = df[df["sex"]  == 'all']
#     df = df.sort_values(by=["georegion", 'date'], ascending=True)
#     return(df)

# @st.cache_data
# def get_by_agegroup_oblig(df):
#     df = df[df["type"]  == 'all']
#     df = df[df["valueCategory"]  == 'cases']
#     df = df[df["georegion"] == 'CHFL']
#     df = df[df["agegroup"]  != 'all']
#     df = df[df["sex"]  == 'all']
#     df = df.sort_values(by=["agegroup", 'date'], ascending=True)
#     return(df)

# @st.cache_data
# def get_by_sex_oblig(df):
#     df = df[df["type"]  == 'all']
#     df = df[df["valueCategory"]  == 'cases']
#     df = df[df["georegion"] == 'CHFL']
#     df = df[df["agegroup"]  == 'all']
#     df = df[df["sex"]  != 'all']
#     df = df.sort_values(by=["sex", 'date'], ascending=True)
#     return(df)

# @st.cache_data
# def get_by_type_oblig(df):
#     df = df[df["type"] != 'all']
#     df = df[df["valueCategory"]  == 'cases']
#     df = df[df["georegion"] == 'CHFL']
#     df = df[df["agegroup"]  == 'all']
#     df = df[df["sex"]  == 'all']
#     df = df.sort_values(by=["sex", 'date'], ascending=True)
#     return(df)

# def prepare_data():
#     df_obli = ss["data"]["data_di"]["INFLUENZA_oblig"]
#     df_obli = df_obli[df_obli["temporal_type"] == "iso_week"]
#     df_obli = preprocess_INFLUENZA(df_obli)

#     df_all_obli = get_all_oblig(df = df_obli)
#     df_can_obli = get_by_cantons_oblig(df_obli)
#     df_age_obli = get_by_agegroup_oblig(df_obli)
#     df_sex_obli = get_by_sex_oblig(df_obli)
#     df_typ_obli = get_by_type_oblig(df_obli)

#     # merge-in '_all' info and assign to ss
#     ss["data"]["df_all_obli"] = df_all_obli
#     ss["data"]["df_can_obli"] = pd.merge(df_can_obli, df_all_obli[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
#     ss["data"]["df_age_obli"] = pd.merge(df_age_obli, df_all_obli[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
#     ss["data"]["df_sex_obli"] = pd.merge(df_sex_obli, df_all_obli[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))
#     ss["data"]["df_typ_obli"] = pd.merge(df_typ_obli, df_all_obli[['date', 'incValue']], how='inner', on='date', suffixes=('', '_all'))

#     # get the global time range
#     if ss["upar"]["date_range"] == 'initial':
#         delta_time = timedelta(days=100)
#         # concat dates from both dfs to get global min and max 
#         df_dates = df_obli['date']
#         time_options = df_dates.sort_values()
#         t_sta = time_options.min() - delta_time
#         t_sta = datetime(year = t_sta.year, month = t_sta.month, day = t_sta.day)
#         t_end = time_options.max() + delta_time
#         t_end = datetime(year = t_end.year, month = t_end.month, day = t_end.day)
#         ss["upar"]["date_range"] = (t_sta, t_end)
#         ss["upar"]["full_date_range"] = (t_sta, t_end)












