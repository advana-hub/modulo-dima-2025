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
    return (
        PCA,
        SparseRandomProjection,
        TfidfVectorizer,
        go,
        johnson_lindenstrauss_min_dim,
        mo,
        np,
        pd,
        px,
        umap,
    )


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
def _(pd):
    df = pd.read_parquet("../data/data.parquet")
    df.head(5)
    return (df,)


@app.cell
def _(mo):
    mo.md(
        r"""Come visto in precedenza, estraiamo a caso $n=1000$ righe ed otteniamo una rappresentazione vettoriale dei testi contenuti nella colonna text."""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ```python
    reviews = df.sample(1_000)[["text", "stars"]]
    ```
    """
    )
    return


@app.cell
def _(df):
    reviews = df.sample(1_000)[["text", "stars"]]

    reviews.head(5)
    return (reviews,)


@app.cell
def _(mo):
    mo.md(
        r"""
    ```python
    tfidf = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        stop_words="english",
        max_features=500
    )
    reviews_tfidf = tfidf.fit_transform(reviews["text"])
    ```
    """
    )
    return


@app.cell
def _(TfidfVectorizer, pd, reviews):
    tfidf = TfidfVectorizer(lowercase=True, strip_accents="unicode", stop_words="english", max_features=500)
    reviews_tfidf = tfidf.fit_transform(reviews["text"])

    pd.DataFrame(
        data=reviews_tfidf.toarray(),
        index=reviews.index,
        columns=tfidf.get_feature_names_out(),
    ).head(5)
    return (reviews_tfidf,)


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
def _(PCA, reviews_tfidf):
    tfidf_pca = PCA(n_components=3)
    reviews_tfidf_r = tfidf_pca.fit_transform(reviews_tfidf)
    return (reviews_tfidf_r,)


@app.cell
def _(np, pd, px, reviews, reviews_tfidf_r):
    reviews_tfidf_r_plot = pd.DataFrame(
        data=np.hstack(
            (
                reviews_tfidf_r[:, :3],
                reviews["stars"].values.reshape(-1, 1),
                reviews["text"].values.reshape(-1, 1),
            )
        ),
        columns=["PC1", "PC2", "PC3", "stars", "text"],
        index=reviews.index,
    )
    reviews_tfidf_r_plot["stars"] = reviews_tfidf_r_plot["stars"].astype(float)

    def format_review(text, words_per_line=10, max_words=50):
        words = text.split()
        if len(words) > max_words:
            words = words[:max_words] + ["..."]
        return "<br>".join([" ".join(words[i : i + words_per_line]) for i in range(0, len(words), words_per_line)])

    reviews_tfidf_r_plot["text"] = reviews_tfidf_r_plot["text"].apply(format_review)

    px.scatter_3d(
        reviews_tfidf_r_plot,
        x="PC1",
        y="PC2",
        z="PC3",
        color="stars",
        hover_data="text",
    )
    return (format_review,)


@app.cell
def _(mo):
    mo.md(
        r"""
    Dalla semplice visualizzazione in 3 dimensioni non sempre è possibile trarre delle conclusioni solide sui dati raccolti. In questo caso, però, colorando i punti in base alla quantità di _stars_ assegnate ad ogni review, è possibile __intuire__ dei pattern.

    È comunque lecito porsi il dubbio: volendo utilizzare PCA come step di preprocessing in una pipeline più lunga, come avremmo potuto, in maniera quantitativa, scegliere una dimensionalità adeguata? In altre parole, una dimensionalità che permetta di **preservare** la maggior parte della varianza, escludendo le componenti superflue?

    Per rispondere a questa domanda, osserviamo l'andamento della somma cumulata di explained_variance_ratio_ che misura, per ogni _principal component_ la quantità di varianza spiegata.

    ```python
    pca = PCA(n_components=100)
    reviews_tfidf_r = pca.fit_transform(reviews_tfidf)

    cumsum = np.cumsum(pca.explained_variance_ratio_)
    ```

    Una scelta ragionevole può essere quella di impostare una soglia di varianza catturata che _ci soddisfi_ (es 75%), e di fermarci alla dimensionalità $d^*$ che ci permette di catturarla.
    """
    )
    return


@app.cell
def _(PCA, np, reviews_tfidf):
    tfidf_pca_2 = PCA(n_components=100)
    tfidf_pca_2.fit_transform(reviews_tfidf)
    cumsum = np.cumsum(tfidf_pca_2.explained_variance_ratio_)
    return (cumsum,)


@app.cell
def _(cumsum, mo):
    thresh = mo.ui.slider(
        label="Explained variance threshold (%)",
        start=0.01,
        value=cumsum[-2] / 2,
        stop=float(cumsum[-2]),
        step=0.001,
    )
    thresh
    return (thresh,)


@app.cell
def _(cumsum, np, thresh):
    d_star = int(np.argmax(cumsum >= thresh.value)) + 1
    return (d_star,)


@app.cell
def _(cumsum, d_star, go, pd):
    var_fig = pd.Series(
        name="Explained variance ratio",
        data=cumsum,
        index=[f"PC{i}" for i in range(1, 101)],
    ).plot()
    var_fig.add_trace(go.Scatter(x=[f"PC{d_star}"], y=[cumsum[d_star]], name=f"d* = {d_star}"))
    var_fig.add_hline(y=cumsum[d_star], line_dash="dash", line_color="red", opacity=0.75)
    var_fig.add_vline(x=f"PC{d_star}", line_dash="dash", line_color="red", opacity=0.75)
    var_fig.update_yaxes(title="Explained variance ratio (%)")
    var_fig.update_xaxes(title="")
    var_fig.update_layout(legend_title_text="")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Random projection

    Abbiamo appena visto come sia possibile scegliere una dimensione target $d^*$ basandoci sul criterio della _varianza preservata_. Vediamo ora un altro approccio.

    Può sembrare strano a dirsi, ma è stato [dimostrato](https://en.wikipedia.org/wiki/Johnson%E2%80%93Lindenstrauss_lemma) che una proiezione lineare casuale di punti ad alta dimensionalità preserva le distanze mutue tra di essi. Detto altrimenti, a valle della random projection, due punti che erano simili in alta dimensionalità lo restano in bassa accettando una distorsione $\varepsilon$.

    Dati $n$ punti di dimensione arbitraria e fissata la quantità di distorsione accettata $\varepsilon$ è possibile effettuare una random projection alla dimensione seguente.

    \[
        d' = 4 \frac{\log(n)}{\varepsilon^2/2 + \varepsilon^2/3}
    \]

    Vediamo come $d'$ varia al variare di $n$ e $\varepsilon$.
    """
    )
    return


@app.cell
def _(go, johnson_lindenstrauss_min_dim, np):
    n_samples = np.arange(100, 10_000, 1000)
    eps = np.linspace(0.1, 0.5, len(n_samples))

    nn, ee = np.meshgrid(n_samples, eps)

    # d_jl = 4 * np.log(nn) / ((ee**2) / 2 + (ee**2) / 3)
    d_jl = johnson_lindenstrauss_min_dim(n_samples=nn, eps=ee)

    hover_template = "n: %{x:.0f}<br>ε: %{y:.2f}<br>d: %{z:.0f}<extra></extra>"

    fig_jl = go.Figure(data=[go.Surface(x=nn, y=ee, z=d_jl, colorscale="Viridis", hovertemplate=hover_template)])

    # Update layout
    fig_jl.update_layout(
        scene=dict(
            xaxis_title="n",
            yaxis_title="ε",
            zaxis_title="d'",
        )
    )

    fig_jl
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Anche in questo caso possiamo sfruttare `scikit-learn`, che ci offre SparseRandomProjectionSparseRandomProjection , ovvero un tranormertransformer che implementa in maniera efficiente la riduzione di dimensionalità via random projection.

    ```python
    from sklearn.random_projection import SparseRandomProjection

    rp = SparseRandomProjection(n_components="auto", eps=0.5)
    reviews_tfidf_r = rp.fit_transform(reviews_tfidf)

    print(reviews_tfidf_r_sp.shape)
    ```
    """
    )
    return


@app.cell
def _(SparseRandomProjection, reviews_tfidf):
    rp = SparseRandomProjection(n_components="auto", eps=0.5)
    reviews_tfidf_r_sp = rp.fit_transform(reviews_tfidf)

    reviews_tfidf_r_sp.shape
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    /// warning | Avendo qui utilizzato un numero relativamente contenuto di samples, questa tecnica di riduzione di dimensionalità si dimostra essere poco efficace.
    ///

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
    return metric, min_dist, n_neighbors, spread


@app.cell
def _(metric, min_dist, n_neighbors, reviews_tfidf, spread, umap):
    reducer = umap.UMAP(
        n_components=3,
        n_neighbors=n_neighbors.value,
        min_dist=min_dist.value,
        metric=metric.value,
        spread=spread.value,
    )

    umap_embedding = reducer.fit_transform(reviews_tfidf)
    return (umap_embedding,)


@app.cell
def _(format_review, np, pd, px, reviews, umap_embedding):
    umap_reviews_tfidf_r_plot = pd.DataFrame(
        data=np.hstack(
            (
                umap_embedding[:, :3],
                reviews["stars"].values.reshape(-1, 1),
                reviews["text"].values.reshape(-1, 1),
            )
        ),
        columns=["e1", "e2", "e3", "stars", "text"],
        index=reviews.index,
    )
    umap_reviews_tfidf_r_plot["stars"] = umap_reviews_tfidf_r_plot["stars"].astype(float)
    umap_reviews_tfidf_r_plot["text"] = umap_reviews_tfidf_r_plot["text"].apply(format_review)

    px.scatter_3d(
        umap_reviews_tfidf_r_plot,
        x="e1",
        y="e2",
        z="e3",
        color="stars",
        hover_data="text",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""Al fine di ottenere una rappresentazione che ci permetta di individuare pattern nei dati, possiamo modificare il numero di vicini considerati (N° neighbors), settare la distanza minima ed il corrispondente valore di _spread_; nonché la metrica di distanza utilizzata."""
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    /// tip | Approfondimenti & link utili

        - [📖 Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow, 3rd Edition - Capitolo 8 - Dimensionality Reduction](https://github.com/ageron/handson-ml3)

        - [🤓 The Johnson-Lindenstrauss bound for embedding with random projections - scikit-learn](https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_johnson_lindenstrauss_bound.html#sphx-glr-auto-examples-miscellaneous-plot-johnson-lindenstrauss-bound-py)

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
