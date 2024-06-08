import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurar la página en modo ancho
st.set_page_config(layout="wide")

# Cargar los datos
df = pd.read_csv('static/datasets/cuentas_similares_netflix.csv')  # Reemplaza 'ruta/al/archivo/dataset.csv' con la ruta real del archivo CSV

# Título de la página
st.title("Análisis de Defunciones en un Hospital")

# Filtros temporales
st.sidebar.header("Filtros Temporales")
ano = st.sidebar.selectbox("Selecciona el Año", sorted(df['ano'].unique()))
trimestre = st.sidebar.selectbox("Selecciona el Trimestre", sorted(df['trimestre'].unique()))
fecha_inicio = st.sidebar.date_input("Selecciona la Fecha de Inicio")
fecha_fin = st.sidebar.date_input("Selecciona la Fecha de Fin")

# Filtros demográficos
st.sidebar.header("Filtros Demográficos")
sexo = st.sidebar.selectbox("Selecciona el Sexo", ['Todos'] + sorted(df['sexo_fallecido'].unique()))
estado_conyugal = st.sidebar.selectbox("Selecciona el Estado Conyugal", ['Todos'] + sorted(df['estado_conyugal_fallecido'].unique()))

# Filtros de causa de muerte
st.sidebar.header("Filtros de Causa de Muerte")
tipo_defuncion = st.sidebar.selectbox("Selecciona el Tipo de Defunción", ['Todos'] + sorted(df['tipo_defuncion'].unique()))
probable_manera_muerte = st.sidebar.selectbox("Selecciona la Probable Manera de Muerte", ['Todos'] + sorted(df['probable_manera_muerte'].unique()))

# Convertir 'fecha_defuncion' a objetos de fecha
df['fecha_defuncion'] = pd.to_datetime(df['fecha_defuncion']).dt.date

# Aplicar filtros
df_filtered = df[(df['ano'] == ano) & 
                 (df['trimestre'] == trimestre) & 
                 (pd.to_datetime(df['fecha_defuncion']) >= fecha_inicio) & 
                 (pd.to_datetime(df['fecha_defuncion']) <= fecha_fin)]

if sexo != 'Todos':
    df_filtered = df_filtered[df_filtered['sexo_fallecido'] == sexo]

if estado_conyugal != 'Todos':
    df_filtered = df_filtered[df_filtered['estado_conyugal_fallecido'] == estado_conyugal]

if tipo_defuncion != 'Todos':
    df_filtered = df_filtered[df_filtered['tipo_defuncion'] == tipo_defuncion]

if probable_manera_muerte != 'Todos':
    df_filtered = df_filtered[df_filtered['probable_manera_muerte'] == probable_manera_muerte]

# Mostrar los datos filtrados
st.subheader("Datos Filtrados")
st.write(df_filtered)

# Visualización básica
st.subheader("Visualización Básica")

# Gráfico de barras de cantidad de defunciones por trimestre
df_trimestre_count = df_filtered.groupby('trimestre').size().reset_index(name='count')
st.bar_chart(df_trimestre_count.set_index('trimestre'))

# Gráfico de pastel de tipo de defunción
df_tipo_defuncion_count = df_filtered.groupby('tipo_defuncion').size().reset_index(name='count')
fig = go.Figure(data=[go.Pie(labels=df_tipo_defuncion_count['tipo_defuncion'], values=df_tipo_defuncion_count['count'])])
st.plotly_chart(fig)
