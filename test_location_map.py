import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

st.sidebar.info(
    """
    - Web App URL: <https://streamlit.geemap.org>
    - GitHub repository: <https://github.com/giswqs/streamlit-geospatial>
    """
)

st.sidebar.title("Contact")
# st.sidebar.info(
#     """
#     Qiusheng Wu: <https://wetlands.io>
#     [GitHub](https://github.com/giswqs) | [Twitter](https://twitter.com/giswqs) | [YouTube](https://www.youtube.com/c/QiushengWu) | [LinkedIn](https://www.linkedin.com/in/qiushengwu)
#     """
# )

st.title("โรงงานมิตรผลทั้งหมด")

# with st.expander("See source code"):
#     with st.echo():

m = leafmap.Map(center=[40, -100], zoom=4)
cities = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv'
regions = 'thailand-with-regions_1526.geojson'

m.add_geojson(regions, layer_name='ASIA Regions')
m.add_points_from_xy(
    cities,
    x="longitude",
    y="latitude",
    color_column='region',
    icon_names=['gear', 'map', 'leaf', 'globe'],
    spin=True,
    add_legend=True,
)

m.to_streamlit(height=700)


# ---------------------------------------------------------------------------------
# import streamlit as st
# from streamlit_chat import message
# from langchain.chains import ConversationalRetrievalChain
# from langchain.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.llms import CTransformers
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import FAISS, Chroma
# from langchain.memory import ConversationBufferMemory

# #load the pdf files from the path
# loader = DirectoryLoader('data1/',glob="*.txt")
# documents = loader.load()

# #split text into chunks
# text_splitter  = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
# text_chunks = text_splitter.split_documents(documents)

# #create embeddings
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
#                                    model_kwargs={'device':"cpu"})

# #vectorstore
# vector_store = Chroma.from_documents(text_chunks,embeddings)

# #create llm
# llm = CTransformers(model="llama-2-7b-chat.ggmlv3.q6_K.bin",model_type="llama",
#                     config={'max_new_tokens':256,'temperature':0.01})

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# chain = ConversationalRetrievalChain.from_llm(llm=llm,chain_type='stuff',
#                                               retriever=vector_store.as_retriever(search_kwargs={"k":2}),
#                                               memory=memory)

# st.title("🧑‍🌾 Mitr Phol Bot 👩‍🌾")
# def conversation_chat(query):
#     result = chain({"question": query, "chat_history": st.session_state['history']})
#     st.session_state['history'].append((query, result["answer"]))
#     return result["answer"]

# def initialize_session_state():
#     if 'history' not in st.session_state:
#         st.session_state['history'] = []

#     if 'generated' not in st.session_state:
#         st.session_state['generated'] = ["Hello! Ask me anything about 🤗"]

#     if 'past' not in st.session_state:
#         st.session_state['past'] = ["Hey! 👋"]

# def display_chat_history():
#     reply_container = st.container()
#     container = st.container()

#     with container:
#         with st.form(key='my_form', clear_on_submit=True):
#             user_input = st.text_input("Question:", placeholder="Ask about your problem", key='input')
#             submit_button = st.form_submit_button(label='Send')

#         if submit_button and user_input:
#             output = conversation_chat(user_input)

#             st.session_state['past'].append(user_input)
#             st.session_state['generated'].append(output)

#     if st.session_state['generated']:
#         with reply_container:
#             for i in range(len(st.session_state['generated'])):
#                 message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
#                 message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

# # Initialize session state
# initialize_session_state()
# # Display chat history
# display_chat_history()

# ------------------------------------------------------------------------------------------------------
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
