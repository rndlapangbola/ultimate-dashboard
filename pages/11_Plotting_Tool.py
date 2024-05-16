import sys
import pandas as pd
import numpy as np
import streamlit as st
import io

st.set_page_config(page_title='Plotting Tool', layout='wide')
st.markdown('# Plotting Tool')

from menu import menu
menu()
