#--------------------             
# Author : Serge Zaugg
# Description : Visualize weekly data 
#--------------------

from streamlit import session_state as ss
from src.ui_elements import ui_render_basic_facet_plot_page, make_lineplot_all_by_disease
import streamlit as st

with st.sidebar:
    st.markdown("""
    :primary[Summary:] Explore incidence history (reported cases) from weekly data for selectable subset of diseases. 
    """)
    st.divider()


# st.write(ss.df_weeks_all_concat)    

ui_render_basic_facet_plot_page(
    data = ss.df_weeks_all_concat, 
    key = "ui_trace_w_", 
    seasonality = "week",
    plotfun = make_lineplot_all_by_disease
    )


