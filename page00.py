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
# [df_data[a].shape for a in df_data]
# [print(df_data[a].columns) for a in df_data]

# df = df_data['BOTULISM_oblig']


for k in df_data.keys():
    
    df = df_data[k]
    st.text(k)
    st.text(df.shape)

    a,b,c,d,e = st.columns(5)
    with a:
        if "valueCategory" in df.columns:
            st.dataframe(df["valueCategory"].value_counts())
    with c:
        if "temporal_type" in df.columns:
            st.dataframe(df['temporal_type'].value_counts()) 
    with d:
        if "georegion" in df.columns:
            st.dataframe(df['georegion'].value_counts()) 
    with e:
        if "georegion_type" in df.columns:
            st.dataframe(df['georegion_type'].value_counts()) 

    a,b,c,d,e = st.columns(5)
    with a:
        if "agegroup" in df.columns:
            st.dataframe(df['agegroup'].value_counts()) 
    with b:
        if "agegroup_type" in df.columns:
            st.dataframe(df['agegroup_type'].value_counts()) 
    with c:
        if "sex" in df.columns:
            st.dataframe(df['sex'].value_counts()) 
    with d:
        if "type" in df.columns:
            st.dataframe(df['type'].value_counts()) 
    

    st.dataframe(df)
    # 'valueCategory', 'temporal', 'temporal_type', 'georegion',
    # 'georegion_type', 'agegroup', 'agegroup_type', 'sex', 'type',


