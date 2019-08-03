import os
import logging
import pandas as pd


class Dataset(object):
    def __init__(self):
        super(Dataset, self).__init__()
        self.train = None
        self.test = None


class DefaultModel(object):
    def __init__(self):
        super(DefaultModel, self).__init__()
        self.dataset = Dataset()
        self.model = None
        self.logger = logging.getLogger('model')
        self.filename = "./model_checkpoints/{}.pickle".format(self.model_name)
        self.train_file = './datasets/{model}/train.csv'.format(
            model=self.model_name)
        self.test_file = './datasets/{model}/test.csv'.format(
            model=self.model_name)

    def load_dataset_if_exists(self):
        if not os.path.exists(self.train_file):
            self.logger.info("No training file in {}".format(self.train_file))
        else:
            self.dataset.train = pd.read_csv(self.train_file)
        if not os.path.exists(self.test_file):
            self.logger.info("No test file in {}".format(self.test_file))
        else:
            self.dataset.test = pd.read_csv(self.test_file)
        return self.dataset

    def build(self):
        raise NotImplementedError

    def fit(self, data):
        raise NotImplementedError

    def predict(self, data):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        raise NotImplementedError

    def load(self, *args, **kwargs):
        raise NotImplementedError
