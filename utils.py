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
from datetime import datetime

API_BASE_URL = "https://api.idd.bag.admin.ch/api/v1"

@st.cache_data(ttl=60*60*12, show_spinner="Downloading data from " + "`" + API_BASE_URL + "`")
def download_all_data(a = 1):
    full_query_string = f"{API_BASE_URL}/data/version"
    r = requests.get(full_query_string, allow_redirects=True)
    data_version = r.json()

    full_query_string = f"{API_BASE_URL}/export/latest/files"
    r = requests.get(full_query_string, allow_redirects=True)
    data_file_list = r.json()

    data_file_list =[a for a in data_file_list if "oblig" in a]

    n_files = len(data_file_list)

    data_di = {}
    for li_index in range(len(data_file_list)):
        print(li_index)
        data_set_name = data_file_list[li_index]
        print(data_set_name)
        full_query_string = f"{API_BASE_URL}/export/latest/" + data_set_name + '/csv'
        r = requests.get(full_query_string, allow_redirects=True)
        raw_text = r.text
        df = pd.read_csv(io.StringIO(raw_text, newline='\n')  , sep=",")
        print(df.shape)
        data_di[data_set_name] = df

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return data_di, data_version, n_files, ts

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

@st.cache_data(show_spinner="Pre-processing data")
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
            'inc14d', 'incValueMean3m', 'testResult', 'testResult_type',
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
        if(len(df[k])==0):
            df[k] = df[k][df[k]["georegion"] == "CH"] # # because of YELLOWFEVER_oblig
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
def stack_dict_of_dfs(di):
    df = pd.concat([d.assign(disease=k) for k, d in di.items()], ignore_index=True)
    df["disease"] = df["disease"].str.removesuffix("_oblig")
    # merge-in desease short names 
    df_dis_abbr = pd.read_csv("resources/disease_abbrev.txt", sep=",")
    df = df.merge(df_dis_abbr, 'left', on = "disease")
    # add iso-week, month and year indicator
    df["year"]  = df['date'].dt.year
    df["month"] = df['date'].dt.month
    df["week"]  = df['date'].dt.isocalendar().week
    # add days elapsed sice today (ref date)
    df["days_elapsed"] = (ss.ref_date - df["date"]).dt.days
    # enforce sorting 
    df = df.sort_values(['disease', 'temporal_type', 'georegion', 'agegroup', 'sex', 'date', 'year', 'week'])
    return df 


@st.cache_data
def data_select_only_all_groups(df):
    for k in df.keys():
        df[k] = df[k][df[k]["sex"] == "all"] 
        df[k] = df[k][df[k]["agegroup"] == "all"] 
        df[k] = df[k][df[k]["type"] == "all"]   
    return df


def get_overview_df():
    a = ss.df_weeks_all_concat.groupby(["temporal_type", "disease"]).size().reset_index()
    b = ss.df_months_all_concat.groupby(["temporal_type", "disease"]).size().reset_index()
    c = ss.df_years_all_concat.groupby(["temporal_type", "disease"]).size().reset_index()

    a['temporal_type'] = "Yes"
    b['temporal_type'] = "Yes"
    c['temporal_type'] = "Yes"

    a.rename(columns={"temporal_type": "weekly"}, inplace=True)
    b.rename(columns={"temporal_type": "monthly"}, inplace=True)
    c.rename(columns={"temporal_type": "yearly"}, inplace=True)

    a = a.drop(columns=[0], errors="ignore")
    b = b.drop(columns=[0], errors="ignore")
    c = c.drop(columns=[0], errors="ignore")

    d = a.merge(b, 'outer', on = "disease").merge(c, 'outer', on = "disease")

    d = d[["disease", "yearly", "monthly", "weekly", ]]
    df_overview = d.fillna("No")

    # merge-in metadata 
    df_descript = pd.read_csv("resources/disease_description.txt", sep=",")
    df_overview = df_overview.merge(df_descript, 'outer', on = "disease")

    df_dis_cate = pd.read_csv("resources/disease_category.txt", sep=",")
    df_overview = df_overview.merge(df_dis_cate, 'outer', on = "disease")

    df_dis_abbr = pd.read_csv("resources/disease_abbrev.txt", sep=",")
    df_overview = df_overview.merge(df_dis_abbr, 'outer', on = "disease")
    
    return(df_overview)




def extrapolate_trend_edges(s, n_edge=6):
    """Replace trend edges using linear extrapolation."""
    s = s.copy()
    y = s.to_numpy(dtype=float).copy()
    n = len(y)
    k = min(n_edge, n // 2)
    if k < 2:
        return s
    x = np.arange(n)
    # Fit lines to the interior, excluding edge regions
    slope_left, intercept_left = np.polyfit(x[k:2*k], y[k:2*k], 1)
    slope_right, intercept_right = np.polyfit(x[n-2*k:n-k], y[n-2*k:n-k], 1)
    # Extrapolate into the edge regions
    y[:k] = slope_left * x[:k] + intercept_left
    y[-k:] = slope_right * x[-k:] + intercept_right
    return pd.Series(y, index=s.index, name=s.name)



@st.cache_data(show_spinner="Computing MA-based trend")
def get_ma_based_trend(df, outcome, wsiz_med, wsiz_mea, n_extrap):
    """ moving-average/median-based estimation of mid-term trend """
    df = df.sort_values(["disease", "date"])
    var_name_ma = outcome + "_ma"
    # two-step moving trend (Robust median–mean smoother)
    df[var_name_ma] = (df.groupby("disease")[outcome]
        .transform(lambda s: s.rolling(wsiz_med, center=True, min_periods= int(wsiz_med/2)).median()))
    df[var_name_ma] = (df.groupby("disease")[var_name_ma]
        .transform(lambda s: s.rolling(wsiz_mea, center=True, min_periods= int(wsiz_mea/2)).mean()))
    # NEW - extrapolate edges 
    if n_extrap > 1:
        df[var_name_ma] = df.groupby("disease")[var_name_ma].transform(lambda s: extrapolate_trend_edges(s, n_edge=n_extrap)) 
    # get residuals 
    df['residuals'] = df[outcome] - df[var_name_ma]
    # reshape for easy plotting
    df_long = df.melt(id_vars=[c for c in df.columns if c not in [outcome, var_name_ma]],
        value_vars=[outcome, var_name_ma],
        var_name="measure",
        value_name= "resp_var")
    return df, df_long




    


    



# from statsmodels.tsa.seasonal import STL

# @st.cache_data(show_spinner="Computing MA-based trend")
# def get_stl_based_trend(df, outcome):

#     var_name_ma = outcome + "_ma"

#     resp = df[outcome]

#     result = STL(
#         endog = resp,
#         period=12,       # monthly data, annual seasonality
#         seasonal=19,     # smoother evolving seasonal pattern; odd
#         trend=37,        # smoother nonlinear trend; odd
#         low_pass=13,     # odd, greater than period
#         robust=True,
#     ).fit()

#     df[var_name_ma] = result.trend
#     df['residuals'] = result.seasonal + result.resid

#     # reshape for easy plotting
#     df_long = df.melt(id_vars=[c for c in df.columns if c not in [outcome, var_name_ma]],
#         value_vars=[outcome, var_name_ma],
#         var_name="measure",
#         value_name= "resp_var")
#     return df, df_long







