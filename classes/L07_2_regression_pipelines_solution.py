# /// script
# dependencies = [
#   "marimo>=0.11.18",
#   "matplotlib==3.10.0",
#   "numpy==2.1.3",
#   "pandas==2.2.3",
#   "pyarrow==18.1.0",
#   "plotly==5.24.1",
#   "scikit-learn==1.6.1",
# ]
# ///

import marimo

__generated_with = "0.13.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.express as px
    from sklearn import metrics
    from sklearn.ensemble import AdaBoostRegressor
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import FunctionTransformer, StandardScaler
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.compose import ColumnTransformer

    pd.options.plotting.backend = "plotly"
    return (
        AdaBoostRegressor,
        ColumnTransformer,
        CountVectorizer,
        DecisionTreeRegressor,
        FunctionTransformer,
        Pipeline,
        StandardScaler,
        metrics,
        mo,
        pd,
        train_test_split,
    )


app._unparsable_cell(
    r"""
    Vediamo ora come applicare quanto appreso nella lezione precedente al consueto dataset di Yelp. Iniziamo, come sempre, con il caricare i dati.
    """,
    name="_"
)


@app.cell
def _(pd):
    data = pd.read_parquet("../data/data.parquet")
    data
    return (data,)


@app.cell
def _(mo):
    mo.md(r"""Il nostro goal è creare un predittore delle _stars_, quali colonne potremmo considerare come input features?""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Per evitare di incorrere in _overfit_ procediamo con la suddivisione del nostro dataset in due parti: training e test set.

    Sfruttiamo, come di consueto, `scikit-learn`: [`train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html).
    """
    )
    return


@app.cell
def _(data, train_test_split):
    train_data, test_data = train_test_split(
        data[["text", "stars", "latitude", "longitude", "review_count"]],
        test_size=0.90,
        random_state=42,
    )
    return test_data, train_data


@app.cell
def _(train_data):
    train_data
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Preprocessing

    Una volta suddiviso il dataset e selezionate le colonne giuste è arrivato il momento di create la matrice dei dati $X$ ed il vettore dei target $\bm{y}$.
    """
    )
    return


@app.cell
def _(test_data, train_data):
    dfX_train = train_data.drop(["stars"], axis="columns")
    dfy_train = train_data["stars"]
    print(f"training samples: {len(dfX_train)}")

    dfX_test = test_data.drop(["stars"], axis="columns")
    dfy_test = test_data["stars"]
    print(f"test samples: {len(dfX_test)}")
    return dfX_test, dfX_train, dfy_test, dfy_train


@app.cell
def _(mo):
    mo.md(
        """
    ## Pipeline n°1: __Bag-of-words__ + __Decision Tree__

    Il processo end-to-end può essere implementato completamente sfruttando la classe [`sklearn.pipeline.Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html).

    Sfruttiamo quanto appreso nei laboratori precedenti per creare la nostra prima pipeline.
    """
    )
    return


@app.cell
def _(
    CountVectorizer,
    DecisionTreeRegressor,
    FunctionTransformer,
    Pipeline,
    StandardScaler,
    dfX_train,
    dfy_train,
):
    pipe_1 = Pipeline(
        [
            (
                "extract_sparse_features",
                CountVectorizer(strip_accents="unicode", stop_words="english", max_features=500),
            ),
            (
                "make_dense_features",
                FunctionTransformer(lambda x: x.toarray(), accept_sparse=True),
            ),
            ("scaling", StandardScaler()),
            ("regression", DecisionTreeRegressor()),
        ]
    )
    pipe_1.fit(dfX_train["text"], dfy_train)
    return (pipe_1,)


@app.cell
def _(dfX_test, pipe_1):
    y_pred_bow = pipe_1.predict(dfX_test["text"])
    return (y_pred_bow,)


@app.cell
def _(dfy_test, metrics, y_pred_bow):
    print(f"MAPE: {metrics.mean_absolute_percentage_error(dfy_test.values, y_pred_bow):.4f}")
    print(f"MAE: {metrics.mean_absolute_error(dfy_test.values, y_pred_bow):.4f}")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Pipeline n°2: __Bag-of-words__ & __Numerical features__ + __Decision Tree__

    La prima pipeline ci permette di lavorare solo sulla trasformazione della colonna `text`. Vediamo come possiamo sfruttare [`sklearn.compose.ColumnTransformer`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html) per estrarre informazione anche da altri tipi di colonne.
    """
    )
    return


@app.cell
def _(CountVectorizer, FunctionTransformer, Pipeline, StandardScaler):
    text_preproc = Pipeline(
        [
            (
                "extract",
                CountVectorizer(strip_accents="unicode", stop_words="english", max_features=500),
            ),
            (
                "make_dense_features",
                FunctionTransformer(lambda x: x.toarray(), accept_sparse=True),
            ),
            ("scaling", StandardScaler()),
        ]
    )
    return (text_preproc,)


@app.cell
def _(ColumnTransformer, StandardScaler, text_preproc):
    feat_extr = ColumnTransformer(
        [
            ("bow", text_preproc, "text"),
            ("numerical", StandardScaler(), ["latitude", "longitude", "review_count"]),
        ]
    )
    return (feat_extr,)


@app.cell
def _(
    DecisionTreeRegressor,
    Pipeline,
    StandardScaler,
    dfX_train,
    dfy_train,
    feat_extr,
):
    pipe_1_extra = Pipeline(
        [
            ("extract_features", feat_extr),
            ("scaling", StandardScaler()),
            ("regression", DecisionTreeRegressor()),
        ]
    )
    pipe_1_extra.fit(dfX_train, dfy_train)
    return (pipe_1_extra,)


@app.cell
def _(dfX_test, pipe_1_extra):
    y_pred_bow_extra = pipe_1_extra.predict(dfX_test)
    return


@app.cell
def _(dfy_test, metrics, y_pred_bow):
    print(f"MAPE: {metrics.mean_absolute_percentage_error(dfy_test.values, y_pred_bow):.4f}")
    print(f"MAE: {metrics.mean_absolute_error(dfy_test.values, y_pred_bow):.4f}")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Pipeline n°3: Ensemble learning (boosting)

    Come accennato nella lezione precedente, i decision trees sono modelli velocissimi da allenare e questo li rende ottimi base-learner per (meta-)algoritmi di ensemble learning. Senza entrare troppo nei dettagli vediamo com'è semplice sostituire alla pipeline precedente lo step finale con un [`sklearn.ensemble.AdaBoostRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostRegressor.html) e valutiamo l'impatto sulle performance.
    """
    )
    return


@app.cell
def _(
    AdaBoostRegressor,
    DecisionTreeRegressor,
    Pipeline,
    StandardScaler,
    dfX_train,
    dfy_train,
    feat_extr,
):
    pipe_2 = Pipeline(
        [
            ("extract_features", feat_extr),
            ("scaling", StandardScaler()),
            (
                "regression",
                AdaBoostRegressor(estimator=DecisionTreeRegressor(), n_estimators=50),
            ),
        ]
    )
    pipe_2.fit(dfX_train, dfy_train)
    return (pipe_2,)


@app.cell
def _(dfX_test, pipe_2):
    y_pred_boost = pipe_2.predict(dfX_test)
    return (y_pred_boost,)


@app.cell
def _(dfy_test, metrics, y_pred_boost):
    print(f"MAPE: {metrics.mean_absolute_percentage_error(dfy_test.values, y_pred_boost):.4f}")
    print(f"MAE: {metrics.mean_absolute_error(dfy_test.values, y_pred_boost):.4f}")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
