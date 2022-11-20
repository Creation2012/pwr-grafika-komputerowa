#!/usr/bin/env python3
import sys
import random
import time

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def triangle(size):
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-size, -size/2)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, size)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(size, -size/2)
    glEnd()

    #glBegin(GL_TRIANGLES)
    #glColor3f(0.0, 0.0, 1.0)
    #glVertex2f(0.0, 0.0)
    #glColor3f(0.0, 1.0, 0.0)
    #glVertex2f(0.0, 50.0)
    #glColor3f(1.0, 0.0, 0.0)
    #glVertex2f(-50.0, 0.0)
    #glEnd()

    glFlush()

def square(x,y,a,b):
    #glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.1, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y+a)
    glVertex2f(x+b, y)
    glEnd()

    glColor3f(0.1, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x+b, y+a)
    glVertex2f(x+b, y)
    glVertex2f(x, y+a)
    glEnd()

    glFlush()

def sierpinski(x,y,a,d,start=False):
    print(f"x:{x}, y:{y}, a:{a}, d:{d}")
    if d == -1:
        return

    #glColor3f(1.0,1.0,1.0) if not start else glColor3f(0.1,0.0,0.0)
    glColor3f(random.random(),random.random(),random.random()) if not start else glColor3f(0.1,0.0,0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y+a)
    glVertex2f(x+a, y)
    glEnd()

    #glColor3f(1.0,1.0,1.0) if not start else glColor3f(0.1,0.0,0.0)
    #glColor3f(random.random(),random.random(),random.random()) if not start else glColor3f(0.1,0.0,0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x+a, y+a)
    glVertex2f(x+a, y)
    glVertex2f(x, y+a)
    glEnd()

    glFlush()
    
    d = d-1

    if start:
        sierpinski(x/3, y/3, a/3, d)
    else:
        # lewa strona (pierwsza kolumna)
        sierpinski(x - a + a/3, y + a/3, a/3, d)
        sierpinski(x - a + a/3, y + a + a/3, a/3, d)
        sierpinski(x - a + a/3, y - a + a/3, a/3, d)

        # srodek (druga kolumna)
        # sierpinski(x - a + a/3, y + a/3, a/3, d) skip srodka - bo wypelniony we wczeniejszym wykonaniu
        sierpinski(x + a/3, y + a + a/3, a/3, d)
        sierpinski(x + a/3, y - a + a/3, a/3, d)

        # prawa strona (trzecia kolumna)
        sierpinski(x + a + a/3, y + a/3, a/3, d)
        sierpinski(x + a + a/3, y + a + a/3, a/3, d)
        sierpinski(x + a + a/3, y - a + a/3, a/3, d)

   # sierpinski(x + i/3, y + 4/3 * i, i/3, d)
   # sierpinski(x + i/3, y + 7/3 * i, i/3, d)
   # sierpinski(x + 4/3*i, y + i/3, i/3, d)
   # sierpinski(x + 4/3*i, y + 4/3*i, i/3, d) 
   # sierpinski(x + 4/3*i, y + 7/3*i, i/3, d)
   # sierpinski(x + 7/3*i, y + i/3, i/3, d)
   # sierpinski(x + 7/3*i, y + 4/3*i, i/3, d)
   # sierpinski(x + 7/3*i, y + 7/3*i, i/3, d)


def square_rnd(x,y,a,b,d=0.0):
    glClear(GL_COLOR_BUFFER_BIT)
    random.seed(d)
    glBegin(GL_TRIANGLES)
    x_deform = random.random()
    y_deform = random.random()
    c1 = glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, y)
    c2 = glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x, (y+a) * y_deform)
    c3 = glColor3f(random.random(), random.random(), random.random())
    glVertex2f((x+b) * x_deform, y)
    glEnd()

    glBegin(GL_TRIANGLES)
    c3
    glVertex2f((x+b) * x_deform, (y+a) * y_deform)
    c1
    glVertex2f((x+b) * x_deform, y)
    c2
    glVertex2f(x, (y+a) * y_deform)
    glEnd()

    glFlush()

def square(x,y,a,b,color):
    #glClear(GL_COLOR_BUFFER_BIT)
    #glColor3f(0.1, 0.0, 0.0)
    color
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y+a)
    glVertex2f(x+b, y)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x+b, y+a)
    glVertex2f(x+b, y)
    glVertex2f(x, y+a)
    glEnd()

    glFlush()

def render(time):
    #triangle(60)
    #square(0,0,50,80,glColor3f(0.5, 0.0, 0.0))
    #square_rnd(0,0,50,90,3.5)
    sierpinski(-100.0, -100.0, 200.0, 6, True)
    #maze(100,5)

def maze(size,s):
    shift = 2 
    x_start = -size/2
    y_start = -size/2
    mul = size / s
    tab = [[0] * s]*s
    square(x_start,y_start,size+shift,size+shift,glColor3f(5.0, 0.0, 0.0))
    for i in range(0,s):
        for j in range(0,s):
            square(x_start + i * mul + shift, y_start + j * mul + shift, mul - shift, mul - shift,glColor3f(1.0, 1.0, 1.0)) 
            tab[i][j] = 1 # tu przechowywac miejsce (x,y)


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT)
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()

