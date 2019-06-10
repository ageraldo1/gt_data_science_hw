from flask_restful import Api,Resource
from init import create_app

app = create_app()
api = Api(app)

from resources.samples import Samples
from resources.metadata import Metadata
from resources.home import Home

api.add_resource(Samples, '/samples', '/samples/<string:sampleid>', '/samples/<string:sampleid>/<string:limit>')
api.add_resource(Metadata, '/metadata/<string:sampleid>')
api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

