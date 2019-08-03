import logging
import sys
import os
sys.path.append(os.path.abspath('.'))
from models.titanic import TitanicModel

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s \
    %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def test():
    model = TitanicModel()
    dataset = model.load_dataset_if_exists()
    if dataset.train is None:
        logging.error("No train found. Exiting")
        return
    model.build()
    model.fit(dataset.train)
    if dataset.test is None:
        logging.error("No test found. Exiting")
        return
    prediction1 = model.predict(dataset.test)
    model.save()
    del model
    model = TitanicModel()
    model.load()
    prediction2 = model.predict(dataset.test)
    assert prediction1 == prediction2, "Non deterministic model"


if __name__ == "__main__":
    test()
