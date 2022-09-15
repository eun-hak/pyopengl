from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *
import random
import numpy
NUM_SPHERES = 50
frameCamera = GLTFrame()
spheres = [GLTFrame()]*NUM_SPHERES

fExtent = 20.0
fStep = 1.0
y = -0.4
yRot = 0.0
# define NUM_SPHERES      50
# GLTFrame    spheres[NUM_SPHERES];
# GLTFrame  frameCamera


def SetupRC():
    global iSphere
    global spheres
    global frameCamera

    glClearColor(0.0, 0.0, 0.50, 1.0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    gltInitFrame(frameCamera)

    for iSphere in range(0, NUM_SPHERES, 1):

        gltInitFrame(spheres[iSphere])
        spheres[iSphere].vLocation.value[0] = float((
            (random.randrange(0, 32767) % 400) - 200) * 0.1)
        spheres[iSphere].vLocation.value[1] = 0.0
        spheres[iSphere].vLocation.value[2] = float((
            (random.randrange(0, 32767) % 400) - 200) * 0.1)


def DrawGround():
    global iLine
    global fExtent
    global fStep
    global y

    glBegin(GL_LINES)

    for iLine in numpy.arange(-fExtent, fExtent, fStep):

        glVertex3f(iLine, y, fExtent)
        glVertex3f(iLine, y, -fExtent)
        glVertex3f(fExtent, y, iLine)
        glVertex3f(-fExtent, y, iLine)
    glEnd()


def RenderScene():
    global i
    global yRot
    yRot += 0.5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    gltApplyCameraTransform(frameCamera)

    DrawGround()

    for i in range(0, NUM_SPHERES, 1):
        glPushMatrix()
        gltApplyActorTransform(spheres[i])
        glutSolidSphere(0.1, 13, 26)
        glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 0.0, -2.5)

    glPushMatrix()
    glRotatef(-yRot * 2.0, 0.0, 1.0, 0.0)
    glTranslatef(1.0, 0.0, 0.0)
    glutSolidSphere(0.1, 13, 26)
    glPopMatrix()

    glRotatef(yRot, 0.0, 1.0, 0.0)
    gltDrawTorus(0.35, 0.15, 40, 20)
    glPopMatrix()
    glPopMatrix()

    glutSwapBuffers()


def SpecialKeys(key, x, y):

    if(key == GLUT_KEY_UP):
        gltMoveFrameForward(frameCamera, 0.1)

    if(key == GLUT_KEY_DOWN):
        gltMoveFrameForward(frameCamera, -0.1)

    if(key == GLUT_KEY_LEFT):
        gltRotateFrameLocalY(frameCamera, 0.1)

    if(key == GLUT_KEY_RIGHT):
        gltRotateFrameLocalY(frameCamera, -0.1)

    glutPostRedisplay()


def TimerFunction(value):

    glutPostRedisplay()
    glutTimerFunc(3, TimerFunction, 1)


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
glutCreateWindow("OpenGL SphereWorld Demo")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
glutSpecialFunc(SpecialKeys)
SetupRC()
glutTimerFunc(33, TimerFunction, 1)
glutMainLoop()
