import numpy as np

# make sample data file

data = np.loadtxt('data01.csv',delimiter=',',skiprows=1)
t = data[:,1]
x = data[:,2]
y = data[:,3]

f = open('data.csv','w+')
f.write('Slice,X,Y\n')
for i in range(len(t)):
	f.write('{},{},{}\n'.format(int(t[i]),int(x[i]),int(y[i])))
f.close()
