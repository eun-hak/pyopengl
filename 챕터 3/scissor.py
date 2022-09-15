from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def RenderScene():

    glClearColor(0.0, 0.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glClearColor(1.0, 0.0, 0.0, 0.0)
    glScissor(100, 100, 600, 400)
    glEnable(GL_SCISSOR_TEST)
    glClear(GL_COLOR_BUFFER_BIT)

    glClearColor(0.0, 1.0, 0.0, 0.0)
    glScissor(200, 200, 400, 200)
    glClear(GL_COLOR_BUFFER_BIT)

    glDisable(GL_SCISSOR_TEST)

    glutSwapBuffers()


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
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 600)
glutCreateWindow("OpenGL Scissor")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
glutMainLoop()
