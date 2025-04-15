import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler,  LabelEncoder
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import training_utils as tr

model_names =[
    "SVC, poly kernel",
    "SVC, rbf kernel",
    "SVC, linear kernel",
    "Logistic regressor",
    "Decision tree",
]
models =[
    SVC(kernel='poly', gamma='auto'),
    SVC(kernel='rbf', gamma='auto'),
    SVC(kernel='linear', gamma='auto'),
    LogisticRegression(),
    DecisionTreeClassifier(max_depth=6),

]
passed_per_feature_model = {
    'hog': [],
    'rgb': [],
    'cr': [],
    'evr': [],
}

encoder = LabelEncoder()
dataframes = {
    'hog': tr.read_and_encode("shared/hog_data_train.csv", encoder),
    'rgb': tr.read_and_encode("shared/rgb_data_train.csv", encoder),
    'cr': tr.read_and_encode("shared/cr_data_train.csv", encoder),
    'evr': tr.read_and_encode("shared/evr_data_train.csv", encoder)
}
test_dataframes = {
    'hog': tr.read_and_encode("shared/hog_data_test.csv", encoder),
    'rgb': tr.read_and_encode("shared/rgb_data_test.csv", encoder),
    'cr': tr.read_and_encode("shared/cr_data_test.csv", encoder),
    'evr': tr.read_and_encode("shared/evr_data_test.csv", encoder)
}

df = dataframes['hog']
tf = test_dataframes['hog']
for i, model in enumerate(models):

    clf = make_pipeline(StandardScaler(), model)
    clf.fit(df.iloc[:, :-2], df['converted_label'])
    passed, total = tr.test(tf, clf)
    print(f"{passed} cases passed out of {total} cases")
    passed_per_feature_model['hog'].append(passed / total)

models = [sklearn.base.clone(model) for model in models]
df = dataframes['rgb']
tf = test_dataframes['rgb']
for i, model in enumerate(models):
    clf = make_pipeline(StandardScaler(), model)
    clf.fit(df.iloc[:, :-2], df['converted_label'])
    passed, total = tr.test(tf, clf)
    print(f"{passed} cases passed_svc_rgb out of {total} cases")
    passed_per_feature_model['rgb'].append(passed / total)
    
df = dataframes['cr']
tf = test_dataframes['cr']
for i, model in enumerate(models):

    clf = make_pipeline(StandardScaler(), model)
    clf.fit(df.iloc[:, :-2], df['converted_label'])
    passed, total = tr.test(tf, clf)
    print(f"{passed} cases passed out of {total} cases")
    passed_per_feature_model['cr'].append(passed / total)

df = dataframes['evr']
tf = test_dataframes['evr']
for i, model in enumerate(models):
    clf = make_pipeline(StandardScaler(), model)
    clf.fit(df.iloc[:, :-2], df['converted_label'])
    passed, total = tr.test(tf, clf)
    print(f"{passed} cases passed_svc_evr out of {total} cases")
    passed_per_feature_model['evr'].append(passed / total)
    

fig, ax = plt.subplots()

x = np.arange(len(models))
width = 0.5

ax.bar(x + 0 / len(dataframes) - (width / len(dataframes)) * (len(dataframes) * 0.5), passed_per_feature_model['hog'], width/len(dataframes), label='hog trained')
ax.bar(x + width / len(dataframes) - (width / len(dataframes)) * (len(dataframes) * 0.5), passed_per_feature_model['rgb'], width/len(dataframes), label='rgb trained')
ax.bar(x + 2 * width / len(dataframes) - (width / len(dataframes)) * (len(dataframes) * 0.5), passed_per_feature_model['cr'], width/len(dataframes), label='cr trained')
ax.bar(x + 3 * width / len(dataframes) - (width / len(dataframes)) * (len(dataframes) * 0.5), passed_per_feature_model['evr'], width/len(dataframes), label='evr trained')
ax.set_title('Passed test cases')
ax.set_xlabel('Model')
ax.set_xticks(x)
ax.set_xticklabels(model_names)
ax.set_ylabel('Cases passed')
ax.legend()
plt.show()

