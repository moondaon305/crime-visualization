import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

st.title("한반도 범죄 발생 지역별 통계 시각화")

csv_path = "https://raw.githubusercontent.com/moondaon305/crime-visualization/main/crime_data.csv"
df = pd.read_csv(csv_path, encoding='utf-8')

df_long = df.melt(id_vars=['범죄대분류', '범죄중분류'], var_name='지역', value_name='발생건수')
df_grouped = df_long.groupby('지역')['발생건수'].sum().reset_index()
df_grouped['지역'] = df_grouped['지역'].str.strip()

geojson_url = "https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2019/json/TL_SCCO_SIG.json"
gdf = gpd.read_file(geojson_url)

merged = gdf.merge(df_grouped, left_on='SIG_KOR_NM', right_on='지역')
merged = merged.reset_index()

fig = px.choropleth(
    merged,
    geojson=gdf.__geo_interface__,
    locations='index',
    color='발생건수',
    hover_name='SIG_KOR_NM',
    projection="mercator",
    color_continuous_scale="Reds",
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig)
