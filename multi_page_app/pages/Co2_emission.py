import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title("Check CO2 Emission")

# Initialize the chart data to None
chart_data = None

if 'chart_data' not in st.session_state:
    st.session_state['chart_data'] = None  # Initialize as None

# Create a Streamlit form for input
with st.form(key='my_form', clear_on_submit=False):
    name = st.text_input("ชื่อ-สกุล", placeholder="โปรดใส่ชื่อ-สกุล", key='input')
    lat = st.number_input("ละติจูด")
    lon = st.number_input("ลองจิจูด")

    submit_button = st.form_submit_button(label='ส่ง')

# Create a Streamlit sidebar for the map rotation angle
with st.sidebar:
    bearing = st.slider("Map Bearing (0-360 degrees)", 0, 360, 0)

if lat and lon:
    new_title = '<p style="font-family:sans-serif; color:Black; font-size: 20px;">CO2 Emission rate</p>'
    st.markdown(new_title, unsafe_allow_html=True)

    # Generate the random data only when it is not available (when the DataFrame is None)
    if st.session_state['chart_data'] is None:
        chart_data = pd.DataFrame(np.random.randn(100, 2) / [97, 97] + [lat, lon], columns=['lat', 'lon'])
        st.session_state['chart_data'] = chart_data
    else:
        chart_data = st.session_state['chart_data']

    # Use the bearing value from the slider to set the initial bearing of the map
    deck = pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=12,
            pitch=50,
            bearing=bearing,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=chart_data,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=10,
                elevation_range=[0, 400],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=chart_data,
                get_position='[lon, lat]',
                get_color='[0, 255, 0, 255]',
                get_radius=200,
            ),
        ],
    )

    st.pydeck_chart(deck)




        # new_title = '<p style="font-family:sans-serif; color:Black; font-size: 20px;">Traffic density heat map</p>'
        # st.markdown(new_title, unsafe_allow_html=True)
        # filepath = "/Users/suchanatratanarueangrong/Mitrphol/streamlit/Mitrphol_heatmap.csv"
        # m = leafmap.Map(tiles='stamentoner')
        # m.set_center(lat=lat, lon=lon, zoom=10)
        # m.add_heatmap(filepath, latitude="latitude", longitude='longitude', value="pop_max", name="Heat map", radius=20)
        # m.to_streamlit(width=700, height=500, add_layer_control=True)
    # with st.container():
        # filepath = "/Users/suchanatratanarueangrong/Mitrphol/streamlit/Mitrphol_heatmap.csv"
        # m = leafmap.Map(tiles='stamentoner')
        # m.add_heatmap(filepath, latitude="latitude", longitude='longitude', value="pop_max", name="Heat map", radius=20)
        # m.to_streamlit(width=700, height=500, add_layer_control=True)