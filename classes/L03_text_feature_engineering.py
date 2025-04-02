# /// script
# dependencies = [
#   "pandas==2.2.3",
#   "pyarrow==18.1.0",
#   "marimo>=0.11.18",
#   "plotly==6.0.0",
#   "scikit-learn==1.6.1",
#   "wordcloud==1.9.4",
#   "matplotlib==3.10.0",
# ]
# ///

import marimo

__generated_with = "0.12.0"
app = marimo.App(width="full")


@app.cell
def _():
    return


@app.cell
def _():
    import random
    import re
    import string

    import marimo as mo
    import pandas as pd
    import plotly.express as px
    return mo, pd, px, random, re, string


@app.cell
def _(mo):
    mo.md(
        r"""
        # Ripartiamo dai dati testuali

        Selezioniamo solo le _features_ (colonne, attributi) di tipo testuale del nostro dataset e "guardiamole in faccia".
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Possiamo essenzialmente distinguere tre tipi di features testuali:

        - degli ID, ovvero identificativi (probabilmente univoci), utilizzati per riferirsi rispettivamente ad una singola recensione, utente o attività commerciale, poco informativi ai fini dell'esplorazione del dataset;
        - il testo della recensione, in formato "libero", uno dei campi principali a cui siamo interessati;
        - il nome dell'attività commerciale e le relative categorie merceologiche.

        Per semplicità facciamo un'ipotesi (da verificare! il mindset deve essere quello dell'_investigatore sospettoso_ 🤓): i nomi delle attività commerciali sono 1-1 con i rispettivi ID e possiamo quindi non preoccuparcene.

        Restano da esplorare quindi le categorie merceologiche e il testo delle recensioni.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# Features categoriche""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## I multiinsiemi (o _bag_)

        Un [**multiinsieme**](https://en.wikipedia.org/wiki/Multiset) è una coppia $(S, m)$ in cui $S$ è un insieme standard, ed $m$ è una mappa $m: S\to\mathbb{Z}^{+}$ che associa ad ogni $s\in S$ un valore positivo che indica la _molteplicità_ con cui $s$ compare in $S$.

        Nella standard library di Python la miglior approssimazione del concetto di multiset è implementata nella classe [`collections.Counter`](https://docs.python.org/3.10/library/collections.html#collections.Counter).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Preprocessing""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Ci interessa stabilire una maniera semplice con cui rispondere alla seguente domanda:

        > Quali sono i records corrispondenti a recensioni di pizzerie?

        Un altro modo per porre la questione è:

        /// tip | Come si può estrarre l'informazione delle categorie in valore numerico e strutturato (tabellare)?
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Rispondere a questa domanda ad ora non è semplice, essenzialmente perchè la feature `categories` presenta due "problemi", dal punto di vista dell'analisi:

        1. ogni valore non corrisponde ad una sola categoria merceologica, ma ad una stringa rappresentante una _lista di categorie_;
        2. le categorie presenti in ciascuna stringa non sono ordinate in maniera coerente nei vari records.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""Iniziamo dal punto (2): ordiniamo le categorie in modo univoco così da ridurre i "falsi" duplicati.""")
    return


@app.cell
def _(mo):
    mo.md(r"""## Encoding""")
    return


@app.cell
def _(mo):
    mo.md(r"""Ora che abbiamo ordinato coerentemente le categorie di ciascun record, per rispondere alla nostra domanda guida, operiamo una semplificazione: supponiamo che il punto (1) non sussista, ovvero che la nostra feature `categories` contenga un unico valore per ciascun record.""")
    return


@app.cell
def _(mo):
    mo.md(r"""La risposta alla nostra domanda su un dataset di questo tipo sarebbe ora più semplice!""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Per poter però utilizzare un dataset come input di alcuni modelli di machine learning è a volte richiesto di codificare le feature categoriche tramite valori numerici: tale processo si chiama _encoding_.

        Per affrontare questo task e numerosi altri, utilizzeremo spesso la library [`scikit-learn`](https://scikit-learn.org/stable/getting_started.html), che è il de-facto standard per l'implementazione di modelli di machine learning in Python.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### L'interfaccia di scikit-learn

        Scikit-learn implementa numerosi modelli di machine learning e altri tool utili attraverso un'interfaccia comune basata su classi Python, dette _estimators_, che espongono:

        - un metodo (funzione) `fit`, che permette di alimentare il modello con il _training set_ (fase di apprendimento);
        - un metodo `predict`, che permette di ottenere le predizioni del modello su dei nuovi dati di input (fase di inferenza).

        Con un'interfaccia simile sono disponibili anche i _transformers_, classi deputate al preprocessing dei dati (prima della fase di apprendimento), che al posto del metodo `predict` espongono un metodo `transform`.

        ```python
        my_estimator = Estimator()
        my_estimator.fit(X, y)
        y_hat = my_estimator.predict(X_new)

        my_transformer = Transformer()
        my_transformer.fit(X)
        X_transformed = my_transformer.transform(X)
        ```
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Ordinal encoding

        Torniamo al task di encoding: il più semplice approccio è quello che mappa ogni valore di una variabile categorica su un numero intero, e tale approccio si dice _ordinal encoding_ ed è implementato da scikit-learn tramite il transformer [`OrdinalEncoder`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html#sklearn.preprocessing.OrdinalEncoder).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        /// warning | L'ordinal encoding non è sempre una buona scelta!
        Infatti, esso introduce di fatto un _ordinamento_ nella variabile encodata, e questo effetto può essere:

        - desiderato (per esempio nel caso in cui i valori categorici siano una scala di gradimento, e.g. "poco", "abbastanza", "molto")
        - indesiderato (come nel caso d'esempio, in cui non c'è una relazione d'ordine naturale tra "pizza" e "fusion")
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### One-hot encoding

        Per i casi in cui non esiste un ordine da imporre su una variabile categorica, è possibile seguire un approccio alternativo denominato _one-hot encoding_, che consiste nel rappresentare ognuno degli N valori della feature categorica di input come una nuova feature binaria.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### MultiLabelBinarizer

        Ora che abbiamo esplorato e risolto il caso di encoding di una variabile categorica "a valori scalari", possiamo tornare al nostro vero dataset. Fortunatamente, anche per un caso più complesso come il nostro, scikit-learn ci viene in soccorso con il [`MultiLabelBinarizer`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""Proviamo ora a rispondere alla nostra domanda di partenza.""")
    return


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

        1. individuazione del _vocabolario_, ovvero dell'insieme di _token_ univoci costituenti il corpus di documenti;
        2. tokenization & counting: costruzione, per ogni documento, del multiinsieme che assegna ad ogni token del vocabolario la molteplicità con cui compare nel documento;
        3. vettorizzazione del multiinsieme per riportare l'informazione in formato strutturato (tabellare).
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

        In caso di corpus molto grandi, è facile avere molti token ad alta frequenza, che in quanto tali risultano poco informativi nel discriminare il contenuto dei vari documenti del corpus e raggrupparli.

        Trattarli come stop words può aiutare ad eliminarli, ma la definizione di _cosa sia_ una stop words dipende altamente dal contesto (e dalla lingua!), si basa sul mantenimento manuale (quindi, oneroso e soggetto ad errori) di una lista di token da eliminare ed è quindi sostanzialmente un task statico che non si adatta all'arrivo di nuovi dati (è intrinsecamente biased).

        Per risolvere quindi il problema di "eliminazione" dei token non informativi ad alta frequenza, è utile adottare un approccio automatico che faccia _inferenza_ di quali sono tali token a partire dal corpus di documenti stesso: tale approccio è un'estensione del concetto di bag of words e si chiama **term frequency–inverse document frequency** o, più semplicemente, [tf–idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf).
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
