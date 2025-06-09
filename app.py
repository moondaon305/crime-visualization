import streamlit as st
import pandas as pd

# GitHub 저장소 raw 파일 URL
csv_url = "https://github.com/moondaon305/crime-visualization/raw/main/crime.csv"

st.title("범죄 발생 지역별 통계 시각화")

try:
    df = pd.read_csv(csv_url, encoding='cp949')  # 인코딩 문제 발생 시 utf-8로 변경해보세요
    st.write("데이터 미리보기")
    st.dataframe(df.head())

    # 예시: 지역별 범죄 건수 합계 계산 및 시각화
    crime_sum_by_region = df.groupby('지역')['범죄건수'].sum().reset_index()

    st.bar_chart(crime_sum_by_region.set_index('지역'))

except Exception as e:
    st.error(f"파일 읽기 중 오류 발생: {e}")
