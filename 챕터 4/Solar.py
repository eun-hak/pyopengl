from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


whiteLight = [0.2, 0.2, 0.2, 1.0]
sourceLight = [0.8, 0.8, 0.8, 1.0]
lightPos = [0.0, 0.0, 0.0, 1.0]

fMoonRot = 0.0
fEarthRot = 0.0


def RenderScene():
    global fMoonRot
    global fEarthRot

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    glTranslatef(0.0, 0.0, -300.0)

    glDisable(GL_LIGHTING)
    glColor3ub(255, 255, 0)
    glutSolidSphere(15.0, 30, 17)
    glEnable(GL_LIGHTING)

    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    glRotatef(fEarthRot, 0.0, 1.0, 0.0)

    glColor3ub(0, 0, 255)
    glTranslatef(105.0, 0.0, 0.0)
    glutSolidSphere(15.0, 30, 17)

    glColor3ub(200, 200, 200)
    glRotatef(fMoonRot, 0.0, 1.0, 0.0)
    glTranslatef(30.0, 0.0, 0.0)
    fMoonRot += 15.0
    if(fMoonRot > 360.0):
        fMoonRot = 0.0

    glutSolidSphere(6.0, 30, 17)

    glPopMatrix()

    fEarthRot += 5.0
    if(fEarthRot > 360.0):
        fEarthRot = 0.0

    glutSwapBuffers()


def SetupRC():

    glEnable(GL_DEPTH_TEST)
    glFrontFace(GL_CCW)
    glEnable(GL_CULL_FACE)

    glEnable(GL_LIGHTING)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, whiteLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, sourceLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glClearColor(0.0, 0.0, 0.0, 1.0)


def TimerFunc(value):

    glutPostRedisplay()
    glutTimerFunc(100, TimerFunc, 1)


def ChangeSize(w, h):
    global fAspect

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    fAspect = w/h

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, fAspect, 1.0, 425.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Earth/Moon/Sun System")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
glutTimerFunc(250, TimerFunc, 1)
SetupRC()
glutMainLoop()
