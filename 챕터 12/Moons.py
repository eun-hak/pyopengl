#Moons.cpp
#OpenGL SuperBible, 3rd Edition
#Richard S. Wright Jr.
#rwright@starstonesoftware.com

# include "../../Common/OpenGLSB.h"	#System and OpenGL Stuff


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLCommon import *
from TGACommon import *

#///////////////////////////////
#Define object names
EARTH	= 1
MARS	= 2
MOON1	= 3
MOON2	= 4


#///////////////////////////////////////////////////////////
#Just draw a sphere of some given radius
def DrawSphere( radius):

    #GLUquadricObj * pObj
    pObj = gluNewQuadric()
    gluQuadricNormals(pObj, GLU_SMOOTH)
    gluSphere(pObj, radius, 26, 13)
    gluDeleteQuadric(pObj)



#///////////////////////////////////////////////////////////
#Called to draw scene
def RenderScene():

    #Clear the window with current clearing color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #Save the matrix state and do the rotations
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    #Translate the whole scene out and into view
    glTranslatef(0.0, 0.0, -300.0)

    #Initialize the names stack
    glInitNames()
    glPushName(0)


    #Draw the Earth
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)
    glTranslatef(-100.0, 0.0, 0.0)
    glLoadName(EARTH)
    DrawSphere(30.0)

    #Draw the Moon
    glTranslatef(45.0, 0.0, 0.0)
    glColor3f(0.85, 0.85, 0.85)
    glPushName(MOON1)
    DrawSphere(5.0)
    glPopName()
    glPopMatrix()

    #Draw Mars
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(100.0, 0.0, 0.0)
    glLoadName(MARS)
    DrawSphere(20.0)

    #Draw Moon1
    glTranslatef(-40.0, 40.0, 0.0)
    glColor3f(0.85, 0.85, 0.85)
    glPushName(MOON1)
    DrawSphere(5.0)
    glPopName()

    #Draw Moon2
    glTranslatef(0.0, -80.0, 0.0)
    glPushName(MOON2)
    DrawSphere(5.0)
    glPopName()
    glPopMatrix()

    #Restore the matrix state
    glPopMatrix()
    #Modelview matrix

    glutSwapBuffers()



#///////////////////////////////////////////////////////////
#Parse the selection buffer to see which
#planet/moon was selected
def ProcessPlanet(pSelectBuff):

    global id, count
    
    cMessage = str("Error, no selection detected")

    #How many names on the name stack
    count = pSelectBuff[0]

    #Bottom of the name stack
    id = pSelectBuff[3]

    #Select on earth or mars, whichever was picked
    
    while True:

    
        if id == EARTH:
            cMessage = str( "You clicked Earth.")

        #If there is another name on the name stack,
        #then it must be the moon that was selected
        #This is what was actually clicked on
            if count == 2:
                cMessage = str( " - Specifically the moon.")

                break

        elif id == MARS:
            cMessage = str( "You clicked Mars.")

            #We know the name stack is only two deep. The precise
            #moon that was selected will be here.
            if count == 2:
        
                if pSelectBuff[4] == MOON1:
                    cMessage = str( " - Specifically Moon #1.")
                else:
                    str(cMessage, " - Specifically Moon #2.")
        
                break
    

    #Display the message about planet and moon selection
    glutSetWindowTitle(cMessage)



#///////////////////////////////////////////////////////////
#Process the selection, which is triggered by a right mouse
#click at(xPos, yPos).
UFFER_LENGTH =64
def ProcessSelection( xPos,  yPos):
    global UFFER_LENGTH
    global  fAspect
    #Screen aspect ratio

    #Space for selection buffer
    selectBuff = []*UFFER_LENGTH

    #Hit counter and viewport storeage
    global hits
    viewport = []*4
    #Setup selection buffer
    glSelectBuffer(UFFER_LENGTH, selectBuff)

    #Get the viewport
    glGetIntegerv(GL_VIEWPORT, viewport)

    #Switch to projection and save the matrix
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()

    #Change render mode
    glRenderMode(GL_SELECT)

    #Establish new clipping volume to be unit cube around
    #mouse cursor point(xPos, yPos) and extending two pixels
    #in the vertical and horzontal direction. Remember OpenGL specifies the
    #y coordinate from the bottom, Windows from the top. So windows position
    #(as measured from the top) subtract the height and you get it in terms
    #OpenGL Likes.
    glLoadIdentity()
    gluPickMatrix(xPos, viewport[3] - yPos, 2, 2, viewport)

    #Apply perspective matrix
    fAspect = viewport[2] / viewport[3]
    gluPerspective(45.0, fAspect, 1.0, 425.0)

    #Draw the scene
    RenderScene()

    #Collect the hits
    hits = glRenderMode(GL_RENDER)

    #If a single hit occured, display the info.
    if hits == 1:
        ProcessPlanet(selectBuff)
    else:
        glutSetWindowTitle("You clicked empty space!")

    #Restore the projection matrix
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    #Go back to modelview for normal rendering
    glMatrixMode(GL_MODELVIEW)



#///////////////////////////////////////////////////////////
#Process the mouse click
def MouseCallback(button,  state,  x,  y):

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        ProcessSelection(x, y)



#///////////////////////////////////////////////////////////
#This function does any needed initialization on the
#rendering context.
def SetupRC():

    #Lighting values
    dimLight = [0.1, 0.1, 0.1, 1.0]
    sourceLight = [0.65, 0.65, 0.65, 1.0]
    lightPos = [0.0, 0.0, 0.0, 1.0]

    #Light values and coordinates
    glEnable(GL_DEPTH_TEST)
    #Hidden surface removal
    glFrontFace(GL_CCW)
    #Counter clock-wise polygons face out
    glEnable(GL_CULL_FACE)
    #Do not calculate insides

    #Enable lighting
    glEnable(GL_LIGHTING)

    #Setup and enable light 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, dimLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, sourceLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glEnable(GL_LIGHT0)

    #Enable color tracking
    glEnable(GL_COLOR_MATERIAL)

    #Set Material properties to follow glColor values
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    #Gray background
    glClearColor(0.60, 0.60, 0.60, 1.0)



#///////////////////////////////////////////////////////////
#Window changed size, reset viewport and projection
def ChangeSize( w,  h):

    global fAspect
    #Screen aspect ratio

    #Prevent a divide by zero
    if(h == 0):
        h = 1

    #Set Viewport to window dimensions
    glViewport(0, 0, w, h)

    #Calculate aspect ratio of the window
    fAspect = w/h

    #Set the perspective coordinate system
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    #Field of view of 45 degrees, near and far planes 1.0 and 425
    gluPerspective(45.0, fAspect, 1.0, 425.0)

    #Modelview matrix reset
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



#///////////////////////////////////////////////////////////
#Entry point of the program

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Pick a Planet or Moon")
glutReshapeFunc(ChangeSize)
glutMouseFunc(MouseCallback)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()



