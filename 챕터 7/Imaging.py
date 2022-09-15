from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import histogram
from OpenGLCommon import *
from TGACommon import *

# static GLubyte *pImage = NULL;
# static GLint iWidth, iHeight, iComponents;
# static GLenum eFormat;
pImage = None
iWidth = [0]
iHeight = [0]
eFormat = [0]
iComponents = [0]
iViewport = [0]*4
iRenderMode = 1
bHistogram = GL_FALSE
# static GLint        iRenderMode = 1;
# static GLboolean    bHistogram = GL_FALSE;


# ifndef __APPLE__
# PFNGLHISTOGRAMPROC				glHistogram = NULL;
# PFNGLGETHISTOGRAMPROC			glGetHistogram = NULL;
# PFNGLCOLORTABLEPROC				glColorTable = NULL;
# PFNGLCONVOLUTIONFILTER2DPROC	glConvolutionFilter2D = NULL;
# endif
glConvolutionFilter2D = None
glColorTable = None
glGetHistogram = None
glHistogram = None


def SetupRC():
    global pImage
    # ifndef __APPLE__
    glHistogram = gltGetExtensionPointer("glHistogram")
    glGetHistogram = gltGetExtensionPointer("glGetHistogram")
    glColorTable = gltGetExtensionPointer("glColorTable")
    glConvolutionFilter2D = gltGetExtensionPointer("glConvolutionFilter2D")
    # endif

    glClearColor(0.0, 0.0, 0.0, 0.0)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    pImage = LoadTGA("C:/temp/horse.tga", iWidth,
                     iHeight, iComponents, eFormat)


# def ShutdownRC(void):

    # free(pImage)


def ProcessMenu(value):
    global iRenderMode
    global bHistogram
    if(value == 6):

        bHistogram = GL_TRUE
        glutPostRedisplay()

    if(value == 0):

        WriteTGA("ScreenShot.tga")
    else:
        iRenderMode = value

    glutPostRedisplay()


def RenderScene():
    global i
    global iLargest
    global lumMat
    global mSharpen
    global mEmboss
    global iViewport
    invertTable = [[0]*256]*3
    histoGram = [0]*256
    # GLint i;                    // Looping variable
    # GLint iViewport[4];         // Viewport
    # GLint iLargest;				// Largest histogram value

    # static GLubyte invertTable[256][3];// Inverted color table

    lumMat = [0.30, 0.30, 0.30, 0.0,
              0.59, 0.59, 0.59, 0.0,
              0.11, 0.11, 0.11, 0.0,
              0.0,  0.0,  0.0,  1.0]

    mSharpen = [[0.0, -1.0, 0.0], [-1.0, 5.0, -1.0], [0.0, -1.0, 0.0]]

    mEmboss = [[2.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]]

    # static GLint histoGram[256];

    glClear(GL_COLOR_BUFFER_BIT)

    glRasterPos2i(0, 0)
    glGetIntegerv(GL_VIEWPORT, iViewport)
    glPixelZoom(iViewport / iWidth, iViewport / iHeight)

    if(bHistogram == GL_TRUE):

        glMatrixMode(GL_COLOR)
        glLoadMatrixf(lumMat)
        glMatrixMode(GL_MODELVIEW)

        glHistogram(GL_HISTOGRAM, 256, GL_LUMINANCE, GL_FALSE)
        glEnable(GL_HISTOGRAM)

    while(True):

        if iRenderMode == 5:
            glConvolutionFilter2D(GL_CONVOLUTION_2D, GL_RGB,
                                  3, 3, GL_LUMINANCE, GL_FLOAT, mSharpen)
            glEnable(GL_CONVOLUTION_2D)
            break

        elif iRenderMode == 4:
            glConvolutionFilter2D(GL_CONVOLUTION_2D, GL_RGB,
                                  3, 3, GL_LUMINANCE, GL_FLOAT, mEmboss)
            glEnable(GL_CONVOLUTION_2D)
            glMatrixMode(GL_COLOR)
            glLoadMatrixf(lumMat)
            glMatrixMode(GL_MODELVIEW)
            break

        elif iRenderMode == 3:

            for i in range(0, 255, 1):
                invertTable[i][0] = (GLubyte)(255 - i)
                invertTable[i][1] = (GLubyte)(255 - i)
                invertTable[i][2] = (GLubyte)(255 - i)

            glColorTable(GL_COLOR_TABLE, GL_RGB, 256, GL_RGB,
                         GL_UNSIGNED_BYTE, invertTable)
            glEnable(GL_COLOR_TABLE)
            break

        elif iRenderMode == 2:
            glMatrixMode(GL_COLOR)
            glScalef(1.25, 1.25, 1.25)
            glMatrixMode(GL_MODELVIEW)
            break

        elif iRenderMode == 1:

            break

    glDrawPixels(iWidth, iHeight, eFormat, GL_UNSIGNED_BYTE, pImage)

    if(bHistogram == GL_TRUE):

        glGetHistogram(GL_HISTOGRAM, GL_TRUE, GL_LUMINANCE, GL_INT, histoGram)

        iLargest = 0

        for i in range(0, 255, 1):
            if(iLargest < histoGram[i]):
                iLargest = histoGram[i]

        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_STRIP)
        for i in range(0, 255, 1):
            glVertex2f(i, histoGram[i] / iLargest * 128.0)
        glEnd()

        bHistogram = GL_FALSE
        glDisable(GL_HISTOGRAM)

    glMatrixMode(GL_COLOR)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_CONVOLUTION_2D)
    glDisable(GL_COLOR_TABLE)

    glutSwapBuffers()


def ChangeSize(w, h):

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
glutInitWindowSize(600, 600)
glutCreateWindow("OpenGL Imaging subset")


if(gltIsExtSupported("GL_ARB_imaging") == 0):
    print("Imaging subset not supported\r\n")


glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)

glutCreateMenu(ProcessMenu)
glutAddMenuEntry("Save Image", 0)
glutAddMenuEntry("Raw Stretched Image", 1)
glutAddMenuEntry("Increase Contrast", 2)
glutAddMenuEntry("Invert Color", 3)
glutAddMenuEntry("Emboss Image", 4)
glutAddMenuEntry("Sharpen Image", 5)
glutAddMenuEntry("Histogram", 6)

glutAttachMenu(GLUT_RIGHT_BUTTON)

SetupRC()

glutMainLoop()

# ShutdownRC()
