import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

st.title("한반도 범죄 발생 지역별 통계 시각화")

# 1. CSV 데이터 불러오기 (여기에 본인 csv raw github URL 또는 로컬 파일 경로 넣기)
csv_path = "https://raw.githubusercontent.com/moondaon305/crime-visualization/main/crime_data.csv"
df = pd.read_csv(csv_path, encoding='utf-8')


# 2. 데이터 형태 변환 (wide → long)
df_long = df.melt(id_vars=['범죄대분류', '범죄중분류'], var_name='지역', value_name='발생건수')

# 3. 지역별 범죄 발생 건수 합계 (범죄 유형 구분 없이 전체 합)
df_grouped = df_long.groupby('지역')['발생건수'].sum().reset_index()

st.write("지역별 총 범죄 발생 건수 데이터 예시")
st.dataframe(df_grouped.head())

# 4. GeoJSON 파일 불러오기 (시군구 경계 geojson 파일 URL 또는 로컬 경로)
geojson_url = "https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2019/json/TL_SCCO_SIG.json"
gdf = gpd.read_file(geojson_url)

# 5. GeoDataFrame 컬럼명 확인 (지역명 컬럼 이름이 'SIG_KOR_NM'임)
# st.write(gdf.columns)
# st.write(gdf['SIG_KOR_NM'].unique())

# 6. 지역명 컬럼 맞추기 (csv의 '지역' 컬럼과 일치하게 변환)
# (예: 공백, 띄어쓰기, 구 이름 등 정확히 맞아야 함)
# 여기서는 간단히 문자열 공백 제거만 처리 예시
df_grouped['지역'] = df_grouped['지역'].str.strip()

# 7. GeoDataFrame과 데이터 병합
merged = gdf.merge(df_grouped, left_on='SIG_KOR_NM', right_on='지역')

# 8. 지도 시각화 (Plotly choropleth)
fig = px.choropleth(
    merged,
    geojson=merged.geometry,
    locations=merged.index,
    color='발생건수',
    hover_name='SIG_KOR_NM',
    projection="mercator",
    color_continuous_scale="Reds",
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig)
