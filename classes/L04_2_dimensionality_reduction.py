# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.11.18",
#     "matplotlib==3.10.0",
#     "numpy==2.1.3",
#     "pandas==2.2.3",
#     "plotly==5.24.1",
#     "scikit-learn==1.6.1",
#     "pyarrow==18.1.0",
#     "umap-learn==0.5.7",
#     "numba==0.61.0",
# ]
# ///

import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    import numpy as np
    import pandas as pd
    import pyarrow

    import umap
    from sklearn import metrics
    from sklearn.decomposition import PCA
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.random_projection import johnson_lindenstrauss_min_dim
    from sklearn.random_projection import SparseRandomProjection

    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    pd.options.plotting.backend = "plotly"
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Dimensionality reduction pt. 2

    Vediamo ora come questa tecnica possa essere applicata per ridurre la dimensionalità del nostro dataset di Yelp. Iniziamo con il caricare in memoria il dataframe delle review già sfruttato nei laboratori precedenti.
    """
    )
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(r"""Come visto in precedenza, estraiamo a caso $n=1000$ righe ed otteniamo una rappresentazione vettoriale dei testi contenuti nella colonna text.""")
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Prima di procedere è necessario chiarire quali siano le nostre intenzioni. Perché stiamo cercando di ridurre la dimensionalità dei dati? Vogliamo semplicemente visualizzare i punti su un piano cartesiano, e allora saremo obbligati a scegliere una dimensione pari a 2 o al massimo 3, o vogliamo usare PCA come step di preprocessing in una pipeline più lunga di operazioni?

    Partiamo con il primo caso. Riduciamo la dimensionalità della rappresentazione a vettoriale a $d'=3$ e visualizziamo la nuvola di punti.
    """
    )
    return


@app.cell
def _():
    return


@app.cell
def _():
    # Hint: per la visualizzazione può essere comodo
    #       usare la seguente funzione
    # px.scatter_3d(
    #     df_3d,
    #     x="PC1",
    #     y="PC2",
    #     z="PC3",
    #     color="stars",
    # )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Dalla semplice visualizzazione in 3 dimensioni non sempre è possibile trarre delle conclusioni solide sui dati raccolti. In questo caso, però, colorando i punti in base alla quantità di _stars_ assegnate ad ogni review, è possibile __intuire__ dei pattern.

    È comunque lecito porsi il dubbio: volendo utilizzare PCA come step di preprocessing in una pipeline più lunga, come avremmo potuto, in maniera quantitativa, scegliere una dimensionalità adeguata? In altre parole, una dimensionalità che permetta di **preservare** la maggior parte della varianza, escludendo le componenti superflue?

    Per rispondere a questa domanda, osserviamo l'andamento della somma cumulata di explained_variance_ratio_ che misura, per ogni _principal component_ la quantità di varianza spiegata.


    Una scelta ragionevole può essere quella di impostare una soglia di varianza catturata che _ci soddisfi_ (es 75%), e di fermarci alla dimensionalità $d^*$ che ci permette di catturarla.
    """
    )
    return


@app.cell
def _():
    thresh = 0.75
    return


@app.cell
def _():
    # hint 1: Osserviamo cosa contiene pca.explained_variance_ratio_
    # hint 2: Per implementare la somma cumulata possiamo usare np.cumsum
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Uniform Manifold Approximation and Projection (UMAP)

    Veniamo infine alla tecnica che, ad oggi, è diventata lo standard _de-facto_ per effettuare task di _dimensionality reduction_ in molti contesti reali: __UMAP__.

    Questa tecnica sfrutta concetti di _manifold learning_, _topological data analysis_ e _fuzzy logic_ per identificare una rappresentazione di dimensione arbitraria di un insieme di punti (originariamente in alta dimensionalità) cercando di preservare il più possibile le loro proprietà _locali_.

    L'algorimo di UMAP prevede due step, il primo passo consiste nella creazione di un _k-neighbor graph_, ovvero un grafo in cui due nodi (_ie_ due samples) sono connessi da un arco se sufficientemente _vicini_ in alta dimensionalità. Il secondo step consiste nell'identificazione di una proiezione in bassa dimensionalità dei punti in maniera tale che il _k-neighbor graph_ costruito su di essa sia il più simile possibile a quello ricavato originariamente.

    Una implementazione di questa tecnica __non__ è disponibile tramite scikit-learn, ma esiste una library Python sviluppata dai creatori di UMAP che offre un transformer totalmente compatibile con le API di scikit-learn (che di fatto sono uno standard nel mondo del machine learning).

    Vediamo come possiamo applicare UMAP al nostro dataset e visualizziamo i samples nello spazio così ottenuto.
    """
    )
    return


@app.cell
def _(mo):
    n_neighbors = mo.ui.slider(
        label="N° neighbors",
        start=2,
        value=15,
        stop=200,
        step=5,
    )
    min_dist = mo.ui.slider(
        label="Minimum distance",
        start=0.001,
        value=0.1,
        stop=0.999,
        step=0.001,
    )
    spread = mo.ui.slider(
        label="Spread",
        start=0.001,
        value=0.1,
        stop=0.999,
        step=0.001,
    )
    metric = mo.ui.dropdown(
        options=["euclidean", "manhattan", "cosine"],
        label="Metric",
        value="euclidean",
    )

    mo.md(f"{n_neighbors}  {min_dist} {spread} {metric}")
    return


@app.cell
def _():
    # hint: controlla la documentazione di umap.UMAP()
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(r"""Al fine di ottenere una rappresentazione che ci permetta di individuare pattern nei dati, possiamo modificare il numero di vicini considerati (N° neighbors), settare la distanza minima ed il corrispondente valore di _spread_; nonché la metrica di distanza utilizzata.""")
    return


@app.cell
def _(mo):
    mo.md(
        """
    /// tip | Approfondimenti & link utili

        - [📖 Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow, 3rd Edition - Capitolo 8 - Dimensionality Reduction](https://github.com/ageron/handson-ml3)

        - [🗺️ How UMAP Works](https://umap-learn.readthedocs.io/en/latest/how_umap_works.html)

        - [🪼 Manifold learning - scikit-learn](https://scikit-learn.org/stable/modules/manifold.html)

    ///
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
