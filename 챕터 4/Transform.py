from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *
import math
GLT_PI = 3.14159
yRot = 0.0


def DrawTorus(mTransform):
    global majorRadius
    global minorRadius
    global objectVertex
    global transformedVertex
    global minorStep
    objectVertex = GLTVector3()
    transformedVertex = GLTVector3()

    majorRadius = 0.35
    minorRadius = 0.15
    numMajor = 40
    numMinor = 20
    # GLTVector3 objectVertex;         // Vertex in object/eye space
    # GLTVector3 transformedVertex;    // New Transformed vertex
    majorStep = 2.0*GLT_PI / numMajor
    minorStep = 2.0*GLT_PI / numMinor
    global i, j
    # int i, j;

    for i in range(0, numMajor, 1):
        a0 = i * majorStep
        a1 = a0 + majorStep
        x0 = math.cos(a0)
        y0 = math.sin(a0)
        x1 = math.cos(a1)
        y1 = math.sin(a1)

        glBegin(GL_TRIANGLE_STRIP)

        for j in range(0, numMinor, 1):

            b = j * minorStep
            c = math.cos(b)
            r = minorRadius * c + majorRadius
            z = minorRadius * math.sin(b)

            objectVertex.value[0] = x0*r
            objectVertex.value[1] = y0*r
            objectVertex.value[2] = z
            gltTransformPoint(objectVertex, mTransform, transformedVertex)
            glVertex3fv(transformedVertex.value)

            objectVertex.value[0] = x1*r
            objectVertex.value[1] = y1*r
            objectVertex.value[2] = z
            gltTransformPoint(objectVertex, mTransform, transformedVertex)
            glVertex3fv(transformedVertex.value)

        glEnd()


def RenderScene():
    global yRot
    global transformationMatrix
    transformationMatrix = GLTMatrix()

    yRot += 0.5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    gltRotationMatrix(gltDegToRad(yRot), 0.0, 1.0, 0.0, transformationMatrix)

    transformationMatrix.value[12] = 0.0
    transformationMatrix.value[13] = 0.0
    transformationMatrix.value[14] = -2.5

    DrawTorus(transformationMatrix)
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
glutCreateWindow("Manual Transformations Demo")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
SetupRC()
glutTimerFunc(33, TimerFunction, 1)
glutMainLoop()
