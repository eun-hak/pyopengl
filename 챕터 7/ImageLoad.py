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


def SetupRC():

    glClearColor(0.0, 0.0, 0.0, 0.0)


def RenderScene():

    # GLubyte *pImage = NULL;
    # GLint iWidth, iHeight, iComponents;
    # GLenum eFormat;
    global pImage
    global iWidth, iHeight, iComponents
    global eFormat

    glClear(GL_COLOR_BUFFER_BIT)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    pImage = LoadTGA("C:/temp/Fire.tga", iWidth, iHeight, iComponents, eFormat)

    glRasterPos2i(0, 0)

    if(pImage != None):
        glDrawPixels(iWidth[0], iHeight[0], eFormat[0],
                     GL_UNSIGNED_BYTE, pImage)

    glutSwapBuffers()


def ChangeSize(w,  h):

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(0.0, w, 0.0, h)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_RGB | GL_DOUBLE)
glutInitWindowSize(512, 512)
glutCreateWindow("OpenGL Image Loading")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)

SetupRC()
glutMainLoop()
