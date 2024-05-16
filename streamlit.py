import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px


st.set_page_config(
    page_title="EWS Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# https://blog.streamlit.io/crafting-a-dashboard-app-in-python-using-streamlit/
data = {
    'Countries': ['Ghana', 'Senegal', 'India', 'Indonesia', 'Turkiye','Ghana', 'Senegal', 'India', 'Indonesia', 'Turkiye'],
    'country_code': ['GHA', 'SEN', 'IND', 'IDN', 'TUR','GHA', 'SEN', 'IND', 'IDN', 'TUR'],
    'id': [1, 2, 4, 5, 6,1, 2, 4, 5, 6],
    'year': [2024, 2024, 2024, 2024, 2024,2023, 2023, 2023, 2023, 2023],
    'risk factor': [7.3, 9.2, 2.4, 5.4, 8.3,6.3, 5.2, 6.4, 3.4, 6.3]
}

df_reshaped = pd.DataFrame(data)

with st.sidebar:
    st.title('🏂 EWS Dashboard')
    
    year_list = list(df_reshaped.year.unique())[::-1]
    
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="risk factor", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="ISO-3",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(df_selected_year['risk factor'])),
                               scope="world",
                               labels={'risk factor':'Risk Factor'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth

def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['risk_difference'] = selected_year_data['risk factor'].sub(previous_year_data['risk factor'], fill_value=0)
  return pd.concat([selected_year_data.Countries, selected_year_data.id, selected_year_data['risk factor'], selected_year_data.risk_difference], axis=1).sort_values(by="risk_difference", ascending=False)

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

col = st.columns((1.5, 4.5, 2), gap='medium')


with col[0]:
    st.markdown('#### Changes in country risk')

    df_risk_difference_sorted = calculate_population_difference(df_reshaped, selected_year)

    if selected_year > 2010:
        first_country_name = df_risk_difference_sorted.Countries.iloc[0]
        first_country_risk = format_number(df_risk_difference_sorted['risk factor'].iloc[0])
        first_country_delta = format_number(df_risk_difference_sorted.risk_difference.iloc[0])
    else:
        first_country_name = '-'
        first_country_risk = '-'
        first_country_delta = ''
    st.metric(label=first_country_name, value=first_country_risk, delta=first_country_delta)

    if selected_year > 2010:
        last_country_name = df_risk_difference_sorted.Countries.iloc[-1]
        last_country_risk = format_number(df_risk_difference_sorted['risk factor'].iloc[-1])   
        last_country_delta = format_number(df_risk_difference_sorted.risk_difference.iloc[-1])   
    else:
        last_country_name = '-'
        last_country_risk = '-'
        last_country_delta = ''
    st.metric(label=last_country_name, value=last_country_risk, delta=last_country_delta)

    
    st.markdown('#### Country risk')

    if selected_year > 2010:
        # Filter states with population difference > 50000
        # df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference_absolute > 50000]
        df_greater_1 = df_risk_difference_sorted[df_risk_difference_sorted.risk_difference > 1]
        df_less_1 = df_risk_difference_sorted[df_risk_difference_sorted.risk_difference < -1]
        
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
    
    choropleth = make_choropleth(df_selected_year, 'country_code', 'risk factor', selected_color_theme)
    st.plotly_chart(choropleth, use_container_width=True)
    
#     heatmap = make_heatmap(df_reshaped, 'year', 'country_code', 'risk factor', selected_color_theme)
#     st.altair_chart(heatmap, use_container_width=True)


with col[2]:
    st.markdown('#### Top Risk Countries')

    st.dataframe(df_selected_year_sorted,
                 column_order=("Countries", "risk factor"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Countries": st.column_config.TextColumn(
                        "Countries",
                    ),
                    "risk factor": st.column_config.ProgressColumn(
                        "Risk factor",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_year_sorted['risk factor']),
                     )}
                 )
    
    with st.expander('About', expanded=True):
        st.write('''
            - Data: [U.S. Census Bureau](<https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html>).
            - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
            - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
            ''')