from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *
from TGACommon import *

iWidth = [0]
iHeight = [0]
eFormat = [0]
iComponents = [0]

iViewport = [0]*4
invertMap = [0]*256
pImage = None
iRenderMode = 1
pModifiedBytes = None


def SetupRC():
    global pImage
    global iWidth, iHeight, iComponents
    global eFormat
    global iRenderMode
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    pImage = LoadTGA("C:/temp/horse.tga", iWidth,
                     iHeight,  iComponents,  eFormat)


# def ShutdownRC(void):

    # free(pImage)


def ProcessMenu(value):
    global iRenderMode
    if(value == 0):
        WriteTGA("ScreenShot.tga")
    else:
        iRenderMode = value

    glutPostRedisplay()


def RenderScene():
    global iViewport
    global pModifiedBytes
    global invertMap
    global i

    glClear(GL_COLOR_BUFFER_BIT)

    glRasterPos2i(0, 0)

    while (True):

        if iRenderMode == 2:
            glPixelZoom(-1.0, -1.0)
            glRasterPos2i(iWidth, iHeight)
            break

        elif iRenderMode == 3:
            glGetIntegerv(GL_VIEWPORT, iViewport)
            glPixelZoom(iViewport / iWidth, iViewport / iHeight)
            break

        elif iRenderMode == 4:
            glPixelTransferf(GL_RED_SCALE, 1.0)
            glPixelTransferf(GL_GREEN_SCALE, 0.0)
            glPixelTransferf(GL_BLUE_SCALE, 0.0)
            break

        elif iRenderMode == 5:
            glPixelTransferf(GL_RED_SCALE, 0.0)
            glPixelTransferf(GL_GREEN_SCALE, 1.0)
            glPixelTransferf(GL_BLUE_SCALE, 0.0)
            break

        elif iRenderMode == 6:
            glPixelTransferf(GL_RED_SCALE, 0.0)
            glPixelTransferf(GL_GREEN_SCALE, 0.0)
            glPixelTransferf(GL_BLUE_SCALE, 1.0)
            break

        elif iRenderMode == 7:
            glDrawPixels(iWidth, iHeight, eFormat, GL_UNSIGNED_BYTE, pImage)

            pModifiedBytes = iWidth * iHeight

            glPixelTransferf(GL_RED_SCALE, 0.3)
            glPixelTransferf(GL_GREEN_SCALE, 0.59)
            glPixelTransferf(GL_BLUE_SCALE, 0.11)

            glReadPixels(0, 0, iWidth, iHeight, GL_LUMINANCE,
                         GL_UNSIGNED_BYTE, pModifiedBytes)

            glPixelTransferf(GL_RED_SCALE, 1.0)
            glPixelTransferf(GL_GREEN_SCALE, 1.0)
            glPixelTransferf(GL_BLUE_SCALE, 1.0)
            break

        elif iRenderMode == 8:
            invertMap[0] = 1.0

            for i in range(1, 256, 1):
                invertMap[i] = 1.0 - (1.0 / 255.0 * i)

            glPixelMapfv(GL_PIXEL_MAP_R_TO_R, 255, invertMap)
            glPixelMapfv(GL_PIXEL_MAP_G_TO_G, 255, invertMap)
            glPixelMapfv(GL_PIXEL_MAP_B_TO_B, 255, invertMap)
            glPixelTransferi(GL_MAP_COLOR, GL_TRUE)
            break

        elif iRenderMode == 1:

            break

    if(pModifiedBytes == None):
        glDrawPixels(iWidth[0], iHeight[0], eFormat[0],
                     GL_UNSIGNED_BYTE, pImage)
    else:

        glDrawPixels(iWidth, iHeight, GL_LUMINANCE,
                     GL_UNSIGNED_BYTE, pModifiedBytes)

        del pModifiedBytes

    glPixelTransferi(GL_MAP_COLOR, GL_FALSE)
    glPixelTransferf(GL_RED_SCALE, 1.0)
    glPixelTransferf(GL_GREEN_SCALE, 1.0)
    glPixelTransferf(GL_BLUE_SCALE, 1.0)
    glPixelZoom(1.0, 1.0)

    glutSwapBuffers()


def ChangeSize(w, h):

    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(0.0,  w, 0.0, h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_RGB | GL_DOUBLE)
glutInitWindowSize(800, 600)
glutCreateWindow("OpenGL Image Operations")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)

glutCreateMenu(ProcessMenu)
glutAddMenuEntry("Save Image", 0)
glutAddMenuEntry("Draw Pixels", 1)
glutAddMenuEntry("Flip Pixels", 2)
glutAddMenuEntry("Zoom Pixels", 3)
glutAddMenuEntry("Just Red Channel", 4)
glutAddMenuEntry("Just Green Channel", 5)
glutAddMenuEntry("Just Blue Channel", 6)
glutAddMenuEntry("Black and White", 7)
glutAddMenuEntry("Invert Colors", 8)
glutAttachMenu(GLUT_RIGHT_BUTTON)
SetupRC()
glutMainLoop()
# ShutdownRC()
