import pandas as pd
import numpy as np


def generate_data(n, k, x_min=0, x_max=10):
    # matrix_x = np.random.uniform(x_min, x_max, (n, k))
    matrix_x = np.random.normal(0.0, 1.0, (n, k))
    # matrix_x2 = np.random.normal(0.0, 1.0, (n, k))
    matrix_x2 = np.random.uniform(x_min, x_max, (n, k))

    # beta = np.random.uniform(-2, 2, (k, 1))
    beta = np.ones((k, 1)) * 11
    xbeta = matrix_x@beta
    correctie = 10.0 / (xbeta.max() - xbeta.min())
    beta *= correctie
    probs = 1 / (1+np.exp(-(matrix_x@beta)))
    y_var = np.zeros((n, 1))
    for i in range(n):
        y_var[i] = int((np.random.uniform(0, 1) < probs[i]) + 0)
    return pd.DataFrame(np.hstack((matrix_x, matrix_x2, y_var)))


data = generate_data(1000, 4)

data.to_csv(r'/Users/roos/Data/' + 'test_data.csv', index=False, header=True)
