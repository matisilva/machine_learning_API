import logging
from models.titanic import TitanicModel
from flask import Flask, Response, jsonify, request
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s \
    %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


# Wrappers
class EndpointAction(object):

    def __init__(self, action, *args, **kwargs):
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.response = Response(status=200, headers={})

    def __call__(self):
        return self.action(self.args, self.kwargs)


class Service(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None,
                     handler=None, methods=["GET"], *args, **kwargs):
        self.app.add_url_rule(endpoint,
                              endpoint_name,
                              EndpointAction(handler, *args, **kwargs),
                              methods=methods)


# Views
def titanic(args, kwargs):
    titanic = kwargs.get("model")
    try:
        prediction = titanic.predict(request.json)
    except Exception as e:
        logging.error(e)
        return Response("Bad Parameters",
                        status=422,
                        mimetype='application/json')
    return jsonify(prediction)


def index(args, kwargs):
    return "Hello world"


# App
service = Service('ML-API')
service.add_endpoint(endpoint='/', endpoint_name='index', handler=index)
models = [TitanicModel()]
for model in models:
    model.load()
    view = locals()[model.model_name]
    service.add_endpoint(endpoint='/{}'.format(model.model_name),
                         endpoint_name=model.model_name,
                         handler=view,
                         methods=["POST", "HEAD", "OPTIONS"],
                         model=model)
app = service.app


if __name__ == "__main__":
    service.run()
