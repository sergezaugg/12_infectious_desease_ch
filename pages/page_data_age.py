



import streamlit as st
from streamlit import session_state as ss
import plotly.express as px

# ss.df_filtered 
# ss.df_filt_max_date 

st.text(ss.df_filt_max_date.shape)

fig = px.bar(
    data_frame=ss.df_filt_max_date ,
    x = 'disease',
    y = 'days_elapsed',
    height = 500
    )

st.plotly_chart(fig, use_container_width=True, key = "aaaaaa")


