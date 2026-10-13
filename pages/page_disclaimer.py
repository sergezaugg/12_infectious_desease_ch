#--------------------             
# Author : Serge Zaugg
# Description : Page with concise background info and credits
#--------------------

import streamlit as st

col_aa, col_bb, = st.columns([0.50, 0.05])
with col_aa: 
    with st.container(border=True, ):
        st.markdown('''
        ### Disclaimer
        This dashboard provides visualizations of infectious diseases surveillance data from the API of teh Swiss Federal Office of Public Health. 
        The dashboard is an independent project and is not an official FOPH product, nor is it endorsed by the FOPH. 
        This dashboard is intended for exploration and informational purposes. 
        It is not intended to provide medical advice, diagnosis, or to replace official public-health information or guidance.
        ''')
       
