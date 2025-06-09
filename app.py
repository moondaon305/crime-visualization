import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="범죄 발생 지역 통계", layout="wide")

st.title("📊 범죄 발생 지역별 통계 시각화")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 한글 깨짐 방지를 위한 인코딩 처리
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='cp949')

    st.subheader("데이터 미리보기")
    st.dataframe(df)

    # 열 이름 목록 보여주기
    st.subheader("시각화")
    columns = df.columns.tolist()
    selected_column = st.selectbox("어떤 열을 시각화할까요?", columns)

    fig, ax = plt.subplots()
    sns.countplot(data=df, x=selected_column, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("왼쪽에서 CSV 파일을 업로드해 주세요.")
