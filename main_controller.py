import os

import numpy as np
from flask import Flask, render_template, redirect, request, send_from_directory
from matplotlib.figure import Figure

from logic.data_forming import get_image
from logic.graphics import build_population_for_continents_by_countries, build_population_for_continents_by_continents, \
    build_clusters, clear_data, create_plot
from logic.models import get_model, linear_regression, polynomial_regression, ridge_regression
from read_data import read_csv

app = Flask(__name__)
mix_data_file = "dataset/mixed_data.csv"
economy_file = "dataset/countries_of_the_world.csv"
population_file = "dataset/world_population.csv"


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')


@app.route('/', methods=['GET', "POST"])
def redirect_home_to_hello():
    return redirect("/hello", code=302)


@app.route('/dataset', methods=['GET', 'POST'])
def get_dataset():
    data = read_csv(mix_data_file)
    return render_template('dataset.html', tables=[data.to_html(classes='data')], titles=data.columns.values)


@app.route('/pop_tendencies', methods=['GET'])
def show_population_tendencies():
    data = read_csv(mix_data_file)
    fig1 = build_population_for_continents_by_countries(data)
    image1 = get_image(fig1)
    fig2 = build_population_for_continents_by_continents(data)
    image2 = get_image(fig2)
    return render_template('pop_tendencies.html', image1=image1, image2=image2)


@app.route('/dendrogram', methods=['GET'])
def show_clusters():
    data = read_csv(mix_data_file)
    data = clear_data(data)
    method = request.args.get('method', default="single", type=str)
    number = request.args.get('count', default=4, type=int)
    model = get_model(data, method)
    ax_clusters, ax_histogram, clusters_objects = build_clusters(data, model, number, method)

    image1 = get_image(ax_histogram)
    image2 = get_image(ax_clusters)

    return render_template('dendrogram.html', image1=image1, image2=image2, clusters=clusters_objects)


@app.route('/regression', methods=['GET'])
def show_regressions():
    data = read_csv(mix_data_file)

    column1 = request.args.get('column1', default="2022 Population", type=str)
    column2 = request.args.get('column2', default="1970 Population", type=str)

    x_data = np.asarray(data[column1].tolist()).reshape(-1, 1)
    y_data = np.asarray(data[column2].tolist()).reshape(-1, 1)

    model_list = [linear_regression(x_data, y_data),
                  polynomial_regression(x_data, y_data),
                  ridge_regression(x_data, y_data)]
    names_list = ["Линейная регрессия", "Полиномиальная регрессия", "Ридж регрессия"]

    pictures = []
    # Через иттератор отрисовываем каждый график в сабплотах и потом выводим его
    for i in range(len(model_list)):
        figure = create_plot(model_list[i][0], model_list[i][1], x_data, y_data, names_list[i], column1, column2)
        pictures.append(get_image(figure))

    return render_template('regressions.html', image1=pictures[0], image2=pictures[1], image3=pictures[2])


if __name__ == '__main__':
    app.run(debug=True)
