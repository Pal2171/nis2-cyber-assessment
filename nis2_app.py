import streamlit as st
import pandas as pd

# Carica i dati dal file Excel
@st.cache_data
def load_data():
    file_path = "NIS2-Cyber-Assessment.xlsx"  # Assicurati che il file sia nello stesso folder
    data_test = pd.read_excel(file_path, sheet_name="NIS2 Cyber Test")
    data_analysis = pd.read_excel(file_path, sheet_name="DataAnalysis")
    dashboard = pd.read_excel(file_path, sheet_name="Dashboard")
    return data_test, data_analysis, dashboard


# Carica i dati
data_test, data_analysis, dashboard = load_data()

# Configurazione dell'app
st.title("NIS2 Cyber Assessment Tool")
st.sidebar.title("Navigazione")
page = st.sidebar.radio("Seleziona una pagina", ["Input", "Analisi", "Dashboard"])

if page == "Input":
    st.header("Input Dati Aziendali")
    nome_azienda = st.text_input("Nome Azienda")
    partita_iva = st.text_input("Partita IVA")
    settore = st.text_input("Settore Merceologico/ATECO")
    referente = st.text_input("Referente Aziendale")
    fatturato = st.number_input("Fatturato (€)", min_value=0.0, step=1000.0)
    dipendenti = st.number_input("Numero di Dipendenti", min_value=0, step=1)
    commerciale = st.text_input("Commerciale")

    if st.button("Salva Dati"):
        st.success("Dati salvati con successo!")
        st.write({
            "Nome Azienda": nome_azienda,
            "Partita IVA": partita_iva,
            "Settore": settore,
            "Referente": referente,
            "Fatturato": fatturato,
            "Dipendenti": dipendenti,
            "Commerciale": commerciale,
        })

elif page == "Analisi":
    st.header("Analisi dei Dati")
    st.write("Ecco un'anteprima dei dati di analisi:")
    st.dataframe(data_analysis)

elif page == "Dashboard":
    st.header("Dashboard dei Risultati")
    st.write("Ecco un'anteprima della dashboard:")
    st.dataframe(dashboard)
    st.bar_chart(dashboard["Punteggio di compliance"])  # Adatta il nome della colonna ai dati reali
