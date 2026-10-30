#--------------------             
# Author : Serge Zaugg
# Description : Visualize yearly data 
#--------------------

from streamlit import session_state as ss
from src.ui_elements import ui_render_basic_facet_plot_page, make_barplot_by_disease_dense_wrapped
import streamlit as st

with st.sidebar:
    st.markdown("""
    :primary[Summary:] Explore incidence history (reported cases) from yearly data for selectable subset of diseases.
    """)
    st.divider()

ui_render_basic_facet_plot_page(
    data = ss.df_years_all_concat, 
    key = "ui_trace_y_", 
    plotfun = make_barplot_by_disease_dense_wrapped
    )



