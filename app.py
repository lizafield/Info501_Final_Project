import os 
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from utils.b2 import B2


# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
rural_data = 'Rural_vs_Urban_date.csv'



# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_KEYID'],
        secret_key=os.environ['B2_APPKEY'])



# ------------------------------------------------------
#                         APP
# ------------------------------------------------------

st.title('Older Populations Living in Rural Areas')


# ------------------------------
# PART 1 : Filter Data
# ------------------------------























