#--------------------             
# Author : Serge Zaugg
# Description : Visualize monthly data 
#--------------------

from streamlit import session_state as ss
from src.ui_elements import ui_render_basic_facet_plot_page
import streamlit as st

with st.sidebar:
    st.markdown("""
    :primary[Summary:] Explore incidence history (reported cases) from monthly data for selectable subset of diseases.
    """)
    st.divider()

ui_render_basic_facet_plot_page(data = ss.df_months_all_concat, key = "ui_trace_m_", seasonality = "month")


