from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
xRot = 0.0
yRot = 0.0


lightPos = [0.0, 0.0, 75.0, 1.0]
specular = [1.0, 1.0, 1.0, 1.0]
specref = [1.0, 1.0, 1.0, 1.0]
ambientLight = [0.5, 0.5, 0.5, 1.0]
spotDir = [0.0, 0.0, -1.0]

MODE_FLAT = 1
MODE_SMOOTH = 2
MODE_VERYLOW = 3
MODE_MEDIUM = 4
MODE_VERYHIGH = 5

iShade = MODE_FLAT
iTess = MODE_VERYLOW


def ProcessMenu(value):

    while (True):

        if iShade == MODE_FLAT:
            break

        elif iShade == MODE_SMOOTH:
            break

        elif iTess == MODE_VERYLOW:
            break

        elif iTess == MODE_MEDIUM:
            break

        elif iTess == MODE_VERYHIGH:
            break

    glutPostRedisplay()


def RenderScene():

    if(iShade == MODE_FLAT):
        glShadeModel(GL_FLAT)
    else:
        glShadeModel(GL_SMOOTH)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(yRot, 0.0, 1.0, 0.0)
    glRotatef(xRot, 1.0, 0.0, 0.0)

    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spotDir)

    glColor3ub(255, 0, 0)

    glTranslatef(lightPos[0], lightPos[1], lightPos[2])
    glutSolidCone(4.0, 6.0, 15, 15)

    glPushAttrib(GL_LIGHTING_BIT)

    glDisable(GL_LIGHTING)
    glColor3ub(255, 255, 0)
    glutSolidSphere(3.0, 15, 15)

    glPopAttrib()

    glPopMatrix()

    glColor3ub(0, 0, 255)

    if(iTess == MODE_VERYLOW):
        glutSolidSphere(30.0, 7, 7)

    else:
        if(iTess == MODE_MEDIUM):
            glutSolidSphere(30.0, 15, 15)
        else:
            glutSolidSphere(30.0, 50, 50)

    glutSwapBuffers()


def SetupRC():

    glEnable(GL_DEPTH_TEST)
    glFrontFace(GL_CCW)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientLight)

    glLightfv(GL_LIGHT0, GL_DIFFUSE, ambientLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 50.0)

    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
    glMateriali(GL_FRONT, GL_SHININESS, 128)

    glClearColor(0.0, 0.0, 0.0, 1.0)


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


def ChangeSize(w,  h):

    global fAspect

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    fAspect = w / h
    gluPerspective(35.0, fAspect, 1.0, 500.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -250.0)

    global nMenu


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Spot Light")
nMenu = glutCreateMenu(ProcessMenu)
glutAddMenuEntry("Flat Shading", 1)
glutAddMenuEntry("Smooth Shading", 2)
glutAddMenuEntry("VL Tess", 3)
glutAddMenuEntry("MD Tess", 4)
glutAddMenuEntry("VH Tess", 5)
glutAttachMenu(GLUT_RIGHT_BUTTON)
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
