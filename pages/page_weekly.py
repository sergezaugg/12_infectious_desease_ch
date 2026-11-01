#--------------------             
# Author : Serge Zaugg
# Description : Visualize weekly data with trend
#--------------------

from streamlit import session_state as ss
from src.utils_ui import ui_render_ma_resid_page
import streamlit as st

with st.sidebar:
    st.markdown("""
    :primary[Summary:] Explore short-term trend from weekly incidence (only 2 diseases available).
    """)
    st.divider()

# title at top 
titl = """
    <span>Short-term trend from 10 weeks moving window (</span>
    <span style="color: #f5630f;">━━━━━━</span>
    <span>) and monthly values (</span>
    <span style="color: #13bee0;">━━━━━━</span>
    <span>)</span>
    """

with st.spinner("Rendering plots"):
    ui_render_ma_resid_page(
        dat_wide = ss.df_weeks_all_concat, 
        key = "ui_trend_w_", 
        left_title = titl,
        seasonality = "week")


