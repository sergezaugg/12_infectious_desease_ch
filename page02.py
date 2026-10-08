#--------------------             
# Author : Serge Zaugg
# Description : Page with concise background info and credits
#--------------------

import streamlit as st

col_aa, col_bb, = st.columns([0.50, 0.05])
with col_aa: 
    with st.container(border=True, ):
        st.markdown('''
        ### CREDITS
        Data kindly provided weekly on this [API](https://www.idd.bag.admin.ch/portal-data) by the Swiss Federal Office of Public Health ([FOPH](https://www.bag.admin.ch/)).
        ''')
        st.markdown('''### LINKS ''')
        st.page_link("https://www.idd.bag.admin.ch/dataexplorer", label="Official visual frontend of FOPH")
        st.page_link("https://www.idd.bag.admin.ch/survey-systems/oblig", label="Mandatory reporting (oblig)")
