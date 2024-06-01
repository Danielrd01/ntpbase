import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
# Set the page title and header
st.title("Simulador CESDE Bello")

df = pd.read_csv('datasets\cesde.csv')

gruposU = sorted(df['GRUPO'].unique())
nivelesU = sorted(df['NIVEL'].unique())
jornadasU =  sorted(df['JORNADA'].unique())
horarioU =  sorted(df['HORARIO'].unique())
submodulosU =  sorted(df['SUBMODULO'].unique())
docentesU =  sorted(df['DOCENTE'].unique())
momentosU =  sorted(df['MOMENTO'].unique())

# -----------------------------------------------------------------------------------
def filtro1():    
    col1, col2 = st.columns(2)
    with col1:
        grupo = st.selectbox("Grupo",gruposU)
    with col2:
        momento = st.selectbox("Momento",momentosU)
    resultado = df[(df['GRUPO']==grupo)&(df['MOMENTO']==momento)]
   
    resultado= resultado.reset_index(drop=True) 
    # Grafico de barras
    estudiante=resultado['NOMBRE']
    fig = go.Figure(data=[
        go.Bar(name='CONOCIMIENTO', x=estudiante, y=resultado['CONOCIMIENTO']),
        go.Bar(name='DESEMPEÑO', x=estudiante, y=resultado['DESEMPEÑO']),
        go.Bar(name='PRODUCTO', x=estudiante, y=resultado['PRODUCTO'])
    ])   
    fig.update_layout(barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    # Tabla
    st.table(resultado[["NOMBRE","CONOCIMIENTO","DESEMPEÑO","PRODUCTO"]])
    
# -----------------------------------------------------------------------------------
def filtro2():
    col1, col2, col3 = st.columns(3)
    with col1:
        grupo = st.selectbox("Grupo",gruposU)
    with col2:
        nombres = df[df['GRUPO']==grupo]
        nombre = st.selectbox("Estudiante",nombres["NOMBRE"])
    with col3:
        momentosU.append("Todos")
        momento = st.selectbox("Momento",momentosU)   

    if momento == "Todos":
        resultado = df[(df['GRUPO']==grupo)&(df['NOMBRE']==nombre)]
        # Grafico de barras
        momentos=sorted(df['MOMENTO'].unique())
        fig = go.Figure(data=[
            go.Bar(name='CONOCIMIENTO', x=momentos, y=resultado['CONOCIMIENTO']),
            go.Bar(name='DESEMPEÑO', x=momentos, y=resultado['DESEMPEÑO']),
            go.Bar(name='PRODUCTO', x=momentos, y=resultado['PRODUCTO'])
        ])   
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)

        resultado= resultado.reset_index(drop=True) 
        m1 = resultado.loc[0,['CONOCIMIENTO','DESEMPEÑO','PRODUCTO']]
        m2 = resultado.loc[1,['CONOCIMIENTO','DESEMPEÑO','PRODUCTO']]
        m3 = resultado.loc[2,['CONOCIMIENTO','DESEMPEÑO','PRODUCTO']]
        tm = pd.Series([m1.mean(),m2.mean(),m3.mean()])       
        st.subheader("Promedio")
        st.subheader(round(tm.mean(),1)) 
    else :   
        resultado = df[(df['GRUPO']==grupo)&(df['MOMENTO']==momento)&(df['NOMBRE']==nombre)]
        # Grafico de barras
        estudiante=resultado['NOMBRE']
        fig = go.Figure(data=[
            go.Bar(name='CONOCIMIENTO', x=estudiante, y=resultado['CONOCIMIENTO']),
            go.Bar(name='DESEMPEÑO', x=estudiante, y=resultado['DESEMPEÑO']),
            go.Bar(name='PRODUCTO', x=estudiante, y=resultado['PRODUCTO'])
        ])   
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)

        resultado= resultado.reset_index(drop=True) 
        conocimiento = resultado.loc[0,['CONOCIMIENTO','DESEMPEÑO','PRODUCTO']]
        st.subheader("Promedio")
        st.subheader(round(conocimiento.mean(),1)) 
  
# -----------------------------------------------------------------------------------
filtros =[
    "Notas por grupo",
    "Notas por estudiante"
]

filtro = st.selectbox("Filtros",filtros)

if filtro:
    filtro_index = filtros.index(filtro)

    if filtro_index == 0:
        filtro1()
    elif filtro_index == 1:
        filtro2()
