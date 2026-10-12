#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss

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
df_overview = d.fillna("No")

# merge-in metadata 
df_descript = pd.read_csv("resources/disease_description.txt", sep=",")
df_overview = df_overview.merge(df_descript, 'outer', on = "disease")

#----------------------------
# display 

def highlight_yes(v):
    if isinstance(v, str):
        v = v.strip().lower()
        if v == "yes":
            return "background-color: darkgreen"
        if v == "no":
            return "background-color: darkred"
    return ""

st.dataframe(
    df_overview.style.map(highlight_yes),
    hide_index=True,
    width="content",
    height=1500,
    column_config={
        "disease": st.column_config.Column(width=200),
        "description": st.column_config.Column(width=700)
    }
)



