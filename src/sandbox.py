#--------------------             
# Author : Serge Zaugg
# Description : misc stuff
#--------------------

import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from src.utils_dataprep import download_all_data




# # download and perp once
# di_downloded = download_all_data()
# di_downloded
# di_downloded[0].keys()
# di_downloded[0]['YELLOWFEVER_oblig']


# import pickle

# # download and perp once
# di_downloded = download_all_data()

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



