#!/usr/bin/env python3
import sys
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0, 1.0]
viewer_light = [0.0, 0.0, 10.0, 1.0]

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

light_ambient = [0.0, 0.5, 0.0, 1.0]
light_diffuse = [0.2, 0.2, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, -25.0, 1.0]

light_ambient_s = [0.3, 0.0, 0.0, 1.0]
light_diffuse_s = [0.1, 0.0, 0.1, 1.0]
light_specular_s = [0.8, 0.8, 0.8, 1.0]
light_position_s = [25.0, 0.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

parameters_name = ["light_ambient", "light_diffuse", "light_specular"]
parameters = [light_ambient, light_diffuse, light_specular]
current_parameter = 0

rgb_position = ["R","G","B"]
position = [0,1,2]
current_position = 0

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # first light
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_diffuse)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_ambient)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # second light
    #glLightfv(GL_LIGHT1, GL_AMBIENT, light_diffuse_s)
    #glLightfv(GL_LIGHT1, GL_DIFFUSE, light_ambient_s)
    #glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular_s)
    #glLightfv(GL_LIGHT1, GL_POSITION, light_position_s)

    #glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    #glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    #glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    #glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    #glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    #glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    #glShadeModel(GL_SMOOTH)
    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT1)

def light_update():
    global viewer_light

    # first light
    glLightfv(GL_LIGHT0, GL_AMBIENT, parameters[0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, parameters[1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, parameters[2])
    glLightfv(GL_LIGHT0, GL_POSITION, viewer_light)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def shutdown():
    pass

def render(time):
    global theta
    global phi
    global upY
    global viewer_light

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

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

    # Budowa wyswietlanego obiektu
    #quadric = gluNewQuadric()
    #gluQuadricDrawStyle(quadric, GLU_FILL)
    #gluSphere(quadric, 3.0, 10, 10)
    #gluDeleteQuadric(quadric)

    #glRotatef(theta,0.1,1.0,0.0)
    #spin(time * 180 / np.pi)
    glPushMatrix()
    egg_triangles(35,time)
    glRotatef(time*180/np.pi%360, 0, 1, 0)
    glPopMatrix()

    offset = 30
    viewer_light = [x + offset for x in viewer_light]

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi,1.0,0.0,0.0)
    glScale(0.1,0.1,0.1)
    glTranslatef(viewer_light[0],viewer_light[1],viewer_light[2])

    glColor3f(0.8,0.8,0.1)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 3.0, 6, 5)
    gluDeleteQuadric(quadric)
    viewer_light = calc_eye()

    light_update()

    glFlush()

def xTrans(u,v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.cos(np.pi * v)

def yTrans(u,v):
    return 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5

def zTrans(u,v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.sin(np.pi * v)

def egg_triangles(N,time):
    #spin(time * 179 / np.pi )
    #global colors
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
            x = tab[i,j,0]
            y = tab[i,j,1]
            z = tab[i,j,2]
            glNormal3f(0,0,1)
            glVertex3f(x,y,z)

            x = tab[i,j+1,0]
            y = tab[i,j+1,1]
            z = tab[i,j+1,2]
            glNormal3f(0,0,1)
            glVertex3f(x,y,z)

            x = tab[i+1,j,0]
            y = tab[i+1,j,1]
            z = tab[i+1,j,2]
            glNormal3f(0,0,1)
            glVertex3f(x,y,z)

            x = tab[i,j+1,0]
            y = tab[i,j+1,1]
            z = tab[i,j+1,2]
            glNormal3f(0,0,1)
            glVertex(x,y,z)

            x = tab[i+1,j,0]
            y = tab[i+1,j,1]
            z = tab[i+1,j,2]
            glNormal3f(0,0,1)
            glVertex3f(x,y,z)

            x = tab[i+1,j+1,0]
            y = tab[i+1,j+1,1]
            z = tab[i+1,j+1,2]
            glNormal3f(0,0,1)
            glVertex3f(x,y,z)

    glEnd()

def calc_eye():
     global theta
     global phi
     global R
     check = 360
     yaw = abs(np.radians(theta % check))
     pitch = abs(np.radians(phi % check))
     roll = abs(np.radians(R % check))
     x = R * np.cos(abs(np.radians(theta%check))) * np.cos(abs(np.radians(phi%check)    ))
     y = R * np.sin(abs(np.radians(phi%check)))
     z = R * np.sin(abs(np.radians(theta%check))) * np.cos(abs(np.radians(phi%check)    ))
 
     return [x,y,z,1.0]

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
    global parameters
    global current_parameter
    global current_position

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        if current_parameter + 1 <= 2:
            current_parameter = current_parameter + 1
        else:
            current_parameter = 0

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        if current_position + 1 <= 2:
            current_position = current_position + 1
        else:
            current_position = 0

    if key == GLFW_KEY_EQUAL and action == GLFW_PRESS:
        if parameters[current_parameter][current_position] + 0.1 <= 1.0:
            parameters[current_parameter][current_position] += 0.1

    if key == GLFW_KEY_MINUS and action == GLFW_PRESS:
        if  parameters[current_parameter][current_position] - 0.1 >= 0.0:
            parameters[current_parameter][current_position] -= 0.1

    print(f"Current parameter: {parameters_name[current_parameter]}")
    print(f"{rgb_position[current_position]}: {parameters[current_parameter][current_position]:.1f}")
    print(f"{parameters_name[0]}:",end='')
    print(', '.join(f'{p:.1f}' for p in parameters[0]))
    print(f"{parameters_name[1]}:",end='')
    print(', '.join(f'{p:.1f}' for p in parameters[1]))
    print(f"{parameters_name[2]}:",end='')
    print(', '.join(f'{p:.1f}' for p in parameters[2]))


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
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
        #light_update()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()

