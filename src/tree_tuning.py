import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,  LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import training_utils as tr

MAX_DEPTH = 13
MIN_DEPTH = 1

models = [ DecisionTreeClassifier(max_depth=i) for i in range(MIN_DEPTH, MAX_DEPTH) ]
passed_per_feature_model = {
    'hog': [],
    'rgb': [],
}

encoder = LabelEncoder()
dataframes = {
    'hog': tr.read_and_encode("shared/hog_data_train.csv", encoder),
    'rgb': tr.read_and_encode("shared/rgb_data_train.csv", encoder)
}
test_dataframes = {
    'hog': tr.read_and_encode("shared/hog_data_test.csv", encoder),
    'rgb': tr.read_and_encode("shared/rgb_data_test.csv", encoder)
}

df = dataframes['hog']
tf = test_dataframes['hog']
for i, model in enumerate(models):

    clf = make_pipeline(StandardScaler(), model)
    clf.fit(df.iloc[:, :-2], df['converted_label'])
    passed, total = tr.test(tf, clf)
    passed_per_feature_model['hog'].append(passed)
    print(f"{i} out of {len(models)}")

df = dataframes['rgb']
tf = test_dataframes['rgb']
for i, model in enumerate(models):
    clf = make_pipeline(StandardScaler(), model)
    clf.fit(df.iloc[:, :-2], df['converted_label'])
    passed, total = tr.test(tf, clf)
    passed_per_feature_model['rgb'].append(passed)
    print(f"{i} out of {len(models)}")
    

fig, ax = plt.subplots()

ax.plot(range(MIN_DEPTH, MAX_DEPTH), passed_per_feature_model['hog'], marker='o', label='hog trained')
ax.plot(range(MIN_DEPTH, MAX_DEPTH), passed_per_feature_model['rgb'], marker='o', label='rgb trained')
ax.set_title('Passed test cases. HOG trained')
ax.set_xlabel('Depth')
ax.set_ylabel('Cases passed')
ax.legend()
plt.show()

