import os

id = os.environ['id']

fp = open('usr/src/process/data/result.txt', 'w')
fp.write('id of the process: ' + str(id))
fp.close()