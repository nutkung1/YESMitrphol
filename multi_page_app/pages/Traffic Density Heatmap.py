import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import leafmap.foliumap as leafmap
import leafmap as lm

st.title("Heat Map")
reply_container = st.container()
container = st.container()

with st.form(key='my_form', clear_on_submit=False):
    lat = st.number_input("ละติจูด",key='input')
    lon = st.number_input("ลองจิจูด")
    submit_button = st.form_submit_button(label='Send')

    if submit_button and lat and lon:
        new_title = '<p style="font-family:sans-serif; color:Black; font-size: 20px;">Traffic density heat map</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        filepath = "/Users/suchanatratanarueangrong/Mitrphol/streamlit/Mitrphol_heatmap.csv"
        m = leafmap.Map(tiles='stamentoner')
        m.set_center(lat=lat, lon=lon, zoom=10)
        m.add_heatmap(filepath, latitude="latitude", longitude='longitude', value="pop_max", name="Heat map", radius=20)
        m.to_streamlit(width=700, height=500, add_layer_control=True)
        # new_title = '<p style="font-family:sans-serif; color:Black; font-size: 20px;">CO2 Emission rate</p>'
        # st.markdown(new_title, unsafe_allow_html=True)
        # chart_data = pd.DataFrame(np.random.randn(100, 2) / [97, 97] + [lat, lon],columns=['lat', 'lon'])
        # st.pydeck_chart(pdk.Deck(
        #     map_style=None,
        #     initial_view_state=pdk.ViewState(
        #     latitude=lat,
        #     longitude=lon,
        #     zoom=12,
        #     pitch=50,
        # ),
        # layers=[
        #     pdk.Layer(
        #         'HexagonLayer',
        #         data=chart_data,
        #         get_position='[lon, lat]',
        #         radius=200,
        #         elevation_scale=10,
        #         elevation_range=[0, 400],
        #         pickable=True,
        #         extruded=True,
        #     ),
        #     pdk.Layer(
        #         'ScatterplotLayer',
        #         data=chart_data,
        #         get_position='[lon, lat]',
        #         get_color='[200, 30, 0, 160]',
        #         get_radius=200,
        #     ),
        #     ],
        # ))
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