import streamlit as st
import leafmap.foliumap as leafmap


"# Mitr Phol Dan Chang Polygon 🗺️"

# st.title("Customizing Leafmap Center in Streamlit")

# Create a Leafmap map with a default center (e.g., [0, 0])
m = leafmap.Map(center=[0, 0], zoom=2)

# Add a GeoJSON layer to the map
in_geojson = '/Users/suchanatratanarueangrong/Mitrphol/streamlit/yes_camp.geojson'
m.add_geojson(in_geojson, layer_name="Cable lines")

# Set a new center point and zoom level
m.set_center(99.80, 14.85, 9.1)

# Display the map in Streamlit
m.to_streamlit()



# "## Add a colorbar"
# with st.echo():

#     m = leafmap.Map()
#     m.add_basemap('USGS 3DEP Elevation')
#     colors = ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
#     vmin = 0
#     vmax = 4000
#     m.add_colorbar(colors=colors, vmin=vmin, vmax=vmax)
#     m.to_streamlit()


# "## Change basemaps"
# with st.echo():
#     m = leafmap.Map()
#     m.add_basemap("Esri.NatGeoWorldMap")
#     m.to_streamlit()


# import ee
# ee.Authenticate()
# ee.Initialize()
# print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())

# ---------------------------------------------------------------------------------

# Data Source: https://public.tableau.com/app/profile/federal.trade.commission/viz/FraudandIDTheftMaps/AllReportsbyState
# US State Boundaries: https://public.opendatasoft.com/explore/dataset/us-state-boundaries/export/

# import streamlit as st
# import pandas as pd
# import folium
# from streamlit_folium import st_folium

# APP_TITLE = 'Fraud and Identity Theft Report'
# APP_SUB_TITLE = 'Source: Federal Trade Commission'

# def display_time_filters(df):
#     year_list = list(df['Year'].unique())
#     year_list.sort()
#     year = st.sidebar.selectbox('Year', year_list, len(year_list)-1)
#     quarter = st.sidebar.radio('Quarter', [1, 2, 3, 4])
#     st.header(f'{year} Q{quarter}')
#     return year, quarter

# def display_state_filter(df, state_name):
#     state_list = [''] + list(df['State Name'].unique())
#     state_list.sort()
#     state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
#     return st.sidebar.selectbox('State', state_list, state_index)

# def display_report_type_filter():
#     return st.sidebar.radio('Report Type', ['Fraud', 'Other'])

# def display_map(df, year, quarter):
#     df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]

#     map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')

#     choropleth = folium.Choropleth(
#         geo_data='data/us-state-boundaries.geojson',
#         data=df,
#         columns=('State Name', 'State Total Reports Quarter'),
#         key_on='feature.properties.name',
#         line_opacity=0.8,
#         highlight=True
#     )
#     choropleth.geojson.add_to(map)

#     df_indexed = df.set_index('State Name')
#     for feature in choropleth.geojson.data['features']:
#         state_name = feature['properties']['name']
#         feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'State Pop'][0]) if state_name in list(df_indexed.index) else ''
#         feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

#     choropleth.geojson.add_child(
#         folium.features.GeoJsonTooltip(['name', 'population', 'per_100k'], labels=False)
#     )

#     st_map = st_folium(map, width=700, height=450)

#     state_name = ''
#     if st_map['last_active_drawing']:
#         state_name = st_map['last_active_drawing']['properties']['name']
#     return state_name

# def display_fraud_facts(df, year, quarter, report_type, state_name, field, title, string_format='${:,}', is_median=False):
#     df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
#     df = df[df['Report Type'] == report_type]
#     if state_name:
#         df = df[df['State Name'] == state_name]
#     df.drop_duplicates(inplace=True)
#     if is_median:
#         total = df[field].sum() / len(df[field]) if len(df) else 0
#     else:
#         total = df[field].sum()
#     st.metric(title, string_format.format(round(total)))

# def main():
#     st.set_page_config(APP_TITLE)
#     st.title(APP_TITLE)
#     st.caption(APP_SUB_TITLE)

#     #Load Data
#     df_continental = pd.read_csv('data/AxS-Continental_Full Data_data.csv')
#     df_fraud = pd.read_csv('data/AxS-Fraud Box_Full Data_data.csv')
#     df_median = pd.read_csv('data/AxS-Median Box_Full Data_data.csv')
#     df_loss = pd.read_csv('data/AxS-Losses Box_Full Data_data.csv')

#     #Display Filters and Map
#     year, quarter = display_time_filters(df_continental)
#     state_name = display_map(df_continental, year, quarter)
#     state_name = display_state_filter(df_continental, state_name)
#     report_type = display_report_type_filter()

#     #Display Metrics
#     st.subheader(f'{state_name} {report_type} Facts')

#     col1, col2, col3 = st.columns(3)
#     with col1:
#         display_fraud_facts(df_fraud, year, quarter, report_type, state_name, 'State Fraud/Other Count', f'# of {report_type} Reports', string_format='{:,}')
#     with col2:
#         display_fraud_facts(df_median, year, quarter, report_type, state_name, 'Overall Median Losses Qtr', 'Median $ Loss', is_median=True)
#     with col3:
#         display_fraud_facts(df_loss, year, quarter, report_type, state_name, 'Total Losses', 'Total $ Loss')


# if __name__ == "__main__":
#     main()
