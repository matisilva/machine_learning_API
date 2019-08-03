import pandas as pd
import pickle
from utils import timed, RowIterator
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from settings.titanic.settings import *
from .default import DefaultModel


def CalculateAge(dataframe):
    dataframe['Title'] = dataframe.Name.apply(
        lambda name: name.split(',')[1].split('.')[0].strip())
    dataframe.Title = dataframe.Title.map(NORMALIZED_TITLES)
    grouped = dataframe.groupby(['Sex', 'Pclass', 'Title'])
    dataframe.Age = grouped.Age.apply(lambda x: x.fillna(x.median()))
    grouped.Age.median()
    return (dataframe)


def CalclateFamilySize(dataframe):
    dataframe['FamilySize'] = dataframe['SibSp'] + dataframe['Parch'] + 1
    dataframe['Embarked'].fillna(value='S', inplace=True)
    return(dataframe)


class TitanicModel(DefaultModel):
    def __init__(self):
        self.model_name = 'titanic'
        super(TitanicModel, self).__init__()

    def build(self):
        self.model = RandomForestClassifier(n_estimators=270)
        self.logger.info("TitanicModel built")
        return self.model

    def parse(self, data, vectorizer=None):
        if isinstance(data, list):
            data = pd.DataFrame.from_dict(data)
        if not isinstance(data, pd.core.frame.DataFrame):
            raise NotImplementedError
        data = CalculateAge(data)
        data = CalclateFamilySize(data)
        d_features = data[FEATURES]
        if hasattr(self, "vectorizer"):
            x_train = self.vectorizer.transform(d_features)
        else:
            self.logger.debug("Building vectorizer")
            self.vectorizer = make_pipeline(RowIterator(), DictVectorizer())
            x_train = self.vectorizer.fit_transform(d_features)
        y_train = None
        self.logger.debug("Shape features {}".format(x_train.shape))
        if hasattr(data, "Survived"):
            y_train = data.Survived
            self.logger.debug("Shape labels {}".format(y_train.shape))
        return x_train, y_train

    @timed
    def fit(self, data):
        if self.model is None:
            self.logger.error("No model built yet")
            raise NotImplementedError
        x_train, y_train = self.parse(data)
        self.model.fit(x_train, y_train)
        self.logger.info("TitanicModel fitted")
        return self.model

    @timed
    def predict(self, data):
        if self.model is None:
            raise NotImplementedError
        data, _ = self.parse(data)
        preds = self.model.predict(data)
        preds = ['Survived' if p else 'Dead' for p in preds]
        return preds

    def save(self):
        if self.model is None:
            self.logger.info("No model to save")
            return
        model = (self.model, self.vectorizer)
        pickle.dump(model, open(self.filename, 'wb'))
        self.logger.info("Model saved")

    def load(self):
        with open(self.filename, 'rb') as f:
            self.model, self.vectorizer = pickle.load(f)
            self.logger.info("Model loaded")
        return self.model
