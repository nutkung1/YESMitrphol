import streamlit as st
import pandas as pd

# Update the file paths to the correct locations
file_path1 = '/Users/suchanatratanarueangrong/Mitrphol/streamlit/example.csv'

st.title("Carbon Credit 👨🏻‍💻")

reply_container = st.container()
container = st.container()

with container:
        with st.form(key='my_form', clear_on_submit=False):
            name = st.text_input("ชื่อ", placeholder="โปรดใส่ชื่อของคุณ", key='input')
            age = st.number_input("อายุ", placeholder="Please fill your age")
            date = st.date_input("วันที่ลง")
            fertilizer = st.text_input("ชนิดปุ๋ยที่ใช้", placeholder="โปรดใส่ชนิดปุ๋ยคุณ")
            fertilizer_kilo = st.number_input("จำนวนปุ๋ยที่ใช้ (กิโลกรัม)", placeholder="โปรดใส่จำนวนปุ๋ยของคุณ")
            rai = st.number_input("จำนวนเนื้อที่ในการปลูกอ้อย (ไร่)", placeholder="โปรดใส่พื้นที่ของคุณ")
            fuel = st.number_input("จำนวนน้ำมันที่ใช้ (ลิตร/ไร่)", placeholder="โปรดใส่จำนวนการใช้น้ำมันของคุณ")
            electric = st.number_input("จำนวนไฟฟ้าที่ใช้ (วัตต์)", placeholder="โปรดใส่จำนวนการใช้ไฟฟ้าของคุณ")
            submit_button = st.form_submit_button(label='Send')

            if submit_button and name and age and date and fertilizer and rai and fertilizer_kilo and fuel and electric:
                df = pd.read_csv(file_path1, encoding='utf-8')
                new_row_dict = {'Name': name, 'Age': age, 'Date': date, 'Fertilizer': fertilizer,
                                    'Kilo': fertilizer_kilo, 'Rai': rai, 'Fuel': fuel, 'Electric': electric}
                df = df.append(new_row_dict, ignore_index=True)
                df.to_csv(file_path1, index=False, encoding='utf-8')
                st.session_state['language'] = 'uc'