from lxml import etree

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
