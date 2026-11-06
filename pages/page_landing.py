#--------------------             
# Author : Serge Zaugg
# Description : landing page (radar)
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
from src.utils_ui import ui_render_landing_page

with st.sidebar:
    st.markdown("""
    :primary[Summary:] Past 6 months of diseases with weekly data (Upper panel)
    and past 2 years of diseases with monthly data (Lower panel).  
    """)

with st.sidebar:
    with st.container(border=True):
        selected_outcome = st.radio("Select outcome", options = ["Incidence", "Count"], index=0, key = "xxdvfgghjkloiww4", horizontal=True)

if selected_outcome == "Incidence": 
    yvars = ["incValue", "incValue_ma"]     
if selected_outcome == "Count":
    yvars = ["value", "value_ma"]

ui_render_landing_page(
    df_trend = ss.df_weeks_recent, df_age = ss.df_weeks_max_date, height = 180 , width = 800, 
    col_tit = ["Update status weekly data", "Weekly diseases-radar (Latest 6 month shown)"], use_contw = False, 
    facet_col_spacing = 0.11, key = "w_",
    y_var1 = yvars[0], y_var2 = yvars[1],
)

ui_render_landing_page(
    df_trend = ss.df_months_recent, df_age = ss.df_months_max_date, height = 800, width = None, 
    col_tit = ["Update status monthly data", "Monthly diseases-radar (Latest 2 years shown)"], use_contw = True, 
    facet_col_spacing = 0.05, key = "m_",
    y_var1 = yvars[0], y_var2 = yvars[1],
)

















