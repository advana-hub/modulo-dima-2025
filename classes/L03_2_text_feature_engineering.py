# /// script
# dependencies = [
#   "pandas==2.2.3",
#   "pyarrow==18.1.0",
#   "marimo>=0.11.18",
#   "scikit-learn==1.6.1",
#   "wordcloud==1.9.4",
#   "matplotlib==3.10.0",
# ]
# ///

import marimo

__generated_with = "0.12.7"
app = marimo.App(width="full")


@app.cell
def _():
    import random
    import re

    from collections import Counter

    import marimo as mo
    import pandas as pd
    return Counter, mo, pd, random, re


@app.cell
def _(mo):
    mo.md(
        r"""
        # Le recensioni

        Alcune domande "business":

        1. di quali _argomenti_ parlano le recensioni?
        2. come possiamo raggruppare le recensioni _simili_ tra loro?
        3. il testo di una recensione contiene informazioni per _stimare_ il punteggio numerico della recensione stessa?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        La risposta a tutte le nostre domande non è unica, ma sicuramente deve essere preceduta da un'altra domanda "preliminare".

        Come possiamo estrarre dell'**informazione strutturata** a partire dalla colonna `text` che contiene il testo delle recensioni?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Estrazione di features sintattiche""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Esploriamo la semantica: le word cloud

        Una [word cloud](https://en.wikipedia.org/wiki/Tag_cloud) è una visualizzazione qualitativa di un testo che mostra le parole di cui è composto; ogni parola è rappresentata con una dimensione proporzionale alla frequenza con cui compare nel testo.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""Rimuoviamo ora le _stop words_, ovvero parole frequenti considerate neutre dal punto di vista semantico in un determinato contesto.""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Bag of words

        Le word cloud permettono di "iniziare a farsi un'idea" qualitativa sul contenuto di un corpus di documenti testuali (nel nostro caso, l'insieme delle recensioni), ma non costituiscono una rappresentazione strutturata delle relative informazioni semantiche.

        L'approccio più semplice tra quelli standard per l'estrazione di feature quantitative a partire da dato testuale riprende sia i concetti di _multiinsieme_ sia quelli di _one-hot encoding_ e si chiama **bag of words**.

        Tale approccio consiste in:

        1. definizione di una procedura di _tokenization_, ovvero suddivisione del testo in componenti più piccole dette _token_;
        2. individuazione del _vocabolario_, ovvero dell'insieme di token univoci costituenti il corpus di documenti;
        3. counting: costruzione, per ogni documento, del _multiinsieme_ che assegna ad ogni token del vocabolario la molteplicità con cui compare nel documento;
        4. vettorizzazione del multiinsieme per riportare l'informazione in formato strutturato (tabellare).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Implementazione manuale

        Proviamo a definire "a mano" una funzione che implementi il bag of words.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""### CountVectorizer""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Fortunatamente scikit-learn implementa un transformer che automatizza quanto fatto a mano da noi, che si chiama [`CountVectorizer`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer).

        Esso ha molti [(iper)parametri](https://en.wikipedia.org/wiki/Hyperparameter_(machine_learning)) da poter configurare: studiamo l'effetto dei principali sul nostro dataset più piccolo.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        /// tip | Una prima rappresentazione strutturata
        Nella sua semplicità, l'approccio bag of words rappresenta la prima risposta alla domanda: _"Come si può estrarre dell'informazione strutturata a partire da un dato testuale?"_

        Essenzialmente, infatti, il bag of words è una mappa
        $$\begin{align*}
        \text{BoW}:\mathcal{D}&\to\mathbb{N}^k\\
        d&\mapsto (n_1,\dots,n_k)
        \end{align*}$$

        che associa ad un documento $d$ in un corpus $\mathcal{D}$ un vettore di $\mathbb{N}^k$ dove $k$ è il numero di token costituenti il vocabolario ed $\text{BoW}(d)_i = n_i$ indica la molteplicità con cui il token $i$-esimo compare nel documento $d$.
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            r"""
            /// warning | L'approccio _bag of words_ ha alcuni limiti, riesci a individuarli?
            ///
            """: mo.md("""
            1. sparsità, che si può risolvere tramite una rappresentazione efficiente in [`scipy.sparse`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html#scipy.sparse.csr_matrix);
            2. si perdono info sul contesto e ordinamento dei token (a meno di non usare [_n-grammi_](https://en.wikipedia.org/wiki/N-gram)).
            """)
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## TF-IDF

        In caso di corpus molto grandi, è facile avere molti token ad alta frequenza, che in quanto tali risultano poco informativi nel discriminare il contenuto dei vari documenti del corpus e raggrupparli (lo abbiamo già notato nelle word cloud).

        Trattarli come stop words può aiutare ad eliminarli, ma la definizione di _cosa sia_ una stop words è spesso meno banale di quanto sembra.
        Le stop words, infatti:

        1. dipendono dal contesto (e, quindi, dalla lingua!);
        2. si basano sul mantenimento manuale (quindi, oneroso e soggetto ad errori) di una lista di token da eliminare;
        3. vengono definite da una procedura sostanzialmente statica che non si adatta all'arrivo di nuovi dati (è intrinsecamente biased).

        /// tip | 
        Per risolvere quindi il problema di "eliminazione" dei token non informativi ad alta frequenza, è utile adottare un approccio automatico che faccia _inferenza_ di quali sono tali token a partire dal corpus di documenti stesso: tale approccio è un'estensione del concetto di bag of words e si chiama **term frequency–inverse document frequency** o, più semplicemente, [tf–idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf).
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        L'approccio prende il nome dai due termini fondamentali che vengono considerati:

        - la _term frequency_ di un token in un documento, indicata come $\text{tf}(t, d)$, che coincide con $\text{BoW}(d)_i$ con $t=t_i$
        - l'_inverse document frequency_ di un token nel corpus di documenti, indicata come $\text{idf}(t)$

        La tf-idf non è altro che il prodotto di questi due termini, ovvero $\text{tf-idf}(t, d)=\text{tf}(t, d)\times\text{idf}(t)$.
        """
    )
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            r"""
            /// tip | L'idea di fondo è semplice!
            ///
            """: mo.md("""
            Pesare la frequenza "locale" di un token in un documento in maniera inversamente proporzionale alla sua frequenza "globale" nel corpus di documenti.

            Ad esempio, il token _the_ in lingua inglese è verosimilmente ad alta frequenza in una recensione, ma il suo valore di tf-idf risulta basso perchè è ad alta frequenza _in tutte le recensioni_!
            """)
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Formalmente, i due termini della tf-idf sono definiti come segue:

        $$\begin{align*}
        \text{tf}(t, d)= &\big|\{t_i \in d\,|\,t_i=t\}\big|\\
        \text{idf}(t)= &\log\frac{1+n}{1+\text{df}(t)}
        \end{align*}$$

        dove

        $$\begin{align*}
        \text{df}(t)=&\big|\{d \in \mathcal{D}\,|\,\text{tf}(t, d) > 0\}\big|\\
        n=&\big|\mathcal{D}\big|
        \end{align*}$$

        I vettori corrispondenti a ciascun documento vengono poi normalizzati (di default tramite norma L2).

        Ulteriori dettagli sull'implementazione in scikit-learn sono disponibili [qui](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        /// note | Relazione tra TF-IDF e bag of words e pipeline di scikit-learn
        Scikit-learn implementa, oltre a estimators e transformers, anche una classe [`Pipeline`](https://scikit-learn.org/stable/modules/compose.html#pipeline) utile ad effettuarne la _composizione_, ovvero $\text{Pipeline}([f, g]) = g \circ f$.

        Il `TfidfVectorizer` che abbiamo utilizzato non è altro che la composizione di `CountVectorizer` con un transformer `TfidfTransformer` dedicato al solo step di calcolo del termine "idf" e successiva normalizzazione.

        Valgono quindi le relazioni:

        - TfidfVectorizer = Pipeline([CountVectorizer, TfidfTransformer])
        - TfidfVectorizer($\cdot$, use_idf=False, norm=None) = CountVectorizer($\cdot$)
        ///
        """
    )
    return


if __name__ == "__main__":
    app.run()
