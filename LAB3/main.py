#!/usr/bin/env python3
import sys
import time as t
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer_beg = [0.0, 0.0, 10.0]
viewer = viewer_beg

theta = 0.0
phi = 0.0
pix2angle = 1.0
scale = 1.0
R = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

direction = 1
up_swap = 0
upY = 1.0

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)

def calc_eye():
    global theta
    global phi
    global R
    check = 360
    yaw = abs(np.radians(theta % check))
    pitch = abs(np.radians(phi % check))
    roll = abs(np.radians(R % check))
    x = R * np.cos(abs(np.radians(theta%check))) * np.cos(abs(np.radians(phi%check)))
    y = R * np.sin(abs(np.radians(phi%check)))
    z = R * np.sin(abs(np.radians(theta%check))) * np.cos(abs(np.radians(phi%check)))

    return [x,y,z]

def render(time):
    global theta
    global phi
    global scale
    global R
    global viewer
    global direction

    global upY
    slp = .001

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # theta - kąt azymutu
    # phi - kąt elewacji

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        theta = theta % 360
        phi += delta_y * pix2angle
        phi = phi % 360

    if phi > 180:
        phi -= 2 * 180
    elif phi <= -180:
        phi += 2 * 180

    if phi < -180 / 2 or phi > 180 / 2:
        upY = -1.0
    else:
        upY = 1.0

    if phi == 90 or phi == 270:
        upY = -upY
        phi += 1

    gluLookAt(viewer_beg[0], viewer_beg[1], viewer_beg[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    #glRotatef(theta, 0.0, 1.0, 0.0)
    #glRotatef(phi, 1.0, 0.0, 0.0)

    zoomin = 0.0 # nie mogą być ujemne
    zoomout = 5.0
    if right_mouse_button_pressed:
        #scale = 2.0
        if zoomin < R + 0.05 * delta_y  < zoomout: # nie ma co ujemnych jak R startuje 1.0
            R += 0.05 * delta_y
    else:
        #scale = 1.0
        R = 1.0

    #glScalef(scale,scale,scale)

    #gluLookAt(viewer[0], viewer[1], viewer[2],
    #          0.0, 0.0, 0.0, 
    #          0.0, upY, 0.0)

    old_pos = viewer[1]
    viewer = calc_eye()
    direction = viewer[1] - old_pos

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, upY, 0.0)

    axes()
    example_object()

    glFlush()

def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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

