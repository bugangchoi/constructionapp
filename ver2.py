import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime,requests
from PIL import Image


df = pd.read_excel("test.xlsx", engine='openpyxl')


st.markdown("<h1 style='text-align: center'>건설안전사고 알림 서비스</h1>", unsafe_allow_html=True)
st.write("")
st.write("")
process_types = df["작업프로세스"].unique().tolist()
process_type = st.selectbox("작업 프로세스 종류 선택", process_types)
option = st.selectbox(
    '안전방호조치 여부',
    ('조치', '비조치', '해당없음'))

filtered_df = df[df["작업프로세스"] == process_type]
city="seoul"
lang="kr"
api="9b833c0ea6426b70902aa7a4b1da285c"
url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&lang={lang}"
response=requests.get(url)
x=response.json()
cel=273.15
temp_unit=" °C"
safety_score = filtered_df["안전지수"].values[0]

def get_safety_color(score):
    if score <= 20:
        return 'red'
    elif score <= 40:
        return 'orange'
    elif score <= 60:
        return 'yellow'
    else:
        return 'skyblue'

def get_safety_text(score):
    if score <= 20:
        return '위험'
    elif score <= 40:
        return '주의'
    elif score <= 60:
        return '보통'
    else:
        return '안전'

color = get_safety_color(safety_score)
text = get_safety_text(safety_score)

temp=round(x["main"]["temp"]-cel,2)
icon=x["weather"][0]["icon"]
current_weather=x["weather"][0]["description"].title()
humidity=x['main']['humidity']

st.write("")
st.write("")
st.markdown("---")
score_html = f"<h1 style='text-align: center; color: {color}; font-weight: bold;'>{safety_score}</h1>"
text_html = f"<h4 style='text-align: center; color: {color};'>{text}</h4>"


col1, col2 = st.columns([1, 2])

plt.rcParams.update({'font.size': 18})

with col1:
    st.markdown("<h4 style='text-align: center'>오늘의 안전지수</h4>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.markdown(score_html, unsafe_allow_html=True)
    st.markdown(text_html, unsafe_allow_html=True)

with col2:
    st.markdown("<h4 style='text-align: center'>오늘의 알림</h4>", unsafe_allow_html=True)
    alert = Image.open('알림.png')
    st.image(alert, use_column_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if humidity >= 70:
        humidity_alert = Image.open('습도알림.png')
        st.image(humidity_alert, use_column_width=True)
    if temp >= 24:
        temperature_alert = Image.open('기온알림.png')
        st.image(temperature_alert, use_column_width=True)
    if option == "비조치":
        safety_alert = Image.open('방호조치알림.png')
        st.image(safety_alert, use_column_width=True)

st.markdown("---")
example1_url = "https://www.csi.go.kr/com/imageViewProc.do?file_no=mUN3ynYi9kdRnTRykUqVSA=="
example2_url = "https://www.csi.go.kr/com/imageViewProc.do?file_no=pn/13Ei2W4Mbni3FjWp/UQ=="

st.markdown("<h2 style='text-align: center'>해당 작업 사고사례</h2>", unsafe_allow_html=True)
st.write("")
st.write("")
col1, col2 = st.columns(2)
with col1:
    imginfo1 = Image.open('사례1.png')
    st.image(example1_url, use_column_width=True)
    st.image(imginfo1, use_column_width=True)
with col2:
    imginfo2 = Image.open('사례2.png')
    st.image(example2_url, use_column_width=True)
    st.image(imginfo2, use_column_width=True)
st.write("")
st.write("")



st.markdown("---")
st.markdown("<h2 style='text-align: center'>오늘의 날씨</h2>", unsafe_allow_html=True)
st.write("")
st.write("")

col1, col2, col3=st.columns(3)
with col1:
    st.markdown("""
                <h3 style='text-align: center;'>기온</h3>
                <h4 style='text-align: center;'><br>{}</h4>
    """.format(str(temp) + temp_unit),unsafe_allow_html=True)
with col2:
    st.markdown("""
                <h3 style='text-align: center;'>습도</h3>
                <h4 style='text-align: center;'><br>{}</h4>
    """.format(str(humidity)),unsafe_allow_html=True)
with col3:
    st.markdown("""
                <h3 style='text-align: center;'>날씨</h3>
                <h4 style='text-align: center;'><br>{}</h4>
    """.format(str(current_weather)),unsafe_allow_html=True)
st.subheader(" ")

st.markdown("---")
st.write("")
st.write("")

st.markdown("<h3 style='text-align: center'>주요 원인 및 재발방지 대책</h3>", unsafe_allow_html=True)

image = Image.open('사고유형.png')
st.image(image, use_column_width=True)
