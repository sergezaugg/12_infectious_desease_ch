#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import download_all_data, data_pre_select, data_select_chfl
from utils import data_select_years, data_select_months, data_select_weeks
pd.set_option("display.max_rows", 200)  # Show up to 100 rows

df_data, data_version, n_files = download_all_data(22)

# df_data.keys()

df_sel = data_pre_select(df_data)
df_sel = data_select_chfl(df_sel)

ss.df_years  = data_select_years(df_sel)
ss.df_months = data_select_months(df_sel)
ss.df_weeks  = data_select_weeks(df_sel)




df_temp = ss.df_months.copy()

for k in df_temp.keys():
    
    df = df_temp[k]
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
    
    st.dataframe(df.head()) # , width = "content")


    


