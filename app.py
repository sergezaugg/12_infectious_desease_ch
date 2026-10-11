#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
from streamlit import session_state as ss
import numpy as np
import plotly.express as px
import pandas as pd



#------------------------------
# prepare app 
st.set_page_config(layout = "wide", initial_sidebar_state = "expanded", page_icon='pics/z_logo_blue.png')
st.logo(image='pics/z_logo_blue.png', size="large", link="https://github.com/sergezaugg")
pd.set_option('display.max_rows', 500)



# build sidebar
with st.sidebar:
    st.markdown(f"""# :primary[**Swiss Infectious Disease Explorer**] """)

# (3) main navigation
pages = [
    st.Page("page00.py",  title="Summary tables"),
    st.Page("page01_weeks.py",  title="Plots weekly"),
    st.Page("page02_months.py",  title="Plots monthly"),
    st.Page("page02_years.py",  title="Plots yearly"),
    st.Page("page02.py",  title="Credits"),
    ]
pg = st.navigation(pages, position = "top")
pg.run()





