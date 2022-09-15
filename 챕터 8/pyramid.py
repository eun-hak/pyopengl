from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *
from TGACommon import *

pImage = None
iWidth = [0]
iHeight = [0]
eFormat = [0]
iComponents = [0]
xRot = 0.0
yRot = 0.0


def ChangeSize(w, h):
    global fAspect

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    fAspect = w/h

    # // Reset coordinate system
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # // Produce the perspective projection
    gluPerspective(35.0, fAspect, 1.0, 40.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def SetupRC():

    #GLubyte * pBytes
    global pBytes
    global xRot, yRot
    global iWidth, iHeight, iComponents, eFormat

    whiteLight = [0.05, 0.05, 0.05, 1.0]
    sourceLight = [0.25, 0.25, 0.25, 1.0]
    lightPos = [-10.0, 5.0, 5.0, 1.0]

    glEnable(GL_DEPTH_TEST)  # // Hidden surface removal
    glFrontFace(GL_CCW)  # // Counter clock-wise polygons face out
    glEnable(GL_CULL_FACE)  # // Do not calculate inside of jet

    glEnable(GL_LIGHTING)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, whiteLight)
    glLightfv(GL_LIGHT0, GL_AMBIENT, sourceLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, sourceLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    pBytes = LoadTGA("C:/temp/Stone.tga", iWidth,
                     iHeight, iComponents, eFormat)
    glTexImage2D(GL_TEXTURE_2D, 0, iComponents[0], iWidth[0],
                 iHeight[0], 0, eFormat[0], GL_UNSIGNED_BYTE, pBytes)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glEnable(GL_TEXTURE_2D)


def SpecialKeys(key,  x,  y):
    global xRot, yRot

    if(key == GLUT_KEY_UP):
        xRot -= 5.0

    if(key == GLUT_KEY_DOWN):
        xRot += 5.0

    if(key == GLUT_KEY_LEFT):
        yRot -= 5.0

    if(key == GLUT_KEY_RIGHT):
        yRot += 5.0

    xRot = xRot % 360
    yRot = yRot % 360

    # // Refresh the Window
    glutPostRedisplay()


# // Called to draw scene
def RenderScene():

    # GLTVector3 vNormal;
    # GLTVector3 vCorners[5] = { { 0.0, .80, 0.0 },     // Top           0
    #                           { -0.5, 0.0, -.50 },    // Back left     1
    #                           { 0.5, 0.0, -0.50 },    // Back right    2
    #                           { 0.5, 0.0, 0.5 },      // Front right   3
    #                           { -0.5, 0.0, 0.5 }};    // Front left    4
    vNormal = GLTVector3()
    vCorners = [GLTVector3(), GLTVector3(), GLTVector3(),
                GLTVector3(), GLTVector3()]
    vCorners[0].value = [0.0, .80, 0.0]
    vCorners[1].value = [-0.5, 0.0, -.50]
    vCorners[2].value = [0.5, 0.0, -0.50]
    vCorners[3].value = [0.5, 0.0, 0.5]
    vCorners[4].value = [-0.5, 0.0, 0.5]
   # // Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # // Save the matrix state and do the rotations
    glPushMatrix()
    # // Move object back and do in place rotation
    glTranslatef(0.0, -0.25, -4.0)
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    # // Draw the Pyramid
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_TRIANGLES)
    # // Bottom section - two triangles
    glNormal3f(0.0, -1.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3fv(vCorners[2].value)

    glTexCoord2f(0.0, 0.0)
    glVertex3fv(vCorners[4].value)

    glTexCoord2f(0.0, 1.0)
    glVertex3fv(vCorners[1].value)

    glTexCoord2f(1.0, 1.0)
    glVertex3fv(vCorners[2].value)

    glTexCoord2f(1.0, 0.0)
    glVertex3fv(vCorners[3].value)

    glTexCoord2f(0.0, 0.0)
    glVertex3fv(vCorners[4].value)

    # // Front Face
    gltGetNormalVector(
        vCorners[0], vCorners[4], vCorners[3], vNormal)
    glNormal3fv(vNormal.value)
    glTexCoord2f(0.5, 1.0)
    glVertex3fv(vCorners[0].value)
    glTexCoord2f(0.0, 0.0)
    glVertex3fv(vCorners[4].value)
    glTexCoord2f(1.0, 0.0)
    glVertex3fv(vCorners[3].value)

    # // Left Face
    gltGetNormalVector(vCorners[0],
                       vCorners[1], vCorners[4], vNormal)
    glNormal3fv(vNormal.value)
    glTexCoord2f(0.5, 1.0)
    glVertex3fv(vCorners[0].value)
    glTexCoord2f(0.0, 0.0)
    glVertex3fv(vCorners[1].value)
    glTexCoord2f(1.0, 0.0)
    glVertex3fv(vCorners[4].value)

    # // Back Face
    gltGetNormalVector(vCorners[0],
                       vCorners[2], vCorners[1], vNormal)
    glNormal3fv(vNormal.value)
    glTexCoord2f(0.5, 1.0)
    glVertex3fv(vCorners[0].value)

    glTexCoord2f(0.0, 0.0)
    glVertex3fv(vCorners[2].value)

    glTexCoord2f(1.0, 0.0)
    glVertex3fv(vCorners[1].value)

    # // Right Face
    gltGetNormalVector(vCorners[0],
                       vCorners[3], vCorners[2], vNormal)
    glNormal3fv(vNormal.value)
    glTexCoord2f(0.5, 1.0)
    glVertex3fv(vCorners[0].value)
    glTexCoord2f(0.0, 0.0)
    glVertex3fv(vCorners[3].value)
    glTexCoord2f(1.0, 0.0)
    glVertex3fv(vCorners[2].value)
    glEnd()

    # // Restore the matrix state
    glPopMatrix()

    # // Buffer swap
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Textured Pyramid")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
