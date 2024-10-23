import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

car_z = 0.0 # Moves car forward and backward along z-axis
car_direction = 0.05 # Speed
move_car = True # Allows car to move or not
scene_rotation = 0 # Allows rotation
rotate_left = False # Rotates left on key held down, initialized as False
rotate_right = False # Rotates right on key held down, initialized as False

# Draws the cube
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
    #Draws cube
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_car():
    glPushMatrix()
    glTranslatef(0, 0, car_z) 
    glRotatef(90, 0, 1, 0) # Rotates car to face front
    
    # Bottom Cube
    glPushMatrix()
    glScalef(2.0, 0.5, 1.0)
    draw_cube()
    glPopMatrix()
    
    # Top Cube
    glPushMatrix()
    glTranslatef(0, 0.5, 0)
    glScalef(1.0, 0.5, 1.0)
    draw_cube()
    glPopMatrix()
    
    glPopMatrix()

def draw_scene():
    draw_car()

def main():
    global car_z, car_direction, move_car, scene_rotation, rotate_left, rotate_right
    
    # Initialization, similar to light example code
    pygame.init()
    screenSize = (800, 600)
    pygame.display.set_mode(screenSize, pygame.DOUBLEBUF | pygame.OPENGL)

    # Perspective
    gluPerspective(45, (screenSize[0] / screenSize[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)
    # Car is seen at a more top-down angle
    glRotatef(15, 1, 0, 0)
    
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            # Allows quit on 'X' button
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Key down, to hold rotate instead of pressing multiple times
            if event.type == KEYDOWN:
                # Esc quite
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                # Space stops animation
                if event.key == K_SPACE:
                    move_car = not move_car
                # Left arrow rotates
                if event.key == K_LEFT:
                    rotate_left = True
                # Right arrow rotates
                if event.key == K_RIGHT:
                    rotate_right = True
            # If key is up, stop rotates
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    rotate_left = False
                if event.key == K_RIGHT:
                    rotate_right = False
        # Clear screen, similar to light example code
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFlush()
        
        if rotate_left:
            scene_rotation -= 1
        if rotate_right:
            scene_rotation += 1
        
        # Allows rotation to the be changed
        glPushMatrix()
        glRotatef(scene_rotation, 0, 1, 0)
        
        # Move car between the left and right bounds, reversing when it hits the boundaries
        if move_car:
            car_z += car_direction  # Update car's z position
            if car_z >= 8 or car_z <= -8:
                car_direction = -car_direction  # Reverse the car's direction
        draw_scene()

        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__": main()
