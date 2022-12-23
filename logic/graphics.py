import math

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from scipy.cluster import hierarchy
from scipy.cluster import hierarchy as clust


def clear_data(data):
    data = data[['Country', 'Density (per km²)', 'Growth Rate']]
    columns = data.columns
    result = data
    for column in columns:
        if column != "Country":
            mean = data[column].mean()
            std = data[column].std()
            result = result.drop(result[result[column] > mean + std * 1.5].index)
            result = result.drop(result[result[column] < mean - std * 1.5].index)
    return result


def build_population_for_continents_by_countries(data_set):
    fig = Figure(figsize=(9, 6))
    ax = fig.subplots()

    column_index = data_set.columns.get_loc('1970 Population')
    x = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]
    year_columns_count = 8
    colors = ['#EDF10B', '#0070FF', '#FFB600', '#FF0000', '#CD00FF', "#00E348"]
    continents = ['Asia', 'Europe', 'Africa', 'Oceania', 'North America', 'South America']
    for i in range(len(colors)):
        data = data_set[data_set.Continent == continents[i]].sort_values(by=['World Population Percentage'],
                                                                         ascending=False).iloc[0:5]
        ax.plot([2022], [data.iloc[0][column_index - 7]], label=continents[i], color=colors[i])

        for j in range(len(data.index)):
            y = []
            for c in range(year_columns_count):
                y.append(data.iloc[j][column_index - c])
            ax.plot(x, y, color=colors[i])

    ax.legend()
    return fig


def build_population_for_continents_by_continents(data_set):
    fig = Figure(figsize=(9, 6))
    ax = fig.subplots()

    column_index = data_set.columns.get_loc('1970 Population')
    x = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]
    year_columns_count = 8
    colors = ['#EDF10B', '#0070FF', '#FFB600', '#FF0000', '#CD00FF', "#00E348"]
    continents = ['Asia', 'Europe', 'Africa', 'Oceania', 'North America', 'South America']

    data = data_set.groupby(['Continent'])[
        data_set.columns.values[column_index - year_columns_count + 1:column_index + 1]].apply(
        lambda rec: rec.astype(int).sum())
    data = data.sort_values(by=['Continent'])

    continents_colors = pd.DataFrame(data=continents, columns=["Continents"])
    continents_colors["colors"] = colors
    continents_colors = continents_colors.sort_values(by=["Continents"])
    colors = continents_colors["colors"].tolist()
    continents = continents_colors['Continents'].tolist()

    column_index = data.columns.get_loc('1970 Population')
    for i in range(len(data)):
        y = []
        for c in range(year_columns_count):
            y.append(data.iloc[i][column_index - c])
        ax.plot(x, y, color=colors[i], label=continents[i])

    ax.legend()
    return fig


def build_clusters(data_set, model, cluster_number, method):
    fig_histogram = Figure(figsize=(9, 6))
    ax_histogram = fig_histogram.subplots()
    fig_clusters = Figure(figsize=(9, 6))
    ax_clusters = fig_clusters.subplots()

    description = 'Hierarchical Clustering Dendrogram; number of clusters: {0}, linkage method: {1}'.format(
        cluster_number, method)
    cm = plt.cm.RdBu

    # Выведем все изначальные данные
    clusters = clust.fcluster(Z=model, t=cluster_number, criterion='maxclust')
    ax_clusters.scatter(
        data_set[['Density (per km²)']], data_set[['Growth Rate']], c=clusters, cmap=cm)
    ax_clusters.set_title(f"Representation of {cluster_number} clusters")
    ax_clusters.set_xlabel("Density (per km²)")
    ax_clusters.set_ylabel('Growth Rate')

    # Выведем дендрограмму
    ax_histogram.set_title(description)
    ax_histogram.set_ylabel('Euclidean Distance')
    hierarchy.dendrogram(model, truncate_mode='level', p=int(math.log2(cluster_number)), ax=ax_histogram)

    clusters_objects = []
    data_set["clusters"] = clusters
    for cluster in data_set['clusters'].unique():
        clusters_objects.append(
            f"cluster {cluster}:\n {str(data_set.loc[data_set['clusters'] == cluster][['Country']].values.tolist())}")

    return fig_clusters, fig_histogram, clusters_objects


def create_plot(model, score, x, y, title, column1, column2):
    fig = Figure(figsize=(9, 6))
    ax = fig.subplots()

    # Задаем цвет и в заголовок пишем название и оценку
    cm = plt.cm.RdBu
    ax.set_title(title + (', score is: %.5f' % score))

    # Получаем данные по x, сортируем и на основании predict рисуем график
    x_data = sorted(x.reshape(-1, 1))
    ax.plot(x_data, model.predict(x_data).reshape(-1, 1))

    ax.set_xlabel(column1)
    ax.set_ylabel(column2)

    # Выводим весь набор данных
    ax.scatter(
        x, y, cmap=cm)

    return fig
