import logging
import math
import time 
from random import *
from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError
import docker


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.0.1',
    'id': 'docker_process',
    'title': {
        'en': 'test',
        'fr': 'test'
    },
    'description': {
        'en': 'Test process for testing docker in conjuction with pygeoapi',
        'fr': 'Test process for testing docker in conjuction with pygeoapi',
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
            'metadata': None,  # TODO how to use?
            'keywords': ['test']
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
            'test': 'some value'
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

        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):
        
        mimetype = 'application/json'

        test = data.get('test', None)
        '''
        if test is None:
            raise ProcessorExecuteError('Cannot process without both points')

        #Simulate processing time
        sleepingTime = 10 #randint(5, 60)
        time.sleep(sleepingTime) 
        '''
        outputs = {
            'id': 'Test',
            #'slept for ': sleepingTime,
            'value': test
        }
        
        client = docker.from_env()
        print(client)

        return mimetype, outputs

    def __repr__(self):
        return '<DockerTestProcessor> {}'.format(self.name)