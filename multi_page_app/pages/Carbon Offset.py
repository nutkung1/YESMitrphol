import streamlit as st
import pandas as pd

# Update the file paths to the correct locations
file_path2 = '/Users/suchanatratanarueangrong/Mitrphol/streamlit/Offset.csv'

st.title("Carbon Offset 👨🏻‍💻")

reply_container = st.container()
container = st.container()

with container:
        with st.form(key='my_form', clear_on_submit=False):
            name1 = st.text_input("ชื่อ", placeholder="โปรดใส่ชื่อของคุณ", key='input')
            age1 = st.number_input("อายุ", placeholder="Please fill your age")
            date1 = st.date_input("วันที่ลง")
            # fertilizer = st.text_input("ชนิดปุ๋ยที่ใช้", placeholder="โปรดใส่ชนิดปุ๋ยคุณ")
            fertilizer_kilo1 = st.number_input("จำนวนปุ๋ยละลายช้าที่ใช้ (กิโลกรัม)", placeholder="โปรดใส่จำนวนปุ๋ยของคุณ")
            # fuel = st.number_input("จำนวนน้ำมันที่ใช้ (ลิตร/ไร่)", placeholder="โปรดใส่จำนวนการใช้น้ำมันของคุณ")
            electric1 = st.number_input("จำนวนพลังงานสะอาดที่ใช้ (วัตต์)", placeholder="โปรดใส่จำนวนการใช้ไฟฟ้าของคุณ")
            submit_button = st.form_submit_button(label='Send')

            if submit_button and name1 and age1 and date1 and fertilizer_kilo1 and electric1:
                df = pd.read_csv(file_path2, encoding='utf-8')
                new_row_dict = {'Name': name1, 'Age': age1, 'Date': date1,
                                'Kilo': fertilizer_kilo1, 'Electric': electric1}
                df = df.append(new_row_dict, ignore_index=True)
                df.to_csv(file_path2, index=False, encoding='utf-8')
                st.session_state['language'] = 'gc'
