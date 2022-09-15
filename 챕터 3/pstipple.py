from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


xRot = 0.0
yRot = 0.0
GL_PI = 3.1415



fire = [0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0xc0,
        0x00, 0x00, 0x01, 0xf0,
        0x00, 0x00, 0x07, 0xf0,
        0x0f, 0x00, 0x1f, 0xe0,
        0x1f, 0x80, 0x1f, 0xc0,
        0x0f, 0xc0, 0x3f, 0x80,
        0x07, 0xe0, 0x7e, 0x00,
        0x03, 0xf0, 0xff, 0x80,
        0x03, 0xf5, 0xff, 0xe0,
        0x07, 0xfd, 0xff, 0xf8,
        0x1f, 0xfc, 0xff, 0xe8,
        0xff, 0xe3, 0xbf, 0x70,
        0xde, 0x80, 0xb7, 0x00,
        0x71, 0x10, 0x4a, 0x80,
        0x03, 0x10, 0x4e, 0x40,
        0x02, 0x88, 0x8c, 0x20,
        0x05, 0x05, 0x04, 0x40,
        0x02, 0x82, 0x14, 0x40,
        0x02, 0x40, 0x10, 0x80,
        0x02, 0x64, 0x1a, 0x80,
        0x00, 0x92, 0x29, 0x00,
        0x00, 0xb0, 0x48, 0x00,
        0x00, 0xc8, 0x90, 0x00,
        0x00, 0x85, 0x10, 0x00,
        0x00, 0x03, 0x00, 0x00,
        0x00, 0x00, 0x10, 0x00]


def RenderScene():

    glClear(GL_COLOR_BUFFER_BIT)

    glPushMatrix()
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    glBegin(GL_POLYGON)
    glVertex2f(-20.0, 50.0)
    glVertex2f(20.0, 50.0)
    glVertex2f(50.0, 20.0)
    glVertex2f(50.0, -20.0)
    glVertex2f(20.0, -50.0)
    glVertex2f(-20.0, -50.0)
    glVertex2f(-50.0, -20.0)
    glVertex2f(-50.0, 20.0)
    glEnd()

    glPopMatrix()

    glutSwapBuffers()


def SetupRC():

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glColor3f(1.0, 0.0, 0.0)
    glEnable(GL_POLYGON_STIPPLE)
    glPolygonStipple(fire)


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
        glOrtho(-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
    else:
        glOrtho(-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Polygon Stippling")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
