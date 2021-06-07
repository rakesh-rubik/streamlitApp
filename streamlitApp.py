import pandas as pd
import numpy as np

import streamlit as st

st.title('The Modern Data Company')

st.write("A small app!!")

consumers = pd.read_csv('SampleData/consumers.csv')
timeseries = pd.read_csv('SampleData/sampleTimeSeries.csv')

#order_data = pd.read_csv('SampleData/inlineItems.csv')
type_of_consumer = consumers.groupby('type')['id'].size()


option = st.sidebar.selectbox(
    'Select State',
     ['All']+list(consumers.state.unique()))

st.write('consumers by type')

if option == 'All':
	st.bar_chart(type_of_consumer)
else:
	st.bar_chart(consumers[consumers.state == option].groupby('type')['id'].size())


# Consumers Map Plot
st.write("ConsumerMapPlot")
if option == 'All':
	st.map(consumers[['lon', 'lat']])

else:
	st.map(consumers[consumers.state == option][['lon', 'lat']])



## line plot
st.write('sampleTimeSeries')
st.line_chart(timeseries)