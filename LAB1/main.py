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
    d = d-1
    if d == 0:
        return

    glColor3f(1.0,1.0,1.0) if not start else glColor3f(0.1,0.0,0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y+a)
    glVertex2f(x+a, y)
    glEnd()

    glColor3f(1.0,1.0,1.0) if not start else glColor3f(0.1,0.0,0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x+a, y+a)
    glVertex2f(x+a, y)
    glVertex2f(x, y+a)
    glEnd()

    glFlush()
    
    i = a
    if start:
        sierpinski(x + i, y + i, i, d)

    sierpinski(x + i/3, y + i/3, i/3, d)
    sierpinski(x + i/3, y + 4/3 * i, i/3, d)
    sierpinski(x + i/3, y + 7/3 * i, i/3, d)
    sierpinski(x + 4/3*i, y + i/3, i/3, d)
    #sierpinski(x + 4/3*i, y + 4/3*i, i/3, False) 
    sierpinski(x + 4/3*i, y + 7/3*i, i/3, d)
    sierpinski(x + 7/3*i, y + i/3, i/3, d)
    sierpinski(x + 7/3*i, y + 4/3*i, i/3, d)
    sierpinski(x + 7/3*i, y + 7/3*i, i/3, d)

def square_rnd(x,y,a,b,d=0.0):
    #glClear(GL_COLOR_BUFFER_BIT)

    random.seed(d)
    glColor3f(random.random(), random.random(), random.random())
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, (y+a) * d)
    glVertex2f((x+b) * d, y)
    glEnd()

    glColor3f(random.random(), random.random(), random.random())
    glBegin(GL_TRIANGLES)
    glVertex2f((x+b) * d, (y+a) * d)
    glVertex2f((x+b) * d, y)
    glVertex2f(x, (y+a) * d)
    glEnd()

    glFlush()

def square(x,y,a,b):
    glClear(GL_COLOR_BUFFER_BIT)

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

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.3, 1.0, 0.9)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glColor3f(1.0, 0.2, 0.4)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(-50.0, 0.0)
    glEnd()

    glFlush()


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
        #render(glfwGetTime())
        #square(0,0,50,60)
        #square_rnd(0,0,10,20,1.0)
        sierpinski(-100.0, -100.0, 200.0, 5, True)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()
