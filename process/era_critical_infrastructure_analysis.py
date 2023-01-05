import logging
from random import *
from pygeoapi.process.base import BaseProcessor
import docker
import traceback
import uuid
import json


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.0.1',
    'id': 'cia',
    'title': {
        'en': 'cia'
    },
    'description': {
        'en': 'Test process for testing docker in conjuction with pygeoapi and RIESGOS'
    },
    'keywords': ['docker', 'test'],
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
            'description': 'absolute path to the intensity.xml',
            'schema': {
                'type': 'String'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,
            'keywords': ['intensity', 'mount']
        },
        'directory': {
            'title': 'directory',
            'description': 'Directory to be mounted to the container',
            'schema': {
                'type': 'String'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None, 
            'keywords': ['directory', 'mount']
        }
    },
    'outputs': {
        'result': {
            'title': 'Result',
            'description': 'the result of the test',
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

        #define evironment variables
        environment = ["id="+self.id, "hazard="+data["hazard"], "country="+data["country"]] 

        client = docker.from_env() #initialize docker client
        print("RIESGOS - Docker-Client:" , client)
        try:
            resultDirectory = data["directory"]
            inputDirectory = data["intensity"]
            print("RIESGOS - Results-Directory: ", resultDirectory)
            container = client.containers.run("tum_era_cia", "sleep infinity", 
            detach=True, 
            environment=environment, #add environmet variables
            volumes={resultDirectory: {'bind': '/usr/share/git/system_reliability/outputs', 'mode': 'rw'}, inputDirectory: {'bind': '/usr/share/git/system_reliability/inputs', 'mode': 'rw'}}) #mount specified directory
            try: 
                #run commands in container
                container.exec_run('/bin/sh') #start shell
                result = {"id": self.id}
                #with open('C:/Daten/Results/' + self.id +'.json', "w") as outfile:
                #    outfile.write(json.dumps(result, indent=4))
                command = 'python3 run_analysis.py --intensity_file inputs/shakemap.xml ' + ' --country ' + data["country"] + ' --hazard ' + data["hazard"] + ' --output_file outputs/' + self.id + '.geojson'
                print(command)
                resultData = container.exec_run(command, detach=False) #execute process
                container.stop() #stop container
                container.remove() #remove container
                print("RIESGOS - Process ran on container!")
            except Exception:
                print("RIESGOS - Process could not be started!")
                traceback.print_exc()
        except Exception: 
            print("RIESGOS - Docker-Container could not be started!")
            traceback.print_exc()
        #generate output of pygeoapi
        try:
            result = open(resultDirectory + '/' + self.id + '.geojson',)
            dataResult = json.load(result)
            outputs = dataResult
            print("RIESGOS - Process finished!")
            return mimetype, outputs #return output
        except Exception:
            traceback.print_exc()

    def __repr__(self):
        return '<ciaProcessor> {}'.format(self.name)