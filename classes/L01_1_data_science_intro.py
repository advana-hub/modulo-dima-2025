
# /// script
# dependencies = [
#   "marimo>=0.11.18",
# ]
# ///

import marimo

__generated_with = "0.11.17"
app = marimo.App(
    width="full",
)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("""# Benvenuti! 👋""")
    return


@app.cell
def _(mo):
    mo.md(r"""## Chi""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Quando/dove

        - una lezione a settimana, il mercoledì pomeriggio, nell’orario 14:00-17:00
        - aula PC3 (al quarto piano, di fronte alla biblioteca)
        - dal 12 marzo al 28 maggio, con l'esclusione del 23 e 30 aprile (pausa festività)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Come

        - sessione di esami: mese di giugno (da concordare)
        - consigliamo a ciascuno di voi di utilizzare il proprio laptop personale
        - prerequisiti (nice-to-have, non bloccanti!): 🐍 Programmazione 2 (48382), 🧠 Machine Learning (114944)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Cosa

        1. Cos’è la Data Science? + modern Python per Data Scientist
        2. Preparazione dati + Analisi esplorativa
        3. Feature engineering
        4. Dimensionality reduction
        5. Clustering
        6. Topic modeling
        7. Regression
        8. Qualche lezione bonus 👀
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Warm-up game

        [Graphs](https://www.graphs.world/)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# Cos'è la Data Science?""")
    return


@app.cell
def _(mo):
    mo.md(
        f"""
        ## Un po' di storia

        - [The History Of Data Science and Pioneers You Should Know](https://onlinestemprograms.wpi.edu/blog/history-data-science-and-pioneers-you-should-know)
        - [Data Science timeline](https://timeline.historyofdatascience.com/)
        {mo.image(src="./data_science_timeline.png", caption="https://medium.com/towards-data-science/the-roots-of-data-science-77c71115229")}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Qualche momento topico

        - 1943: Warren McCulloch e Walter Pitts pubblicano il paper [“A Logical Calculus of the ideas Imminent in Nervous Activity](https://home.csulb.edu/~cwallis/382/readings/482/mccolloch.logical.calculus.ideas.1943.pdf);
        - 1949: Nicholas Metropolis e Stanislav Ulam pubblicano il paper [The Monte Carlo Method](https://people.bordeaux.inria.fr/pierre.delmoral/MetropolisUlam49.pdf), basato sul loro lavoro di ricerca svolto nel decennio precedente all'interno del Progetto Manhattan nei laboratori di Los Alamos;
        - 1957: [Arthur Samuel](https://en.wikipedia.org/wiki/Arthur_Samuel_(computer_scientist)), pioniere dell'AI e contributor di TeX, conia il termine _"machine learning"_;
        - 1962: [John Tukey](https://en.wikipedia.org/wiki/John_Tukey), ideatore dell'algoritmo FFT, getta le basi teoriche per una definizione della futura Data Science in _"The Future of Data Analysis"_, indicando per primo ciò che la differenzia dalla statistica:

            > _**procedures** for analyzing data, **techniques** for interpreting the results of such procedures, ways of **planning the gathering of data to make its analysis easier**, more precise or more accurate, and **all the machinery and results of (mathematical) statistics** which apply to analyzing data_;

        - 1970: [Edgar Codd](https://en.wikipedia.org/wiki/Edgar_F._Codd) della IBM definisce il concetto di _"database relazionale"_;

        - 1986: [Geoffrey Hinton](https://en.wikipedia.org/wiki/Geoffrey_Hinton) pubblica il paper [Learning representations by back-propagating errors](https://www.cs.utoronto.ca/~hinton/absps/naturebp.pdf), che definisce uno standard per il processo di apprendimento delle reti neurali profonde.

            /// tip | Nobel per la Fisica 2024
            Per questo e suoi altri lavori, è stato insignito del premio Nobel per la Fisica nel 2024!
            ///

        - 2007: Prima release della libreria Python che diventerà lo standard per il machine learning: [scikit-learn](https://en.wikipedia.org/wiki/Scikit-learn)!
        - 2008: Il termine _"data scientist"_ emerge come buzzword online (nel 2012 verrà definito "il lavoro più sexy del secolo!")
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        /// tip
        Fin dall'inizio era quindi chiaro agli addetti ai lavori che i problemi che avrebbe dovuto affrontare la data science non erano _nuovi di per sè_, ma il fatto che riguardassero il (giovane) mondo dei dati poneva delle complessità nuove relativamente all'approccio.
        ///

        In tempi più recenti, non tutti gli statistici sono risultati persuasi del fatto che la data science fosse una _nuova_ disciplina:

        > _Aren’t **we** Data Science?_ <small>Marie Davidian, American Statistical Association President, 2013</small>

        > Is data science just a **rebranding** of statistics? <small>Martin Goodson, Royal Statistical Society, 2015</small>
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        [Leo Breiman](https://en.wikipedia.org/wiki/Leo_Breiman), co-ideatore dell'algoritmo Random Forest, ha infine identificato due obiettivi principali della _scienza dei dati_:

        1. **prediction** ➜ to be able to predict what the responses are going to be to future input variables;
        2. **inference** ➜ infer how nature is associating the response variables to the input variables.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        /// tip | Recap
        Possiamo quindi riassumere dicendo: la data science è una disciplina che tenta di applicare il metodo sperimentale e principi/strumenti statistici all'analisi dei dati, occupandosi anche degli aspetti tecnici relativi a procedure e tecniche di acquisizione e gestione dati, al fine ultimo di produrre modelli descrittivi del dato analizzato, approfondire la relazione tra le variabili in input e le variabili in output (target) di un modello e predirre le variabili di output in corrispondenza di input noti.
        ///
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Quali strumenti si usano?

        Una definizione (anonima) non poi così distante dalla realtà cita:

        > _A Data Scientist is a person who is better at statistics than any software engineer and better at software engineering than any statistician._
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
            rf"""
            E' ormai chiaro infatti che spesso un Data Scientist non si limita a padroneggiare matematica, statistica e gli aspetti di modellazione, ma deve anche "sporcarsi le mani" con il mondo del software, dell'ingegneria dei dati, del cloud computing, etc. In questo senso, proviamo a fare una lista (disordinata!) di strumenti e competenze utili ad un Data Scientist:
    
            - **conoscenze in svariate branche della matematica**: algebra lineare, algebra modulare, teoria degli insiemi, problemi inversi e teoria della regolarizzazione, ricerca operativa, probabilità, statistica descrittiva, statistica inferenziale, metodi bayesiani, metodi montecarlo, calcolo numerico, analisi di Fourier e teoria dei segnali, ...
            - **conoscenze di software engineering e database**: SQL/NoSQL, calcolo parallelo e distribuito, DevOps/MLOps, versioning del codice, cloud computing, programmazione in vari linguaggi...
            - **visualizzazione dati e informazioni**: sia dal punto di vista tecnico (che libreria di quale linguaggio uso?) sia dal punto di vista teorico (è meglio mappare una certa info tramite il colore o la dimensione?)
            - **machine learning & co.**: supervised vs unsupervised, deep learning, reinforcement learning, generative AI e LLM, ...
            - **soft skills**: comunicazione scientifica, business translation, teamwork, capacità di problem e framing di un problema sconosciuto...
            - **project management**: pianificazione e controllo di tempi e costi, rispetto scadenze, ...
            - **competenze di dominio**: telco, energy, supply chain, sales & marketing, pharma, logistics, ...

            {mo.image(src="data-science-landscape.jpg")}
            """
        )
    return


@app.cell
def _(mo):
    mo.md(
        f"""
        ## Topology of data professions

        <!-- <iframe src="https://excalidraw.com/#json=9U_RDdeKx2Tg4SQiZpIE3,JtO8qRPcUsmBMD169zzhgg" style="width:100%;height:100px"> -->

        {mo.image(src="topology_data_prof.svg", caption="https://excalidraw.com/#json=9U_RDdeKx2Tg4SQiZpIE3,JtO8qRPcUsmBMD169zzhgg")}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        rf"""
        ## Machine Learning

        A livello tecnico, uno degli aspetti caratterizzanti che distingue un Data Scientist da un Data Analyst e da un Data Engineer sono le competenze verticali, spesso generaliste, sul **machine learning** (quelle specialistiche le lasciamo ai Machine Learning Engineers!)

        {mo.image(src="./ml_map.svg")}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## L'analogia della cucina!""")
    return


@app.cell
def _(mo):
    mo.image(src="./kitchen_analogy.png", caption="https://excalidraw.com/#json=dRNsELmZ1KWGTHahyrBse,76yV4koB0Q3QTuNorMedlg")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
