import streamlit as st
import pandas as pd
import requests 
import snowflake.connector

#  Conector snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()

st.title("My Parents New Healthy Dinner")
st.header("Breakfast Favorite")
st.caption("Omega 3 & Blueberry Oatmeal")
st.caption("Kale, Spinach & Rocket Smoothie")
st.caption("Hard-Boiled Free-Range Egg")

# Mostra tabela na página
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Lista de frutas selecionadas
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
Fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(Fruits_to_show)

# Nova seção para mostrar fruityvice api response
st.header("Fruityvice Fruit Advice!")

# Input da fruta para obter informações
fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)

# Request da api
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#Normalizando dados 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# Mostrar dados em formato de tabela
st.dataframe(fruityvice_normalized)

#  Texto conector snowflake
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)



