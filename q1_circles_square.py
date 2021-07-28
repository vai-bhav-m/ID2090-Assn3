#!/usr/bin/python3.8

# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Parameters chosen for this case
n = 15                                                                   # No. of spheres
r = np.sort(np.abs(np.random.normal(loc=4,scale=2,size = n)))[::-1]      # Randomly generated radii sorted in decreasing order
prec = 0.1                                                               # Precision paramter: determines the precision of movement of spheres while placing them

# Estimating initial size of bounding square from sum of areas of circles
s = (np.sum(np.pi*r*r))**0.5
print(f"Parameters for this trial:-\nNo of circles: {n}\nRadii of circles:\n{r}\nPrecision parameter: {prec}")
print(f"Initial guess of the side length of required square: {s:4.2f}\n")

image_n = 1                         # Counter to save generated images in a sequence
items = {                           # Items Dictionary: keeps count of all objects placed on the map
    'Square': [(0,0,s)],
    'Circles': [(r[0],r[0],r[0])]
}


# Defining some helphul helper functions
def plot_scenario():
    ''' This function plots the objects present in the items dictionary and saves the plot as a png image'''
    plt.clf()
    plt.title(f"Fitting each circle into a square with side {s:4.2f}")
    rectangle = plt.Rectangle((items['Square'][0][0],items['Square'][0][1]), items['Square'][0][2], items['Square'][0][2], ec='red', fc='None')    
    plt.gca().add_patch(rectangle)
    plt.xlim([-1,s+1])
    plt.ylim([-1,s+1])
    plt.gca().set_aspect('equal', adjustable='box')

    for x in items['Circles']:
        circle = plt.Circle((x[0], x[1]), x[2], ec='blue', fc='None')
        plt.gca().add_patch(circle)

    global image_n
    plt.savefig(f'sq_circle_plot_{image_n}.png')
    image_n += 1
    plt.show(block=False)
    plt.pause(0.01)


def check_overlap(x0,y0,r0):
    '''
    This function checks if a circle placed at (x0, y0) with radius r0 violates any of the following constraints:
    1. If the circle expands beyond any side of the bounding square
    2. If the circle overlaps with any other circle currently placed in the environment
    '''

    # Overlap with square
    if y0 - r0 < 0:                            # Circle extends beyond the bottom of the square
        return 'square bottom'
    elif y0 + r0 > s:                          # Circle extends beyond the top of the square
        return 'square top'
    elif x0 - r0 < 0:                          # Circle extends beyond the left edge of the square
        return 'square left'
    elif x0 + r0 > s:                          # Circle extends beyond the right edge of the square
        return 'square right'

    # Circle overlap with any of the already present circles
    for x in items['Circles']:
        d = ((x[0]-x0)**2 + (x[1]-y0)**2)**0.5
        if d < x[2] + r0:
            return 'circle overlap'

    return 'No overlap!'


def try_fit():
    '''
    This function attempts to fit all n circles in the given square. If it is unable to do so, it returns a 
    value suggesting that the square is too small for this operation.
    '''
    for radius in r[1:]:
        placed = 0
        x0, y0, r0 = radius, radius, radius
        basey = radius
        sq_small = 0
        while placed == 0:
            flag = check_overlap(x0, y0, r0)

            if flag == 'No overlap!':                    # Place the circle when there is no overlap
                items['Circles'].append((x0,y0,r0))
                placed = 1
                plot_scenario()

            elif flag == 'circle overlap':               # Moving the circle right by the prec parameter in case of circle overlap
                x0, y0 = x0+prec, y0

            elif flag == 'square right':                 # If the circle encounters the right boundary, attempt fitting
                x0, y0 = radius, basey + prec            # from the left boundary but from an increased height of 1*prec parameter
                basey += prec

            elif flag == 'square top':                   # If the circle encouters the top boundary, the bounding square is too small to accomodate all circles
                sq_small = 1
                break
        if sq_small == 1:
            print('Square is too small!')
            return 'No'
    return 'Yes'



plot_scenario()
code_works = try_fit()
while code_works == 'No':
    s += prec                         # Incrementing the size of the square if it's too small
    print(f'Changing the dimension of the square by {prec} to {s:4.2f} and re-trying fitting:')

    items = {
    'Square': [(0,0,s)],
    'Circles': [(r[0],r[0],r[0])]
    }

    prec = 0.1
    plot_scenario()
    code_works = try_fit()

print(f"\nLooks like we finally managed to fit all the circles in a square of side length = {s:5.3f} units")
plt.show()
