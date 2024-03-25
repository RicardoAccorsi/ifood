import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
import os
import sys

from matplotlib.colors import ListedColormap
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from matplotlib.ticker import PercentFormatter

def inspecao_outliers(df, column, whisker_width=1.5):

    # quantiles
    q1 = df[column].quantile(.25)
    q3 = df[column].quantile(.75)

    # interquartil
    iqr = q3 - q1

    # limites inferior e superior
    lower_bound = q1 - whisker_width * iqr
    upper_bound = q3 + whisker_width * iqr

    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

def pairplot(dataframe, columns, hue_column=None, alpha=0.5, corner=True, palette="tab10"):
    analysis = columns.copy() + [hue_column]

    sns.pairplot(dataframe[analysis], diag_kind="kde", hue=hue_column, plot_kws=dict(alpha=alpha), corner=corner, palette=palette);


def elbow_silhouette(X, random_state=42, range_k=(2,11)):
    if not sys.warnoptions:
        warnings.simplefilter("ignore")
        os.environ["PYTHONWARNINGS"] = "ignore"
    
    elbow = {}
    silhouette = []
    
    n_range = range(*range_k)
    
    for i in n_range:
        # instancia do algoritmo
        kmeans = KMeans(n_clusters=i, random_state=random_state, n_init=10)
        
        # fit dos dados
        kmeans = kmeans.fit(X)
    
        # pegar infos para o elbow method
        elbow[i] = kmeans.inertia_
    
        # pegar infos para o silhouette score
        labels = kmeans.labels_
        silhouette.append(silhouette_score(X, labels))
        
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), tight_layout=True)
    
    sns.lineplot(x=list(elbow.keys()), y=list(elbow.values()), ax=axs[0])
    sns.lineplot(x=list(n_range), y=silhouette, ax=axs[1])
    
    axs[0].set_xlabel("K")
    axs[0].set_ylabel("Inertia")
    axs[0].set_title("Elbow Method")
    
    axs[1].set_xlabel("K")
    axs[1].set_ylabel("Silhouette Score")
    axs[1].set_title("Silhouette Method")
    
    plt.show()


def visualizar_clusters(dataframe, colunas, qtd_cores, centroids, mostrar_centroids=True, mostrar_pontos=False, coluna_clusters=None):

    fig = plt.figure(figsize=(12, 5))
    
    ax = fig.add_subplot(111, projection="3d")
    
    cores = plt.cm.tab10.colors[:qtd_cores]
    cores = ListedColormap(cores)
    
    x = dataframe[colunas[0]]
    y = dataframe[colunas[1]]
    z = dataframe[colunas[2]]
    
    for i, ponto in enumerate(centroids):
        if mostrar_centroids:
            ax.scatter(*ponto, s=500, alpha=.5)
            ax.text(*ponto, f"{i}", fontsize=20, horizontalalignment="center", verticalalignment="center")
    
        if mostrar_pontos:
            s = ax.scatter(x, y, z, c=coluna_clusters, cmap=cores)
            ax.legend(*s.legend_elements(), bbox_to_anchor=(1.4, 1))
    
    ax.set_xlabel(colunas[0])
    ax.set_ylabel(colunas[1])
    ax.set_zlabel(colunas[2])
    ax.set_title("Clusters")
    
    plt.show()


def cluster_percent(dataframe, colunas, rows_cols=(2, 3), figsize=(15, 8), column_cluster="cluster"):
    
    fig, axs = plt.subplots(*rows_cols, figsize=figsize, sharey=True)

    # lidando com o caso de visualizacao de uma unica coluna
    if not isinstance(axs, np.ndarray):
        axs = np.array(axs)
    
    for ax, col in zip(axs.flatten(), colunas):
        h = sns.histplot(dataframe, x=column_cluster, ax=ax, palette="tab10", hue=col, multiple="fill", stat="percent", discrete=True, shrink=.8)
    
        # pegar n de clusters
        n_clusters = dataframe[f"{column_cluster}"].nunique()
    
        # colocar ticks com n clusters
        h.set_xticks(range(n_clusters))
    
        # formatar escala para percentual
        h.yaxis.set_major_formatter(PercentFormatter(1))
    
        # eliminar label de y
        h.set_ylabel("")
    
        # tirar o s ticks da figura
        h.tick_params(axis="both", which="both", length=0)
    
        # colocar percentual em cada barra
        for bars in h.containers:
            h.bar_label(bars, label_type="center", labels=[f"{bar.get_height():.0%}" for bar in bars], color="white", weight="bold", fontsize=11)
    
        # tirar linha preta de divisao de cada barra
        for bar in h.patches:
            bar.set_linewidth(0)
    
    # ajustar espaçamento
    plt.subplots_adjust(hspace=.3, wspace=.3)
    
    plt.show()


def column_percent(dataframe, colunas, rows_cols=(2, 3), figsize=(15, 8), column_cluster="cluster"):
    
    fig, axs = plt.subplots(*rows_cols, figsize=figsize, sharey=True)

    # lidando com o caso de visualizacao de uma unica coluna
    if not isinstance(axs, np.ndarray):
        axs = np.array(axs)
    
    for ax, col in zip(axs.flatten(), colunas):
        h = sns.histplot(dataframe, x=col, ax=ax, palette="tab10", hue=column_cluster, multiple="fill", stat="percent", discrete=True, shrink=.8)
    
        # pegar n de categorias por coluna
        n_ticks = dataframe[col].nunique()
    
        # colocar ticks com n clusters
        h.set_xticks(range(n_ticks))
    
        # formatar escala para percentual
        h.yaxis.set_major_formatter(PercentFormatter(1))
    
        # eliminar label de y
        h.set_ylabel("")
    
        # tirar o s ticks da figura
        h.tick_params(axis="both", which="both", length=0)
    
        # colocar percentual em cada barra
        for bars in h.containers:
            h.bar_label(bars, label_type="center", labels=[f"{bar.get_height():.0%}" for bar in bars], color="white", weight="bold", fontsize=11)
    
        # tirar linha preta de divisao de cada barra
        for bar in h.patches:
            bar.set_linewidth(0)
    
        # pegar informação da legenda
        legend = h.get_legend()
        legend.remove()
    
    # colocar legenda a nível de figura
    labels = [text.get_text() for text in legend.get_texts()]
    fig.legend(handles=legend.legend_handles, labels=labels, loc="upper center", ncols=dataframe[column_cluster].nunique(), title="Clusters")
    
    # ajustar espaçamento
    plt.subplots_adjust(hspace=.3, wspace=.3)
    
    plt.show()


def show_clusters_2D(dataframe, colunas, qtd_cores, centroids, mostrar_centroids=True, mostrar_pontos=False, coluna_clusters=None):

    fig = plt.figure(figsize=(12, 5))
    
    ax = fig.add_subplot(111)
    
    cores = plt.cm.tab10.colors[:qtd_cores]
    cores = ListedColormap(cores)
    
    x = dataframe[colunas[0]]
    y = dataframe[colunas[1]]
    
    for i, ponto in enumerate(centroids):
        if mostrar_centroids:
            ax.scatter(*ponto, s=500, alpha=.5)
            ax.text(*ponto, f"{i}", fontsize=20, horizontalalignment="center", verticalalignment="center")
    
        if mostrar_pontos:
            s = ax.scatter(x, y, c=coluna_clusters, cmap=cores)
            ax.legend(*s.legend_elements(), bbox_to_anchor=(1.4, 1))
    
    ax.set_xlabel(colunas[0])
    ax.set_ylabel(colunas[1])
    ax.set_title("Clusters")
    
    plt.show()