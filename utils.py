#--------------------             
# Author : Serge Zaugg
# Description : All functions an UI elements used my the streamlit app
#--------------------

import numpy as np
import pandas as pd 
import plotly.express as px
import streamlit as st
from streamlit import session_state as ss
import requests
import io


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

def convert_iso_date_to_datetime(s):
    """ helper used in data_pre_select """
    s = str(s)
    if "-M" in s:  # Monthly: 2013-M05
        return pd.to_datetime(s.replace("-M", "-") + "-01")
    elif "-W" in s:  # Weekly: 2013-W13
        return pd.to_datetime(f"{s[:4]}-W{s[-2:]}-1", format="%G-W%V-%u")
    elif s.isdigit() and len(s) == 4:  # Yearly: 2005
        return pd.Timestamp(f"{s}-01-01")    
    else:
        return pd.NaT

@st.cache_data
def data_pre_select(df):
    for k in df.keys():
        # keep only cases (no precomputed summaries)
        df[k] = df[k][df[k]["valueCategory"] == "cases"]
        # keep only relevant variables 
        cols_to_drop = ['georegion_type', 'agegroup_type', 'valueYearCumSum', 'valueMean3y', 'trend', 'prct', 
            'inc14d', 'incValueMean3m',
            'deltaValue', 'deltaIncValue', 'incValuePrctChange', 'valueMean5y', 'dataComplete']
        df[k] = df[k].drop(columns=cols_to_drop, errors="ignore")
        # drop rows if outcom is NA
        df[k] = df[k].dropna(subset=["value", "incValue"], how="all")
        # spec for years which are int already 
        if df[k]["temporal"].dtype == "int64":
            df[k]["temporal"] = df[k]["temporal"].astype(str)
            df[k]["temporal"] = df[k]["temporal"].str[:4]
        # convert nasty csv-style-strings to date    
        df[k]['date'] = df[k]["temporal"].apply(convert_iso_date_to_datetime)

    return df    

@st.cache_data
def data_select_chfl(df):
    for k in df.keys():
        df[k] = df[k][df[k]["georegion"] == "CHFL"] 
    return df

@st.cache_data
def data_select_years(x):
    df_year = {}
    for k in x.keys():
        df = x[k]
        df = df[df["temporal_type"] == "year"] 
        if df.shape[0] > 0:
            df_year[k] = df
    return(df_year)

@st.cache_data
def data_select_months(x):
    df_month = {}
    for k in x.keys():
        df = x[k]
        df = df[df["temporal_type"] == "month"] 
        if df.shape[0] > 0:
            df_month[k] = df
    return df_month

@st.cache_data
def data_select_weeks(x):
    df_iso_week = {}
    for k in x.keys():
        df = x[k]
        df = df[df["temporal_type"] == "iso_week"] 
        if df.shape[0] > 0:
            df_iso_week[k] = df
    return df_iso_week

def make_lineplot_by_age_and_sex(x, tit):
    if "agegroup" not in x.columns:
            x["agegroup"] = "not_defined"
    if "sex" not in x.columns:
            x["sex"] = "not_defined"        
    if "type" not in x.columns:
            x["type"] = "not_defined"        

    fig = px.line(
        data_frame = x,
        x = "date",
        y = "value",
        color = "agegroup",
        facet_row= "sex",
        facet_col= "type",
        title = tit,
        height = 500

        )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="gray", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="gray", mirror=True)
    return fig








