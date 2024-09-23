import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Custom function to set a nice color palette for the pie chart
def set_color_palette():
    return ['#ff9999', '#66b3ff']

st.title("Carbon DashBoard Hub")
df = pd.read_csv('/Users/suchanatratanarueangrong/Mitrphol/streamlit/example.csv')
df1 = pd.read_csv('/Users/suchanatratanarueangrong/Mitrphol/streamlit/Offset.csv')
labels = ['Carbon Used', 'Carbon Offset']
carbon_credit = sum(df['Kilo'] + (sum(df['Rai']) * sum(df['Fuel'] + 7))) + sum(df['Electric'])
carbon_offset = sum(df1['Kilo']) + sum(df1['Electric'])
divider = sum(df['Kilo'] + (sum(df['Rai']) * sum(df['Fuel'] + 7))) + sum(df['Electric']) + sum(df1['Kilo']) + sum(df1['Electric'])
percent_carbon_credit = carbon_credit / divider * 100
percent_carbon_offset = carbon_offset / divider * 100
sizes = [percent_carbon_credit, percent_carbon_offset]
explode = (0.1, 0)

# Set a nice color palette for the pie chart
colors = set_color_palette()

# Create the pie chart with improved styling
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax1.axis('equal')

# Use st.columns to split the layout
col1, col2 = st.columns([3, 1])

# Style the pie chart title and data descriptions
col1.subheader("Carbon Distribution")
col1.pyplot(fig1)
col1.write("Carbon Used: {:.2f}%".format(percent_carbon_credit))
col1.write("Carbon Offset: {:.2f}%".format(percent_carbon_offset))

# Place additional information or data in the second column
col2.subheader("Additional Information")
col2.write("Total Carbon Used: {:.2f}".format(carbon_credit))
col2.write("Total Carbon Offset: {:.2f}".format(carbon_offset))

# Read the CSV file

# Read the CSV file
new_title = '<p style="font-family:sans-serif; color:Black; font-size: 26px;">กราฟแสดงผลราคาของการขาย Carbon Credit ต่อ จำนวน Carbon</p>'
st.markdown(new_title, unsafe_allow_html=True)
# Read the CSV file
gdp = pd.read_csv("/Users/suchanatratanarueangrong/Mitrphol/streamlit/CO2:price.csv")

# Convert the 'date' column to datetime
gdp['date'] = pd.to_datetime(gdp['date'])

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 5))
ax2 = ax.twinx()

# Set the plot title and labels
ax.set_title('The amount of Carbon Offset as compared to Carbon Footprint', fontsize=16)
ax.set_xlabel('Year', fontsize=12)

# Plot the data with improved aesthetics
ax.plot(gdp['date'], gdp['price/tCO2'], color='green', marker='o', linestyle='-', label='Price/tCO2', linewidth=2)
ax2.plot(gdp['date'], gdp['amount/tCO2'], color='red', marker='o', linestyle='-', label='Amount/tCO2', linewidth=2)

# Fill area under the line plot
ax.fill_between(gdp['date'], gdp['price/tCO2'], color='lightgreen', alpha=0.2)

# Set y-axis labels
ax.set_ylabel('Price/tCO2', color='green', fontsize=12)
ax2.set_ylabel('Amount/tCO2', color='red', fontsize=12)

# Set legends
ax.legend(loc='upper left', fontsize=12)
ax2.legend(loc='upper right', fontsize=12)

# Set x-axis ticks
ax.set_xticks(gdp['date'])
ax.set_xticklabels(gdp['date'].dt.year, rotation=45, fontsize=10)

# Add grid lines to the y-axis
ax.yaxis.grid(color='lightgray', linestyle='dashed')

# Customize the tick labels
ax.tick_params(axis='y', labelcolor='green')
ax2.tick_params(axis='y', labelcolor='red')

# Add a background grid
ax.grid(axis='both', linestyle='--', alpha=0.5)

# Add a legend
plt.legend(loc='upper right')

# Customize the background color
fig.patch.set_facecolor('white')

# Display the plot using Streamlit
st.pyplot(fig)


