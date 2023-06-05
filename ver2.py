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
st.write("")
st.write("")
option = st.selectbox(
    '공정율',
    ('10% 미만', '10~19%', '20~29%', '30~39%', '40~49%', '50~59%', '60~69%', '70~79%', '80~89%', '90% 이상'))

filtered_df = df[df["작업프로세스"] == process_type]
city="seoul"
lang="kr"
api="9b833c0ea6426b70902aa7a4b1da285c"
url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&lang={lang}"
response=requests.get(url)
x=response.json()
cel=273.15
temp_unit=" °C"
temp=round(x["main"]["temp"]-cel,2)
icon=x["weather"][0]["icon"]
current_weather=x["weather"][0]["description"].title()
humidity=x['main']['humidity']

def get_temp_score(temp):
    if temp>23 and temp<=26: 
        return 20
    if temp>20 and temp<=23:
        return 17.2
    if temp>26 and temp<=29:
        return 15.8
    if temp>17 and temp<=20:
        return 12.9
    if temp>8 and temp<=11:
        return 12.4
    if temp>14 and temp<=17:
        return 12.2
    if temp>5 and temp<=8:
        return 11.8
    if temp>2 and temp<=5:
        return 9.9
    if temp>11 and temp<=14:
        return 9.5
    if temp>29 and temp<=32:
        return 8.6
    if temp>-1 and temp <=2:
        return 6.1
    if temp>-4 and temp<=-1:
        return 1.9
    if temp>-7 and temp<=-4:
        return 0.6
    if temp>-10 and temp<=-7:
        return 0
    else:
        return '범위 밖'
    
temp_score=get_temp_score(temp)

def get_humidity_score(humidity):
    if humidity>50 and humidity<=60:
       return 20
    if humidity>60 and humidity<=70:
        return 19.9
    if humidity>40 and humidity<=50:
        return 12.2
    if humidity>30 and humidity<=40:
        return 10.9
    if humidity>70 and humidity<=80:
        return 9.9
    if humidity>20 and humidity<=30:
        return 5.0
    if humidity>80 and humidity<=90:
        return 3.3
    if humidity>90 and humidity<=100:
        return 1.0
    if humidity>10 and humidity<=20:
        return 0.9
    if humidity>=0 and humidity<=10:
        return 0
    
humidity_score=get_humidity_score(humidity)

def get_processrate_score(option):
    if option=='10% 미만':
        return 7.0
    if option=='10~19%':
        return 20.0
    if option=='20~29%':
        return 19.2
    if option=='30~39%':
        return 16.5
    if option=='40~49%':
        return 8.8
    if option=='50~59%':
        return 7.0
    if option=='60~69%':
        return 2.1
    if option=='70~79%':
        return 1.7
    if option=='80~89%':
        return 0.0
    if option=='90% 이상':
        return 2.1

processrate_score=get_processrate_score(option)

safety_score = round(20+11+temp_score+humidity_score+processrate_score)


def get_safety_color(score):
    if score >= 80:
        return 'red'
    elif score >= 60:
        return 'orange'
    elif score >= 40:
        return 'yellow'
    else:
        return 'skyblue'

def get_safety_text(score):
    if score >= 80:
        return '위험'
    elif score >= 60:
        return '주의'
    elif score >= 40:
        return '보통'
    else:
        return '안전'

color = get_safety_color(safety_score)
text = get_safety_text(safety_score)



st.write("")
st.write("")
st.markdown("---")
st.write("")
st.write("")
score_html = f"<h1 style='text-align: center; color: {color}; font-weight: bold;'>{safety_score}</h1>"
text_html = f"<h4 style='text-align: center; color: {color};'>{text}</h4>"


col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<h4 style='text-align: center'>오늘의 안전지수</h4>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.markdown(score_html, unsafe_allow_html=True)
    st.markdown(text_html, unsafe_allow_html=True)

with col2:
    st.markdown("<h4 style='text-align: center'>오늘의 알림</h4>", unsafe_allow_html=True)
    alert = Image.open('알림.png')
    st.write("")
    st.write("")
    st.image(alert, use_column_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")
    st.write("")
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
st.write("")
st.write("")
st.markdown("<h2 style='text-align: center'>해당 작업 사고사례</h2>", unsafe_allow_html=True)
st.write("")
st.write("")
col1, col2 = st.columns(2)
with col1:
    st.write("")
    st.write("")
    imginfo1 = Image.open('사례1.png')
    st.image(example1_url, use_column_width=True)
    st.image(imginfo1, use_column_width=True)
    st.write("")
    st.write("")
with col2:
    st.write("")
    st.write("")
    imginfo2 = Image.open('사례2.png')
    st.image(example2_url, use_column_width=True)
    st.image(imginfo2, use_column_width=True)
    st.write("")
    st.write("")

st.write("")
st.write("")


st.markdown("---")
st.markdown("<h2 style='text-align: center'>오늘의 날씨</h2>", unsafe_allow_html=True)
st.write("")
st.write("")

col1, col2, col3=st.columns(3)
with col1:
    st.write("")
    st.write("")
    st.markdown("""
                <h3 style='text-align: center;'>기온</h3>
                <h4 style='text-align: center;'><br>{}</h4>
    """.format(str(temp) + temp_unit),unsafe_allow_html=True)
    st.write("")
    st.write("")
with col2:
    st.write("")
    st.write("")
    st.markdown("""
                <h3 style='text-align: center;'>습도</h3>
                <h4 style='text-align: center;'><br>{}</h4>
    """.format(str(humidity)),unsafe_allow_html=True)
    st.write("")
    st.write("")
with col3:
    st.write("")
    st.write("")
    st.markdown("""
                <h3 style='text-align: center;'>날씨</h3>
                <h4 style='text-align: center;'><br>{}</h4>
    """.format(str(current_weather)),unsafe_allow_html=True)
    st.write("")
    st.write("")
st.subheader(" ")

st.markdown("---")
st.write("")
st.write("")

st.markdown("<h3 style='text-align: center'>주요 원인 및 재발방지 대책</h3>", unsafe_allow_html=True)
st.write("")
st.write("")
image = Image.open('사고유형.png')
st.image(image, use_column_width=True)
