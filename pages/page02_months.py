#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

from streamlit import session_state as ss
from ui_elements import ui_render_factplot_page

ui_render_factplot_page(data = ss.df_months_all_concat, key = "fig_m", seasonality = "month")
