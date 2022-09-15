from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


xRot = 0.0
yRot = 0.0
GL_PI = 3.1415
fElect1 = 0.0


def RenderScene():
    global fElect1
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -100.0)

    glColor3ub(255, 0, 0)
    glutSolidSphere(10.0, 15, 15)

    glColor3ub(255, 255, 0)

    glPushMatrix()

    glRotatef(fElect1, 0.0, 1.0, 0.0)

    glTranslatef(90.0, 0.0, 0.0)

    glutSolidSphere(6.0, 15, 15)

    glPopMatrix()

    glPushMatrix()
    glRotatef(45.0, 0.0, 0.0, 1.0)
    glRotatef(fElect1, 0.0, 1.0, 0.0)
    glTranslatef(-70.0, 0.0, 0.0)
    glutSolidSphere(6.0, 15, 15)
    glPopMatrix()

    glPushMatrix()
    glRotatef(360.0 - 45.0, 0.0, 0.0, 1.0)
    glRotatef(fElect1, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 0.0, 60.0)
    glutSolidSphere(6.0, 15, 15)
    glPopMatrix()

    fElect1 += 10.0
    if (fElect1 > 360.0):
        fElect1 = 0.0

    glutSwapBuffers()


def SetupRC():

    glEnable(GL_DEPTH_TEST)

    glFrontFace(GL_CCW)

    glEnable(GL_CULL_FACE)

    glClearColor(0.0, 0.0, 0.0, 1.0)


def TimerFunc(value):

    glutPostRedisplay()
    glutTimerFunc(100, TimerFunc, 1)


def SpecialKeys(key, x, y):
    global xRot
    global yRot

    if(key == GLUT_KEY_UP):
        xRot -= 5.0

    if(key == GLUT_KEY_DOWN):
        xRot += 5.0

    if(key == GLUT_KEY_LEFT):
        yRot -= 5.0

    if(key == GLUT_KEY_RIGHT):
        yRot += 5.0

    if(key > 356.0):
        xRot = 0.0

    if(key < -1.0):
        xRot = 355.0

    if(key > 356.0):
        yRot = 0.0

    if(key < -1.0):
        yRot = 355.0

    glutPostRedisplay()


def ChangeSize(w, h):

    global nRange
    nRange = 100.0

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if(w <= h):
        glOrtho(-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange*2, nRange*2)
    else:
        glOrtho(-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange*2, nRange*2)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("OpenGL Atom")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
glutTimerFunc(500, TimerFunc, 1)
SetupRC()
glutMainLoop()
