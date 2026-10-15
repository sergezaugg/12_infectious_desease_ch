#--------------------             
# Author : Serge Zaugg
# Description : define big UI elements here 
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
import plotly.express as px

# ---------------------------
# ui elements  

def ui_sel_country_in_two_steps(data, key):
    """ Re-usable st element to select countries in two steps"""
    # get full list of coutries 
    df_options = ss.df_overview[['dis_abbrev', 'type']]
    # reduce options to diseases that exist in current data
    dis_levels_exist =data['dis_abbrev'].unique()
    df_options = df_options[df_options['dis_abbrev'].isin(dis_levels_exist)]
    # get full list of disease types 
    opt_types = df_options['type'].unique()

    # step 1 : select a subset of disease types 
    def caba_update_dis_options():
        ss[key+"_03"] = df_options.loc[df_options['type'].isin(st.session_state[key + "_02"]), 'dis_abbrev'].tolist()
    sel_type = st.pills("Select disease type", options=opt_types, selection_mode="multi", 
        default = opt_types[0],
        on_change= caba_update_dis_options,
        key = key+"_02", persist_state = "session")

    # step 2 : select diseases within selected subset of disease types 
    opt_disea_subset = df_options.loc[df_options['type'].isin(sel_type), 'dis_abbrev'].tolist()
    sel_dis = st.multiselect("Select diseases", 
        options = opt_disea_subset, 
        key = key+"_03", format_func=lambda x: x[:9],
        default = opt_disea_subset,  
        # persist_state = "session"
        )

    return sel_dis


def ui_render_basic_facet_plot_page(data, key, seasonality):
   
    with st.sidebar:
        outcome_options = ["incValue", "value"] # ,  "pop"]
        selected_outcome = st.radio("Select outcome", options = outcome_options, index=0, key= key+"_01", persist_state = "session", 
                                    horizontal=True, format_func=lambda x: ss.labels[x],)

        sel_dis = ui_sel_country_in_two_steps(data = data, key = key + "two_steps")


    # apply user selection upon user's confirmation
    if True:
        n_dis = len(sel_dis)
        df_plot = data[data['dis_abbrev'].isin(sel_dis)]
        fig_a = make_lineplot_all_by_disease(x = df_plot, xvar = "date",  col_var = None,   n_facets = n_dis, outcome = selected_outcome, 
                                            labels = ss.labels, show_x_grid = True,
                                            facet_labels = False)
     
        if seasonality == "month":
            fig_b = make_lineplot_all_by_disease(x = df_plot, xvar = "month", col_var = "year", n_facets = n_dis, outcome = selected_outcome, 
                                            labels = ss.labels, show_x_grid = False,
                                             facet_labels = True)
        elif seasonality == "week":            
            # enforce sorting 
            df_plot =df_plot.sort_values(['disease', 'temporal_type', 'week', 'date', ])
            fig_b = make_lineplot_all_by_disease(x = df_plot, xvar = "week", col_var = "year", n_facets = n_dis, outcome = selected_outcome, 
                                            labels = ss.labels, show_x_grid = False,
                                            facet_labels = True)
        elif seasonality == "year": 
            fig_b = px.line()
        else:
            print("shit")

        ss[key] = [fig_a, fig_b]

    if key in ss:
        with st.container(border=True):
            c1,c2 = st.columns([4,2])
            with c1:
                st.text("Reported Cases History")
                st.plotly_chart(ss[key][0], use_container_width=True, key = "k_fig_a")
            with c2:
                st.text("Reported Cases By Month")
                st.plotly_chart(ss[key][1], use_container_width=True, key = "k_fig_b")


def ui_render_ma_resid_page(dat_long, dat_wide, key):

    with st.sidebar:
            # outcome_options = ["incValue", "value"] # ,  "pop"]
            # selected_outcome = st.radio("Select outcome", options = outcome_options, index=0, key= key+"_01", persist_state = "session", 
            #                             horizontal=True, format_func=lambda x: ss.labels[x],)

            sel_dis = ui_sel_country_in_two_steps(data = dat_long, key = "two_steps_ma" + key)


    n_dis = len(sel_dis)
    df_plot_long = dat_long[dat_long['dis_abbrev'].isin(sel_dis)]
    df_plot_wide = dat_wide[dat_wide['dis_abbrev'].isin(sel_dis)]

    fig_smo, fig_res  = make_plots_smo_resid(
        df_long = df_plot_long, 
        df_wide = df_plot_wide, 
        xvar = "date", outcome = "resp_var", labels = ss.labels, n_facets = n_dis)

    with st.container(border=True):
        c0, c1 = st.columns([7,8])
        with c0:
            st.text("Long-Term Trend From Monthly Data")
            st.plotly_chart(fig_smo, use_container_width=True, key = "two_steps_smo")
        with c1:   
            st.text("Residuals From Trend") 
            st.plotly_chart(fig_res, use_container_width=True, key = "two_steps_res")



# ---------------------------
# plots 


@st.cache_data(show_spinner="Rendering plots")
def make_lineplot_all_by_disease(x, xvar, col_var, n_facets, outcome, labels, facet_labels, show_x_grid):

    # pre-compute vertical spacings dependent on n_facets
    facet_height = 150
    spacing_px = 60
    height_b = (n_facets * facet_height + (n_facets - 1) * spacing_px + 200)
    facet_row_spacing = spacing_px / height_b

    fig = px.line(
        data_frame = x,
        x = xvar,
        y = outcome,
        color = col_var,
        facet_row= "disease",
        facet_row_spacing = facet_row_spacing,
        markers=True,
        height = height_b,
        labels=labels,
        )

    fig.update_traces(marker=dict(size=5))   
    fig.update_layout(
        showlegend=False,
        margin=dict(l=30, r=30, t=50, b=40),
        legend=dict(title=None, bordercolor="white", borderwidth=1, orientation="h", x=0, xanchor="left", y=1.015, yanchor="top",),
        )
    fig.update_xaxes(
        showline = True, linewidth=1.8, mirror=True, showticklabels=True, ticks="inside",
        title_font=dict(size=14),
        dtick="M12", tick0="2000-01-01", gridcolor="#535053",
        showgrid=show_x_grid, 
        )   
    fig.update_yaxes(
        matches=None,
        showline = True, linewidth=1.8, mirror=True,
        title_font=dict(size=16),
        range=[0.0, None]
        ) 

    fig.for_each_annotation(lambda a: a.update(x=1.015,font=dict(size=16)))
    for annotation in fig.layout.annotations:
        annotation.text = annotation.text.replace("disease=", "")
        annotation.textangle = 90
    if facet_labels == False:
        fig.for_each_annotation(lambda a: a.update(text=""))    

    return fig


@st.cache_data(show_spinner="Rendering plots")
def make_plots_smo_resid(df_long, df_wide, xvar, outcome, labels, n_facets):

    """  """
    # pre-compute vertical spacings dependent on n_facets
    facet_height = 150
    spacing_px = 60
    height_b = (n_facets * facet_height + (n_facets - 1) * spacing_px + 200)
    facet_row_spacing = spacing_px / height_b

    colrs = ["#eeeeee", "#13bee0", "#f5630f"]

    fig_smo = px.line(
        data_frame = df_long,
        x = xvar,
        y = outcome,
        color = "measure",
        facet_row= "disease",
        facet_row_spacing = facet_row_spacing, # 0.01,
        height = height_b, # 6500,
        color_discrete_map={
            "incValue":    colrs[1],
            "incValue_ma": colrs[2],
        },
        labels=labels,
        )

    # add margin left and right 
    x_min = df_long["date"].min()
    x_max = df_long["date"].max()
    margin = (x_max - x_min) * 0.03
    fig_smo.update_xaxes(range=[x_min - margin, x_max + margin])

    fig_smo.update_layout(
        showlegend=False,
        margin=dict(l=30, r=30, t=50, b=40),
        )
    fig_smo.update_xaxes(
        showline = True, linewidth=1.8, mirror=True, showticklabels=True, ticks="inside",
        title_font=dict(size=14),
        dtick="M12", tick0="2000-01-01", gridcolor="#535053",
        showgrid=False, 
        )   
    fig_smo.update_yaxes(
        matches=None,
        showline = True, linewidth=1.8, mirror=True,
        title_font=dict(size=16),
        range=[0.0, None]
        ) 
    fig_smo.for_each_annotation(lambda a: a.update(text=""))    




    # ------------------

    fig_res = px.line(
        data_frame = df_wide,
        x = xvar,
        y = "residuals",
        facet_row= "disease",
        facet_row_spacing = facet_row_spacing,
        height = height_b,
        labels=labels,
        color_discrete_sequence=[colrs[0]],
        )
    # add margin left and right 
    x_min = df_wide["date"].min()
    x_max = df_wide["date"].max()
    margin = (x_max - x_min) * 0.03
    fig_res.update_xaxes(range=[x_min - margin, x_max + margin])
    
    fig_res.add_hline(y=0.0, line_color=colrs[2], line_width=2)
    fig_res.update_layout(
        showlegend=False,
        margin=dict(l=50, r=150, t=50, b=40),
        )
    fig_res.update_xaxes(
        showline = True, linewidth=1.8, mirror=True, showticklabels=True, ticks="inside",
        title_font=dict(size=14),
        dtick="M12", tick0="2000-01-01", gridcolor="#535053",
        showgrid=False, 
        )   
    fig_res.update_yaxes(
        matches=None,
        showline = True, linewidth=1.8, mirror=True,
        title_font=dict(size=16),
        range=[0.0, None]
        ) 
    fig_res.for_each_annotation(lambda a: a.update(x=1.015,font=dict(size=16)))
    for annotation in fig_res.layout.annotations:
        annotation.text = annotation.text.replace("disease=", "")
        annotation.textangle = 90

    return fig_smo, fig_res    







