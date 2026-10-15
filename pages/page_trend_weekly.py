#--------------------             
# Author : Serge Zaugg
# Description : Visualize monthly data with trend
#--------------------

from streamlit import session_state as ss
from ui_elements import ui_render_ma_resid_page
import streamlit as st

with st.sidebar:
    st.markdown("""
    :primary[Summary:] Explore long-term trend from weekly incidence (currently only 2 disease available).
    """)
    st.divider()

ui_render_ma_resid_page(dat_long = ss.df_w_ma_long, dat_wide = ss.df_w_ma_wide, key = "ui_trend_w_")


