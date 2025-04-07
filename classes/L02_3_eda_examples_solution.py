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
def _(pd):
    df = pd.read_parquet("../data/data.parquet")
    return (df,)


@app.cell
def _(mo):
    mo.md(r"""# Analisi dello schema""")
    return


@app.cell
def _(mo):
    mo.md("""## quanti campioni ho a disposizione?""")
    return


@app.cell
def _(df):
    len(df)
    return


@app.cell
def _(mo):
    mo.md(r"""## quanti attributi ho a disposizione?""")
    return


@app.cell
def _(df):
    len(df.columns)
    return


@app.cell
def _(mo):
    mo.md(r"""## uno shortcut""")
    return


@app.cell
def _(df):
    df.shape
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
def _(df):
    df.columns
    return


@app.cell
def _(mo):
    mo.md(r"""## sono presenti solo valori numerici?""")
    return


@app.cell
def _(df):
    df.dtypes.to_frame("dtype").transpose()
    return


@app.cell
def _(mo):
    mo.md(r"""## vediamo una preview e sfruttiamo la UX di Marimo!""")
    return


@app.cell
def _(df):
    df.head()
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
def _(df):
    df.duplicated().max()
    return


@app.cell
def _(mo):
    mo.md(r"""## ci sono colonne con valori mancanti o non validi?""")
    return


@app.cell
def _(df):
    df.isnull().max()
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
def _(df):
    df.select_dtypes("number")
    return


@app.cell
def _(mo):
    mo.md(r"""## i dati seguono delle distribuzioni particolari?""")
    return


@app.cell
def _(df):
    df.select_dtypes("number").hist()
    return


@app.cell
def _(mo):
    mo.md(r"""## i dati presentano dinamiche temporali "interessanti"?""")
    return


@app.cell
def _():
    "ciaomiao"[:4]
    return


@app.cell
def _(df):
    str(df["date"][0].time())[:5]
    return


@app.cell
def _(pd):
    df_animals = pd.DataFrame({"animal": ["dog", "cat", "cat"], "names": ["fido", "romeo", "matisse"], "n_legs": [4, 3, 4]})
    return (df_animals,)


@app.cell
def _(df_animals):
    df_animals.groupby("animal")["n_legs"].mean()
    return


@app.cell
def _(df_animals):
    df_animals["animal"].nunique()
    return


@app.cell
def _(df):
    (
        df
        .assign(review_time=lambda x: x["date"].apply(lambda x: str(x.time())[:5]))
        .groupby("review_time")
        ["review_id"]
        .nunique()
        .plot()
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## ci sono relazioni tra le colonne?""")
    return


@app.cell
def _(df):
    df.plot.scatter(x="latitude", y="longitude")
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _(df, px):
    fig = px.scatter(df, x="longitude", y="latitude")
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
      )
    return (fig,)


@app.cell
def _(mo):
    mo.md(r"""# Spazio alla curiosità: visualizziamo!""")
    return


@app.cell
def _(df):
    df.groupby("user_id")["review_id"].nunique().sort_values().tail(1).to_frame().index[0]
    return


@app.cell
def _(df):
    top_reviewer = (
        df
        .groupby("user_id")
        ["review_id"]
        .nunique()
        .sort_values(ascending=False)
        .head(1)
        .index
        .item()
    )
    return (top_reviewer,)


@app.cell
def _(top_reviewer):
    top_reviewer
    return


@app.cell
def _(df, top_reviewer):
    df.loc[df["user_id"]==top_reviewer].sort_values(by="business_id").reset_index(drop=True)
    return


@app.cell
def _(df, top_reviewer):
    user_data = df.loc[df["user_id"]==top_reviewer].sort_values("date").reset_index(drop=True)
    user_data
    return (user_data,)


@app.cell
def _():
    import folium
    import folium.plugins
    return (folium,)


@app.cell
def _(folium, user_data):
    geomap = folium.Map(
        location=[
            user_data["latitude"].mean(),
            user_data["longitude"].mean()
        ],
        zoom_start=13
    )

    for i, row in user_data.iterrows():
        popup = folium.Popup(
            row["categories"] + "<br><br>" + row["text"],
            min_width=500,
            max_width=500
        )
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup,
            tooltip=row.drop(["text", "categories"]).to_frame().to_html()
        ).add_to(geomap)

    geomap
    return geomap, i, popup, row


@app.cell
def _(df):
    df["text"]
    return


if __name__ == "__main__":
    app.run()
