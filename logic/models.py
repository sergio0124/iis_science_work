import pandas
from sklearn.model_selection import train_test_split
from scipy.cluster import hierarchy
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures


def generate_test(X, y):
    return train_test_split(X, y, test_size=.4)


def get_model(data, method):
    clusters = hierarchy.linkage(data[['Density (per km²)', 'Growth Rate']], method=method)
    return clusters


# Создаём линейную регрессию
# Считаем точность
def linear_regression(x_data, y_data):
    x_train_data, x_test_data, y_train_data,  y_test_data = generate_test(x_data, y_data)

    linear_model = LinearRegression()
    linear_model.fit(x_train_data, y_train_data)
    yp = linear_model.predict(x_test_data)
    linear_model_score = r2_score(y_test_data, yp)
    return linear_model, linear_model_score


# Создаем полиномиальную регрессию
# высчитываем точность.
def polynomial_regression(x_data, y_data):
    x_train_data, x_test_data, y_train_data,  y_test_data = generate_test(x_data, y_data)

    polynomial_model = PolynomialFeatures(degree=5)
    linear = LinearRegression()
    pipeline = Pipeline(
        [("polynomial_features", polynomial_model), ("linear_regression", linear)])
    pipeline.fit(x_train_data, y_train_data)
    yp = pipeline.predict(x_test_data)
    polynomial_model_score = r2_score(y_test_data, yp)

    return pipeline, polynomial_model_score


# В задании была гребневая полиномиальная регрессия, способ создания я на-
# шел через пайплайн. Оцениваем его через специальную функцию в пакете sklearn
def ridge_regression(x_data, y_data):
    x_train_data, x_test_data, y_train_data,  y_test_data = generate_test(x_data, y_data)

    polynomial_model = PolynomialFeatures(degree=5)
    ridge = Ridge(alpha=1.0)
    pipeline = Pipeline(
        [("polynomial_features", polynomial_model), ("ridge_regression", ridge)])
    pipeline.fit(x_train_data, y_train_data)
    yp = pipeline.predict(x_test_data)
    pipeline_score = r2_score(y_test_data, yp)
    return pipeline, pipeline_score

