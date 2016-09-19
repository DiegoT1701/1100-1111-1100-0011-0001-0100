public classimport java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.ArrayList;
import javax.imageio.ImageIo;

public class CADProject{
	private static BufferedImage image;
	private static PrintWriter out;
	private static String name = "saitama-ok";
	private static int limit = 10;
	private static boolean dark = false;
	private static double[][] colors;
	private static final int MAX_LINES = 19989;
	//code to make a cube in OpenSCAD
	public static String cube(double width, double height, double depth){
		return "cube(["+width+","+height+","+depth+"])";
	}

	//code to translate an object in OpenSCAD
	public static String translate(double cubeWidth, double cubeHeight, double cubeDepth, double w, double h, double d){
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
}