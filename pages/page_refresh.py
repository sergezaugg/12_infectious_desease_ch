#--------------------             
# Author : Serge Zaugg
# Description : refresh 
#--------------------

import streamlit as st
from streamlit import session_state as ss
from utils import download_all_data

c1, c2 = st.columns([15, 50])
with c1:
    # password protected maintenance dev-mode
    dev_mode = st.text_input("🔧🛠️ Maintenance access: enter code 🍴🥄", value="", type="password") == st.secrets['maintenancecode']
    if dev_mode:
        with st.container(border=True, height = 400):    
            if st.button("🔄 Refresh data"):
                del ss["di_prep"]
                download_all_data.clear()
                st.rerun()


# st.write(dict(st.session_state))
# st.write({k: v for k, v in st.session_state.items() if k.startswith("fig")})
# st.write({k for k, v in st.session_state.items() if k.startswith("two_steps")})
# st.write({k for k, v in st.session_state.items() })
st.write([k for k in st.session_state ])
