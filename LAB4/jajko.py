#!/usr/bin/env python3
import sys
import numpy as np
import random
import time

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def shutdown():
    pass

def axes():
    #spin(time * 180 / np.pi)
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def xTrans(u,v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.cos(np.pi * v)

def yTrans(u,v):
    return 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5

def zTrans(u,v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.sin(np.pi * v)

def egg(N,time):
    spin(time * 180 / np.pi)
    glBegin(GL_POINTS)
    tab = np.zeros((N,N,3))
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)
            tab[i,j,0] = xTrans(u,v)
            tab[i,j,1] = yTrans(u,v)
            tab[i,j,2] = zTrans(u,v)
            
    for i in range(N):
        for j in range(N):
            x = tab[i,j,0]
            y = tab[i,j,1]
            z = tab[i,j,2]
            glVertex3f(x,y,z)
    glEnd()
    

def egg_lines(N,time):
    spin(time * 180 / np.pi)
    glBegin(GL_LINES)
    tab = np.zeros((N,N,3))
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)
            tab[i,j,0] = xTrans(u,v)
            tab[i,j,1] = yTrans(u,v)
            tab[i,j,2] = zTrans(u,v)

    for i in range(N):
        for j in range(N-1):
            x = tab[i,j,0]
            y = tab[i,j,1]
            z = tab[i,j,2]
            glVertex3f(x,y,z)
            x = tab[i,j+1,0]
            y = tab[i,j+1,1]
            z = tab[i,j+1,2]
            glVertex3f(x,y,z)

    for i in range(N-1):
        for j in range(N):
            x = tab[i,j,0]
            y = tab[i,j,1]
            z = tab[i,j,2]
            glVertex3f(x,y,z)
            x = tab[i+1,j,0]
            y = tab[i+1,j,1]
            z = tab[i+1,j,2]
            glVertex3f(x,y,z)

    glEnd()


def egg_triangles(N,time):
    spin(time * 180 / np.pi )
    global colors
    glBegin(GL_TRIANGLES)
    tab = np.zeros((N,N,3))
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)
            tab[i,j,0] = xTrans(u,v)
            tab[i,j,1] = yTrans(u,v)
            tab[i,j,2] = zTrans(u,v)


    for i in range(N-1):
        for j in range(N-1):
            glColor3f(colors[i,j,0], colors[i,j,1], colors[i,j,2])
            x = tab[i,j,0]
            y = tab[i,j,1]
            z = tab[i,j,2]
            glVertex3f(x,y,z)

            glColor3f(colors[i,j+1,0],colors[i,j+1,1],colors[i,j+1,2])
            x = tab[i,j+1,0]
            y = tab[i,j+1,1]
            z = tab[i,j+1,2]
            glVertex3f(x,y,z)

            glColor3f(colors[i+1,j,0],colors[i+1,j,1],colors[i+1,j,2])
            x = tab[i+1,j,0]
            y = tab[i+1,j,1]
            z = tab[i+1,j,2]
            glVertex3f(x,y,z)

            glColor3f(colors[i,j+1,0], colors[i,j+1,1],colors[i,j+1,2])
            x = tab[i,j+1,0]
            y = tab[i,j+1,1]
            z = tab[i,j+1,2]
            glVertex(x,y,z)

            glColor3f(colors[i+1,j,0],colors[i+1,j,1],colors[i+1,j,2])
            x = tab[i+1,j,0]
            y = tab[i+1,j,1]
            z = tab[i+1,j,2]
            glVertex3f(x,y,z)

            glColor3f(colors[i+1,j+1,0],colors[i+1,j+1,1], colors[i+1,j+1,2])
            x = tab[i+1,j+1,0]
            y = tab[i+1,j+1,1]
            z = tab[i+1,j+1,2]
            glVertex3f(x,y,z)

    glEnd()

def egg_special(N,time):
    spin(time * 180 / np.pi )
    global colors
    glBegin(GL_TRIANGLES)
    tab = np.zeros((N,N,3))
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)
            tab[i,j,0] = xTrans(u,v)
            tab[i,j,1] = yTrans(u,v)
            tab[i,j,2] = zTrans(u,v)

    for i in range(N):
        for j in range(N):
            for o in range(N):
                glColor3f(colors[i,j,0], tab[i,j,1], tab[i,j,2])
                x = tab[i,j,0]
                y = tab[i,j,1]
                z = tab[i,j,2]
                glVertex3f(x,y,z)
                glColor3f(colors[i,o,0], tab[i,o,1], tab[i,o,2])
                x = tab[i,o,0]
                y = tab[i,o,1]
                z = tab[i,o,2]
                glVertex3f(x,y,z)
                glColor3f(colors[j,o,0], tab[j,o,1], tab[j,o,2])
                x = tab[j,o,0]
                y = tab[j,o,1]
                z = tab[j,o,2]
                glVertex3f(x,y,z)

    glEnd()

def egg_stripes(N,time):
    spin(time * 180 / np.pi )
    global colors
    glBegin(GL_TRIANGLE_STRIP)
    tab = np.zeros((N,N,3))
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)
            tab[i,j,0] = xTrans(u,v)
            tab[i,j,1] = yTrans(u,v)
            tab[i,j,2] = zTrans(u,v)


    for i in range(N-1):
        for j in range(N-1):
            for o in range(N-1):
                #glColor3f(1.0,0.0,1.0)
                glColor3f(colors[i,j,0], tab[i,j,1], tab[i,j,2])

                x = tab[i,j,0]
                y = tab[i,j,1]
                z = tab[i,j,2]
                glVertex3f(x,y,z)
                glColor3f(colors[i,o,0], tab[i,o,1], tab[i,o,2])

                x = tab[j,i,0]
                y = tab[j,i,1]
                z = tab[j,i,2]
                glVertex3f(x,y,z)
    glEnd()

colors = np.random.rand(20,20,3)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #axes()
    #egg(100,time)
    #egg_lines(30,time)
    egg_triangles(15,time)
    #egg_stripes(15,time)
    #egg_special(20,time)
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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

