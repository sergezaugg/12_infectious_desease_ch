#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
from utils import make_lineplot_by_age_and_sex


for k in ss.df_years.keys():
    df = ss.df_years[k] 
    fig = make_lineplot_by_age_and_sex(df, k)
    st.plotly_chart(fig, use_container_width=True, key = k)

