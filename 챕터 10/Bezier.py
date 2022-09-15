# Bezier.c
# OpenGL SuperBible
# Demonstrates OpenGL evaluators to draw bezier curve
# Program by Richard S. Wright Jr.

# include "../../Common/OpenGLSB.h"	#System and OpenGL Stuff
# include "../../Common/GLTools.h"   #GLTools

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Common.OpenGLCommon import *
from Common.TGACommon import *

# The number of control points for this curve
nNumPoints = 4


# ctrlPoints = [[[ -4.0, 0.0, 4.0]],
#                               [[ -2.0, 4.0, 0.0]],
#                               [[2.0,-4.0,0.0]],
#                              [[  4.0, 0.0, -4.0 ]]];

# GLfloat ctrlPoints[4][3]= {{  -4.0f, 0.0f, 0.0f},	// End Point
# 							{ -6.0f, 4.0f, 0.0f},	// Control Point
# 							{  6.0f, -4.0f, 0.0f},	// Control Point
# 							{  4.0f, 0.0f, 0.0f }};	// End Point


ctrlPoints = [[-4.0, 0.0, 0.0], [-6.0, 4.0, 0.0],
              [6.0, -4.0, 0.0], [4.0, 0.0, 0.0]]


# ctrlPoints = [[[-4.0, 0.0],

#                [4.0, 0.0]],

#               [[-4.0, 0.0],

#                [4.0, 0.0]],

#               [[-4.0, 0.0],

#                [4.0, 0.0]]]

# This function is used to superimpose the control poi.pynts over the curve


def DrawPoints():

    # Set point size larger to make more visible
    glPointSize(5.0)

    # Loop through all control points for this example
    glBegin(GL_POINTS)

    for i in range(0, nNumPoints, 1):

        for j in range(0, 1, 1):

            glVertex2f(ctrlPoints[i][j], ctrlPoints[i][j+1])

    # for i in range (0,nNumPoints,1):

    #         glVertex2fv(ctrlPoints[i]);
    glEnd()


# Called to draw scene
def RenderScene():

    # Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT)

    # Sets up the bezier
    # This actually only needs to be called once and could go in
    # the setup function
    glMap1f(GL_MAP1_VERTEX_3,  # Type of data generated
            0.0,  # Lower u range
            100.0,  # Upper u range
            # 3,							#Distance between points in the data
            # nNumPoints,					#number of control points
            ctrlPoints)  # array of control points

    # Enable the evaluator
    glEnable(GL_MAP1_VERTEX_3)

    # Use a line strip to "connect-the-dots"
    glBegin(GL_LINE_STRIP)
    for i in range(0, 100, 1):

        # Evaluate the curve at this point
        glEvalCoord1f(i)

    glEnd()

    # Use higher level functions to map to a grid, then evaluate the
    # entire thing.
    # Put these two functions in to replace above loop

    # Map a grid of 100 points from 0 to 100
    glMapGrid1d(100, 0.0, 100.0)

    # Evaluate the grid, using lines
    glEvalMesh1(GL_LINE, 0, 100)

    # Draw the Control Points
    DrawPoints()

    # Flush drawing commands
    glutSwapBuffers()


# This function does any needed initialization on the rendering
# context.
def SetupRC():

    # Clear Window to white
    glClearColor(1.0, 1.0, 1.0, 1.0)

    #Draw in Blue
    glColor3f(0.0, 0.0, 1.0)


# ///////////////////////////////////////
# Set 2D Projection
def ChangeSize(w,  h):

    # Prevent a divide by zero
    if(h == 0):
        h = 1

    # Set Viewport to window dimensions
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

    # Modelview matrix reset
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("2D Bezier Curve")
glutReshapeFunc(ChangeSize)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
