#--------------------             
# Author : Serge Zaugg
# Description : Page with concise background info and credits
#--------------------

import streamlit as st

col_aa, col_bb, = st.columns([0.50, 0.50])
with col_aa: 
    with st.container(border=True, ):
        st.markdown('''
        ### INFO
        The Swiss Infectious Disease Explorer is an app to get a quick and descriptive overview of latest available data on 
        42 infectious disease in Switzerland.
        High quality Surveillance data is hard to gather and compile and the data therefore typically has a latency of a few weeks.
        Simple and general analysis methods are used intentionally and the focus is on transparent and informative visualization.

        ''')
        st.markdown('''
        ### CREDITS
        Data kindly provided weekly on this [API](https://www.idd.bag.admin.ch/portal-data) by the Swiss Federal Office of Public Health ([FOPH](https://www.bag.admin.ch/)).
        ''')
        st.markdown('''### LINKS ''')
       
        st.markdown(
            '[Official visual frontend of FOPH](https://www.idd.bag.admin.ch/dataexplorer)',
            unsafe_allow_html=False)

        st.markdown(
            '[Mandatory reporting (oblig)](https://www.idd.bag.admin.ch/survey-systems/oblig)',
            unsafe_allow_html=False)




col_aa, col_bb, = st.columns([0.50, 0.50])
with col_aa: 
    with st.container(border=True, ):
        
        st.markdown('''
            ### CASE REPORTING BIAS   
            Reported cases do not necessarily reflect the true incidence of a disease.
            Underreporting may occur due to limited testing, asymptomatic infections, or incomplete reporting.
            Reporting practices can vary across regions, time periods, and healthcare settings.
            Observed trends should therefore be interpreted with caution, as changes may reflect reporting differences rather than actual disease dynamics.
            ''')

        st.markdown('''
            ### MEDIAN–MEAN SMOOTHER  
            Most of this app shows purely descriptive plots, so not much methods here, just this:
            Long-Term Trend is estimated from  monthly data.
            A median–mean smoother is used. This is a two-step operation passing the data first through a moving median stage (window size 12 months) 
            for an outlier-robust estimation of trend and to remove seasonality, if present.
            In second step the data is piped through a more localized moving mean stage to restore natural continuity.
            (An academic expression to say "look better")
            ''')