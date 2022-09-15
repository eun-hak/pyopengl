
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def RenderScene():

    glClear(GL_COLOR_BUFFER_BIT)

    glFlush()


def SetupRC():

    glClearColor(0.0, 0.0, 1.0, 1.0)


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(800, 600)
glutCreateWindow("Simple")
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
