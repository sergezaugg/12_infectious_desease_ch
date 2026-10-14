#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

from streamlit import session_state as ss
from ui_elements import ui_render_basic_facet_plot_page
import streamlit as st

ui_render_basic_facet_plot_page(data = ss.df_months_all_concat, key = "fig_m", seasonality = "month")

with st.sidebar:
    st.divider()
    st.markdown("""
    :primary[Summary:] Explore monthly data. 
    """)
