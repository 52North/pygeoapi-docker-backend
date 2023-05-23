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
  "id": "echo",
  "title": "Echo Process",
  "description": "This process accepts and number of input and simple echoes each input as an output.",
  "version": "1.0.0",
  "jobControlOptions": [
    "async-execute",
    "sync-execute"
  ],
  "outputTransmission": [
    "value",
    "reference"
  ],
  "inputs": {
    "echoInput": {
      "title": "String Literal Input Example",
      "description": "This is an example of a STRING literal input.",
      "schema": {
        "type": "string",
        "enum": [
          "Value1",
          "Value2",
          "Value3"
        ]
      }
    }
  },
  "outputs": {
    "echoOutput": {
      "schema": {
        "type": "string",
        "enum": [
          "Value1",
          "Value2",
          "Value3"
        ]
      }
    }
  },
  "links": [
    {
      "href": "https://processing.example.org/oapi-p/processes/echo/execution",
      "rel": "http://www.opengis.net/def/rel/ogc/1.0/execute",
      "title": "Execute endpoint",
      "type": "endpoint"
    }
  ],
    'example': {
        'inputs': {
            'echo': 'echoValue'
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

        echo = data.get('echoInput', None)

        if echo is None:
            raise ProcessorExecuteError('Cannot process without echo value')

        outputs = {
            'echoOutput': echo
        }

        return mimetype, outputs

    def __repr__(self):
        return '<echoProcessor> {}'.format(self.name)