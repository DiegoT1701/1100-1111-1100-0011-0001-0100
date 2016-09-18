from PIL import Image
import os
import math

#code to make a cube in OpenSCAD
def cube(width, height, depth):
    return "cube(["+str(width)+", "+str(height)+", "+str(depth)+"]);"

#code to translate a cube in OpenSCAD
def translate(cube_width, cube_height, cube_depth, width, height, depth):
    return "translate(["+str(width)+", "+str(height)+", "+str(depth)+"]){"+cube(cube_width,cube_height,cube_depth)+"}"

print("start") #output marker in console
name = "saitama-ok" #name of image

#opens image and checks to see what kind of image file it is
try:
    img = Image.open(name+".png")
except:
    try:
        img = Image.open(name+".jpg")
    except:
        img = Image.open(name+".jpeg")

pixels = img.load() #gets all the pixels in an image, where pixels[x, y] returns the pixel in position [x, y] of the image
limit = 10 #max limit to the height of a cube
file = open("project.txt","w") #
dark = False
colors = []
depth_ratio = 1
print("getting values")
for y in range(img.size[1]):
    row = []
    for x in range(img.size[0]):
        pixel = image[x,y]
        try:
            gValue = (pixel[0] * 0.2989) + (pixel[1] * 0.1140) + (pixel[2] * .5870)
        except:
            gValue = pixel
        if(dark):
            gValue = abs(gValue-256)
        row.append(limit*(gValue/256))
    pix.append(row)
colored = 0
print("getting colors")
for y in range(len(pix)):
    for x in range(len(pix[0])):
       if pix[y][x] > 0:
           colored += 1
compress = math.ceil(math.sqrt((len(pix)*len(pix[0]))/19989))
grid = []
print("getting resolution")
for y in range(0,len(pix)):
    row = []
    for x in range(0,len(pix[0])):
        '''
        gValue = 0
        i = 0
        j = 0
        for j in range(compress):
            for i in range(compress):
                try:
                  gValue += pix[y][x+i]
                except:
                    pass
                try:
                   gValue += pix[y + j][x]
                except:
                    pass
        gValue/=(compress*compress)
        '''
        gValue = pix[y][x]
        row.append(gValue)
    grid.append(row)
res = 2
cad = []
print("done resolution")
for y in range(len(grid)):
    row = []
    for x in range(len(grid[0])):
        sum = grid[y][x]
        count = 1
        for i in range(-res,res+1):
            try:
                sum+=grid[y+i][x]
                count+=1
            except:
                pass
            try:
                sum+=grid[y][x+i]
                count+=1
            except:
                pass
        row.append(round((sum/count),2))
    cad.append(row)
print("not")
for y in range(len(cad)):
    for x in range(len(cad[0])):
        if cad[y][x] > 0:
           f.write(translate(1,1,cad[y][x],len(cad)-y,len(cad[0])-x,0)+"\n")
print("end")
f.close()
os.system("project.txt")