#--------------------             
# Author : Serge Zaugg
# Description : define big UI elements here 
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
import plotly.express as px
from utils import make_lineplot_all_by_disease


labels = {
    "value": "Cases count",
    "incValue": "Cases per 10⁵ hab",  
    "pop": "Total population",
    "date" : "Date",
}


def ui_render_factplot_page(data, key, aa=1):
    df_options = ss.df_overview[['dis_abbrev', 'type']]
    # reduce options to diseases that exist in this time resolution
    dis_levels_exist =data['dis_abbrev'].unique()
    df_options = df_options[df_options['dis_abbrev'].isin(dis_levels_exist)]
    opt_types = df_options['type'].unique()

    with st.sidebar:
        outcome_options = ["value", "incValue"] # ,  "pop"]
        selected_outcome = st.radio("Select outcome", options = outcome_options, index=0, key= key+"_01", persist_state = "session", 
                                    horizontal=True, format_func=lambda x: labels[x],)
        sel_type = st.pills("Select disease type", options=opt_types, selection_mode="multi", persist_state = "session", key = key+"_02")
        opt_disea_subset = df_options[df_options['type'].isin(sel_type)]

        with st.form("disease_selection", border=False):
            sel_dis = st.pills("Select diseases", options = opt_disea_subset, selection_mode="multi", default = opt_disea_subset, 
                            persist_state = "session", key = key+"_03", format_func=lambda x: x[:9],)
            submitted = st.form_submit_button("Apply")

    # apply user selection upon user's confirmation
    if submitted:
        n_dis = len(sel_dis)
        df_plot = data[data['dis_abbrev'].isin(sel_dis)]
        fig = make_lineplot_all_by_disease(x = df_plot, n_facets = n_dis, outcome = selected_outcome, labels = labels)
        ss[key] = fig

    if key in ss:
        with st.container(border=True):
            st.plotly_chart(ss[key], use_container_width=True, key = "k_fig_yearly")
