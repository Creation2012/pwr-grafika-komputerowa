#!/usr/bin/env python3
import sys
import numpy as np 

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image
import glob

viewer = [0.0, 0.0, 10.0]

upY = 1.0

theta = 0.0
phi = 0.0
pix2angle = 1.0

R = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

current_texture = 0

ids = []
textures = None
texture_idx = 0

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
    
    return [x,y,z,1.0]

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    images = []
    global ids
    global textures
    glEnable(GL_TEXTURE_2D)

    for filename in glob.glob('tekstury/*'):
        im=Image.open(filename)
        images.append(im)

    textures = glGenTextures(len(images))

    for i, img in enumerate(images):
        glBindTexture(GL_TEXTURE_2D, textures[i])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, img.size[0], img.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, img.tobytes("raw", "RGB", 0, -1)
        )

def render(time):
    global viewer
    global theta
    global phi
    global upY

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #gluLookAt(viewer[0], viewer[1], viewer[2],
    #          0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    gluLookAt(0.0,0.0, 10.0,
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    viewer = calc_eye()

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        theta = theta % 360
        phi += delta_y * pix2angle
        phi = phi % 360

    if phi > 180:
        phi -= 360
    elif phi <= -180:
        phi += 360

    if phi < -90 or phi > 90:
        upY = -1.0
    else:
        upY = 1.0

    if phi == 90 or phi == 270:
        upY = -upY
        phi += 1

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)
    glTranslatef(viewer[0],viewer[1],viewer[2])

    #square()
    #pyramid()
    sphere()


def square():
    glScalef(3.0,3.0,3.0)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glEnd()
    glFlush()

def pyramid():
    #glScalef(3.0,3.0,3.0)

    glBindTexture(GL_TEXTURE_2D, textures[texture_idx])
    glBegin(GL_TRIANGLES)

    # up
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    # right
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)

    # back
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)

    # left
    glTexCoord2f(0.0, 0.0)
    glVertex3f( 0.0, 1.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glEnd()

def sphere():
    glBindTexture(GL_TEXTURE_2D, textures[texture_idx])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluQuadricTexture(quadric, True)
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

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
    global textures
    global texture_idx
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        texture_idx = texture_idx + 1 if (texture_idx + 1) < len(textures) else 0

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


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

