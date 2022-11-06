# Planets.c
# OpenGL SuperBible, 3rd Edition
# Richard S. Wright Jr.
# rwright@starstonesoftware.com

# include "../../Common/OpenGLSB.h"	#System and OpenGL Stuff

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *
from TGACommon import *
# ///////////////////////////////
# Define object names
SUN = 1
MERCURY = 2
VENUS = 3
EARTH = 4
MARS = 5


# ///////////////////////////////////////////////////////////
# Just draw a sphere of some given radius
def DrawSphere(radius):

    #GLUquadricObj *pObj;
    pObj = gluNewQuadric()
    gluQuadricNormals(pObj, GLU_SMOOTH)
    gluSphere(pObj, radius, 26, 13)
    gluDeleteQuadric(pObj)


# ///////////////////////////////////////////////////////////
# Called to draw scene
def RenderScene():

    # Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Save the matrix state and do the rotations
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    # Translate the whole scene out and into view
    glTranslatef(0.0, 0.0, -300.0)

    # Initialize the names stack
    glInitNames()
    glPushName(0)

    # Name and draw the Sun
    glColor3f(1.0, 1.0, 0.0)
    glLoadName(SUN)
    DrawSphere(15.0)

    # Draw Mercury
    glColor3f(0.5, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(24.0, 0.0, 0.0)
    glLoadName(MERCURY)
    DrawSphere(2.0)
    glPopMatrix()

    # Draw Venus
    glColor3f(0.5, 0.5, 1.0)
    glPushMatrix()
    glTranslatef(60.0, 0.0, 0.0)
    glLoadName(VENUS)
    DrawSphere(4.0)
    glPopMatrix()

    # Draw the Earth
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(100.0, 0.0, 0.0)
    glLoadName(EARTH)
    DrawSphere(8.0)
    glPopMatrix()

    # Draw Mars
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(150.0, 0.0, 0.0)
    glLoadName(MARS)
    DrawSphere(4.0)
    glPopMatrix()

    # Restore the matrix state
    glPopMatrix()  # Modelview matrix

    glutSwapBuffers()


# ///////////////////////////////////////////////////////////
# Present the information on which planet/sun was selected
# and displayed
def ProcessPlanet(id):

    while True:

        if id == SUN:
            glutSetWindowTitle("You clicked on the Sun!")
            break

        elif id == MERCURY:
            glutSetWindowTitle("You clicked on Mercury!")
            break

        elif id == VENUS:
            glutSetWindowTitle("You clicked on Venus!")
            break

        elif id == EARTH:
            glutSetWindowTitle("You clicked on Earth!")
            break

        elif id == MARS:
            glutSetWindowTitle("You clicked on Mars!")
            break

        else:
            glutSetWindowTitle("Nothing was clicked on!")
            break


# ///////////////////////////////////////////////////////////
# Process the selection, which is triggered by a right mouse
# click at (xPos, yPos).
BUFFER_LENGTH = 64


def ProcessSelection(xPos,  yPos):

    # Space for selection buffer

    # ic GLuint selectBuff[BUFFER_LENGTH];

    selectBuff = []*BUFFER_LENGTH

    # Hit counter and viewport storage

    # GLint hits, viewport[4];
    viewport = []*4
    # Setup selection buffer
    glSelectBuffer(BUFFER_LENGTH, selectBuff)

    # Get the viewport
    glGetIntegerv(GL_VIEWPORT, viewport)

    # Switch to projection and save the matrix
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()

    # Change render mode
    glRenderMode(GL_SELECT)

    # Establish new clipping volume to be unit cube around
    # mouse cursor point (xPos, yPos) and extending two pixels
    # in the vertical and horizontal direction
    glLoadIdentity()
    gluPickMatrix(xPos, viewport[3] - yPos, 2, 2, viewport)

    # Apply perspective matrix
    fAspect = viewport[2] / viewport[3]
    gluPerspective(45.0, fAspect, 1.0, 425.0)

    # Draw the scene
    RenderScene()

    # Collect the hits
    hits = glRenderMode(GL_RENDER)

    # If a single hit occurred, display the info.
    if(hits == 1):
        ProcessPlanet(selectBuff[3])
    else:
        glutSetWindowTitle("Nothing was clicked on!")

    # Restore the projection matrix
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    # Go back to modelview for normal rendering
    glMatrixMode(GL_MODELVIEW)


# ///////////////////////////////////////////////////////////
# Process the mouse click
def MouseCallback(button,  state,  x,  y):

    if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        ProcessSelection(x, y)


# ///////////////////////////////////////////////////////////
# This function does any needed initialization on the
# rendering context.
def SetupRC():

    # Lighting values
    dimLight = [0.1, 0.1, 0.1, 1.0]
    sourceLight = [0.65, 0.65, 0.65, 1.0]
    lightPos = [0.0, 0.0, 0.0, 1.0]

    # Light values and coordinates
    glEnable(GL_DEPTH_TEST)  # Hidden surface removal
    glFrontFace(GL_CCW)  # Counter clock-wise polygons face out
    glEnable(GL_CULL_FACE)  # Do not calculate insides

    # Enable lighting
    glEnable(GL_LIGHTING)

    # Setup and enable light 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, dimLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, sourceLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glEnable(GL_LIGHT0)

    # Enable color tracking
    glEnable(GL_COLOR_MATERIAL)

    # Set Material properties to follow glColor values
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Gray background
    glClearColor(0.60, 0.60, 0.60, 1.0)


# ///////////////////////////////////////////////////////////
# Window changed size, reset viewport and projection
def ChangeSize(w, h):

    # Prevent a divide by zero
    if(h == 0):
        h = 1

    # Set Viewport to window dimensions
    glViewport(0, 0, w, h)

    # Calculate aspect ratio of the window
    fAspect = w/h

    # Set the perspective coordinate system
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Field of view of 45 degrees, near and far planes 1.0 and 425
    gluPerspective(45.0, fAspect, 1.0, 425.0)

    # Modelview matrix reset
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# ///////////////////////////////////////////////////////////
# Entry point of the program

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Pick a Planet")
glutReshapeFunc(ChangeSize)
glutMouseFunc(MouseCallback)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
