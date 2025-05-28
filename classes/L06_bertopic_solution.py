# /// script
# dependencies = [
#   "umap-learn==0.5.7",
#   "pyarrow==18.1.0",
#   "marimo>=0.11.18",
#   "plotly==5.24.1",
#   "drawdata==0.3.7",
#   "scikit-learn==1.6.1",
#   "numpy==2.2.3",
#   "scipy==1.15.2",
#   "loguru==0.7.3",
#   "bertopic==0.17.0",
#   "hdbscan==0.8.40",
#   "pandas==2.2.3",
#   "matplotlib==3.10.3",
#   "datamapplot>=0.1",
# ]
# ///

import marimo

__generated_with = "0.13.11"
app = marimo.App(width="full")


@app.cell
def _():
    import matplotlib
    import marimo as mo
    import pandas as pd
    import umap

    from bertopic import BERTopic
    from hdbscan import HDBSCAN
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.pipeline import make_pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans
    return BERTopic, CountVectorizer, HDBSCAN, TfidfVectorizer, mo, pd, umap


@app.cell
def _(mo):
    mo.md(r"""# Topic Modeling""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Le recensioni

    Alcune domande "business":

    1. di quali _argomenti_ parlano le recensioni?
    2. come possiamo raggruppare le recensioni _simili_ tra loro?
    3. il testo di una recensione contiene informazioni per _stimare_ il punteggio numerico della recensione stessa? _(a questa proveremo a rispondere la prossima lezione)_
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Definizione


    Il [topic modeling](https://it.wikipedia.org/wiki/Topic_model) si può definire come segue:
    è una branca dell'elaborazione del linguaggio naturale (NLP) che consente agli utenti finali di identificare temi/argomenti (topic) all'interno di una collezione di documenti. Ha applicazioni in molteplici settori industriali per il text mining (l'estrazione di conoscenza da testi) e per ottenere informazioni (o spunti) rilevanti dai dati testuali.

    O più semplicemente:

    > scoprire gli argomenti (topic) astratti che "emergono" da una raccolta di documenti

    Qui possiamo vedere come tutti gli argomenti analizzati in precedenza tornino utili:

    - Text Embeddings

    - Dimensionality Reduction

    - Feature engineering

    - Clustering
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Cos'è un topic?

    Quindi cos'è un topic in parole semplice --> gruppo di documenti affini dal punto di vista semantico (ad uno o più livelli di astrazione)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # BERTopic

    Ogni topic in BERTopic corrisponde a un cluster di documenti che sono semanticamente simili. Un topic può essere rappresentato in molti modi, ad esempio tramite le parole che si trovano più frequentemente.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Modularità

    Una caratteristica fondamentale di BERTopic è la sua architettura modulare. Questo significa che non è un algoritmo monolitico, ma piuttosto una pipeline composta da diverse fasi di elaborazione indipendenti. Per ciascuna di queste fasi, BERTopic ti offre la flessibilità di scegliere e configurare i modelli da impiegare.

    Questa possibilità di selezione e personalizzazione dei componenti rende le tue scelte molto simili alla definizione degli iperparametri in un tradizionale modello di machine learning. Puoi sperimentare con diverse combinazioni per ottimizzare i risultati in base al tuo specifico dataset e ai tuoi obiettivi.
    """
    )
    return


@app.cell
def _(mo):
    mo.image(src="https://maartengr.github.io/BERTopic/algorithm/modularity.svg")
    return


@app.cell
def _(pd):
    df = pd.read_parquet(r"..\data\data.parquet").sample(1000)
    docs = df["text"].tolist()
    return (docs,)


@app.cell
def _(HDBSCAN, TfidfVectorizer, UMAP, docs):
    vectorizer = TfidfVectorizer(max_features=500, stop_words="english")
    embeddings = vectorizer.fit_transform(docs)

    # reducer = PCA(n_components=20)
    reducer = UMAP(n_components=20)
    # clusterer = KMeans(n_clusters=10)
    clusterer = HDBSCAN()
    return clusterer, embeddings, reducer, vectorizer


@app.cell
def _(
    BERTopic,
    CountVectorizer,
    clusterer,
    docs,
    embeddings,
    reducer,
    vectorizer,
):
    topic_model = BERTopic(
        embedding_model=vectorizer,
        umap_model=reducer,
        hdbscan_model=clusterer,
        vectorizer_model=CountVectorizer(stop_words="english")
    )
    topics, _ = topic_model.fit_transform(docs, embeddings)
    return topic_model, topics


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Algoritmo

    BERTopic presuppone che i documenti contenenti lo stesso tema (topic) siano semanticamente simili.

    La generazione dei temi (topic) prevede tre fasi:

    1. Ogni documento viene convertito nella sua rappresentazione di embedding (o vettoriale) utilizzando il framework Sentence-BERT(SBERT)ciò permette la conversione di frasi e paragrafi in rappresentazioni vettoriali dense usando modelli linguistici pre-addestrati.
    2. La dimensionalità degli embedding risultanti viene ridotta per ottimizzare il processo di clustering utilizzando la tecnica UMAP (Uniform Manifold Approximation and Projection). Questa tecnica è impiegata poiché è stato dimostrato che preserva meglio le caratteristiche locali e globali dei dati ad alta dimensionalità nelle dimensioni proiettate inferiori.
    3. Successivamente, i cluster vengono ottenuti da questi embedding ridotti tramite HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise).I temi (topic) vengono estratti dai cluster così formati utilizzando una variazione personalizzata del TF-IDF basata sulle classi (class-based TF-IDF).
    """
    )
    return


@app.cell
def _(mo):
    mo.accordion({"Approfondimento su cTF-IDF": """
    Il TF-IDF classico è dato da:
    ![](https://miro.medium.com/v2/resize:fit:720/format:webp/1*D7YhrLFR2w1GtwvMZh1kjg.jpeg)

    La suddetta equazione è leggermente modificata per il TF-IDF basato sulle classi. La classe c rappresenta insieme dei documenti di ciascun cluster, concatenati in un unico documento per cluster.

    ![](https://miro.medium.com/v2/resize:fit:720/format:webp/1*rC_gFLEBBv_uRyxxuljSIw.jpeg)

    Questo approccio permette di generare distribuzioni termine-tema per ogni cluster di documenti. Il numero di temi può essere ridotto a un valore specificato dallutente, fondendo iterativamente la rappresentazione TF-IDF (basata sulle classi) del tema meno frequente con quella del tema ad esso più simile."""})
    return


@app.cell
def _(mo):
    mo.md(r"""# Interpretazione dei topic""")
    return


@app.cell
def _(mo):
    mo.md(r"""## Parole caratterizzanti""")
    return


@app.cell
def _(topic_model):
    topic_model.visualize_barchart()
    return


@app.cell
def _(mo):
    mo.md(r"""## Gerarchia tra topic""")
    return


@app.cell
def _(topic_model):
    topic_model.visualize_hierarchy()
    return


@app.cell
def _(mo):
    mo.md(r"""## Distribuzione topic vs documenti""")
    return


@app.cell
def _(mo):
    mo.md(r"""Possiamo poi considerare la matrice $n×m$, dove $n$ rappresenta i documenti e $m$ gli argomenti e visualizzare la "distribuzione degli argomenti" in un documento, ovvero capire con che probabilità ciascun documento può essere attribuito ad ogni topic.""")
    return


@app.cell
def _(docs, topic_model):
    topic_distr, _ = topic_model.approximate_distribution(docs)
    return (topic_distr,)


@app.cell
def _(docs, mo):
    document_index = mo.ui.slider(start=0, stop=len(docs)-1, value=0, label="Documento n°")
    document_index
    return (document_index,)


@app.cell
def _(docs, document_index):
    selected_document = docs[document_index.value]
    return (selected_document,)


@app.cell
def _(document_index, mo, selected_document, topic_distr, topic_model, topics):
    (
        mo.md(f"Documento assegnato a: **topic {topics[document_index.value]}**"),
        mo.md(selected_document),
        topic_model.visualize_distribution(topic_distr[document_index.value])
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Distribuzione tokens vs topic""")
    return


@app.cell
def _(docs, document_index, selected_document, topic_model):
    # Calculate the topic distributions on a token-level
    topic_distr_calc, topic_token_distr = topic_model.approximate_distribution(docs, calculate_tokens=True)

    # Visualize the token-level distributions
    topic_model.visualize_approximate_distribution(
        selected_document, topic_token_distr[document_index.value]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## DataMapPlot""")
    return


@app.cell
def _(docs, embeddings, topic_model, umap):
    reduced_embeddings = (
        umap.UMAP(
            n_neighbors=10,
            n_components=2,
            min_dist=0.0,
            metric='cosine'
        )
        .fit_transform(embeddings)
    )

    topic_model.visualize_document_datamap(
        docs,
        reduced_embeddings=reduced_embeddings,
        interactive=True,
        enable_search=True
    )
    return


if __name__ == "__main__":
    app.run()
