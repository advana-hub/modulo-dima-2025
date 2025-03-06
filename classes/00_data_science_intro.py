
# /// script
# dependencies = [
#   "marimo==0.10.12",
# ]
# ///
import marimo

__generated_with = "0.10.12"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # 0. Info organizzative

        - quando si terranno gli incontri
        - criteri di superamento dell'esame (partecipazione attiva + colloquio finale)
        - roadmap del corso
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        # 1. Warm-up game

        [Graphs](https://www.graphs.world/)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        # 2. Cos'è la Data Science?

        ## 2.1 Un po' di storia

        _(un po' di storia da [50 years of Data Science](http://courses.csail.mit.edu/18.337/2015/docs/50YearsDataScience.pdf))_


        [John Tukey](https://en.wikipedia.org/wiki/John_Tukey)[^1] nel 1962 getta le basi teoriche per una definizione della futura Data Science in _"The Future of Data Analysis"_, indicando per primo ciò che la differenzia dalla statistica:

        > _**procedures** for analyzing data, **techniques** for interpreting the results of such procedures, ways of **planning the gathering of data to make its analysis easier**, more precise or more accurate, and **all the machinery and results of (mathematical) statistics** which apply to analyzing data_

        !!! tip
            FIn dall'inizio era quindi chiaro agli addetti ai lavori che i problemi che avrebbe dovuto affrontare la data science non erano _nuovi di per sè_, ma il fatto che riguardassero il (giovane) mondo dei dati poneva delle complessità nuove relativamente all'approccio.

        In tempi più recenti, non tutti gli statistici sono risultati persuasi del fatto che la data science fosse una _nuova_ disciplina:

        > _Aren’t **we** Data Science?_ <small>Marie Davidian, American Statistical Association President, 2013</small>

        > Is data science just a **rebranding** of statistics? <small>Martin Goodson, Royal Statistical Society, 2015</small>

        [Leo Breiman](https://en.wikipedia.org/wiki/Leo_Breiman)[^2] ha infine identificato due obiettivi principali della _scienza dei dati::

        1. **prediction** ➜ to be able to predict what the responses are going to be to future input variables;
        2. **inference** ➜ infer how nature is associating the response variables to the input variables.

        !!! tip
            Possiamo quindi riassumere dicendo: la data science è una disciplina che tenta di applicare il metodo sperimentale e principi/strumenti statistici all'analisi dei dati, occupandosi anche degli aspetti tecnici relativi a procedure e tecniche di acquisizione e gestione dati, al fine ultimo di produrre modelli descrittivi del dato analizzato, approfondire la relazione tra le variabili in input e le variabili in output (target) di un modello e predirre le variabili di output in corrispondenza di input noti.

        !!! info "Nobel per la Fisica 2024"
            ...

        ## 2.2 Quali strumenti si usano?

        Una definizione (anonima) non poi così distante dalla realtà cita:

        > _A Data Scientist is a person who is better at statistics than any software engineer and better at software engineering than any statistician._

        E' ormai chiaro infatti che spesso un Data Scientist non si limita a padroneggiare matematica, statistica e gli aspetti di modellazione, ma deve anche "sporcarsi le mani" con il mondo del software, dell'ingegneria dei dati, del cloud computing, etc. In questo senso, proviamo a fare una lista (disordinata!) di strumenti e competenze utili ad un Data Scientist:

        - conoscenze in svariate branche della matematica: algebra lineare, algebra modulare, teoria degli insiemi, problemi inversi e teoria della regolarizzazione, ricerca operativa, probabilità, statistica descrittiva, statistica inferenziale, metodi bayesiani, metodi montecarlo, calcolo numerico, analisi di Fourier e teoria dei segnali, 


        [^1]: Ideatore dell'algoritmo FFT.
        [^2]: Co-ideatore dell'algoritmo Random Forest.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        [topology of data professions](https://excalidraw.com/#json=9U_RDdeKx2Tg4SQiZpIE3,JtO8qRPcUsmBMD169zzhgg)

        <!-- <iframe src="https://excalidraw.com/#json=9U_RDdeKx2Tg4SQiZpIE3,JtO8qRPcUsmBMD169zzhgg" style="width:100%;height:100px"> -->
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        # Mindset/approccio

        - le meta-skill di uno stem e la capacità di problem solving lo abilitano a fare framing di un problema business sconosciuto in maniera rapida e sostanzialmente corretta (via via il modello mentale si arricchirà di dettagli)
        - "vedi cose che gli altri non vedono"
        """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
