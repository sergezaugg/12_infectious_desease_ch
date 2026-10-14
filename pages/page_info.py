#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss

n_dis = ss.df_overview.shape[0]

df_display = ss.df_overview

cols = ['disease', 'dis_abbrev', 'type', 'description', 'yearly', 'monthly', 'weekly', ]
df_display = df_display[cols]

# st.text(ss.df_overview.columns)

st.text(f"Nb diseases from mandatory reporting system in this dataset N = {int(n_dis)}")
st.text("FOPH Data Version:  " + ss.data_version['name'])
st.text("Downloaded on:  "     + ss.ts_downl)

def highlight_yes(v):
    if isinstance(v, str):
        v = v.strip().lower()
        if v == "yes":
            return "background-color: darkgreen"
        if v == "no":
            return "background-color: darkred"
    return ""

st.dataframe(
    df_display.style.map(highlight_yes),
    hide_index=True,
    width="content",
    height=1600,
    column_config={
    "disease": st.column_config.Column("Disease", width=200),
    "description": st.column_config.Column("Description", width=500),
    'dis_abbrev': st.column_config.Column("Shortname", width=100), 
    'type': st.column_config.Column("Transm.", width=100),  
    'yearly': st.column_config.Column("Avail. yearly", width=100), 
    'monthly': st.column_config.Column("Avail. monthly", width=100), 
    'weekly': st.column_config.Column("Avail. weekly", width=100),

}

 

)



