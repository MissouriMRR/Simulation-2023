# FILE CONTAINS CHARACTERISTICS OF GENERATED IMAGES
# SUCH AS IMAGE DIMENSIONS, SHAPE DIMENSIONS, CHAR
# FONT SIZE, CHAR COORDINATES.

# List of possible shapes, colors, and chars for ODLCs.
shapeList = ["circle", "semicircle", "quartercircle", "triangle", "rectangle", "pentagon", "star", "cross"]
colorList = ["white", "black", "red", "blue", "green", "purple", "brown", "orange"]
charList = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Dimensions (in pixels) of every generated image.
IMG_BKGRD_WIDTH = 8000
IMG_BKGRD_HEIGHT = 8000

# Original fixed dimensions of every circle.
CIRCLE_DIAMETER = 3500

# Original fixed dimensions of every semicircle.
SEMICIRCLE_RADIUS = 2800

# Original fixed dimensions of every quartercircle.
QUARTERCIRCLE_RADIUS = 3800

# Original fixed dimensions of every polygon.
BOUNDING_CIRCLE_RADIUS = 3000

# Original fixed dimensions of every rectangle. 
RECTANGLE_WIDTH = 2900
RECTANGLE_HEIGHT = 5000

# Original fixed circumradius of every star.
STAR_CIRCUMRADIUS = 3200

# DO NOT CHANGE! Constant scaling value for inverted pentagon's circumradius inside star.
PENTAGON_CIRCUMRADIUS_SCALING_VALUE = 2.615

# Original fixed dimensions of the cross rectangles.
CROSS_RECTANGLE_WIDTH = 2300
CROSS_RECTANGLE_HEIGHT = 6600

# Character symbol characteristics.
FONT_SIZE = 2200
CHAR_X_COORD = IMG_BKGRD_WIDTH/2
CHAR_Y_COORD = IMG_BKGRD_HEIGHT/2