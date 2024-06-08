import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos
df = pd.read_csv('static/datasets/cuentas_similares_netflix.csv')

# Título de la página
st.title("Cuentas Clientes Replay")

# Agregar un filtro para el tipo de dispositivo preferido
dispositivos_preferidos = ['Todos'] + list(df['Dispositivo_Preferido'].unique())
filtro_dispositivo = st.selectbox("Selecciona un tipo de dispositivo preferido", dispositivos_preferidos)

# Agregar un filtro para la fecha de ingreso
fecha_min = pd.to_datetime(df['Fecha_Ingreso']).min().date()
fecha_max = pd.to_datetime(df['Fecha_Ingreso']).max().date()
fecha_inicio = st.date_input("Selecciona la fecha de inicio", fecha_min)
fecha_fin = st.date_input("Selecciona la fecha de fin", fecha_max)

# Agregar un filtro para el estado de pago
estado_pago = st.selectbox("Selecciona el estado de pago", ["Todos", "Ha pagado", "No ha pagado"])

# Agregar un filtro para seleccionar cliente por cliente
clientes = df['Correo'].unique()
filtro_cliente = st.selectbox("Selecciona un cliente", ["Todos"] + list(clientes))

# Calcular las cantidades exactas de cada dispositivo
cantidades_dispositivos = df.groupby('Dispositivo_Preferido').size().reset_index()
cantidades_dispositivos.columns = ['Dispositivo_Preferido', 'Cantidad']

# Actualizar el filtro de dispositivos para mostrar las cantidades exactas
if filtro_dispositivo == 'Todos':
    filtro_dispositivo_label = 'Todos'
else:
    cantidad_seleccionada = cantidades_dispositivos[cantidades_dispositivos['Dispositivo_Preferido'] == filtro_dispositivo]['Cantidad'].values[0]
    filtro_dispositivo_label = f"{filtro_dispositivo} ({cantidad_seleccionada})"

# Filtrar los datos por el tipo de dispositivo preferido y el rango de fechas seleccionado
if filtro_dispositivo != "Todos":
    df_filtrado = df[df['Dispositivo_Preferido'] == filtro_dispositivo]
else:
    df_filtrado = df

# Aplicar los demás filtros
df_filtrado = df_filtrado[(pd.to_datetime(df_filtrado['Fecha_Ingreso']).dt.date >= fecha_inicio) & 
                          (pd.to_datetime(df_filtrado['Fecha_Ingreso']).dt.date <= fecha_fin)]

if estado_pago == "Ha pagado":
    df_filtrado = df_filtrado[df_filtrado['Fecha_Pago'] != 'No ha pagado']
elif estado_pago == "No ha pagado":
    df_filtrado = df_filtrado[df_filtrado['Fecha_Pago'] == 'No ha pagado']

if filtro_cliente != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Correo'] == filtro_cliente]

# Mostrar los datos filtrados en una tabla
st.write("### Datos filtrados:")
st.dataframe(df_filtrado)

# Crear un gráfico de barras que muestre la cantidad de personas que usan cada tipo de dispositivo
fig = px.bar(cantidades_dispositivos, x='Dispositivo_Preferido', y='Cantidad', 
             title='Cantidad de personas por tipo de dispositivo preferido', 
             color='Dispositivo_Preferido', color_discrete_map={'Smart TV': 'blue', 'Tablet': 'green', 'Computadora': 'orange', 'Smartphone': 'red'})

# Mostrar las cantidades exactas en las barras
for i in range(len(cantidades_dispositivos)):
    fig.add_annotation(x=cantidades_dispositivos['Dispositivo_Preferido'][i], 
                       y=cantidades_dispositivos['Cantidad'][i], 
                       text=str(cantidades_dispositivos['Cantidad'][i]), 
                       font=dict(color='black', size=12),
                       showarrow=False)

st.plotly_chart(fig)
