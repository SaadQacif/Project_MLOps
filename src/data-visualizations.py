import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,  LabelEncoder
from sklearn.linear_model import LogisticRegression
import pandas as pd
import training_utils as tr

import os
import pickle
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve, average_precision_score, classification_report


# box plot rgb distributions
encoder = LabelEncoder()
df = tr.read_and_encode("shared/rgb_data_train.csv", encoder)
frame = [
                 np.array(df.query('label == "Healthy"')['mean_green']) / 255,
                 np.array(df.query('label == "Early Blight"')['mean_green']) / 255,
                 np.array(df.query('label == "Late Blight"')['mean_green']) / 255,
             ]
# print(frame[:5, :5])

labels = ['Healthy', 'Early Blight', 'Late Blight']
colors = ['peachpuff', 'orange', 'tomato']

fig, ax = plt.subplots()
ax.set_ylabel('green mean')

bplot = ax.boxplot(frame,
                   patch_artist=True,  # fill with color
                   tick_labels=labels)  # will be used to label x-ticks

# fill with colors
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

ax.set_ylim(0, 1)
plt.show()

frame = [
                 np.array(df.query('label == "Healthy"')['mean_red']) / 255,
                 np.array(df.query('label == "Early Blight"')['mean_red']) / 255,
                 np.array(df.query('label == "Late Blight"')['mean_red']) / 255,
             ]
# print(frame[:5, :5])

labels = ['Healthy', 'Early Blight', 'Late Blight']
colors = ['peachpuff', 'orange', 'tomato']

fig, ax = plt.subplots()
ax.set_ylabel('red mean')

bplot = ax.boxplot(frame,
                   patch_artist=True,  # fill with color
                   tick_labels=labels)  # will be used to label x-ticks

# fill with colors
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

ax.set_ylim(0, 1)
plt.show()

frame = [
                 np.array(df.query('label == "Healthy"')['mean_blue']) / 255,
                 np.array(df.query('label == "Early Blight"')['mean_blue']) / 255,
                 np.array(df.query('label == "Late Blight"')['mean_blue']) / 255,
             ]
# print(frame[:5, :5])

labels = ['Healthy', 'Early Blight', 'Late Blight']
colors = ['peachpuff', 'orange', 'tomato']

fig, ax = plt.subplots()
ax.set_ylabel('blue mean')

bplot = ax.boxplot(frame,
                   patch_artist=True,  # fill with color
                   tick_labels=labels)  # will be used to label x-ticks

# fill with colors
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

ax.set_ylim(0, 1)
plt.show()

df = tr.read_and_encode("shared/cr_data_train.csv", encoder)
frame = [
                 np.array(df.query('label == "Healthy"')['CR']),
                 np.array(df.query('label == "Early Blight"')['CR']),
                 np.array(df.query('label == "Late Blight"')['CR']),
             ]
# print(frame[:5, :5])

labels = ['Healthy', 'Early Blight', 'Late Blight']
colors = ['peachpuff', 'orange', 'tomato']

fig, ax = plt.subplots()
ax.set_ylabel('Convexity ratio')

bplot = ax.boxplot(frame,
                   patch_artist=True,  # fill with color
                   tick_labels=labels)  # will be used to label x-ticks

# fill with colors
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

ax.set_ylim(0, 1)
plt.show()

# encoder = pickle.load(open(f"{os.getcwd()}/bin/encoder.pkl", 'rb'))
# models_by_features = pickle.load(open(f"{os.getcwd()}/bin/models_by_features.pkl", 'rb'))

# test_dataframes = {
#     'hog': tr.read_and_encode("shared/hog_data_test.csv", encoder),
#     'rgb': tr.read_and_encode("shared/rgb_data_test.csv", encoder),
#     'cr': tr.read_and_encode("shared/cr_data_test.csv", encoder),
#     'evr': tr.read_and_encode("shared/evr_data_test.csv", encoder)
# }

# df = test_dataframes['rgb']

# X, y = df.iloc[:, :-2], df['converted_label']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# model = models_by_features['rgb']

# precision, recall, thresholds = precision_recall_curve(y_test, y_scores)
# average_precision = average_precision_score(y_test, y_scores)

# plt.figure(figsize=(8, 6))
# plt.plot(recall, precision, label=f'Precision-Recall Curve (AP = {average_precision:.2f})', color='blue')
# plt.xlabel('Recall')
# plt.ylabel('Precision')
# plt.title('Precision-Recall Curve')
# plt.legend()
# plt.grid()
# plt.show()

# print("Classification Report:")
# print(classification_report(y_test, model.predict(X_test)))
