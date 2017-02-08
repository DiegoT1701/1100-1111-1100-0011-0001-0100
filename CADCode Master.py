from PIL import Image
import os
import math

def cube(width, height, depth):
    return "cube(["+str(width)+", "+str(height)+", "+str(depth)+"]);"

def translate(cube_width, cube_height, cube_depth, width, height, depth):
    return "translate(["+str(width)+", "+str(height)+", "+str(depth)+"]){"+cube(cube_width,cube_height,cube_depth)+"}"

name = "team_logo"
run_length = False
copies = 1
compress = 2.85#math.ceil(((img.size[0]) * (img.size[1] / copies)) / 19989)
vertical = False
limit = 20
dark =  False
percent = 14.5
rng = limit * (percent / 100)

try:
    img = Image.open("images\\"+name+".jpg")
except:
    try:
        img = Image.open("images\\"+name+".jpeg")
    except:
        img = Image.open("images\\"+name+".png")
if vertical :
	img = img.rotate(90)

code = []
pixels = img.load()
y = 0
countY = 0
while y < img.size[1] :
	row = []
	x = 0
	countX = 0
	while x < img.size[0] :
		countX = countX + 1
		pixel = pixels[x, y]
		grayscale = limit * (((pixel[0] * 0.2989) + (pixel[1] * 0.1140) + (pixel[2] * 0.5870)) / 256)
		distance = 1
		empty = False
		if run_length and x + distance < img.size[0] :
			next_pixel = pixels[x + distance, y]
			next_gray = limit * (((next_pixel[0] * 0.2989) + (next_pixel[1] * 0.1140) + (next_pixel[2] * 0.5870)) / 256)
			while x + distance < img.size[0] and next_gray >= grayscale - rng and next_gray <= grayscale + rng :
				distance = distance + 1
				try :
					next_pixel = pixels[x + distance, y]
					next_gray = limit * (((next_pixel[0] * 0.2989) + (next_pixel[1] * 0.1140) + (next_pixel[2] * 0.5870)) / 256)
				except :
					pass
		if dark :
			grayscale = limit - grayscale
		if run_length :
			x = x + distance
			if grayscale > rng :
				code.append(translate(1, distance, grayscale, y, x - distance, 1) + "\n")
		else :
			x = x + compress
			code.append(translate(1, 1, grayscale, countY, countX, 1) + "\n")
	if run_length :
		y = y + 1
	else :
		y = y + compress
	countY = countY + 1
if run_length :
	code.append(translate(img.size[1], img.size[0], 1, 0, 0 ,0))
else :
	code.append(translate(countY, countX, 1, 0, 0 ,0))
	
max_copies = math.ceil(len(code) / 19989)
copies = max_copies
files = []
for i in range(copies) :
    files.append(open(name+str(i + 1)+".txt", "w"))

print(str(len(code)), "lines")
print("max copies = ", str(max_copies))
print(copies,"copies")
print(str(100 - percent) + "% of original")

for i in range(len(code)):
    files[int(i / 19988)].write(code[i])

for i in range(copies) :
    files[i].close()

for i in range(copies) :
    os.system(name + str(i + 1) + ".txt")