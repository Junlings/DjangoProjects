import pickle

f = open('Target_store','r')

res = pickle.load(f)

i = 0
for key in res:
    print res[i]['state']
    i += 1
print 1