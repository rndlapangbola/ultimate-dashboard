import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import pandas as pd

st.set_page_config(page_title='Event Tagger', layout='wide')
st.markdown('# Event Tagger')

from menu import menu
menu()

if 'coor' not in st.session_state:
    st.session_state['coor'] = []

xval = 617.6470588235249
yval = 400

value = streamlit_image_coordinates('./data/lapangkosong4.jpg', width=xval, height=yval, key="local",)

if value is not None:
  coor = value['x'], value['y']
  if coor not in st.session_state['coor']:
    st.session_state['coor'].append(coor)
    st.experimental_rerun()
df = pd.DataFrame(st.session_state['coor'])
df = df.rename(columns={df.columns[0]:'X',df.columns[1]:'Y'})
df['X'] = (df['X']*100)/xval
df['Y'] = df['Y']/4
edited_df = st.data_editor(df, num_rows="dynamic")
