import streamlit as st
import pandas as pd
import numpy as np


#The first step is to create a new Python script. Let's call it uber_pickups.py.
st.title('Uber pickups in NYC')

#Let's start by writing a function to load the data.
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Now let's test the function and review the output.
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")
#look at the raw data you're working with before you start working with it
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
#add a subheader just below the raw data section
st.subheader('Number of pickups by hour')
#Use NumPy to generate a histogram that breaks down pickup times binned by hour
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
#Draw this histogram
st.bar_chart(hist_values)
#Add a subheader for the section
st.subheader('Map of all pickups')
#Use the st.map() function to plot the data
st.map(data)
# redraw the map to Filter results with a slider
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)



