#!/usr/bin/env python
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    glClreaColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)

    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSwapInterval(1)

    startup()

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwWaitEvents()

    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()


