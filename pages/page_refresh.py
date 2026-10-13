#--------------------             
# Author : Serge Zaugg
# Description : refresh 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from utils import download_all_data

if st.button("🔄 Refresh data"):
    del ss["di_prep"]
    download_all_data.clear()
    st.rerun()




