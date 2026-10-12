#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import numpy as np
import plotly.express as px
import pandas as pd
from utils import download_all_data, data_pre_select, data_select_chfl
from utils import data_select_years, data_select_months, data_select_weeks, data_select_only_all_groups, stack_dict_of_dfs

#------------------------------
# prepare app 
st.set_page_config(layout = "wide", initial_sidebar_state = "expanded", page_icon='pics/z_logo_blue.png')
st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")
pd.set_option('display.max_rows', 500)


df_data, data_version, n_files = download_all_data(22)

df_sel = data_pre_select(df_data)
df_sel = data_select_chfl(df_sel)

ss.df_years  = data_select_years(df_sel)
ss.df_weeks  = data_select_weeks(df_sel)

ss.df_months = data_select_months(df_sel)
ss.df_months_all = data_select_only_all_groups(ss.df_months)
ss.df_months_concat = stack_dict_of_dfs(di = ss.df_months_all)

# build sidebar
with st.sidebar:
    st.markdown(f"""# :primary[**Swiss Infectious Disease Explorer**] """)

# (3) main navigation
pages = [
    st.Page("page00.py",  title="Summary tables"),
    st.Page("page01_weeks.py",  title="Plots weekly"),
    st.Page("page02_months.py",  title="Plots monthly"),
    st.Page("page02_years.py",  title="Plots yearly"),
    st.Page("page02.py",  title="Credits"),
    ]
pg = st.navigation(pages, position = "top")
pg.run()





