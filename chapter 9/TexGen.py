from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Common.OpenGLCommon import *
from Common.TGACommon import *
# // TexGen.c
# // OpenGL SuperBible
# // Demonstrates OpenGL Texture Coordinate Generation
# // Program by Richard S. Wright Jr.

# include "../../Common/OpenGLSB.h"	// System and OpenGL Stuff
# include "../../Common/gltools.h"   // gltools library

# // Rotation amounts
xRot = 0.0
yRot = 0.0

toTextures = [2]*2
iRenderMode = 3


# ///////////////////////////////////////////////////////////////////////////////
# // Reset flags as appropriate in response to menu selections
def ProcessMenu(value):
    global iRenderMode
    # // Projection plane
    zPlane = [0.0, 0.0, 1.0, 0.0]

    # // Store render mode
    iRenderMode = value

    # // Set up textgen based on menu selection
    # switch(value)
    while True:

        if value == 1:
            # // Object Linear
            glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
            glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
            glTexGenfv(GL_S, GL_OBJECT_PLANE, zPlane)
            glTexGenfv(GL_T, GL_OBJECT_PLANE, zPlane)
            break

        elif value == 2:
            # // Eye Linear
            glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
            glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
            glTexGenfv(GL_S, GL_EYE_PLANE, zPlane)
            glTexGenfv(GL_T, GL_EYE_PLANE, zPlane)
            break

        elif value == 3:

            # // Sphere Map
            glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
            glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
            break

    glutPostRedisplay()  # // Redisplay


# ///////////////////////////////////////////////////////////////////////////////
# // Called to draw scene
def RenderScene():

    # // Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # // Switch to orthographic view for background drawing
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)

    glMatrixMode(GL_MODELVIEW)
    # glBindTexture(GL_TEXTURE_2D, toTextures[1]);    // Background texture

    # // We will specify texture coordinates
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)

    # // No depth buffer writes for background
    glDepthMask(GL_FALSE)

    # // Background image
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(0.0, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex2f(1.0, 0.0)

    glTexCoord2f(1.0, 1.0)
    glVertex2f(1.0, 1.0)

    glTexCoord2f(0.0, 1.0)
    glVertex2f(0.0, 1.0)
    glEnd()

    # // Back to 3D land
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    # // Turn texgen and depth writing back on
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glDepthMask(GL_TRUE)

    # // May need to swtich to stripe texture
    if(iRenderMode != 3):
        glBindTexture(GL_TEXTURE_2D, toTextures[0])

    # // Save the matrix state and do the rotations
    glPushMatrix()
    glTranslatef(0.0, 0.0, -2.0)
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    # // Draw the tours
    gltDrawTorus(0.35, 0.15, 61, 37)

    # // Restore the matrix state
    glPopMatrix()

    # // Display the results
    glutSwapBuffers()


# ///////////////////////////////////////////////////////////////////////////////
# // This function does any needed initialization on the rendering
# // context.
def SetupRC():

    iWidth = [0]
    iHeight = [0]
    eFormat = [0]
    iComponents = [0]
    global pBytes
    global toTextures
    # GLenum eFormat;                     #// Texture format
    #global eFormat

    glEnable(GL_DEPTH_TEST)  # // Hidden surface removal
    glFrontFace(GL_CCW)  # // Counter clock-wise polygons face out
    glEnable(GL_CULL_FACE)  # // Do not calculate inside of jet

    # // White background
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # // Decal texture environment
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    # // Two textures
    glGenTextures(2, toTextures)

    #  ///////////////////////////////////////////
    # // Load the main texture
    glBindTexture(GL_TEXTURE_2D, toTextures[0])
    pBytes = LoadTGA("C:\\Users\\akfmz\Desktop\opngl 세미나\챕터 9\stripes.tga",
                     iWidth, iHeight, iComponents, eFormat)
    glTexImage2D(GL_TEXTURE_2D, 0, iComponents[0], iWidth[0],
                 iHeight[0], 0, eFormat[0], GL_UNSIGNED_BYTE, pBytes)
    # free(pBytes);

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glEnable(GL_TEXTURE_2D)

    #  ///////////////////////////////////////////
    # // Load environment map
    glBindTexture(GL_TEXTURE_2D, toTextures[1])
    pBytes = LoadTGA("C:\\Users\\akfmz\Desktop\opngl 세미나\챕터 9\Environment.tga",
                     iWidth, iHeight, iComponents, eFormat)
    glTexImage2D(GL_TEXTURE_2D, 0, iComponents[0], iWidth[0],
                 iHeight[0], 0, eFormat[0], GL_UNSIGNED_BYTE, pBytes)
    # free(pBytes);

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glEnable(GL_TEXTURE_2D)

    # // Turn on texture coordiante generation
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)

    # // Sphere Map will be the default
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)


# /////////////////////////////////////////////////////
# // Handle arrow keys
def SpecialKeys(key,  x,  y):

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

    # // Refresh the Window
    glutPostRedisplay()


# //////////////////////////////////////////////////////////
# // Reset projection and light position
def ChangeSize(w,  h):

    global fAspect

    # // Prevent a divide by zero
    if(h == 0):
        h = 1

    # // Set Viewport to window dimensions
    glViewport(0, 0, w, h)

    # // Reset coordinate system
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    fAspect = w / h
    gluPerspective(45.0, fAspect, 1.0, 225.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# ///////////////////////////////////////////////////////////////////////////////
# // Program Entry Point


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Texture Coordinate Generation")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()

# // Create the Menu
glutCreateMenu(ProcessMenu)
glutAddMenuEntry("Object Linear", 1)
glutAddMenuEntry("Eye Linear", 2)
glutAddMenuEntry("Sphere Map", 3)
glutAttachMenu(GLUT_RIGHT_BUTTON)

glutMainLoop()

# // Don't forget the texture objects
glDeleteTextures(2, toTextures)
