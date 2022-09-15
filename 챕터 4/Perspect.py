from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
global nRange
xRot = 0.0
yRot = 0.0
GL_PI = 3.1415



def ChangeSize(w,h):
    global fAspect

    if(h == 0):
        h = 1;
    glViewport(0, 0, w, h)
    fAspect = w/h

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, fAspect, 1.0, 400.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    

def SetupRC():
    whiteLight = [0.45, 0.45, 0.45, 1.0]
    sourceLight = [0.25, 0.25, 0.25, 1.0]
    lightPos = [-50.0, 25.0, 250.0, 0.0]
    # GLfloat  whiteLight[] = { 0.45f, 0.45f, 0.45f, 1.0f }
    # GLfloat  sourceLight[] = { 0.25f, 0.25f, 0.25f, 1.0f }
    # GLfloat	 lightPos[] = { -50.f, 25.0f, 250.0f, 0.0f }

    glEnable(GL_DEPTH_TEST)
    glFrontFace(GL_CCW)
    glEnable(GL_CULL_FACE)

    glEnable(GL_LIGHTING)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, whiteLight)
    glLightfv(GL_LIGHT0, GL_AMBIENT, sourceLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, sourceLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glClearColor(0.0, 0.0, 0.0, 1.0)
def SpecialKeys(key, x, y):
    global xRot
    global yRot

    if(key == GLUT_KEY_UP):
        xRot -= 5.0

    if(key == GLUT_KEY_DOWN):
        xRot += 5.0

    if(key == GLUT_KEY_LEFT):
        yRot -= 5.0

    if(key == GLUT_KEY_RIGHT):
        yRot += 5.0
        # 이 밑에 2개가 if 쪽인지 아닌지
    xRot = xRot % 360
    yRot = yRot % 360

    glutPostRedisplay()


def RenderScene():
    global fZ
    global bZ

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    fZ = 100.0
    bZ = -100.0

    glPushMatrix()
    glTranslatef(0.0, 0.0, -300.0)
    glRotatef(xRot, 1.0, 0.0, 0.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)

    glColor3f(1.0, 0.0, 0.0)

    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, 1.0)

    glVertex3f(-50.0, 50.0, fZ)
    glVertex3f(-50.0, -50.0, fZ)
    glVertex3f(-35.0, -50.0, fZ)
    glVertex3f(-35.0, 50.0, fZ)

    glVertex3f(50.0, 50.0, fZ)
    glVertex3f(35.0, 50.0, fZ)
    glVertex3f(35.0, -50.0, fZ)
    glVertex3f(50.0, -50.0, fZ)

    glVertex3f(-35.0, 50.0, fZ)
    glVertex3f(-35.0, 35.0, fZ)
    glVertex3f(35.0, 35.0, fZ)
    glVertex3f(35.0, 50.0, fZ)

    glVertex3f(-35.0, -35.0, fZ)
    glVertex3f(-35.0, -50.0, fZ)
    glVertex3f(35.0, -50.0, fZ)
    glVertex3f(35.0, -35.0, fZ)

    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-50.0, 50.0, fZ)
    glVertex3f(50.0, 50.0, fZ)
    glVertex3f(50.0, 50.0, bZ)
    glVertex3f(-50.0, 50.0, bZ)

    glNormal3f(0., -1.0, 0.0)
    glVertex3f(-50.0, -50.0, fZ)
    glVertex3f(-50.0, -50.0, bZ)
    glVertex3f(50.0, -50.0, bZ)
    glVertex3f(50.0, -50.0, fZ)

    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(50.0, 50.0, fZ)
    glVertex3f(50.0, -50.0, fZ)
    glVertex3f(50.0, -50.0, bZ)
    glVertex3f(50.0, 50.0, bZ)

    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-50.0, 50.0, fZ)
    glVertex3f(-50.0, 50.0, bZ)
    glVertex3f(-50.0, -50.0, bZ)
    glVertex3f(-50.0, -50.0, fZ)
    glEnd()

    glFrontFace(GL_CW)

    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, -1.0)

    glVertex3f(-50.0, 50.0, bZ)
    glVertex3f(-50.0, -50.0, bZ)
    glVertex3f(-35.0, -50.0, bZ)
    glVertex3f(-35.0, 50.0, bZ)

    glVertex3f(50.0, 50.0, bZ)
    glVertex3f(35.0, 50.0, bZ)
    glVertex3f(35.0, -50.0, bZ)
    glVertex3f(50.0, -50.0, bZ)

    glVertex3f(-35.0, 50.0, bZ)
    glVertex3f(-35.0, 35.0, bZ)
    glVertex3f(35.0, 35.0, bZ)
    glVertex3f(35.0, 50.0, bZ)

    glVertex3f(-35.0, -35.0, bZ)
    glVertex3f(-35.0, -50.0, bZ)
    glVertex3f(35.0, -50.0, bZ)
    glVertex3f(35.0, -35.0, bZ)

    glColor3f(0.75, 0.75, 0.75)

    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-35.0, 35.0, fZ)
    glVertex3f(35.0, 35.0, fZ)
    glVertex3f(35.0, 35.0, bZ)
    glVertex3f(-35.0, 35.0, bZ)

    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-35.0, -35.0, fZ)
    glVertex3f(-35.0, -35.0, bZ)
    glVertex3f(35.0, -35.0, bZ)
    glVertex3f(35.0, -35.0, fZ)

    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(-35.0, 35.0, fZ)
    glVertex3f(-35.0, 35.0, bZ)
    glVertex3f(-35.0, -35.0, bZ)
    glVertex3f(-35.0, -35.0, fZ)

    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(35.0, 35.0, fZ)
    glVertex3f(35.0, -35.0, fZ)
    glVertex3f(35.0, -35.0, bZ)
    glVertex3f(35.0, 35.0, bZ)
    glEnd()

    glFrontFace(GL_CCW)

    glPopMatrix()

    glutSwapBuffers()




glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow("Perspective Projection")
glutReshapeFunc(ChangeSize)
glutSpecialFunc(SpecialKeys)
glutDisplayFunc(RenderScene)
SetupRC()
glutMainLoop()
    
  
    
  