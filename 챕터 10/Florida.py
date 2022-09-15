#Florida.c
#OpenGL SuperBible
#Demonstrates polygon tesselation
#Program by Richard S. Wright Jr.
#include "../../Common/OpenGLSB.h"	#System and OpenGL Stuff
#include "../../Common/GLTools.h"   #OpenGL Tools library
#include <math.h>
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Common.OpenGLCommon import *
from Common.TGACommon import *
#Nuke CALLBACK for everybody but Windows
#ifndef WIN32
#define CALLBACK
global CALLBACK
#endif


#/////////////////////////////////
#Coast Line Data
COAST_POINTS = 24
vCoast = [[-70.0, 30.0, 0.0 ],
                                    [-50.0, 30.0, 0.0 ],
                                    [-50.0, 27.0, 0.0 ],
                                    [ -5.0, 27.0, 0.0 ],
                                    [  0.0, 20.0, 0.0 ],
                                    [  8.0, 10.0, 0.0 ],
                                    [ 12.0,  5.0, 0.0 ],
                                    [ 10.0,  0.0, 0.0 ],
                                    [ 15.0,-10.0, 0.0 ],
                                    [ 20.0,-20.0, 0.0 ],
                                    [ 20.0,-35.0, 0.0 ],
                                    [ 10.0,-40.0, 0.0 ],
                                    [  0.0,-30.0, 0.0 ],
                                    [ -5.0,-20.0, 0.0 ],
                                    [-12.0,-10.0, 0.0 ],
                                    [-13.0, -5.0, 0.0 ],
                                    [-12.0,  5.0, 0.0 ],
                                    [-20.0, 10.0, 0.0 ],
                                    [-30.0, 20.0, 0.0 ],
                                    [-40.0, 15.0, 0.0 ],
                                    [-50.0, 15.0, 0.0 ],
                                    [-55.0, 20.0, 0.0 ],
                                    [-60.0, 25.0, 0.0 ],
                                    [-70.0, 25.0, 0.0 ]];

#Lake Okeechobee
LAKE_POINTS =4
vLake = [[ 10.0, -20.0, 0.0 ],
[ 15.0, -25.0, 0.0 ],
[ 10.0, -30.0, 0.0 ],
[  5.0, -25.0, 0.0 ]]


#Which Drawing Method
DRAW_LOOPS    =  0
DRAW_CONCAVE  =  1
DRAW_COMPLEX  =  2
iMethod = DRAW_LOOPS;   #Default, draw line loops

#////////////////////////////////////////////////////////////////////
#Reset flags as appropriate in response to menu selections
def ProcessMenu( value):
    global iMethod
    #Save menu identifier as method flag
    iMethod = value;
        
    #Trigger a redraw
    glutPostRedisplay();
    
    
#////////////////////////////////////////////////////////////////////
#Tesselation error callback
def tessError( error):
    
    #Get error message string
    szError = gluErrorString(error);
    
    #Set error message as window caption
    glutSetWindowTitle(szError);
    
    
#///////////////////////////////////////////////////
#Called to draw scene
def RenderScene():
    
    
      
    #Clear the window
    glClear(GL_COLOR_BUFFER_BIT);
         
    

    while True:

        
        if iMethod == DRAW_LOOPS:                    #Draw line loops
            
            glColor3f(0.0, 0.0, 0.0);    #Just black outline
            
            #Line loop with coastline shape
            glBegin(GL_LINE_LOOP);
            
            for i in range(0,COAST_POINTS,1):
                glVertex3dv(vCoast[i]);
            glEnd();

            #Line loop with shape of interior lake
            glBegin(GL_LINE_LOOP);
            
            for i in range (0,LAKE_POINTS,1):
                glVertex3dv(vLake[i]);
            glEnd();
            
            break;
            
        if iMethod == DRAW_CONCAVE:              #Tesselate concave polygon
            
            #Tesselator object
            GLUtesselator *pTess;
            
            #Green polygon
            glColor3f(0.0, 1.0, 0.0); 
            
            #Create the tesselator object
            pTess = gluNewTess();
            
            #Set callback functions
            #Just call glBegin at begining of triangle batch
            gluTessCallback(pTess, GLU_TESS_BEGIN, glBegin);
            
            #Just call glEnd at end of triangle batch
            gluTessCallback(pTess, GLU_TESS_END, glEnd);
            
            #Just call glVertex3dv for each  vertex
            gluTessCallback(pTess, GLU_TESS_VERTEX, glVertex3dv);
            
            #Register error callback
            gluTessCallback(pTess, GLU_TESS_ERROR, tessError);
            
            #Begin the polygon
            gluTessBeginPolygon(pTess, None);
            
            #Gegin the one and only contour
            gluTessBeginContour(pTess);

            #Feed in the list of vertices
            
            for i in range(0,COAST_POINTS,1):
                gluTessVertex(pTess, vCoast[i], vCoast[i]); #Can't be NULL
                
            #Close contour and polygon
            gluTessEndContour(pTess);
            gluTessEndPolygon(pTess);
            
            #All done with tesselator object
            gluDeleteTess(pTess);
            
            break;
    
        if iMethod == DRAW_COMPLEX:          #Tesselate, but with hole cut out
            
            #Tesselator object
            GLUtesselator *pTess;
            
            #Green polygon
            glColor3f(0.0, 1.0, 0.0); 

             #Create the tesselator object
            pTess = gluNewTess();
            
            #Set callback functions
            #Just call glBegin at begining of triangle batch
            gluTessCallback(pTess, GLU_TESS_BEGIN, glBegin);
            
            #Just call glEnd at end of triangle batch
            gluTessCallback(pTess, GLU_TESS_END, glEnd);
            
            #Just call glVertex3dv for each  vertex
            gluTessCallback(pTess, GLU_TESS_VERTEX, glVertex3dv);
            
            #Register error callback
            gluTessCallback(pTess, GLU_TESS_ERROR, tessError);

            #How to count filled and open areas
            gluTessProperty(pTess, GLU_TESS_WINDING_RULE, GLU_TESS_WINDING_ODD);
            
            #Begin the polygon
            gluTessBeginPolygon(pTess, None); #No user data
            
            #First contour, outline of state
            gluTessBeginContour(pTess);
            
            for i in range(0,COAST_POINTS,1):
                gluTessVertex(pTess, vCoast[i], vCoast[i]);
            gluTessEndContour(pTess);
            
            #Second contour, outline of lake
            gluTessBeginContour(pTess);
            
            for i in range(0,LAKE_POINTS,1):
                gluTessVertex(pTess, vLake[i], vLake[i]);
            gluTessEndContour(pTess);
            
            #All done with polygon
            gluTessEndPolygon(pTess);
            
            #No longer need tessellator object
            gluDeleteTess(pTess);            
            
            break;
        
        
    #Swap buffers
    glutSwapBuffers();
    


#This function does any needed initialization on the rendering
#context. Basically, just make a blue background
def SetupRC():
    
    #Blue background
    glClearColor(0.0, 0.0, 1.0, 1.0 );
    


#////////////////////////////////////////////////////////////////
#Reset projection
def ChangeSize( w,  h):
    
    #Prevent a divide by zero
    if(h == 0):
        h = 1;

    #Set Viewport to window dimensions
    glViewport(0, 0, w, h);

    #Reset projection matrix stack
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    #Establish clipping volume (left, right, bottom, top, near, far)
    gluOrtho2D(-80, 35, -50, 50);


    #Reset Model view matrix stack
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    

#//////////////////////////////////////////////////////////////////

glutInit();
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
glutInitWindowSize(500, 400);
glutCreateWindow("Tesselated Florida");

#Create the Menu
glutCreateMenu(ProcessMenu);
glutAddMenuEntry("Line Loops",DRAW_LOOPS);
glutAddMenuEntry("Concave Polygon",DRAW_CONCAVE);
glutAddMenuEntry("Complex Polygon",DRAW_COMPLEX);
glutAttachMenu(GLUT_RIGHT_BUTTON);

glutReshapeFunc(ChangeSize);
glutDisplayFunc(RenderScene);
SetupRC();
glutMainLoop();

