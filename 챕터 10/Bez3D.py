#Bez3d.c
#OpenGL SuperBible
#Program by Richard S. Wright Jr.

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Common.OpenGLCommon import *
from Common.TGACommon import *
#include "../../Common/OpenGLSB.h"	#System and OpenGL Stuff
#include "../../Common/GLTools.h"   #GLTools

#The number of control points for this curve
nNumPoints = 3

ctrlPoints = [[[ -4.0, 0.0, 4.0],	
                               [-2.0, 4.0, 4.0],	
                               [ 4.0, 0.0, 4.0 ]],
							 
                              [[ -4.0, 0.0, 0.0],	
                              [ -2.0, 4.0, 0.0],	
                              [  4.0, 0.0, 0.0 ]],
							  
                             [[  -4.0, 0.0, -4.0],	
                              [-2.0, 4.0, -4.0],	
                              [  4.0, 0.0, -4.0 ]]];


#This function is used to superimpose the control points over the curve
def DrawPoints():
    
  

    #Set point size larger to make more visible
    glPointSize(5.0);

    #Loop through all control points for this example
    glBegin(GL_POINTS);
    
    for i in range (0,nNumPoints,1):

        
        for j in range(0,3,1):

            glVertex3fv(ctrlPoints[i][j]);
    glEnd();
    



#Called to draw scene
def RenderScene():
    
    #Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT);

    #Save the modelview matrix stack
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();

    #Rotate the mesh around to make it easier to see
    glRotatef(45.0, 0.0, 1.0, 0.0);
    glRotatef(60.0, 1.0, 0.0, 0.0);

    #Sets up the Bezier
    #This actually only needs to be called once and could go in
    #the setup function
    glMap2f(GL_MAP2_VERTEX_3,	#Type of data generated
    0.0,						#Lower u range
    10.0,						#Upper u range
    #3,							#Distance between points in the data
    #3,							#Dimension in u direction (order)
    0.0,						#Lover v range
    10.0,						#Upper v range
    #9,							#Distance between points in the data
    #3,							#Dimension in v direction (order)
    ctrlPoints);		#array of control points

    #Enable the evaluator
    glEnable(GL_MAP2_VERTEX_3);

    #Use higher level functions to map to a grid, then evaluate the
    #entire thing.

    #Map a grid of 10 points from 0 to 10
    glMapGrid2f(10,0.0,10.0,10,0.0,10.0);

    #Evaluate the grid, using lines
    glEvalMesh2(GL_LINE,0,10,0,10);

    #Draw the Control Points
    DrawPoints();

    #Restore the modelview matrix
    glPopMatrix();

    #Dispalay the image
    glutSwapBuffers();
    

#This function does any needed initialization on the rendering
#context. 
def SetupRC():
    
    #Clear Window to white
    glClearColor(1.0, 1.0, 1.0, 1.0 );

    #Draw in Blue
    glColor3f(0.0, 0.0, 1.0);
    


def ChangeSize( w,  h):
    
    #Prevent a divide by zero
    if(h == 0):
        h = 1;

    #Set Viewport to window dimensions
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    glOrtho(-10.0, 10.0, -10.0, 10.0, -10.0, 10.0);

    #Modelview matrix reset
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    

glutInit();
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
glutInitWindowSize(800, 600);
glutCreateWindow("3D Bezier Surface");
glutReshapeFunc(ChangeSize);
glutDisplayFunc(RenderScene);
SetupRC();
glutMainLoop();

