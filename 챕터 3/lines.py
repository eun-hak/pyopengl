from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy
xRot = 0.0
yRot = 0.0
GL_PI = 3.1415


def RenderScene():
    global x
    global y
    global z
    global angle
    global GL_PI
    glClear(GL_COLOR_BUFFER_BIT)

    glPushMatrix()
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    glBegin(GL_LINES)

    z = 0.0

    for angle in numpy.arange(0.0, GL_PI, (GL_PI / 20.0)):

        x = 50.0*math.sin(angle)
        y = 50.0*math.cos(angle)
        glVertex3f(x, y, z)

        x = 50.0*math.sin(angle+GL_PI)
        y = 50.0*math.cos(angle+GL_PI)
        glVertex3f(x, y, z)

    glEnd()

    glPopMatrix()

    glutSwapBuffers()


def SetupRC():

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glColor3f(0.0, 1.0, 0.0)


def SpecialKeys(key, x, y):
    global xRot
    global yRot

    if(key == GLUT_KEY_UP):
        xRot -= 5.0

    if(key == GLUT_KEY_DOWN):
        xRot += 5.0

    if(key == GLUT_KEY_LEFT):
        yRot -= 5.0

    if(key == GLUT_KEY_RIGHT):
        yRot += 5.0

    if(key > 356.0):
        xRot = 0.0

    if(key < -1.0):
        xRot = 355.0

    if(key > 356.0):
        yRot = 0.0

    if(key < -1.0):
        yRot = 355.0

    glutPostRedisplay()


def ChangeSize(w, h):

    global nRange
    nRange = 100.0

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if(w <= h):
        glOrtho(-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
    else:
        glOrtho(-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Lines Example")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
