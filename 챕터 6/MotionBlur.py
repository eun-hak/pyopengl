from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *
import random
import numpy
mShadowMatrix = GLTMatrix()
fLightpos = GLTVector4()
fLightPos = [-100.0, 100.0, 50.0, 1.0]
fNoLight = [0.0, 0.0, 0.0, 0.0]
fLowLight = [0.25, 0.25, 0.25, 1.0]
fBrightLight = [1.0, 1.0, 1.0, 1.0]
fLightPosMirror = [-100, -100, 50, 1]


yRot = 45.0


def SetupRC():

    glClearColor(fLowLight[0], fLowLight[1], fLowLight[2], fLowLight[3])

    glCullFace(GL_BACK)
    glFrontFace(GL_CCW)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, fNoLight)
    glLightfv(GL_LIGHT0, GL_AMBIENT, fLowLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, fBrightLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, fBrightLight)
    glLightfv(GL_LIGHT0, GL_POSITION, fLightPos)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMateriali(GL_FRONT, GL_SHININESS, 128)


def DrawGround(void):
    global fExtent
    global fStep
    global y
    global fColor
    global iStrip, iRun
    global iBounce
    fExtent = 20.0
    fStep = 0.5
    y = 0.0
    iBounce = 0

    glShadeModel(GL_FLAT)

    for iStrip in numpy.arange(-fExtent, fExtent, fStep):

        glBegin(GL_TRIANGLE_STRIP)

        for iRun in numpy.arange(fExtent, -fExtent, -fStep):

            if((iBounce % 2) == 0):
                fColor = 1.0
            else:
                fColor = 0.0

            glColor4f(fColor, fColor, fColor, 0.5)
            glVertex3f(iStrip, y, iRun)
            glVertex3f(iStrip + fStep, y, iRun)

            iBounce += 1

        glEnd()

    glShadeModel(GL_SMOOTH)


def DrawGeometry(void):

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    DrawGround(void)

    glColor3f(1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.5, -3.5)
    glRotatef(-(yRot * 2.0), 0.0, 1.0, 0.0)
    glTranslatef(1.0, 0.0, 0.0)
    glutSolidSphere(0.1, 17, 9)
    glPopMatrix()


def RenderScene():
    global yRot
    global fPass
    global fPasses
    fPasses = 10.0
    yRot = 35.0

    for fPass in numpy.arange(0, fPasses, 1):

        yRot += .75

        DrawGeometry(void)

        if(fPass == 0.0):
            glAccum(GL_LOAD, 0.5)
        else:
            glAccum(GL_ACCUM, 0.5 * (1.0 / fPasses))

    glAccum(GL_RETURN, 1.0)
    glutSwapBuffers()


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

    glTranslatef(0.0, -0.4, 0.0)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_ACCUM)
glutInitWindowSize(800, 600)
glutCreateWindow("Motion Blur with the Accumulation Buffer")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)

SetupRC()
glutMainLoop()
