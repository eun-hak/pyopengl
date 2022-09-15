from tkinter import W
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
dRadius = 0.1
dAngle = 0.0


def RenderScene():
    global dRadius
    global dAngle

    glClearColor(0.0, 0.0, 1.0, 0.0)

    if(dAngle == 0.0):
        glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_POINTS)
    glVertex2d(dRadius * math.cos(dAngle), dRadius * math.sin(dAngle))
    glEnd()

    dRadius *= 1.01
    dAngle += 0.1

    if(dAngle > 30.0):

        dRadius = 0.1
        dAngle = 0.0

    glFlush()


def Timer(value):
    glutTimerFunc(50, Timer, 0)
    glutPostRedisplay()


def ChangeSize(w, h):

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(-4.0, 4.0, -3.0, 3.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_RGB)
glutInitWindowSize(800, 600)
glutCreateWindow("OpenGL Single Buffered")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
glutTimerFunc(50, Timer, 0)
glutMainLoop()
