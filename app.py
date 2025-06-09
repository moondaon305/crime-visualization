import streamlit as st
import pandas as pd

csv_url = "https://raw.githubusercontent.com/moondaon305/crime-visualization/main/%EA%B2%BD%EC%B0%B0%EC%B2%AD_%EB%B2%94%EC%A3%84%20%EB%B0%9C%EC%83%9D%20%EC%A7%80%EC%97%AD%EB%B3%84%20%ED%86%B5%EA%B3%84_20231231.csv"

st.title("범죄 발생 지역별 통계 시각화")

try:
    df = pd.read_csv(csv_url, encoding='cp949')  # 인코딩 에러나면 utf-8도 시도해보세요
    st.write("데이터 미리보기")
    st.dataframe(df.head())

    # 지역별 범죄건수 합계 시각화 (컬럼명 예시에 맞게 수정하세요)
    crime_sum_by_region = df.groupby('지역')['범죄건수'].sum().reset_index()

    st.bar_chart(crime_sum_by_region.set_index('지역'))

except Exception as e:
    st.error(f"파일 읽기 중 오류 발생: {e}")
