import sklearn
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler,  LabelEncoder
from sklearn.linear_model import LogisticRegression
import training_utils as tr
import pickle


model = LogisticRegression()
models_by_features = {}

encoder = LabelEncoder()

dataframes = {
    'hog': tr.read_and_encode("shared/hog_data_train.csv", encoder),
    'rgb': tr.read_and_encode("shared/rgb_data_train.csv", encoder)
}

df = dataframes['hog']
clf = make_pipeline(StandardScaler(), sklearn.base.clone(model))
clf.fit(df.iloc[:, :-2], df['converted_label'])
models_by_features['hog'] = clf

df = dataframes['rgb']
clf = make_pipeline(StandardScaler(), sklearn.base.clone(model))
clf.fit(df.iloc[:, :-2], df['converted_label'])
models_by_features['rgb'] = clf
    
# Pickle encoder
pickle.dump(encoder, open("bin/encoder.pkl", 'wb'))


# Pickle all models
pickle.dump(models_by_features, open("bin/models_by_features.pkl", 'wb'))
