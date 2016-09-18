from PIL import Image
import os
import math


def cube(width, height, depth):
    return "cube(["+str(width)+", "+str(height)+", "+str(depth)+"]);"
def translate(cube_width, cube_height, cube_depth, width, height, depth):


    return "translate(["+str(width)+", "+str(height)+", "+str(depth)+"]){"+cube(cube_width,cube_height,cube_depth)+"}"
name = "saitama-ok"
print("start")
try:
    img = Image.open(name+".png")
except:
    try:
        img = Image.open(name+".jpg")
    except:
        img = Image.open(name+".jpeg")
image = img.load()
limit = 10
f = open("project.txt","w")
dark = False
pix = []
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
        row.append(limit*(round(gValue/256,3)))
    pix.append(row)
colored = 0
print("getting colors")
for y in range(len(pix)):
    for x in range(len(pix[0])):
        colored += 1 if pix[y][x] > 0 else 0
compress = math.ceil(math.sqrt(colored/19989))
grid = []
print("getting resolution")
for y in range(len(pix)):
    row = []
    for x in range(len(pix[0])):
        gValue = 0
        i = 0
        j = 0
        while x + i < len(pix[0]) and i < compress:
            try:
              gValue += pix[y][x+i]
            except:
                pass
            i+=1
        while y + j < len(pix[1]) and j < compress:
            try:
               gValue += pix[y + j][x]
            except:
                pass
            j+=1
        gValue/=compress
        row.append(gValue)
    grid.append(row)
res = 1
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
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if cad[y][x] > 0:
          f.write(translate(1,1,cad[y][x],len(grid)-y,len(grid[0])-x,0)+"\n")
print("end")
f.close()
os.system("project.txt")