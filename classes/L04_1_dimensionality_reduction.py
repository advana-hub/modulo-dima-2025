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

__generated_with = "0.12.9"
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

    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    pd.options.plotting.backend = "plotly"
    return PCA, go, make_subplots, metrics, mo, np, pd, px, pyarrow, umap


@app.cell
def _(mo):
    mo.md(
        """
        # Dimensionality reduction

        In questa lezione proseguiamo con l'esplorazione del campo del machine learning non supervisionato vedendo una panoramica dei sistemi di riduzione di dimensionalità.

        ## High-dimensional data

        Nello svolgimento della professione del data scientist può capitare di imbattersi in dati che presentano un elevato numero di features, ovvero dati _ad alta dimensionalità_. Pensiamo ad esempio:

        - ad una rappresentazione tramite __bag-of-words__, in ambito NLP
        - ai pixel di immagini a colori, in ambito computer vision
        - alle misure di espressione genica, in ambio biologico

        e via così.

        Lavorare con dati ad alta dimensionalità è non solo più oneroso dal punto di vista delle risorse occupate (in termini di CPU, memoria e spazio di archiviazione), ma introduce anche alcune difficoltà modellistiche.

        ## Curse of dimensionality

        Calcoliamo la distanza media di $n=50$ campioni raccolti in un ipercubo unitario di dimensione arbitraria $d$. Cosa possiamo notare?
        """
    )
    return


@app.cell
def _(np):
    samples = np.random.uniform(0, 1, size=(50, 1_000))
    return (samples,)


@app.cell
def _(mo):
    n_features = mo.ui.number(label=r"$d$", start=2, stop=1_000)
    func_name = mo.ui.dropdown(
        options=["Euclidean", "Manhattan", "Cosine"],
        label="Distanza",
        value="Euclidean",
    )
    mo.md(f"{n_features}  {func_name}")
    return func_name, n_features


@app.cell
def _(func_name, metrics, n_features, pd, samples):
    stats = []
    for i in range(2, n_features.value + 1):
        distances = metrics.pairwise_distances(samples[:, :i], metric=func_name.value.lower())
        stats.append({"d": i, "mean": distances.mean(), "std": distances.std()})
    stats = pd.DataFrame(stats)
    return distances, i, stats


@app.cell
def _():
    formulae = {
        "Euclidean": r"$d(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_{i=1}^{d} (x_i - y_i)^2}$",
        "Manhattan": r"$d(\mathbf{x}, \mathbf{y}) = \sum_{i=1}^{d} |x_i - y_i|$",
        "Cosine": r"$d(\mathbf{x}, \mathbf{y}) = 1 - \frac{\sum_{i=1}^{d} x_i y_i}{\|\mathbf{x}\| \|\mathbf{y}\|}$",
    }
    return (formulae,)


@app.cell
def _(formulae, func_name, go, stats):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stats["d"],
            y=stats["mean"],
            mode="markers",
            error_y=dict(
                symmetric=True,
                array=stats["std"],
            ),
        )
    )
    fig.update_layout(title=formulae[func_name.value])
    fig.update_xaxes(title=r"$d$")
    fig.update_yaxes(title=f"{func_name.value} distance")

    fig
    return (fig,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Al crescere di $d$ la nostra intuizione di _distanza_ non regge più. I campioni, seppur appartenenti tutti allo stesso ipercubo, risultano sempre molto lontani l'uno dall'altro. Questo può inficiare la capacità dei nostri modelli di apprendere correttamente pattern sottostanti e riduce l'affidabilità delle predizioni.

        Come possiamo attenuare questo effetto spiacevole?

        ## Principal Components Analysis (PCA)

        La tecnica più nota per la riduzione di dimensionalità è detta PCA. A partire da un set di dati di dimensione $d$, questa tecnica permette di identificare l'iperpiano di dimensione $d' < d$ tale per cui proiettando i dati su di esso la varianza viene maggiormente preservata.

        Vediamo un esempio concreto. Assumiamo di avere raccolto dei campioni in uno spazio 3d e visualizziamoli tramite scatterplot. Cosa possiamo notare?
        """
    )
    return


@app.cell
def _(np, px):
    cov = np.array([[4, 3, 1], [3, 3, 1.5], [1, 1.5, 2]])
    mean = np.array([0, 0, 0])

    samples_3d = np.random.multivariate_normal(mean, cov, 300)

    fig1 = px.scatter_3d(x=samples_3d[:, 0], y=samples_3d[:, 1], z=samples_3d[:, 2])
    fig1
    return cov, fig1, mean, samples_3d


@app.cell
def _(mo):
    mo.md(
        r"""
        I punti non sono equamente distribuiti nelle tre direzioni ortogonali dello spazio in cui sono rappresentati. Hanno infatti una chiara _predilezione_ per una direzione, che risulta diagonale rispetto agli assi dello spazio in cui sono immersi.

        PCA, in sostanza, si occupa di individuare la direzione lungo la quale si sviluppa la maggior parte della varianza. A partire da quella cerca poi le componenti perpendicolari che, via via, catturano la restante parte della varianza. Aiutiamoci, come sempre, con `scikit-learn`.

        ``` python
        from sklearn.decomposition import PCA

        pca = PCA(n_components=2)
        X_r = pca.fit_transform(X)
        ```
        """
    )
    return


@app.cell
def _(PCA, samples_3d):
    pca = PCA(n_components=2)
    samples_2d = pca.fit_transform(samples_3d)
    return pca, samples_2d


@app.cell
def _(go, make_subplots, np, pca, samples_2d, samples_3d):
    pc_vectors = (pca.components_.T * np.sqrt(pca.explained_variance_)).T

    # Create the figure with two subplots
    fig2 = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "scatter3d"}, {"type": "scatter"}]],
    )

    # Left subplot: 2D scatter plot of PCA-transformed data
    fig2.add_trace(
        go.Scatter(x=samples_2d[:, 0], y=samples_2d[:, 1], mode="markers", name="2d points"),
        row=1,
        col=2,
    )

    # Right subplot: 3D scatter plot of original data
    fig2.add_trace(
        go.Scatter3d(
            x=samples_3d[:, 0],
            y=samples_3d[:, 1],
            z=samples_3d[:, 2],
            mode="markers",
            marker=dict(size=3, opacity=0.3),
            name="3d points",
        ),
        row=1,
        col=1,
    )

    # Right subplot: Add principal component vectors in 3D
    origin = np.mean(samples_3d, axis=0)  # Center of the ellipsoid
    for k in range(2):
        fig2.add_trace(
            go.Scatter3d(
                x=[origin[0], origin[0] + pc_vectors[k, 0] * 3],
                y=[origin[1], origin[1] + pc_vectors[k, 1] * 3],
                z=[origin[2], origin[2] + pc_vectors[k, 2] * 3],
                mode="lines",
                line=dict(color="red", width=5),
                name=f"PC{k + 1}",
            ),
            row=1,
            col=1,
        )

    fig2
    return fig2, k, origin, pc_vectors


@app.cell
def _(mo):
    mo.md(
        r"""
        I vettori rappresentati in rosso nello spazio 3d (figura a sinistra) sono detti _principal components_. Sfruttando l'implementazione di PCA offerta da `scikit-learn` non solo abbiamo identificato questi vettori, ma abbiamo anche proiettato la nuvola di punti sul piano da essi identificato (figura a destra); ottenendo così la nostra prima __dimensionality reduction__ (da $d=3$ a $d'=2$).

        Quando sopra può essere generalizzato a casi con più alta dimensionalità. Questa tecnica permette sempre di proiettare i sample di dimensione arbitraria in spazi a bassa dimensione preservando il più possibile la struttura _globale_ della nuvola di punti originale.

        /// tip | Per individuare le componenti principali, PCA sfrutta una tecnica di fattorizzazione nota come Singular value decomposition (SVD). Questa fattorizzazione permette di scomporre una matrice di dati di training $X$ come prodotto tra $U \Sigma V^T$ dove $V$ contiene i vettori che formano le _principal components_ e $\Sigma$ è una matrice simmetrica che riporta sulla diagonale la misura della varianza catturata dall'i-esima _principal component_. Come esercizio a casa, prova a scrivere una tua implementazione di PCA che sfrutti [np.linalg.svd](https://numpy.org/doc/2.2/reference/generated/numpy.linalg.svd.html).
        """
    )
    return


if __name__ == "__main__":
    app.run()
