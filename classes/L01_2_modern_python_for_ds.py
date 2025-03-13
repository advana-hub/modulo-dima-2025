# /// script
# dependencies = [
#   "marimo==0.11.19",
# ]
# ///

import marimo

__generated_with = "0.11.17"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # Hello world!

        👋 Questo è un primo esempio di _notebook interattivo_ in cui è possibile eseguire codice Python. La libreria che implementa tale strumento si chiama [marimo](https://github.com/marimo-team/marimo).

        /// note | Info
        In questa lezione approfondiremo il mondo Python, i concetti di notebook e librerie e tanto altro.
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        # Prima di iniziare: qualche info utile su Python

        ![](https://imgs.xkcd.com/comics/python.png)
        from [XKCD](https://xkcd.com/353/)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Principi di design

        - Python è un linguaggio creato negli anni '90, ma ciònonostante negli anni si è modernizzato ed è tutt'ora lo standard nel mondo analisi dati, data science, machine learning, AI (e non solo!).

        - Supporta sia programmazione _ad oggetti_ (OOP, object-oriented programming), sia programmazione _funzionale_ (FP, functional programming) ed altri paradigmi di programmazione.

        - Al posto di parentesi o punteggiatura, utilizza la spaziatura (indentazione e/o whitespaces) come informazione _semantica_ per delimitare istruzioni e blocchi di codice.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Esiste una lista di "principi" di design, detta [The Zen of Python](https://peps.python.org/pep-0020/#the-zen-of-python), che nelle intenzioni del creatore del linguaggio dovrebbero essere seguiti da ogni sviluppatore. Eccone un estratto:

        ```
        Beautiful is better than ugly.
        Explicit is better than implicit.
        Simple is better than complex.
        Complex is better than complicated.
        Flat is better than nested.
        Sparse is better than dense.
        Readability counts.
        Special cases aren't special enough to break the rules.
        Although practicality beats purity.
        Errors should never pass silently.
        Unless explicitly silenced.
        There should be one-- and preferably only one --obvious way to do it.
        Now is better than never.
        Although never is often better than *right* now.
        If the implementation is hard to explain, it's a bad idea.
        If the implementation is easy to explain, it may be a good idea.
        ```

        /// tip |
        Python ha quindi tanti lati in comuni con alcuni principi matematici: un buon codice Python, come una buona dimostrazione, dovrebbe essere **semplice**, **comprensibile** e in qualche modo **esteticamente appagante**.
        ///

        <!-- ## 1.2 Duck typing

        Python è un linguaggio [dynamically typed](https://en.wikipedia.org/wiki/Dynamic_programming_language): semplificando, i tipi delle variabili vengono valutati a _runtime_ (ovvero durante l'esecuzione di un dato script) e possono mutare, a differenza di quanto accade nei linguaggi _statically typed_ nei quali i tipi vengono verificati durante una fase di _compilazione_ - che nella pratica di Python è "trasparente", non va gestita esplicitamente - e non possono mutare.

        Questo rende Python più conciso e semplice da scrivere, ma anche più prono ad errori e più lento di altri linguaggi (es. TypeScript). Il suo approccio alla tipizzazione è definito [duck typing](https://en.wikipedia.org/wiki/Duck_typing):

        !!! tip "🦆 Duck typing"
            _If it walks like a duck and it quacks like a duck, then it must be a duck!_ -->
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""# Come si può iniziare a utilizzare Python?""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Installazione

        Esistono davvero tantissimi modi per installare Python, qui consigliamo i nostri preferiti (che sono attualmente _i più comodi_ da utilizzare per la data science):

        - ✨ tramite [uv](https://docs.astral.sh/uv/guides/install-python/#installing-python), una new-entry nell'ecosistema di gestori di librerie e progetti Python
        - tramite [miniconda](https://docs.anaconda.com/miniconda/)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Utilizzo

        Esistono forse ancora più modi per utilizzare Python; di nuovo, consigliamo i seguenti perchè sono degli standard nel mondo della data science:

        - notebook interattivi:
            - ✨ [marimo](https://docs.marimo.io/getting_started/index.html), una new-entry nell'ecosistema di strumenti di sviluppo Python, ancora molto "giovane" ma promettente
            - [JupyterLab](https://jupyterlab.readthedocs.io/en/latest/getting_started/installation.html), un ambiente di sviluppo costruito intorno all'utilizzo di [notebook interattivi](https://jupyterlab.readthedocs.io/en/latest/user/notebook.html)
            - prodotti commerciali (es. Google Colab, Hugging Face, Kaggle)
        - IDE (_integrated development environment_):
            - ✨ [Visual Studio Code (VSC)](https://code.visualstudio.com/), distribuito da Microsoft, molto completo che supporta anche i notebook Jupyter
            - PyCharm
        - terminali:
            - una qualunque shell Windows (es. `cmd`, `PowerShell`)
            - una qualunque shell Linux (es. `bash`)
            - una qualunque shell macOS (es. `zsh`)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Estensione

        Python implementa un set di funzionalità molto basilari dette _standard library_. Per estendere tali funzionalità si deve quasi sempre installare _librerie_ esterne (detti anche _pacchetti_), ognuno deputato a implementare una o più funzionalità complesse dedicate ad uno specifico scopo: visualizzazione dati, gestione di web server, crittografia, calcolo simbolico, etc.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Gli ingredienti essenziali per installare nuove librerie sono:

        - un _virtual environment_ -> un ambiente isolato (pensiamo ad un folder su disco) dedicato ad un progetto specifico, in cui è installata una versione di Python (potenzialmente diversa da quella installata al punto (3.1)) e le librerie esterne necessarie al progetto
        - un tool per _installare e gestire_ le librerie esterne all'interno del virtual environment -> una volta installate esse diventano le **dipendenze** del progetto cui si sta lavorando (e si parla quindi di _dependencies management_)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        E' quindi consigliabile avere (almeno) un virtual environment dedicato a ciascun progetto cui si sta lavorando, per evitare di avere conflitti di gestione delle varie versioni delle librerie e ritrovarsi in quello che è definito [dependency hell](https://www.xkcd.com/1987/) 👿

        ![](https://imgs.xkcd.com/comics/python_environment.png)

        Esistono tanti tool alternativi per creare virtual environment (tra cui i già citati uv e miniconda), mentre il principale tool per installazione di pacchetti si chiama [pip](https://pip.pypa.io/en/stable/) (_package installer for Python_).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Runbook

        Riassumendo, per partire con Python consigliamo di seguire i passi:

        1. aprire un terminale
        2. installare [uv](https://docs.astral.sh/uv/getting-started/installation/)
        3. posizionarsi nel folder desiderato (tramite `cd nome_folder`) e creare un virtual environment tramite [uv](https://docs.astral.sh/uv/pip/environments/#creating-a-virtual-environment): `uv venv --python 3.12`
        4. installare le librerie necessarie tramite `uv pip install` (uv avrà cura di installarle nell'environment appena creato!)
        5. scegliere uno strumento di sviluppo (IDE e/o notebook), aprire un nuovo notebook/file Python e importare le librerie tramite `import nome_libreria` oppure `import nome_libreria as alias_libreria`
        6. sviluppare e divertirsi!
        """
    )
    return


@app.cell
def _(mo):
    git_toggle = mo.ui.switch(label="Usando git?", value=True)
    return (git_toggle,)


@app.cell
def _(git_toggle, mo):
    mo.md(
        rf"""
        # Come si possono utilizzare i notebook di questo corso?

        Il materiale del corso verrà rilasciato sulla piattaforma GitHub, in questa Git repository: https://github.com/advana-hub/modulo-dima-2025

        Potete procedere:

        - eseguendo direttamente ciascun notebook grazie all'installazione di uv, tramite il comando `uvx marimo run https://github.com/advana-hub/modulo-dima-2025/blob/main/classes/<NOME_LEZIONE>.py`
        - oppure per una strada più classica, che richiede però qualche setup aggiuntivo
    
        {git_toggle}

        """
    )
    return


@app.cell
def _(git_toggle, mo):
    way_with_git = """
        1. installare [git](https://git-scm.com/downloads)
        2. clonare la repository tramite `git clone https://github.com/advana-hub/modulo-dima-2025.git`
    """
    way_without_git = """
        1. scaricare il contenuto del repository dedicato a questo modulo sotto forma di file compresso al link [https://github.com/advana-hub/modulo-dima-2025/releases](https://github.com/advana-hub/modulo-dima-2025/releases)
        2. estrarre il contenuto dello zip file
    """


    mo.md(f"""
    {way_with_git if git_toggle.value else way_without_git}
        3. eseguire/modificare ogni notebook localmente tramite `uvx marimo edit <NOME_LEZIONE>.py` (se avete creato un venv e installato marimo, non serve nemmeno il comando `uvx`)
        """)
    return way_with_git, way_without_git


@app.cell
def _(mo):
    mo.md(
        f"""
        # Python essentials

        type hierarchy (**semplificata!**), per chi vuole solo la cruda verità [qui](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy) c'è la gerarchia completa

        {mo.image(src="./type_hierarchy.svg", caption="https://excalidraw.com/#json=nbhV07l_tp8bjcbIknT1f,zjuvujbH_PCPtLdyDmaHjg")}
        """
    )
    return


@app.cell
def _(mo):
    mo.carousel([mo.md(
        r"""
        esistono svariati _tipi_ basilari, tra cui i principali sono:

        - `int` -> numero intero
        - `float` -> numero decimale
        - `str` -> stringa di testo
        - `bool` -> booleano
        """), 

                 mo.md(
        r"""ci sono poi _tipi_ dedicati a strutture dati più complesse:

            - `list` -> collezione di oggetti referenziati rispetto alla propria _posizione_ (quindi, ordinabile)
                <!-- - `tuple` -> come la lista, ma _immutabile_ -->
            <!-- - `set` -> equivalente del concetto matematico di insieme (non ordinabile, senza ripetizioni, ...) -->
            - `dict` -> collezione di oggetti referenziati rispetto alla _chiave_ cui sono associati, ovvero mappa tra un insieme di _chiavi_ ed un insieme di _valori_
            <!-- - questi tipi supportano la definizione (efficiente!) tramite _comprehension_ -->
            - `DataFrame` -> struttura ormai standard per implementare il concetto di tabella (implementate da librerie esterne, es. della library per elaborazione dati `pandas`)"""),

                 mo.md(
        r"""
    - a seconda del proprio tipo, ogni variabile espone alcuni metodi (funzioni) con cui può essere manipolata, accessibili tramite la notazione `variabile.metodo()`
    - esistono gli operatori standard aritmetici (+, -, *, /, etc.) e di confronto (>, <, >=, !=, ==, `in`, `is`, `not`, etc.)
    - esiste la possibilità di commentare il codice tramite `#`
    - esistono i classici strumenti per il _controllo del flusso_: clausole `if/elif/else`, cicli `for` e `while`, gestione degli errori tramite `try/except`, `match/case`
    - esiste la possibilità di definire funzioni tramite `def`, le quali potranno accettare input sia in maniera _posizionale_ (arguments) che _nominale_ (keyword arguments), ricalcando la differenza tra `list` e `dict`
    - esiste la possibilità di definire anche nuovi "oggetti" (classi) tramite `class` che, di fatto, sono nuovi _tipi_ 🤯
    - tante funzionalità di MATLAB sono disponibili nella libreria [numpy](https://numpy.org/doc/stable/user/numpy-for-matlab-users.html), che sta per _numerical Python_, ed è alla base di tantissimi strumenti Python ormai standard per l'algebra lineare, il calcolo scientifico, l'analisi dati e il machine learning -> Numpy è il backend di pandas, ma ormai è quasi del tutto trasparente per noi "utenti finali"
        """)

                ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        # Help!

        Come ogni buon amico, Python offre alcune ricche funzionalità di _help_.
        """
    )
    return


@app.cell
def _():
    help(print)
    return


@app.cell
def _():
    help("if")
    return


@app.cell
def _():
    help("TRUTHVALUE")
    return


@app.cell
def _():
    help("symbols")
    return


if __name__ == "__main__":
    app.run()
