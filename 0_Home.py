import streamlit as st

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
