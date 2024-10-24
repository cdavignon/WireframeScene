# Cole Davignon & Aidan Armellino
# Assignment 2
# 10/24/24
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

car_location = 0.0 # Car's location on z-axis
travel_distance = 0.05 # Distance of how far car moves
move_car = True # Allows car to move or not, depending on space bar pressed
rotation = 0 # Allows rotation, changes if left key vs right key held
rotate_left = False # Rotates left on key held down
rotate_right = False # Rotates right on key held down
wheel_rotation = 0.0 # Allows wheels to rotate in animation

def main():    
    init()
    main_loop()

def init():
    global running, cyl
    # Initialization, similar to light example code
    pygame.init()
    screenSize = (800, 600)
    pygame.display.set_mode(screenSize, pygame.DOUBLEBUF | pygame.OPENGL)
    # Perspective
    gluPerspective(45, (screenSize[0] / screenSize[1]), 0.1, 50.0)
    # Shifted back 20 units
    glTranslatef(0.0, 0.0, -20)
    # Car is seen at a more top-down angle
    glRotatef(15, 1, 0, 0) 
    running = True 
    # Quadric for cylinders and wheels
    cyl = gluNewQuadric()  

def draw_cube():
    vertices = [
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, -1],
        [-1, 1, -1],
        [1, 1, 1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, 1, 1],
    ]
    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7)
    )
    # Draws cube in position
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_car():
    glPushMatrix()
    glTranslatef(0, 0, car_location) # Translates car's location on z axis, changes when animated
    glRotatef(90, 0, 1, 0)
    # Bottom Cube
    glPushMatrix()
    glScalef(2.0, 0.5, 1.0)
    draw_cube()
    glPopMatrix()
    # Top Cube
    glPushMatrix()
    glTranslatef(0, 1, 0)
    glScalef(1.0, 0.5, 1.0)
    draw_cube()
    glPopMatrix()
    # Add wheels
    draw_wheels()
    glPopMatrix()

def draw_wheels():
    global wheel_rotation, cyl
    glPushMatrix()
    gluQuadricDrawStyle(cyl, GLU_LINE)
    # Wheel location is relative to direction car is first going
    # Draw front left wheel
    glPushMatrix()
    glTranslatef(-1.5, -1, 1)
    glRotatef(wheel_rotation, 0, 0, 1)
    gluCylinder(cyl, 0.5, 0.5, 0.5, 16, 16)
    glPopMatrix()
    # Draw rear left wheel
    glPushMatrix()
    glTranslatef(1.5, -1, 1)
    glRotatef(wheel_rotation, 0, 0, 1)
    gluCylinder(cyl, 0.5, 0.5, 0.5, 16, 16)
    glPopMatrix()
    # Draw front right wheel
    glPushMatrix()
    glTranslatef(-1.5, -1, -1.5)
    glRotatef(wheel_rotation, 0, 0, 1)
    gluCylinder(cyl, 0.5, 0.5, 0.5, 16, 16)
    glPopMatrix()
    # Draw rear right wheel
    glPushMatrix()
    glTranslatef(1.5, -1, -1.5)
    glRotatef(wheel_rotation, 0, 0, 1)
    gluCylinder(cyl, 0.5, 0.5, 0.5, 16, 16)
    glPopMatrix()
    glPopMatrix()

def draw_side_cylinders():
    global cyl
    glPushMatrix()
    gluQuadricDrawStyle(cyl, GLU_LINE)
    # Draw left cylinder
    glTranslatef(-5.0, -1, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(cyl, 1.5, 0, 4, 32, 32)
    glPopMatrix()
    # Draw right cylinder
    glPushMatrix()
    glTranslatef(5.0, -1, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(cyl, 1.5, 0, 4, 32, 32)
    glPopMatrix()

def draw_scene():
    draw_car()
    draw_side_cylinders()

def main_loop():
    global car_location, travel_distance, move_car, rotate_left, rotate_right, running
    while running == True:
        for event in pygame.event.get():
            # Allows quit on 'X' button
            if event.type == pygame.QUIT:
                running = False
            # Key down, to hold rotate instead of pressing multiple times
            if event.type == KEYDOWN:
                # ASCII code for Esc is 27; ends scene
                if event.key == 27:
                    running = False
                # Space stops animation
                if event.key == K_SPACE:
                    move_car = not move_car
                # Left arrow sets rotate to true
                if event.key == K_LEFT:
                    rotate_left = True
                # Right arrow sets rotate to true
                if event.key == K_RIGHT:
                    rotate_right = True
            # If key is up, stop rotating
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    rotate_left = False
                if event.key == K_RIGHT:
                    rotate_right = False
        # Clear screen, similar to light example code
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFlush()
        # Checks if scene is rotating
        isRotating()
        # Allows rotation to the be changed
        glPushMatrix()
        glRotatef(rotation, 0, 1, 0)
        # Animation function        
        animate()
        # Draws car and side cylinders
        draw_scene()
        glPopMatrix()
        clock = pygame.time.Clock()
        pygame.display.flip()
        clock.tick(60)

def isRotating():
    global rotate_left, rotate_right, rotation
    # If left key is pressed, rotate CW
    if rotate_left == True:
        rotation -= 1
    # Else if right key is pressed, rotate CCW
    if rotate_right == True :
        rotation += 1
    
def animate():
    global car_location, travel_distance, move_car, wheel_rotation
    if move_car == True:
        car_location += travel_distance  # Update car's z position by 0.05 every time
        if travel_distance > 0:  # If car is moving forward, wheels rotate in that direction
            wheel_rotation += 2
        else:  # If car is moving backward, wheels rotate in other direction
            wheel_rotation -= 2 
        
        if car_location >= 8 or car_location <= -8: # If car is beyond paramaters, reverse the direction
            travel_distance = -travel_distance # sets reversal by making distance negative  

if __name__ == "__main__": main()
