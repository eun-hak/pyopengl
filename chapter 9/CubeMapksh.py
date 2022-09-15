# CubeMap.c
# OpenGL SuperBible
# Demonstrates an immersive 3D environment using actors
# and a camera. This version adds lights and material properties
# and shadows.
# Program by Richard S. Wright Jr.

import random
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from OpenGLCommon import *
from TGACommon import *

# include "../../Common/OpenGLSB.h"   #System and OpenGL Stuff
# include "../../Common/GLTools.h"   #OpenGL toolkit
# include <math.h>
pImage = None
iWidth = [0]
iHeight = [0]
eFormat = [0]
iComponents = [0]
NUM_SPHERES = 30

# Light and material Data
fLightpos = GLTVector4()
mShadowMatrix = GLTMatrix()

fLightpos.value = [-100.0, 100.0, 50.0, 1.0]
fNoLight = [0.0, 0.0, 0.0, 0.0]
fLowLight = [0.25, 0.25, 0.25, 1.0]
fBrightLight = [1.0, 1.0, 1.0, 1.0]
yRot = 0.0
frameCamera = GLTFrame()

spheres = [GLTFrame() for i in range(NUM_SPHERES)]

SPHERE_TEXTURE = 1
GROUND_TEXTURE = 0
CUBE_MAP = 2
NUM_TEXTURES = 3
textureObjects = []*NUM_TEXTURES

szTextureFiles = ["grass.tga", "orb.tga", "DOWN.tga"]

szCubeFaces = ["right.tga", "left.tga", "up.tga",
               "down.tga", "backward.tga", "forward.tga"]

cube = [GL_TEXTURE_CUBE_MAP_POSITIVE_X,
        GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
        GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
        GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
        GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
        GL_TEXTURE_CUBE_MAP_NEGATIVE_Z]


# //////////////////////////////////////////////////////////////////
# This function does any needed initialization on the rendering
# context.
def SetupRC():
    global NUM_TEXTURES
    global CUBE_MAP
    global NUM_SPHERES
    global textureObjects
    global fLightpos
    global spheres, frameCamera
    global mShadowMatrix
    global pImage, iWidth, iHeight, eFormat, iComponents
    global szTextureFiles
    global szCubeFaces

    # Grayish background
    glClearColor(fLowLight[0], fLowLight[1], fLowLight[2], fLowLight[3])

    # Cull backs of polygons
    glCullFace(GL_BACK)
    glFrontFace(GL_CCW)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    # Setup light parameters
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, fNoLight)
    glLightModeli(GL_LIGHT_MODEL_COLOR_CONTROL, GL_SEPARATE_SPECULAR_COLOR)
    glLightfv(GL_LIGHT0, GL_AMBIENT, fLowLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, fBrightLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, fBrightLight)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Mostly use material tracking
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMateriali(GL_FRONT, GL_SHININESS, 128)

    gltInitFrame(frameCamera)  # Initialize the camera

    # Randomly place the sphere inhabitants
    for iSphere in range(0, NUM_SPHERES, 1):

        gltInitFrame(spheres[iSphere])
        
        # Pick a random location between -20 and 20 at .1 increments
        spheres[iSphere].vLocation.value[0] = float(((random.randrange(0, 32767) % 400) - 200) * 0.1)
        spheres[iSphere].vLocation.value[1] = 0.0
        spheres[iSphere].vLocation.value[2] = float(((random.randrange(0, 32767) % 400) - 200) * 0.1)
    # Set up texture maps
    glEnable(GL_TEXTURE_2D)
    textureObjects =  glGenTextures(NUM_TEXTURES)
    #glGenTextures(NUM_TEXTURES, textureObjects)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    # Load regular textures

    for i in range(0, CUBE_MAP, 1):

        glBindTexture(GL_TEXTURE_2D, textureObjects[i])

        # Load this texture map
        glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)
        pBytes = LoadTGA(szTextureFiles[i],
                         iWidth, iHeight, iComponents, eFormat)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_COMPRESSED_RGB,
                     iWidth[0], iHeight[0], 0, eFormat[0], GL_UNSIGNED_BYTE, pBytes)
        # free(pBytes);

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)


    glBindTexture(GL_TEXTURE_CUBE_MAP, textureObjects[CUBE_MAP])
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_REPEAT)

    # Load Cube Map images

    for i in range(0, 6, 1):

        # Load this texture map
        #glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_GENERATE_MIPMAP, GL_TRUE);
        pBytes = LoadTGA(szCubeFaces[i], iWidth, iHeight, iComponents, eFormat)
        glTexImage2D(cube[i], 0, iComponents[0], iWidth[0],
                     iHeight[0], 0, eFormat[0], GL_UNSIGNED_BYTE, bytes(pBytes))
        # free(pBytes);

    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP)
    glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP)


# ////////////////////////////////////////////////////////////////////////
# Do shutdown for the rendering context
def ShutdownRC():
    global textureObjects

    # Delete the textures
    glDeleteTextures(NUM_TEXTURES, textureObjects)


# ///////////////////////////////////////////////////////////
# Draw the ground as a series of triangle strips
def DrawGround():
    global textureObjects, GROUND_TEXTURE
    fExtent = 20.0
    fStep = 1.0
    y = -0.4
    #global iStrip, iRun
    s = 0.0
    t = 0.0
    texStep = 1.0 / (fExtent * .075)

    glBindTexture(GL_TEXTURE_2D, textureObjects[GROUND_TEXTURE])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    for iStrip in numpy.arange(-fExtent, fExtent, fStep):
        t = 0.0
        glBegin(GL_TRIANGLE_STRIP)

        for iRun in numpy.arange(fExtent, -fExtent, -fStep):
            glTexCoord2f(s, t)
            glNormal3f(0.0, 1.0, 0.0)  # All Point up
            glVertex3f(iStrip, y, iRun)

            glTexCoord2f(s + texStep, t)
            glNormal3f(0.0, 1.0, 0.0)  # All Point up
            glVertex3f(iStrip + fStep, y, iRun)

            t += texStep

        glEnd()
        s += texStep


# ///////////////////////////////////////////////////////////////////////
# Draw random inhabitants and the rotating torus/sphere duo
def DrawInhabitants():
    global yRot
    global textureObjects
    global NUM_SPHERES
    global SPHERE_TEXTURE
    global CUBE_MAP
    global spheres
    global fBrightLight
    global fNoLight
    # Rotation angle for animation
    #global i

    yRot += 0.5
    glColor4f(1.0, 1.0, 1.0, 1.0)

    # Draw the randomly located spheres
    glBindTexture(GL_TEXTURE_2D, textureObjects[SPHERE_TEXTURE])
    for i in range(0, NUM_SPHERES, 1):
        glPushMatrix()
        gltApplyActorTransform(spheres[i])
        gltDrawSphere(0.3, 21, 11)
        glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 0.1, -2.5)

    # Torus alone will be specular
    glMaterialfv(GL_FRONT, GL_SPECULAR, fBrightLight)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    glDisable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_CUBE_MAP)
    glBindTexture(GL_TEXTURE_CUBE_MAP, textureObjects[CUBE_MAP])

    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glEnable(GL_TEXTURE_GEN_R)
    gltDrawTorus(0.35, 0.15, 61, 37)
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_TEXTURE_GEN_R)
    glDisable(GL_TEXTURE_CUBE_MAP)
    glEnable(GL_TEXTURE_2D)
    glMaterialfv(GL_FRONT, GL_SPECULAR, fNoLight)
    glPopMatrix()


# Called to draw scene
def RenderScene():
    global fLightpos

    # Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    gltApplyCameraTransform(frameCamera)

    # Position light before any other transformations
    glLightfv(GL_LIGHT0, GL_POSITION, fLightpos.value)

    # Draw the ground
    glColor3f(1.0, 1.0, 1.0)
    DrawGround()

    # Draw inhabitants
    DrawInhabitants()

    glPopMatrix()

    # Do the buffer Swap
    glutSwapBuffers()


# Respond to arrow keys by moving the camera frame of reference
def SpecialKeys(key,  x,  y):

    if(key == GLUT_KEY_UP):
        gltMoveFrameForward(frameCamera, 0.1)

    if(key == GLUT_KEY_DOWN):
        gltMoveFrameForward(frameCamera, -0.1)

    if(key == GLUT_KEY_LEFT):
        gltRotateFrameLocalY(frameCamera, 0.1)

    if(key == GLUT_KEY_RIGHT):
        gltRotateFrameLocalY(frameCamera, -0.1)

    # Refresh the Window
    glutPostRedisplay()


# ///////////////////////////////////////////////////////////
# Called by GLUT library when idle (window not being
# resized or moved)
def TimerFunction(value):

    # Redraw the scene with new coordinates
    glutPostRedisplay()
    glutTimerFunc(3, TimerFunction, 1)


def ChangeSize(w,  h):

    #global fAspect

    # Prevent a divide by zero, when window is too short
    # (you cant make a window of zero width).
    if(h == 0):
        h = 1

    glViewport(0, 0, w, h)

    fAspect = w / h

    # Reset the coordinate system before modifying
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Set the clipping volume
    gluPerspective(35.0, fAspect, 1.0, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("OpenGL SphereWorld Demo + Cube Maps")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
glutSpecialFunc(SpecialKeys)

SetupRC()
glutTimerFunc(33, TimerFunction, 1)

glutMainLoop()

ShutdownRC()