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
name = "solo" #name of image

#opens image and checks to see what kind of image file it is
try:
    img = Image.open("images\\"+name+".png")
except:
    try:
        img = Image.open("images\\"+name+".jpg")
    except:
        img = Image.open("images\\"+name+".jpeg")

pixels = img.load() #gets all the pixels in an image, where pixels[x, y] returns the pixel in position [x, y] of the image
limit = 30 #max limit to the height of a cube
copies = math.ceil((img.size[1] * img.size[0]) / 19998) #number of sections in which the image will be divided into to improve quality of each
files = [] #list of files where code is to be written 
#adding a new file to the list for each of the sections of the image
for i in range(copies) :
    files.append(open(name+str(i + 1)+".txt", "w"))

dark =  False #lets you change between extruding inward or outward
colors = [] #array of arrays of doubles where all the grayscale values for each pixel is held
depth_ratio = 1 #lets you change the how far away the top of the highest cube is from the top of the lowest cube
print("getting values") #output marker in console

#gets grayscale values from pixels to colors array
for y in range(img.size[1]): 
    row = [] #array of doubles that stores the grayscale values for each pixel in this row of pixels of the image
    for x in range(img.size[0]):
        pixel = pixels[x,y] 
        #checks to see if pixel returns a RGB tuple or just a regular value(possibly due to vector imaging)
        try:
            gValue = (pixel[0] * 0.2989) + (pixel[1] * 0.1140) + (pixel[2] * .5870) #formula to find grayscale of image; 30% of the red value, 59% of the green value and 11% of the blue value
        except:
            gValue = pixel

        #if dark, then extrude is inverted
        if(dark):
            gValue = abs(gValue - 255)
        
        row.append(limit * (gValue / 255)) #puts the grayscale value into the row array and makes sure that the height doesn't surpass the determined limit by dividing the grayscale value by the max grayscale value of 255 and multiplying that by the limit
    colors.append(row) #puts the row of values into the colors array

res = -1 #arbitrary number by which to get the average of the surrounding pixels for each pixel; i.e. each pixel's grayscale value will be the average of itself and the res amount of pixels around it
cad = [] #new array of arrays of grayscale values so that it can get the average for the original pixels, without getting the average of the average of pixels
compress = math.ceil((math.sqrt((img.size[1] * img.size[0]) / copies) / 19989)) #number by which the final number of lines of code can be divided so that the output doesn't go over OpenSCAD's max lines of 19989
min = 1000000 #value of lowest height cube, set as the highest so that it can be compared to lower heights

print("getting resolution") #output marker for console

#goes through the grayscale values and skips each compress amount of pixels so that the total number of lines doesn't go over OpenSCAD's max of 19989 of lines
for y in range(0, len(colors), compress):
    row = [] #array of doubles which will hold the average grayscale of the surrounding pixels and the pixel itself
    for x in range(0, len(colors[0]),compress):
        sum = colors[y][x] #number which will hold the total grayscale values of the surrounding res pixels and the pixel itself
        count = 1 #number of pixels which were added to sum, so as to get the average
        #goes through all the surrounding res pixels and adds their grayscale values to the sum
        
        for i in range(-res, res + 1):
            #goes through each of the surrounding pixels and checks to make sure that it doesn't go over bounds'
            print("res")
            try:
                sum+=colors[y + i][x]
                count+=1
            except:
                pass
            try:
                sum += colors[y][x + i]
                count += 1
            except:
                pass
            try:
                sum += colors[y + i][x + i]
                count += 1
            except:
                pass
            try:
                sum += colors[y - i][x + i]
                count += 1
            except:
                pass
                
        ave = sum / count
        if ave < min : 
            min = ave
        if min < 1 : 
            min = 1
        row.append(ave)
        
    cad.append(row)
print("printing") #output marker for console
#prints every line of code to the text file and skips empty lines of code (i.e. cubes with 0 depth)
for y in range(len(cad)):
    for x in range(len(cad[0])):
        files[int(y / (len(cad) / copies))].write(translate(1, 1, cad[y][x], y, x, 1)+"\n")
        
print("end") #output marker for console
print("\n[Image resolution to Render resolution is 1 :", str(compress),"]")
for i in range(copies) :
    files[i].close()
for i in range(copies) :
    os.system(name + str(i + 1) + ".txt")
