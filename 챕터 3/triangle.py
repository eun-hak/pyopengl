from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy


xRot = 0.0
yRot = 0.0
GL_PI = 3.1415

iCull = 0
iOutline = 0
iDepth = 0


def ProcessMenu(value):
    global iCull
    global iOutline
    global iDepth
    while (True):
        if iDepth != iDepth:
            break
        elif iCull != iCull:
            break
        elif iOutline != iOutline:
            break

    glutPostRedisplay()


def RenderScene():
    global x
    global y
    global iPivot
    global angle

    iPivot = 1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if(iCull):
        glEnable(GL_CULL_FACE)
    else:
        glDisable(GL_CULL_FACE)

    if(iDepth):
        glEnable(GL_DEPTH_TEST)
    else:
        glDisable(GL_DEPTH_TEST)

    if(iOutline):
        glPolygonMode(GL_BACK, GL_LINE)
    else:
        glPolygonMode(GL_BACK, GL_FILL)

    glPushMatrix()
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    glBegin(GL_TRIANGLE_FAN)

    glVertex3f(0.0, 0.0, 75.0)

    for angle in numpy.arange(0, 2*GL_PI, GL_PI/8):

        x = 50.0*math.sin(angle)
        y = 50.0*math.cos(angle)

        if((iPivot % 2) == 0):
            glColor3f(0.0, 1.0, 0.0)
        else:
            glColor3f(1.0, 0.0, 0.0)

        iPivot += 1
        glVertex2f(x, y)

    glEnd()

    glBegin(GL_TRIANGLE_FAN)

    glVertex2f(0.0, 0.0)

    for angle in numpy.arange(0, 4*GL_PI, GL_PI/8):

        x = 50.0*math.sin(angle)
        y = 50.0*math.cos(angle)

        if((iPivot % 2) == 0):
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(0.0, 1.0, 0.0)

        iPivot += 1

        glVertex2f(x, y)

    glEnd()

    glPopMatrix()

    glutSwapBuffers()


def SetupRC():

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glColor3f(0.0, 1.0, 0.0)
    glShadeModel(GL_FLAT)
    glFrontFace(GL_CW)


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
glutCreateWindow("Triangle Culling Example")
glutCreateMenu(ProcessMenu)
glutAddMenuEntry("Toggle depth test", 1)
glutAddMenuEntry("Toggle cull backface", 2)
glutAddMenuEntry("Toggle outline back", 3)
glutAttachMenu(GLUT_RIGHT_BUTTON)
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
