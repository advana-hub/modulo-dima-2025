# /// script
# dependencies = [
#   "duckdb==1.1.3",
#   "pandas==2.2.3",
#   "pyarrow==18.1.0",
#   "marimo>=0.11.18",
#   "plotly==5.24.1",
#   "folium==0.19.4",
# ]
# ///

import marimo

__generated_with = "0.12.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px

    pd.options.plotting.backend = "plotly"
    return mo, pd, px


@app.cell
def _(mo):
    mo.md(
        r"""
        # Il nostro dataset

        | domanda | risposta |
        | ------- | -------- |
        | Da che contesto provengono i dati? | dataset didattico offerto da Yelp, azienda di servizi commerciali |
        | Quale fenomeno o processo descrivono i dati? | recensioni di esercizi commerciali |
        | Qual è il sistema sorgente che li ha prodotti? | ignoto |
        | dato strutturato o non strutturato? | strutturato |
        | in che formato è disponibile il dato? | parquet |
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        # Caricamento del dataset

        Cheatsheet: [pandas](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# Analisi dello schema""")
    return


@app.cell
def _(mo):
    mo.md("""## quanti campioni ho a disposizione?""")
    return


@app.cell
def _(mo):
    mo.md(r"""## quanti attributi ho a disposizione?""")
    return


@app.cell
def _(mo):
    mo.md(r"""## uno shortcut""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## quali attributi contiene il mio dataset?

        - ci sono grandezze temporali?
        - ci sono dati testuali?
        - ci sono dati geografici?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## sono presenti solo valori numerici?""")
    return


@app.cell
def _(mo):
    mo.md(r"""## vediamo una preview del dataset""")
    return


@app.cell
def _(mo):
    mo.md(r"""# Analisi dei valori""")
    return


@app.cell
def _(mo):
    mo.md(r"""## ci sono righe duplicate?""")
    return


@app.cell
def _(mo):
    mo.md(r"""## ci sono colonne con valori mancanti o non validi?""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## valori numerici

        - ci sono colonne con valori anomali o fuori scala (per dati numerici)?
        - i valori numerici sono continui o numerabili?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## i dati seguono delle distribuzioni particolari?""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## i dati presentano dinamiche temporali "interessanti"?

        Proviamo, ad esempio, a visualizzare la distribuzione degli orari in cui gli utenti pubblicano recensioni
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## ci sono relazioni tra le colonne?

        Visualizziamo per esempio lat e lon
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        # Spazio alla curiosità: visualizziamo!

        Scopo dell'esperimento: visualizzare su mappa geografica i luoghi recensiti dall'utente che ha espresso più recensioni.
        """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
