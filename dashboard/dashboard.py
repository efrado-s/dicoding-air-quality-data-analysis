import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.header("Dicoding Air Quality Analysis Dashboard")
st.markdown(
    """
    > Created by Efrado Suryadi
    """
)

# Prepare the data
st.markdown(
    """
    ## Data information
    """
)

# Read csv
file_name = "main_data.csv"
main_df = pd.read_csv(os.path.join(os.getcwd(), file_name))

st.dataframe(data=main_df)

st.markdown(
    """
    The data above is a processed data that is originally taken from this Github [source](https://github.com/marceloreis/HTI/tree/master). 
    I have done the cleaning session and now it is shown as above. 

    #### Seeing data according to its station
    To see data according to its station, use the following table:
    """
)

# Set interactive filter
station_filter = st.multiselect(
    "Select Station",
    options=main_df['station'].unique(),
    default=main_df['station'].unique()
)

filtered_df = main_df[(main_df['station'].isin(station_filter))]

st.write(filtered_df)

# Question 1
st.write(
    """
    ----
    ## Questions
    ### Question 1: What is the most frequent wind direction in Beijing?

    To answer the question above, I decide to make 
    a plot on the number of appearance of each wind direction 
    value in the `wd` column.

    >  Keep in mind that the `wd` value consists of null, 
    > but since it is only a small percent of it, 
    > I decided to not handle it and treat it only as "Not specified"
    """
)

# Create a horizontal bar plot 
# to show the most frequent wind direction in Beijing

wd_count = main_df['wd'].value_counts().sort_values(ascending=True)

# Create a horizontal bar plot
fig, ax = plt.subplots(figsize=(8, 6)) 
wd_count.plot(kind='barh', color='skyblue', ax=ax)

# Add labels and title
ax.set_xlabel('Number of Appearances')
ax.set_ylabel('Wind Direction')
ax.set_title('Frequency of Wind Directions')

# Add gridlines
ax.grid(axis='x', linestyle='--', alpha=0.7)

# Display the plot in Streamlit
st.pyplot(fig)

st.write(
    """
    **Answer:** 
    From the plot above we can see that the 
    answer of question 1 is NE, which is the north east wind.
    """
)

# Question 2
st.write(
    """
    ### Question 2: What kind of temperature changes pattern exist in Beijing stations?
    To answer this question, I decided to use only one station, which is `Aotizhongxin`, 
    since all of the stations are in Beijing, the temperature difference wouldn't be that great.
    """
)

# Change `date_time` data type into datetime
main_df['date_time'] = pd.to_datetime(main_df['date_time'])

# Filter the data for station 'Aotizhongxin'
temp_df = main_df[main_df['station'] == 'Aotizhongxin']

# Add Streamlit slider for selecting the year range
year_range = st.slider('Select Year Range', 2013, 2017, (2013, 2017))

# Filter the dataframe based on the selected year range
filtered_df = temp_df[(temp_df['date_time'].dt.year >= year_range[0]) & (temp_df['date_time'].dt.year <= year_range[1])]

# Create the plot
fig, ax = plt.subplots(figsize=(20, 6))
ax.plot(filtered_df['date_time'], filtered_df['TEMP'], alpha=0.8)

# Add labels, title, and grid
ax.set_title(f'Trend of temperature changes from {year_range[0]} to {year_range[1]} in Aotizhongxin')
ax.set_xlabel('Date Time')
ax.set_ylabel('Temperature')
ax.grid(True)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout to prevent clipping of labels

# Display the plot in Streamlit
st.pyplot(fig)

st.write(
    """
    **Answer:** From the charts above, we can see that pattern do exist in temperature changes in Beijing. 
    To be more specific, the pattern usually starts low first in the first three months(which can be seen as a season), 
    with their lowest temperature point below zero celcius. When April is reach, the temperature starting to rise, 
    with its lowest temperature point not even below zero celcius now (this also marks a change of season). 
    In the middle of the year, usually on July, the average temperature in that month would be higher than other months. 
    And then, the temperature would start going down again in September until November, where its lowest temperature now reach zero celcius. 
    After November, which means it is now December, the temperature would start going below zero celcius again, which marks the start of winter.
    """
)

st.caption(
    "Owned by Efrado Suryadi"
)