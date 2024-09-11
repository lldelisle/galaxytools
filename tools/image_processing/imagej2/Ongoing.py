import sys

from ij import IJ
from ij.plugin.filter import Analyzer
#import ij.gui.Overlay
#import ij.gui.Roi

FILL_COLOR = (255,255,0,128)
STROKE_COLOR = (0,0,0,255)
STROKE_WIDTH = 2

black_background = False

imp = IJ.openImage("/home/ldelisle/Documents/mygit/galaxytools/tools/image_processing/imagej2/test-data/blobs.gif")
input_image_plus_copy = imp.duplicate()
IJ.run(imp, "Options...", "edm=Overwrite iterations=1 count=1 black");
image_processor_copy = input_image_plus_copy.getProcessor()
analyzer = Analyzer(input_image_plus_copy)
OPTIONS = ["edm=Overwrite", "iterations=1", "count=1"]

# Set binary options.
options_list = OPTIONS
if black_background:
    options_list.append("black")
options = " ".join(options_list)
IJ.run(input_image_plus_copy, "Options...", options)

if not image_processor_copy.isBinary():
    # Convert the image to binary grayscale.
    IJ.run(input_image_plus_copy, "Make Binary", "")

IJ.run(input_image_plus_copy, "Analyze Particles...", "in_situ show=[Overlay Masks]")

input_image_plus_copy.show()

ov = input_image_plus_copy.getOverlay()

for i, roi in enumerate(ov):
	# shape x y x_rad y_rad label fontSize x1 y1 x2 y2 points width height fill_color stroke_color stroke_width z c t roi_name roi_description
	# Polygon (300,300),(350,350),(300,400) (255,255,0,128) (0,0,0,255) 2 1 0 0 Example ROI This is an example ROI
	if roi.getName() is None:
		roi.name = "ROI_%d" % i
	poly = roi.getPolygon()
	x_values = poly.xpoints
	y_values = poly.ypoints
	points_coo = ",".join(["(%d,%d)" % (x, y) for x, y in zip(x_values, y_values)])
  	print("Polygon\t\t\t\t\t\t\t\t\t\t%s\t%s\t%s\t%d\t0\t0\t0\t%s\t" % (points_coo, FILL_COLOR, STROKE_COLOR, STROKE_WIDTH, roi.getName()))
  