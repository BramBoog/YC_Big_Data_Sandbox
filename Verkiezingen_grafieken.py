import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import inspect
import Verkiezingen_functies as verfuncs



def combineer_uitslagen_v15(df, n1=3, n2=3, optie_1=1, optie_2=2):
    """
    Combineert de 'zetel' kolommen van 2 functie returns naar keuze. Output is de gecombineerde dataframe plus de namen vd gekozen verdelingsleutels
    """
    opties_dict = {# dictionary dient als switch. Hiermee kan worden meegegeven welke functies worden geplot
        1: lambda df, n: verfuncs.landelijke_uitslag(df), 
        2: lambda df, n: verfuncs.landelijke_uitslag_top_n(df, n),
        3: lambda df, n: verfuncs.landelijke_uitslag_kiesmannen(df),
        4: lambda df, n: verfuncs.zetels_per_gewonnen_gemeente(df)
    }
    lijn = 4 # op welke regel staat 
    df_1 = opties_dict.get(optie_1)(df, n1)
    df_2 = opties_dict.get(optie_2)(df, n2)
    get_name = lambda optie, n: inspect.getsource(combineer_uitslagen_v15).split('\n')[optie+lijn].split(':')[-1].split('(')[0].strip().replace("_n", f"_{n}")
    naam1 = get_name(optie_1, n1)
    naam2 = get_name(optie_2, n2)
    col_naam1 = f"zetels obv {naam1}"
    col_naam2 = f"zetels obv {naam2}"
    df_combi = pd.concat([df_1['zetels'], df_2['zetels']], axis=1).replace(np.nan, 0)
    df_combi.columns = [col_naam1, col_naam2]
    return df_combi[(df_combi[col_naam1] != 0) | (df_combi[col_naam2] != 0)], naam1, naam2

def plot_landelijk_vs_top_n_v2(df, n1=3, n2=3, optie1=1, optie2=2, log=False):
    """
    Plot 2 verschillende zetelverdeelsleutels tegen elkaar.
    """
    combi_df, naam1, naam2 = combineer_uitslagen_v15(df, n1, n2, optie1, optie2)
    col1 = combi_df.columns[0]
    col2 = combi_df.columns[1]
    i = np.arange(0, len(list(combi_df.index))) #space the x axis labels
    width = 0.4

    fig, ax = plt.subplots(figsize=(10,5))
    fig.subplots_adjust(hspace = 1, wspace = .1)
    rects1 = ax.bar(i - width/2, height=combi_df[col1], width = width, label=naam1, color='teal')
    rects2 = ax.bar(i + width/2, height=combi_df[col2], width = width, label=naam2, color='black')

    ax.set_xticks(i, list(combi_df.index), rotation=90)
    if log: ax.set_yscale('log')
    plt.ylabel('zetels')
    plt.title('Zetelverdeling Tweede Kamer')
    ax.legend()

    ax.bar_label(rects1) # laat het aantal zien boven elke bar
    ax.bar_label(rects2)
    plt.close() # voorkomt dubbel print van grafiek
    return fig



def plot_uitslag(df):
    plt.figure(figsize=(15,10))                  # totale figuur
    plt.bar(df.index, df['zetels'] )             # data x & y as
    plt.xticks(rotation=90)                      # leesbaarheid x as labels (90 graden draaien)
    plt.title('Uitslag (totaal aantal zetels = ' + str(df['zetels'].sum()) + ')')
    plt.ylabel('Zetels')
    plt.plot()
