# /// script
# dependencies = [
#   "marimo>=0.11.18",
# ]
# ///

import marimo

__generated_with = "0.11.17"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo    
    return mo


@app.cell
def _(mo):
    mo.md(
        """
        # Exploratory Data Analysis (EDA)

        L'obiettivo dell'**analisi esplorativa dei dati** è quello di conoscere meglio il contenuto di un dataset, sia "in assoluto" sia relativamente alle conoscenze pregresse a disposizione.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# Prima di iniziare l'esplorazione""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Domande di contesto

        - Da che contesto provengono i dati?
        - Quale fenomeno o processo descrivono i dati?
        - Qual è il sistema sorgente che li ha prodotti?
            - Chi gestisce il sistema sorgente?
            - Chi è il responsabile della qualità del dato?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## La struttura dei dati

        Esistono due grandi famiglie di dati:

        - dati **strutturati**, ovvero dati essenzialmente tabellari, che possono essere "immaginati" (e immagazzinati!) come tabelle in un database relazionale (interrogabile via SQL) o in un DataFrame
        - dati **non strutturati**, ovvero tutto il resto: email, chat, analitiche di interazioni web e social, audio, video, immagini, documenti testuali
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        /// warning | "Dati strutturati ≠ dati numerici"
        Ad esempio, un dataset strutturato (tabellare) può benissimo comprendere del testo.
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        /// note | "Perchè le immagini sono considerate dati _non strutturati_?"
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        In un dato strutturato esiste uno **schema** ben definito che indica in maniera chiara quale _informazione_ è contenuta in ciascuna posizione della struttura.

        Possiamo pensare a tale schema come a un **metadato** (ovvero un dato riguardo i nostri dati, che indicano che cosa riguardano i nostri dati 🤯).


        /// tip | "Rappresentazione standard"
        In un dato tabellare, di norma, si usa uno schema essenzialmente matriciale in cui alla posizione $(i, j)$ si trova il $j$-esimo attributo dell'$i$-esimo campione del dataset.
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        indici riga = $(0, 1, 2, 3)$

        indici colonna = $(0, 1, 2)$

        | nome   | altezza | peso |
        | ------ | ------- | ---- |
        | Andrea |   1.67  | 56   |
        | Alex   |   1.82  | 78   |
        | Robin  |   1.74  | 63   |
        | Batman |   1.90  | 90   |

        L'informazione contenuta alla posizione $(1, 2)$ è il peso di Alex.

        Se incremento di 1 l'indice di riga mantenendo fisso l'indice colonna, spostandomi cioè alla posizione $(2, 2)$, so che troverò sempre un'informazione relativa al peso (di Robin, questa volta).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Le immagini, pur essendo immagazzinate tramite tensori (decisamente strutturati), non sono però dotate di uno schema altrettanto efficace!

        Nella prima delle seguenti immagini, per esempio:

        - che _informazione_ è contenuta dal primo pixel in alto a sinistra?
        - E come cambia l'informazione muovendosi alla "riga" di pixel successivi?
        - In quali pixel è rappresentato _il naso_ del cane?

        E le stesse risposte valgono anche per la seconda immagine?

        |  |  |
        | - | - |
        | ![](data:image/jpeg;base64,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) | ![](data:image/jpeg;base64,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) |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        /// note | "Questo è un dato strutturato?"

        ```
        La Costituzione

        Parte I

        Diritti e doveri dei cittadini

        Titolo II

        Rapporti etico-sociali

        Articolo 34

        La scuola è aperta a tutti.
        L'istruzione inferiore, impartita per almeno otto anni, è obbligatoria e gratuita.
        I capaci e meritevoli, anche se privi di mezzi, hanno diritto di raggiungere i gradi più alti degli studi.
        La Repubblica rende effettivo questo diritto con borse di studio, assegni alle famiglie ed altre provvidenze,
        che devono essere attribuite per concorso.
        ```
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        /// tip | "Dati non strutturati ~ informazione difficile da localizzare, estrarre e "navigare""
        Se ci si "accontenta", tutto è strutturato. Se l'informazione cui si è interessati è viceversa ad un più alto livello di astrazione, la struttura non è così semplice da ottenere.
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Il formato dei dati

        /// note | "D'ora in avanti parleremo principalmente di dati tabellari (strutturati)"
        ///

        I formati più comuni per dati strutturati:

        - csv (comma-separated values)
        - json (JavaScript Object Notation)
        - parquet (column-oriented data file format)
        - XML (eXtensible Markup Language)
        - xlsx (Excel file format, sostanzialmente un archivio compresso contenente XML)
        - ...
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# EDA = curiosità + investigazione + visualizzazione""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Qualche domanda per iniziare

        /// note | "Rappresentazione standard"
        In un dato tabellare, di norma, si usa uno schema essenzialmente matriciale in cui alla posizione $(i, j)$ si trova il $j$-esimo attributo dell'$i$-esimo campione del dataset.
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Analisi dello schema

        - quanti campioni ho a disposizione?
        - quanti attributi ho a disposizione?
        - quali attributi contiene il mio dataset?
        - sono presenti solo valori numerici?
        - ci sono grandezze temporali?
        - ci sono dati testuali?
        - ci sono dati geografici?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Analisi dei valori

        - pulizia dei dati:
            - ci sono righe duplicate?
            - ci sono colonne con valori mancanti o non validi?
            - ci sono colonne con valori anomali o fuori scala (per dati numerici)?
        - i valori numerici sono continui o numerabili?
        - i dati seguono delle distribuzioni particolari?
        - i dati presentano dinamiche temporali "interessanti"?
        - ci sono relazioni tra le colonne?
        """
    )
    return


if __name__ == "__main__":
    app.run()
