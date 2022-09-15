from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def RenderScene():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)
    glRectf(-25.0, 25.0, 25.0, -25.0)
    glFlush()


def SetupRC():
    glClearColor(0.0, 0.0, 1.0, 1.0)


def ChangeSize(w, h):
    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspectRatio = w / h

    if (w <= h):
        glOrtho(-100.0, 100.0, -100 / aspectRatio,
                100.0 / aspectRatio, 1.0, -1.0)

    else:

        glOrtho(-100.0 * aspectRatio, 100.0 *
                aspectRatio, -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(800, 600)
glutCreateWindow("GLRect")
glutDisplayFunc(RenderScene)
glutReshapeFunc(ChangeSize)
SetupRC()
glutMainLoop()
