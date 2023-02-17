import logging
from random import *
from pygeoapi.process.base import BaseProcessor
import docker
import traceback
import uuid
import json
from urllib.request import urlopen
import validators
import os

#curl -X POST "http://localhost:5000/processes/cia/execution" -H "Content-Type: application/json" -d "{\"mode\": \"async\", \"inputs\":{\"hazard\": \"earthquake\", \"country\": \"ecuador\", \"intensity\": \"https://riesgos.52north.org/shakemap_example.xml\"}}"

LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.0.1',
    'id': 'cia',
    'title': {
        'en': 'cia'
    },
    'description': {
        'en': 'Test process for testing docker in conjuction with pygeoapi, Docker and RIESGOS'
    },
    'keywords': ['RIESGOS', 'Earthquake'],
    'links': [{
        'type': 'text/html',
        'rel': 'about',
        'title': 'information',
        'href': 'https://example.org/process',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'hazard': {
            'title': 'hazard',
            'description': 'hazard to analyse',
            'schema': {
                'type': 'String'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,
            'keywords': ['hazard']
        },
        'country': {
            'title': 'country',
            'description': 'country to analyse',
            'schema': {
                'type': 'String'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,
            'keywords': ['country']
        },
        'intensity': {
            'title': 'intensity',
            'description': 'remote path to a shakemap.xml',
            'schema': {
                'type': 'String'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,
            'keywords': ['intensity']
        }
    },
    'outputs': {
        'result': {
            'title': 'Result',
            'description': 'Result as .geojson-File',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'test': 'some value',
            'directory': 'someabsolutepath'
        }
    }
}


class ciaProcessor(BaseProcessor):
    """Test Processor example"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.test.TestProcessor
        """
        self.id =  str(uuid.uuid4()) #generate job id
        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):
        
        mimetype = 'application/json'

        #define evironment variables from request
        environment = ["id="+self.id, "hazard="+data["hazard"], "country="+data["country"]] 

        try:
            #initialize docker client
            client = docker.from_env() 
            print("RIESGOS - Docker-Client:" , client)
        except Exception:
            print("RIESGOS - Docker-Client could not be started!")
            traceback.print_exc()
        try:
            #initialize directories and input files from environment
            resultDirectory = os.environ['ouputDir']
            inputDirectory = os.environ['inputDir']
            inputs = data["intensity"]
            response = urlopen(inputs) #read remote inputs
            input = response.read() #parse input

            try:
                #store input file
                inputFile = open("inputs/" + self.id + "shakemap.xml", "wb") 
                inputFile.write(input)
                inputFile.close()
                print("RIESGOS - Remote inputs read!")
            except Exception:
                print("RIESGOS - Remote inputs could not be read!")
                traceback.print_exc()

            #start container
            container = client.containers.run("tum_era_cia", "sleep infinity", 
            detach=True, 
            environment=environment, 
            volumes={str(resultDirectory): {'bind': '/usr/share/git/system_reliability/outputs', 'mode': 'rw'},
            str(inputDirectory): {'bind': '/usr/share/git/system_reliability/inputs', 'mode': 'rw'}}) 

            try: 
                #run commands in container
                container.exec_run('/bin/sh') #start shell
                #run process
                command = 'python3 run_analysis.py --intensity_file inputs/' + self.id + 'shakemap.xml ' + ' --country ' + data["country"] + ' --hazard ' + data["hazard"] + ' --output_file outputs/' + self.id + '.geojson'
                resultData = container.exec_run(command, detach=False) #execute process
                container.stop() #stop container
                container.remove() #remove container
                print("RIESGOS - Process ran on container!")
                os.remove('inputs/' + self.id + 'shakemap.xml') #clean input directory
            except Exception:
                print("RIESGOS - Process could not be started!")
                traceback.print_exc()
        except Exception: 
            print("RIESGOS - Docker-Container could not be started!")
            traceback.print_exc()
        #generate output of pygeoapi
        try:
            #open result file
            result = open('results/' + self.id + '.geojson')
            dataResult = json.load(result) #load result data
            outputs = dataResult #initialize output
            os.remove('results/' + self.id + '.geojson') #clean output directory
            print("RIESGOS - Process finished!")
            return mimetype, outputs #return output
        except Exception:
            print("RIESGOS - Outputs could not be found!")
            traceback.print_exc()

    def __repr__(self):
        return '<ciaProcessor> {}'.format(self.name)