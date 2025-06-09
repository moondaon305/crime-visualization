import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="범죄 발생 지역별 통계", layout="wide")

st.title("📊 범죄 발생 지역별 통계 시각화")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except pd.errors.EmptyDataError:
        st.error("⚠️ CSV 파일이 비어 있거나 내용을 읽을 수 없습니다.")
    else:
        st.success("✅ 데이터 업로드 성공!")
        
        # '지역' 열을 문자열로 변환
        df['지역'] = df['지역'].astype(str)

        st.subheader("📌 데이터 미리보기")
        st.dataframe(df)

        st.subheader("📍 지역별 범죄 건수 비교")

        crime_types = ['살인', '강도', '강간·강제추행', '절도', '폭력']
        selected_crime = st.selectbox("🔎 분석할 범죄 유형을 선택하세요:", crime_types)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='지역', y=selected_crime, data=df, ax=ax, palette='coolwarm')
        plt.xticks(rotation=45)
        plt.title(f"{selected_crime} 발생 건수 (지역별)")
        st.pyplot(fig)
else:
    st.info("⬅️ 왼쪽에서 CSV 파일을 업로드해 주세요.")
