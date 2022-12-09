import os

test = os.environ['TEST']

fp = open('result.txt', 'w')
fp.write(test)
fp.close()