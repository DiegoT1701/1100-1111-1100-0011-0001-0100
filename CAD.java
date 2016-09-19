import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.ArrayList;

import javax.imageio.ImageIO;
public class CAD{
	private static BufferedImage image;
	private static PrintWriter out;
	private static String name = "saitama-ok";
	private static int limit = 10;
	private static boolean dark = false;
	private static double[][] colors;
	private static final int MAX_LINES = 19989;
	//code to make a cube in OpenSCAD
	public static String cube(int width, int height, double depth){
		return "cube(["+width+","+height+","+depth+"])";
	}
	//code to translate an object in OpenSCAD
	public static String translate(int cubeWidth, int cubeHeight, double cubeDepth, int w, int h, int d){
		return "translate(["+w+","+h+","+d+"]){"+cube(cubeWidth,cubeHeight,cubeDepth)+";}";
	}
	public static void main(String[] args) throws IOException{
		
		//opens image and automatically checks to see what king of image file it is (png, jpg, etc)
		try{
			image = ImageIO.read(new File("images\\"+name+".png")); 
		}
		catch(Exception e){
			try{
				image = ImageIO.read(new File("images\\"+name+".jpg"));
			}
			catch(Exception x){
				image = ImageIO.read(new File("images\\"+name+".jpeg"));
			}
		}
		getValues();
		out = new PrintWriter("cad.txt","UTF-8");
		ArrayList<String> cad = code();
		double res = Math.ceil((double)cad.size() / (double)MAX_LINES); //value with which to skip between pixels so as to not go over the max amount of lines of code in OpenSCAD
		
		for(int i = 0; i < cad.size(); i++)
			out.println(cad.get(i));
		out.close();
	}
	//load the grayscale value from each pixel to a 2D array of doubles
	public static void getValues(){
		colors = new double[image.getHeight()][image.getWidth()];
		for(int y = 0; y < image.getHeight(); y++)
			for(int x = 0; x < image.getWidth(); x++){
				Color pixelColor = new Color(image.getRGB(x,y));
				double gValue = (((pixelColor.getRed()*0.2989)+(pixelColor.getBlue()*0.5870)+(pixelColor.getGreen()*0.1140))); // The grayscale value is 30% of the red value, 59% of the green value and 11% of the blue value
				//lets the user change from extruding inward and extruding outward
				if(dark)
					gValue = Math.abs(gValue-256);
				colors[y][x] = limit * ((double)gValue / 256); //limits the height of the cube by the ratio{ cubeHeight : maxHeight = grayscale : maxGrayscale}
			}
	}
	//writes the code for each cube given the grayscale values
	public static ArrayList<String> code(){
		ArrayList<String> list = new ArrayList<String>();
		for(int y = 0; y < colors.length; y++)
			for(int x = 0; x < colors[0].length; x++)
				if(colors[y][x] > 0) //skips a pixel if it doesn't have any height, allows for more space for code
					list.add(translate(1,1,colors[y][x],colors.length-y,colors[0].length-x,0));
		return list;
	}
	//prints the code to a .txt file
	public static void print(ArrayList<String> cad){
		
		out.close();
	}
}