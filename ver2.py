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

filtered_df = df[df["작업프로세스"] == process_type]
city="seoul"
api="9b833c0ea6426b70902aa7a4b1da285c"
url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
response=requests.get(url)
x=response.json()
cel=273.15
temp_unit=" °C"
safety_score = filtered_df["안전지수"].values[0]
accidentpercent=20

temp=str(round(x["main"]["temp"]-cel,2))
icon=x["weather"][0]["icon"]
current_weather=x["weather"][0]["description"].title()

st.write("")
st.write("")
st.markdown("---")

col1, col2 = st.columns([1, 2])

plt.rcParams.update({'font.size': 18})

with col1:
    st.markdown("<h4 style='text-align: center'>오늘의 안전지수</h4>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    fig, ax = plt.subplots()
    ax.pie([safety_score, 100 - safety_score], labels=[safety_score, ""], colors=['skyblue', 'white'])
    ax.axis('equal')
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)


with col2:
    st.markdown("<h4 style='text-align: center'>오늘의 알림</h4>", unsafe_allow_html=True)
    
    accident_type = filtered_df["사고유형1"].values[0]
    prevention_measure = filtered_df["재발방지1-1"].values[0]
    st.write("")
    st.write("")
    st.write("오늘의 작업 중 발생빈도가 높은 사고 유형은 **{}** 이므로".format(accident_type))
    st.write("**{}** 에 주의하시기 바랍니다.".format(prevention_measure))

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
example1_url = "https://www.csi.go.kr/com/imageViewProc.do?file_no=mUN3ynYi9kdRnTRykUqVSA=="
example2_url = "https://www.csi.go.kr/com/imageViewProc.do?file_no=pn/13Ei2W4Mbni3FjWp/UQ=="

st.markdown("<h2 style='text-align: center'>해당 작업 사고사례</h2>", unsafe_allow_html=True)
st.write("")
st.write("")
col1, col2 = st.columns(2)
with col1:
    st.image(example1_url, use_column_width=True)
with col2:
    st.image(example2_url, use_column_width=True)
st.write("")
st.write("")
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h5 style='text-align: center'>철근콘크리트 공사-시스템동바리</h5>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center'>새벽 우천 후 시스템비계 작업발판에서 거푸집 조립 작업 후 이동하며 넘어짐, 요추 골절 발생</h6>", unsafe_allow_html=True)
with col2:
    st.markdown("<h5 style='text-align: center;'>철골 공사</h5>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center;'>지붕 층 슬라브에서 철근 운반 중 기 배근된 철근에 전도방지 조치 미흡으로 걸려 넘어짐, 발목 골절</h6>", unsafe_allow_html=True)


st.markdown("---")
st.markdown("<h2 style='text-align: center'>오늘의 날씨</h2>", unsafe_allow_html=True)
st.write("")
st.write("")

col1, col2=st.columns(2)
with col1:
    st.markdown("""
                <h3 style='text-align: center;'>기온</h3>
                <h4 style='text-align: center;'><br>{}</h4>
    """.format(str(temp+temp_unit)),unsafe_allow_html=True)
with col2:
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
