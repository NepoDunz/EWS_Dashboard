

import streamlit as st
import pandas as pd
import altair as alt
# from mpl_toolkits.basemap import Basemap
import numpy as np
# import json
# import requests
# import geopandas as gpd
# import matplotlib.pyplot as plt
# import plotly.express as px



st.set_page_config(
    page_title="EWS Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

# # Add CSS to change the background color
# st.markdown(
#     """
#     <style>
#     body {
#         background-color: #333333;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# https://blog.streamlit.io/crafting-a-dashboard-app-in-python-using-streamlit/

data = {
    'Countries': ['Ghana', 'Senegal', 'India', 'Indonesia', 'Turkiye','Ghana', 'Senegal', 'India', 'Indonesia', 'Turkiye'],
    'country_code': ['GHA', 'SEN', 'IND', 'IDN', 'TUR','GHA', 'SEN', 'IND', 'IDN', 'TUR'],
    'id': [1, 2, 4, 5, 6,1, 2, 4, 5, 6],
    'year': [2024, 2024, 2024, 2024, 2024,2023, 2023, 2023, 2023, 2023],
    'Overall risk factor': [7.3, 9.2, 2.4, 5.4, 8.3,6.3, 5.2, 6.4, 3.4, 6.3],
    'Fiscal risk factor': [7.3, 9.2, 2.4, 5.4, 8.3,6.3, 5.2, 6.4, 3.4, 6.3],
    'Financial risk factor': [7.3, 9.2, 2.4, 5.4, 8.3,6.3, 5.2, 6.4, 3.4, 6.3],
    'External risk factor': [7.3, 9.2, 2.4, 5.4, 8.3,6.3, 5.2, 6.4, 3.4, 6.3]
}

# Generate random values for the 'risk factor' column
data['Fiscal risk factor'] = np.round(np.random.uniform(0, 10, size=len(data['Countries'])),1)
data['Financial risk factor'] = np.round(np.random.uniform(0, 10, size=len(data['Countries'])),1)
data['External risk factor'] = np.round(np.random.uniform(0, 10, size=len(data['Countries'])),1)
df_reshaped = pd.DataFrame(data)

with st.sidebar:
    st.title('🏂 EWS Dashboard')
    
    year_list = list(df_reshaped.year.unique())[::-1]
    
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="Overall risk factor", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


# def make_choropleth(input_df, input_id, input_column, input_color_theme):
#     choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="ISO-3",
#                                color_continuous_scale=input_color_theme,
#                                range_color=(0, max(df_selected_year['Overall risk factor'])),
#                                scope="world",
#                                labels={'Overall risk factor':'Risk Factor'}
#                               )
#     choropleth.update_layout(
#         template='plotly_dark',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         margin=dict(l=0, r=0, t=0, b=0),
#         height=350
#     )
#     return choropleth
# Sample data for demonstration
# world = alt.topo_feature('https://vega.github.io/vega-datasets/data/world-110m.json', 'countries')

# def make_world_chart(input_df, input_id, input_column, selected_color_theme):
#     # Create Altair Chart
#     chart = alt.Chart(world).mark_geoshape(
#         fill='lightgray',
#         stroke='white'
#     ).transform_lookup(
#         lookup='id',
#         from_=alt.LookupData(input_df, input_id, [input_column])
#     ).encode(
#         color=alt.Color(input_column, scale=alt.Scale(scheme=selected_color_theme))
#     ).properties(
#         width=700,
#         height=400
#     ).project(
#         'equirectangular'
#     )

#     return chart

# def make_world_chart(input_df, input_id, input_column, selected_color_theme):
#     # Load GeoJSON data from URL
#     url = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson'
#     geojson_data = json.loads(requests.get(url).text)

#     # Convert GeoJSON to DataFrame
#     geojson_df = pd.json_normalize(geojson_data['features'])

#     # Merge the input DataFrame with the GeoDataFrame
#     merged = pd.merge(geojson_df, input_df, left_on='properties.iso_a3', right_on=input_id, how='left')

#     # Create an Altair chart
#     chart = alt.Chart(alt.Data(values=merged)).mark_geoshape(
#         fill='lightgray',
#         stroke='white'
#     ).encode(
#         color=alt.Color(input_column, scale=alt.Scale(scheme=selected_color_theme))
#     ).properties(
#         width=700,
#         height=400
#     ).project('naturalEarth1')

#     return chart

def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['risk_difference'] = selected_year_data['Overall risk factor'].sub(previous_year_data['Overall risk factor'], fill_value=0)
  return pd.concat([selected_year_data.Countries, selected_year_data.id, selected_year_data['Overall risk factor'], selected_year_data.risk_difference], axis=1).sort_values(by="risk_difference", ascending=False)

def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

col = st.columns((2.5, 4, 3), gap='medium')


with col[2]:
    st.markdown('#### Changes in country risk')

    df_risk_difference_sorted = calculate_population_difference(df_reshaped, selected_year)

    if selected_year > 2010:
        first_country_name = df_risk_difference_sorted.Countries.iloc[0]
        first_country_risk = (df_risk_difference_sorted['Overall risk factor'].iloc[0])
        first_country_delta = round(df_risk_difference_sorted.risk_difference.iloc[0])
    else:
        first_country_name = '-'
        first_country_risk = '-'
        first_country_delta = ''
    st.metric(label=first_country_name, value=first_country_risk, delta=first_country_delta)

    if selected_year > 2010:
        last_country_name = df_risk_difference_sorted.Countries.iloc[-1]
        last_country_risk = df_risk_difference_sorted['Overall risk factor'].iloc[-1] 
        last_country_delta = round(df_risk_difference_sorted.risk_difference.iloc[-1])   
    else:
        last_country_name = '-'
        last_country_risk = '-'
        last_country_delta = ''
    st.metric(label=last_country_name, value=last_country_risk, delta=last_country_delta)

    
    st.markdown('#### Country risk')

    if selected_year > 2010:
        # Filter states with population difference > 50000
        # df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference_absolute > 50000]
        df_greater_1 = df_risk_difference_sorted[df_risk_difference_sorted.risk_difference > 0]
        df_less_1 = df_risk_difference_sorted[df_risk_difference_sorted.risk_difference < 0]
        
        # % of States with population difference > 50000
        country_risk_greater = round((len(df_greater_1)/df_risk_difference_sorted.Countries.nunique())*100)
        country_risk_less = round((len(df_less_1)/df_risk_difference_sorted.Countries.nunique())*100)
        donut_chart_greater = make_donut(country_risk_greater, 'Risk increase', 'red')
        donut_chart_less = make_donut(country_risk_less, 'Risk decrease', 'green')
    else:
        country_risk_greater = 0
        country_risk_less = 0
        donut_chart_greater = make_donut(country_risk_greater, 'Risk increase', 'red')
        donut_chart_less = make_donut(country_risk_less, 'Risk decrease', 'green')

    risk_col = st.columns((0.2, 1, 0.2))
    with risk_col[1]:
        st.write('Risk increase')
        st.altair_chart(donut_chart_greater)
        st.write('Risk decrease')
        st.altair_chart(donut_chart_less)


with col[1]:
    st.markdown('#### Default risk')
    
#     choropleth = make_choropleth(df_selected_year, 'country_code', 'Overall risk factor', selected_color_theme)
#     st.plotly_chart(choropleth, use_container_width=True)

    # world_chart = make_world_chart(df_selected_year, 'country_code', 'Overall risk factor', selected_color_theme)
    # st.altair_chart(world_chart, use_container_width=True)
    
    heatmap = make_heatmap(df_reshaped, 'year', 'country_code', 'Overall risk factor', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)

with st.expander('About', expanded=True):
        st.write('''
            - Data: EWS
            - :orange[**Changes in country risk**]: difference in overall risk since last update
            - :orange[**Country risk**]: share of countries with increase/decrease in country risk
            ''')


# with col[0]:
#     st.markdown('#### Top Risk Countries')

#     st.dataframe(df_selected_year_sorted,
#                  column_order=("Countries", "Overall risk factor"),
#                  hide_index=True,
#                  width=None,
#                  column_config={
#                     "Countries": st.column_config.TextColumn(
#                         "Countries",
#                     ),
#                     "Overall risk factor": st.column_config.ProgressColumn(
#                         "Risk factor",
#                         format="%f",
#                         min_value=0,
#                         max_value=max(df_selected_year_sorted['Overall risk factor']),
#                      )}
#                  )


# with col[0]:
#     st.markdown('#### Top Risk Countries')

#     # Reshape the DataFrame to have risk factors as rows
#     df_melted = df_selected_year_sorted.melt(id_vars=["Countries"], 
#                                              value_vars=["Overall risk factor", "Fiscal risk factor", "Financial risk factor", "External risk factor"],
#                                              var_name="Risk Factor", 
#                                              value_name="Risk Score")
    
#     # Display the DataFrame
#     st.dataframe(df_melted, 
#                  width=None,
#                  height=None)

with col[0]:
    st.markdown('#### Top Risk Countries')

    st.dataframe(df_selected_year_sorted,
                 column_order=("Countries", "Overall risk factor", "Fiscal risk factor", "Financial risk factor", "External risk factor"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Countries": st.column_config.TextColumn(
                        "Countries",
                    ),
                    "Overall risk factor": st.column_config.ProgressColumn(
                        "Overall Risk",
                        format="%f",
                        min_value=0,
                        max_value=10,
                     ),
                    "Fiscal risk factor": st.column_config.ProgressColumn(
                        "Fiscal Risk",
                        format="%f",
                        min_value=0,
                        max_value=10,
                     ),
                    "Financial risk factor": st.column_config.ProgressColumn(
                        "Financial Risk",
                        format="%f",
                        min_value=0,
                        max_value=10,
                     ),
                    "External risk factor": st.column_config.ProgressColumn(
                        "External Risk",
                        format="%f",
                        min_value=0,
                        max_value=10,
                     )}
                 )
    
# with col[0]:
#     st.markdown('#### Top Risk Countries')

#     for index, row in df_selected_year_sorted.iterrows():
#         st.write(row['Countries'])
#         st.write('Overall risk factor:')
#         st.progress(row['Overall risk factor'] / 10)
#         st.write('Fiscal risk factor:')
#         st.progress(row['Fiscal risk factor'] / 10)
#         st.write('Financial risk factor:')
#         st.progress(row['Financial risk factor'] / 10)
#         st.write('External risk factor:')
#         st.progress(row['External risk factor'] / 10)
