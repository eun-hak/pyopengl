from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from ctypes import*
import struct
import binascii


# Define targa header.
class TGAHEADER(Structure):
    _fields_ = [
        # Size of ID field that follows header (0)
        ("identsize", c_byte),
        ("colorMapType", c_byte),           # 0 = None, 1 = paletted
        # 0 = none, 1 = indexed, 2 = rgb, 3 = grey, +8=rle
        ("imageType", c_byte),
        ("colorMapStart", c_ushort),          # First colour map entry
        ("colorMapLength", c_ushort),         # Number of colors
        ("colorMapBits", c_char),   # bits per palette entry
        ("xstart", c_ushort),                 # image x origin
        ("ystart", c_ushort),                # image y origin
        ("width", c_ushort),                  # width in pixels
        ("height", c_ushort),               # height in pixels
        ("bits", c_byte),                   # bits per pixel (8 16, 24, 32)
        ("descriptor", c_byte)             # image descriptor
    ]

    def setTgaHeader(self, value):
        self._fields_[0] = value[0:1]
        self._fields_[1] = value[1:2]
        self._fields_[2] = value[2:3]
        self._fields_[3] = value[3:5]
        self._fields_[4] = value[5:7]
        self._fields_[5] = value[7:8]
        self._fields_[6] = value[8:10]
        self._fields_[7] = value[10:12]
        self._fields_[8] = value[12:14]
        self._fields_[9] = value[14:16]
        self._fields_[10] = value[16:17]
        self._fields_[11] = value[17:18]

    def getidentsize(self): return struct.unpack(
        '<B', self._fields_[0])[0]  # 튜플로 안 하고 싶으면 [0]??

    def getcolorMapType(self): return struct.unpack('<B', self._fields_[1])[0]
    def getimageType(self): return struct.unpack('<B', self._fields_[2])[0]
    def getcolorMapStart(self): return struct.unpack('<H', self._fields_[3])[0]
    def getcolorMapLength(self): return struct.unpack(
        '<H', self._fields_[4])[0]

    def getcolorMapBits(self): return struct.unpack('<B', self._fields_[5])[0]
    def getxstart(self): return struct.unpack('<H', self._fields_[6])[0]
    def getystart(self): return struct.unpack('<H', self._fields_[7])[0]
    def getwidth(self): return struct.unpack('<H', self._fields_[8])[0]
    def getheight(self): return struct.unpack('<H', self._fields_[9])[0]
    def getbits(self): return struct.unpack('<B', self._fields_[10])[0]
    def getdescriptor(self): return struct.unpack('<B', self._fields_[11])[0]

##################################
# Allocate memory and load targa bits. Returns pointer to new buffer,
# height, and width of texture, and the OpenGL format of data.
# Call free() on buffer when finished!
# This only works on pretty vanilla targas... 8, 24, or 32 bit color
# only, no palettes, no RLE encoding.
# GLbyte *gltLoadTGA(const char *szFileName, GLint *iWidth, GLint *iHeight, GLint *iComponents, GLenum *eFormat)


def LoadTGA(szFileName, iWidth, iHeight, iComponents, eFormat):
    pFile = ""         # File pointer  #그냥 선언부
    tgaHeader = TGAHEADER()      # TGA file header
    lImageSize = 0.0      # Size in bytes of image
    sDepth = 0.0         # Pixel depth
    pBits = None          # Pointer to bits

    # Default/Failed values
    iWidth[0] = 0  # 매개변수 초기화
    iHeight[0] = 0
    eFormat[0] = GL_BGR
    iComponents[0] = GL_RGB8

    # Attempt to open the fil
    pFile = open(szFileName, "rb")  # readbyte
    print(pFile)
    if (pFile == None):
        return None

    # Read in header (binary)
    # pFile.read(tgaHeader, 18, 1, pFile) #pFile에서 18byte를 읽어서 tgaHeader에 저장
    tgaHeader.setTgaHeader(pFile.read(18))

    # Do byte swap for big vs little endian
# ifdef __APPLE__  #big endian 방식을 little endian 방식으로 바꿈
    # BYTE_SWAP(tgaHeader.colorMapStart)
    # BYTE_SWAP(tgaHeader.colorMapLength)
    # BYTE_SWAP(tgaHeader.xstart)
    # BYTE_SWAP(tgaHeader.ystart)
    # BYTE_SWAP(tgaHeader.width)
    # BYTE_SWAP(tgaHeader.height)
# endif

    # Get width, height, and depth of texture
    iWidth[0] = tgaHeader.getwidth()
    iHeight[0] = tgaHeader.getheight()
    sDepth = tgaHeader.getbits() // 8

    # Put some validity checks here. Very simply, I only understand
    # or care about 8, 24, or 32 bit targa's.
    if (tgaHeader.getbits() != 8 and tgaHeader.getbits() != 24 and tgaHeader.getbits() != 32):
        return None

    # Calculate size of image buffer
    lImageSize = iWidth[0] * iHeight[0] * sDepth

    # Allocate memory and check for success
    pBits = [0] * lImageSize
    if (pBits == None):
        return None

    # Read in the bits
    # Check for read error. This should catch RLE or other
    # weird formats that I don't want to recognize
    pData = pFile.read(lImageSize)
    if len(pData) != lImageSize:
        return None

    for idx in range(lImageSize):
        pBits[idx] = pData[idx]

    # Set OpenGL format expected
    if (sDepth == 3):
        eFormat = GL_BGR
        iComponents = GL_RGB8

    if (sDepth == 4):
        eFormat = GL_BGRA
        iComponents = GL_RGBA8

    if (sDepth == 1):
        eFormat = GL_LUMINANCE
        iComponents = GL_LUMINANCE8

    # Done with File
    pFile.close()

    # Return pointer to image data
    return pBits
