# /// script
# dependencies = [
#   "duckdb==1.1.3",
#   "pandas==2.2.3",
#   "pyarrow==18.1.0",
#   "marimo>=0.11.18",
#   "plotly==5.24.1",
#   "folium==0.19.4",
#   "sqlglot==26.9.0",
# ]
# ///

import marimo

__generated_with = "0.11.22"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import os
    from pathlib import Path

    pd.options.plotting.backend = "plotly"
    return Path, mo, os, pd, px


@app.cell
def _(mo):
    mo.md(
        r"""
        # Preparazione dati

        /// tip | Scopo di questo notebook
        Lo scopo di questo notebook è dare un assaggio delle complessità e dei problemi che si affrontano per _acquisire_ e _preparare_ dei dati prima di analizzarli.

        Nelle realtà più mature, di questi problemi si occupano i Data Engineers.
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# Carichiamo i dataset grezzi""")
    return


@app.cell
def _(pd):
    yelp_academic_dataset_business = pd.read_json(
        "../../raw_data/yelp_academic_dataset_business.json",
        lines=True
    )
    return (yelp_academic_dataset_business,)


@app.cell
def _(pd):
    yelp_academic_dataset_checkin = pd.read_json(
        "../../raw_data/yelp_academic_dataset_checkin.json",
        lines=True
    )
    return (yelp_academic_dataset_checkin,)


@app.cell
def _(pd):
    yelp_academic_dataset_tip = pd.read_json(
        "../../raw_data/yelp_academic_dataset_tip.json",
        lines=True
    )
    return (yelp_academic_dataset_tip,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Ecco che a volte arrivano i limiti fisici

        Se eseguiamo questo codice per caricare il dataset degli utenti...

        `python
        yelp_academic_dataset_user_full = pd.read_json(
            "../../raw_data/yelp_academic_dataset_user.json",
            lines=True
        )
        `

        ...a seconda del nostro hardware otteniamo un bel [MemoryError](https://docs.python.org/3/library/exceptions.html#MemoryError)!
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cosa facciamo ora ? 

        A volte può capitare che non sia possibile accedere immediatamente all'intero dataset e quindi è necessario creare dei piccoli sample così da avviare le analisi e prepare le trasformazioni dei dati per un flusso che cercherà di ottimizzare la lettura.
        """
    )
    return


@app.cell
def _(pd):
    yelp_academic_dataset_user_full = pd.read_json(
        "../../raw_data/yelp_academic_dataset_user.json",
        lines=True,
        chunksize = 100_000
    )
    return (yelp_academic_dataset_user_full,)


@app.cell
def _(yelp_academic_dataset_user_full):
    yelp_academic_dataset_user_chunk = next(yelp_academic_dataset_user_full)
    return (yelp_academic_dataset_user_chunk,)


@app.cell
def _(pd):
    yelp_academic_dataset_review_full = pd.read_json(
        "../../raw_data/yelp_academic_dataset_review.json",
        lines=True,
        chunksize = 100_000
    )
    return (yelp_academic_dataset_review_full,)


@app.cell
def _(yelp_academic_dataset_review_full):
    yelp_academic_dataset_review_chunk = next(yelp_academic_dataset_review_full)
    return (yelp_academic_dataset_review_chunk,)


@app.cell
def _(yelp_academic_dataset_business):
    yelp_academic_dataset_business.head(5)
    return


@app.cell
def _(yelp_academic_dataset_checkin):
    yelp_academic_dataset_checkin.head(5)
    return


@app.cell
def _(yelp_academic_dataset_tip):
    yelp_academic_dataset_tip.head(5)
    return


@app.cell
def _(yelp_academic_dataset_review_chunk):
    yelp_academic_dataset_review_chunk.head(5)
    return


@app.cell
def _(yelp_academic_dataset_user_chunk):
    yelp_academic_dataset_user_chunk.head(5)
    return


@app.cell
def _(mo):
    mo.md(r"""# Analisi dello schema""")
    return


@app.cell
def _(mo):
    mo.md(
        """
        Possiamo notare come alcune colonne sono fondamentali per poter collegare i diversi file, in particolare:

        - user_id
        - business_id
        - review_id

        /// note | yelp_academic_dataset_review
        In questo dataset i tre campi sono tutti presenti!
        ///

        /// note | Dataset potenzialmente meno utili
        Notiamo che due file hanno informazioni meno significative: yelp_academic_dataset_checkin, yelp_academic_dataset_tip... potremmo non tenerli più in memoria.
        ///

        /// note | Dataset più informativi
        Invece altri due file hanno informazioni più interessanti per costruire il dataset di partenza: 

        - yelp_academic_dataset_user_chunk, che contiene informazioni sui singoli utenti e sulla media di recensioni e amici collegati;
        - yelp_academic_dataset_business, contenente informazioni sui singoli negozi, la loro posizione, il loro punteggio medio e il loro numero di recensioni.
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""## Quanti campioni ho a disposizione?""")
    return


@app.cell
def _(
    yelp_academic_dataset_business,
    yelp_academic_dataset_review_chunk,
    yelp_academic_dataset_user_chunk,
):
    print("N° records\n")

    print('Business dataset:', len(yelp_academic_dataset_business))
    print('Review dataset:', len(yelp_academic_dataset_review_chunk))
    print('User dataset:', len(yelp_academic_dataset_user_chunk))
    return


@app.cell
def _(mo):
    mo.md(r"""## Quali attributi ho a disposizione? E quali sono necessari?""")
    return


@app.cell
def _(yelp_academic_dataset_business):
    yelp_academic_dataset_business.columns
    return


@app.cell
def _(yelp_academic_dataset_review_chunk):
    yelp_academic_dataset_review_chunk.columns
    return


@app.cell
def _(yelp_academic_dataset_user_chunk):
    yelp_academic_dataset_user_chunk.columns
    return


@app.cell
def _(mo):
    mo.md(
        """
        /// tip | Idea
        Andiamo a selezionare un gruppo di colonne per alleggerire il nostro dataset, con informazioni che noi riteniamo utili per le nostre analisi. Un paio di consigli:

        1. **favorire il riciclo**: cerchiamo sempre di essere elastici e di non creare strutture troppo rigide, molto spesso le analisi si basano sempre sugli stessi dataset ma concentrandosi su colonne diverse;
        2. **meglio un uovo oggi che un gallina domani**: cercare di avere un buon dataset di partenza (non eccessivamente grande ma anche non eccessivamente piccolo) può favorire ulteriori analisi successivamente.
        3. **rispetto della privacy**: a meno di indicazioni/contesti specifici, è sempre meglio escludere dai dataset informazioni personali e/o sensibili
        ///
        """
    )
    return


@app.cell
def _(
    yelp_academic_dataset_business,
    yelp_academic_dataset_review_chunk,
    yelp_academic_dataset_user_chunk,
):
    df_review = yelp_academic_dataset_review_chunk.loc[:, ['review_id', 'user_id', 'business_id', 'stars', 'text', 'date']]
    df_user = yelp_academic_dataset_user_chunk.loc[:, ['user_id', 'name', 'review_count', 'yelping_since',   'fans', 'average_stars']]
    df_business = yelp_academic_dataset_business.loc[:, ['business_id', 'name','latitude', 'longitude', 'review_count', 'categories','city']]
    return df_business, df_review, df_user


@app.cell
def _(mo):
    mo.md(
        """
        # Costruiamo il nostro dataset

        Ora possiamo creare il nostro dataset di partenza che utilizzeremo d'ora in avanti.
        """
    )
    return


@app.cell
def _(df_business, df_review):
    df_filtered_review = df_review.loc[df_review['date'] > '2014-01-01 00:00:00']
    df_filtered_business = df_business.loc[df_business['city'] == 'Philadelphia']
    return df_filtered_business, df_filtered_review


@app.cell
def _(df_business, df_filtered_business, df_filtered_review, df_review):
    print(f'Size filtered review {len(df_filtered_review)} vs review {len(df_review)}')
    print(f'Size filtered business {len(df_filtered_business)} vs business {len(df_business)}')
    return


@app.cell
def _(mo):
    mo.accordion({"Piccola nota: Pandas merge vs SQL join": mo.md(
        """Il comando `pandas.merge` è l'equivalente di una JOIN in SQL.

        **df1**

        | X | Y |
        |---|---|
        | 1 | a |
        | 2 | b |
        | 3 | c |

        **df2**

        | X | Z |
        |---|---|
        | 1 | cane |
        | 3 | gatto |
        | 5 | pippo |

        **df1.merge(df2)**

        | X | Y | Z |
        |---|---|---|
        | 1 | a | cane |
        | 3 | c | gatto |
        """
    )})
    return


@app.cell
def _(df_business, df_filtered_business, df_filtered_review, df_review):
    df_dataset = df_review.merge(df_business, on='business_id')
    df_dataset_filtered = df_filtered_review.merge(df_filtered_business, on='business_id')
    return df_dataset, df_dataset_filtered


@app.cell
def _(df_dataset_filtered):
    df_dataset_filtered.head()
    return


@app.cell
def _(mo):
    mo.md(r"""## Uno shortcut: SQL e DuckDB""")
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT review.review_id,
        	review.user_id,
        	review.business_id,
        	review.stars,
        	review.date,
        	review.text,
        	business.name,
        	business.latitude,
        	business.longitude,
        	business.categories,
        	business.review_count
        FROM '../../raw_data/yelp_academic_dataset_review.json' AS review
        	JOIN '../../raw_data/yelp_academic_dataset_business.json' AS business ON review.business_id = business.business_id
        WHERE business.city = 'Philadelphia'
        	AND date_part('year', review.date) >= 2014 USING sample 10000
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# Persistenza su disco""")
    return


@app.cell
def _(mo):
    save_data = mo.ui.checkbox(label="Vuoi salvare i dati su disco?")
    save_data
    return (save_data,)


@app.cell
def _(mo, save_data):
    path = None
    if save_data.value:
        path = mo.ui.text(label="Path", placeholder="Inserire il percorso locale in cui salvare i file, relativo al folder corrente...", full_width=True)
    path
    return (path,)


@app.cell
def _(Path, __file__, df_dataset_filtered, os, path):
    def persist(*args) -> None:
        os.makedirs(Path(__file__).parent.joinpath(path.value).as_posix(), exist_ok=True)
        df_dataset_filtered.to_parquet(f"{Path(__file__).parent.joinpath(path.value).joinpath('review_business_merge.parquet').as_posix()}")
    return (persist,)


@app.cell
def _(Path, __file__, mo, path, persist, save_data):
    confirm = None
    if save_data.value:    
        confirm = mo.ui.button(label=f"Salva in {Path(__file__).parent.joinpath(path.value)}", on_click=persist)
    confirm
    return (confirm,)


if __name__ == "__main__":
    app.run()
