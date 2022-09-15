from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *

xRot = 0.0
yRot = 0.0
lightPos = GLTVector4()

ambientLight = [0.3, 0.3, 0.3, 1.0]
diffuseLight = [0.7, 0.7, 0.7, 1.0]
specular = [1.0, 1.0, 1.0, 1.0]
lightPos.value = [-75, 150.0, -50.0, 0.0]


specref = [1.0, 1.0, 1.0, 1.0]


shadowMat = GLTMatrix()
vNormal = GLTVector3()

vPoints = [GLTVector3(),
           GLTVector3(),
           GLTVector3()]


def DrawJet(nShadow):
    global shadowMat
    global vNormal
    global vPoints
    if(nShadow == 0):
        glColor3ub(128, 128, 128)
    else:
        glColor3ub(0, 0, 0)

    glBegin(GL_TRIANGLES)
    glNormal3f(0.0, -1.0, 0.0)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, 0.0, 60.0)
    glVertex3f(-15.0, 0.0, 30.0)
    glVertex3f(15.0, 0.0, 30.0)

    vPoints[0].value = [15.0, 0.0,  30.0]
    vPoints[1].value = [0.0,  15.0, 30.0]
    vPoints[2].value = [0.0,  0.0,  60.0]

    gltGetNormalVector(vPoints[0], vPoints[1],
                       vPoints[2], vNormal)

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


def RenderScene():
    global shadowMat
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBegin(GL_QUADS)
    glColor3ub(0, 32, 0)
    glVertex3f(400.0, -150.0, -200.0)
    glVertex3f(-400.0, -150.0, -200.0)
    glColor3ub(0, 255, 0)
    glVertex3f(-400.0, -150.0, 200.0)
    glVertex3f(400.0, -150.0, 200.0)
    glEnd()

    glPushMatrix()

    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos.value)
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    DrawJet(0)

    glPopMatrix()

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glPushMatrix()

    glMultMatrixf(shadowMat.value)

    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    DrawJet(1)

    glPopMatrix()

    glPushMatrix()
    glTranslatef(lightPos.value[0], lightPos.value[1], lightPos.value[2])
    glColor3ub(255, 255, 0)
    glutSolidSphere(5.0, 10, 10)
    glPopMatrix()

    glEnable(GL_DEPTH_TEST)

    glutSwapBuffers()


def SetupRC():
    global points
    global shadowMat
    global lightPos
    #lightPos = GLTVector4()

    points = [GLTVector3(),
              GLTVector3(),
              GLTVector3()]
    points[0].value = [-30.0, -149.0, -20.0]
    points[1].value = [-30.0, -149.0, 20.0]
    points[2].value = [40.0, -149.0, 20.0]

    glEnable(GL_DEPTH_TEST)
    glFrontFace(GL_CCW)
    glEnable(GL_CULL_FACE)

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos.value)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
    glMateriali(GL_FRONT, GL_SHININESS, 128)

    glClearColor(0.0, 0.0, 1.0, 1.0)

    gltMakeShadowMatrix(points, lightPos, shadowMat)


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

    fAspect = w/h
    gluPerspective(60.0, fAspect, 200.0, 500.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -400.0)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos.value)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Shadow")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
