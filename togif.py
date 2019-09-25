import imageio, glob, re

'''
Note:
	- Last update: 15/9/2019
Bug:
	- filenames not sorted -> gif not in seq
'''

def file_num(f):
	return int(re.split('[_ .]',f)[1])

files = glob.glob("img/plot_*.png")

images = []

for f in sorted(files,key=file_num):
    images.append(imageio.imread(f))

imageio.mimsave('plot_ani.gif', images, duration=0.5)


