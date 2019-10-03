import glob
import numpy as np

# make clean sample data files

files = glob.glob('raw/raw*.csv')

n = 1

for f in files:
	data = np.loadtxt(f,delimiter=',',skiprows=1)
	t = data[:,1]
	x = data[:,2]
	y = data[:,3]

	f = open('data'+str(n).rjust(2,'0')+'.csv','w+')
	f.write('T,X,Y\n')
	for i in range(len(t)):
		f.write('{},{},{}\n'.format(int(t[i]),int(x[i]),int(y[i])))
	f.close()

	n += 1


