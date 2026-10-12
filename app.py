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

#------------------------------
# prepare app 
st.set_page_config(layout = "wide", initial_sidebar_state = "expanded", page_icon='pics/z_logo_blue.png')
st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")
pd.set_option('display.max_rows', 500)


di_data, data_version, n_files = download_all_data(22)

di_sel = data_pre_select(di_data).copy()
di_sel = data_select_chfl(di_sel)

ss.di_weeks  = data_select_weeks(di_sel).copy()
ss.di_weeks_all = data_select_only_all_groups(ss.di_weeks)
ss.df_weeks_all_concat = stack_dict_of_dfs(di = ss.di_weeks_all)

ss.di_months = data_select_months(di_sel).copy()
ss.di_months_all = data_select_only_all_groups(ss.di_months)
ss.df_months_all_concat = stack_dict_of_dfs(di = ss.di_months_all)

ss.di_years  = data_select_years(di_sel).copy()
ss.di_years_all = data_select_only_all_groups(ss.di_years)
ss.df_years_all_concat = stack_dict_of_dfs(di = ss.di_years_all)

del(di_data, di_sel)
gc.collect()

# build sidebar
with st.sidebar:
    st.markdown(f"""#:primary[**Swiss Infectious Disease Explorer**]""")

# (3) main navigation
p01 = st.Page("pages/page00.py",  title="Summary tables")
p02 = st.Page("pages/page01_weeks.py",  title="Plots weekly")
p03 = st.Page("pages/page02_months.py",  title="Plots monthly")
p04 = st.Page("pages/page02_years.py",  title="Plots yearly")
p05 = st.Page("pages/page02.py",  title="Credits")

pg = st.navigation([p01, p02, p03, p04, p05], position = "top")
pg.run()





