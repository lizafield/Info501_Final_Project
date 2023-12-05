import os 
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import tools
import matplotlib.pyplot as plt

#from utils.b2 import B2


# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
rural_data = 'Rural_vs_Urban_date.csv'



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
Below are graphs depicting the change over time in people aged 60+ living in rural areas.  Countries are grouped by World Bank Income Groups (figure 1) and WHO Region (figure 2). 
'''
)


#grouped by income group
grouped_f1 = df_rural_60_mf.groupby(['World bank income group', 'Year'])['Percentage'].mean()
flat_f1 = grouped_f1.reset_index()

st.subheader("Rural Population Based on Country's Income Level")
st.line_chart(flat_f1, x = 'Year', y = 'Percentage', color = 'World bank income group',
               width = 1000, height = 600)



#grouped by WHO Region
grouped_f2 = df_rural_60_mf.groupby(['WHO region', 'Year'])['Percentage'].mean()
flat_f2 = grouped_f2.reset_index()

st.subheader("Rural Population Based on Region")
st.line_chart(flat_f2, x = 'Year', y = 'Percentage', color = 'WHO region', 
               width = 1000, height = 600)


# ------------------------------
# PART 3 : Age Groups over Time by Country (selected)
# ------------------------------

st.write(
'''
### Change in Older Populations Living in Rural Areas by Age Group
Here, you can select a country to see how their older populations living in rural areas have changed over time.  Each graph contains 5 lines, for different age groups.  
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

st.line_chart(flat_f3, x = 'Year', y = 'Percentage', color = 'Age group')


# ------------------------------
# PART 4 : Age Groups by Econ Level (Year selected)
# ------------------------------

st.write(
'''
### Age Groups living Rurally by Economic Level
How do the different age groups compare across the different World Bank income groups?  See the chart below.  Use the slider to watch how the numbers change over time. 
'''
)

#list of years to select from
year_list = rural_df.Year.unique()

#slider selection for an individual year
sel_year = st.select_slider(
       'Year', options = year_list, key = 'f4')

#temp data frame for selected year
sel_year_df = rural_df.loc[(rural_df['Age group'] != '60+') & (rural_df['Sex'] == "Both sexes") & (rural_df['Residence area'] == 'Rural') & (rural_df['Year'] == sel_year)].reset_index()

#formatting a functioning table for the graph
grouped_f4 = sel_year_df.groupby(['Age group', 'World bank income group'])['Percentage'].mean()
flat_f4 = grouped_f4.reset_index()

#creating plotly grouped bar chart
fig4 = px.histogram(
       flat_f4, x = 'World bank income group', y = 'Percentage', color = 'Age group', 
       barmode = 'group', 
       category_orders = {'World bank income group': [
              'Low income',
              'Lower middle income',
              'Upper middle income',
              'High income']}
)

#plotly chart to streamlit chart
st.plotly_chart(fig4)


# ------------------------------
# PART 5 : Highest and Lowest Percentage Each Year (Year selected)
# ------------------------------


st.write(
'''
### Which Countries had the Highest and Lowest portions of their Older Populations living Rurally?
Which countries yada yada  
'''
)

#list of years to select from
year_list5 = rural_df.Year.unique()

#dropdown selection for an individual year
sel_year5 = st.select_slider(
       'Year', options = year_list5, key = 'f5')

#temp data frame for selected year
sel_year5_df = rural_df.loc[(rural_df['Age group'] == '60+') & (rural_df['Sex'] == "Both sexes") & (rural_df['Residence area'] == 'Rural') & (rural_df['Year'] == sel_year5)].reset_index()

#-----Lowest Table

#formatting a functioning table for lowest
grouped_f5 = sel_year5_df.groupby(['Country'])['Percentage'].mean()
sorted_f5 = grouped_f5.sort_values().head(10)
flat_f5 = sorted_f5.reset_index()

#lowest table
#st.dataframe(flat_f5)

#-----Highest Table

#formatting a functioning table for highest
grouped_f5h = sel_year5_df.groupby(['Country'])['Percentage'].mean()
sorted_f5h = grouped_f5h.sort_values(ascending=False).head(10)
flat_f5h = sorted_f5h.reset_index()

#highest table
#st.dataframe(flat_f5h)

#create toggle for highest and lowest
st.button('Rural', key=f5pt2)
if st.button('Urban'):
  st.dataframe(flat_f5)
else: 
  st.dataframe(flat_f5h)





# ------------------------------
# PART 6 : Difference between Men and Women by Econ Group YOY
# ------------------------------


st.write(
'''
### How do men and women compare across different economic regions?
Which countries yada yada  
'''
)

####SELECT AGE GROUP######
#renaming age group column
f6_df = rural_df.rename(columns={"Age group" : "Age_group"})

#list of age groups to select from
age_list = f6_df.Age_group.unique()

#dropdown selection for an individual year
sel_age = st.selectbox(
       'Age_group', age_list, key = 'f6')


##########Data Frame creation for graphs#############

###HIGH INCOME - MALE###
f6_high_m = rural_df.loc[(rural_df['Age group'] == sel_age) & (rural_df['Sex'] == "Male") & (rural_df['Residence area'] == 'Rural') & (rural_df['World bank income group'] == 'High income')].reset_index()
gr_f6_high_m = f6_high_m.groupby(['Sex', 'Year'])['Percentage'].mean()
flat_f6_high_m = gr_f6_high_m.reset_index()

###HIGH INCOME - FEMALE###
f6_high_f = rural_df.loc[(rural_df['Age group'] == sel_age) & (rural_df['Sex'] == "Female") & (rural_df['Residence area'] == 'Rural') & (rural_df['World bank income group'] == 'High income')].reset_index()
gr_f6_high_f = f6_high_f.groupby(['Sex', 'Year'])['Percentage'].mean()
flat_f6_high_f = gr_f6_high_f.reset_index()

###UPPER MIDDLE INCOME - MALE###
f6_upmid_m = rural_df.loc[(rural_df['Age group'] == sel_age) & (rural_df['Sex'] == "Male") & (rural_df['Residence area'] == 'Rural') & (rural_df['World bank income group'] == 'Upper middle income')].reset_index()
gr_f6_upmid_m = f6_upmid_m.groupby(['Sex', 'Year'])['Percentage'].mean()
flat_f6_upmid_m = gr_f6_upmid_m.reset_index()

###UPPER MIDDLE - FEMALE###
f6_upmid_f = rural_df.loc[(rural_df['Age group'] == sel_age) & (rural_df['Sex'] == "Female") & (rural_df['Residence area'] == 'Rural') & (rural_df['World bank income group'] == 'Upper middle income')].reset_index()
gr_f6_upmid_f = f6_upmid_f.groupby(['Sex', 'Year'])['Percentage'].mean()
flat_f6_upmid_f = gr_f6_upmid_f.reset_index()

###LOWER MIDDLE INCOME - MALE###
f6_lowmid_m = rural_df.loc[(rural_df['Age group'] == sel_age) & (rural_df['Sex'] == "Male") & (rural_df['Residence area'] == 'Rural') & (rural_df['World bank income group'] == 'Lower middle income')].reset_index()
gr_f6_lowmid_m = f6_lowmid_m.groupby(['Sex', 'Year'])['Percentage'].mean()
flat_f6_lowmid_m = gr_f6_lowmid_m.reset_index()

###LOWER MIDDLE - FEMALE###
f6_lowmid_f = rural_df.loc[(rural_df['Age group'] == sel_age) & (rural_df['Sex'] == "Female") & (rural_df['Residence area'] == 'Rural') & (rural_df['World bank income group'] == 'Lower middle income')].reset_index()
gr_f6_lowmid_f = f6_lowmid_f.groupby(['Sex', 'Year'])['Percentage'].mean()
flat_f6_lowmid_f = gr_f6_lowmid_f.reset_index()

###LOWER MIDDLE INCOME - MALE###
f6_low_m = rural_df.loc[(rural_df['Age group'] == sel_age) & (rural_df['Sex'] == "Male") & (rural_df['Residence area'] == 'Rural') & (rural_df['World bank income group'] == 'Low income')].reset_index()
gr_f6_low_m = f6_low_m.groupby(['Sex', 'Year'])['Percentage'].mean()
flat_f6_low_m = gr_f6_low_m.reset_index()

###LOWER MIDDLE - FEMALE###
f6_low_f = rural_df.loc[(rural_df['Age group'] == sel_age) & (rural_df['Sex'] == "Female") & (rural_df['Residence area'] == 'Rural') & (rural_df['World bank income group'] == 'Low income')].reset_index()
gr_f6_low_f = f6_low_f.groupby(['Sex', 'Year'])['Percentage'].mean()
flat_f6_low_f = gr_f6_low_f.reset_index()


###GRAPH CREATION###

fig_f6, axs = plt.subplots(2, 2)
axs[0, 0].plot(flat_f6_low_m['Year'], flat_f6_low_m['Percentage'], 'tab:blue', label="Male")
axs[0, 0].plot(flat_f6_low_f['Year'], flat_f6_low_f['Percentage'], 'tab:red', label="Female")
axs[0, 0].set_title('Low Income')
axs[0, 0].set_xlim(left=1980, right=2015)
axs[0, 0].set_ylim(bottom=0, top=100)
axs[0, 0].legend(loc="lower right")
axs[0, 1].plot(flat_f6_lowmid_m['Year'], flat_f6_lowmid_m['Percentage'], 'tab:blue', label="Male")
axs[0, 1].plot(flat_f6_lowmid_f['Year'], flat_f6_lowmid_f['Percentage'], 'tab:red', label="Female")
axs[0, 1].set_title('Lower Middle Income')
axs[0, 1].set_xlim(left=1980, right=2015)
axs[0, 1].set_ylim(bottom=0, top=100)
axs[0, 1].legend(loc="lower right")
axs[1, 0].plot(flat_f6_upmid_m['Year'], flat_f6_upmid_m['Percentage'], 'tab:blue', label="Male")
axs[1, 0].plot(flat_f6_upmid_f['Year'], flat_f6_upmid_f['Percentage'], 'tab:red', label="Female")
axs[1, 0].set_title('Upper Middle Income')
axs[1, 0].set_xlim(left=1980, right=2015)
axs[1, 0].set_ylim(bottom=0, top=100)
axs[1, 0].legend(loc="upper right")
axs[1, 1].plot(flat_f6_high_m['Year'], flat_f6_high_m['Percentage'], 'tab:blue', label="Male")
axs[1, 1].plot(flat_f6_high_f['Year'], flat_f6_high_f['Percentage'], 'tab:red', label="Female")
axs[1, 1].set_title('High Income')
axs[1, 1].set_xlim(left=1980, right=2015)
axs[1, 1].set_ylim(bottom=0, top=100)
axs[1, 1].legend(loc="upper right")


for ax in axs.flat:
   ax.set(xlabel='Year', ylabel='Percentage')


plt.suptitle('Percentage of Older Males vs Older Females Living Rurally')
plt.tight_layout(pad=1.08, h_pad=None, w_pad=None)

st.pyplot(fig=fig_f6)

st.dataframe(flat_f6_high_m)





