import requests
import shutil
import Image
import os
from StringIO import StringIO

radius = 30
width = 2*radius

def process_journeymap(folder):
	os.mkdir(folder + "_tiles")
	for x in range(-radius, radius):
		for y in range(-radius, radius):
			print x,y
			try:
				tile = Image.open(folder+"/"+str(x)+","+str(y)+"_Normal.region.png")
				newtile = Image.new("RGBA", (512,512), "white")
				# Remove the night-coloured map
				box = (0,0,512,512)
				tile = tile.crop(box)
				newtile.paste(tile, box)
				# Save with new indexing: 0,0 is the top-left corner
				newtile.save(folder+"_tiles/"+str(x+radius)+"_"+str(y+radius)+".png")
			except:
				pass

def create_zoomed_tiles():
	# Recursively make larger (area) tiles from smaller ones
	for z in range (5,0,-1):
		print "z=",z
		shutil.rmtree("master/"+str(z))
		os.mkdir("master/"+str(z))
		for x in range(2**z):
			print " ",x,"/",2**z
			for y in range(2**z):
				# Create a new tile from 4 tiles of the previous size
				newtile = Image.new("RGBA", (1024,1024), "white")
				for i in range(2):
					for j in range(2):
						try:
							tile = Image.open("master/"+str(z+1)+"/"+str(2*x+i)+"_"+str(2*y+j)+".png")
							box = (i*512, j*512, (i+1)*512, (j+1)*512)
							newtile.paste(tile, box)
						except:
							pass
				# Resize so the new tiles are still 512x512			
				newtile = newtile.resize((512,512), Image.ANTIALIAS)			
				newtile.save("master/"+str(z)+"/"+str(x)+"_"+str(y)+".png")


# Deprecated, creates single image of whole map
def create_map():
	radius = 30
	m = Image.new("RGBA", (2*radius*102, 2*radius*102), "white")
	for x in range(-radius, radius):
		for y in range(-radius, radius):
			try:
				tile = Image.open("tiles/"+str(x)+"_"+str(y)+".png")
				box = ((radius+x)*102, (radius+y)*102, (radius+x+1)*102, (radius+y+1)*102)
				m.paste(tile, box)
			except:
				pass
	m.save("map.png")


def download_tiles():
	# Download tiles from the civ transport map
	masterurl = "http://civcraft.slimecraft.eu/"
	url = lambda x,y: masterurl+"tiles/4/tile_"+str(x)+"_"+str(y)+"_normal.png"

	for x in range(-30, 30):
		for y in range(-30, 30):
			print x,y,
			response = requests.get(url(x,y), stream=True)
			if response.status_code == 200:
				print "ok"
				i = Image.open(StringIO(response.content))
				i = i.resize((512,512), Image.ANTIALIAS)
				i.save("tiles/"+str(x+radius)+"_"+str(y+radius)+".png")
			else:
				print "404"
			del response

	return valid

def merge():
	for x in range(width):
		print x,"/",width
		for y in range(width):
			try:
				old = Image.open("master/6/"+str(x)+"_"+str(y)+".png")
			except:
				old = Image.new("RGBA", (512,512), "white")
			try:
				new = Image.open("tyro_tiles/"+str(x)+"_"+str(y)+".png")
				old.paste(new, (0,0,512,512), new)
				old.save("master/6/"+str(x)+"_"+str(y)+".png")
			except:
				pass
	#a = Image.open("tiles/29_29.png")
	#b = Image.open("master/6/29_29.png")
	#a.paste(b, (0,0,512,512), b)
	#a.save("test.png")

#process_journeymap("tyro")
#merge()
create_zoomed_tiles()
