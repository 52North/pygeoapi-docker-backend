import os

id = os.environ['id']

fp = open('usr/src/process/data/' + id +'.txt', 'w')
fp.write('id of the process: ' + str(id))
fp.close()