import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd
from datetime import date, timedelta

def run():
    st.set_page_config(
        page_title="Home Page",
    )

    st.write("# Selamat datang di Dashboard Lapangbola! 👋")

    st.markdown(
        """
        Dashboard ini dibuat oleh **Prana dari R&D Lapangbola** untuk mempermudah akses 
        data-data yang telah diolah baik untuk konten maupun laporan ke LIB serta 
        dapat dipergunakan untuk plotting (xG map, passing network, dll).
        **👈 Pilih fitur pada sidebar** untuk melihat dan 
        menggunakan fitur-fitur dashboard ini.

        ### Fitur:
        - **Match Center**: Berisi statistik dan visualisasi data seluruh pertandingan Liga 1 (Liga 2 menyusul).
        - **Season Statistics**: Berisi milestones tim di Liga 1 serta statistik tim dan pemain di musim ini.
        - **Team Detailed**: Berisi statistik dan visualisasi data tim secara lebih detail.
        - **Player Detailed**: Berisi statistik dan visualisasi data pemain secara lebih detail.
        - **Player Search**: Untuk membuat list pemain terbaik sesuai kriteria yang dibutuhkan.
        - **Plotting xG**: Untuk plotting xG map dan assist/key pass map.
        - **Plotting Passing Network**: Untuk plotting passing network.
        - **Excel-to-XML Converter**: Untuk mengkonversi file timeline (.xlsx) ke format XML untuk video tagging.
        - ***Coming Soon***
        
        ### Terima kasih kepada:
        - Kang Dani dan Dzikry,
        - Tim Operasional,
        - Tim Konten,
        - Serta seluruh elemen Lapangbola.
    """
    )


if __name__ == "__main__":
    run()

st.markdown('### User counter:')

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="mytable", ttl="10m").execute()
df = pd.DataFrame(rows.data)
df = df[(df['name']!='admin') & (df['name']!='email') & (df['name']!='Prana')].reset_index(drop=True)

df['tanggal'] = pd.to_datetime(df['tanggal'])
df['waktu'] = pd.to_datetime(df['waktu'])

temp = df[['tanggal','name']].rename(columns={'tanggal':'date','name':'access count'})
temp['date'] = temp['date'].dt.strftime('%d/%m/%Y')
temp = temp.groupby(['date'], as_index=False).count()
st.bar_chart(temp, x="date", y="access count")

us = df['name'][len(df)-1]
tg = str((df['tanggal'][len(df)-1]).strftime("%d/%m/%Y"))
wts = (df['waktu'][len(df)-1])
jkt = wts + timedelta(hours=7)
wt = str(jkt.strftime("%X"))

st.write('Last accessed by '+us+' on '+tg+' at '+wt+' WIB')

from menu import menu
menu()
