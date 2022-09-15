# Toon.c
# OpenGL SuperBible
# Demonstrates Cell/Toon shading with a 1D texture
# Program by Richard S. Wright Jr.
from math import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGLCommon import *
from TGACommon import *
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


GLT_PI = 3.14
yRot = 0.0


# Draw a torus (doughnut), using the current 1D texture for light shading
def toonDrawTorus(majorRadius, minorRadius, numMajor, numMinor, vLightDir):

    global GLT_PI

    mModelViewMatrix = GLTMatrix()
    vNormal = GLTVector3()
    vTransformedNormal = GLTVector3()
    majorStep = 2.0*GLT_PI / numMajor
    minorStep = 2.0*GLT_PI / numMinor
    i = 0.0
    j = 0.0

    # Get the modelview matrix
    temp = glGetFloatv(GL_MODELVIEW_MATRIX)
    mModelViewMatrix.setValue2DArray(temp)

    # Normalize the light vector
    gltNormalizeVector(vLightDir)

    # Draw torus as a series of triangle strips
    # for (i = 0 i < numMajor ++i)
    for i in range(0, numMajor, 1):

        a0 = i * majorStep
        a1 = a0 + majorStep
        x0 = cos(a0)
        y0 = sin(a0)
        x1 = cos(a1)
        y1 = sin(a1)

        glBegin(GL_TRIANGLE_STRIP)
        # for (j = 0 j <= numMinor ++j)
        for j in range(0, numMinor, 1):

            b = j * minorStep
            c = cos(b)
            r = minorRadius * c + majorRadius
            z = minorRadius * sin(b)

            # First point
            vNormal.value[0] = x0 * c
            vNormal.value[1] = y0 * c
            vNormal.value[2] = z / minorRadius
            gltNormalizeVector(vNormal)
            gltRotateVector(vNormal, mModelViewMatrix, vTransformedNormal)

            # Texture coordinate is set by intensity of light
            glTexCoord1f(gltVectorDotProduct(vLightDir, vTransformedNormal))
            glVertex3f(x0*r, y0*r, z)

            # Second point
            vNormal.value[0] = x1 * c
            vNormal.value[1] = y1 * c
            vNormal.value[2] = z / minorRadius
            gltNormalizeVector(vNormal)
            gltRotateVector(vNormal, mModelViewMatrix, vTransformedNormal)

            # Texture coordinate is set by intensity of light
            glTexCoord1f(gltVectorDotProduct(vLightDir, vTransformedNormal))
            glVertex3f(x1*r, y1*r, z)

        glEnd()


# Called to draw scene
def RenderScene():

    # Rotation angle
    global yRot

    # Where is the light coming from
    vLightDir = GLTVector3()
    vLightDir.value = [-1.0, 1.0, 1.0]

    # Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glTranslatef(0.0, 0.0, -2.5)
    glRotatef(yRot, 0.0, 1.0, 0.0)
    toonDrawTorus(0.35, 0.15, 50, 25, vLightDir)
    glPopMatrix()

    # Do the buffer Swap
    glutSwapBuffers()

    # Rotate 1/2 degree more each frame
    yRot += 0.5

# This function does any needed initialization on the rendering
# context.


def SetupRC():

    # Load a 1D texture with toon shaded values
    # Green, greener...
    toonTable = [[0, 32, 0],
                 [0, 64, 0],
                 [0, 128, 0],
                 [0, 192, 0]]

    # Bluish background
    glClearColor(0.0, 0.0, .50, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage1D(GL_TEXTURE_1D, 0, GL_RGB, 4, 0,
                 GL_RGB, GL_UNSIGNED_BYTE, toonTable)

    glEnable(GL_TEXTURE_1D)


# /
# Called by GLUT library when idle (window not being
# resized or moved)
def TimerFunction(value):

    # Redraw the scene with new coordinates
    glutPostRedisplay()
    glutTimerFunc(33, TimerFunction, 1)


def ChangeSize(w, h):

    fAspect = 0.0

    # Prevent a divide by zero, when window is too short
    # (you cant make a window of zero width).
    if (h == 0):
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


# /
# Program entry point
if __name__ == '__main__':

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Toon/Cell Shading Demo")
    glutReshapeFunc(ChangeSize)
    glutDisplayFunc(RenderScene)
    glutTimerFunc(33, TimerFunction, 1)

    SetupRC()
    glutMainLoop()
