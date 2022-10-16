from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Radians are king... but we need a way to swap back and forth
GLT_PI = 3.14159265358979323846
GLT_PI_DIV_180 = 0.017453292519943296
GLT_INV_PI_DIV_180 = 57.2957795130823229
def gltDegToRad(x): return ((x)*GLT_PI_DIV_180)
def gltRadToDeg(x): return ((x)*GLT_INV_PI_DIV_180)

###########################################
######## GLTools.h Data Struct Type
###########################################
# Two component floating point vector
class GLTVector2:
    def __init__(self): self.value = [0.0, 0.0]


# Three component floating point vector
class GLTVector3:
    def __init__(self): self.value = [0.0, 0.0, 0.0]


# Four component floating point vector
class GLTVector4:
    def __init__(self): self.value = [0.0, 0.0, 0.0, 0.0]


# A column major 4x4 matrix of type GLfloat
class GLTMatrix:
    def __init__(self):
        self.value = [
            0.0, 0.0, 0.0, 0.0
            , 0.0, 0.0, 0.0, 0.0
            , 0.0, 0.0, 0.0, 0.0
            , 0.0, 0.0, 0.0, 0.0
        ]

    def setValue2DArray(self, array_):
        for i in range(4):
            for j in range(4):
                self.value[i * 4 + j] = array_[i][j]

class GLTVectorMatrix:
    def __init__(self):
        self.value = [
            0.0, 0.0, 0.0, 0.0
            , 0.0, 0.0, 0.0, 0.0
            , 0.0, 0.0, 0.0, 0.0
            , 0.0, 0.0, 0.0, 0.0
        ]


# The Frame of reference container
class GLTFrame:
    def __init__(self):
        self.vLocation = GLTVector3()
        self.vUp = GLTVector3()
        self.vForward = GLTVector3()


###########################################
######## FrameMath.c
###########################################

# Initialize a frame of reference.
# Uses default OpenGL viewing position and orientation
def gltInitFrame(pFrame: GLTFrame):
    pFrame.vLocation.value[0] = 0.0
    pFrame.vLocation.value[1] = 0.0
    pFrame.vLocation.value[2] = 0.0

    pFrame.vUp.value[0] = 0.0
    pFrame.vUp.value[1] = 1.0
    pFrame.vUp.value[2] = 0.0

    pFrame.vForward.value[0] = 0.0
    pFrame.vForward.value[1] = 0.0
    pFrame.vForward.value[2] = -1.0


# Derives a 4x4 transformation matrix from a frame of reference
def gltGetMatrixFromFrame(pFrame: GLTFrame, mMatrix: GLTVectorMatrix):
    # Derived X Axis
    vXAxis = GLTVector3()

    # Calculate X Axis
    gltVectorCrossProduct(pFrame.vUp, pFrame.vForward, vXAxis)
    # Just populate the matrix
    # X column vector
    # memcpy(mMatrix, vXAxis, sizeof(GLTVector3))
    mMatrix.value[0: 3] = vXAxis.value
    mMatrix.value[3] = 0.0

    # y column vector
    # memcpy(mMatrix+4, pFrame.vUp, sizeof(GLTVector3))
    mMatrix.value[4: 7] = pFrame.vUp.value
    mMatrix.value[7] = 0.0

    # z column vector
    # memcpy(mMatrix+8, pFrame.vForward, sizeof(GLTVector3))
    mMatrix.value[8: 11] = pFrame.vForward.value
    mMatrix.value[11] = 0.0

    #Translation / Location vector
    # memcpy(mMatrix+12, pFrame.vLocation, sizeof(GLTVector3))
    mMatrix.value[12: 15] = pFrame.vLocation.value
    mMatrix.value[15] = 1.0

# Apply an actors transform given it's frame of reference
def gltApplyActorTransform(pFrame: GLTFrame):
    mTransform = GLTMatrix()
    gltGetMatrixFromFrame(pFrame, mTransform)
    glMultMatrixf(mTransform.value)


# Apply a camera transform given a frame of reference. This is
# pretty much just an alternate implementation of gluLookAt using
# floats instead of doubles and having the forward vector specified
# instead of a point out in front of me.
def gltApplyCameraTransform(pCamera: GLTFrame):
    mMatrix = GLTMatrix()
    vAxisX = GLTVector3()
    zFlipped = GLTVector3()

    zFlipped.value[0] = -pCamera.vForward.value[0]
    zFlipped.value[1] = -pCamera.vForward.value[1]
    zFlipped.value[2] = -pCamera.vForward.value[2]

    # Derive X vector
    gltVectorCrossProduct(pCamera.vUp, zFlipped, vAxisX)

    # Populate matrix, note this is just the rotation and is transposed
    mMatrix.value[0] = vAxisX.value[0]
    mMatrix.value[4] = vAxisX.value[1]
    mMatrix.value[8] = vAxisX.value[2]
    mMatrix.value[12] = 0.0

    mMatrix.value[1] = pCamera.vUp.value[0]
    mMatrix.value[5] = pCamera.vUp.value[1]
    mMatrix.value[9] = pCamera.vUp.value[2]
    mMatrix.value[13] = 0.0

    mMatrix.value[2] = zFlipped.value[0]
    mMatrix.value[6] = zFlipped.value[1]
    mMatrix.value[10] = zFlipped.value[2]
    mMatrix.value[14] = 0.0

    mMatrix.value[3] = 0.0
    mMatrix.value[7] = 0.0
    mMatrix.value[11] = 0.0
    mMatrix.value[15] = 1.0

    # Do the rotation first
    glMultMatrixf(mMatrix.value)
    # Now, translate backwards
    glTranslatef(-pCamera.vLocation.value[0], -pCamera.vLocation.value[1], -pCamera.vLocation.value[2])


# March a frame of reference forward. This simply moves
# the location forward along the forward vector.
def gltMoveFrameForward(pFrame: GLTFrame, fStep: float):
    pFrame.vLocation.value[0] += pFrame.vForward.value[0] * fStep
    pFrame.vLocation.value[1] += pFrame.vForward.value[1] * fStep
    pFrame.vLocation.value[2] += pFrame.vForward.value[2] * fStep


# Move a frame of reference up it's local Y axis
def gltMoveFrameUp(pFrame: GLTFrame, fStep: float):
    pFrame.vLocation.value[0] += pFrame.vUp.value[0] * fStep
    pFrame.vLocation.value[1] += pFrame.vUp.value[1] * fStep
    pFrame.vLocation.value[2] += pFrame.vUp.value[2] * fStep


# Move a frame of reference along it's local X axis
def gltMoveFrameRight(pFrame: GLTFrame, fStep: float):
    vCross = GLTVector3()
    gltVectorCrossProduct(pFrame.vUp, pFrame.vForward, vCross)
    pFrame.vLocation.value[0] += vCross.value[0] * fStep
    pFrame.vLocation.value[1] += vCross.value[1] * fStep
    pFrame.vLocation.value[2] += vCross.value[2] * fStep


# Translate a frame in world coordinates
def gltTranslateFrameWorld(pFrame: GLTFrame, x: float, y: float, z: float):
    pFrame.vLocation.value[0] += x
    pFrame.vLocation.value[1] += y
    pFrame.vLocation.value[2] += z


# Translate a frame in local coordinates
def gltTranslateFrameLocal(pFrame: GLTFrame, x: float, y: float, z: float):
    gltMoveFrameRight(pFrame, x)
    gltMoveFrameUp(pFrame, y)
    gltMoveFrameForward(pFrame, z)


# Rotate a frame around it's local Y axis
def gltRotateFrameLocalY(pFrame: GLTFrame, fAngle: float):
    mRotation = GLTMatrix()
    vNewForward = GLTVector3()

    gltRotationMatrix(float(gltDegToRad(fAngle)), 0.0, 1.0, 0.0, mRotation)
    gltRotationMatrix(fAngle, pFrame.vUp.value[0], pFrame.vUp.value[1], pFrame.vUp.value[2], mRotation)

    gltRotateVector(pFrame.vForward, mRotation, vNewForward)
    # memcpy(pFrame.vForward, vNewForward, sizeof(GLTVector3))
    pFrame.vForward.value[0: 3] = vNewForward.value


#  Rotate a frame around it's local X axis
def gltRotateFrameLocalX(pFrame: GLTFrame, fAngle: float):
    mRotation = GLTMatrix()
    vCross = GLTVector3()

    gltVectorCrossProduct(vCross, pFrame.vUp, pFrame.vForward)
    gltRotationMatrix(fAngle, vCross.value[0], vCross.value[1], vCross.value[2], mRotation)

    vNewVect = GLTVector3()
    # Inline 3x3 matrix multiply for rotation only
    vNewVect.value[0] = mRotation.value[0] * pFrame.vForward.value[0] + mRotation.value[4] * pFrame.vForward.value[1] + mRotation.value[8] * \
                  pFrame.vForward.value[2]
    vNewVect.value[1] = mRotation.value[1] * pFrame.vForward.value[0] + mRotation.value[5] * pFrame.vForward.value[1] + mRotation.value[9] * \
                  pFrame.vForward.value[2]
    vNewVect.value[2] = mRotation.value[2] * pFrame.vForward.value[0] + mRotation.value[6] * pFrame.vForward.value[1] + mRotation.value[10] * \
                  pFrame.vForward.value[2]
    # memcpy(pFrame.vForward, vNewVect, sizeof(GLfloat)*3)
    vNewVext = pFrame.vForward.value[0: 3]

    # Update pointing up vector
    vNewVect.value[0] = mRotation.value[0] * pFrame.vUp.value[0] + mRotation.value[4] * pFrame.vUp.value[1] + mRotation.value[8] * pFrame.vUp.value[2]
    vNewVect.value[1] = mRotation.value[1] * pFrame.vUp.value[0] + mRotation.value[5] * pFrame.vUp.value[1] + mRotation.value[9] * pFrame.vUp.value[2]
    vNewVect.value[2] = mRotation.value[2] * pFrame.vUp.value[0] + mRotation.value[6] * pFrame.vUp.value[1] + mRotation.value[10] * pFrame.vUp.value[2]
    # memcpy(pFrame.vUp, vNewVect, sizeof(GLfloat) * 3)
    pFrame.vUp.value[0: 3] = vNewVext.value


# Rotate a frame around it's local Z axis
def gltRotateFrameLocalZ(pFrame: GLTFrame, fAngle: GLfloat):
    mRotation = GLTMatrix()

    # Only the up vector needs to be rotated
    gltRotationMatrix(fAngle, pFrame.vForward.value[0], pFrame.vForward.value[1], pFrame.vForward.value[2], mRotation)

    vNewVect = GLTVector3()
    vNewVect.value[0] = mRotation.value[0] * pFrame.vUp.value[0] + mRotation.value[4] * pFrame.vUp.value[1] + mRotation.value[8] * pFrame.vUp.value[2]
    vNewVect.value[1] = mRotation.value[1] * pFrame.vUp.value[0] + mRotation.value[5] * pFrame.vUp.value[1] + mRotation.value[9] * pFrame.vUp.value[2]
    vNewVect.value[2] = mRotation.value[2] * pFrame.vUp.value[0] + mRotation.value[6] * pFrame.vUp.value[1] + mRotation.value[10] * pFrame.vUp.value[2]
    # memcpy(pFrame.vUp, vNewVect, sizeof(GLfloat) * 3)
    pFrame.vUp.value[0: 3] = vNewVext


###########################################
######## MatrixMath.c
###########################################

# Load a matrix with the Idenity matrix
def gltLoadIdentityMatrix(m: GLTMatrix):
    identity = GLTMatrix()
    identity.value = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    ]

    # memcpy(m, identity, sizeof(GLTMatrix))
    m = identity


# Multiply two 4x4 matricies. Assumes normal OpenGL column major ordering
def gltMultiplyMatrix(m1: GLTMatrix, m2: GLTMatrix, mProduct: GLTMatrix):
    mProduct.value[0] = m1.value[0] * m2.value[0] + m1.value[4] * m2.value[1] + m1.value[8] * m2.value[2] + m1.value[12] * m2.value[3]
    mProduct.value[4] = m1.value[0] * m2.value[4] + m1.value[4] * m2.value[5] + m1.value[8] * m2.value[6] + m1.value[12] * m2.value[7]
    mProduct.value[8] = m1.value[0] * m2.value[8] + m1.value[4] * m2.value[9] + m1.value[8] * m2.value[10] + m1.value[12] * m2.value[11]
    mProduct.value[12] = m1.value[0] * m2.value[12] + m1.value[4] * m2.value[13] + m1.value[8] * m2.value[14] + m1.value[12] * m2.value[15]

    mProduct.value[1] = m1.value[1] * m2.value[0] + m1.value[5] * m2.value[1] + m1.value[9] * m2.value[2] + m1.value[13] * m2.value[3]
    mProduct.value[5] = m1.value[1] * m2.value[4] + m1.value[5] * m2.value[5] + m1.value[9] * m2.value[6] + m1.value[13] * m2.value[7]
    mProduct.value[9] = m1.value[1] * m2.value[8] + m1.value[5] * m2.value[9] + m1.value[9] * m2.value[10] + m1.value[13] * m2.value[11]
    mProduct.value[13] = m1.value[1] * m2.value[12] + m1.value[5] * m2.value[13] + m1.value[9] * m2.value[14] + m1.value[13] * m2.value[15]

    mProduct.value[2] = m1.value[2] * m2.value[0] + m1.value[6] * m2.value[1] + m1.value[10] * m2.value[2] + m1.value[14] * m2.value[3]
    mProduct.value[6] = m1.value[2] * m2.value[4] + m1.value[6] * m2.value[5] + m1.value[10] * m2.value[6] + m1.value[14] * m2.value[7]
    mProduct.value[10] = m1.value[2] * m2.value[8] + m1.value[6] * m2.value[9] + m1.value[10] * m2.value[10] + m1.value[14] * m2.value[11]
    mProduct.value[14] = m1.value[2] * m2.value[12] + m1.value[6] * m2.value[13] + m1.value[10] * m2.value[14] + m1.value[14] * m2.value[15]

    mProduct.value[3] = m1.value[3] * m2.value[0] + m1.value[7] * m2.value[1] + m1.value[11] * m2.value[2] + m1.value[15] * m2.value[3]
    mProduct.value[7] = m1.value[3] * m2.value[4] + m1.value[7] * m2.value[5] + m1.value[11] * m2.value[6] + m1.value[15] * m2.value[7]
    mProduct.value[11] = m1.value[3] * m2.value[8] + m1.value[7] * m2.value[9] + m1.value[11] * m2.value[10] + m1.value[15] * m2.value[11]
    mProduct.value[15] = m1.value[3] * m2.value[12] + m1.value[7] * m2.value[13] + m1.value[11] * m2.value[14] + m1.value[15] * m2.value[15]


# Create a translation matrix
def gltTranslationMatrix(x: float, y: float, z: float, mTranslate: GLTMatrix):
    gltLoadIdentityMatrix(mTranslate)
    mTranslate.value[12] = x
    mTranslate.value[13] = y
    mTranslate.value[14] = z


# Create a scaling matrix
def gltScalingMatrix(x: float, y: float, z: float, mScale: GLTMatrix):
    gltLoadIdentityMatrix(mScale)
    mScale.value[0] = x
    mScale.value[5] = y
    mScale.value[11] = z


# Creates a 4x4 rotation matrix, takes radians NOT degrees
def gltRotationMatrix(angle: float, x: float, y: float, z: float, mMatrix: GLTMatrix):
    vecLength, sinSave, cosSave, oneMinusCos = 0.0, 0.0, 0.0, 0.0
    xx, yy, zz, xy, yz, zx, xs, ys, zs = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    # If NULL vector passed in, this will blow up...
    if x == 0.0 and y == 0.0 and z == 0.0:
        gltLoadIdentityMatrix(mMatrix)
        return

    # Scale vector
    vecLength = float(math.sqrt(x * x + y * y + z * z))

    # Rotation matrix is normalized
    x /= vecLength
    y /= vecLength
    z /= vecLength

    sinSave = float(math.sin(angle))
    cosSave = float(math.cos(angle))
    oneMinusCos = 1.0 - cosSave

    xx = x * x
    yy = y * y
    zz = z * z
    xy = x * y
    yz = y * z
    zx = z * x
    xs = x * sinSave
    ys = y * sinSave
    zs = z * sinSave

    mMatrix.value[0] = (oneMinusCos * xx) + cosSave
    mMatrix.value[4] = (oneMinusCos * xy) - zs
    mMatrix.value[8] = (oneMinusCos * zx) + ys
    mMatrix.value[12] = 0.0

    mMatrix.value[1] = (oneMinusCos * xy) + zs
    mMatrix.value[5] = (oneMinusCos * yy) + cosSave
    mMatrix.value[9] = (oneMinusCos * yz) - xs
    mMatrix.value[13] = 0.0

    mMatrix.value[2] = (oneMinusCos * zx) - ys
    mMatrix.value[6] = (oneMinusCos * yz) + xs
    mMatrix.value[10] = (oneMinusCos * zz) + cosSave
    mMatrix.value[14] = 0.0

    mMatrix.value[3] = 0.0
    mMatrix.value[7] = 0.0
    mMatrix.value[11] = 0.0
    mMatrix.value[15] = 1.0


# Creates a shadow projection matrix out of the plane equation
# coefficients and the position of the light. The return value is stored
# in destMat
# def gltMakeShadowMatrix(GLTVector3 vPoints.value[3], GLTVector4 vLightPos, GLTMatrix destMat)
def gltMakeShadowMatrix(vPoints: GLTVector3, vLightPos: GLTVector4, destMat: GLTMatrix):
    vPlaneEquation = GLTVector4()
    dot = 0.0

    gltGetPlaneEquation(vPoints[0], vPoints[1], vPoints[2], vPlaneEquation)

    # Dot product of plane and light position
    dot = (
        vPlaneEquation.value[0] * vLightPos.value[0] +
        vPlaneEquation.value[1] * vLightPos.value[1] +
        vPlaneEquation.value[2] * vLightPos.value[2] +
        vPlaneEquation.value[3] * vLightPos.value[3]
    )

    # Now do the projection
    # First column
    destMat.value[0] = dot - vLightPos.value[0] * vPlaneEquation.value[0]
    destMat.value[4] = 0.0 - vLightPos.value[0] * vPlaneEquation.value[1]
    destMat.value[8] = 0.0 - vLightPos.value[0] * vPlaneEquation.value[2]
    destMat.value[12] = 0.0 - vLightPos.value[0] * vPlaneEquation.value[3]

    # Second column
    destMat.value[1] = 0.0 - vLightPos.value[1] * vPlaneEquation.value[0]
    destMat.value[5] = dot - vLightPos.value[1] * vPlaneEquation.value[1]
    destMat.value[9] = 0.0 - vLightPos.value[1] * vPlaneEquation.value[2]
    destMat.value[13] = 0.0 - vLightPos.value[1] * vPlaneEquation.value[3]

    # Third Column
    destMat.value[2] = 0.0 - vLightPos.value[2] * vPlaneEquation.value[0]
    destMat.value[6] = 0.0 - vLightPos.value[2] * vPlaneEquation.value[1]
    destMat.value[10] = dot - vLightPos.value[2] * vPlaneEquation.value[2]
    destMat.value[14] = 0.0 - vLightPos.value[2] * vPlaneEquation.value[3]

    # Fourth Column
    destMat.value[3] = 0.0 - vLightPos.value[3] * vPlaneEquation.value[0]
    destMat.value[7] = 0.0 - vLightPos.value[3] * vPlaneEquation.value[1]
    destMat.value[11] = 0.0 - vLightPos.value[3] * vPlaneEquation.value[2]
    destMat.value[15] = dot - vLightPos.value[3] * vPlaneEquation.value[3]


# Transpose the matrix in place
def gltTransposeMatrix(mTranspose: GLTMatrix):
    temp = 0.0

    temp = mTranspose.value[1]
    mTranspose.value[1] = mTranspose.value[4]
    mTranspose.value[4] = temp

    temp = mTranspose.value[2]
    mTranspose.value[2] = mTranspose.value[8]
    mTranspose.value[8] = temp

    temp = mTranspose.value[3]
    mTranspose.value[3] = mTranspose.value[12]
    mTranspose.value[12] = temp

    temp = mTranspose.value[6]
    mTranspose.value[6] = mTranspose.value[9]
    mTranspose.value[9] = temp

    temp = mTranspose.value[7]
    mTranspose.value[7] = mTranspose.value[13]
    mTranspose.value[13] = temp

    temp = mTranspose.value[11]
    mTranspose.value[11] = mTranspose.value[14]
    mTranspose.value[14] = temp


# This function is not exported by library, just for this modules use only
# 3x3 determinant
def DetIJ(m: GLTMatrix, i: int, j: int) -> float:
    x, y, ii, jj = 0, 0, 0, 0
    ret = 0.0
    mat = [
        0.0, 0.0, 0.0
        , 0.0, 0.0, 0.0
        , 0.0, 0.0, 0.0
    ]
    x = 0
    for ii in range(4):
        if ii == i: continue
        y = 0
        for jj in range(4):
            if jj == j: continue
            mat[x][y] = m[(ii * 4) + jj]
            y += 1
        x += 1

    ret = mat[0][0] * (mat[1][1] * mat[2][2] - mat[2][1] * mat[1][2])
    ret -= mat[0][1] * (mat[1][0] * mat[2][2] - mat[2][0] * mat[1][2])
    ret += mat[0][2] * (mat[1][0] * mat[2][1] - mat[2][0] * mat[1][1])

    return ret


# Invert matrix
def gltInvertMatrix(m: GLTMatrix, mInverse: GLTMatrix):
    i, j = 0, 0
    det, detij = 0.0, 0.0

    # calculate 4x4 determinant
    det = 0.0
    for i in range(4):
        det += (-m.value[i] * DetIJ(m, 0, i)) if (i & 0x1) else (m.value[i] * DetIJ(m, 0, i))

    det = 1.0 / det

    # calculate inverse
    for i in range(4):
        for j in range(4):
            detij = DetIJ(m, j, i)
            mInverse.value[(i * 4) + j] = (-detij * det) if ((i + j) & 0x1) else (detij * det)

###########################################
######## VectorMath.c
###########################################

# Adds two vectors together
def gltAddVectors(vFirst: GLTVector3, vSecond: GLTVector3, vResult: GLTVector3):
    vResult.value[0] = vFirst.value[0] + vSecond.value[0]
    vResult.value[1] = vFirst.value[1] + vSecond.value[1]
    vResult.value[2] = vFirst.value[2] + vSecond.value[2]


# Subtract one vector from another
def gltSubtractVectors(vFirst: GLTVector3, vSecond: GLTVector3, vResult: GLTVector3):
    vResult.value[0] = vFirst.value[0] - vSecond.value[0]
    vResult.value[1] = vFirst.value[1] - vSecond.value[1]
    vResult.value[2] = vFirst.value[2] - vSecond.value[2]


# Scales a vector by a scalar
def gltScaleVector(vVector: GLTVector3, fScale: GLfloat):
    vVector.value[0] *= fScale
    vVector.value[1] *= fScale
    vVector.value[2] *= fScale


# Gets the length of a vector squared
def gltGetVectorLengthSqrd(vVector: GLTVector3) -> float:
    return (vVector.value[0] * vVector.value[0]) + (vVector.value[1] * vVector.value[1]) + (vVector.value[2] * vVector.value[2])


# Gets the length of a vector
def gltGetVectorLength(vVector: GLTVector3) -> float:
    return math.sqrt(gltGetVectorLengthSqrd(vVector))


# Scales a vector by it's length - creates a unit vector
def gltNormalizeVector(vNormal: GLTVector3):
    fLength = 1.0 / gltGetVectorLength(vNormal)
    gltScaleVector(vNormal, fLength)


# Copies a vector
def gltCopyVector(vSource: GLTVector3, vDest: GLTVector3):
    # memcpy(vDest, vSource, sizeof(GLTVector3))
    vDest = vSoure


# Get the dot product between two vectors
def gltVectorDotProduct(vU: GLTVector3, vV: GLTVector3) -> float:
    return vU.value[0] * vV.value[0] + vU.value[1] * vV.value[1] + vU.value[2] * vV.value[2]


# Calculate the cross product of two vectors
def gltVectorCrossProduct(vU: GLTVector3, vV: GLTVector3, vResult: GLTVector3):
    vResult.value[0] = vU.value[1] * vV.value[2] - vV.value[1] * vU.value[2]
    vResult.value[1] = -vU.value[0] * vV.value[2] + vV.value[0] * vU.value[2]
    vResult.value[2] = vU.value[0] * vV.value[1] - vV.value[0] * vU.value[1]


# Given three points on a plane in counter clockwise order, calculate the unit normal
def gltGetNormalVector(vP1: GLTVector3, vP2: GLTVector3, vP3: GLTVector3, vNormal: GLTVector3):
    vV1 = GLTVector3()
    vV2 = GLTVector3()

    gltSubtractVectors(vP2, vP1, vV1)
    gltSubtractVectors(vP3, vP1, vV2)

    gltVectorCrossProduct(vV1, vV2, vNormal)
    gltNormalizeVector(vNormal)


# Transform a point by a 4x4 matrix
def gltTransformPoint(vSrcVector: GLTVector3, mMatrix: GLTMatrix, vOut: GLTVector3):
    vOut.value[0] = mMatrix.value[0] * vSrcVector.value[0] + mMatrix.value[4] * vSrcVector.value[1] + mMatrix.value[8] * vSrcVector.value[2] + mMatrix.value[12]
    vOut.value[1] = mMatrix.value[1] * vSrcVector.value[0] + mMatrix.value[5] * vSrcVector.value[1] + mMatrix.value[9] * vSrcVector.value[2] + mMatrix.value[13]
    vOut.value[2] = mMatrix.value[2] * vSrcVector.value[0] + mMatrix.value[6] * vSrcVector.value[1] + mMatrix.value[10] * vSrcVector.value[2] + mMatrix.value[14]


# Rotates a vector using a 4x4 matrix. Translation column is ignored
def gltRotateVector(vSrcVector: GLTVector3, mMatrix: GLTMatrix, vOut: GLTVector3):
    vOut.value[0] = mMatrix.value[0] * vSrcVector.value[0] + mMatrix.value[4] * vSrcVector.value[1] + mMatrix.value[8] * vSrcVector.value[2]
    vOut.value[1] = mMatrix.value[1] * vSrcVector.value[0] + mMatrix.value[5] * vSrcVector.value[1] + mMatrix.value[9] * vSrcVector.value[2]
    vOut.value[2] = mMatrix.value[2] * vSrcVector.value[0] + mMatrix.value[6] * vSrcVector.value[1] + mMatrix.value[10] * vSrcVector.value[2]

# Gets the three coefficients of a plane equation given three points on the plane.
def gltGetPlaneEquation(vPoint1: GLTVector3, vPoint2: GLTVector3, vPoint3: GLTVector3, vPlane: GLTVector3):
    # Get normal vector from three points. The normal vector is the first three coefficients
    # to the plane equation...
    gltGetNormalVector(vPoint1, vPoint2, vPoint3, vPlane)

    # Final coefficient found by back substitution
    vPlane.value[3] = -(vPlane.value[0] * vPoint3.value[0] + vPlane.value[1] * vPoint3.value[1] + vPlane.value[2] * vPoint3.value[2])


# Determine the distance of a point from a plane, given the point and the
# equation of the plane.
def gltDistanceToPlane(vPoint: GLTVector3, vPlane: GLTVector4) -> float:
    return vPoint.value[0] * vPlane.value[0] + vPoint.value[1] * vPlane.value[1] + vPoint.value[2] * vPlane.value[2] + vPlane.value[3]


###########################################
######## tours.c
###########################################

def gltDrawTorus(majorRadius: float, minorRadius: float, numMajor: int, numMinor: int):
    vNormal = GLTVector3()
    majorStep = 2.0 * GLT_PI / numMajor
    minorStep = 2.0 * GLT_PI / numMinor

    for i in range(numMajor+1):
        a0 = i * majorStep
        a1 = a0 + majorStep
        x0 = math.cos(a0)
        y0 = math.sin(a0)
        x1 = math.cos(a1)
        y1 = math.sin(a1)
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(numMinor+1):
            b = j * minorStep
            c = math.cos(b)
            r = minorRadius * c + majorRadius
            z = minorRadius * math.sin(b)

            # First point
            glTexCoord2f((i) / (numMajor), (j) / (numMinor))
            vNormal.value[0] = x0 * c
            vNormal.value[1] = y0 * c
            vNormal.value[2] = z / minorRadius
            gltNormalizeVector(vNormal)
            glNormal3fv(vNormal.value)
            glVertex3f(x0 * r, y0 * r, z)

            glTexCoord2f((i + 1) / (numMajor), (j) / (numMinor))
            vNormal.value[0] = x1 * c
            vNormal.value[1] = y1 * c
            vNormal.value[2] = z / minorRadius
            glNormal3fv(vNormal.value)
            glVertex3f(x1 * r, y1 * r, z)
        glEnd()


###########################################
######## sphere.c
###########################################
# For best results, put this in a display list
# Draw a sphere at the origin
def gltDrawSphere(fRadius: float, iSlices: int, iStacks: int):
    drho = float(3.141592653589 / iStacks)
    dtheta = 2.0 * 3.141592653589 / iSlices
    ds = 1.0 / iSlices
    dt = 1.0 / iStacks
    t = 1.0
    s = 0.0
    
    for i in range(0, iStacks):
        rho = i * drho
        srho = math.sin(rho)
        crho = math.cos(rho)
        srhodrho = math.sin(rho + drho)
        crhodrho = math.cos(rho + drho)

        # Many sources of OpenGL sphere drawing code uses a triangle fan
        # for the caps of the sphere. This however introduces texturing
        # artifacts at the poles on some OpenGL implementations
        glBegin(GL_TRIANGLE_STRIP)
        s = 0.0
        for j in range(0, iSlices + 1):
            theta = 0.0
            if (j == iSlices):
                theta = 0.0
            else:
                theta = j * dtheta
            
            stheta = -math.sin(theta)
            ctheta = math.cos(theta)

            x = stheta * srho
            y = ctheta * srho
            z = crho
            
            glTexCoord2f(s, t)
            glNormal3f(x, y, z)
            glVertex3f(x * fRadius, y * fRadius, z * fRadius)

            x = stheta * srhodrho
            y = ctheta * srhodrho
            z = crhodrho
            glTexCoord2f(s, t - dt)
            s += ds
            glNormal3f(x, y, z)
            glVertex3f(x * fRadius, y * fRadius, z * fRadius)

        glEnd()

        t -= dt
        
def gltDrawUnitAxes():

    pObj = 0.0	# Temporary, used for quadrics

    # Measurements
    fAxisRadius = 0.025
    fAxisHeight = 1.0
    fArrowRadius = 0.06
    fArrowHeight = 0.1

    # Setup the quadric object
    pObj = gluNewQuadric()
    gluQuadricDrawStyle(pObj, GLU_FILL)
    gluQuadricNormals(pObj, GLU_SMOOTH)
    gluQuadricOrientation(pObj, GLU_OUTSIDE)
    gluQuadricTexture(pObj, GLU_FALSE)

    ###############################################
    # Draw the blue Z axis first, with arrowed head
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(pObj, fAxisRadius, fAxisRadius, fAxisHeight, 10, 1)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.0)
    gluCylinder(pObj, fArrowRadius, 0.0, fArrowHeight, 10, 1)
    glRotatef(180.0, 1.0, 0.0, 0.0)
    gluDisk(pObj, fAxisRadius, fArrowRadius, 10, 1)
    glPopMatrix()

    ###############################################
    # Draw the Red X axis 2nd, with arrowed head
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glRotatef(90.0, 0.0, 1.0, 0.0)
    gluCylinder(pObj, fAxisRadius, fAxisRadius, fAxisHeight, 10, 1)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.0)
    gluCylinder(pObj, fArrowRadius, 0.0, fArrowHeight, 10, 1)
    glRotatef(180.0, 0.0, 1.0, 0.0)
    gluDisk(pObj, fAxisRadius, fArrowRadius, 10, 1)
    glPopMatrix()
    glPopMatrix()

    ###############################################
    # Draw the Green Y axis 3rd, with arrowed head
    glColor3f(0.0, 1.0, 0.0)
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    gluCylinder(pObj, fAxisRadius, fAxisRadius, fAxisHeight, 10, 1)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.0)
    gluCylinder(pObj, fArrowRadius, 0.0, fArrowHeight, 10, 1)
    glRotatef(180.0, 1.0, 0.0, 0.0)
    gluDisk(pObj, fAxisRadius, fArrowRadius, 10, 1)
    glPopMatrix()
    glPopMatrix()

    ###############################################
    # White Sphere at origin
    glColor3f(1.0, 1.0, 1.0)
    gluSphere(pObj, 0.05, 15, 15)

    # Delete the quadric
    gluDeleteQuadric(pObj)