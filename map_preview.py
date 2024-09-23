import streamlit as st
import leafmap.foliumap as leafmap

st.sidebar.info(
    """
    - Web App URL: <https://streamlit.geemap.org>
    - GitHub repository: <https://github.com/giswqs/streamlit-geospatial>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Qiusheng Wu: <https://wetlands.io>
    [GitHub](https://github.com/giswqs) | [Twitter](https://twitter.com/giswqs) | [YouTube](https://www.youtube.com/c/QiushengWu) | [LinkedIn](https://www.linkedin.com/in/qiushengwu)
    """
)

# Customize page title
st.title("บริษัท น้ำตาลมิตรผล จำกัด")

st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/giswqs/streamlit-multipage-template).
    """
)

st.header("สาระสำคัญ")

markdown = """
1. platform นี้จะประกอบไปด้วยการกรอก carbon credit เพื่อลดแรงการโกงของชาวไร่ บลาๆ.
2. สามารถดูแล้วเข้าใจง่าย ชัดเจนว่าปัจจุบัน carbon credit เป็นเท่าไหร่แล้ว.
3. สามารถเชื่อมต่อกับ plantform เช่น OneAgri Smart GIS etc. ของมิตรผลเพื่อเพิ่ม ฟีเจอร์ อื่นได้.
4. มีภาพถ่ายดาวเทียมเพื่อเพิ่มประสิทธิถาพในการทำงานมากขึ้น.

"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True, center=(16.465548, 102.126841), zoom=10)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
