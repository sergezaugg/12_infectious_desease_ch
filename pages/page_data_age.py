#--------------------             
# Author : Serge Zaugg
# Description : landing page
#--------------------

import streamlit as st
from streamlit import session_state as ss
import plotly.express as px

# ss.df_filtered 
# ss.df_filt_max_date 
# st.dataframe(ss.df_filtered_1y)
# st.text(ss.ref_date)

colrs = ["#eeeeee", "#4a4d4d", "#f5630f"]


fig = px.line(
    data_frame = ss.df_filtered_1y,
    x = "date",
    y = "resp_var",
    color = "measure",
    facet_col= "disease",
    facet_col_wrap=7,
    facet_row_spacing = 0.05,
    facet_col_spacing = 0.04,
    # markers=True,
    height = 700,
    # labels=labels,
    color_discrete_map={
        "incValue":    colrs[1],
        "incValue_ma": colrs[2],
        },
    )
fig.update_layout(
    showlegend=False,
    margin=dict(l=50, r=50, t=50, b=40),
    legend=dict(title=None, bordercolor="white", borderwidth=1, orientation="h", x=0, xanchor="left", y=1.015, yanchor="top",),
    )
fig.update_xaxes(
    showline = True, linewidth=1.8, mirror=True, 
    title_font=dict(size=14),
    dtick="M6",
    gridcolor="#535053",
    showgrid=True,
    title_text=None,
    # ticks="inside",
    showticklabels=False, 
    ticks=""
    )   
fig.update_yaxes(
    matches=None,
    showticklabels=True,
    ticks="inside",
    showline=True,
    linewidth=1.8,
    mirror=True,
    title_font=dict(size=16),
    rangemode="tozero",
    title_text=None
)
for ann in fig.layout.annotations:
    ann.text = ann.text.replace("disease=", "")
    ann.update(y = ann.y + 0.008, yanchor="top")

fig.add_vline(x=ss.ref_date,line_color="green",line_width=2,line_dash="dot",)







#---------------------------------------
# data age 

fig_bar = px.bar(
    data_frame=ss.df_filt_max_date ,
    x = 'days_elapsed',
    y = 'disease',
    height = 800,
    orientation="h",
    )
fig_bar.update_xaxes(range=[30, None])
fig_bar.update_yaxes(showline = True, linewidth=1.8, mirror=True, )
fig_bar.update_xaxes(showline = True, linewidth=1.8, mirror=True, )
fig_bar.update_traces(width=0.5)

fig_bar.update_layout(
    margin=dict(l=50, r=10, t=50, b=40)
)


c0, c1 = st.columns([2,8])
with c0:
    st.plotly_chart(fig_bar , use_container_width=False, key = "aaaaaa")
with c1:
    st.plotly_chart(fig,      use_container_width=True, key = "afbafbsefb")





