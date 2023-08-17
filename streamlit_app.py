import streamlit 
import pandas as pd
import requests 
import snowflake.connector

streamlit.title("My Parents New Healthy Dinner")
streamlit.header("Breakfast Favorite")
streamlit.caption("Omega 3 & Blueberry Oatmeal")
streamlit.caption("Kale, Spinach & Rocket Smoothie")
streamlit.caption("Hard-Boiled Free-Range Egg")

# Mostra tabela na página
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Lista de frutas selecionadas
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
Fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(Fruits_to_show)

# Nova seção para mostrar fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

# Input da fruta para obter informações
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# Request da api
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#Normalizando dados 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# Mostrar dados em formato de tabela
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
minha_cur = minha_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Olá do floco de neve:")
streamlit.text(my_data_row)



