#!/usr/bin/env python3
import sys
import random
import time
import numpy as np
import kruskal
import keyboard

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

cell_size = 1
shift = 2
x_start = 0
y_start = 0
mul = 1
size = 100
s = 20 

def startup():
    update_viewport(None, 1600, 1600)
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

    glColor3f(1, 1, 1)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y+a)
    glVertex2f(x+b, y)
    glEnd()

    glColor3f(1, 1, 1)
    glBegin(GL_TRIANGLES)
    glVertex2f(x+b, y+a)
    glVertex2f(x+b, y)
    glVertex2f(x, y+a)
    glEnd()

    glFlush()

def sierpinski(x,y,a,d,start=False):
    #print(f"x:{x}, y:{y}, a:{a}, d:{d}")
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

def square_clr(x,y,a,b,color):
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

def x_wall(x,y):
    square(x + shift, y, shift, cell_size) # poziomo 

def y_wall(x,y):
    square(x,y+shift,cell_size,shift) # pionowo

def detect_wall(i, j, s):
    if (i - j) < 0:
        y = int(i/s)
        if y > s:
            y = y - 1

        if (abs(i-j)) % s == 0:
            #gorny
            #x = max(i,j) % (s - 1) 
            x = max(i,j) % s
            y = y + 1
            x_pos = x_start + x * mul + shift
            y_pos = y_start + y * mul
            square(x_pos, y_pos,shift, cell_size)
        else:
            #lewa tu jednak prawa???
            #x = min(i,j) % (s - 1) + 1
            x = max(i,j) % s
            x_pos = x_start + x * mul 
            y_pos = y_start + y * mul + shift
            square(x_pos, y_pos,cell_size, shift)
    elif (i - j) >= 0:
        x = min(i,j) % (s - 1) + 1
        y = int(min(i,j)/s)
        if y > s:
            y = y - 1
        if (i - j) % s == 0:
            #dolny
            x = i % (s - 1)
            y = y + 1
            x_pos = x_start + x * mul + shift
            y_pos = y_start + y * mul
            square(x_pos, y_pos,shift, cell_size)
        else:
            #prawa tu lewa
            x = i % (s - 1)
            x_pos = x_start + x * mul
            y_pos = y_start + y * mul + shift 
            square(x_pos, y_pos, cell_size, shift) 

    #print("i: ", i, "j: ", j)
    #print("x_pos: ", x_pos, "y_pos: ", y_pos)
    #print("x: ", x, " y: ", y)

def neighbours(graph,i,j,size,s):
    if i - s >= 0 and graph[i-s][j] == 0:
        graph[i-s][j] = random.randint(1,100)
        graph[j][i-s] = graph[i-s][j]
    if i + s < size and graph[i+s][j] == 0:
        graph[i+s][j] = random.randint(1,100)
        graph[j][i+s] = graph[i+s][j]
    if j - 1 >= 0 and (j % s - 1) > s:
        graph[i][j-1] = random.randint(1,100)
        graph[j-1][i] = graph[i][j-1]
    if (j % s + 1) < s:
        graph[i][j+1] = random.randint(1,100)
        graph[j+1][i] = graph[i][j+1] 

    return graph

def maze_entrance_and_exit():
    x_pos = x_start + shift 
    y_pos = y_start
    square(x_pos, y_pos,shift, cell_size)
    x_pos = x_pos + size - 1 * mul 
    y_pos = y_pos + size
    square(x_pos, y_pos,shift, cell_size)

def maze_foundry(sarg,field):
    global s
    s = field
    global size
    size = sarg
    global shift
    shift = 2
    global x_start
    x_start = -size/2
    global y_start
    y_start = -size/2
    global mul
    mul = size / s
    global cell_size
    cell_size = mul - shift

    square_clr(x_start,y_start,size+shift,size+shift,glColor3f(5.0, 0.0, 0.0))

    for i in range(0,s):
        for j in range(0,s):
            x_pos = x_start + i * mul + shift
            y_pos = y_start + j * mul + shift
            square_clr(x_pos, y_pos, cell_size, mul - shift,glColor3f(1.0, 1.0, 1.0)) 

def maze_kruskal():
    global visited
    global s
    visited = set()

    #prinr(graph)
    path = kruskal.kruskalMST(graph,s * s)
    #print(path)

    #print("cell_size: ", cell_size, " mul: ", mul)
    #print("x_start: ", x_start, " y_start:", y_start)
    #print()
    #print(path)
    for wall in path:
        detect_wall(wall[0], wall[1], s)

def render(time):
    #triangle(60)
    #square(0,0,50,80,glColor3f(0.5, 0.0, 0.0))
    #square_rnd(0,0,50,90,3.5)
    #sierpinski(-100.0, -100.0, 200.0, 6, True)
    global s
    maze_foundry(150,s)
    maze_kruskal()
    maze_entrance_and_exit()

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

    global graph
    global s
    graph = np.zeros((s*s,s*s))
    for i in range(0,s*s):
        graph = neighbours(graph,i,i,s,s)

    startup()
    while not glfwWindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT)
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
        if keyboard.is_pressed('spacebar'):
            for i in range(0,s*s):
                graph = neighbours(graph,i,i,s,s)

    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()

