import numpy as np
import pandas as pd
import streamlit as st

st.title('Pickups in Bengaluru')

@st.cache_data
def generate_random_data(num_rows=10):
    """Generates a DataFrame with random data."""
    data = {
        'pickup_location': np.random.choice(['Location A', 'Location B', 'Location C'], num_rows),
        'dropoff_location': np.random.choice(['Location D', 'Location E', 'Location F'], num_rows),
        'pickup_time': pd.date_range(start='2023-01-01', periods=num_rows, freq='H'),
        'passenger_count': np.random.randint(1, 5, num_rows),
        'lat': np.random.uniform(-90, 90, num_rows),
        'lon': np.random.uniform(-180, 180, num_rows)
    }
    return pd.DataFrame(data)

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = generate_random_data(100)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done with cache!')

st.subheader('Raw data')
st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data['pickup_time'].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)


st.subheader('Map of all pickups')
st.map(data)
