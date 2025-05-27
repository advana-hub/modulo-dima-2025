# /// script
# dependencies = [
#   "marimo>=0.11.18",
#   "matplotlib==3.10.0",
#   "numpy==2.2.1",
#   "pandas==2.2.3",
#   "plotly==5.24.1",
#   "pyarrow==18.1.0",
#   "scikit-learn==1.6.1",
# ]
# ///

import marimo

__generated_with = "0.13.11"
app = marimo.App(width="full", app_title="08_regression")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    import plotly.graph_objects as go
    import plotly.express as px

    from plotly.subplots import make_subplots
    from sklearn.linear_model import LinearRegression
    from sklearn.datasets import make_regression
    from sklearn.linear_model import Lasso

    from sklearn.tree import DecisionTreeRegressor, plot_tree
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error as mae

    pd.options.plotting.backend = "plotly"
    return (
        DecisionTreeRegressor,
        Lasso,
        LinearRegression,
        cross_val_score,
        go,
        mae,
        make_regression,
        make_subplots,
        mo,
        np,
        pd,
        plot_tree,
        px,
        train_test_split,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
    # La Regressione

    Nel gergo del Machine Learning (ML), si parla di problemi di regressione quando, a partire da un set di dati di input $X$, si cerca di imparare una funzione $f(X)$ che approssimi bene i valori di una variabile target $y$ **che assume valori _continui_**.
    """
    )
    return


@app.cell
def _(mo):
    mo.accordion(
        {
            "🤓 Un po' di formalismo": r"A partire da una matrice di dati $X \in \mathbb{R}^{n \times d}$ (avente $n$ sample descritti da $d$ predittori) ed un corrispondente vettore target $\bm{y} \in \mathbb{R}^{n}$ l'obbiettivo della regressione è imparare una funzione $f: \mathbb{R}^{d} \rightarrow \mathbb{R}$ che associ ad ogni input $\bm{x}_i \in \mathbb{R}^d$ una predizione corrispondente $\hat{y}_i \in \mathbb{R}$ che sia una _buona approssimazione_ di $y_i$. In ML quando, come nel caso della regressione, ad ogni $i-$esimo sample $\bm{x}_i$ è associato un output $y_i$ si parla di problemi **supervisionati**.",
            "👀 Altri spunti": r"La regressione non è l'unico tipo di problema supervisionato che si tratta in ML. Quando infatti ad ogni sample $\bm{x}_i$ è associato un valore discreto (solitamente chiamato __etichetta__, o in inglese __label__) $y_i \in [1,2,\dots,k]$ si parla di problemi di __classificazione__. In particolare, quando la label può assumere solo due valori (tipicamente codificati in $[1, 0]$ o $[1, -1]$) si parla di problemi di classificazione __binaria__.",
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Vediamo un esempio semplice, ma concreto. Immaginiamo di avere raccolto per ciascuno dei nostri $n$ campioni (*aka* samples) un solo predittore $x_i$ ed un solo target $y_i \in \mathbb{R}$. Assumiamo poi che, così come il target, anche il predittore assuma solo valori continui (*ie* $x_i \in \mathbb{R}$) (vedremo più avanti che questa condizione non è strettamente necessaria in generale).

    Visualizziamo questo dataset su un piano cartesiano e proviamo a rispondere alle seguenti domande.

    1. Sapremmo individuare *ad occhio* la relazione ($f$) tra il predittore $x_i$ ed il target $y_i$?
    2. Nel rispondere alla prima domanda, che ruolo gioca il numero di samples $n$?
    """
    )
    return


@app.cell
def _(mo):
    num_samples = mo.ui.slider(start=10, stop=100, step=1, label=r"$n$")

    num_samples
    return (num_samples,)


@app.cell
def _(np):
    x_full = np.random.uniform(0, 10, 100)
    return (x_full,)


@app.cell
def _(np, num_samples, pd, x_full):
    x = x_full[: num_samples.value]
    y = np.sin(np.pi * x)

    df = pd.DataFrame({"x": x, "y": y})

    fig = df.set_index("x")["y"].plot(kind="scatter")
    fig.update_layout(xaxis_title=r"Feature ($x_i$)", yaxis_title=r"Target ($y_i$)")
    fig.update_layout(yaxis=dict(range=[-1.1, 1.1]), xaxis=dict(range=[-0.5, 10.5]))
    fig.update_layout(showlegend=False)

    fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Nei casi reali trovare una funzione (*ie* un __modello__) $f(X)$ che approssimi bene il vettore target $\bm{y}$

    $$
        f(X) = \hat{\bm{y}} \approx \bm{y}
    $$

    può non essere semplice, molti fattori possono concorrere a rendere questa funzione difficile da individuare. Ad esempio ci capiterà spesso di avere molti predittori (esistono casi in cui $d \gg n$), alcuni dei quali completamente slegati dal target (*ie* confounding factors), altri che presentano collinearità, sicuramente le misure (target compreso) comprenderanno un certo livello di fluttuazione randomica (che dovremo cercare di __non__ considerare nel modello), e così via.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Sono task di regressione, ad esempio:

    1. la predizione del prezzo di un immobile a partire da informazioni quali: posizione, metratura, esposizione...
    2. la predizione del costo dell'assicurazione sanitaria di un cittadino a partire da informazioni quali: stato di salute, età, numero di figli...
    3. la predizione dei volumi di $\text{CO}_2$ emessi dalle industrie agro-alimentari a partire da informazioni quali: tipologia di coltivazione, consumo di corrente elettrica, utilizzo di fertilizzanti/pesticidi...

    Alcuni esempi reali: [1]((https://www.kaggle.com/datasets/prokshitha/home-value-insights)), [2](https://www.kaggle.com/datasets/mirichoi0218/insurance), [3](https://www.kaggle.com/datasets/alessandrolobello/agri-food-co2-emission-dataset-forecasting-ml).

    ## Metodi lineari

    L'approccio più semplice alla regressione è quello __lineare__. In questo caso, per ogni $i$-esimo campione $\bm{x}_i$, la predizione $\hat{y}_i$ della variabile target ad esso associata $y_i$ sarà data dalla combinazione lineare dei suoi $j$-esimi predittori (con $j=1,\dots,d$).

    $$
        \hat{y}_i = w_1 \cdot x_{i1} + w_2 \cdot x_{i2} + \dots + w_d \cdot x_{nd}
    $$

    La fase in cui ad ogni predittore si associa un peso $w_j$ è detta __allenamento__ del modello. Ma come si allena un modello lineare?

    ### 🫳🏻 Hands-on

    Consideriamo per semplicità un caso bidimensionale

    $$
        y_i = w_1 \cdot x_{i1} + w_2 \cdot x_{i2}
    $$

    e proviamo a cercare __a mano__ il valore dei pesi $w_j$.
    """
    )
    return


@app.cell
def _(np):
    X1 = np.random.randn(10, 2)
    return (X1,)


@app.cell
def _(mo):
    w1 = mo.ui.slider(start=-5, stop=5, step=0.05, value=0, label=r"$w_1$")
    w1
    return (w1,)


@app.cell
def _(mo):
    w2 = mo.ui.slider(start=-5, stop=5, step=0.05, value=0, label=r"$w_2$")
    w2
    return (w2,)


@app.cell
def _(X1, np, w1, w2):
    guess_coeff = np.array([w1.value, w2.value])

    real_coeff = np.array([1.5, -3])

    y1 = X1.dot(real_coeff)
    y1_hat = X1.dot(guess_coeff)
    return y1, y1_hat


@app.cell
def _(X1, pd, y1, y1_hat):
    df1 = pd.DataFrame(
        {
            "x1": X1[:, 0],
            "x2": X1[:, 1],
            "y_true": y1,
            "y_hat": y1_hat,
            "absolute_error": (y1 - y1_hat) ** 2,
        }
    )
    return (df1,)


@app.cell
def _(df1, go, make_subplots):
    fig1 = make_subplots(
        rows=1,
        cols=2,
        shared_xaxes=True,
        subplot_titles=["Target vero vs predizione", "Errore di predizione"],
    )

    fig1.add_trace(
        go.Scatter(x=df1.index, y=df1["y_hat"], name=r"$\hat{y}$", mode="markers"),
        row=1,
        col=1,
    )
    fig1.add_trace(
        go.Scatter(x=df1.index, y=df1["y_true"], name=r"$y$", mode="markers"),
        row=1,
        col=1,
    )
    fig1.add_trace(
        go.Bar(x=df1.index, y=df1["absolute_error"], name=r"$(\hat{y}_i - y_i)^2$"),
        row=1,
        col=2,
    )

    fig1.update_layout(
        xaxis_title=r"$i$",
        yaxis_title="",
        xaxis2_title=r"$i$",
        yaxis2_title=r"$(\hat{y}_i - y_i)^2$",
        yaxis2=dict(range=[0, 100]),
    )

    fig1
    return


@app.cell
def _(mo):
    mo.md("""Stanco di cercare? La soluzione è qui sotto 👇""")
    return


@app.cell
def _(mo):
    mo.accordion({"⚠️ SPOILER ALERT ⚠️": r"I pesi reali sono $\bm{w} = [1.5, -3]$"})
    return


@app.cell
def _(mo):
    mo.md(
        """
    /// tip | Implementazione

    Fino ad ora abbiamo visto esempi _noiseless_ ovvero in cui le fluttuazioni randomiche di $x$ ed $y$ erano pari a zero. Da qui in avanti iniziamo a considerare casi più realistici.
    ///
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Ordinary Least Squares

    Fortunatamente esistono modi migliori per cercare una buona approssimazione del vettore dei pesi $\bm{w}$. Il primo esempio che vediamo è la classica regressione lineare. Nel gergo del ML questa tecnica spesso prende il nome di Ordinary Least Squares (OLS).

    Dai nostri esperimenti manuali abbiamo potuto constatare come la minimizzazione dell'errore di predizione $(\hat{y}_i - y_i)^2$ possa aiutarci nell'individuare la direzione giusta da seguire per ottenere il nostro vettore dei pesi $\bm{w}$. Provando a tradurre in formule questo concetto, ci basterà quindi impostare un problema di minimo.

    $$
        \bm{\hat{w}_{OLS}} = \min_{\bm{w}} ||X \cdot \bm{w} - \bm{y}||_2^2
    $$

    Questo problema è convesso e differenziabile, presenta quindi una soluzione in [forma chiusa](https://en.wikipedia.org/wiki/Ordinary_least_squares#Estimation). Prima di passare a casi reali, vediamo come possiamo applicare questa tecnica al caso precedente. Sfruttiamo, come sempre, [scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html).
    """
    )
    return


@app.cell
def _(LinearRegression, X1, mo, y1):
    estimator = LinearRegression()
    estimator.fit(X1, y1)

    print(estimator.coef_)

    mo.show_code()
    return (estimator,)


@app.cell
def _(estimator, mo):
    mo.md(f"""`{estimator.coef_}`""")
    return


@app.cell
def _(mo):
    mo.md(
        """
    In questo modulo sfruttiamo sempre funzioni di librearia già disponibili, ma la soluzione di OLS è molto semplice da implementare in Python. Provaci a casa e facci sapere com'è andata.

    ### Lasso

    Fino qui è stato tutto molto semplice. Iniziamo a complicarci un po' la vita, ma restiamo ancora un attimo nell'ambito dei dati sintetici (arriveranno presto quelli reali).

    Quando si affrontano problemi di regressione si prende sempre in considerazione il fatto che la relazione tra $X$ (input) ed $\\bm{y}$ (output) non potrà mai essere ricostruita __esattamente__. I casi sopra, in quanto sintetici, ci danno accesso alla __vera__ relazione tra input ed output ma questo non deve trarci in inganno. Nei casi reali a tale relazione __non si ha mai accesso__. Ciò che si può fare è individuare un approccio che, dato un set di dati in input ($X$), ricostruisca al meglio possibile il target ($\\bm{y}$) accettando di commettere degli errori di predizione.

    /// tip | Curiosità

    Nel mondo del ML (o meglio, della statistica) esiste un famoso aforisma, attribuito a George Box.
    > [All models are wrong, but some are useful](https://en.wikipedia.org/wiki/All_models_are_wrong)
    ///
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Sfruttiamo nuovamente scikit-learn ed estendiamo il caso bidimensionale precedente ad un generico caso $d$-dimensionale. Aggiungiamo anche un nuovo livello di complessità: la relazione tra input ed output risentirà, in questo caso, di un rumore che assumiamo additivo gaussiano con media nulla e deviazione standard $\sigma$ (ovvero $ε \sim \mathcal{N}(0, \sigma^2)$).

    $$
        \bm{y} = f(X) + ε
    $$
    """
    )
    return


@app.cell
def _(mo):
    n_samples_synth1 = mo.ui.slider(start=10, stop=1_000, step=10, value=100, label=r"$n$")
    n_samples_synth1
    return (n_samples_synth1,)


@app.cell
def _(mo):
    n_features_synth1 = mo.ui.slider(start=3, stop=10, step=1, value=3, label=r"$d$")
    n_features_synth1
    return (n_features_synth1,)


@app.cell
def _(mo):
    sigma_synth1 = mo.ui.slider(start=0, stop=3, step=0.01, value=0.1, label=r"$\sigma$")
    sigma_synth1
    return (sigma_synth1,)


@app.cell
def _(make_regression, n_features_synth1, n_samples_synth1, pd, sigma_synth1):
    X_values, y_values, coeff_values = make_regression(
        n_samples=n_samples_synth1.value,
        n_features=n_features_synth1.value,
        n_informative=n_features_synth1.value // 2,
        noise=sigma_synth1.value,
        coef=True,
        random_state=42,
    )

    dfX1 = pd.DataFrame(
        data=X_values,
        columns=[f"feature_{i}" for i in range(n_features_synth1.value)],
    )
    dfy1 = pd.Series(data=y_values, name="target")
    return coeff_values, dfX1, dfy1


@app.cell
def _(mo):
    mo.md(r"""Ispezioniamo visivamente features e target.""")
    return


@app.cell
def _(dfX1, dfy1, mo):
    mo.carousel([dfX1, dfy1])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    In questo caso non sappiamo a priori quale sia il legame tra $X$ ed $\bm{y}$, assumiamo che sia lineare ma non è detto che __tutte__ le feature siano effettivamente utili a ricostruire il target.

    Nel mondo dei modelli lineari, una feature è __inutile__ ai fini della predizione quando il suo peso è nullo ($w_j = 0$). Chiediamoci quindi, OLS è in grado di stimare dei vettori dei pesi $\bm{w}$ in cui alcune entrate sono nulle?

    Testiamolo empiricamente.
    """
    )
    return


@app.cell
def _(LinearRegression, dfX1, dfy1, mo):
    w_OLS = LinearRegression().fit(dfX1, dfy1).coef_

    print(w_OLS)

    mo.show_code()
    return (w_OLS,)


@app.cell
def _(mo, w_OLS):
    mo.md(f"""`{w_OLS}`""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Per come è scritto il problema di minimo in OLS, è possibile ottenere pesi _ragionevolemente piccoli_, ma non nulli.

    Vediamo quindi come possiamo riscrivere il problema di minimo precedente, al fine di introdurre questa possibilità.

    $$
        \bm{\hat{w}_{l1}} = \min_{\bm{w}} ||X \cdot \bm{w} - \bm{y}||_2^2 + \alpha ||\bm{w}||_1
    $$

    Nel gergo del ML l'addendo di sinistra è noto come __loss function__ ed è il contributo che misura l'aderenza della soluzione che si cerca al dato; ci dice in sostanza _quanto possiamo fidarci_ dei dati. L'addendo di destra è detta __regularization penalty__ e misura la quantità di informazione nota a priori che vogliamo aggiungere. In generale la penalty _tiene a bada_ i coefficienti $\hat{\bm{w}}$ e, a seconda di come è definita, permette alla soluzione di soddisfare alcune proprietà.

    Quando la penalty sui coefficienti è data dalla norma $L_1$ il problema prende il nome di [__Lasso regression__](https://en.wikipedia.org/wiki/Lasso_(statistics)) e ci permette di poter _scartare_ alcune features ritenute inutili ai fini della predizione.

    /// tip | 

    Il problema di minimo è convesso, ma non differenziabile, per essere risolto necessita quindi di [algoritmi iterativi](https://en.wikipedia.org/wiki/Proximal_gradient_methods_for_learning#Lasso_regularization).
    ///

    Un'altra grande differenza rispetto al caso precedente è la presenza del parametro $\alpha$. Questo parametro ci permette di decidere quanta regolarizzazione _forzare_ nella nostra soluzione. Il parametro $\alpha$ regola il _trade-off_ tra aderenza al dato e semplicità della soluzione trovata. Questo tema è di importanza fondamentale nel ML, e sarà chiarito meglio in seguito.

    Come sempre, scikit-learn ci viene in aiuto.
    """
    )
    return


@app.cell
def _(mo):
    alpha_lasso = mo.ui.slider(start=0.001, stop=1, step=0.01, value=1.0, label=r"$\alpha$")
    alpha_lasso
    return (alpha_lasso,)


@app.cell
def _(Lasso, alpha_lasso, dfX1, dfy1, mo):
    w_l1 = Lasso(alpha=alpha_lasso.value).fit(dfX1, dfy1).coef_

    print(w_l1)

    mo.show_code()
    return (w_l1,)


@app.cell
def _(mo, w_l1):
    mo.md(f"""`{w_l1}`""")
    return


@app.cell
def _(coeff_values, mo):
    mo.accordion(
        {
            "⚠️ SPOILER ALERT ⚠️": f"""
                Il _vero_ vettore dei pesi in realtà era noto: `{coeff_values}`
            """
        }
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Altri metodi lineari

    /// tip | Ridge regression

    Penalizzare il funzionale tramite norma $L_1$ non è né l'unica scelta possibile, né la più ovvia. Nel mondo del ML è anche molto utilizzata una strategia nota come __Ridge regression__, in cui la penalità sfrutta la norma $L_2$. Questo metodo, data la sua semplicità, è stato indipendentemente scoperto e ri-scoperto nella storia. Studiando la letteratura infatti lo si può trovare sotto molti nomi, quali $L_2$-regularization, [weight decay](https://proceedings.neurips.cc/paper_files/paper/1991/file/8eefcfdf5990e441f0fb6f3fad709e21-Paper.pdf), [Tikhonov regularization](https://en.wikipedia.org/wiki/Ridge_regression#Tikhonov_regularization), [regularization network](https://link.springer.com/article/10.1023/A:1018946025316) ...
    ///

    /// tip  | Elastic-Net

    Perchè quindi non penalizzare il problema sia con la norma $L_1$ che con la norma $L_2$? Ovviamente anche questa è una scelta possibile, e molto ben studiata in letteratura, che prende il nome di [__Elastic-Net__](https://en.wikipedia.org/wiki/Elastic_net_regularization).
    ///
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Approcci lineari a metodi non lineari

    Un concetto fondamentale da apprendere quando si trattano problemi di regressione nel mondo reale è che i metodi lineari possono essere utilizzati anche per risolvere problemi in cui la relazione tra input ed output può essere non lineare. Al fine di riuscirci è però necessario il nostro intervento. Vediamo un esempio.

    Immaginiamo di aver osservato l'andamento nel tempo di una certa grandezza, di aver raccolto i dati e di aver osservato il seguente andamento.
    """
    )
    return


@app.cell
def _(np):
    t1 = np.linspace(0, 10, 100)
    sin_t1 = np.sin(2 * np.pi * t1)
    t1_sq = -0.1 * t1**2
    noise = 0.2 * np.random.randn(len(t1))

    y_t1 = sin_t1 + t1_sq + noise
    return t1, y_t1


@app.cell
def _(mo, pd, px, t1, y_t1):
    df_t = pd.DataFrame({"t": t1, "y_t": y_t1})

    fig3 = px.scatter(x=t1, y=y_t1)
    fig3.update_layout(xaxis_title=r"$t$", yaxis_title=r"$y_t$")

    mo.carousel([fig3, df_t])
    return (df_t,)


@app.cell
def _(mo):
    mo.md(
        """La relazione tra $t$ ed $y_t$ è chiaramente non lineare. Proviamo a vedere che tipo di predizione otterremmo utilizzando comunque $OLS$ (approccio naïve)."""
    )
    return


@app.cell
def _(LinearRegression, df_t):
    ols = LinearRegression(fit_intercept=False)
    ols.fit(df_t[["t"]], df_t["y_t"])
    df_t["y_t_naive"] = ols.predict(df_t[["t"]])

    fig4 = df_t[["t", "y_t", "y_t_naive"]].set_index("t").plot()
    fig4.update_layout(title=f"Mean absolute error: {((df_t['y_t'] - df_t['y_t_naive']).abs()).mean():.2f}")
    return (ols,)


@app.cell
def _(mo):
    mo.md(
        r"""
    Questo modello evidentemente non performa bene.

    Spingiamoci oltre, cosa notiamo nei dati raccolti? La variabile target $y_t$ ha due diversi andamenti. Uno, che possiamo genericamente definire _decrescente_ ed un altro che chiameremo _ondulatorio_. Entrambi gli andamenti __non__ sono correttamente catturati dal modello naïve.

    Proviamo quindi a capire come fornire questo genere di informazione al modello. Costruire nuovi predittori sulla base di quelli raccolti non solo è sempre possibile, ma è anche una compito fondamentale del data scientist, tanto da avere un nome: __feature engineering__.

    Per introdurre la componente decrescente, quale funzione scegliamo?
    """
    )
    return


@app.cell
def _(mo, np):
    func_1 = mo.ui.dropdown(
        options={
            "log(1+t)": np.log1p,
            "√t": np.sqrt,
            "-t": lambda t: -t,
            "-t^2": lambda t: -(t**2),
        },
        value="log(1+t)",  # initial value
        label="Componente decrescente:",
    )
    func_1
    return (func_1,)


@app.cell
def _(mo):
    mo.md(r"""Per introdurre la componente oscillatoria possiamo utilizzare seni e/o coseni. Quale scegliamo?""")
    return


@app.cell
def _(mo, np):
    func = mo.ui.dropdown(
        options={
            "cos(2πt)": np.cos,
            "sin(2πt)": np.sin,
        },
        value="cos(2πt)",  # initial value
        label="Componente oscillatoria:",
    )
    func
    return (func,)


@app.cell
def _(df_t, func, func_1, mo, np, ols):
    df_t["decr"] = func_1.value(df_t["t"].values)
    df_t["oscill"] = func.value(2 * np.pi * df_t["t"])

    ols.fit(df_t[["decr", "oscill"]], df_t["y_t"])
    df_t["y_t_pred"] = ols.predict(df_t[["decr", "oscill"]])

    fig5 = df_t[["t", "y_t", "y_t_pred", "y_t_naive"]].set_index("t").plot()
    fig5.update_layout(title=f"Mean absolute error: {((df_t['y_t'] - df_t['y_t_pred']).abs()).mean():.2f}")

    mo.carousel([fig5, df_t])
    return


@app.cell
def _(func, func_1, mo, ols):
    mo.md(
        f"""Il modello scelto è: y = f(X) = {func_1.selected_key} · ({ols.coef_[0]:.2f}) + {func.selected_key} · {ols.coef_[1]:.2f}"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Metodi non-lineari

    Tra i possibili approcci alla regressione basati su metodi non-lineari (_ie_ dove non ha quindi senso parlare di coefficienti associati ai predittori) spicca per semplicità e diffusione la famiglia dei __decision trees__ (DT).

    Allenare un DT significa identificare una serie di divisioni (dette _split_) dei predittori in input $X$ le quali, considerate nel loro insieme, permettono di approssimare bene il target $\bm{y}$. Vediamo un esempio pratico.

    ### Decision-tree regression

    Riprendiamo il dataset precedente e proviamo, _senza calcolare nuove features_, ad allenare un DT sulla sola variabile temporale $t$. In questo contesto potremo controllare il numero di split, ovvero il numero di volte in cui viene identificata un intervallo del predittore al quale è associato un valor medio del target.
    """
    )
    return


@app.cell
def _(df_t, mo):
    n_samples_tree = len(df_t)

    max_depth = mo.ui.slider(start=1, stop=10, label="N°split", value=1)
    max_depth
    return (max_depth,)


@app.cell
def _(DecisionTreeRegressor, max_depth):
    tree = DecisionTreeRegressor(max_depth=max_depth.value)
    return (tree,)


@app.cell
def _(df_t, mo, plot_tree, tree):
    df_t["y_pred_tree"] = tree.fit(df_t[["t"]], df_t["y_t"]).predict(df_t[["t"]])

    fig6 = df_t[["t", "y_t", "y_pred_tree"]].set_index("t").plot()
    fig6.update_layout(title=f"Mean absolute error: {((df_t['y_t'] - df_t['y_pred_tree']).abs()).mean():.2f}")

    mo.carousel(
        [
            fig6,
            plot_tree(
                tree,
                filled=False,
                rounded=True,
                feature_names=["t"],
                class_names=["y_t"],
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    /// tip | "Ensemble methods"

    Un grande punto di forza dei DT è la velocità con cui è possibile allenarli, anche in presenza di molti predittori e di molti samples. Questo li rende dei perfetti candidati per fungere da _base learner_ di metodi _ensemble_. Questi metodi, combinando insieme le predizioni effettuate da tantissimi DT allenati su porzioni diverse del dataset, implementano la cossidetta __wisdom of the croud__.
    ///

    ## Training error _vs_ test error

    Siamo arrivati all'ultima tappa del nostro breve excursus sulla regressione. Fino a questo momento abbiamo adottato un approccio qualitativo nel valutare la bontà delle nostre predizioni. Ovviamente nei casi reali questo non è sufficiente, è infatti necessario __misurare__ la bontà della predizione. Per farlo è necessario ricorrere a delle _metriche_, ovvero delle misure di prossimità tra le nostre predizioni $\hat{y}_i$ ed i target $y_i$.

    Una metrica spesso utilizzata è il _mean absolute error_ (MAE) definito come

    $$
        \text{MAE}(\hat{\bm{y}}, \bm{y}) = \frac{1}{n}\sum_{i=1}^n|\hat{y}_i - y_i|
    $$

    misura che è anche possibile esprimere in termini _relativi_ come _mean absolute **percentage** error_ (MAPE)

    $$
        \text{MAPE}(\hat{\bm{y}}, \bm{y}) = \frac{1}{n}\sum_{i=1}^n\frac{|\hat{y}_i - y_i|}{\max(\epsilon, |y_i|)}
    $$

    dove $\epsilon$ è semplicemente un numero piccolo strettamente positivo che fa sì di non incappare in divisioni per zero.

    /// tip | Comunicare con il business

    La mera misura dell'errore di predizione spesso non è sufficiente, il business infatti potrebbe non riuscire a comprendere cosa significhi un MAE 7 o un MAPE del 5%. Sarà quindi nostro compito tradurre l'errore di misura in una grandezza facilmente comprensibile per i nostri clienti business (tipicamente, in €).
    ///

    Poniamoci ora in caso realistico, siamo i data scientist di un'azienda che vende pubblicità online. Abbiamo raccolto nel tempo una serie di misure $X$ che ben descrivono i nostri clienti. Per ottimizzare il nostro motore di Ads ci serve predire il numero medio di secondi $\bm{y}$ che il cliente passa sulle nostre pagine sponsorizzate. Per ogni secondo non correttamente previsto la mancata revenue è stimata attorno ai 100€.

    Come possiamo muoverci?
    """
    )
    return


@app.cell
def _(np, pd, train_test_split):
    n_full = 500
    np.random.seed(42)
    X_full = np.random.uniform(1e-3, 10, n_full).reshape(-1, 1)
    y_full = 5 + (np.sin(2 * np.pi * X_full.ravel()) / np.sqrt(X_full.ravel())) + 0.25 * np.random.randn(n_full)

    X_train, X_test, y_train, y_test = train_test_split(X_full, y_full, test_size=400, random_state=42)

    df_train = pd.DataFrame({"x": X_train.ravel(), "y": y_train})
    df_test = pd.DataFrame({"x": X_test.ravel(), "y": y_test})
    return X_test, X_train, df_test, df_train, n_full, y_train


@app.cell
def _(df_train):
    df_train[["x", "y"]]
    return


@app.cell
def _(DecisionTreeRegressor, X_train, df_train, y_train):
    tree2 = DecisionTreeRegressor(max_depth=20)
    tree2.fit(X_train, y_train)
    df_train["y_pred"] = tree2.predict(X_train)
    return (tree2,)


@app.cell
def _(mo):
    mo.md(
        """
    ```python
    decision_tree = DecisionTreeRegressor(max_depth=20)
    decision_tree.fit(X, y)
    y_pred = decision_tree.predict(X)
    mancata_revenue = 100 * np.sum(np.abs(y - y_pred))
    ```
    """
    )
    return


@app.cell
def _(df_train, go, mae, n_full, np, tree2):
    xaxis = np.linspace(df_train["x"].min(), df_train["x"].max(), n_full)
    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(x=df_train["x"], y=df_train["y"], mode="markers", name=r"$y_i$"))

    fig7.add_trace(go.Scatter(x=xaxis, y=tree2.predict(xaxis.reshape(-1, 1)), name=r"$\hat{y}$"))
    fig7.update_layout(
        xaxis_title=r"$x_i$",
        yaxis_title=r"$y_i$",
        title=f"MAE = {mae(df_train['y'], df_train['y_pred']):.3f} s | mancata revenue: {100 * ((df_train['y'] - df_train['y_pred']).abs()).sum():.0f} €",
    )
    fig7
    return (xaxis,)


@app.cell
def _(mo):
    mo.md(
        r"""Soddisfatti del risultato, mandiamo il modello in produzione. Passa il tempo ed iniziano ad arrivare nuovi dati, ad un mese di distanza la situazione cambia drasticamente."""
    )
    return


@app.cell
def _(X_test, df_test, df_train, go, mae, tree2, xaxis):
    df_test["y_pred"] = tree2.predict(X_test)

    fig8 = go.Figure()
    fig8.add_trace(go.Scatter(x=df_train["x"], y=df_train["y"], mode="markers", name=r"$y_i$"))

    fig8.add_trace(go.Scatter(x=df_test["x"], y=df_test["y"], name=r"$y_i$", mode="markers"))

    fig8.add_trace(go.Scatter(x=xaxis, y=tree2.predict(xaxis.reshape(-1, 1)), name=r"$\hat{y}$"))

    fig8.update_layout(
        xaxis_title=r"$x_i$",
        yaxis_title=r"$y_i$",
        title=f"MAE = {mae(df_test['y'], df_test['y_pred']):.3f} s | mancata revenue: {100 * ((df_test['y'] - df_test['y_pred']).abs()).sum():.0f} €",
    )
    fig8
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Cosa è successo? Quali meccanismi avrei potuto mettere in atto per mitigare questo problema?

    Quello che abbiamo osservato in questo esempio giocattolo è il più classico dei casi di __overfit__. La stima dell'errore di cui dobbiamo corredare il nostro modello allenato non è quella calcolata sui dati sui quali il modello è stato allenato, quanto quella sui dati __futuri__ che il modello potrà incontrare una volta messo in produzione. Ma, in quanto _futuri_, quei dati non sono disponibili al momento dell'allenamento. Come possiamo uscire da questo impasse?

    In letteratura esistono molte tecniche per stimare l'__errore di generalizzazione__ dei modelli predittivi. Queste tecniche condividono una strategia base, ovvero i dati a propria disposizione vegnono iterativamente divisi in due gruppi, detti _training_ e _test_ set. Fingendo di non conoscere il test set, il modello sotto esame viene allenato sul training set e valutato sul test set. Tale procedura è ripetuta iterativamente, ogni volta estraendo a caso i sample da far appartenere ai due gruppi. Gli errori compiuti nelle varie iterazioni vengono poi mediate. Queste strategie prendono il nome di __cross-validation__.

    Come sempre scikit-learn ci aiuta ed implementa questa tecnica, vedi snippet seguente.

    ```python
    from sklearn.model_selection import cross_val_score

    decision_tree = DecisionTreeRegressor(max_depth=20)
    scores = cross_val_score(decision_tree, X_train, y_train, scoring='neg_mean_absolute_error')
    print(-1 * np.mean(scores))
    ```
    """
    )
    return


@app.cell
def _(DecisionTreeRegressor, X_train, cross_val_score, mo, np, y_train):
    tree3 = DecisionTreeRegressor(max_depth=20)
    scores = cross_val_score(tree3, X_train, y_train, scoring="neg_mean_absolute_error")
    mo.md(f"`{-1 * np.mean(scores)}`")
    return (scores,)


@app.cell
def _(mo):
    mo.md(
        r"""Questa stima dell'errore medio è molto più in linea con quella ottenuta empiricamente sui dati del mese successivo e, noto il numero di utenti per il prossimo mese, ci avrebbe permesso una stima migliore della mancata revenue."""
    )
    return


@app.cell
def _(mo):
    n_users_next_month = mo.ui.slider(start=100, stop=400, label="N° utenti prossimo mese")
    n_users_next_month
    return (n_users_next_month,)


@app.cell
def _(mo, n_users_next_month, np, scores):
    mo.md(
        f"""Mancata revenue stimata: {(-1 * np.mean(scores)):.3f} x {n_users_next_month.value} = {(100 * -1 * np.mean(scores) * n_users_next_month.value):.0f} €"""
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    /// tip | Approfondimenti & link utili

            - [📖 The Elements of Statistical Learning](https://www.sas.upenn.edu/~fdiebold/NoHesitations/BookAdvanced.pdf)

            - [🖥️ Linear Models - scikit-learn](https://scikit-learn.org/1.6/modules/linear_model.html)

            - [🌴 Decision trees - scikit-learn](https://scikit-learn.org/1.6/modules/tree.html)

            - [🌳 Ensemble methods - scikit-learn](https://scikit-learn.org/1.6/modules/ensemble.html)

            - [📐 Metrics - scikit-learn](https://scikit-learn.org/stable/modules/model_evaluation.html)

            - [🧣 Overfit - scikit-learn](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html#underfitting-vs-overfitting)
    ///
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
