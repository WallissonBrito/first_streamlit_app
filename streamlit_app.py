import streamlit as st
import pandas as pd

st.title("My Parents New Healthy Dinner")
st.header("Breakfast Favorite")
st.caption("Omega 3 & Blueberry Oatmeal")
st.caption("Kale, Spinach & Rocket Smoothie")
st.caption("Hard-Boiled Free-Range Egg")

# Display the table on the page.
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)



