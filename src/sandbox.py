#--------------------             
# Author : Serge Zaugg
# Description : misc stuff
#--------------------

import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from src.utils import download_all_data
# from src.utils import data_select_years, data_select_months, data_select_weeks, data_select_only_all_groups, stack_dict_of_dfs
# from src.utils import get_overview_df
# from resources.styles import apply_global_styles



# import pickle

# # download and perp once
# di_downloded = download_all_data(22)

# # Save
# with open("temp/bag_data.pkl", "wb") as f:
#     pickle.dump(di_downloded, f)

# # Reload
# with open("temp/bag_data.pkl", "rb") as f:
#     di_reloded = pickle.load(f)


# len(di_downloded)
# len(di_reloded)

# di_data, data_version, n_files, ts_downl = di_downloded
# di_data, data_version, n_files, ts_downl = di_reloded

# di_data.keys()
# di_data['BOTULISM_oblig'].shape



