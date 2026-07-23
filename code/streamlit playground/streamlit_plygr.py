""" Where we try out Streamlit and we get familiar with some of its functions. To see the end result, 
in terminal run: streamlit run your_script.py """

import streamlit as st
import pandas as pd
import numpy as np


# With st.write, you can write just about anything to the app: text, data, Matplotlib figures, Altair charts and more
st.title('Playing around with Streamlit functions')
st.write("Hello, Streamlit! This is a simple app to demonstrate some features (looks like magic!)")

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

st.write("Here's a first attempt at using data to create a table:")


df      # writing a variable on a separate line, automatically displays it on the app!


# If we want to display a STATIC TABLE  though, we can use st.table() instead of st.write(), the same is true for st.dataframe():
st.write("The same table, but STATIC:")
st.table(df)


# It also has a wide set of functions to display charts, which we won't need, and widgets! Like buttons, select boxes, sliders, etc. 
st.write("Here's a slider widget, not useful for us, but how cool is it??")
x = st.slider('x')  
st.write(x, 'squared is', x * x)

option = st.selectbox(
    'Which week would you like to see?',
     df['first column'])

st.write('You selected: ', option, 'which corresponds to the value', df['second column'][option-1])


if st.checkbox('Person 1'):
  st.write('Person 1 is selected!')
if st.checkbox('Person 2'):
  st.write('Person 2 is selected!')

# We can put the parameters in the sidebar, make it cleaner, for example:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)
add_input_number = st.sidebar.number_input('Insert the number of people working this month', min_value=1, max_value=10, value=1, step=1)


left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")