import marimo

__generated_with = "0.11.21"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
        # Modalità

        - data da definire tra il 25 giugno e l'11 luglio
        - unica sessione (mattino)
        - presentazione **di durata max 10'** di un elaborato
        - possibilità di organizzarsi in gruppi di lavoro, caso in cui
            - ogni componente dovrà avere un ruolo attivo durante la presentazione
            - il limite di durata è da intendersi _per componente del gruppo_

        # Contenuti

        Cosa intendiamo per _elaborato da presentare_?

        - formato a piacere (marimo/Jupyter notebook, script da eseguire, codice in altro formato, presentazione di slide, ...)
        - tema inerente i contenuti del modulo e più in generale la Data Science/la professione del Data Scientist, es.  
            - tecniche di elaborazione dati
            - algoritmi e modelli
            - rielaborazione/approfondimento di un'analisi del dataset visto a lezione o produzione di un'analisi originale
        - è possibile
            - approfondire uno degli argomenti affrontati
            - dedicarsi ad uno o più dei contenuti "bonus"
            - esplorare un argomento non menzionato (purchè pertinente)

        # Qualche proposta

        **N.B.:** _non è_ obbligatorio fare riferimento a questa lista!

        - Cross-validation
        - SQL
        - Hyperparameters tuning
        - Natural Language Processing (NLP)
        - Sentence Encoders / Embeddings
        - BERTopic
        - Approfondimenti dataviz (viz interattive, geodata e mappe, ...)
        - Deep Learning / ML per Computer Vision
        - Interpretable Machine Learning
        - Ensemble Learning e Stacking
        - Feature selection
        - Time series e forecasting
        - Support Vector Machines
        - Topological Data Analysis
        - Matrix completion e data imputation
        - Problemi di interesse business
           - Anomaly e fraud detection
           - Churn prediction
           - Recommender systems
           - Association rule learning e metodo Apriori
        - Test statistici
        - Problemi di ricerca operativa
        - Metodi per enforcement di sparsità (es. Lasso)
        - Regolarizzazione di Tikhonov e metodo Ridge
        - Metodo Elastic Net
        - Generalized Linear Models

        # Dataset

        Potete:

        1. riutilizzare il dataset del corso
        2. usare dei "vostri" dati, purchè siate disposti a condividerli durante la presentazione dell'elaborato (es. BERTopic su export di chat WhatsApp)
        3. oppure ancora potete utilizzare un nuovo dataset reperito online, per esempio a partire dalle seguenti repository:

            1. https://www.kaggle.com/datasets?tags=13204-NLP
            2. https://www.openml.org/search?type=data&sort=runs&status=active
            3. https://www.dati.gov.it/view-dataset
            4. https://data.europa.eu/data/datasets?locale=en
            5. https://ec.europa.eu/eurostat/en/web/main/data
            6. https://github.com/awesomedata/awesome-public-datasets?tab=readme-ov-file#awesome-public-datasets
            7. https://idrogeo.isprambiente.it/app/
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
