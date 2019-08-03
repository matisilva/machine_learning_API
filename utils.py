import time
import logging
from sklearn.base import TransformerMixin
logger = logging.getLogger('timer')


class RowIterator(TransformerMixin):
    """ Prepare dataframe for DictVectorizer """
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return (row for _, row in X.iterrows())


def timed(func):
    def time_taken(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.debug("{} took {}".format(func.__name__,
                                         end - begin))
        return result
    return time_taken
