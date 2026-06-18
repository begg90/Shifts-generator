"""Where we try out Streamlit and we get familiar with some of its functions. To see the end result, 
in terminal run: streamlit run your_script.py """

import streamlit as st
import pandas as pd

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df

# writing a variable, automatically displays it on the app! It's almost magic XD
