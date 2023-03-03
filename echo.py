import logging
import math
import time 
from random import *
from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError

#execute command
#curl -X POST "http://localhost:5000/processes/echo/execution" -H "Content-Type: application/json" -d "{\"mode\": \"async\", \"inputs\":{\"echo\": \"42\"}}"

LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.0.1',
    'id': 'echo',
    'title': {
        'en': 'echo',
        'fr': 'echo'
    },
    'description': {
        'en': 'Echo process for testing the pygeoapi',
        'fr': 'Echo process for testing the pygeoapi',
    },
    'keywords': ['echo'],
    'links': [{
        'type': 'text/html',
        'rel': 'about',
        'title': 'information',
        'href': 'https://example.org/process',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'echo': {
            'title': 'Echo Value',
            'description': 'Just a value',
            'schema': {
                'type': 'int'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['echo']
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
            'echo': 'some value'
        }
    }
}


class echoProcessor(BaseProcessor):
    """Echo Processor example"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.test.TestProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):

        mimetype = 'application/json'

        echo = data.get('echo', None)

        if echo is None:
            raise ProcessorExecuteError('Cannot process without both points')

        outputs = {
            'id': 'Echo',
            #'slept for ': sleepingTime,
            'value': echo
        }

        return mimetype, outputs

    def __repr__(self):
        return '<echoProcessor> {}'.format(self.name)