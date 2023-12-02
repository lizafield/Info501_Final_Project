import os 
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

#from utils.b2 import B2


# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
rural_data = 'Rural_vs_Urban_date.csv'



# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
#load_dotenv()

#load Backblaze connection
#b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
       #key_id=os.environ['B2_KEYID'],
       #secret_key=os.environ['B2_APPKEY'])



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

st.line_chart(flat_f1, x = 'Year', y = 'Percentage', color = 'World bank income group', #color_discrete_sequence = ['#332288','#44AA99','#88CCEE','#CC6677'],
               width = 1000, height = 600)



#grouped by WHO Region
grouped_f2 = df_rural_60_mf.groupby(['WHO region', 'Year'])['Percentage'].mean()
flat_f2 = grouped_f2.reset_index()

st.line_chart(flat_f2, x = 'Year', y = 'Percentage', color = 'WHO region', #color_discrete_sequence = ['#332288','#44AA99','#882255','#CC6677','#DDCC77','#88CCEE'],
               width = 1000, height = 600)


# ------------------------------
# PART 3 : Age Groups over Time by Country (selected)
# ------------------------------

st.write(
'''
### Change in Older Populations Living in Poverty by Age Group
Here, you can select a country to see how their older populations living in rural areas have changed over time.  This shows different age groups, starting with 60-64. 
'''
)

#list of countries to select from
countries_list = rural_df.Country.unique()

#dropdown selection for an individual country
sel_country = st.selectbox(
       'Country', countries_list)

#temp data frame for selected country
sel_country_df = rural_df.loc[(rural_df['Age group'] != '60+') & (rural_df['Sex'] == "Both sexes") & (rural_df['Residence area'] == 'Rural') & (rural_df['Country'] == sel_country)].reset_index()

#formatting a functioning table for the graph
grouped_f3 = sel_country_df.groupby(['Age group', 'Year'])['Percentage'].mean()
flat_f3 = grouped_f3.reset_index()

st.dataframe(flat_f3)
st.line_chart(flat_f3, x = 'Year', y = 'Percentage', color = 'Age group')
