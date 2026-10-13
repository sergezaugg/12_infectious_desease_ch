#--------------------             
# Author : Serge Zaugg
# Description : refresh 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from utils import download_all_data
import time

c1, c2 = st.columns([15, 50])
with c1:
    dev_mode = st.text_input("Maintenance access: enter code", value="", type="password") == st.secrets['refreshcode']
    if dev_mode:
        with st.container(border=True, height = 400):    
            @st.cache_resource
            def get_refresh_state():
                return {"last_refresh": 0.0}
            refresh_state = get_refresh_state()
            COOLDOWN = 300  # 5 minutes
            if st.button("🔄 Refresh data"):
                elapsed = time.time() - refresh_state["last_refresh"]
                if elapsed < COOLDOWN:
                    st.warning(f"Please wait {int(COOLDOWN - elapsed)} seconds before refreshing again.")
                else:
                    refresh_state["last_refresh"] = time.time()
                    del ss["di_prep"]
                    download_all_data.clear()
                    st.rerun()

   


