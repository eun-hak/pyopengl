from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *


def RenderScene():

    glClear(GL_COLOR_BUFFER_BIT)

    glShadeModel(GL_SMOOTH)

    glBegin(GL_TRIANGLES)

    glColor3ub(255, 0, 0)
    glVertex3f(0.0, 200.0, 0.0)

    glColor3ub(0, 255, 0)
    glVertex3f(200.0, -70.0, 0.0)

    glColor3ub(0, 0, 255)
    glVertex3f(-200.0, -70.0, 0.0)
    glEnd()

    glutSwapBuffers()


def SetupRC():

    glClearColor(0.0, 0.0, 0.0, 1.0)


def ChangeSize(w, h):

    global windowHeight, windowWidth

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    glLoadIdentity()

    if(w <= h):
        windowHeight = 250.0*h/w
        windowWidth = 250.0
    else:
        windowWidth = 250.0*w/h
        windowHeight = 250.0

    glOrtho(-windowWidth, windowWidth, -windowHeight, windowHeight, 1.0, -1.0)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("RGB Triangle")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
