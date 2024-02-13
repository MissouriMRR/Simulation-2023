import random
import math
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from ODLCcharacteristics import *

# ----------------------- SHAPE DRAW FUNCTIONS ----------------------- #

def draw_circle(drawObject, color):
    adj_circle_diameter = CIRCLE_DIAMETER + random.randint(0,0)

    top_left_x_coord = (IMG_BKGRD_WIDTH-adj_circle_diameter)/2
    top_left_y_coord = (IMG_BKGRD_HEIGHT-adj_circle_diameter)/2

    bottom_right_x_coord = (top_left_x_coord+adj_circle_diameter)
    bottom_right_y_coord = (top_left_y_coord+adj_circle_diameter)    
    
    circle_coords = [(top_left_x_coord, top_left_y_coord), (bottom_right_x_coord, bottom_right_y_coord)]
    
    drawObject.ellipse(circle_coords, fill=color, outline=color)


def draw_semicircle(drawObject, color):
    adj_semicircle_radius = SEMICIRCLE_RADIUS + random.randint(0,0)
    
    top_left_x_coord = (IMG_BKGRD_WIDTH-2*adj_semicircle_radius)/2
    top_left_y_coord = (IMG_BKGRD_HEIGHT-2*adj_semicircle_radius)/2 + adj_semicircle_radius/2.2

    bottom_right_x_coord = (top_left_x_coord+2*adj_semicircle_radius)
    bottom_right_y_coord = (top_left_y_coord+2*adj_semicircle_radius)

    semicircle_coords = [(top_left_x_coord, top_left_y_coord), (bottom_right_x_coord, bottom_right_y_coord)]

    drawObject.pieslice(semicircle_coords, 180, 360, fill=color, outline=color)


def draw_quartercircle(drawObject, color):
    adj_quartercircle_radius = QUARTERCIRCLE_RADIUS + random.randint(0,0)
    
    # Coords below are altered to move bounding box of the circle down 
    # and to the right in order to center the quartercircle pieslice.
    top_left_x_coord = (IMG_BKGRD_WIDTH-(adj_quartercircle_radius*2))/2 + (adj_quartercircle_radius/2.5)
    top_left_y_coord = (IMG_BKGRD_HEIGHT-(adj_quartercircle_radius*2))/2 + (adj_quartercircle_radius/2.5)

    bottom_right_x_coord = top_left_x_coord+adj_quartercircle_radius*2
    bottom_right_y_coord = top_left_y_coord+adj_quartercircle_radius*2

    quartercircle_bounding_box_coords = [(top_left_x_coord, top_left_y_coord), (bottom_right_x_coord, bottom_right_y_coord)]

    drawObject.pieslice(quartercircle_bounding_box_coords, 180, 270, fill=color, outline=color)    


def draw_triangle(drawObject, color):
    bounding_circle_coords = (IMG_BKGRD_WIDTH/2, IMG_BKGRD_HEIGHT/2, BOUNDING_CIRCLE_RADIUS)

    drawObject.regular_polygon(bounding_circle_coords, 3, fill=color, outline=color)


def draw_rectangle(drawObject, color):
    # Adjusts rectangle dimensions to add variability.
    adj_rect_width = RECTANGLE_WIDTH + random.randint(0, 0)
    adj_rect_height = RECTANGLE_HEIGHT + random.randint(0, 0)

    top_left_x_coord = (IMG_BKGRD_WIDTH-adj_rect_width)/2
    top_left_y_coord = (IMG_BKGRD_HEIGHT-adj_rect_height)/2

    bottom_right_x_coord = (top_left_x_coord+adj_rect_width)
    bottom_right_y_coord = (top_left_y_coord+adj_rect_height)

    rectangle_coords = [(top_left_x_coord, top_left_y_coord), (bottom_right_x_coord, bottom_right_y_coord)]

    drawObject.rectangle(rectangle_coords, fill=color, outline=color)


def draw_pentagon(drawObject, color):
    bounding_circle_coords = (IMG_BKGRD_WIDTH/2, IMG_BKGRD_HEIGHT/2, BOUNDING_CIRCLE_RADIUS)

    drawObject.regular_polygon(bounding_circle_coords, 5, fill=color, outline=color)


def draw_star(drawObject, color):
    star_circumradius = STAR_CIRCUMRADIUS

    # Define angle for vertices generation.
    angle = math.radians(144)
    outer_star_vertices = []

    # Generation of 5 star vertices.
    for i in range(5):
        outer_x = star_circumradius * math.cos(angle * i - math.pi / 2) + IMG_BKGRD_WIDTH / 2
        outer_y = star_circumradius * math.sin(angle * i - math.pi / 2) + IMG_BKGRD_HEIGHT / 2
        outer_star_vertices.append((outer_x, outer_y))
    
    # Upside down regular polygon drawn to fill in white space between star vertex triangles.
    drawObject.regular_polygon((IMG_BKGRD_WIDTH/2, IMG_BKGRD_HEIGHT/2, star_circumradius/PENTAGON_CIRCUMRADIUS_SCALING_VALUE), 5, fill=color, outline=color, rotation=180)
    drawObject.polygon(outer_star_vertices, fill=color, outline=color,)


def draw_cross(drawObject, color):
    # Adjusts rectangle dimensions to add variability.
    adj_rect_width = CROSS_RECTANGLE_WIDTH + random.randint(0, 0)
    adj_rect_height = CROSS_RECTANGLE_HEIGHT + random.randint(0, 0)

    top_left_x_coord = (IMG_BKGRD_WIDTH-adj_rect_width)/2
    top_left_y_coord = (IMG_BKGRD_HEIGHT-adj_rect_height)/2

    bottom_right_x_coord = (top_left_x_coord+adj_rect_width)
    bottom_right_y_coord = (top_left_y_coord+adj_rect_height)
    
    vertical_rectangle_coords = [(top_left_x_coord, top_left_y_coord), (bottom_right_x_coord, bottom_right_y_coord)]
    horizontal_rectangle_coords = [(top_left_y_coord, top_left_x_coord), (bottom_right_y_coord, bottom_right_x_coord)]

    drawObject.rectangle(vertical_rectangle_coords, fill=color, outline=color)
    drawObject.rectangle(horizontal_rectangle_coords, fill=color, outline=color)


# ----------------------- ODLC SHAPE DRAW FUNCTION ----------------------- #

def draw_ODLC_shape(drawObject, shapeName, shapeColor):
    if (shapeName == "circle"):
        draw_circle(drawObject, shapeColor)
    if (shapeName == "semicircle"):
        draw_semicircle(drawObject, shapeColor)
    if (shapeName == "quartercircle"):
        draw_quartercircle(drawObject, shapeColor)
    if (shapeName == "triangle"):
        draw_triangle(drawObject, shapeColor)
    if (shapeName == "rectangle"):
        draw_rectangle(drawObject, shapeColor)
    if (shapeName == "pentagon"):
        draw_pentagon(drawObject, shapeColor)
    if (shapeName == "star"):
        draw_star(drawObject, shapeColor)
    if (shapeName == "cross"):
        draw_cross(drawObject, shapeColor)


# ----------------------- ODLC CHARACTER DRAW FUNCTION ----------------------- #

def draw_ODLC_char(drawObject, char, charColor):
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    drawObject.text((CHAR_X_COORD, CHAR_Y_COORD), char, font=font, fill=charColor, anchor="mm")


# ----------------------- RANDOM ODLC GENERATION FUNCTION ----------------------- #

def generate_random_ODLCs(numODLCs):

    current_time = datetime.now()
    formatted_time = current_time.strftime("%d-%m-%Y-%H-%M-%S")
    
    # Automatically creates new directory where the random ODLCs are saved.
    generated_ODLCs_directory = f"random-generated-ODLCs-{formatted_time}"
    os.mkdir(f"./{generated_ODLCs_directory}")

    for i in range(numODLCs):
        # Creates a new image with specified dimensions and background color.
        image = Image.new("RGBA", (IMG_BKGRD_WIDTH, IMG_BKGRD_HEIGHT), (255, 255, 255, 0))
        # Creates a drawing object.
        drawObj = ImageDraw.Draw(image)

        # Picking random shape, shapeColor, char, charColor
        shape = random.choice(shapeList)
        shapeColor = random.choice(colorList)
        char = random.choice(charList)
        charColor = random.choice(colorList)

        while (shapeColor == charColor):
            shapeColor = random.choice(colorList)
            charColor = random.choice(colorList)

        # Draws shape with shapeColor.
        draw_ODLC_shape(drawObj, shape, shapeColor)

        # Draws char with charColor.
        draw_ODLC_char(drawObj, char, charColor)

        # Saves image file with name: "shapeColor-shape-charColor-char.png"
        #image.save(f"random-generated-ODLCs/{shapeColor}-{shape}-{charColor}-{char}.png")
        image.save(f"{generated_ODLCs_directory}/{shapeColor}-{shape}-{charColor}-{char}.png")

# ----------------------- ALL ODLC GENERATION FUNCTION ----------------------- #

# Generates all possible combinations of ODLC objects.
def all_ODLC_combos_generation():

    current_time = datetime.now()
    formatted_time = current_time.strftime("%d-%m-%Y-%H-%M-%S")
    
    # Automatically creates new directory where the random ODLCs are saved.
    generated_ODLCs_directory = f"all-generated-ODLCs-{formatted_time}"
    os.mkdir(f"./{generated_ODLCs_directory}")

    for shape in shapeList:
        for shapeColor in colorList:
            for char in charList:
                for charColor in colorList:
                    if shapeColor == charColor:
                        continue
                    
                    # Creates a new image with specified dimensions and background color.
                    image = Image.new("RGBA", (IMG_BKGRD_WIDTH, IMG_BKGRD_HEIGHT), (255, 255, 255, 0))
                    # Creates a drawing object.
                    drawObj = ImageDraw.Draw(image)
                    
                    # Draws shape with shapeColor.
                    draw_ODLC_shape(drawObj, shape, shapeColor)

                    # Draws char with charColor.
                    draw_ODLC_char(drawObj, char, charColor)

                    # Saves image file with name: "shapeColor-shape-charColor-char.png"
                    image.save(f"{generated_ODLCs_directory}/{shapeColor}-{shape}-{charColor}-{char}.png")