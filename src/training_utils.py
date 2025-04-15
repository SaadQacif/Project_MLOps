import numpy as np
import pandas as pd


def read_and_encode(path, encoder, rows=None):
    df = pd.read_csv(path, nrows=rows)
    df['converted_label'] = encoder.fit_transform(df['label'])
    return df


def fit(df, pipeline):
    x = np.array(df.iloc[:, :-2])

    y = np.array(df['converted_label'])

    pipeline.fit(x, y)


def test(df, pipeline):

    test_x = np.array(df.iloc[:, :-2])
    test_y = np.array(df.loc[:,'converted_label'])

    results = pipeline.predict(test_x) == test_y
    total = results.shape[0]
    passed = np.sum(results)
    return passed, total

