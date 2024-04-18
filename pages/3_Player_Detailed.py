import sys
import io
import streamlit as st
import pandas as pd
import numpy as np
from tempfile import NamedTemporaryFile
import urllib

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.patches as patches
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch

from fungsiplot import beli_pizza
from fungsiplot import plot_compare

from listfungsi import data_team
from listfungsi import data_player
from listfungsi import get_list
from listfungsi import get_detail
from listfungsi import get_radar
from listfungsi import get_simi

st.set_page_config(page_title='Team Detailed', layout='wide')
st.markdown('# Team Detailed')

@st.cache_data(ttl=600)
def load_data(sheets_url):
    xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
    return pd.read_excel(xlsx_url)

df1 = load_data(st.secrets["datateam"])
df2 = load_data(st.secrets["datapemain"])
th = load_data(st.secrets["th"])
cf = load_data(st.secrets["cf"])
cd = load_data(st.secrets["cd"])

from datetime import date
df1['Date'] = pd.to_datetime(df1.Date)
df1['Month'] = df1['Date'].dt.strftime('%B')
df22 = get_detail(df2)
df = pd.merge(df1, df2.drop(['Name'], axis=1), on='Player ID', how='left')
fulldata = get_detail(df)
mlist = get_list(fulldata)
