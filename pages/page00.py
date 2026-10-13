#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import get_overview_df


n_dis = ss.df_overview.shape[0]

st.text(f"Nb diseases from mandatory reporting system in this dataset N = {int(n_dis)}")

def highlight_yes(v):
    if isinstance(v, str):
        v = v.strip().lower()
        if v == "yes":
            return "background-color: darkgreen"
        if v == "no":
            return "background-color: darkred"
    return ""

st.dataframe(
    ss.df_overview.style.map(highlight_yes),
    hide_index=True,
    width="content",
    height=1500,
    column_config={
        "disease": st.column_config.Column(width=200),
        "description": st.column_config.Column(width=700)
    }
)



