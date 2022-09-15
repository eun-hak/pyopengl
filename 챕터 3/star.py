from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

xRot = 0.0
yRot = 0.0
GL_PI = 3.1415
MODE_SOLID = 0
MODE_LINE = 1
MODE_POINT = 2
bEdgeFlag = True
iMode = MODE_SOLID


def ProcessMenu(value):
    global MODE_SOLID
    global MODE_LINE
    global MODE_POINT
    global bEdgeFlag
    while(True):
        if iMode == MODE_SOLID:
            break
        elif iMode == MODE_LINE:
            break
        elif iMode == MODE_POINT:
            break
        elif bEdgeFlag == True:
            break
        elif bEdgeFlag == False:
            break

    glutPostRedisplay()


def RenderScene():
    global MODE_SOLID
    global MODE_LINE
    global MODE_POINT
    global bEdgeFlag

    glClear(GL_COLOR_BUFFER_BIT)

    if(iMode == MODE_LINE):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    if(iMode == MODE_POINT):
        glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)

    if(iMode == MODE_SOLID):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glPushMatrix()
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    glBegin(GL_TRIANGLES)

    glEdgeFlag(bEdgeFlag)
    glVertex2f(-20.0, 0.0)
    glEdgeFlag(True)
    glVertex2f(20.0, 0.0)
    glVertex2f(0.0, 40.0)

    glVertex2f(-20.0, 0.0)
    glVertex2f(-60.0, -20.0)
    glEdgeFlag(bEdgeFlag)
    glVertex2f(-20.0, -40.0)
    glEdgeFlag(True)

    glVertex2f(-20.0, -40.0)
    glVertex2f(0.0, -80.0)
    glEdgeFlag(bEdgeFlag)
    glVertex2f(20.0, -40.0)
    glEdgeFlag(True)

    glVertex2f(20.0, -40.0)
    glVertex2f(60.0, -20.0)
    glEdgeFlag(bEdgeFlag)
    glVertex2f(20.0, 0.0)
    glEdgeFlag(True)

    glEdgeFlag(bEdgeFlag)
    glVertex2f(-20.0, 0.0)
    glVertex2f(-20.0, -40.0)
    glVertex2f(20.0, 0.0)

    glVertex2f(-20.0, -40.0)
    glVertex2f(20.0, -40.0)
    glVertex2f(20.0, 0.0)
    glEdgeFlag(True)

    glEnd()

    glPopMatrix()

    glutSwapBuffers()


def SetupRC():

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glColor3f(0.0, 1.0, 0.0)


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


global nModeMenu
global nEdgeMenu
global nMainMenu

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutCreateWindow("Solid and Outlined Star")

nModeMenu = glutCreateMenu(ProcessMenu)
glutAddMenuEntry("Solid", 1)
glutAddMenuEntry("Outline", 2)
glutAddMenuEntry("Points", 3)

nEdgeMenu = glutCreateMenu(ProcessMenu)
glutAddMenuEntry("On", 4)
glutAddMenuEntry("Off", 5)

nMainMenu = glutCreateMenu(ProcessMenu)
glutAddSubMenu("Mode", nModeMenu)
glutAddSubMenu("Edges", nEdgeMenu)
glutAttachMenu(GLUT_RIGHT_BUTTON)

glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
