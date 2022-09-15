from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGLCommon import *
import numpy
import math
import random
SMALL_STARS = 100

vSmallStars = [GLTVector2()] * SMALL_STARS
MEDIUM_STARS = 40

vMediumStars = [GLTVector2()] * MEDIUM_STARS
LARGE_STARS = 15

vLargeStars = [GLTVector2()] * LARGE_STARS
SCREEN_X = 800
SCREEN_Y = 600


def ProcessMenu(value):

    while (True):

        if value == 1:

            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_BLEND)
            glEnable(GL_POINT_SMOOTH)
            glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            glEnable(GL_POLYGON_SMOOTH)
            glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
            break

        elif value == 2:
            glDisable(GL_BLEND)
            glDisable(GL_LINE_SMOOTH)
            glDisable(GL_POINT_SMOOTH)
            glDisable(GL_POLYGON_SMOOTH)
            break

        else:
            break

    glutPostRedisplay()


def RenderScene():

    global i
    global x
    global y
    global r
    global angle
    x = 700.0
    y = 500.0
    r = 50.0
    angle = 0.0

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glColor3f(1.0, 1.0, 1.0)

    glPointSize(1.0)
    glBegin(GL_POINTS)

    for i in range(0, SMALL_STARS, 1):
        glVertex2fv(vSmallStars[i].value)
    glEnd()

    glPointSize(3.05)
    glBegin(GL_POINTS)
    for i in range(0, MEDIUM_STARS, 1):
        glVertex2fv(vMediumStars[i].value)
    glEnd()

    glPointSize(5.5)
    glBegin(GL_POINTS)
    for i in range(0, LARGE_STARS, 1):
        glVertex2fv(vLargeStars[i].value)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)

    for angle in numpy.arange(0, 2.0 * 3.141592, 0.1):

        glVertex2f(x + float(math.cos(angle)) * r,
                   y + float(math.sin(angle)) * r)
        glVertex2f(x + r, y)
    glEnd()

    glLineWidth(3.5)
    glBegin(GL_LINE_STRIP)
    glVertex2f(0.0, 25.0)
    glVertex2f(50.0, 100.0)
    glVertex2f(100.0, 25.0)
    glVertex2f(225.0, 125.0)
    glVertex2f(300.0, 50.0)
    glVertex2f(375.0, 100.0)
    glVertex2f(460.0, 25.0)
    glVertex2f(525.0, 100.0)
    glVertex2f(600.0, 20.0)
    glVertex2f(675.0, 70.0)
    glVertex2f(750.0, 25.0)
    glVertex2f(800.0, 90.0)
    glEnd()

    glutSwapBuffers()


def SetupRC():
    global vSmallStars
    global i

    for i in range(0, SMALL_STARS, 1):
        vSmallStars[i].value[0] = (random.randrange(0, 32676) % SCREEN_X)
        vSmallStars[i].value[1] = (random.randrange(0, 32676) %
                                   (SCREEN_Y - 100))+100.0

    for i in range(0, MEDIUM_STARS, 1):
        vMediumStars[i].value[0] = (
            random.randrange(0, 32676) % SCREEN_X * 10)/10.0
        vMediumStars[i].value[1] = (random.randrange(0, 32676) %
                                    (SCREEN_Y - 100))+100.0

    for i in range(0, LARGE_STARS, 1):
        vLargeStars[i].value[0] = (
            random.randrange(0, 32676) % SCREEN_X*10)/10.0
        vLargeStars[i].value[1] = (random.randrange(0, 32676) %
                                   (SCREEN_Y - 100)*10.0) / 10.0 + 100.0

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glColor3f(0.0, 0.0, 0.0)


def ChangeSize(w,  h):

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(0.0, SCREEN_X, 0.0, SCREEN_Y)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Smoothing Out The Jaggies")

glutCreateMenu(ProcessMenu)
glutAddMenuEntry("Antialiased Rendering", 1)
glutAddMenuEntry("Normal Rendering", 2)
glutAttachMenu(GLUT_RIGHT_BUTTON)

glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
