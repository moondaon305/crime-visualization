import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Streamlit 앱 제목 설정
st.title('📊 지역별 범죄 통계 시각화')
st.subheader('제공된 데이터 기반')

# CSV 파일 경로 (같은 디렉토리에 있다고 가정)
csv_file_path = '범죄 발생 지역별 통계.csv'

# CSV 파일 로드 및 데이터 전처리
@st.cache_data # 데이터를 캐시하여 앱 성능 향상
def load_and_process_data(path):
    try:
        # 파일 로드 (한글 인코딩 고려)
        df = pd.read_csv(path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding='euc-kr')

    # 숫자 컬럼만 선택하여 NaN 값을 0으로 채우기 (데이터 타입 문제 방지)
    # 예시 데이터에서 '강도'의 서울중구 값이 비어있어서 오류를 방지하기 위함
    numeric_cols = df.columns[2:] # '서울종로구', '서울중구' 등 지역 컬럼
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # 지역 컬럼들을 '지역'과 '발생건수' 컬럼으로 녹이기 (melt)
    # 이렇게 하면 각 지역의 범죄 건수가 행으로 표현되어 시각화에 용이해집니다.
    df_melted = df.melt(id_vars=['범죄대분류', '범죄중분류'],
                        var_name='지역',
                        value_name='발생건수')

    return df_melted

df_processed = load_and_process_data(csv_file_path)

if df_processed is not None:
    st.subheader('전처리된 데이터 미리보기')
    st.dataframe(df_processed.head())

    st.subheader('데이터 통계 요약')
    st.write(df_processed.describe())

    st.markdown('---') # 구분선

    # ------------------- 시각화 섹션 -------------------

    # 1. 지역별 총 범죄 발생 건수
    st.header('지역별 총 범죄 발생 건수')
    total_crime_by_region = df_processed.groupby('지역')['발생건수'].sum().reset_index()
    fig_total_region = px.bar(total_crime_by_region, x='지역', y='발생건수',
                              title='각 지역별 총 범죄 발생 건수',
                              labels={'지역': '지역', '발생건수': '총 발생 건수'},
                              color='지역')
    st.plotly_chart(fig_total_region)

    st.markdown('---') # 구분선

    # 2. 범죄 대분류 및 중분류별 지역 통계
    st.header('범죄 유형별 지역 통계')

    # 필터링을 위한 선택 박스
    all_major_categories = ['전체'] + df_processed['범죄대분류'].unique().tolist()
    selected_major_category = st.selectbox('범죄 대분류 선택', all_major_categories)

    if selected_major_category == '전체':
        filtered_df = df_processed
    else:
        filtered_df = df_processed[df_processed['범죄대분류'] == selected_major_category]

    # 선택된 대분류에 해당하는 중분류만 필터링
    all_minor_categories = ['전체'] + filtered_df['범죄중분류'].unique().tolist()
    selected_minor_category = st.selectbox('범죄 중분류 선택', all_minor_categories)

    if selected_minor_category != '전체':
        filtered_df = filtered_df[filtered_df['범죄중분류'] == selected_minor_category]

    # 시각화 (선택된 데이터에 따라 동적 변화)
    if not filtered_df.empty:
        fig_crime_type_region = px.bar(filtered_df, x='지역', y='발생건수',
                                       color='범죄중분류', barmode='group',
                                       title=f'{selected_major_category} - {selected_minor_category}별 지역별 범죄 발생 건수',
                                       labels={'지역': '지역', '발생건수': '발생 건수', '범죄중분류': '범죄 중분류'})
        st.plotly_chart(fig_crime_type_region)
    else:
        st.warning('선택한 조건에 해당하는 데이터가 없습니다.')

    st.markdown('---') # 구분선

    # 3. 특정 지역의 범죄 유형 분포
    st.header('특정 지역의 범죄 유형 분포')
    all_regions = df_processed['지역'].unique().tolist()
    selected_region_for_pie = st.selectbox('범죄 유형 분포를 볼 지역 선택', all_regions)

    if selected_region_for_pie:
        region_data = df_processed[df_processed['지역'] == selected_region_for_pie]
        crime_type_distribution = region_data.groupby('범죄중분류')['발생건수'].sum().reset_index()

        fig_pie = px.pie(crime_type_distribution, values='발생건수', names='범죄중분류',
                         title=f'{selected_region_for_pie}의 범죄 중분류별 발생 비율',
                         hole=0.3) # 도넛 차트
        st.plotly_chart(fig_pie)

else:
    st.error(f"'{csv_file_path}' 파일을 로드할 수 없습니다. 파일이 존재하며 올바른 형식인지 확인해주세요.")
    st.info("제공해주신 CSV 내용을 '범죄 발생 지역별 통계.csv' 파일에 저장했는지 확인해주세요.")
