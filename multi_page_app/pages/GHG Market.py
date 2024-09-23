import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Set a custom title with HTML styling
new_title = '<p style="font-family:sans-serif; color:Black; font-size: 26px;">กราฟแสดงผลราคาการขาย Carbon Credit ผ่านโครงการ T-Ver และ T-VerPremium</p>'
st.markdown(new_title, unsafe_allow_html=True)

# Read the data
df = pd.read_csv("/Users/suchanatratanarueangrong/Mitrphol/streamlit/GHG_price_not-Tver.csv")
df['date'] = pd.to_datetime(df['date'])

# Create a figure and axis with higher DPI for better quality
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

# Plot the data with improved aesthetics
ax.plot(df['date'], df['Baht_high'], label="T-Ver Premium", color='green', linestyle='-.', linewidth=2)
ax.plot(df['date'], df['Baht_low'], label="T-ver", color='blue', linestyle=':', linewidth=2)

# Set labels and title
ax.set_ylabel("Baht/tCO2", fontsize=12)
ax.set_xlabel("Year", fontsize=12)
# ax.set_title("กราฟแสดงผลราคาของการขาย Carbon Credit ต่อ จำนวน Carbon", fontsize=16)

# Customize legend
ax.legend(fontsize=12, loc='lower right')

# Customize the grid
ax.grid(True, linestyle='--', alpha=0.6)

# Customize the tick labels
ax.tick_params(axis='both', which='major', labelsize=10)

# Display the plot in Streamlit
st.pyplot(fig)
