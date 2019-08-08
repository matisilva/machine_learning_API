import logging
import requests
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s \
    %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def make_sample_request():
    url = "http://0.0.0.0:80/titanic"
    payload = [{
        "PassengerId": 892,
        "Pclass": 3,
        "Name": "Kelly, Mr. James",
        "Sex": "male",
        "Age": 34.5,
        "SibSp": 0,
        "Parch": 0,
        "Ticket": 330911,
        "Fare": 7.8292,
        "Cabin": "",
        "Embarked": "Q"
    }, {
        "PassengerId": 892,
        "Pclass": 3,
        "Name": "Jhona, Mrs. Jerna",
        "Sex": "female",
        "Age": 14,
        "SibSp": 0,
        "Parch": 0,
        "Ticket": 330911,
        "Fare": 7.8292,
        "Cabin": "",
        "Embarked": "Q"
    }]
    response = requests.post(url,
                             json=payload)
    logging.info("Response {} ".format(response.text))


if __name__ == '__main__':
    make_sample_request()
