"""Where we try out Streamlit and we get familiar with some of its functions. To see the end result, 
in terminal run: streamlit run your_script.py """

import streamlit as st
import pandas as pd


# With st.write, you can write just about anything to the app: text, data, Matplotlib figures, Altair charts and more

st.write("Hello, Streamlit! This is a simple app to demonstrate some of its features.")

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df      # writing a variable on a separate line, automatically displays it on the app!


