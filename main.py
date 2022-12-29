import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

tab1, tab2, tab3, tab4 = st.tabs(
    ["All", "Distribution", "Radar Type", "Lat-Lon"])

with tab1:
    st.header("All")
    df = pd.read_excel('./list_jp_radars.xlsx')
    df['region_id'] = df['region_id'].apply(str)
    distributor = list(np.unique(df['distributor']))
    radar_type = list(np.unique(df['radar_type']))
    option_distribution = st.selectbox('Select a Distributor: ', distributor)
    option_radar_type = st.selectbox('Select a Radar Type:', radar_type)
    # st.write('You selected:', option_distribution)

    # option_distribution = st.sidebar.selectbox("Select a Distributor:",
    #                                            distributor)
    # option_radar_type = st.sidebar.selectbox("Select a Radar Type:", radar_type)

    df_fillter = df[(df['distributor'] == option_distribution)
                    & (df['radar_type'] == option_radar_type)]
    df_small = df_fillter[['lat', 'lon']]
    df_small.dropna(inplace=True)
    st.map(df_small)
    st.dataframe(df_fillter)

    # title = st.text_input('Movie title', 'Life of Brian')
    # st.write('The current movie title is', title)

with tab2:
    st.header("Distribution")

    option_distribution = st.selectbox('Select a Distributor:', distributor)

    df_cband = df[(df['distributor'] == option_distribution)
                  & (df['radar_type'] == 'cband')]
    df_vil_cband = df_cband[['lat', 'lon']]
    df_vil_cband.dropna(inplace=True)

    df_xband = df[(df['distributor'] == option_distribution)
                  & (df['radar_type'] == 'xband')]
    df_vil_xband = df_xband[['lat', 'lon']]
    df_vil_xband.dropna(inplace=True)

    # lon_min, lon_max, lat_min, lat_max
    lon_min = st.text_input('Longtitude Min', 139.41898670588236)
    lon_max = st.text_input('Longtitude Max', 140.59545729411767)
    lat_min = st.text_input('Latitude Min', 35.24538254954955)
    lat_max = st.text_input('Latitude Max', 36.146283450450454)

    lon_min = float(lon_min)
    lon_max = float(lon_max)
    lat_min = float(lat_min)
    lat_max = float(lat_max)

    df_distribution = df[(df['distributor'] == option_distribution)]
    df_distribution.reset_index(inplace=True)
    df_distribution.drop(columns='index', inplace=True)
    radar_list = []
    for i in range(df_distribution.shape[0]):
        lat = df_distribution['lat'][i]
        lon = df_distribution['lon'][i]
        if lon_min <= lon and lon <= lon_max:
            if lat_min <= lat and lat <= lat_max:
                radar_list.append(i)

    df_show = df_distribution.filter(items=radar_list, axis=0)

    LAND_COVER = [[[lon_max, lat_min], [lon_max, lat_max], [lon_min, lat_max],
                   [lon_min, lat_min]]]

    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=37.40572931061236,
                longitude=139.83859489908298,
                zoom=5,
                pitch=30,
            ),
            layers=[
                pdk.Layer('ScatterplotLayer',
                          data=df_vil_xband,
                          get_position='[lon, lat]',
                          get_color='[200, 30, 0, 120]',
                          get_radius=10000),
                pdk.Layer('ScatterplotLayer',
                          data=df_vil_cband,
                          get_position='[lon, lat]',
                          get_color='[0, 255, 5, 120]',
                          get_radius=20000),
                pdk.Layer(
                    'PolygonLayer',
                    LAND_COVER,
                    stroked=False,
                    # processes the data as a flat longitude-latitude pair
                    get_polygon='-',
                    get_fill_color=[0, 0, 0, 20])
            ]))

    st.dataframe(df_show)

with tab3:
    st.header("Radar Type")

    option_radar_type = st.selectbox('Select a Distributor:  ', radar_type)

    df_radar_type = df[(df['radar_type'] == option_radar_type)]
    # df_vil_radar_type = df_radar_type[['lat', 'lon']]
    # df_vil_radar_type.dropna(inplace=True)

    df_jma = df_radar_type[(df_radar_type['distributor'] == 'jma')]
    df_vil_jma = df_jma[['lat', 'lon']]
    df_vil_jma.dropna(inplace=True)

    df_dias = df_radar_type[(df_radar_type['distributor'] == 'dias')]
    df_vil_dias = df_dias[['lat', 'lon']]
    df_vil_dias.dropna(inplace=True)

    df_frics = df_radar_type[(df_radar_type['distributor'] == 'frics')]
    df_vil_frics = df_frics[['lat', 'lon']]
    df_vil_frics.dropna(inplace=True)

    # lon_min, lon_max, lat_min, lat_max
    lon_min = st.text_input('Longtitude Min ', 139.41898670588236)
    lon_max = st.text_input('Longtitude Max ', 140.59545729411767)
    lat_min = st.text_input('Latitude Min ', 35.24538254954955)
    lat_max = st.text_input('Latitude Max ', 36.146283450450454)

    lon_min = float(lon_min)
    lon_max = float(lon_max)
    lat_min = float(lat_min)
    lat_max = float(lat_max)

    df_distribution = df[(df['radar_type'] == option_radar_type)]
    df_distribution.reset_index(inplace=True)
    df_distribution.drop(columns='index', inplace=True)
    radar_list = []
    for i in range(df_distribution.shape[0]):
        lat = df_distribution['lat'][i]
        lon = df_distribution['lon'][i]
        if lon_min <= lon and lon <= lon_max:
            if lat_min <= lat and lat <= lat_max:
                radar_list.append(i)

    df_show = df_distribution.filter(items=radar_list, axis=0)

    LAND_COVER = [[[lon_max, lat_min], [lon_max, lat_max], [lon_min, lat_max],
                   [lon_min, lat_min]]]

    polygon_layer = pdk.Layer(
        'PolygonLayer',
        LAND_COVER,
        stroked=False,
        # processes the data as a flat longitude-latitude pair
        get_polygon='-',
        get_fill_color=[0, 0, 0, 20])

    jma_layer = pdk.Layer('ScatterplotLayer',
                          data=df_vil_jma,
                          get_position='[lon, lat]',
                          get_color='[0, 250, 0, 120]',
                          get_radius=20000),

    dias_layer = pdk.Layer('ScatterplotLayer',
                           data=df_vil_dias,
                           get_position='[lon, lat]',
                           get_color='[200, 30, 0, 120]',
                           get_radius=10000)

    if option_radar_type == 'xband':
        frics_layer_radius = 10000
    else:
        frics_layer_radius = 20000

    frics_layer = pdk.Layer('ScatterplotLayer',
                            data=df_vil_frics,
                            get_position='[lon, lat]',
                            get_color='[0, 30, 250, 120]',
                            get_radius=frics_layer_radius),

    st.write('Red:  DIAS')
    st.write('GREEN: JMA')
    st.write('BLUE: FRICS')

    st.pydeck_chart(
        pdk.Deck(map_style=None,
                 initial_view_state=pdk.ViewState(
                     latitude=37.40572931061236,
                     longitude=139.83859489908298,
                     zoom=5,
                     pitch=30,
                 ),
                 layers=[jma_layer, dias_layer, frics_layer, polygon_layer]))

    st.dataframe(df_show)

with tab4:
    st.header("Lat Lon")

    df_jma = df[(df['distributor'] == 'jma')]
    df_vil_jma = df_jma[['lat', 'lon']]
    df_vil_jma.dropna(inplace=True)

    df_dias = df[(df['distributor'] == 'dias')]
    df_vil_dias = df_dias[['lat', 'lon']]
    df_vil_dias.dropna(inplace=True)

    df_frics = df[(df['distributor'] == 'frics')]
    df_frics_xband = df_frics[df_frics['radar_type'] == 'xband']
    df_vil_frics_xband = df_frics_xband[['lat', 'lon']]
    df_vil_frics_xband.dropna(inplace=True)

    df_frics_cband = df_frics[df_frics['radar_type'] == 'cband']
    df_vil_frics_cband = df_frics_cband[['lat', 'lon']]
    df_vil_frics_cband.dropna(inplace=True)

    # lon_min, lon_max, lat_min, lat_max
    lon_min = st.text_input('Longtitude Min:', 139.41898670588236)
    lon_max = st.text_input('Longtitude Max:', 140.59545729411767)
    lat_min = st.text_input('Latitude Min:', 35.24538254954955)
    lat_max = st.text_input('Latitude Max:', 36.146283450450454)

    lon_min = float(lon_min)
    lon_max = float(lon_max)
    lat_min = float(lat_min)
    lat_max = float(lat_max)

    radar_list = []
    for i in range(df.shape[0]):
        lat = df['lat'][i]
        lon = df['lon'][i]
        if lon_min <= lon and lon <= lon_max:
            if lat_min <= lat and lat <= lat_max:
                radar_list.append(i)

    df_show = df.filter(items=radar_list, axis=0)

    LAND_COVER = [[[lon_max, lat_min], [lon_max, lat_max], [lon_min, lat_max],
                   [lon_min, lat_min]]]

    polygon_layer = pdk.Layer(
        'PolygonLayer',
        LAND_COVER,
        stroked=False,
        # processes the data as a flat longitude-latitude pair
        get_polygon='-',
        get_fill_color=[0, 0, 0, 20])

    jma_layer = pdk.Layer('ScatterplotLayer',
                          data=df_vil_jma,
                          get_position='[lon, lat]',
                          get_color='[0, 250, 0, 120]',
                          get_radius=30000),

    dias_layer = pdk.Layer('ScatterplotLayer',
                           data=df_vil_dias,
                           get_position='[lon, lat]',
                           get_color='[200, 30, 0, 120]',
                           get_radius=10000)

    frics_xband_layer = pdk.Layer('ScatterplotLayer',
                                  data=df_vil_frics_xband,
                                  get_position='[lon, lat]',
                                  get_color='[0, 30, 250, 120]',
                                  get_radius=10000),

    frics_cband_layer = pdk.Layer('ScatterplotLayer',
                                  data=df_vil_frics_cband,
                                  get_position='[lon, lat]',
                                  get_color='[0, 30, 250, 120]',
                                  get_radius=30000),
    st.write('Red:  DIAS')
    st.write('GREEN: JMA')
    st.write('BLUE: FRICS')
    st.pydeck_chart(
        pdk.Deck(map_style=None,
                 initial_view_state=pdk.ViewState(
                     latitude=37.40572931061236,
                     longitude=139.83859489908298,
                     zoom=5,
                     pitch=30,
                 ),
                 layers=[
                     jma_layer, dias_layer, frics_xband_layer,
                     frics_cband_layer, polygon_layer
                 ]))

    st.dataframe(df_show)