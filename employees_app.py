import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
#Title for the app
st.title('Análisis de deserción de empleados: Ejercicio de aprendizaje')

data_url='https://raw.githubusercontent.com/raciv65/Modulo_5_Tec/main/Employees.csv' 
#Funtion
@st.cache
def load_data(nrows):
  #Return data without NAN values, also the size of the actual data and the size pre-drop NAN values
  data = pd.read_csv(data_url)
  data = data.head(nrows)
  data_len_before = len(data)
  data.dropna(inplace = True)
  data_len_after =len(data)
  return data, data_len_before, data_len_after

@st.cache
def variable_selected():
  employee = [id_employee for id_employee in employees['Employee_ID']]
  hometown = [home for home in employees['Hometown'].unique()]
  unit = [unit_for_select for unit_for_select in employees['Unit'].unique() ]
  return employee, hometown, unit


sidebar = st.sidebar
sidebar.header('Datos de empleados')
sidebar.write('En esta parte puedes seleccionar los registros disponinles del conjunto de datos de empleados.')
nrows = sidebar.number_input('Número de registros para mostrar.', min_value=1, max_value=7000, value=500)
  #Get the data
employees, before_NAN, after_NAN = load_data(nrows)
sidebar.text(f'Se carga la información de {after_NAN} sin datos nulos de los {before_NAN} seleccionados.')

#Option menu
selected = option_menu(None, ["Resumen", "Gráficas",  "Análisis"], 
    icons=['file-text-fill','bar-chart-fill','gear-fill'],
    menu_icon='cast',
    default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "red"},
    }
)



if selected == 'Resumen':
  st.header('Resumen')


#Summary of the app
  st.text('''
El presente documento tiene como objetivo integrar los diferentes conocimientos 
adquiridos en módulos previos. Para ello en el presente se realizará un análisis
 exploratorio de los datos, obtener medidas estadísticas descriptivas y visualizar
información relevante en gráficas independientes, suerpuestas y conjuntas.
En particular, con los datos de Hackathon HackerEarth 2020,
respecto a la deserción laboral los cuales se muestran en el siguiente sitio.''')




  if sidebar.checkbox('Mostrar la tabla de conjunto de datos completos', value =True):
    st.write('Tabla con los datos completos')
    st.dataframe(employees)


  sidebar.subheader('Criterios de selección')

  employee, hometown, unit = variable_selected()

  search_selected = sidebar.selectbox('¿Cómo te gustaría seleccionar y filtrar la información?',('Escribir parte del ID del empleado','Por ciudad','Por área de empleado'))
  with st.form('Selected values'):
    if search_selected == 'Por ciudad':
      hometown_selected = sidebar.multiselect('Selecciona la ciudad o ciudades', options = hometown, default = hometown)
      employees_selected = employees.loc[employees['Hometown'].isin(hometown_selected)]
    if search_selected == 'Por área de empleado':
      unit_selected =sidebar.multiselect('Selecciona el área o áreas de los empleados:', options = unit, default = unit)
      employees_selected = employees.loc[employees['Unit'].isin(unit_selected)]
    if search_selected == 'Escribir parte del ID del empleado':
      employee_id_input =sidebar.text_input('Escribe parte del ID empleado:', value ='0')
      employees_selected = employees.loc[employees['Employee_ID'].str.contains(employee_id_input)]
      levels = [level for level in employees_selected['Education_Level'].unique()]
      level_selected = sidebar.multiselect('Selecciona nivel educativo', options =levels, default =levels)
      if level_selected:
        employees_selected = employees_selected.loc[employees['Education_Level'].isin(level_selected)]


  if sidebar.checkbox(f'Mostrar la tabla con los {len(employees_selected)} empleados selecionados', value=True):
    st.write(f'Tabla sólo con los datos seleccionados: se muestran {len(employees_selected)} registros')
    st.dataframe(employees_selected)

if selected == 'Gráficas':

  st.header('Gráficas')
  st.write('En esta sección se muestran gráficas relacionadas a los datos de decersión de los empleados')

  st.subheader('Histograma por edad')
  fig_histogram = px.histogram(employees, x='Age', nbins=10, text_auto = True)
  fig_histogram.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

  st.plotly_chart(fig_histogram)

  st.subheader('Gráfica de frecuencia en en las unidades funcionales')
  fig_frequencies = px.bar(employees['Unit'].value_counts(), x='Unit', text_auto = True)
  fig_frequencies.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

  st.plotly_chart(fig_frequencies)


if selected == 'Análisis':
    st.header('Análisis')
    st.write('En esta sección se muestran el valor de la deserción por ciudad y las correlaciones que hay entre la deserción de los empleados')


    st.subheader('Deserción por ciudad')
    
    fig_by_hometown = px.bar(employees.groupby('Hometown').mean(), y='Attrition_rate', text_auto = True)
    fig_by_hometown.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    st.plotly_chart(fig_by_hometown)

    st.subheader('Deserción por edad')

    fig_by_age = px.scatter(employees, x='Age', y='Attrition_rate')
    st.plotly_chart(fig_by_age)

    st.subheader('Deserción por tiempo de servicio')

    fig_by_time_of_service = px.scatter(employees, x='Time_of_service', y='Attrition_rate')
    st.plotly_chart(fig_by_time_of_service)













