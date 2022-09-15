from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
from OpenGLCommon import *
import numpy
NUM_SPHERES = 30
fLightPos = GLTVector4()
spheres = [GLTFrame()]*NUM_SPHERES
frameCamera = GLTFrame()

fLightPos.value = [-100.0, 100.0, 50.0, 1.0]
fNoLight = [0.0, 0.0, 0.0, 0.0]
fLowLight = [0.25, 0.25, 0.25, 1.0]
fBrightLight = [1.0, 1.0, 1.0, 1.0]
mShadowMatrix = GLTMatrix()

vPoints = [GLTVector3(), GLTVector3(), GLTVector3()]
yRot = 0.0


def SetupRC():
    global vPoints
    global fLightPos
    global mShadowMatrix
    vPoints[0].value = [0.0, -0.4, 0.0]
    vPoints[1].value = [10.0, -0.4, 0.0]
    vPoints[2].value = [5.0, -0.4, -5.0]

    global iSphere

    glEnable(GL_MULTISAMPLE)

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

    gltMakeShadowMatrix(vPoints, fLightPos, mShadowMatrix)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMateriali(GL_FRONT, GL_SHININESS, 128)

    gltInitFrame(frameCamera)

    for iSphere in range(0, NUM_SPHERES, 1):

        gltInitFrame(spheres[iSphere])

        spheres[iSphere].vLocation.value[0] = (float)(
            (random.randrange(0, 32767) % 400) - 200) * 0.1
        spheres[iSphere].vLocation.value[1] = 0.0
        spheres[iSphere].vLocation.value[2] = (float)(
            (random.randrange(0, 32767) % 400) - 200) * 0.1


def DrawGround(void):

    global fExtent
    global fStep
    global y
    fExtent = 20.0
    fStep = 1.0
    y = -0.4
    global iStrip, iRun

    for iStrip in numpy.arange(-fExtent, fExtent, fStep):
        glBegin(GL_TRIANGLE_STRIP)
        glNormal3f(0.0, 1.0, 0.0)

        for iRun in numpy.arange(fExtent, -fExtent, -fStep):

            glVertex3f(iStrip, y, iRun)
            glVertex3f(iStrip + fStep, y, iRun)

        glEnd()


def DrawInhabitants(nShadow):
    global yRot

    global i

    if(nShadow == 0):
        yRot += 0.5
    else:
        glColor3f(0.0, 0.0, 0.0)

    if(nShadow == 0):
        glColor3f(0.0, 1.0, 0.0)

    for i in range(0, NUM_SPHERES, 1):

        glPushMatrix()
        gltApplyActorTransform(spheres[i])
        glutSolidSphere(0.3, 17, 9)
        glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 0.1, -2.5)

    if(nShadow == 0):
        glColor3f(0.0, 0.0, 1.0)

    glPushMatrix()
    glRotatef(-yRot * 2.0, 0.0, 1.0, 0.0)
    glTranslatef(1.0, 0.0, 0.0)
    glutSolidSphere(0.1, 17, 9)
    glPopMatrix()

    if(nShadow == 0):

        glColor3f(1.0, 0.0, 0.0)
        glMaterialfv(GL_FRONT, GL_SPECULAR, fBrightLight)

    glRotatef(yRot, 0.0, 1.0, 0.0)
    gltDrawTorus(0.35, 0.15, 61, 37)
    glMaterialfv(GL_FRONT, GL_SPECULAR, fNoLight)
    glPopMatrix()


def RenderScene():
    global fLightpos
    global mShadowMatrix
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    gltApplyCameraTransform(frameCamera)

    glLightfv(GL_LIGHT0, GL_POSITION, fLightPos.value)

    glColor3f(0.60, .40, .10)
    DrawGround(void)

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glPushMatrix()
    glMultMatrixf(mShadowMatrix.value)
    DrawInhabitants(1)
    glPopMatrix()
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)

    DrawInhabitants(0)

    glPopMatrix()

    glutSwapBuffers()


def SpecialKeys(key,  x,  y):

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


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(800, 600)
glutCreateWindow("OpenGL SphereWorld Demo + Lights and Shadow")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
glutSpecialFunc(SpecialKeys)
SetupRC()
glutTimerFunc(33, TimerFunction, 1)
glutMainLoop()
