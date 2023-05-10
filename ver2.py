import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel("test.xlsx", engine='openpyxl')


st.markdown("<h1 style='text-align: center'>건설안전사고 예측 시스템</h1>", unsafe_allow_html=True)

process_types = df["작업프로세스"].unique().tolist()
process_type = st.selectbox("작업 프로세스 종류 선택", process_types)


filtered_df = df[df["작업프로세스"] == process_type]

st.markdown("---")

st.markdown("<h2 style='text-align: center'>우리 현장의 안전지수</h2>", unsafe_allow_html=True)

safety_score = filtered_df["안전지수"].values[0]
col1, col2=st.columns(2)
col1.metric("점수", str(safety_score))
col2.metric("전체 사고 수 대비 해당 작업 사고 발생률", "20%")

col1, col2 = st.columns([1, 2])


with col1:
    st.markdown("<div style='border-radius: 10px; background-color: #F5F5F5; padding: 10px;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center'>safe index</h4>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.pie([safety_score, 100 - safety_score], labels=["safe", "danger"])
    ax.axis('equal')
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)


with col2:
    st.markdown("<div style='border-radius: 10px; background-color: #F5F5F5; padding: 10px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center'>오늘의 알림</h4>", unsafe_allow_html=True)
    accident_type = filtered_df["사고유형1"].values[0]
    prevention_measure = filtered_df["재발방지1-1"].values[0]
    st.write("오늘의 작업 중 발생빈도가 높은 사고 유형은", accident_type, "이므로")
    st.write(prevention_measure,"에 주의하시기 바랍니다.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("<h3 style='text-align: center'>주요 원인 및 재발방지 대책</h3>", unsafe_allow_html=True)

col1,col2=st.columns([1,2])
with col1:
    st.write("주원인1-1: ", filtered_df["주원인1-1"].values[0])
    st.write("주원인1-2: ", filtered_df["주원인1-2"].values[0])
    st.write("주원인1-3: ", filtered_df["주원인1-3"].values[0])

with col2:
    st.markdown("<div style='border-radius: 10px; background-color: #F5F5F5; padding: 10px; text-align: center;'>", unsafe_allow_html=True)
    st.write("재발방지1-1: ", filtered_df["재발방지1-1"].values[0])
    st.write("재발방지1-2: ", filtered_df["재발방지1-2"].values[0])
    st.write("재발방지1-3: ", filtered_df["재발방지1-3"].values[0])
    st.markdown("</div>", unsafe_allow_html=True)

