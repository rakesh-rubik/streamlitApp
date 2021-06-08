import pandas as pd
import numpy as np
import datetime as dt
from datetime import date 

import streamlit as st

st.title('The Modern Data Company')

st.write("A small app!!")



# Reading datasets

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
type_of_consumer = consumers.groupby('type')['id'].size().T

left_column, right_column = st.beta_columns(2)



option1 = st.sidebar.selectbox(
    'Select State',
     ['All']+list(consumers.state.unique()))

left_column.write('retailers by type')

if option1 == 'All':
	left_column.bar_chart(type_of_consumer, width=200, height=300)
else:
	left_column.bar_chart(consumers[consumers.state == option1].groupby('type')['id'].size(), width=200, height=300)


# Consumers Map Plot
right_column.write("retailers distribution across state/country")
if option1 == 'All':
	right_column.map(consumers[['lon', 'lat']], use_container_width=False)

else:
	right_column.map(consumers[consumers.state == option1][['lon', 'lat']], use_container_width=False)


# Option 2
option2 = st.sidebar.selectbox(
    'Select type',
     ['All']+list(consumers.type.unique()))



st.write(option1+" "+option2+' Sales')

if option1 == 'All' and option2 == 'All':
	st.line_chart(order_data.groupby('date')['Quantities'].sum())

elif option1 == 'All' and option2 != 'All':
	st.line_chart(order_data[order_data.type == option2].groupby('date')['Quantities'].sum())	

elif option1 != 'All' and option2 == 'All':
	st.line_chart(order_data[order_data.state == option1].groupby('date')['Quantities'].sum())

else:
	st.line_chart(order_data[(order_data.state == option1) & (order_data.type == option2)].groupby('date')['Quantities'].sum())