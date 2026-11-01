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
    :primary[Upper panel:] Review past 6 months of diseases with weekly data.  

    :primary[Lower panel:] Review past 24 months (2 years) of diseases with monthly data.  
    """)
    st.divider()

ui_render_landing_page(
    df_trend = ss.df_weeks_recent, df_age = ss.df_weeks_max_date, height = 180 , width = 800, 
    col_tit = ["Update status weekly data", "Weekly diseases-radar (Latest 6 month shown)"], use_contw = False, 
    facet_col_spacing = 0.11, key = "w_",
    y_var1 = "incValue", y_var2 = "incValue_ma" 
    # y_var1 = "value", y_var2 = "value_ma" 
)

ui_render_landing_page(
    df_trend = ss.df_months_recent, df_age = ss.df_months_max_date, height = 800, width = None, 
    col_tit = ["Update status monthly data", "Monthly diseases-radar (Latest 2 years shown)"], use_contw = True, 
    facet_col_spacing = 0.05, key = "m_",
    y_var1 = "incValue", y_var2 = "incValue_ma" 
)

















