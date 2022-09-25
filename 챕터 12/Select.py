#Planets.c
#OpenGL SuperBible, 3rd Edition
#Richard S. Wright Jr.
#rwright@starstonesoftware.com
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *
from TGACommon import *
import math

#include "../../Common/OpenGLSB.h"	#System and OpenGL Stuff
#include <math.h>

class Rectangle:
    top= 0
    bottom= 0
    left= 0
    right= 0


# struct Rectangle
# 	{

# 	int top;
# 	int bottom;
# 	int left;
# 	int right;
# 	};


#///////////////////////////
#Object Names
TORUS  =1
SPHERE=	2
boundingRect =  Rectangle()


#struct Rectangle boundingRect;	#Bounding rectangle
selectedObject = 0	#Who is selected
global fAspect;					#Display aspect ratio


#if !defined(M_PI)
M_PI =3.14159265
#endif

#///////////////////////////////////////////////////////////
#Draw a torus (doughnut)  
#at z = 0... torus aligns with xy plane
def DrawTorus(numMajor,  numMinor):
    global M_PI
    majorRadius = 0.35;
    minorRadius = 0.15;
    majorStep = 2.0*M_PI / numMajor;
    minorStep = 2.0*M_PI / numMinor;
    global i, j;
    global c, r, z;

    glEnable(GL_NORMALIZE);

    for i in range(0,numMajor,1):
        a0 = i * majorStep;
        a1 = a0 + majorStep;
        x0 = math.cos(a0);
        y0 = math.sin(a0);
        x1 = math.cos(a1);
        y1 = math.sin(a1);

        glBegin(GL_TRIANGLE_STRIP);
       
        for j in range (0,numMinor,1):

            b = j * minorStep;
            c = math.cos(b);
            r = minorRadius * c + majorRadius;
            z = minorRadius * math.sin(b);

            glTexCoord2f(i/numMajor, j/numMinor);
            glNormal3f(x0*c, y0*c, z/minorRadius);
            glVertex3f(x0*r, y0*r, z);

            glTexCoord2f((i+1)/numMajor, j/numMinor);
            glNormal3f(x1*c, y1*c, z/minorRadius);
            glVertex3f(x1*r, y1*r, z);
            
        glEnd();
        
    glDisable(GL_NORMALIZE);
	


#///////////////////////////////////////////////////////////
#Just draw a sphere of some given radius
def DrawSphere( radius):
	
	#GLUquadricObj *pObj;
	pObj = gluNewQuadric();
	gluQuadricNormals(pObj, GLU_SMOOTH);
	gluSphere(pObj, radius, 26, 13);
	gluDeleteQuadric(pObj);
	

#
#///////////////////////////////////////////////////////////
#Render the torus and sphere
def DrawObjects():
	
	#Save the matrix state and do the rotations
	glMatrixMode(GL_MODELVIEW);
	glPushMatrix();

	#Translate the whole scene out and into view	
	glTranslatef(-0.75, 0.0, -2.5);	

	#Initialize the names stack
	glInitNames();
	glPushName(0);

	#Set material color, Yellow
	#torus
	glColor3f(1.0, 1.0, 0.0);
	glLoadName(TORUS);
	glPassThrough(TORUS);
	DrawTorus(40, 20);


	#Draw Sphere
	glColor3f(0.5, 0.0, 0.0);
	glTranslatef(1.5, 0.0, 0.0);
	glLoadName(SPHERE);
	glPassThrough(SPHERE);	
	DrawSphere(0.5);

	#Restore the matrix state
	glPopMatrix();	#Modelview matrix
	
	
#///////////////////////////////////////////////////////////
#Called to draw scene
def RenderScene():
	
    #Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    #Draw the objects in the scene
    DrawObjects();

    #If something is selected, draw a bounding box around it
    if(selectedObject != 0):

        
        viewport=[]*4

        #Get the viewport
        glGetIntegerv(GL_VIEWPORT, viewport);

        #Remap the viewing volume to match window coordinates (approximately)
        glMatrixMode(GL_PROJECTION);
        glPushMatrix();
        glLoadIdentity();

        #Establish clipping volume (left, right, bottom, top, near, far)
        glOrtho(viewport[0], viewport[2], viewport[3], viewport[1], -1, 1);
        glMatrixMode(GL_MODELVIEW);

        glDisable(GL_LIGHTING);
        glColor3f(1.0, 0.0, 0.0);
        glBegin(GL_LINE_LOOP);
        glVertex2i(boundingRect.left, boundingRect.top);
        glVertex2i(boundingRect.left, boundingRect.bottom);
        glVertex2i(boundingRect.right, boundingRect.bottom);
        glVertex2i(boundingRect.right, boundingRect.top);
        glEnd();
        glEnable(GL_LIGHTING);
    
    
    
    #### 인덴트 확인
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glMatrixMode(GL_MODELVIEW);

    glutSwapBuffers();
	



#///////////////////////////////////////////////////////////
#Go into feedback mode and draw a rectangle around the object
FEED_BUFF_SIZE	= 32768
def MakeSelection(nChoice):
	
    #Space for the feedback buffer
    feedBackBuff= []*FEED_BUFF_SIZE;

    #Storage for counters, etc.
    global size,i,j,count;

    #Initial minimum and maximum values
    boundingRect.right = boundingRect.bottom = -999999.0;
    boundingRect.left = boundingRect.top =  999999.0;

    #Set the feedback buffer
    glFeedbackBuffer(FEED_BUFF_SIZE,GL_2D, feedBackBuff);

    #Enter feedback mode
    glRenderMode(GL_FEEDBACK);

    #Redraw the scene
    DrawObjects();

    #Leave feedback mode
    size = glRenderMode(GL_RENDER);

    #Parse the feedback buffer and get the
    #min and max X and Y window coordinates
    i = 0;
    while(i < size):

        
        #Search for appropriate token
        if(feedBackBuff[i] == GL_PASS_THROUGH_TOKEN):

            if(feedBackBuff[i+1] ==nChoice):

            
                i+= 2;
                #Loop until next token is reached
                while(i < size and feedBackBuff[i] != GL_PASS_THROUGH_TOKEN):

                    
                    #Just get the polygons
                    if(feedBackBuff[i] == GL_POLYGON_TOKEN):
                    
                        #Get all the values for this polygon
                        count = feedBackBuff[++i]; #How many vertices
                        i+=1

                        #Loop for each vertex
                        for j in range(0,count,1):

                            
                            #Min and Max X
                            if(feedBackBuff[i] > boundingRect.right):
                                boundingRect.right = feedBackBuff[i];

                            if(feedBackBuff[i] < boundingRect.left):
                                boundingRect.left = feedBackBuff[i];
                            i+=1;

                            #Min and Max Y
                            if(feedBackBuff[i] > boundingRect.bottom):
                                boundingRect.bottom = feedBackBuff[i];

                            if(feedBackBuff[i] < boundingRect.top):
                                boundingRect.top = feedBackBuff[i];
                            i+=1
                        
                    
                else:
                    i+=1	#Get next index and keep looking

                break;
            
        i+=1

	


#///////////////////////////////////////////////////////////
#Process the selection, which is triggered by a right mouse
#click at (xPos, yPos).

def ProcessSelection(xPos,  yPos):
    global fAspect
    BUFFER_LENGTH = 64
    #Space for selection buffer
    selectBuff = []*BUFFER_LENGTH;

    #Hit counter and viewport storage
    global hits
    viewport = []*4;

    #Setup selection buffer
    glSelectBuffer(BUFFER_LENGTH);

    #Get the viewport
    #glGetIntegerv(GL_VIEWPORT , viewport);
    #glGetIntegerv(GL_VIEWPORT)
    viewport = glGetIntegerv(GL_VIEWPORT)
    #Switch to projection and save the matrix
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();

    #Change render mode
    glRenderMode(GL_SELECT);

    #Establish new clipping volume to be unit cube around
    #mouse cursor point (xPos, yPos) and extending two pixels
    #in the vertical and horizontal direction
    glLoadIdentity();
    gluPickMatrix(xPos, viewport[3] - yPos, 2,2, viewport);

    #Apply perspective matrix 
    gluPerspective(60.0, fAspect, 1.0, 425.0);

    #Draw the scene
    DrawObjects();

    #Collect the hits
    hits = glRenderMode(GL_RENDER);

    #Restore the projection matrix
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();

    #Go back to modelview for normal rendering
    glMatrixMode(GL_MODELVIEW);

    #If a single hit occurred, display the info.
    if(hits == 1):
        
        MakeSelection(selectBuff[3]);
        if(selectedObject == selectBuff[3]):
            selectedObject = 0;
        else:
            selectedObject = selectBuff[3];
        

    glutPostRedisplay();
	



#///////////////////////////////////////////////////////////
#This function does any needed initialization on the rendering
#context.  Here it sets up and initializes the lighting for
#the scene.
def SetupRC():
	
	#Lighting values
	dimLight =  [0.1, 0.1, 0.1, 1.0 ]
	sourceLight =  [0.65, 0.65, 0.65, 1.0 ]
	lightPos =  [0.0, 0.0, 0.0, 1.0 ]

	#Light values and coordinates
	glEnable(GL_DEPTH_TEST);	#Hidden surface removal
	glFrontFace(GL_CCW);		#Counter clock-wise polygons face out
	#//glEnable(GL_CULL_FACE);		#Do not calculate insides

	#Enable lighting
	glEnable(GL_LIGHTING);

	#Setup and enable light 0
	glLightfv(GL_LIGHT0,GL_AMBIENT,dimLight);
	glLightfv(GL_LIGHT0,GL_DIFFUSE,sourceLight);
	glLightfv(GL_LIGHT0,GL_POSITION,lightPos);
	glEnable(GL_LIGHT0);

	#Enable color tracking
	glEnable(GL_COLOR_MATERIAL);
	
	#Set Material properties to follow glColor values
	glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);

	#Gray background
	glClearColor(0.60, 0.60, 0.60, 1.0 );
	glLineWidth(2.0);
	


#///////////////////////////////////////////////////////////
#Set viewport and projection
def ChangeSize( w,  h):
    global fAspect
    #Prevent a divide by zero
    if(h == 0):
        h = 1;

    #Set Viewport to window dimensions
    glViewport(0, 0, w, h);

    #Calculate aspect ratio of the window
    fAspect = w/h;

    #Set the perspective coordinate system
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    #Field of view of 45 degrees, near and far planes 1.0 and 425
    gluPerspective(60.0, fAspect, 1.0, 425.0);

    #Modelview matrix reset
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
	

#//////////////////////////////////////////////////////////
#Process the mouse click
def MouseCallback( button,  state,  x,  y):
	
	if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
		ProcessSelection(x, y);
	

#///////////////////////////////////////////////////////////
#Program entry point

glutInit();
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
glutInitWindowSize(800,600);
glutCreateWindow("Select an Object");
glutReshapeFunc(ChangeSize);
glutMouseFunc(MouseCallback);
glutDisplayFunc(RenderScene);
SetupRC();
glutMainLoop();

