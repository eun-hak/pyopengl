from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGLCommon import *
import numpy
NUM_SPHERES = 30
fLightPos = [-100.0, 100.0, 50.0, 1.0]
fNoLight = [0.0, 0.0, 0.0, 0.0]
fLowLight = [0.25, 0.25, 0.25, 1.0]
fBrightLight = [1.0, 1.0, 1.0, 1.0]
fLightPosMirror = [-100.0, -100.0, 50.0, 1.0]


yRot = 0.0


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
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMateriali(GL_FRONT, GL_SHININESS, 128)


def DrawGround(void):

    global fExtent
    global fStep
    global y
    global iBounce
    fExtent = 20.0
    fStep = 0.5
    y = 0.0
    global fColor
    global iStrip, iRun
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


def DrawWorld(void):
    global yRot
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0.0, 0.5, -3.5)

    glPushMatrix()
    glRotatef(-yRot * 2.0, 0.0, 1.0, 0.0)
    glTranslatef(1.0, 0.0, 0.0)
    glutSolidSphere(0.1, 17, 9)
    glPopMatrix()

    glRotatef(yRot, 0.0, 1.0, 0.0)
    gltDrawTorus(0.35, 0.15, 61, 37)

    glPopMatrix()


def RenderScene():
    global fLightPosMirror
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glLightfv(GL_LIGHT0, GL_POSITION, fLightPosMirror)
    glPushMatrix()
    glFrontFace(GL_CW)
    glScalef(1.0, -1.0, 1.0)
    DrawWorld(void)
    glFrontFace(GL_CCW)
    glPopMatrix()

    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    DrawGround(void)
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

    glLightfv(GL_LIGHT0, GL_POSITION, fLightPos)
    DrawWorld(void)
    glPopMatrix()

    glutSwapBuffers()


def TimerFunction(value):
    global yRot
    yRot += 1.0

    glutPostRedisplay()

    glutTimerFunc(1, TimerFunction, 1)


def ChangeSize(w,  h):

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
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("OpenGL Blending and Transparency")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
glutTimerFunc(10, TimerFunction, 1)
SetupRC()
glutMainLoop()
