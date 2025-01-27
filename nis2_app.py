import streamlit as st
import pandas as pd
from lxml import etree  # Per gestire i file XBRL

# Funzione per caricare i dati da un file Excel
@st.cache_data
def load_data():
    file_path = "NIS2-Cyber-Assessment.xlsx"  # Assicurati che il file Excel sia nello stesso folder
    data_test = pd.read_excel(file_path, sheet_name="NIS2 Cyber Test")
    data_analysis = pd.read_excel(file_path, sheet_name="DataAnalysis")
    dashboard = pd.read_excel(file_path, sheet_name="Dashboard")
    return data_test, data_analysis, dashboard

# Funzione per estrarre i dati da un file XBRL
def parse_xbrl(file):
    """Estrai dati principali da un file XBRL."""
    tree = etree.parse(file)
    root = tree.getroot()

    # Namespace XBRL
    ns = {
        "xbrli": "http://www.xbrl.org/2003/instance",
        "itcc-ci": "http://www.infocamere.it/itnn/fr/itcc/ci/2014-11-17",
    }

    # Estrai informazioni principali
    nome_azienda = root.find(".//itcc-ci:DatiAnagraficiDenominazione", ns)
    partita_iva = root.find(".//itcc-ci:DatiAnagraficiPartitaIva", ns)
    fatturato = root.find(".//itcc-ci:ValoreProduzioneRicaviVenditePrestazioni", ns)

    # Ritorna un dizionario con i dati
    return {
        "nome_azienda": nome_azienda.text if nome_azienda is not None else "Non disponibile",
        "partita_iva": partita_iva.text if partita_iva is not None else "Non disponibile",
        "fatturato": fatturato.text if fatturato is not None else "Non disponibile",
    }

# Carica i dati Excel
data_test, data_analysis, dashboard = load_data()

# Configurazione dell'app
st.title("NIS2 Cyber Assessment Tool")
st.sidebar.title("Navigazione")
page = st.sidebar.radio("Seleziona una pagina", ["Input", "Analisi", "Dashboard"])

if page == "Input":
    st.header("Input Dati Aziendali")
    partita_iva = st.text_input("Partita IVA")
    file_xbrl = st.file_uploader("Carica il file XBRL", type=["xml", "txt"])

    if file_xbrl and st.button("Estrarre Dati"):
        try:
            dati_azienda = parse_xbrl(file_xbrl)
            st.success("Dati estratti con successo!")
            st.write(f"**Nome Azienda:** {dati_azienda['nome_azienda']}")
            st.write(f"**Partita IVA:** {dati_azienda['partita_iva']}")
            st.write(f"**Fatturato:** €{dati_azienda['fatturato']}")
        except Exception as e:
            st.error(f"Errore durante l'estrazione: {e}")

elif page == "Analisi":
    st.header("Analisi dei Dati")
    st.write("Ecco un'anteprima dei dati di analisi:")
    st.dataframe(data_analysis)

elif page == "Dashboard":
    st.header("Dashboard dei Risultati")
    st.write("Ecco un'anteprima della dashboard:")
    st.dataframe(dashboard)
    st.bar_chart(dashboard["Punteggio di compliance"])  # Adatta il nome della colonna ai dati reali
