import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 범죄 발생 지역별 통계 시각화")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("데이터 미리보기:")
    st.dataframe(df)

    if st.checkbox("컬럼 목록 보기"):
        st.write(df.columns.tolist())

    if '지역' in df.columns and '발생건수' in df.columns:
        crime_by_region = df.groupby('지역')['발생건수'].sum().sort_values(ascending=False)
        
        st.subheader("지역별 범죄 발생 건수")
        fig, ax = plt.subplots()
        sns.barplot(x=crime_by_region.values, y=crime_by_region.index, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("⚠️ '지역' 또는 '발생건수' 컬럼이 데이터에 없습니다.")
