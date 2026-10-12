#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
from utils import make_lineplot_by_age_and_sex, data_select_only_all_groups

df_weeks_all = data_select_only_all_groups(ss.df_weeks)

for k in df_weeks_all.keys():
    df = df_weeks_all[k] 
    fig = make_lineplot_by_age_and_sex(df, k)
    st.plotly_chart(fig, use_container_width=True, key = k)
   
    
