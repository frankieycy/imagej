import glob, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

rc('text', usetex=True)

# ----------------------------------------- #

'''
Note:
	- PHYS3710 Short Experimental Project - Analysis Codes
	- Last: 3/10/2019
	- outputs (images) written to img/ (prepare this!)
	- generate distributions for different tau's
	- variance (diffusion spread) relates linearly with tau -> Avogadro constant

Measurements:
	- temperature: 22.5 deg
	- diameter: 1.04 micron
'''

# ----------------------------------------- #

out = 'img/' # location of outputs

# remove old plots
old = glob.glob(out+"*.png")
for f in old:
	os.remove(f)

# ---------- distributions in time ---------- #

px_to_μm = 200/1051 # scale: pixel to μm
to_sec = 5 # scale: time in second

tau = range(1,50,1)

extension = 'csv'
files = glob.glob('data*.{}'.format(extension)) # get all .csv files

delta_x2_arr = [] # stores variance for diff tau

for dt in tau:
	delta_x = [] # x-displacement
	delta_y = [] # y-diaplacement

	# ---------- read data from files ---------- #

	for f in files:
		data = np.loadtxt(f,delimiter=",",skiprows=1)
		T = len(data) # total time
		t = data[:,0] # time; unit: 5s
		x = data[:,1] # x-coord; unit: pixel
		y = data[:,2] # y-coord

		for t in range(dt,T): # compute displacements
			delta_x.append((x[t]-x[t-dt])*px_to_μm)
			delta_y.append((y[t]-y[t-dt])*px_to_μm)

	delta_x.extend(delta_y) # gather displacements in x,y-dim

	# ---------- plot histogram: Gaussian with spread ~dt ---------- #

	fig = plt.figure()
	axes = plt.gca()
	axes.set_xlim([-10,10])
	axes.set_ylim([0,1])
	plt.hist(delta_x,color='black',bins=35,density=True,
		range=[-10,10],label=r"$\tau$={}s".format(to_sec*dt))
	plt.title(r"Distribution of displacement $\Delta x$")
	plt.xlabel(r"displacement $\Delta x$ ($\rm{\mu m}$)")
	plt.ylabel(r"density")
	plt.legend()
	#plt.show()
	fig.savefig(out+'plot_{}.png'.format(dt),dpi=200)
	plt.close()

	# ----------------------------------------- #

	delta_x = np.array(delta_x)
	mean_x = np.mean(delta_x) # mean displacement
	delta_x2 = np.mean(delta_x**2) # mean squared displacement (variance)
	delta_x2_arr.append(delta_x2) # stores delta_x2

	# ---------- statistics ---------- #

	print("--- dt={} ---".format(dt))
	print("<delta_x> = {}".format(round(mean_x,4))) # ~0
	print("<delta_x^2> = {}".format(round(delta_x2,4))) # ~dt

# ---------- Einstein's diffusion relation ---------- #

tau = to_sec*np.array(tau)
x = np.linspace(0,max(tau),2)
m,b = np.polyfit(tau,delta_x2_arr,deg=1) # line fit

fig = plt.figure()
axes = plt.gca()
axes.set_xlim([0,max(tau)])
plt.plot(tau,delta_x2_arr,linestyle='-',marker='.',color='black',
	label="experimental") # ~linear
plt.plot(x,b+m*x,'--',color='grey',
	label="y={}+{}x (fitted)".format(round(b,4),round(m,4)))
plt.title(r"$\langle \Delta x^2 \rangle$ against $\tau$")
plt.xlabel(r"time interval $\tau$ (s)")
plt.ylabel(r"mean squared displacement $\langle \Delta x^2 \rangle$ ($\rm{\mu m}^2$)")
plt.legend()
fig.savefig(out+'x2tau.png'.format(dt),dpi=200)
plt.close()

# ----------------------------------------- #

print("--- analysis ---")
print("slope = {}".format(round(m,10)))

# ----------------------------------------- #

f = open("x2tau.csv","w+") # print tau,var to file
f.write('tau,var\n')
for i in range(len(tau)):
	f.write('{},{}\n'.format(tau[i],delta_x2_arr[i]))
f.close()

