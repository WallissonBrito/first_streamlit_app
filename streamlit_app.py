import streamlit 
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


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

#  Função fruta escolhida
def get_fruityvice_data(this_fruit_choice):
  # Request da api
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  #Normalizando dados 
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# Nova seção para mostrar fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  # Input da fruta para obter informações
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")

  else:    
    back_from_function = get_fruityvice_data(fruit_choice)
    # Mostrar dados em formato de tabela
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()
  
#  Não executa nada após aqui 
streamlit.stop()

#  Conexão com snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

#  Comando query para seleção 
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()

#  Exibir lista de frutas
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# Inserir fruta na lista
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")





