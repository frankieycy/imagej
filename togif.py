import imageio, glob, re

'''
Note:
	- collects distribution outputs from plot.py into a .gif animation
	- Last: 15/9/2019
'''

def file_num(f):
	return int(re.split('[_ .]',f)[1])

files = glob.glob("img/plot_*.png") # get distribution plots

images = []

for f in sorted(files,key=file_num):
    images.append(imageio.imread(f))

imageio.mimsave('plot_ani.gif', images, duration=0.5) # convert to .gif


