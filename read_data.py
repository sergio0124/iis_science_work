import pandas as pd

economy_file = "dataset/countries_of_the_world.csv"
population_file = "dataset/world_population.csv"
mixed_data_file = "dataset/mixed_data.csv"


def read_csv(filename):
    return pd.read_csv(filename).dropna()


def mix_data():
    pop_data_set = read_csv(population_file)
    econ_data_set = read_csv(economy_file)[
        ['Country', 'GDP ($ per capita)', 'Literacy (%)', 'Infant mortality (per 1000 births)']]
    econ_data_set = econ_data_set.dropna()
    econ_data_set['Country'] = econ_data_set['Country'] \
        .apply(lambda x: x.rstrip())
    econ_data_set['Literacy (%)'] = econ_data_set['Literacy (%)'] \
        .apply(lambda x: float(x.replace(',', '.')))
    econ_data_set['Infant mortality (per 1000 births)'] = econ_data_set['Infant mortality (per 1000 births)'] \
        .apply(lambda x: float(x.replace(',', '.')))

    result_dataset = pd.merge(pop_data_set, econ_data_set, on='Country')
    return result_dataset


def save_data(dataset, file_name):
    dataset.to_csv(file_name)


def check_data():
    missed = []
    pop_data_set = read_csv(population_file)
    econ_data_set = read_csv(economy_file)[
        ['Country', 'GDP ($ per capita)', 'Literacy (%)', 'Infant mortality (per 1000 births)']]
    econ_data_set = econ_data_set.dropna()
    econ_data_set['Country'] = econ_data_set['Country'] \
        .apply(lambda x: x.rstrip())
    for i in range(len(pop_data_set)):
        cur_country = pop_data_set.loc[i].Country
        if len(econ_data_set[econ_data_set['Country'] == cur_country]) == 0:
            missed.append(cur_country)
    print(len(missed))
    print(missed)


print(len(read_csv(mixed_data_file)))
