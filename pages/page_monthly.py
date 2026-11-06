#--------------------             
# Author : Serge Zaugg
# Description : Visualize monthly data with trend
#--------------------

from streamlit import session_state as ss
from src.utils_ui import ui_render_ma_resid_page
import streamlit as st

with st.sidebar:
    st.markdown("""
    :primary[Summary:] Explore long-term trend from monthly incidence data for multiple diseases.
    """)

# title at top 
titl = """
    <span>Long-term trend from 12 month moving window (</span>
    <span style="color: #f5630f;">━━━━━━</span>
    <span>) and monthly values (</span>
    <span style="color: #13bee0;">━━━━━━</span>
    <span>)</span>
    """

with st.spinner("Rendering plots"):
    ui_render_ma_resid_page(
        dat_wide = ss.df_months_all_concat, 
        key = "ui_trend_m_", 
        left_title = titl,
        seasonality = "month")


