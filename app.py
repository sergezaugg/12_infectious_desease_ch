#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run app.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from src.utils_dataprep import download_all_data, data_pre_select, data_select_chfl, get_ma_based_trend
from src.utils_dataprep import data_select_years, data_select_months, data_select_weeks, data_select_only_all_groups, stack_dict_of_dfs
from src.utils_dataprep import get_overview_df
from resources.styles import apply_global_styles

#------------------------------
# (1) prepare app 
st.set_page_config(layout = "wide", initial_sidebar_state = "expanded", page_title="SID-Explorer", page_icon='pics/z_logo_blue.png')
apply_global_styles() # apply custom CSS styles 
st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")
pd.set_option('display.max_rows', 500)

#------------------------------
# (2) run the data prep 
# Do once per session and if admin triggers refresh 
if "di_prep" not in ss:

    #------------------------------
    # initialize session state (constant values)
    # how much days back to show on landing page
    ss.recent_days_monthly = 365*2
    ss.recent_days_weekly = 30*6
    # params for trend computation monthly
    ss.wsiz_med_m = 12
    ss.wsiz_mea_m = 7
    ss.n_extrap_m = 5 
    # params for trend computation weekly
    ss.wsiz_med_w = 7
    ss.wsiz_mea_w = 5
    ss.n_extrap_w = 3 
    # define labels used in multiple pages 
    ss.labels = {
        "value" :  "Cases count",
        "incValue": "Cases per 10⁵ hab",  
        "value_long" :  "Cases count",
        "incValue_long": "Cases per 10⁵ hab",  
        "resp_var": "Cases per 10⁵ hab", 
        "incValue_residuals" : "Residuals", 
        "value_residuals" : "Residuals", 
        "pop"   :  "Total population",
        "date"  :  "Date",
        "week"  :  "Week",
        "month" :  "Month",
    }

    df_dis_abbr = pd.read_csv("resources/disease_abbrev.txt", sep=",")
    
    #------------------------------
    # basic data preparation
    ss.ref_date = pd.Timestamp.today().normalize()
    # download and perp once
    ss.di_data, ss.data_version, ss.n_files, ss.ts_downl, ss.dl_status = download_all_data()
    ss.di_prep = data_pre_select(ss.di_data)
    # extract pre-digested dfs 
    ss.di_prep_chfl = data_select_chfl(ss.di_prep)

    # objects for the pages 
    ss.di_weeks  = data_select_weeks(ss.di_prep_chfl)
    ss.di_weeks_all = data_select_only_all_groups(ss.di_weeks)
    ss.df_weeks_all_concat = stack_dict_of_dfs(di = ss.di_weeks_all, ref_date = ss.ref_date, df_abbr = df_dis_abbr)

    ss.di_months = data_select_months(ss.di_prep_chfl)
    ss.di_months_all = data_select_only_all_groups(ss.di_months)
    ss.df_months_all_concat = stack_dict_of_dfs(di = ss.di_months_all, ref_date = ss.ref_date, df_abbr = df_dis_abbr)

    ss.di_years  = data_select_years(ss.di_prep_chfl)
    ss.di_years_all = data_select_only_all_groups(ss.di_years)
    ss.df_years_all_concat = stack_dict_of_dfs(di = ss.di_years_all, ref_date = ss.ref_date, df_abbr = df_dis_abbr)
    
    # create important lookup  table used many places
    ss.df_overview = get_overview_df() 
    
    # get data age of each disease
    ss.df_months_max_date = ss.df_months_all_concat.loc[ss.df_months_all_concat.groupby("disease")["date"].idxmax()]
    ss.df_weeks_max_date  = ss.df_weeks_all_concat.loc[ss.df_weeks_all_concat.groupby("disease")["date"].idxmax()]

    #------------------------------
    # advanced data preparation

    # get monthly trend via Robust median–mean smoother
    dfa = get_ma_based_trend(df = ss.df_months_all_concat, outcome = "value", 
        wsiz_med = ss.wsiz_med_m, wsiz_mea = ss.wsiz_mea_m, n_extrap = ss.n_extrap_m)
    dfb = get_ma_based_trend(df = ss.df_months_all_concat, outcome = "incValue", 
        wsiz_med = ss.wsiz_med_m, wsiz_mea = ss.wsiz_mea_m, n_extrap = ss.n_extrap_m)
    # merge smoother values into main df
    df_m_ma_wide = dfa.merge(dfb, how = 'inner', on = ["disease", "date"])
    ss.df_months_all_concat = ss.df_months_all_concat.merge(df_m_ma_wide, how = 'inner', on = ["disease", "date"])

    # get weekly trend via Robust median–mean smoother
    dfa = get_ma_based_trend(df = ss.df_weeks_all_concat, outcome = "value", 
        wsiz_med = ss.wsiz_med_w, wsiz_mea = ss.wsiz_mea_w, n_extrap = ss.n_extrap_w)
    dfb = get_ma_based_trend(df = ss.df_weeks_all_concat, outcome = "incValue", 
        wsiz_med = ss.wsiz_med_w, wsiz_mea = ss.wsiz_mea_w, n_extrap = ss.n_extrap_w)
    # merge smoother values into main df
    df_w_ma_wide = dfa.merge(dfb, how = 'inner', on = ["disease", "date"])
    ss.df_weeks_all_concat = ss.df_weeks_all_concat.merge(df_w_ma_wide, how = 'inner', on = ["disease", "date"])
    
    # filter past few years relative to today 
    ss.df_months_recent = ss.df_months_all_concat.loc[ss.df_months_all_concat["days_elapsed"] <= ss.recent_days_monthly]
    ss.df_weeks_recent  = ss.df_weeks_all_concat.loc [ ss.df_weeks_all_concat["days_elapsed"] <= ss.recent_days_weekly]

    # remove dev-only items from ss 
    for key in ["di_weeks", "di_months", "di_years", "di_weeks_all", "di_months_all", "di_years_all"]:
        del st.session_state[key]

# dev
# data_pre_select.clear()
# get_ma_based_trend.clear()
# st.write(ss.df_months_all_concat)

#------------------------------
# (3) Protects ss keys from being deleted (for multi-page consistency across clicks)
# exclude key of forms which have their own Widget state management
my_list = list(st.session_state.keys())
my_list = [x for x in my_list if not x.startswith("ui_trend_m_disease_form2")]
my_list = [x for x in my_list if not x.startswith("ui_trend_w_disease_form2")]
my_list = [x for x in my_list if not x.startswith("ui_trace_y_disease_form2")]
for key in my_list:
    st.session_state[key] = st.session_state[key]

#------------------------------
# (4) build frontend

# sidebar
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
   
# pages 
p01 = st.Page("pages/page_landing.py", title="Epi-Radar", default=True)
p02 = st.Page("pages/page_weekly.py", title="Weekly History")
p03 = st.Page("pages/page_monthly.py", title="Monthly History")
p04 = st.Page("pages/page_yearly.py", title="Yearly History")
p05 = st.Page("pages/page_info.py", title="Diseases")
p06 = st.Page("pages/page_about.py", title="About")
p07 = st.Page("pages/page_methods.py", title="Methods")
p08 = st.Page("pages/page_disclaimer.py", title="Disclaimer")
p09 = st.Page("pages/page_refresh.py", title="Maintenance")

# navigation
pg = st.navigation([p01, p02, p03, p04, p05, p06, p07, p08, p09], position = "top")

# execute pages code 
pg.run()

