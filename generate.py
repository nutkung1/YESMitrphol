import pandas as pd
import numpy as np

lat = 99.873886664899999
lon = 15.1531762388

# Generate random data
df = pd.DataFrame(np.random.randn(100, 2) / [97, 97] + [lat, lon], columns=['lat', 'lon'])

# Specify the file path where you want to save the CSV file
file_path = "/Users/suchanatratanarueangrong/Mitrphol/streamlit/pydeck.csv"

# Save the DataFrame to a CSV file
df.to_csv(file_path, index=False)

print(f"Data saved to {file_path}")
