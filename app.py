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
#load_dotenv()

# load Backblaze connection
#b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
       # key_id=os.environ['B2_KEYID'],
       # secret_key=os.environ['B2_APPKEY'])



# ------------------------------------------------------
#                         APP
# ------------------------------------------------------

st.title('Older Populations Living in Rural Areas')


# ------------------------------
# PART 1 : Filter Data
# ------------------------------
#importing the file, a temp countermeasure until I can get backblaze working correctly
df = pd.read_csv('./Rural_vs_Urban_data.csv' , encoding='latin-1')

#renaming column 
r_df = df.rename(columns={"Value Numeric" : "Percentage"})

#dropping unnecessary columns
rural_df = r_df.drop(columns=['Indicator', 'Value String'])

#creating new df that shows rows for 60+, both sexes, and rural areas.  This gives a good baseline to start with
df_rural_60_mf = rural_df.loc[(rural_df['Age group'] == '60+') & (rural_df['Sex'] == "Both sexes") & (rural_df['Residence area'] == 'Rural')]


# ------------------------------
# PART 2 : YOY by Income/Region
# ------------------------------

st.write(
'''
### Rural Populations 1980 to 2015
Below are graphs depicting the change in people aged 60+ living in rural areas.  Countries are grouped by World Bank Income Groups (figure 1) and WHO Region (figure 2). 
'''
)


#grouped by income group
grouped_f1 = df_rural_60_mf.groupby(['World bank income group', 'Year'])['Percentage'].mean()
flat_f1 = grouped_f1.reset_index()

fig_1 = px.line(flat_f1, x = 'Year', y = 'Percentage', color = 'World bank income group', color_discrete_sequence = ['#332288','#44AA99','#88CCEE','#CC6677'],
               width = 1000, height = 600, markers = True)
fig_1.update_yaxes(range=[0,100])
st.plotly_chart(fig_1, use_container_width = True)


#grouped by WHO Region
grouped_f2 = df_rural_60_mf.groupby(['WHO region', 'Year'])['Percentage'].mean()
flat_f2 = grouped_f2.reset_index()

fig_2 = px.line(flat_f2, x = 'Year', y = 'Percentage', color = 'WHO region', color_discrete_sequence = ['#332288','#44AA99','#882255','#CC6677','#DDCC77','#88CCEE'],
               width = 1000, height = 600, markers = True)
fig_2.update_yaxes(range=[0,100])
st.plotly_chart(fig_2, use_container_width = True)







