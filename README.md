# Generic API wrapper for ML model deploy

## How to run the sample model [Titanic kaggle challenge]?
For the first time run you have to train the model. You can call..

```bash 
python scripts/test_titanic.py
```
.. to get the first model checkpoint and test the model save/load procedure.

Once you have the model pretrained you can now enable the server to receive the
requests and predict over them.

You only have to run

```bash
docker-compose up -d
```

## How to test the API?
Just run the following with the server online.
```bash
python request_titanic.py
```

If you want to send your data you could use also cURL as follows..
```bash
curl -X POST \
  http://0.0.0.0/titanic \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '[{
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
},
    ...
]'
```

..and the response will be ..

```bash
["Dead", ...]
```

## How to add new models to my API
TODO

## How to scale my API?
```bash
docker-compose scale API=5
```
