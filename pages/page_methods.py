import streamlit as st


col_aa, col_bb, = st.columns([0.50, 0.50])
with col_aa: 
        
    st.markdown('''
        Most of this app shows purely descriptive plots, so not much methods here, just this:
        Long-Term Trend is estimated from  monthly data.
        A median–mean smoother is used. This is a two-step operation passing the data first through a moving median stage (window size 12 months) 
        for an outlier-robust estimation of trend and to remove seasonality, if present.
        In second step the data is piped through a more localized moving mean stage to restore natural continuity.
        (An academic expression to say "look better")
        ''')

