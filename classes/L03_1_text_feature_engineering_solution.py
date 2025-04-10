# /// script
# dependencies = [
#   "pandas==2.2.3",
#   "pyarrow==18.1.0",
#   "marimo>=0.11.18",
#   "scikit-learn==1.6.1",
# ]
# ///

import marimo

__generated_with = "0.12.7"
app = marimo.App(width="full")


@app.cell
def _():
    import random

    import marimo as mo
    import pandas as pd
    return mo, pd, random


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
def _(pd):
    df = pd.read_parquet("../data/data.parquet")
    return (df,)


@app.cell
def _(df):
    df.select_dtypes("object").head(5)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Possiamo essenzialmente distinguere tre tipi di features testuali:

        - degli ID, ovvero identificativi (probabilmente univoci), utilizzati per riferirsi rispettivamente ad una singola recensione, utente o attività commerciale, poco informativi ai fini dell'esplorazione del dataset;
        - il testo della recensione, in formato "libero", uno dei campi principali a cui siamo interessati;
        - il nome dell'attività commerciale;
        - le relative categorie merceologiche.

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
def _(df):
    df["categories"]
    return


@app.cell
def _(df):
    df["categories"].nunique()
    return


@app.cell
def _(df):
    df["categories"].unique()
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
def _():
    from collections import Counter
    return (Counter,)


@app.cell
def _(Counter, df):
    Counter(df["categories"]).most_common(10)
    return


@app.cell
def _(mo):
    mo.md(r"""### Proviamo a risolvere i problemi di ordinamento delle categorie""")
    return


@app.cell
def _():
    category_1 = "Restaurants, Pizza"
    category_2 = "Pizza, Restaurants"
    return category_1, category_2


@app.cell
def _(category_1):
    category_1_splitted = sorted(category_1.split(", "))
    category_1_splitted
    return (category_1_splitted,)


@app.cell
def _(category_2):
    category_2_splitted = sorted(category_2.split(", "))
    category_2_splitted
    return (category_2_splitted,)


@app.cell
def _(category_1_splitted, category_2_splitted):
    category_1_splitted == category_2_splitted
    return


@app.cell
def _(Counter, df):
    separator = ", "
    Counter(
        df["categories"].apply(
            lambda category: separator.join(sorted(category.split(separator)))
        )
    ).most_common(10)
    return (separator,)


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
        2. le categorie presenti in ciascuna stringa non sono ordinate in maniera coerente nei vari samples.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""Iniziamo dal punto (2): ordiniamo le categorie in modo univoco così da ridurre i "falsi" duplicati - adottiamo una tecnica simile alla precedente.""")
    return


@app.cell
def process_categories():
    def process_categories(categories: str) -> tuple:
        return tuple(sorted(categories.split(", ")))
    return (process_categories,)


@app.cell
def _(df, process_categories):
    df["sorted_categories"] = df["categories"].apply(process_categories)
    return


@app.cell
def _(Counter, df):
    Counter(df["sorted_categories"]).most_common(10)
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
def _(pd, random):
    categories = ["pizza", "pasta", "veg", "fusion", "burger"]

    n_records = 100
    df_simple = pd.DataFrame(
        {
            "id": list(range(n_records)),
            "category": random.choices(categories, k=n_records),
        }
    )
    df_simple
    return categories, df_simple, n_records


@app.cell
def _(mo):
    mo.md(r"""La risposta alla nostra domanda su un dataset di questo tipo sarebbe ora più semplice!""")
    return


@app.cell
def _(df_simple):
    df_simple.loc[df_simple["category"] == "pizza", ["id", "category"]]
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Per poter però utilizzare un dataset come input di alcuni modelli di machine learning è a volte richiesto di codificare le feature categoriche tramite valori numerici: tale processo si chiama _encoding_.

        Proviamo ad implementare a mano due tecniche standard di encoding: quello _ordinale_ e quello [_one-hot_](https://en.wikipedia.org/wiki/One-hot).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""### Ordinal encoding (manuale)""")
    return


@app.cell
def _(df_simple):
    category_map = {
        category: index for index, category in enumerate(df_simple["category"].unique())
    }
    return (category_map,)


@app.cell
def _(category_map, df_simple):
    df_simple["category_mapped"] = df_simple["category"].map(category_map)
    df_simple[["id", "category", "category_mapped"]]
    return


@app.cell
def _(mo):
    mo.md(r"""### One-hot encoding (manuale)""")
    return


@app.cell
def _(category_map, df_simple):
    for category in category_map.keys():
        df_simple[category] = df_simple["category"].apply(
            lambda value: 1 if value == category else 0
        )
    return (category,)


@app.cell
def _(df_simple):
    df_simple
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Scikit-learn

        Per affrontare questo task e numerosi altri, utilizzeremo spesso la library [`scikit-learn`](https://scikit-learn.org/stable/getting_started.html), che è il de-facto standard per l'implementazione di modelli di machine learning in Python.

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
        ### OrdinalEncoder

        Torniamo al task di encoding: il più semplice approccio è quello che mappa ogni valore di una variabile categorica su un numero intero, e tale approccio si dice _ordinal encoding_ ed è implementato da scikit-learn tramite il transformer [`OrdinalEncoder`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html#sklearn.preprocessing.OrdinalEncoder).
        """
    )
    return


@app.cell
def _():
    from sklearn.preprocessing import OrdinalEncoder
    return (OrdinalEncoder,)


@app.cell
def _(df_simple):
    type(df_simple["category"])
    return


@app.cell
def _(df_simple):
    type(df_simple[["category"]])
    return


@app.cell
def _(OrdinalEncoder, df_simple):
    ordinal_encoder = OrdinalEncoder()
    X = df_simple[["category"]]
    ordinal_encoder.fit(X)
    return X, ordinal_encoder


@app.cell
def _(ordinal_encoder):
    ordinal_encoder.categories
    return


@app.cell
def _(ordinal_encoder):
    ordinal_encoder.categories_
    return


@app.cell
def _(X, ordinal_encoder):
    X_transformed = ordinal_encoder.transform(X)
    X_transformed[:5]
    return (X_transformed,)


@app.cell
def _(X, X_transformed, pd):
    pd.concat(
        [
            X,
            pd.Series(
                index=X.index, data=X_transformed.ravel(), name="encoded_categories"
            ),
        ],
        axis="columns",
    ).head(10)
    return


@app.cell
def _(X_transformed, ordinal_encoder):
    ordinal_encoder.inverse_transform(X_transformed)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        /// warning | L'ordinal encoding non è sempre una buona scelta!
        Infatti, esso introduce di fatto un _ordinamento_ nella variabile encodata, e questo effetto può essere:

        - desiderato (per esempio nel caso in cui i valori categorici siano una scala di gradimento, e.g. "poco", "abbastanza", "molto")
        - indesiderato (come nel caso d'esempio, in cui non c'è una relazione d'ordine naturale tra "pizza" e "fusion")

        Inoltre, l'encoding ordinale determina implicitamente anche una _metrica_ di distanza tra i valori encodati e un'aritmetica tra essi, che non sempre possono essere coerenti con le relazioni tra i valori di partenza.
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### OneHotEncoder

        Per i casi in cui non esiste un ordine da imporre su una variabile categorica, è possibile seguire un approccio alternativo denominato _one-hot encoding_, che consiste nel rappresentare ognuno degli N valori della feature categorica di input come una nuova feature binaria.
        """
    )
    return


@app.cell
def _():
    from sklearn.preprocessing import OneHotEncoder
    return (OneHotEncoder,)


@app.cell
def _(OneHotEncoder, X):
    onehot_encoder = OneHotEncoder(sparse_output=True)
    onehot_encoder.fit(X)
    return (onehot_encoder,)


@app.cell
def _(onehot_encoder):
    onehot_encoder.get_feature_names_out()
    return


@app.cell
def _(X, onehot_encoder):
    onehot_encoder.transform(X)
    return


@app.cell
def _(X, onehot_encoder):
    onehot_encoder.transform(X).todense()
    return


@app.cell
def _(X, onehot_encoder, pd):
    pd.concat(
        [
            X,
            pd.DataFrame(
                index=X.index,
                data=onehot_encoder.transform(X).todense(),
                columns=onehot_encoder.get_feature_names_out(),
            ),
        ],
        axis="columns",
    ).head(5)
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
def _(pd, random):
    multi_categories = [
        ["pizza", "fusion"],
        ["burger", "veg"],
        ["pasta"],
        ["pasta", "fusion"],
    ]
    df_multi = pd.DataFrame(
        {"id": range(100), "categories": random.choices(multi_categories, k=100)}
    )
    df_multi
    return df_multi, multi_categories


@app.cell
def _(df_multi):
    from sklearn.preprocessing import MultiLabelBinarizer

    multilabel_binarizer = MultiLabelBinarizer()
    multilabel_binarizer.fit(df_multi["categories"])
    multilabel_binarizer.classes_
    return MultiLabelBinarizer, multilabel_binarizer


@app.cell
def _(df_multi, multilabel_binarizer):
    multilabel_binarizer.transform(df_multi["categories"])[:5]
    return


@app.cell
def _(df_multi, multilabel_binarizer, pd):
    pd.concat(
        [
            df_multi,
            pd.DataFrame(
                index=df_multi.index,
                data=multilabel_binarizer.transform(df_multi["categories"]),
                columns=multilabel_binarizer.classes_,
            ),
        ],
        axis="columns",
    ).head(5)
    return


@app.cell
def _(mo):
    mo.md(r"""Proviamo ora a rispondere alla domanda di partenza sul nostro dataset.""")
    return


@app.cell
def _(df, multilabel_binarizer, pd):
    df_encoded = df.join(
        pd.DataFrame(
            data=multilabel_binarizer.fit_transform(df["sorted_categories"]),
            columns=multilabel_binarizer.classes_,
        )
    )
    df_encoded.sample(100)
    return (df_encoded,)


if __name__ == "__main__":
    app.run()
