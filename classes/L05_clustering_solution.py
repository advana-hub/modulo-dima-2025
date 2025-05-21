# /// script
# dependencies = [
#   "pandas==2.2.3",
#   "pyarrow==18.1.0",
#   "marimo>=0.11.18",
#   "plotly==6.0.1",
#   "drawdata==0.3.8",
#   "scikit-learn==1.6.1",
#   "numpy==2.2.5",
#   "scipy==1.15.3",
#   "loguru==0.7.3",
#   "ipython==9.2.0",
# ]
# ///

import marimo

__generated_with = "0.13.11"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.express as px
    import pandas as pd
    from drawdata import ScatterWidget
    import json
    from loguru import logger
    from sklearn.base import BaseEstimator
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.figure_factory as ff
    from functools import reduce
    from collections import Counter
    return (
        BaseEstimator,
        Counter,
        ff,
        logger,
        make_subplots,
        mo,
        np,
        pd,
        px,
        reduce,
    )


@app.cell
def _(mo):
    mo.md(r"""# Clustering""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Definizione

    Il [clustering](https://en.wikipedia.org/wiki/Cluster_analysis) si può definire come segue:

    > azione di raggruppare un insieme di oggetti in vari gruppi (clusters) in maniera tale che oggetti appartenente allo stesso gruppo siano più "simili" tra loro rispetto che a quelli negli altri gruppi

    Tre aspetti fondamentali del clustering sono i seguenti:

    - l'apprendimento di un modello avviene in maniera **non supervisionata**, ovvero non si ha un training set a disposizione in cui esistono etichette che permettono di associare un oggetto ad un gruppo (se così fosse, parleremmo di un problema, supervisionato, di _classificazione_);
    - non esiste quindi una "verità" di riferimento con cui valutare in maniera univoca e oggettiva la bontà di un modello di clustering: spesso la valutazione dipende in maniera utilitaristica da come si vuole utilizzare il modello e avviene insieme a qualche esperto del contesto da cui provengono i dati;
    - ogni modello utilizza una sua definizione di "similarità" tra oggetti, che lo caratterizza.

    L'ipotesi, come spesso accade nell'analisi dati, è che esista un processo (fisico, industriale, sociale, informatico, etc.), completamente o parzialmente ignoto, che ha generato i dati e rispetto al quale essi possono essere raggruppati: lo scopo del clustering è ricostruire i gruppi pur senza avere piena conoscenza del processo generatore.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    /// tip | Draw your data

    Copiando in una cella il codice sotto ed eseguendolo potrete letteralmente _disegnare_ un dataset su cui sperimentare i vari algoritmi di clustering!

    ```python
    widget = mo.ui.anywidget(ScatterWidget())
    widget
    ```

    ///
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""Definiamo una funzione utile per visualizzare dati e output dei modelli della lezione.""")
    return


@app.cell
def _(BaseEstimator, pd, px):
    def plot(data: pd.DataFrame,
             x: str = "x",
             y: str = "y",
             color_by: str | None = None,
             fitted_model: BaseEstimator | None = None
            ) -> None:
        fig = px.scatter(
            data,
            x=x,
            y=y,
            color=color_by,
            color_discrete_map={"-1": "gray"}
        )
        if fitted_model is not None:
            centroids = getattr(fitted_model, "cluster_centers_", None)
            if centroids is None:
                centroids = fitted_model.medoids_        
            fig.add_scatter(
                x=centroids[:, 0],
                y=centroids[:, 1],
                mode="markers",
                name="centroids",
                marker=dict(
                    symbol="x",
                    size=20,
                    color="black",
                    line=dict(width=2, color='white')
                ),
            )
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1))
        return fig
    return (plot,)


@app.cell
def _(make_subplots, pd, px):
    def stack_scatter(data: pd.DataFrame, color_by: str, d3: bool = False, add_text: bool = False):

        handler = "scatter_3d" if d3 else "scatter"

        # Create a subplot with 1 row and 2 columns
        fig = make_subplots(
            rows=1,
            cols=2, specs=[[{'type': handler.replace("_", "")}, {'type': handler.replace("_", "")}]]
        )    
        # Create first scatter3d plot
        kwargs = dict(
            data_frame=data,
            x="pc1",
            y="pc2",
            color="stars",
            hover_data="stars",        
        )
        if d3: kwargs["z"] = "pc3"
        fig1 = getattr(px, handler)(**kwargs)
        fig.add_trace(fig1.data[0], row=1, col=1)

        # Create second scatter3d plot
        hover_data = ["stars", "categories"]
        if add_text: hover_data.append("text")
        kwargs = dict(
            data_frame=data.assign(text=data["text"].str.replace(".", "<br>")),
            x="pc1",
            y="pc2",
            color=color_by,
            color_discrete_map={"-1": "gray"},
            hover_data=hover_data
        )
        if d3: kwargs["z"] = "pc3"
        fig2 = getattr(px, handler)(**kwargs)
        for trace in fig2.data:
            fig.add_trace(trace, row=1, col=2)
        return fig
    return (stack_scatter,)


@app.cell
def _(ff):
    def plot_starts_dist(df_, cluster_label: str):
        hist_data = [df_.loc[df_[cluster_label] == j, "stars"] for j in df_[cluster_label].unique()]
        group_labels = [f"Cluster {j}" for j in df_[cluster_label].unique()]   
        return ff.create_distplot(hist_data, group_labels, bin_size=1, show_rug=False, show_curve=False)
    return (plot_starts_dist,)


@app.cell
def _(Counter, pd, px, reduce):
    def plot_categories_by_cluster(data: pd.DataFrame):
        df_cat = pd.DataFrame()
        for i, row in data.groupby("hdbscan_cluster").agg({
                "categories": lambda x: Counter(tuple(reduce(lambda x1, x2: x1 + x2, x.str.split(", "))))
            }).iterrows():
            if row.name != "-1":
                df_cat = pd.concat(
                    [
                        df_cat,
                        (
                            pd.DataFrame(row["categories"], index=["n_samples"])
                            .transpose()
                            .reset_index()
                            .rename({"index": "category"}, axis="columns")
                            .assign(cluster=row.name)
                    )
                ])
        return px.bar(df_cat, x="cluster", color="category", y="n_samples")
    return (plot_categories_by_cluster,)


@app.cell
def _(pd):
    sample = pd.read_json("../data/clustering_sample.json")
    return (sample,)


@app.cell
def _(sample):
    sample.shape
    return


@app.cell
def _(plot, sample):
    plot(sample)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## I modelli in scikit-learn

    Come sempre scikit-learn è il nostro riferimento, e possiamo trovare numerosi modelli di [clustering](https://scikit-learn.org/stable/modules/clustering.html), tutti implementati come estimators con i consueti metodi fit e predict.

    La similarità, in questo contesto, è implementata attraverso una [_metrica_](https://en.wikipedia.org/wiki/Metric_space#Definition), ad esempio quella euclidea.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # K-means

    Uno dei più semplici modelli di clustering si chiama [K-means](https://en.wikipedia.org/wiki/K-means_clustering), il cui nome spiega già parte del funzionamento. Per determinare $K$ clusters, infatti, il modello:

    1. inizializza $K$ punti detti _centroidi_, rappresentanti di ciascun cluster;
    2. assegna ciascun punto del dataset al cluster che permette di minimizzare la varianza intra-clusters (intuitivamente: ogni punto viene assegnato al cluster il cui centroide è più vicino rispetto alla **metrica euclidea**);
    3. aggiorna la definizione dei centroidi come baricentro dei clusters (ovvero, effettuando la _media_ delle relative coordinate);
    4. itera i punti (2) e (3) fino a convergenza rispetto ad un determinato criterio.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    /// tip | In formule
    Sostanzialmente il K-means si può formulare come problema di minimo.

    Dato un insieme $X=\{x_i\}_{i=1}^N$ di punti $x_i\in\mathbb{R}^d$ da raggruppare in $2\leq K\leq N$ clusters, si cerca una partizione $\mathcal{C}=\{C_1, \dots, C_K\}$ di $X$ che risolva il seguente problema:
    $$\argmin_\mathcal{C}\sum_{j=1}^K\sum_{x_i\in C_j}\|x_i - \mu_j\| _2^2$$
    ///
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## KMeans in scikit-learn""")
    return


@app.cell
def _(mo):
    n_clusters = mo.ui.slider(start=2, stop=10, step=1, value=2, label="n_clusters")
    n_clusters
    return (n_clusters,)


@app.cell
def _(n_clusters, plot, sample):
    from sklearn.cluster import KMeans

    sklearn_kmeans = KMeans(n_clusters=n_clusters.value)
    sample["sklearn_label"] = sklearn_kmeans.fit_predict(sample[["x", "y"]]).astype(str)
    plot(sample, color_by="sklearn_label", fitted_model=sklearn_kmeans)
    return (KMeans,)


@app.cell
def _(mo):
    mo.accordion({
        "K-means e tassellazioni": """/// tip | Se a qualcuno il risultato del K-means avesse ricordato la tassellazione di Voronoi...
        ...è proprio così! La partizione costituita dai clusters individuati con il K-means è infatti equivalente alla tassellazione di Voronoi indotta dai centroidi (baricentri, medie) dei clusters.
        ///"""
    })
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Iperparametri

    La maggior parte dei modelli di machine learning richiede di impostare il valore di alcuni iperparametri prima di poter avviare la fase di apprendimento vera e propria, e il K-means non fa eccezione.

    L'impatto di alcuni tra tali iperparametri sulla qualità del risultato è spesso significativo, ed esistono quindi vari approcci per stabilirne il valore: euristiche, ricerca esaustive (brute-force), campionamenti più o meno "smart", mix di "art and science", ...
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### `n_clusters`

    Una caratteristica che difficilmente passa inosservata del K-means è presenza del **numero di clusters** tra i suoi iperparametri. A seconda del dataset di interesse, può non essere semplice/scontato determinare tale numero "a priori", ed è quindi utile avere a disposizione dei metodi per stimarlo "a partire dai dati".

    Vediamo in particolare un approccio euristico visivo basato sul [silhouette score](https://scikit-learn.org/stable/modules/clustering.html#silhouette-coefficient).
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Il **silhouette score** è definito per ogni sample $x_i\in X$ attraverso due grandezze ad esso associate, ovvero:

    - la media $a_i$ delle distanze tra $x_i$ e i punti del medesimo cluster;
    - la media $b_i$ delle distanze tra $x_i$ e i punti del cluster _più vicino_ dopo quello di appartenenza.

    In formula:
    $$s_i = \frac{b_i-a_i}{\max(a_i, b_i)}$$

    Tale score si estende all'intero dataset $X$ semplicemente considerando la media degli score dei singoli campioni.
    """
    )
    return


@app.cell
def _(mo):
    mo.accordion({
        "Come si interpreta geometricamente il silhouette score?": """/// note | Nota
        Innanzitutto è semplice notare che $s_i\\in [-1,1]$, e successivamente interpretarne il significato geometrico alla luce della definizione di $a_i$ e $b_i$ e la loro relazione:

        - se $s_i \\approx 0$, significa che $x_i$ è vicino alla frontiera tra il proprio cluster ed il successivo più vicino;
        - se $s_i \\approx 1$, significa che $x_i$ è molto più vicino al proprio cluster che non al successivo candidato;
        - se $s_i << 0$, significa che $x_i$ potrebbe essere stato assegnato al cluster "sbagliato" (cioè non al suo più vicino).
        ///"""
    })
    return


@app.cell
def _():
    from sklearn.metrics import silhouette_samples, silhouette_score
    return silhouette_samples, silhouette_score


@app.cell
def _(pd, px):
    def plot_silhouette(n_clusters, sample_silhouette_values, cluster_labels, silhouette_avg):
        fig = None
        for j in range(n_clusters):
            if fig is None:
                fig = px.line(pd.Series(sample_silhouette_values[cluster_labels == j]).sort_values().reset_index(drop=True).to_frame(f"C{j+1}"))
            else:
                tmp = (
                    pd.Series(sample_silhouette_values[cluster_labels == j])
                    .sort_values()
                    .reset_index(drop=True)
                    .to_frame("y")
                    .reset_index()
                    .rename({"index": "x"}, axis=1)
                )
                fig.add_scatter(x=tmp["x"], y=tmp["y"], name=f"C{j+1}")
                fig.add_hline(silhouette_avg, line_width=1, line_dash="dash", line_color="white")
        return fig
    return (plot_silhouette,)


@app.cell
def _(
    KMeans,
    logger,
    plot_silhouette,
    sample,
    silhouette_samples,
    silhouette_score,
):
    range_n_clusters = [2, 3, 4, 5]
    figs = []

    for _n_clusters in range_n_clusters:
        clusterer = KMeans(n_clusters=_n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(sample[["x", "y"]])
        silhouette_avg = silhouette_score(sample[["x", "y"]], cluster_labels)
        logger.info(f"Silhouette with {_n_clusters}: {silhouette_avg}")
        sample_silhouette_values = silhouette_samples(sample[["x", "y"]], cluster_labels)
        figs.append(plot_silhouette(_n_clusters, sample_silhouette_values, cluster_labels, silhouette_avg))
    return (figs,)


@app.cell
def _(figs):
    figs
    return


@app.cell
def _(mo):
    mo.md(r"""## Feature engineering""")
    return


@app.cell
def _(pd, plot):
    sample2 = pd.read_json("../data/clustering_sample2.json")
    plot(sample2)
    return (sample2,)


@app.cell
def _(KMeans, plot, sample2):
    model = KMeans(n_clusters=2)
    sample2["naive_label"] = model.fit_predict(sample2[["x", "y"]]).astype(str)
    plot(sample2, color_by="naive_label", fitted_model=model)
    return (model,)


@app.cell
def _(model, np, plot, sample2):
    x_c, y_c = (400, 250)
    sample2["rho"] = np.sqrt((sample2["x"] - x_c)**2 + (sample2["y"] - y_c)**2)
    sample2["theta"] = np.degrees(np.arctan2(sample2["y"], sample2["x"]))
    sample2["polar_label"] = model.fit_predict(sample2[["rho", "theta"]]).astype(str)
    plot(sample2, color_by="polar_label")
    return


@app.cell
def _(model, plot, sample2):
    plot(sample2, x="rho", y="theta", color_by="polar_label", fitted_model=model)
    return


@app.cell
def _(mo):
    mo.md(r"""## Sul nostro dataset""")
    return


@app.cell
def _(pd):
    df = pd.read_parquet("../data/data.parquet")[["text", "stars", "categories"]]
    return (df,)


@app.cell
def _():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import PCA
    from sklearn.pipeline import Pipeline
    return PCA, Pipeline, TfidfVectorizer


@app.cell
def _(mo):
    n_components = mo.ui.slider(start=3, stop=40, step=1, value=3, label="n_components")
    n_components
    return (n_components,)


@app.cell
def _(PCA, Pipeline, TfidfVectorizer, df, n_components, pd):
    tfidf = TfidfVectorizer(lowercase=True, strip_accents="unicode", stop_words="english", max_features=500)
    pca = PCA(n_components=n_components.value)
    pipeline = Pipeline([('vectorizer', tfidf), ('reducer', pca)])
    df_ = df.join(
        pd.DataFrame(
            pipeline.fit_transform(df["text"]),
            columns=[f"pc{j+1}" for j in range(n_components.value)]
        )
    )
    return (df_,)


@app.cell
def _(KMeans, df_):
    kmeans = KMeans(n_clusters=2)
    df_["kmeans_cluster"] = kmeans.fit_predict(df_[[c for c in df_.columns if c.startswith("pc")]]).astype(str)
    return


@app.cell
def _(df_):
    df_
    return


@app.cell
def _(TfidfVectorizer, df_):
    cluster_0_repr = set(
        TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            stop_words="english",
            ngram_range=(3, 3),
            max_features=50
        )
        .fit(df_.loc[df_["kmeans_cluster"] == "0", "text"])
        .get_feature_names_out()
    )
    return (cluster_0_repr,)


@app.cell
def _(TfidfVectorizer, df_):
    cluster_1_repr = set(
        TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            stop_words="english",
            ngram_range=(3, 3),
            max_features=50
        )
        .fit(df_.loc[df_["kmeans_cluster"] == "1", "text"])
        .get_feature_names_out()
    )
    return (cluster_1_repr,)


@app.cell
def _(cluster_0_repr, cluster_1_repr):
    sorted(cluster_0_repr.difference(cluster_1_repr))
    return


@app.cell
def _(cluster_0_repr, cluster_1_repr):
    sorted(cluster_1_repr.difference(cluster_0_repr))
    return


@app.cell
def _(df_, plot_starts_dist):
    plot_starts_dist(df_, cluster_label="kmeans_cluster")
    return


@app.cell
def _(df_, stack_scatter):
    stack_scatter(df_, color_by="kmeans_cluster")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    /// warning | Limiti del KMeans
    I limiti principali del KMeans sono:

    1. la necessità di definire in input e a priori la numerosità dei clusters;
    2. l'utilizzo della sola distanza euclidea come metrica di similarità tra punti;
    3. la sensibilità agli outliers;
    4. curse of dimensionality.

    ///
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # HDBSCAN

    HDBSCAN è un modello di clustering più avanzato del KMeans il cui nome sta per "**Hierarchical Density-Based Spatial Clustering of Applications with Noise**".
    """
    )
    return


@app.cell
def _(mo):
    mo.accordion(items={"Qualche spunto intuitivo sul suo funzionamento (più dettagli [qui](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html#))": """
    /// tip | 1. Trasformazione dello spazio
    L'idea intuitiva di questo primo step è stabilire una metrica di distanza, da questa derivare un concetto di _densità_ che permetta di segmentare lo spazio in zone con tanti punti "molto" vicini tra loro (rispetto alla distanza scelta) vs zone con pochi punti lontani tra loro, e infine esasperare le distanze tra i punti delle zone a bassa densità (sia tra loro, sia rispetto alle zone ad alta densità) -> questo permette di individuare gli outlier e "allontanarli" rispetto al resto dei punti, di fatto definendo una nuova distanza indotta dalla precedente detta **$k$-mutual reachability distance**.
    ///

    /// tip | 2. Costruzione del grafo
    In questo step si definisce un grafo in cui i nodi sono i punti del dataset e, per ciascuna coppia di nodi, si aggiunge un arco con peso pari alla relativa $k$-mutual reachability distance, e di questo grafo si costruisce il [minimum spanning tree (MST)](https://en.wikipedia.org/wiki/Minimum_spanning_tree). Così facendo si ottiene un secondo grafo con le seguenti proprietà:

    1. rimuovendo un qualunque edge dal MST, esso si sconnette (in quanto _tree_);
    2. non esistono archi con peso minore (ovvero, coppie di nodi a distanza inferiore) di quelli appartenenti al MST per ripristinare la connettività.
    ///

    /// tip | 3. Costruzione di una gerarchia di componenti connesse
    A partire dal MST si costruisce una gerarchia di componenti connesse:

    1. si ordinano gli archi del MST per peso (distanza tra i punti) crescente;
    2. per ogni nuovo edge:
        1. se entrambi i nodi non fanno parte di alcun cluster preesistente, si crea con essi un nuovo cluster;
        2. se esattamente un nodo fa già parte di un cluster, si uniscono entrambi i nodi dell'edge a tale cluster;
        3. se entrambi i nodi fanno già parte di un cluster, si uniscono tali cluster tra loro.

    Questo step crea una struttura gerarchica nel senso della distanza, da cui è possibile estrarre dei clusters in corrispondenza di un dato valore di soglia della distanza.
    ///

    /// tip | 4. Compressione della gerarchia filtrando i clusters troppo piccoli
    In questo step, tutti i cluster troppo piccoli (ovvero, con troppi pochi punti al loro interno) ai livelli "bassi" della gerarchia (ovvero, relativi a punti tra loro "vicini", con distanza "piccola") vengo uniti tra loro, condensando la gerarchia granulare in una a più alto livello.
    ///

    /// tip | 5. Estrazione dei clusters definitivi dalla struttura compressa
    A partire dalla struttura gerarchica compressa, si selezionano i clusters più _stabili_, ovvero la cui presenza è più "costante" a vari livelli di threshold di distanza.
    ///

    Per ulteriori dettagli, vedere [qui](https://lanselin.github.io/introbook_vol1/HDBSCAN.html)."""})
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Iperparametri

    ### metric

    Indica la metrica iniziale del punto (1) con cui viene valutata la distanza tra i punti.

    ### min_cluster_size

    Indica il numero minimo di campioni assegnati ad un "gruppo di punti" perchè tale gruppo venga "promosso" a cluster.

    ### min_samples

    Corrisponde al numero $k$ di punti che definiscono l'intorno della _k-mutual reachability distance_ del punto (1). Intuitivamente, maggiore è `min_samples` e maggiore è la distanza tra punti outliers e zone ad alta densità.
    """
    )
    return


@app.cell
def _():
    from sklearn.cluster import HDBSCAN
    from sklearn.metrics.pairwise import PAIRWISE_DISTANCE_FUNCTIONS
    return (HDBSCAN,)


@app.cell
def _(mo):
    supported_metrics = sorted([    
        'l2',
        'l1',
        'cosine',
    ])

    metric = mo.ui.dropdown(options=supported_metrics, label="metric", value="l2")
    min_cluster_size = mo.ui.slider(start=5, stop=300, step = 1, label="min_cluster_size", value=5)
    return metric, min_cluster_size


@app.cell
def _(metric, min_cluster_size, mo):
    min_samples = mo.ui.slider(start=5, stop=300, step = 1, label="min_samples", value=min_cluster_size.value)

    metric, min_cluster_size, min_samples
    return (min_samples,)


@app.cell
def _(HDBSCAN, metric, min_cluster_size, min_samples, plot, sample):
    hdbscan = HDBSCAN(
        store_centers="medoid",
        metric=metric.value,
        min_cluster_size=min_cluster_size.value,
        min_samples=min_samples.value,
    )

    sample["hdbscan_label"] = hdbscan.fit_predict(sample[["x", "y"]]).astype(str)
    plot(sample, color_by="hdbscan_label", fitted_model=hdbscan)
    return


@app.cell
def _(metric, min_cluster_size, min_samples):
    metric, min_cluster_size, min_samples
    return


@app.cell
def _(HDBSCAN, metric, min_cluster_size, min_samples, plot, sample2):
    hdbscan2 = HDBSCAN(
        store_centers="medoid",
        metric=metric.value,
        min_cluster_size=min_cluster_size.value,
        min_samples=min_samples.value,
    )

    sample2["hdbscan_label"] = hdbscan2.fit_predict(sample2[["x", "y"]]).astype(str)
    plot(sample2, color_by="hdbscan_label", fitted_model=hdbscan2)
    return


@app.cell
def _(mo):
    mo.md(r"""## Sul nostro dataset""")
    return


@app.cell
def _(metric, min_cluster_size, min_samples, n_components):
    n_components, metric, min_cluster_size, min_samples
    return


@app.cell
def _(HDBSCAN, df_, metric, min_cluster_size, min_samples, stack_scatter):
    hdbscan3 = HDBSCAN(
        store_centers="medoid",
        metric=metric.value,
        min_cluster_size=min_cluster_size.value,
        min_samples=min_samples.value,
    ) 
    df_["hdbscan_cluster"] = hdbscan3.fit_predict(df_[[c for c in df_.columns if c.startswith("pc")]]).astype(str)
    stack_scatter(df_, color_by="hdbscan_cluster")
    return


@app.cell
def _(df_, plot_categories_by_cluster):
    plot_categories_by_cluster(df_)
    return


@app.cell
def _(mo):
    mo.md(r"""# Homework""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Implementare il KMeans!

    Per implementarlo ti suggeriamo di "adottare" l'interfaccia di scikit-learn, e farlo sfruttando un concetto base della programmazione ad oggetti (paradigma [ben supportato](https://docs.python.org/3/tutorial/classes.html#) in Python), ovvero la [class inheritance](https://en.wikipedia.org/wiki/Inheritance_(object-oriented_programming)).

    In sostanza, definire una classe che _estende_ il concetto di "estimator" di scikit-learn.

    Sotto troverai lo pseudocodice da cui partire; una volta implementato il KMeans, sarà poi necessario testarlo sul DataFrame `sample` e visualizzarne i risultati tramite la funzione `plot`.

    ### Pseudocodice

    ```python
    class BasicKMeans(BaseEstimator):

        def __init__(self, # l'argomento "self" indica un'istanza della classe che stai definendo,
                           # ed è utile per condividere attributi tra i metodi di una classe
                     *,
                     n_clusters: int = 3,
                     ... # definisci qui gli altri iperparametri del modello
            ) -> None:
            self.n_clusters = n_clusters
            ... # e salva il valore degli altri iperparametri sul self!

        def fit(self, X: pd.DataFrame) -> "BasicKMeans":
            \"""Questo metodo è sostanzialmente un'euristica per approssimare "al meglio" 
            la soluzione al problema di ottimizzazione tramite cui è definito il KMeans.
            Output: il metodo `fit` non deve restituire alcun risultato, ma salvare sul `self`
            le informazioni relative ai centroidi individuati come "baricentro" dei clusters.
            \"""
            # 1. inizializzo i centroidi in maniera randomica (ad esempio, selezionando `n_clusters`
            # punti dell'input X)
            # 2. avvio ciclo while (o analogo ciclo for illimitato, tramite `itertools.count`)
            # 2.1 assegno ciascun punto di X al cluster con centroide più vicino
            # 2.2 ricalcolo i centroidi come baricentri dei cluster
            # 2.3 verifico al convergenza dell'algoritmo, ovvero se
            # - i centroidi non sono cambiati in maniera significativa rispetto all'iterazione precedente
            # - oppure se ho raggiunto un numero molto elevato di iterazioni
            # -> allora interrompo il ciclo while
            # 3. i centroidi da salvare sul self sono quelli dell'ultima iterazione
            return self

        def predict(self, X: pd.DataFrame) -> pd.DataFrame:
            \"""In questo metodo si deve assegnare ciascun punto del DataFrame X di input
            ad uno dei clusters individuati dal metodo `fit`.
            Hint: ciascun punto va assegnato al cluster il cui centroide risulta più vicino.
            Output: il DataFrame in uscita dovrà avere una nuova colonna "label" in cui per 
            ogni punto è riportato l'ID del cluster corrispondente.
            \"""
            # 1. per ogni campione (ovvero punto, riga) di X
            # 2. calcolo la distanze dai centroidi individuati dal `fit` (e salvati sul `self`)
            # 3. assegno il punto al cluster con il centroide più vicino
            # 4. salvo l'etichetta del cluster in una colonna dedicata
            return ...
    ```
    """
    )
    return


@app.cell
def _(BaseEstimator, logger, np, pd):
    import itertools
    from scipy.spatial.distance import euclidean

    class BasicKMeans(BaseEstimator):

        def __init__(self,
                     *,
                     n_clusters: int = 8,
                     init: str | list = "random",
                     max_iter: int = 300,
                     tol: float = 1e-4,
                     verbose: int = 0,
                     random_state: int | None = None
            ) -> None:
            self.n_clusters = n_clusters
            self.init = init
            self.max_iter = max_iter
            self.tol = tol
            self.verbose = verbose
            self.random_state = random_state

        def fit(self, X: pd.DataFrame):
            centroids = X.sample(self.n_clusters, random_state=self.random_state).values if self.init == "random" else self.init
            self._log(f"Centroidi inizializzati: {centroids}")
            converged = False
            for n in itertools.count(start=1):
                self._log(f"Iterazione: {n}")
                clusters = [[] for _ in range(self.n_clusters)]

                for i, point in X.iterrows():
                    distances_to_each_centroid = [euclidean(point, centroid) for centroid in centroids]
                    cluster_assignment = np.argmin(distances_to_each_centroid)
                    clusters[cluster_assignment].append(i)

                new_centroids = np.array([
                    np.mean(X.loc[cluster], axis=0)            
                    for cluster in clusters
                ])
                self._log(f"Centroidi aggiornati: {new_centroids}")
                delta_centroids = abs(new_centroids - centroids).max()
                converged = delta_centroids < self.tol
                if converged:
                    self._log(f"Tolleranza raggiunta: {delta_centroids}")
                centroids = new_centroids
                max_iter_reached = n == self.max_iter
                if max_iter_reached:
                    self._log("Max iter raggiunto.")
                if converged or max_iter_reached:                
                    self.labels_ = self._reshape_clusters(clusters)
                    self.cluster_centers_ = centroids
                    break
            self.is_fitted_ = True
            return self

        def predict(self, X: pd.DataFrame) -> pd.DataFrame:
            clusters = [[] for _ in range(self.n_clusters)]
            for i, point in X.iterrows():
                distances_to_each_centroid = [euclidean(point, centroid) for centroid in self.cluster_centers_]
                cluster_assignment = np.argmin(distances_to_each_centroid)
                clusters[cluster_assignment].append(i)
            return self._reshape_clusters(clusters)

        def fit_predict(self, X: pd.DataFrame) -> pd.DataFrame:
            self.fit(X)
            return self.predict(X)

        def _log(self, message: str) -> None:
            if self.verbose:
                logger.info(message)

        @staticmethod
        def _reshape_clusters(clusters: list) -> pd.DataFrame:
            df = pd.DataFrame()
            for label, indices in enumerate(clusters):
                df = pd.concat([df, pd.Series(indices).to_frame("index").assign(label=lambda _: label)])
            return df.set_index("index").sort_index()
    return (BasicKMeans,)


@app.cell
def _(BasicKMeans, plot, sample):
    basic_kmeans = BasicKMeans(n_clusters=4)
    sample["basic_label"] = basic_kmeans.fit_predict(sample[["x", "y"]]).astype(str)
    plot(sample, color_by="basic_label", fitted_model=basic_kmeans)
    return


if __name__ == "__main__":
    app.run()
