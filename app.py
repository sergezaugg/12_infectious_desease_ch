#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import numpy as np
import plotly.express as px
st.set_page_config(layout="wide", initial_sidebar_state = "expanded")

# build sidebar
with st.sidebar:
    st.markdown(f"""# :primary[**Swiss desease Explorer**] """)

# (3) main navigation
pages = [
    st.Page("page00.py",  title="Dev - Explore"),
    st.Page("page01_weeks.py",  title="Basic plots weeks"),
    st.Page("page02_months.py",  title="Basic plots months"),
    st.Page("page02.py",  title="Credits"),
    ]
pg = st.navigation(pages, position = "top")
pg.run()





