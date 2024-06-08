import pandas as pd
import streamlit as st
import altair as alt

# Cargar el conjunto de datos
df = pd.read_csv('static/datasets/defuncion.csv')

# Crear la interfaz de usuario con Streamlit
st.title('Defunciones en el Área Metropolitana')

# Calcular la cantidad total de hombres y mujeres fallecidos
total_gender_counts = df['sexo_fallecido'].value_counts().reset_index()
total_gender_counts.columns = ['Género', 'Cantidad']

# Gráfico de barras para la cantidad total de hombres y mujeres fallecidos
st.subheader('Cantidad total de fallecidos por género')
st.write(total_gender_counts)

bar_chart_gender = alt.Chart(total_gender_counts).mark_bar().encode(
    x='Género',
    y='Cantidad',
    color='Género'
).properties(
    width=400,
    height=300
)

st.altair_chart(bar_chart_gender, use_container_width=True)

# Definir los filtros adicionales
city_options = ['Todas'] + df['municipio_residencia'].unique().tolist()
city_filter = st.selectbox("Filtrar por ciudad de fallecimiento:", city_options)

age_min = df['edad_fallecido'].min()
age_max = df['edad_fallecido'].max()
age_range = st.slider("Filtrar por rango de edad:", min_value=age_min, max_value=age_max, value=(age_min, age_max))

site_of_death_options = ['Todas'] + df['sitio_defuncion'].unique().tolist()
site_of_death_filter = st.selectbox("Filtrar por sitio de defunción:", site_of_death_options)

death_type_options = ['Todas'] + df['tipo_defuncion'].unique().tolist()
death_type_filter = st.selectbox("Filtrar por tipo de defunción:", death_type_options)

death_manner_options = ['Todas'] + df['probable_manera_muerte'].unique().tolist()
death_manner_filter = st.selectbox("Filtrar por probable manera de muerte:", death_manner_options)

# Aplicar los filtros adicionales
filtered_df = df.copy()

if city_filter != 'Todas':
    filtered_df = filtered_df[filtered_df['municipio_residencia'] == city_filter]

filtered_df = filtered_df[(filtered_df['edad_fallecido'] >= age_range[0]) & (filtered_df['edad_fallecido'] <= age_range[1])]

if site_of_death_filter != 'Todas':
    filtered_df = filtered_df[filtered_df['sitio_defuncion'] == site_of_death_filter]

if death_type_filter != 'Todas':
    filtered_df = filtered_df[filtered_df['tipo_defuncion'] == death_type_filter]

if death_manner_filter != 'Todas':
    filtered_df = filtered_df[filtered_df['probable_manera_muerte'] == death_manner_filter]

# Gráfico de barras para la cantidad de personas fallecidas por ciudad
if len(filtered_df) > 0:
    city_death_counts = filtered_df['municipio_residencia'].value_counts().reset_index()
    city_death_counts.columns = ['Ciudad', 'Cantidad de Fallecidos']
    
    # Obtener solo las primeras 5 ciudades con más fallecidos
    city_death_counts = city_death_counts.head(5)

    st.subheader('Cantidad de personas fallecidas por ciudad (Top 5)')
    st.write(city_death_counts)

    bar_chart_city = alt.Chart(city_death_counts).mark_bar().encode(
        x='Cantidad de Fallecidos',
        y=alt.Y('Ciudad', sort='-x'),
        color=alt.Color('Ciudad', legend=None)
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(bar_chart_city, use_container_width=True)
