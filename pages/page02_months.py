#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
from utils import make_lineplot_all_by_disease

with st.sidebar:
    outcome_options = ["value", "incValue",  "pop"]
    selected_outcome = st.radio("Select outcome", options = outcome_options, index=0, key="k_p10_01")

fig = make_lineplot_all_by_disease(x = ss.df_months_all_concat, height = 5000, outcome = selected_outcome)

with st.container(border=True):
    st.plotly_chart(fig, use_container_width=True, key = "k_fig_monthly")





