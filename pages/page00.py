#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss

# st.dataframe(ss.df_years_all_concat.head())


a = ss.df_weeks_all_concat.groupby(["temporal_type", "disease"]).size().reset_index()
b = ss.df_months_all_concat.groupby(["temporal_type", "disease"]).size().reset_index()
c = ss.df_years_all_concat.groupby(["temporal_type", "disease"]).size().reset_index()

a['temporal_type'] = "Yes"
b['temporal_type'] = "Yes"
c['temporal_type'] = "Yes"

a.rename(columns={"temporal_type": "weekly"}, inplace=True)
b.rename(columns={"temporal_type": "monthly"}, inplace=True)
c.rename(columns={"temporal_type": "yearly"}, inplace=True)

a = a.drop(columns=[0], errors="ignore")
b = b.drop(columns=[0], errors="ignore")
c = c.drop(columns=[0], errors="ignore")

d = a.merge(b, 'outer', on = "disease").merge(c, 'outer', on = "disease")

d = d[["disease", "yearly", "monthly", "weekly", ]]
d = d.fillna("No")
# st.dataframe(d, hide_index=True, width = "content", height=1500)

def highlight_yes(v):
    if isinstance(v, str):
        v = v.strip().lower()
        if v == "yes":
            return "background-color: darkgreen"
        if v == "no":
            return "background-color: darkred"
    return ""

st.dataframe(
    d.style.map(highlight_yes),
    hide_index=True,
    width="content",
    height=1500
)


