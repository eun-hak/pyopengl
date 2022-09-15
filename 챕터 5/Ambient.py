from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


xRot = 0.0
yRot = 0.0


def RenderScene():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    glColor3ub(0, 255, 0)
    glBegin(GL_TRIANGLES)
    glVertex3f(0.0, 0.0, 60.0)
    glVertex3f(-15.0, 0.0, 30.0)
    glVertex3f(15.0, 0.0, 30.0)

    glVertex3f(15.0, 0.0, 30.0)
    glVertex3f(0.0, 15.0, 30.0)
    glVertex3f(0.0, 0.0, 60.0)

    glVertex3f(0.0, 0.0, 60.0)
    glVertex3f(0.0, 15.0, 30.0)
    glVertex3f(-15.0, 0.0, 30.0)

    glColor3ub(192, 192, 192)
    glVertex3f(-15.0, 0.0, 30.0)
    glVertex3f(0.0, 15.0, 30.0)
    glVertex3f(0.0, 0.0, -56.0)

    glVertex3f(0.0, 0.0, -56.0)
    glVertex3f(0.0, 15.0, 30.0)
    glVertex3f(15.0, 0.0, 30.0)

    glVertex3f(15.0, 0.0, 30.0)
    glVertex3f(-15.0, 0.0, 30.0)
    glVertex3f(0.0, 0.0, -56.0)

    glColor3ub(64, 64, 64)
    glVertex3f(0.0, 2.0, 27.0)
    glVertex3f(-60.0, 2.0, -8.0)
    glVertex3f(60.0, 2.0, -8.0)

    glVertex3f(60.0, 2.0, -8.0)
    glVertex3f(0.0, 7.0, -8.0)
    glVertex3f(0.0, 2.0, 27.0)

    glVertex3f(60.0, 2.0, -8.0)
    glVertex3f(-60.0, 2.0, -8.0)
    glVertex3f(0.0, 7.0, -8.0)

    glVertex3f(0.0, 2.0, 27.0)
    glVertex3f(0.0, 7.0, -8.0)
    glVertex3f(-60.0, 2.0, -8.0)

    glColor3ub(255, 255, 0)
    glVertex3f(-30.0, -0.50, -57.0)
    glVertex3f(30.0, -0.50, -57.0)
    glVertex3f(0.0, -0.50, -40.0)

    glVertex3f(0.0, -0.5, -40.0)
    glVertex3f(30.0, -0.5, -57.0)
    glVertex3f(0.0, 4.0, -57.0)

    glVertex3f(0.0, 4.0, -57.0)
    glVertex3f(-30.0, -0.5, -57.0)
    glVertex3f(0.0, -0.5, -40.0)

    glVertex3f(30.0, -0.5, -57.0)
    glVertex3f(-30.0, -0.5, -57.0)
    glVertex3f(0.0, 4.0, -57.0)

    glColor3ub(255, 0, 0)
    glVertex3f(0.0, 0.5, -40.0)
    glVertex3f(3.0, 0.5, -57.0)
    glVertex3f(0.0, 25.0, -65.0)

    glVertex3f(0.0, 25.0, -65.0)
    glVertex3f(-3.0, 0.5, -57.0)
    glVertex3f(0.0, 0.5, -40.0)

    glVertex3f(3.0, 0.5, -57.0)
    glVertex3f(-3.0, 0.5, -57.0)
    glVertex3f(0.0, 25.0, -65.0)
    glEnd()

    glPopMatrix()

    glutSwapBuffers()


def SetupRC():
    global ambientLight

    ambientLight = [1.0, 1.0, 1.0, 1.0]

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glFrontFace(GL_CCW)

    glEnable(GL_LIGHTING)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientLight)

    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glClearColor(0.0, 0.0, 0.5, 1.0)


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
    nRange = 80.0

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if(w <= h):
        glOrtho(-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
    else:
        glOrtho(-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Ambient Light Jet")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
