#Nurbc.c
#OpenGL SuperBible
#Program by Richard S. Wright Jr.

#include "../../Common/OpenGLSB.h"	#System and OpenGL Stuff
#include "../../Common/GLTools.h"   #GLTools

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Common.OpenGLCommon import *
from Common.TGACommon import *
#NURBS object pointer
#pNurb = None
pNurb = gluNewNurbsRenderer()
#The number of control points for this curve
nNumPoints = 4; #4 X 4

#Mesh extends four units -6 to +6 along x and y axis
#Lies in Z plane
#                u  v  (x,y,z)	
ctrlPoints  =   [[-6.0, -6.0, 0.0],
                                [2.0, -2.0, 8.0],
                              [2.0,  6.0, 0.0],
                               [6.0, 6.0,  0.0]]


#Knot sequence for the NURB
Knots= [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]



#Called to draw the control points in Red over the NURB
def DrawPoints():
    
    

	#Large Red Points
	glPointSize(5.0);
	glColor3ub(255,0,0);

	#Draw all the points in the array
	glBegin(GL_POINTS);
		
	for i in range(0,4,1):
		glVertex3fv(ctrlPoints[i]);	
	glEnd();
    

#NURBS callback error handler
def NurbsErrorHandler( nErrorCode):
    cMessage = []*64
    #cMessage[64];

    #Extract a text message of the error
    str(cMessage,"NURBS error occured: ");
	
    str(cMessage,gluErrorString(nErrorCode));

    #Display the message to the user
    glutSetWindowTitle(cMessage);
    



#Called to draw scene
def RenderScene():
	global pNurb

	#Draw in Blue
	glColor3ub(0,0,220);

	#Clear the window with current clearing color
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	#Save the modelview matrix stack
	glMatrixMode(GL_MODELVIEW);
	glPushMatrix();

	#Rotate the mesh around to make it easier to see
	glRotatef(330.0, 1.0,0.0,0.0);

	#Render the NURB
	#Begin the NURB definition
	gluBeginCurve(pNurb);

	#Evaluate the surface
	gluNurbsCurve(pNurb, 
		#8, 
		Knots,
		#3,
		ctrlPoints, 
		#4,
		GL_MAP1_VERTEX_3);

	#Done with surface
	gluEndCurve(pNurb);

	#Show the control points
	DrawPoints();

	#Restore the modelview matrix
	glPopMatrix();

	#Dispalay the image
	glutSwapBuffers();
	

#This function does any needed initialization on the rendering
#context.  Here it sets up and initializes the lighting for
#the scene.
def SetupRC():
	
	#Clear Window to white
	glClearColor(1.0, 1.0, 1.0, 1.0 );

	#Setup the Nurbs object
	pNurb = gluNewNurbsRenderer();
	gluNurbsProperty(pNurb, GLU_SAMPLING_TOLERANCE, 25.0);
	gluNurbsProperty(pNurb, GLU_DISPLAY_MODE, GLU_FILL);
	


def ChangeSize( w,  h):
	
	#Prevent a divide by zero
	if(h == 0):
		h = 1;

	#Set Viewport to window dimensions
	glViewport(0, 0, w, h);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	#Perspective view
	gluPerspective (45.0, w/h, 1.0, 40.0);

	#Modelview matrix reset
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	#Viewing transformation, position for better view
	glTranslatef (0.0, 0.0, -20.0);
	


glutInit();
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
glutInitWindowSize(800, 600);
glutCreateWindow("NURBS Curve");
glutReshapeFunc(ChangeSize);
glutDisplayFunc(RenderScene);
SetupRC();
glutMainLoop();

	
