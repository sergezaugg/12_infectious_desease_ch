#--------------------             
# Author : Serge Zaugg
# Description : Visualize monthly data with trend
#--------------------

from streamlit import session_state as ss
from src.ui_elements import ui_render_ma_resid_page
import streamlit as st

with st.sidebar:
    st.markdown("""
    :primary[Summary:] Explore short-term trend from weekly incidence (only 2 diseases available).
    """)
    st.divider()

with st.spinner("Rendering plots"):
    ui_render_ma_resid_page(
        dat_long = ss.df_w_ma_long, 
        dat_wide = ss.df_w_ma_wide, 
        key = "ui_trend_w_", 
        left_title = "Short-term Trend from 10 weeks moving window",
        seasonality = "week")


