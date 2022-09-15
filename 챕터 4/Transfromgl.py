from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *

GLT_PI = 3.14159
yRot = 0.0


def RenderScene():
    global yRot
    global rotationMatrix, translationMatrix, transformationMatrix
    transformationMatrix = GLTMatrix()
    translationMatrix = GLTMatrix()
    rotationMatrix = GLTMatrix()

    yRot += 0.5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    gltRotationMatrix(gltDegToRad(yRot), 0.0, 1.0, 0.0, transformationMatrix)
    transformationMatrix.value[12] = 0.0
    transformationMatrix.value[13] = 0.0
    transformationMatrix.value[14] = -2.5

    glLoadMatrixf(transformationMatrix.value)

    gltDrawTorus(0.35, 0.15, 40, 20)

    glutSwapBuffers()


def SetupRC():

    glClearColor(0.0, 0.0, 0.50, 1.0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


def TimerFunction(value):

    glutPostRedisplay()
    glutTimerFunc(33, TimerFunction, 1)


def ChangeSize(w, h):

    global fAspect

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    fAspect = w / h

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(35.0, fAspect, 1.0, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("OpenGL Transformations Demo")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
SetupRC()
glutTimerFunc(33, TimerFunction, 1)
glutMainLoop()
