import os

id = os.environ['id'] #read evironment variable

fp = open('usr/src/process/data/' + id +'.txt', 'w') #create result file
fp.write('id of the process: ' + str(id)) #write result
fp.close() #close result file