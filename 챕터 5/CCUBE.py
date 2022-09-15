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

    glBegin(GL_QUADS)

    glColor3ub(255, 255, 255)

    glVertex3f(50.0, 50.0, 50.0)

    glColor3ub(255, 255, 0)
    glVertex3f(50.0, -50.0, 50.0)

    glColor3ub(255, 0, 0)
    glVertex3f(-50.0, -50.0, 50.0)

    glColor3ub(255, 0, 255)
    glVertex3f(-50.0, 50.0, 50.0)

    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(50.0, 50.0, -50.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(50.0, -50.0, -50.0)

    glColor3f(0.0, 0.0, 0.0)
    glVertex3f(-50.0, -50.0, -50.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-50.0, 50.0, -50.0)

    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(50.0, 50.0, -50.0)

    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(50.0, 50.0, 50.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(-50.0, 50.0, 50.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-50.0, 50.0, -50.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(50.0, -50.0, -50.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(50.0, -50.0, 50.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-50.0, -50.0, 50.0)

    glColor3f(0.0, 0.0, 0.0)
    glVertex3f(-50.0, -50.0, -50.0)

    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(50.0, 50.0, 50.0)

    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(50.0, 50.0, -50.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(50.0, -50.0, -50.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(50.0, -50.0, 50.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(-50.0, 50.0, 50.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-50.0, 50.0, -50.0)

    glColor3f(0.0, 0.0, 0.0)
    glVertex3f(-50.0, -50.0, -50.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-50.0, -50.0, 50.0)
    glEnd()

    glPopMatrix()

    glutSwapBuffers()


def SetupRC():

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_DITHER)
    glShadeModel(GL_SMOOTH)


def SpecialKeys(key, x, y):
    
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
    global fAspect

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    fAspect = w / h
    gluPerspective(35.0, fAspect, 1.0, 1000.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -400.0)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("RGB Cube")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
