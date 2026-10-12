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


@st.cache_data(ttl=60*60*12, show_spinner="Downloading BAG data...")
def download_all_data(a = 1):
    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/data/version'
    r = requests.get(full_query_string, allow_redirects=True)
    data_version = r.json()

    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/files'
    r = requests.get(full_query_string, allow_redirects=True)
    data_file_list = r.json()

    data_file_list =[a for a in data_file_list if "oblig" in a]

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

@st.cache_data(show_spinner="Pre-processing data...")
def data_pre_select(df):
    for k in df.keys():
        if "agegroup" not in df[k].columns:
            df[k]["agegroup"] = "all"
        if "sex" not in df[k].columns:
            df[k]["sex"] = "all"        
        if "type" not in df[k].columns:
            df[k]["type"] = "all"        
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

@st.cache_data
def make_lineplot_by_age_and_sex(x, tit):
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


@st.cache_data(show_spinner="Rendering plot ...")
def make_lineplot_all_by_disease(x, height, outcome):

    fig = px.line(
        data_frame = x,
        x = "date",
        y = outcome,
        facet_row= "disease",
        facet_row_spacing = 0.01,
        markers=True,
        height = height,
        # render_mode="webgl",
        )

    fig.update_traces(marker=dict(size=5))   
    fig.update_layout(
        showlegend=True,
        margin=dict(l=50, r=190, t=50, b=40),
        legend=dict(title=None, bordercolor="white", borderwidth=1, orientation="h", x=0, xanchor="left", y=1.015, yanchor="top",),
        )
    fig.update_xaxes(
        showline = True, linewidth=1.8, mirror=True, showticklabels=True, ticks="inside",
        title_font=dict(size=14),
        dtick="M12", tick0="2000-01-01", showgrid=True, gridcolor="#535053"
        )   
    fig.update_yaxes(
        matches=None,
        showline = True, linewidth=1.8, mirror=True,
        title_font=dict(size=16),
        range=[0.0, None]
        ) 
    fig.for_each_annotation(lambda a: a.update(x=1.015,font=dict(size=16)))
    for annotation in fig.layout.annotations:
        annotation.text = annotation.text.replace("disease=", "")
        annotation.textangle = 0

    return fig

    
@st.cache_data
def stack_dict_of_dfs(di):
    return pd.concat([d.assign(disease=k) for k, d in di.items()], ignore_index=True)


@st.cache_data
def data_select_only_all_groups(df):
    for k in df.keys():
        df[k] = df[k][df[k]["sex"] == "all"] 
        df[k] = df[k][df[k]["agegroup"] == "all"] 
        df[k] = df[k][df[k]["type"] == "all"]   
    return df


