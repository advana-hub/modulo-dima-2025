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

__generated_with = "0.12.9"
app = marimo.App(width="full")


@app.cell
def _():
    import random

    from collections import Counter
    from typing import Callable

    import marimo as mo
    import pandas as pd

    return Callable, Counter, mo, pd, random


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
def _(pd):
    df = pd.read_parquet("../data/data.parquet")
    return (df,)


@app.cell
def _(df):
    df["text"].head(5)
    return


@app.cell
def _(df, mo):
    mo.md(
        rf"""
        La risposta a tutte le nostre domande non è unica, ma sicuramente deve essere preceduta da un'altra domanda "preliminare".

        Come possiamo estrarre dell'**informazione strutturata** a partire dalla colonna `text` che contiene il testo delle recensioni?

        {df[["text"]].head().to_html()}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Estrazione di features sintattiche""")
    return


@app.cell
def _(pd):
    def basic_text_features(df):
        features = pd.DataFrame(index=df.index)
        text_column = "text"
        features[text_column] = df[text_column]
        features["text_length"] = df[text_column].str.len()
        features["word_count"] = df[text_column].str.split().str.len()
        features["sentence_count"] = df[text_column].apply(
            lambda x: x.count(".") + x.count("!") + x.count("?")
        )
        return features

    return (basic_text_features,)


@app.cell
def _(basic_text_features, df):
    features = basic_text_features(df.head(1_000))
    features
    return (features,)


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
def _():
    from wordcloud import WordCloud

    def build_wordcloud(
        frequencies: dict | None = None, text: str | None = None, **kwargs
    ) -> None:
        stopwords = kwargs.get("stopwords")
        if stopwords is None:
            return WordCloud(**kwargs).generate_from_frequencies(frequencies).to_array()
        else:
            return WordCloud(**kwargs).generate_from_text(text).to_array()

    return WordCloud, build_wordcloud


@app.cell
def _(Counter, build_wordcloud, df, mo):
    mo.md(f"""Cosa si può notare nella seguente wordcloud?
    {
        mo.image(
            build_wordcloud(
                frequencies=Counter(" ".join(df["text"][:1_000]).split()),
            ),
            width=500,
        )
    }""")
    return


@app.cell
def _(df):
    lowercase_text = df["text"].str.lower()
    return (lowercase_text,)


@app.cell
def _(df, lowercase_text, mo, pd):
    index = 100
    mo.md(
        rf"""{pd.DataFrame(columns=["original", "cleaned"], data=[[df["text"].iloc[index], lowercase_text.iloc[index]]]).to_html()}"""
    )
    return (index,)


@app.cell
def _(Counter, build_wordcloud, lowercase_text, mo):
    mo.image(
        build_wordcloud(frequencies=Counter(" ".join(lowercase_text[:1_000]).split())),
        width=500,
    )
    return


@app.cell
def _(mo):
    mo.md(r"""Rimuoviamo ora le _stop words_, ovvero parole frequenti considerate neutre dal punto di vista semantico in un determinato contesto.""")
    return


@app.cell
def _():
    # SEE: https://github.com/explosion/spaCy/blob/master/spacy/lang/en/stop_words.py
    # Stop words
    stop_words = set(
        """
        a about above across after afterwards again against all almost alone along
        already also although always am among amongst amount an and another any anyhow
        anyone anything anyway anywhere are around as at

        back be became because become becomes becoming been before beforehand behind
        being below beside besides between beyond both bottom but by

        call can cannot ca could

        did do does doing done down due during

        each eight either eleven else elsewhere empty enough even ever every
        everyone everything everywhere except

        few fifteen fifty first five for former formerly forty four from front full
        further

        get give go

        had has have he hence her here hereafter hereby herein hereupon hers herself
        him himself his how however hundred

        i if in indeed into is it its itself

        keep

        last latter latterly least less

        just

        made make many may me meanwhile might mine more moreover most mostly move much
        must my myself

        name namely neither never nevertheless next nine no nobody none noone nor not
        nothing now nowhere

        of off often on once one only onto or other others otherwise our ours ourselves
        out over own

        part per perhaps please put

        quite

        rather re really regarding

        same say see seem seemed seeming seems serious several she should show side
        since six sixty so some somehow someone something sometime sometimes somewhere
        still such

        take ten than that the their them themselves then thence there thereafter
        thereby therefore therein thereupon these they third this those though three
        through throughout thru thus to together too top toward towards twelve twenty
        two

        under until up unless upon us used using

        various very very via was we well were what whatever when whence whenever where
        whereafter whereas whereby wherein whereupon wherever whether which while
        whither who whoever whole whom whose why will with within without would

        yet you your yours yourself yourselves
        """.split()
    )

    contractions = ["n't", "'d", "'ll", "'m", "'re", "'s", "'ve"]
    stop_words.update(contractions)

    for apostrophe in ["‘", "’"]:
        for stopword in contractions:
            stop_words.add(stopword.replace("'", apostrophe))
    return apostrophe, contractions, stop_words, stopword


@app.cell
def _(build_wordcloud, lowercase_text, mo, stop_words):
    mo.image(
        build_wordcloud(text=". ".join(lowercase_text[:1_000]), stopwords=stop_words),
        width=500,
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Bag of words

        Le word cloud permettono di "iniziare a farsi un'idea" qualitativa sul contenuto di un corpus di documenti testuali (nel nostro caso, l'insieme delle recensioni), ma non costituiscono una rappresentazione strutturata delle relative informazioni semantiche.

        L'approccio più semplice tra quelli standard per l'estrazione di feature quantitative a partire da dato testuale riprende sia i concetti di _multiinsieme_ sia quelli di _one-hot encoding_ e si chiama **bag of words**.

        Tale approccio consiste in:<a id="bow-steps"></a>

        1. definizione di una procedura di _tokenization_, ovvero suddivisione del testo in componenti più piccole dette _token_;
        2. individuazione del _vocabolario_, ovvero dell'insieme di token univoci costituenti il corpus di documenti;
        3. counting: costruzione, per ogni documento, del _multiinsieme_ che assegna ad ogni token del vocabolario la molteplicità con cui compare nel documento;
        4. vettorizzazione del multiinsieme per riportare l'informazione in formato strutturato (tabellare).
        """
    )
    return


@app.cell
def _(pd):
    small_df = pd.DataFrame(
        {
            "text": [
                "Un asino, un cane, un gallo e una gatta, vanno a Brema.",
                "Sulla strada per Brema, scacciano dei briganti da un casolare accogliente.",
                "Una notte un brigante prova a rientrare nel casolare.",
                "Agli occhi del brigante, gli occhi del gatto appaiono come un paio di carboni ardenti.",
            ]
        }
    )
    return (small_df,)


@app.cell
def _(small_df):
    small_df
    return


@app.cell
def _(mo):
    mo.md(r"""### CountVectorizer""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Scikit-learn implementa un transformer che corrispondente al bag of words, che si chiama [`CountVectorizer`](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer).

        Esso ha molti [(iper)parametri](https://en.wikipedia.org/wiki/Hyperparameter_(machine_learning)) da poter configurare: studiamo l'effetto dei principali sul nostro dataset più piccolo.
        """
    )
    return


@app.cell
def _():
    from sklearn.feature_extraction.text import CountVectorizer
    return (CountVectorizer,)


@app.cell
def _(
    CountVectorizer,
    binary,
    lowercase,
    max_df,
    max_features,
    min_df,
    ngram_range,
    small_df,
    stop_words_,
):
    vectorizer = CountVectorizer(
        lowercase=lowercase.value,
        binary=binary.value,
        max_df=max_df.value,
        min_df=min_df.value,
        max_features=max_features.value,
        ngram_range=tuple(ngram_range.value),
        stop_words=None if not stop_words_.value else stop_words_.value.split(),
        # tokenizer=lambda x: x.split(" "),
        # preprocessor=lambda x: x.replace(".", "").replace(",", ""),
    )
    vectorizer.fit(small_df["text"])
    return (vectorizer,)


@app.cell
def _(mo):
    lowercase = mo.ui.switch(value=False, label="lowercase")
    binary = mo.ui.switch(value=False, label="binary")
    max_df = mo.ui.slider(start=0.0, stop=1.0, step=0.1, value=1.0, label="max_df")
    min_df = mo.ui.slider(start=1, stop=3, step=1, value=1, label="min_df")
    max_features = mo.ui.slider(
        start=1, stop=40, step=1, value=40, label="max_features"
    )
    ngram_range = mo.ui.range_slider(
        start=1, stop=3, step=1, value=(1, 1), label="ngram_range"
    )
    stop_words_ = mo.ui.text_area(full_width=True, label="stop_words")

    lowercase, binary, max_df, min_df, max_features, ngram_range, stop_words_
    return (
        binary,
        lowercase,
        max_df,
        max_features,
        min_df,
        ngram_range,
        stop_words_,
    )


@app.cell
def _(pd, small_df, vectorizer):
    (
        small_df.join(
            pd.DataFrame(
                data=vectorizer.transform(small_df["text"]).toarray(),
                columns=vectorizer.get_feature_names_out(),
            )
        )
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        /// tip | Una prima rappresentazione strutturata
        Nella sua semplicità, l'approccio bag of words rappresenta la prima risposta alla domanda: _"Come si può estrarre dell'informazione strutturata a partire da un dato testuale?"_

        Essenzialmente, infatti, il bag of words è una mappa<a id="bow-map"></a>
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
def _(vectorizer):
    vectorizer.vocabulary_
    return


@app.cell
def _(vectorizer):
    new_text = "Questa è una frase presa da un'altra fiaba: la Bella e la Bestia!"
    vectorizer.transform([new_text]).toarray()
    return (new_text,)


@app.cell
def _(new_text, vectorizer):
    vectorizer.build_analyzer()(new_text)
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

        - la _term frequency_ di un token in un documento, indicata come $\text{tf}(t, d)$, che coincide con $\text{BoW}(d)_i$ con $t=t_i$ - ovvero il numero di occorrenze di un token in uno specifico documento;
        - l'_inverse document frequency_ di un token nel corpus di documenti, indicata come $\text{idf}(t)$, ovvero una quantità inversamente proporzionale al numero di occorrenze di un token nell'intero corpus dei documenti.

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
def _():
    from sklearn.feature_extraction.text import TfidfVectorizer

    return (TfidfVectorizer,)


@app.cell
def _(
    TfidfVectorizer,
    binary,
    lowercase,
    max_df,
    max_features,
    min_df,
    ngram_range,
    stop_words_,
):
    tfidf_vectorizer = TfidfVectorizer(
        lowercase=lowercase.value,
        binary=binary.value,
        max_df=max_df.value,
        min_df=min_df.value,
        max_features=max_features.value,
        ngram_range=tuple(ngram_range.value),
        stop_words=None if not stop_words_.value else stop_words_.value.split(),
        # tokenizer=lambda x: x.split(" "),
        # preprocessor=lambda x: x.replace(".", "").replace(",", ""),
    )
    return (tfidf_vectorizer,)


@app.cell
def _(
    binary,
    lowercase,
    max_df,
    max_features,
    min_df,
    ngram_range,
    stop_words_,
):
    lowercase, binary, max_df, min_df, max_features, ngram_range, stop_words_
    return


@app.cell
def _(pd, small_df, tfidf_vectorizer):
    small_df.join(
        pd.DataFrame(
            data=tfidf_vectorizer.fit_transform(small_df["text"]).toarray(),
            columns=tfidf_vectorizer.get_feature_names_out(),
        )
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


@app.cell
def _(mo):
    mo.md(
        r"""
        # Assignment per il 07/05

        /// tip | implementare una versione "casalinga" del bag of words
        ///

        Prova a scrivere una o più funzioni (o direttamente una classe con i suoi metodi!) che implementino il bag of words visto a lezione.

        L'interfaccia di tale implementazione deve soddisfare i seguenti requisiti:

        1. ricevere in input il dataframe `small_df` definito in precedenza;
        2. restituire il medesimo dataframe con la colonna di `"text"` originale e in più le colonne corrispondenti alla vettorizzazione del bag of words.

        Non preoccuparti di gestire "tutte le casistiche" che ti vengono in mente (a meno tu non voglia farlo!), lo scopo di questo esercizio è prendere confidenza con Python, Pandas e le idee fondamentali del bag of words.

        Per aiutarti, puoi fare riferimento alla sua [rappresentazione funzionale](#bow-map) oppure ai [passi](#bow-steps) tramite cui lo abbiamo definito.
        """
    )
    return


@app.cell
def _(bag_of_words, small_df):
    bag_of_words(small_df)
    return


@app.cell
def _(Callable, Counter, pd):
    def tokenize(text: str) -> list:
        return text.split()

    def build_vocabulary(df: pd.DataFrame, *, text_column_name: str, tokenizer: Callable) -> set:
        return set(tokenizer(" ".join(df[text_column_name])))

    def count(text: str, vocabulary: set, tokenizer: Callable) -> dict:
        return {
            token: count
            for token, count in Counter(tokenizer(text)).items()
            if token in vocabulary
        }

    def vectorize(df: pd.DataFrame, count_column_name: str) -> pd.DataFrame:
        return pd.concat(
            [df, pd.DataFrame(df[count_column_name].tolist())], axis="columns"
        ).drop(count_column_name, axis="columns")

    def count_and_vectorize(df: pd.DataFrame, 
                            *,
                            vocabulary: set,
                            tokenizer: Callable, 
                            text_column_name: str, 
                            count_column_name: str) -> pd.DataFrame:
        df[count_column_name] = df[text_column_name].apply(lambda x: count(x, vocabulary, tokenizer))
        return vectorize(df, count_column_name=count_column_name)

    def bag_of_words(df: pd.DataFrame,
                     text_column_name: str = "text",
                     count_column_name: str = "count",
                     tokenizer: Callable = tokenize
                    ) -> pd.DataFrame:
        _df = df.copy()
        vocabulary = build_vocabulary(
            _df, 
            text_column_name=text_column_name, 
            tokenizer=tokenizer)    
        return count_and_vectorize(
            _df, 
            vocabulary=vocabulary, 
            text_column_name=text_column_name, 
            count_column_name=count_column_name, 
            tokenizer=tokenizer
        )
    return (
        bag_of_words,
        build_vocabulary,
        count,
        count_and_vectorize,
        tokenize,
        vectorize,
    )


if __name__ == "__main__":
    app.run()
