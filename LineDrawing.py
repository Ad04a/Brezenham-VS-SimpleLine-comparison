
import numpy as np
import math
from random import randint
from functools import wraps
import time
from PIL import Image

simple_line_save_filename = "simple_line.png"
mid_point_save_filename = "mid_point.png"

#decorator for measuring execution time of a function
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

def draw_simple_line(start_x, start_y, end_x, end_y, img_array, intenzity=255):

    x,y,last_x,last_y = 0,0,0,0
    if(start_x < end_x):
        x = start_x
        y = start_y
        last_x = end_x
        last_y = end_y
    else:
        #fliping the points so we can always draw from left to right
        x = end_x
        y = end_y
        last_x = start_x
        last_y = start_y 

    #helping swap for when the X values are equal
    if(x==last_x):
        y = min(start_y, end_y)
        last_y = max(start_y, end_y)

    #the difference in coordinates of the two points used to determine slope of the line
    dx = last_x - x
    dy = last_y - y # if dy is negative that means the last point is bellow the first

    if dx == 0:
        #when dx is 0 that means the X of both points are equal so we just draw streight line without more calculations
        while y <= last_y:
            y+=1
            img_array[1079-y][x] = intenzity
        return
    
    tan = dy/dx
    
    while x != last_x or (y != last_y if (tan>1 or tan<-1) else False):
        
        
        if tan>1 or tan<-1:
            #for angled below -45 and above 45 degree we have to change the y value first 
            #because it can pass through the last point of thel ine without breaking the loop
            img_array[1079-y][x] = intenzity
            y+= 1 if tan>0 else -1
            temp_x = (y-last_y)/tan + last_x
            x = math.ceil(temp_x) if temp_x>math.floor(temp_x)+0.5 else math.floor(temp_x)
            
            
        else:
            #calculate the Y value for the pixel we have to color
            temp_y = last_y + tan*(x - last_x)
            y = math.ceil(temp_y) if temp_y>math.floor(temp_y)+0.5 else math.floor(temp_y)
            img_array[1079-y][x] = intenzity
            x+= 1 
        
        


def draw_mid_point_line(start_x, start_y, end_x, end_y, img_array, intenzity=255):
    """ Function that can draw a line between two points in any direction based on the Brezenham algorithm
        For the purpose of this function point (0,0) is in the down left corner
    """

    #coloring the first pixel and determining from where to draw the line(start from the point with smaller x)
    x,y,last_x,last_y = 0,0,0,0
    if(start_x < end_x):
        x = start_x
        y = start_y
        last_x = end_x
        last_y = end_y
    else:
        #fliping the points so we can always draw from left to right
        x = end_x
        y = end_y
        last_x = start_x
        last_y = start_y 

    #helping swap for when the X values are equal
    if(x==last_x):
        y = min(start_y, end_y)
        last_y = max(start_y, end_y)

    #the difference in coordinates of the two points used to determine slope of the line
    dx = last_x - x
    dy = last_y - y # if dy is negative that means the last point is bellow the first
    
    if dx == 0:
        #when dx is 0 that means the X of both points are equal so we just draw streight line without more calculations
        while y <= last_y:
            y+=1
            img_array[1079-y][x] = intenzity
        return

    #tangent of the angle that the line makes with the X axis
    tan = dy/dx

    #vars to increment the decision and find the next decision point 
    incrN  = -2*dx
    incrNE = 2*(dy-dx)
    incrE  = 2*dy
    incrSE = 2*(dy+dx)
    incrS  = 2*dx
    
    #d - #decision var used to determine whether the next drawn point should be below or above the line / starting decision value
    #low_incre - decision incrementation if the current decision is under the line
    #high_incre - decision incrementation if the current decision is above the line
    d,low_incre, high_incre = 0,0,0 
    """ the relation ship of the slope of the line and the additions we have to use
        dy>1 : N - NE (y)
        0<dy<1 : NE - E (x)
        0>dy>-1 : E - SE (x)
        dy<-1 : SE - S (y)
        the following if statements define this corelations thogether with the starting value for the decision variable
    """

    #we will work in range between 90 and -90 dgrees
    if tan >1:
        #here the angle is greater than 45 degrees
        high_incre = incrN
        low_incre  = incrNE
        d = dy-2*dx 

    elif tan >0:
        #here the angle is less than 45 and greater than 0 degrees
        high_incre = incrNE
        low_incre  = incrE
        d = 2*dy-dx 

    elif tan >-1:
        #here the angle is less than 0 and greater than -45 degrees
        high_incre = incrE
        low_incre  = incrSE
        d = 2*dy+dx 

    else:
        #here the angle is less than -45 degrees
        high_incre = incrSE
        low_incre  = incrS
        d = dy+2*dx

    
    #coloring every pixel until we reach the x coordinate of the last point
    img_array[1079-y][x] = intenzity

    #we iterate by x or y because we dont knpw if the slope is sharp or not
    while x != last_x or (y != last_y if (tan>1 or tan<-1) else False):
        """
        in this loop we constantly increment/decrement the main coordinate of the slope
        /increment - 1quadrant , decrement - 4qudrant/
        for angles between 45 and -45 it is x
        and for angles greater than 45 or less than -45 it is y

        in adition we increment the secondary coordinate based on the decision variable
        for points above the starting point that happens when the decision var is above the line
        and for points below the starting point that happens when the decision is under the line
        """

        if d<= 0 :
            #the decision var is bellow the line
            d+= low_incre 
            if(tan>1):
                x+= 1
                y+= 1
            elif(tan<-1):
                y-=1
            else:
                y+= 0 if tan>0 else -1
                x+= 1 
        else :
            #the decision var is above the line
            d+= high_incre 
            if(tan>1):
                y+=1
            elif(tan<-1):
                y-=1
                x+=1
            else:
                y+= 1 if tan>0 else 0
                x+= 1
        #we color the pixel after all the caltulations
        if y<-1 or x>1919:
            print(start_x, start_y, end_x, end_y, " - ", x,y)
        img_array[1079-y][x] = intenzity


def file_test_simple_line():
    output_array = [[0 for i in range(1920)] for i in range(1080)]
    draw_simple_line(400,300,800,600,output_array)
    draw_simple_line(400,300,0,0,output_array)
    draw_simple_line(400,300,500,600,output_array)
    
    draw_simple_line(400,300,400,0,output_array)
    draw_simple_line(400,300,400,600,output_array)
    draw_simple_line(400,300,800,300,output_array)
    draw_simple_line(400,300,0,300,output_array)
    draw_simple_line(800,1070,800,0,output_array)

    draw_simple_line(400,300,0,600,output_array)
    draw_simple_line(400,300,1200,0,output_array)
    draw_simple_line(400,300,500,1079,output_array)
    draw_simple_line(400,300,300,1079,output_array)
    draw_simple_line(400,300,500,0,output_array)
    draw_simple_line(400,300,300,0,output_array)
    draw_simple_line(0,1079,1919,1078,output_array)
    draw_simple_line(0,1,1919,2,output_array)
    draw_simple_line(1,1079,0,0,output_array)
    draw_simple_line(1918,1079,1919,0,output_array)
    draw_simple_line(1444, 436, 1681, 797,output_array)

    return output_array


def file_test_mid_point():
    output_array = [[0 for i in range(1920)] for i in range(1080)]
    draw_mid_point_line(400,300,800,600,output_array)
    draw_mid_point_line(400,300,0,0,output_array)
    draw_mid_point_line(400,300,500,600,output_array)
    
    draw_mid_point_line(400,300,400,0,output_array)
    draw_mid_point_line(400,300,400,600,output_array)
    draw_mid_point_line(400,300,800,300,output_array)
    draw_mid_point_line(400,300,0,300,output_array)
    draw_mid_point_line(800,1070,800,0,output_array)

    draw_mid_point_line(400,300,0,600,output_array)
    draw_mid_point_line(400,300,1200,0,output_array)
    draw_mid_point_line(400,300,500,1079,output_array)
    draw_mid_point_line(400,300,300,1079,output_array)
    draw_mid_point_line(400,300,500,0,output_array)
    draw_mid_point_line(400,300,300,0,output_array)
    draw_mid_point_line(0,1079,1919,1078,output_array)
    draw_mid_point_line(0,1,1919,2,output_array)
    draw_mid_point_line(1,1079,0,0,output_array)
    draw_mid_point_line(1918,1079,1919,0,output_array)
    draw_mid_point_line(1444, 436, 1681, 797,output_array)

    return output_array


@timeit
def simple_line_timer(lines_num):

    #image array to draw lines on
    output_array = [[0 for i in range(1920)] for i in range(1080)]
    random_points = [[randint(0,1919), randint(0,1079)] for i in range(lines_num*2)]

    for i in range(lines_num):
        draw_simple_line(random_points[i][0],random_points[i][1],random_points[i+lines_num][0],random_points[i+lines_num][1], output_array)
    return output_array


@timeit
def mid_point_timer(lines_num):
    #image array to draw lines on
    output_array = [[0 for i in range(1920)] for i in range(1080)]
    random_points = [[randint(0,1919), randint(0,1079)] for i in range(lines_num*2)]

    for i in range(lines_num):
         draw_mid_point_line(random_points[i][0],random_points[i][1],random_points[i+lines_num][0],random_points[i+lines_num][1], output_array)
    return output_array


#convert NumPy array to pillow Image and write to file

filtered_aray = np.asarray(file_test_mid_point())
eq_img = Image.fromarray(filtered_aray).convert("RGB")
eq_img.save(mid_point_save_filename)

filtered_aray = np.asarray(mid_point_timer(10))
eq_img = Image.fromarray(filtered_aray).convert("RGB")
eq_img.save("10_timer_"+mid_point_save_filename)

filtered_aray = np.asarray(mid_point_timer(10_000))
eq_img = Image.fromarray(filtered_aray).convert("RGB")
eq_img.save("timer_"+mid_point_save_filename)

filtered_aray = np.asarray(file_test_simple_line())
eq_img = Image.fromarray(filtered_aray).convert("RGB")
eq_img.save(simple_line_save_filename)

filtered_aray = np.asarray(simple_line_timer(10))
eq_img = Image.fromarray(filtered_aray).convert("RGB")
eq_img.save("10_timer_"+simple_line_save_filename)

filtered_aray = np.asarray(simple_line_timer(10_000))
eq_img = Image.fromarray(filtered_aray).convert("RGB")
eq_img.save("timer_"+simple_line_save_filename)
#timer section - the times for each function will be printed in terminal
