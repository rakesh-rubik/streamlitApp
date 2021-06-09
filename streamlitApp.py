import pandas as pd
import numpy as np
import datetime as dt
from datetime import date 
import matplotlib.pyplot as plt

import streamlit as st

st.title('The Modern Data Company')

st.write("A small app!!")



# Reading datasets

from streamlit import caching

clear_cache = st.button('Clear Cache')
if clear_cache:
	caching.clear_cache()



consumers = pd.read_csv('SampleData/consumers.csv')

@st.cache(allow_output_mutation=True)
def read_order_data():
	d = pd.read_csv('SampleData/OrderData.csv')
	return d

order_data = read_order_data()

order_data.rename(columns = {'Consumer_ID':'id'}, inplace = True)

order_data.Order_DateTime = pd.to_datetime(order_data.Order_DateTime)

order_data['date'] = order_data.Order_DateTime.dt.date


order_data = order_data.merge(consumers[['id','type', 'state']], on = 'id', how = 'left')




#order_data = pd.read_csv('SampleData/inlineItems.csv')
type_of_consumer = consumers.groupby('type')['id'].size()

left_column, right_column = st.beta_columns(2)



option_state = st.sidebar.selectbox(
    'Select State',
     ['All']+list(consumers.state.unique()))

# Option 2
option_type = st.sidebar.selectbox(
    'Select type',
     ['All']+list(consumers.type.unique()), )
############## Bar
left_column.write('retailers by type')

if option_state == 'All':
	left_column.bar_chart(type_of_consumer, width=200, height=500)
else:
	left_column.bar_chart(consumers[consumers.state == option_state].groupby('type')['id'].size(), width=200, height=500)


##############Map
# Consumers Map Plot
right_column.write("retailers distribution across state/country based on type")
if option_state == 'All' and option_type == 'All':
	right_column.map(consumers[['lon', 'lat']], use_container_width=False)

elif option_state == 'All' and option_type != 'All':
	right_column.map(consumers[consumers.type == option_type][['lon', 'lat']], use_container_width=False)

elif option_state != 'All' and option_type == 'All':
	right_column.map(consumers[consumers.state == option_state][['lon', 'lat']], use_container_width=False)

else:
	right_column.map(consumers[(consumers.state == option_state) & (consumers.type == option_type)][['lon', 'lat']], use_container_width=False)


#############Sales 
st.write(option_state+" "+option_type+' Sales')

if option_state == 'All' and option_type == 'All':
	st.line_chart(order_data.groupby('date')['Quantities'].sum())

elif option_state == 'All' and option_type != 'All':
	st.line_chart(order_data[order_data.type == option_type].groupby('date')['Quantities'].sum())
	

elif option_state != 'All' and option_type == 'All':
	st.line_chart(order_data[order_data.state == option_state].groupby('date')['Quantities'].sum())

else:
	st.line_chart(order_data[(order_data.state == option_state) & (order_data.type == option_type)].groupby('date')['Quantities'].sum())


#fig, ax = plt.subplots()
#st.write(option_state+' Sales')
#if option_state == 'All':
#	ax.plot(order_data[order_data.type == 'Hospital'].groupby('date')['Quantities'].sum())
#	ax.plot(order_data[order_data.type == 'Pharmacy'].groupby('date')['Quantities'].sum())
#if option_state != 'All':
#	ax.plot(order_data[(order_data.type == 'Hospital') & (order_data.state == option_state)].groupby('date')['Quantities'].sum())
#	ax.plot(order_data[(order_data.type == 'Pharmacy') & (order_data.state == option_state)].groupby('date')['Quantities'].sum())

#st.pyplot(fig)

#st.json({'foo':'bar','fu':'ba'})



st.write('It was fun!!')

st.write("Contact US")


details = {'question':[], 'email':[]}
with st.form("Details"):


	st.write("Please fill details below")
	ques = st.text_area('Enter your question - ')
	email = st.text_input('Enter your email - ')
	submitted = st.form_submit_button("Submit")

	if submitted:
		details['question'].append(ques)
		details['email'].append(email)
		ques = st.empty()
		email = st.empty()
st.write(details)