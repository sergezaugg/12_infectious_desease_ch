#--------------------             
# Author : Serge Zaugg
# Description : Page with concise background info and credits
#--------------------

import streamlit as st

col_aa, col_bb, = st.columns([0.50, 0.40])
with col_aa: 
    with st.container(border=True):
        st.markdown('''
        ### About this web-app
        The Swiss Infectious Disease Explorer gives quick and descriptive overview of latest available data on 
        42 infectious disease in Switzerland.
        Simple and general analysis methods are used intentionally and the focus is on transparent and informative visualization.
        ''') 

    with st.container(border=True):
        st.markdown('''    
        ### Credits 
        Data kindly compiled and curated by the [Swiss Federal Office of Public Health (FOPH)](https://www.bag.admin.ch/).   
        The data is provided weekly (updated Wednesdays) on this [API](https://www.idd.bag.admin.ch/portal-data).   
        A visual data explorer of FOPH can be found [here](https://www.idd.bag.admin.ch/dataexplorer).   
        ''') 

    with st.container(border=True):
        st.markdown('''   
        ### Author
        Created by: :primary[[Serge Zaugg](https://www.linkedin.com/in/dkifh34rtn345eb5fhrthdbgf45/)]     
        GitHub: :primary[[Pollito-ML](https://github.com/sergezaugg)]
        ''')

