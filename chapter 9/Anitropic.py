from pickle import GLOBAL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Common.OpenGLCommon import *
from Common.TGACommon import *
# // Anisotropic.c
# // Demonstrates anisotropic texture filtering
# // OpenGL SuperBible
# // Richard S. Wright Jr.
# include "../../Common/OpenGLSB.h"	// System and OpenGL Stuff
# include "../../Common/GLTools.h"   // GLTools

# // Rotation amounts
zPos = -60.0

# // Texture objects
# define TEXTURE_BRICK   0
# define TEXTURE_FLOOR  1
# define TEXTURE_CEILING 2
# define TEXTURE_COUNT   3
TEXTURE_BRICK = 0
TEXTURE_FLOOR = 1
TEXTURE_CEILING = 2
TEXTURE_COUNT = 3

textures = [TEXTURE_COUNT]*TEXTURE_COUNT
szTextureFiles = ["C:/temp/brick.tga",
                  "C:/temp/floor.tga",
                  "C:/temp/ceiling.tga"]


# ///////////////////////////////////////////////////////////////////////////////
# // Change texture filter for each texture object
def ProcessMenu(value):

    global iLoop
    global fLargest

    # for(iLoop = 0; iLoop < TEXTURE_COUNT; iLoop++)
    #     {

    for iLoop in range(0, TEXTURE_COUNT, 1):

        glBindTexture(GL_TEXTURE_2D, textures[iLoop])

        # switch(value)
        #     {

        while(True):

            if value == 0:
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                break

            elif value == 1:
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                break

            elif value == 2:
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
                break

            elif value == 3:
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
                break

            elif value == 4:
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
                break

            elif value == 5:
                glTexParameteri(
                    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
                break

            elif value == 6:
                glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT, fLargest)
                glTexParameterf(
                    GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, fLargest)
                break

            elif value == 7:
                glTexParameterf(
                    GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, 1.0)
                break

    # // Trigger Redraw
    glutPostRedisplay()


# //////////////////////////////////////////////////////////////////
# // This function does any needed initialization on the rendering
# // context.  Here it sets up and initializes the texture objects.
def SetupRC():
    iWidth = [0]
    iHeight = [0]
    eFormat = [0]
    iComponents = [0]
    global pBytes
    # GLubyte *pBytes;
    # GLint iWidth, iHeight, iComponents;
    # GLenum eFormat;
    # GLint iLoop;

    # // Black background
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # // Textures applied as decals, no lighting or coloring effects
    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    # // Load textures
    glGenTextures(TEXTURE_COUNT, textures)
    # for(iLoop = 0; iLoop < TEXTURE_COUNT; iLoop++)
    #
    for iLoop in range(0, TEXTURE_COUNT, 1):
        # // Bind to next texture object
        glBindTexture(GL_TEXTURE_2D, textures[iLoop])

        # // Load texture, set filter and wrap modes
        pBytes = LoadTGA(szTextureFiles[iLoop],
                         iWidth, iHeight, iComponents, eFormat)
        gluBuild2DMipmaps(GL_TEXTURE_2D, iComponents[0], iWidth[0],
                          iHeight[0], eFormat[0], GL_UNSIGNED_BYTE, bytes(pBytes))
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        # // Don't need original texture data any more
        # free(pBytes);


# ///////////////////////////////////////////////////
# // Shutdown the rendering context. Just deletes the
# // texture objects
def ShutdownRC():

    glDeleteTextures(TEXTURE_COUNT, textures)


# ///////////////////////////////////////////////////
# // Respond to arrow keys, move the viewpoint back
# // and forth
def SpecialKeys(key,  x,  y):

    if(key == GLUT_KEY_UP):
        zPos += 1.0

    if(key == GLUT_KEY_DOWN):
        zPos -= 1.0

    # // Refresh the Window
    glutPostRedisplay()


# /////////////////////////////////////////////////////////////////////
# // Change viewing volume and viewport.  Called when window is resized
def ChangeSize(w,  h):

    global fAspect
    # // Prevent a divide by zero
    if(h == 0):
        h = 1

    # // Set Viewport to window dimensions
    glViewport(0, 0, w, h)

    fAspect = w/h

    # // Reset coordinate system
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # // Produce the perspective projection
    gluPerspective(90.0, fAspect, 1, 120)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# ///////////////////////////////////////////////////////
# // Called to draw scene
def RenderScene():

    global z

    # // Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT)

    # // Save the matrix state and do the rotations
    glPushMatrix()
    # // Move object back and do in place rotation
    glTranslatef(0.0, 0.0, zPos)

    # // Floor
    # for(z = 60.0f; z >= 0.0f; z -= 10)
    for z in range(60, 0, -10):
        glBindTexture(GL_TEXTURE_2D, textures[TEXTURE_FLOOR])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-10.0, -10.0, z)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(10.0, -10.0, z)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(10.0, -10.0, z - 10.0)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(-10.0, -10.0, z - 10.0)
        glEnd()

        # // Ceiling
        glBindTexture(GL_TEXTURE_2D, textures[TEXTURE_CEILING])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-10.0, 10.0, z - 10.0)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(10.0, 10.0, z - 10.0)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(10.0, 10.0, z)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(-10.0, 10.0, z)
        glEnd()

        # // Left Wall
        glBindTexture(GL_TEXTURE_2D, textures[TEXTURE_BRICK])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-10.0, -10.0, z)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(-10.0, -10.0, z - 10.0)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(-10.0, 10.0, z - 10.0)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(-10.0, 10.0, z)
        glEnd()

        # // Right Wall
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(10.0, 10.0, z)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(10.0, 10.0, z - 10.0)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(10.0, -10.0, z - 10.0)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(10.0, -10.0, z)
        glEnd()

    # // Restore the matrix state
    glPopMatrix()

    # // Buffer swap
    glutSwapBuffers()


# // Standard initialization stuff
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 600)
glutCreateWindow("Anisotropic Tunnel")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)

# // Add menu entries to change filter
glutCreateMenu(ProcessMenu)
glutAddMenuEntry("GL_NEAREST", 0)
glutAddMenuEntry("GL_LINEAR", 1)
glutAddMenuEntry("GL_NEAREST_MIPMAP_NEAREST", 2)
glutAddMenuEntry("GL_NEAREST_MIPMAP_LINEAR", 3)
glutAddMenuEntry("GL_LINEAR_MIPMAP_NEAREST", 4)
glutAddMenuEntry("GL_LINEAR_MIPMAP_LINEAR", 5)
glutAddMenuEntry("Anisotropic Filter", 6)
glutAddMenuEntry("Anisotropic Off", 7)
glutAttachMenu(GLUT_RIGHT_BUTTON)

# // Startup, loop, shutdown
SetupRC()
glutMainLoop()
ShutdownRC()
