#--------------------             
# Author : Serge Zaugg
# Description : Main interactive visualization page 
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import download_all_data
pd.set_option("display.max_rows", 200)  # Show up to 100 rows

df_data, data_version, n_files = download_all_data(22)

# df_data.keys()


# pre-selection 
for k in df_data.keys():
    
    df_data[k] = df_data[k][df_data[k]["valueCategory"] == "cases"]

    cols_to_drop = ['georegion_type', 'agegroup_type', 'valueYearCumSum', 'valueMean3y', 'trend', 'prct', 
        'inc14d', 'incValueMean3m',
        'deltaValue', 'deltaIncValue', 'incValuePrctChange', 'valueMean5y', 'dataComplete']
    df_data[k] = df_data[k].drop(columns=cols_to_drop, errors="ignore")

    df_data[k] = df_data[k].dropna(subset=["value", "incValue"], how="all")




# select only all CH
for k in df_data.keys():
    df_data[k] = df_data[k][df_data[k]["georegion"] == "CHFL"] 




# filter out the per-month data 
df_month = {}
for k in df_data.keys():
    df = df_data[k]
    df = df[df["temporal_type"] == "month"] 
    if df.shape[0] > 0:
        df_month[k] = df


# filter out the per-year data 
df_year = {}
for k in df_data.keys():
    df = df_data[k]
    df = df[df["temporal_type"] == "year"] 
    if df.shape[0] > 0:
        df_year[k] = df

# filter out the per-iso_week data 
df_iso_week = {}
for k in df_data.keys():
    df = df_data[k]
    df = df[df["temporal_type"] == "iso_week"] 
    if df.shape[0] > 0:
        df_iso_week[k] = df


# st.text([len(df_month), len(df_year), len(df_iso_week)])


df_data = df_iso_week




for k in df_data.keys():
    
    df = df_data[k]
    st.text(k)
    st.text(df.shape)


    a,b,c,d,e,f = st.columns(6)
    with a:
        if "valueCategory" in df.columns:
            st.dataframe(df["valueCategory"].value_counts())
    with b:
        if "temporal_type" in df.columns:
            st.dataframe(df['temporal_type'].value_counts()) 
    with c:
        if "georegion" in df.columns:
            st.dataframe(df['georegion'].value_counts()) 
    with d:
        if "agegroup" in df.columns:
            st.dataframe(df['agegroup'].value_counts()) 
    with e:
        if "sex" in df.columns:
            st.dataframe(df['sex'].value_counts()) 
    with f:
        if "type" in df.columns:
            st.dataframe(df['type'].value_counts()) 
    

    # st.dataframe(df.head(), width = "content")


    


