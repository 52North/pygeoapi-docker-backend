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
    'id': 'dockerTest',
    'title': {
        'en': 'dockerTest'
    },
    'description': {
        'en': 'Test process for testing docker in conjuction with pygeoapi'
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
        'test': {
            'title': 'Test Value',
            'description': 'Just a value',
            'schema': {
                'type': 'int'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,
            'keywords': ['test']
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


class DockerTestProcessor(BaseProcessor):
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
        environment = ["id="+self.id] 

        client = docker.from_env() #initialize docker client
        print("RIESGOS - Docker-Client:" , client)
        try:
            directory = data["directory"]
            print("RIESGOS - Results-Directory: ", directory)
            container = client.containers.run("lexal95/dockerprocess", "sleep infinity", 
            detach=True, 
            environment=environment, #add environmet variables
            volumes={directory: {'bind': '/usr/src/process/data', 'mode': 'rw'}}) #mount specified directory
            try: 
                #run commands in container
                container.exec_run('/bin/sh') #start shell
                test = container.exec_run('python3 usr/src/process/process.py', detach=False) #execute process
                container.stop() #stop container
                container.remove() #remove container
            except Exception:
                print("RIESGOS - Process could not be started!")
                traceback.print_exc()
        except Exception: 
            print("RIESGOS - Docker-Container could not be started!")
            traceback.print_exc()
        #genrate output of pygeoapi
        result = open(directory + self.id + 'json',)
        dataResult = json.load(result)
        outputs = dataResult

        return mimetype, outputs #return output

    def __repr__(self):
        return '<DockerTestProcessor> {}'.format(self.name)