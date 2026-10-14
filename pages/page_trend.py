
from streamlit import session_state as ss
from ui_elements import ui_render_ma_resid_page
import streamlit as st

with st.sidebar:
    st.markdown("""
    :primary[Summary:] Explore long-term trend from monthly incidence (reported cases) data for selectable subset of diseases.
    """)
    st.divider()

ui_render_ma_resid_page(dat_long = ss.df_m_ma_long, dat_wide = ss.df_m_ma_wide, key = "enxfhsnbdfhrgtzu")




