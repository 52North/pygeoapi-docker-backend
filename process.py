import os

test = os.environ['TEST']

fp = open('usr/src/process/result.txt', 'w')
fp.write(test)
fp.close()