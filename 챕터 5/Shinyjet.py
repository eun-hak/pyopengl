from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *

xRot = 0.0
yRot = 0.0

vNormal = GLTVector3()

vPoints = [GLTVector3(),
           GLTVector3(),
           GLTVector3()]


def RenderScene():
    global vNormal
    global vPoints

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    glColor3ub(128, 128, 128)
    glBegin(GL_TRIANGLES)
    glNormal3f(0.0, -1.0, 0.0)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, 0.0, 60.0)
    glVertex3f(-15.0, 0.0, 30.0)
    glVertex3f(15.0, 0.0, 30.0)

    vPoints[0].value = [15.0, 0.0,  30.0]
    vPoints[1].value = [0.0,  15.0, 30.0]
    vPoints[2].value = [0.0,  0.0,  60.0]

    gltGetNormalVector(
        vPoints[0], vPoints[1], vPoints[2], vNormal)

    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [0.0, 0.0,  60.0]
    vPoints[1].value = [0.0,  15.0, 30.0]
    vPoints[2].value = [-15.0,  0.0,  30.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)

    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [-15.0, 0.0,  30.0]
    vPoints[1].value = [0.0,  15.0, 30.0]
    vPoints[2].value = [0.0,  0.0,  -56.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [0.0, 0.0,  -56.0]
    vPoints[1].value = [0.0,  15.0, 30.0]
    vPoints[2].value = [15.0,  0.0,  30.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(15.0, 0.0, 30.0)
    glVertex3f(-15.0, 0.0, 30.0)
    glVertex3f(0.0, 0.0, -56.0)

    vPoints[0].value = [0.0, 2.0,  27.0]
    vPoints[1].value = [-60.0,  2.0, -8.0]
    vPoints[2].value = [60.0,  2.0,  -8.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [60.0, 2.0,  -8.0]
    vPoints[1].value = [0.0,  7.0, -8.0]
    vPoints[2].value = [0.0,  2.0,  27.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [60.0, 2.0,  -8.0]
    vPoints[1].value = [-60.0,  2.0, -8.0]
    vPoints[2].value = [0.0,  7.0,  -8.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [60.0, 2.0,  -8.0]
    vPoints[1].value = [-60.0,  2.0, -8.0]
    vPoints[2].value = [0.0,  7.0,  -8.0]
    #vPoints[0].value = [0.0, 2.0, 27.0]
    #vPoints[1].value = [0.0,  7.0, -8.0]
    #vPoints[2].value = [60.0,  2.0,  -8.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-30.0, -0.50, -57.0)
    glVertex3f(30.0, -0.50, -57.0)
    glVertex3f(0.0, -0.50, -40.0)

    vPoints[0].value = [0.0, -0.5, 40.0]
    vPoints[1].value = [30.0,  -0.5, -57.0]
    vPoints[2].value = [0.0,  4.0,  -57.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [0.0, 4.0, 57.0]
    vPoints[1].value = [-30.0,  -0.5, -57.0]
    vPoints[2].value = [0.0,  -0.5,  -40.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [30.0, -0.5, -57.0]
    vPoints[1].value = [-30.0,  -0.5, -57.0]
    vPoints[2].value = [0.0,  4.0,  -57.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [0.0, 0.5, -40.0]
    vPoints[1].value = [3.0,  0.5, -57.0]
    vPoints[2].value = [0.0,  25.0,  -65.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [0.0, 25.0, -65.0]
    vPoints[1].value = [-3.0,  0.5, -57.0]
    vPoints[2].value = [0.0,  0.5,  -40.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    vPoints[0].value = [3.0, 0.5, -57.0]
    vPoints[1].value = [-3.0,  0.5, -57.0]
    vPoints[2].value = [0.0,  25.0,  -65.0]

    gltGetNormalVector(vPoints[0], vPoints[1], vPoints[2], vNormal)
    glNormal3fv(vNormal.value)
    glVertex3fv(vPoints[0].value)
    glVertex3fv(vPoints[1].value)
    glVertex3fv(vPoints[2].value)

    glEnd()

    glPopMatrix()

    glutSwapBuffers()


def SetupRC():
    global ambientLight
    global diffuseLight
    global specular
    global specref

    ambientLight = [0.3, 0.3, 0.3, 1.0]
    diffuseLight = [0.7, 0.7, 0.7, 1.0]

    specular = [1.0, 1.0, 1.0, 1.0]
    specref = [1.0, 1.0, 1.0, 1.0]

    glEnable(GL_DEPTH_TEST)
    glFrontFace(GL_CCW)
    glEnable(GL_CULL_FACE)

    glEnable(GL_LIGHTING)

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
    glMateriali(GL_FRONT, GL_SHININESS, 128)

    glClearColor(0.0, 0.0, 1.0, 1.0)


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
    global fAspect
    global lightPos
    lightPos = [-50.0, 50.0, 100.0, 1.0]

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    fAspect = w / h
    gluPerspective(45.0, fAspect, 1.0, 225.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glTranslatef(0.0, 0.0, -150.0)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Shiny Jet")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
