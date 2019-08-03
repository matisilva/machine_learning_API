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
Suppouse you want a model called `my_new_model`

1) Add a file `my_new_model.py` inside __models__ folder. There you can inherit 
from _DefaultModel_ such as _TitanicModel_ 
```python
class TitanicModel(DefaultModel):
```

2) Then you can add your settings inside __settings/my_new_model__ folder

3) (Optional) you can use __datasets__ folder and __scripts__ folder to place 
sample datasets for *fit* and *predict* and also scripts for testing 
respectively.

4) If you want to serve the model you only need one more step. 
Add your model inside in `service.py` 
Define one new view for the model..
```python
# Views
def my_new_model(args, kwargs):
    my_new_model = kwargs.get("model")
    try:
        prediction = my_new_model.predict(request.json)
    except Exception as e:
        logging.error(e)
        return Response("Bad Parameters",
                        status=422,
                        mimetype='application/json')
    return jsonify(prediction)
```

..and don't forget to initialize your model inside models variable.
```
# App
models = [..., MyNewModel()]
```

Then you will find it available to predict just in `/my_new_model>`


## How to scale my API?
First scale in `docker_compose.yml` adding new services as you want starting 
from a copy of *api* service.
```
  my_new_service:
    image: generic-ml-api
    build: ./
    command: "gunicorn --bind 0.0.0.0:5000 service:app"
    volumes: 
      - ./model_checkpoints:/src/model_checkpoints
      - ./datasets:/src/datasets
```

..then modify the file `nginx/nginx.conf` adding your new service there..

```
     upstream apis {
        server api:5000;
        server api2:5000;
        server my_new_service:5000;
     }

```
