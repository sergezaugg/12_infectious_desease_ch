#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run app.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import numpy as np
import plotly.express as px
import pandas as pd
from utils import download_all_data, data_pre_select, data_select_chfl
from utils import data_select_years, data_select_months, data_select_weeks, data_select_only_all_groups, stack_dict_of_dfs
import gc
from utils import get_overview_df
from resources.styles import apply_global_styles

#------------------------------
# prepare app 
st.set_page_config(layout = "wide", initial_sidebar_state = "expanded", page_icon='pics/z_logo_blue.png')
apply_global_styles() # apply custom CSS styles 
st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")
pd.set_option('display.max_rows', 500)

#------------------------------
# run the data prep pipe only and exactly once on session startup - cago en la puuuuuuta :-)
# many caches function will consume resources and time even on cache hit!
if "di_prep" not in ss:
    # download and perp once
    ss.di_data, ss.data_version, ss.n_files, ss.ts_downl = download_all_data(22)
    ss.di_prep = data_pre_select(ss.di_data.copy())
    # extract pre-digested dfs 
    ss.di_prep_chfl = data_select_chfl(ss.di_prep)
    # objects for the pages 
    ss.di_weeks  = data_select_weeks(ss.di_prep_chfl)
    ss.di_weeks_all = data_select_only_all_groups(ss.di_weeks)
    ss.df_weeks_all_concat = stack_dict_of_dfs(di = ss.di_weeks_all)
    ss.di_months = data_select_months(ss.di_prep_chfl)
    ss.di_months_all = data_select_only_all_groups(ss.di_months)
    ss.df_months_all_concat = stack_dict_of_dfs(di = ss.di_months_all)
    ss.di_years  = data_select_years(ss.di_prep_chfl)
    ss.di_years_all = data_select_only_all_groups(ss.di_years)
    ss.df_years_all_concat = stack_dict_of_dfs(di = ss.di_years_all)
    ss.df_overview = get_overview_df()

# st.text(ss.df_years_all_concat['week'].dtype)
# # add month and year vars 
# s = ss.df_months_all_concat['date']
# ss.df_months_all_concat["year"] = s.dt.year
# ss.df_months_all_concat["month"] = s.dt.month
# # st.text(ss.df_months_all_concat.shape)

# YELLOWFEVER_oblig
# [(st.text(a) , st.text(ss.di_prep_chfl[a]["temporal_type"].unique().tolist()) )for a in ss.di_prep_chfl]
# [(st.text(a) , st.dataframe(ss.di_data[a]) )for a in ss.di_data]
# st.dataframe(ss.di_data['YELLOWFEVER_oblig'])

# st.dataframe(ss.df_years_all_concat)
# st.text(len(ss.df_weeks_all_concat['disease'].unique()))
# st.dataframe((ss.df_months_all_concat))
# st.text(len(ss.df_years_all_concat['disease'].unique()))

# build sidebar
with st.sidebar:
    st.markdown(f"""### :primary[**Swiss Infectious Disease Explorer**]""")
    st.text("V-" + ss.data_version['name'] + " • D-" + ss.ts_downl + " • N-" + str(ss.n_files))
   
# (3) main navigation
p01 = st.Page("pages/page00.py",  title="Overview")
p02 = st.Page("pages/page01_weeks.py",  title="Weekly")
p03 = st.Page("pages/page02_months.py",  title="Monthly")
p04 = st.Page("pages/page02_years.py",  title="Yearly")
p05 = st.Page("pages/page02.py",  title="Info")
p20 = st.Page("pages/page_disclaimer.py",  title="Disclaimer")

pg = st.navigation([p01, p02, p03, p04, p05, p20], position = "top")
pg.run()





