# Nurbs.c
# OpenGL SuperBible
# Program by Richard S.Wright Jr.

# include "../../Common/OpenGLSB.h"	# System and OpenGL Stuff
# include "../../Common/GLTools.h"   # GLTools

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Common.OpenGLCommon import *
from Common.TGACommon import *

# NURBS object pointer
pNurb = None

# The number of control points for this curve
nNumPoints = 4 # 4 X 4

# Mesh extends four units - 6 to + 6 along x and y axis
# Lies in Z plane
#u v(x, y, z)
ctrlPoints = [[[-6.0, -6.0, 0.0],     # u = 0, v = 0
                [	-6.0, -2.0, 0.0],  #		v = 1
                [   -6.0,  2.0, 0.0],  #		v = 2
                [   -6.0,  6.0, 0.0]], #		v = 3

                [[  -2.0, -6.0, 0.0],  # u = 1	v = 0
                [   -2.0, -2.0, 8.0],  #		v = 1
                [   -2.0,  2.0, 8.0],  #		v = 2
#              [   -2.0, -2.0, 0.0],  #		v = 1
#              [   -2.0,  2.0, 0.0],  #		v = 2
                [   -2.0,  6.0, 0.0]], #		v = 3

                [[   2.0, -6.0, 0.0 ], # u =2   v = 0
                [   2.0, -2.0, 8.0],   #        v = 1
                [   2.0, 2.0, 8.0],    #        v = 2
#              [   2.0, -2.0, 0.0],   #        v = 1
#              [   2.0, 2.0, 0.0],    #        v = 2
                [   2.0, 6.0, 0.0]],   #        v = 3

                [[  6.0, -6.0, 0.0],     # u = 3  v = 0
                [   6.0, -2.0, 0.0],     #        v = 1
                [   6.0, 2.0, 0.0],      #        v = 2
                [   6.0, 6.0, 0.0]]]    #        v = 3

# Knot sequence for the NURB
Knots = [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]

# Called to draw the control points in Red over the NURB
def DrawPoints():

    global ctrlPoints

    i, j = 0, 0

    # Large Red Points
    glPointSize(5.0)
    glColor3ub(255, 0, 0)

    # Draw all the points in the array
    glBegin(GL_POINTS)
    for i in range(0, 4, 1):
        for j in range(0, 4, 1):
            glVertex3fv(ctrlPoints[i][j])
    glEnd()

# NURBS callback error handler
def NurbsErrorHandler(nErrorCode):

    cMessage = [0 for i in range(64)]

    # Extract a text message of the error
    #strcpy(cMessage, "NURBS error occured: ")
    cMessage = "".join("NURBS error occured: ")
    #strcat(cMessage, gluErrorString(nErrorCode))
    errorCode = cMessage + gluErrorString(nErrorCode)

    # Display the message to the user
    #glutSetWindowTitle(cMessage)
    glutSetWindowTitle(errorCode)


# Called to draw scene
def RenderScene():

    global pNurb, ctrlPoints

    # Draw in Blue
    glColor3ub(0, 0, 220)

    # Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Save the modelview matrix stack
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    # Rotate the mesh around to make it easier to see
    glRotatef(330.0, 1.0, 0.0, 0.0)

    # Render the NURB
    # Begin the NURB definition
    gluBeginSurface(pNurb)

    # Evaluate the surface
    gluNurbsSurface(pNurb, # pointer to NURBS renderer
    #8, Knots,              # No.of knots and knot array u direction
    #8, Knots,              # No.of knots and knot array v direction
    Knots, Knots,
    #4 * 3,                 # Distance between control points in u dir.
    #3,                     # Distance between control points in v dir.
    ctrlPoints, # Control points
    #4, 4,                  # u and v order of surface
    GL_MAP2_VERTEX_3)     # Type of surface
    
    # Done with surface
    gluEndSurface(pNurb)
    
    # Show the control points
    DrawPoints()
    
    # Restore the modelview matrix
    glPopMatrix()
    
    # Dispalay the image
    glutSwapBuffers()

# This function does any needed initialization on the rendering
# context.Here it sets up and initializes the lighting for
# the scene.
def SetupRC():

    global pNurb

    # Light values and coordinates
    whiteLight = [0.7, 0.7, 0.7, 1.0]
    specular = [0.7, 0.7, 0.7, 1.0]
    shine = [100.0]
    
    # Clear Window to white
    glClearColor(1.0, 1.0, 1.0, 1.0 )
    
    # Enable lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Enable color tracking
    glEnable(GL_COLOR_MATERIAL)

    # Set Material properties to follow glColor values
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, shine)

    # Automatically generate normals for evaluated surfaces
    glEnable(GL_AUTO_NORMAL)
    
    # Setup the Nurbs object
    pNurb = gluNewNurbsRenderer()
    
    # Install error handler to notify user of NURBS errors
    gluNurbsCallback(pNurb, GLU_ERROR, NurbsErrorHandler)

    gluNurbsProperty(pNurb, GLU_SAMPLING_TOLERANCE, 25.0)
    # Uncomment the next line and comment the one following to produce a
    # wire frame mesh.
    # gluNurbsProperty(pNurb, GLU_DISPLAY_MODE, GLU_OUTLINE_POLYGON)
    gluNurbsProperty(pNurb, GLU_DISPLAY_MODE, GLU_FILL)

def ChangeSize(w, h):

    # Prevent a divide by zero
    if (h == 0):
        h = 1
    
    # Set Viewport to window dimensions
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # Perspective view
    gluPerspective(45.0, w / h, 1.0, 40.0)
    
    # Modelview matrix reset
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Viewing transformation, position for better view
    glTranslatef (0.0, 0.0, -20.0)

if __name__ == '__main__':

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"NURBS Surface")
    glutReshapeFunc(ChangeSize)
    glutDisplayFunc(RenderScene)
    SetupRC()
    glutMainLoop()