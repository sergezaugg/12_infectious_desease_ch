#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run app.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from src.utils import download_all_data, data_pre_select, data_select_chfl, get_ma_based_trend
from src.utils import data_select_years, data_select_months, data_select_weeks, data_select_only_all_groups, stack_dict_of_dfs
from src.utils import get_overview_df
from resources.styles import apply_global_styles

#------------------------------
# prepare app 
st.set_page_config(layout = "wide", initial_sidebar_state = "expanded", page_title="SID-Explorer", page_icon='pics/z_logo_blue.png')
apply_global_styles() # apply custom CSS styles 
st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")
pd.set_option('display.max_rows', 500)

#------------------------------
# prepare data once (only run on startup and when dev triggers refresh)
# run the data prep pipe only and exactly once on session startup MCELP
# because many caches function will consume resources and time even on cache hit!
if "di_prep" not in ss:
    ss.ref_date = pd.Timestamp.today().normalize()
    # download and perp once
    ss.di_data, ss.data_version, ss.n_files, ss.ts_downl, ss.dl_status = download_all_data(22)
    ss.di_prep = data_pre_select(ss.di_data)
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
    ss.df_overview = get_overview_df() # important lookup  table used many places

    # get trend via Robust median–mean smoother
    ss.df_m_ma_wide, ss.df_m_ma_long = get_ma_based_trend(df = ss.df_months_all_concat, outcome = "incValue", 
        wsiz_med = 12, wsiz_mea =7, n_extrap = 5)
    ss.df_w_ma_wide, ss.df_w_ma_long = get_ma_based_trend(df = ss.df_weeks_all_concat, outcome = "incValue", 
        wsiz_med = 10, wsiz_mea =5, n_extrap = 3)

    # filter past few years relative to today 
    ss.df_months_filtered_2y = ss.df_m_ma_long.loc[ss.df_m_ma_long["days_elapsed"] <= 365*2]
    ss.df_weeks_filtered_recent  = ss.df_w_ma_long.loc[ss.df_w_ma_long["days_elapsed"] <= 30*6]
    # get data age of each disease
    ss.df_months_max_date = ss.df_months_all_concat.loc[ss.df_months_all_concat.groupby("disease")["date"].idxmax()]
    ss.df_weeks_max_date  = ss.df_weeks_all_concat.loc[ss.df_weeks_all_concat.groupby("disease")["date"].idxmax()]

    ss.labels = {
        "value" :  "Cases count",
        "incValue": "Cases per 10⁵ hab",  
        "resp_var": "Cases per 10⁵ hab",  
        "pop"   :  "Total population",
        "date"  :  "Date",
        "week"  :  "Week",
        "month" :  "Month",
    }

    # lighten the ss 
    for key in ["di_weeks", "di_months", "di_years", "di_weeks_all", "di_months_all", "di_years_all"]:
        del st.session_state[key]







# Protects every ss key from being deleted (for multi-page consistency across clicks)
for key in list(st.session_state.keys()):
    st.session_state[key] = st.session_state[key]

# build sidebar
with st.sidebar:
    st.markdown(f"""## :primary[**Swiss Infectious Disease Explorer**]""")
    st.markdown("""
        <div style="line-height: 1.3; margin-bottom: 0.9em;;">
            <div>Data Version: <code>{}</code></div>
            <div>Downloaded: <code>{}</code></div>
            <div>Reference date: <code>{}</code></div>
        </div>
    """.format(ss.data_version['name'], ss.ts_downl, ss.ref_date.date()),
    unsafe_allow_html=True)
    st.caption(ss.dl_status)
    st.divider()
   
# main navigation
p00 = st.Page("pages/page_landing.py",  title="Epi-Radar", default=True)
p01 = st.Page("pages/page_info.py",  title="Diseases")
p02 = st.Page("pages/page01_weeks.py",  title="Weekly-History")
p03 = st.Page("pages/page02_months.py",  title="Monthly-History")
p04 = st.Page("pages/page02_years.py",  title="Yearly-History")
p06 = st.Page("pages/page_trend_monthly.py",  title="Monthly-Trend")
p07 = st.Page("pages/page_trend_weekly.py",  title="Weekly-Trend")
p05 = st.Page("pages/page_about.py",  title="About")
p20 = st.Page("pages/page_disclaimer.py",  title="Disclaimer")
p21 = st.Page("pages/page_refresh.py",  title="Dev")
p22 = st.Page("pages/page_methods.py",  title="Methods")

pg = st.navigation([p00, p06, p07, p03, p02, p04, p01, p05, p22, p20, p21], position = "top")

pg.run()





