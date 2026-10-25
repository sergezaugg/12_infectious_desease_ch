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



import pickle

# download and perp once
di_downloded = download_all_data(22)

# Save
with open("temp/bag_data.pkl", "wb") as f:
    pickle.dump(di_downloded, f)

# Reload
with open("temp/bag_data.pkl", "rb") as f:
    di_reloded = pickle.load(f)


len(di_downloded)
len(di_reloded)


di_data, data_version, n_files, ts_downl = di_downloded
di_data, data_version, n_files, ts_downl = di_reloded

di_data.keys()
di_data['BOTULISM_oblig'].shape













# # play with API

# import numpy as np
# import pandas as pd 
# import plotly.express as px
# import streamlit as st
# from streamlit import session_state as ss
# import requests
# import io
# from datetime import datetime

# API_BASE_URL = "https://api.idd.bag.admin.ch/api/v1"




# full_query_string = f"{API_BASE_URL}/data/version"

# full_query_string = f"{API_BASE_URL}/data/sets"



# r = requests.get(full_query_string, allow_redirects=True)
# data_version = r.json()


# full_query_string = f"{API_BASE_URL}/export/20261014/files"
# full_query_string = f"{API_BASE_URL}/export/20261021/files"
# full_query_string = f"{API_BASE_URL}/export/latest/files"
# full_query_string = f"{API_BASE_URL}/export/20261020/files" # 'status': 400, 'error'

# r = requests.get(full_query_string, allow_redirects=True)
# r.status_code

# data_file_list = r.json()

# data_file_list =[a for a in data_file_list if "oblig" in a]

# n_files = len(data_file_list)

# data_di = {}
# for li_index in range(len(data_file_list)):
#     print(li_index)
#     data_set_name = data_file_list[li_index]
#     print(data_set_name)
#     full_query_string = f"{API_BASE_URL}/export/latest/" + data_set_name + '/csv'
#     r = requests.get(full_query_string, allow_redirects=True)
#     raw_text = r.text
#     df = pd.read_csv(io.StringIO(raw_text, newline='\n')  , sep=",")
#     print(df.shape)
#     data_di[data_set_name] = df

# ts = datetime.now().strftime("%Y-%m-%d %H:%M")

# # return data_di, data_version, n_files, ts




