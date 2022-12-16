import os

id = os.environ['id'] #read evironment variable

output = {'processID': id,
'message': 'docker process done...'}
fp = open('usr/src/process/data/' + id +'.json', 'w') #create result file
fp.write(str(output)) #write result
fp.close() #close result file