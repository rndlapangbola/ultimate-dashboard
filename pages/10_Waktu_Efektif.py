import sys
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patheffects as path_effects
from highlight_text import HighlightText, ax_text, fig_text
from PIL import Image
from tempfile import NamedTemporaryFile
import urllib
import os
from textwrap import wrap # countries name lisibility

github_url = 'https://github.com/google/fonts/blob/main/ofl/poppins/Poppins-Bold.ttf'
url = github_url + '?raw=true'

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

bold = fm.FontProperties(fname=f.name)

github_url = 'https://github.com/google/fonts/blob/main/ofl/poppins/Poppins-Regular.ttf'
url = github_url + '?raw=true'

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

reg = fm.FontProperties(fname=f.name)

github_url = 'https://github.com/google/fonts/blob/main/ofl/poppins/Poppins-Italic.ttf'
url = github_url + '?raw=true'

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

ita = fm.FontProperties(fname=f.name)

path_eff = [path_effects.Stroke(linewidth=2, foreground='#ffffff'),
            path_effects.Normal()]

st.set_page_config(page_title='Waktu Efektif', layout='centered')
st.markdown('# Waktu Efektif')

from menu import menu
menu()

sys.path.append("listfungsi.py")
import listfungsi
from listfungsi import wefektif
from listfungsi import genmomentum

col1, col2 = st.columns(2)
with col1:
    tl_data_1 = st.file_uploader("Upload file timeline excel babak pertama!", key=2)
    try:
        d1 = pd.read_excel(tl_data_1, skiprows=[0])
        mtch = d1['Match'].unique().tolist()[0]
    except ValueError:
        st.error("Please upload the timeline file")

with col2:
    tl_data_2 = st.file_uploader("Upload file timeline excel babak kedua!", key=3)
    try:
        d2 = pd.read_excel(tl_data_2, skiprows=[0])
    except ValueError:
        st.error("Please upload the timeline file")

for idx, i in enumerate([d1, d2]):
  if idx == 0:
    b1 = wefektif(i)[0].rename(columns={'Time':'First Half'})
    s1 = wefektif(i)[1]
  else:
    b2 = wefektif(i)[0].rename(columns={'Time':'Second Half'})
    s2 = wefektif(i)[1]
b = pd.merge(b1, b2, on='Team')
b['Total'] = b['First Half'] + b['Second Half']
col = ['First Half', 'Second Half', 'Total']
for c in col:
  b[c] = pd.to_datetime(b[c], unit='s').dt.strftime('%H:%M:%S')
st.write(b)

col1, col2 = st.columns(2)
with col1:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        s1.to_excel(writer, sheet_name='Sheet1', index=False)
    download = st.download_button(
        label="Download Sequences Babak I",
        data=buffer.getvalue(),
        file_name='sequences-1.xlsx',
        mime='application/vnd.ms-excel',
        key = 0)
with col2:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        s2.to_excel(writer, sheet_name='Sheet1', index=False)
    download = st.download_button(
        label="Download Sequences Babak II",
        data=buffer.getvalue(),
        file_name='sequences-2.xlsx',
        mime='application/vnd.ms-excel',
        key = 1)

mm = genmomentum(d1, d2)
st.pyplot(mm)
with open('pnet.jpg', 'rb') as img:
    fn = 'Match Momentum '+mtch+'.jpg'
    btn = st.download_button(label="Download Match Momentum", data=img, file_name=fn, mime="image/jpg")
#if 'coor' not in st.session_state:
#    st.session_state['coor'] = []

#xval = 617.6470588235249
#yval = 400

#value = streamlit_image_coordinates('./data/Lapangkosong.jpg', width=xval, height=yval, key="local",)

#if value is not None:
#  coor = value['x'], value['y']
#  if coor not in st.session_state['coor']:
#    st.session_state['coor'].append(coor)
#    st.experimental_rerun()
#df = pd.DataFrame(st.session_state['coor'])
#df = df.rename(columns={df.columns[0]:'X',df.columns[1]:'Y'})
#df['X'] = (df['X']*100)/xval
#df['Y'] = df['Y']/4
#edited_df = st.data_editor(df, num_rows="dynamic")
