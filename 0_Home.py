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
        ### Terima kasih kepada:
        - Kang Dani dan Dzikry,
        - Tim Operasional,
        - Tim Konten,
        - Serta seluruh elemen Lapangbola.
    """
    )


if __name__ == "__main__":
    run()
