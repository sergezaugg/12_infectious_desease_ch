#--------------------             
# Author : Serge Zaugg
# Description : landing page
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
from ui_elements import ui_render_landing_page

with st.sidebar:
    st.markdown("""
    :primary[Summary:] Review update status of all monthly data and see estimated trends of the past two years. 
    """)
    st.divider()

ui_render_landing_page(
    df_trend = ss.df_weeks_filtered_2y, df_age = ss.df_weeks_max_date, height = 180 , width = 900, 
    col_tit = ["Update status weekly data", "Weekly diseases-radar"], use_contw = True, key = "w_"
)

ui_render_landing_page(
    df_trend = ss.df_months_filtered_2y, df_age = ss.df_months_max_date, height = 800, width = None, 
    col_tit = ["Update status monthly data", "Monthly diseases-radar"], use_contw = True, key = "m_"
)

















