!!ARBfp1.0

# dilation.fp
#
# maximum of 3x3 kernel

ATTRIB iTC0 = fragment.texcoord[0];  # input texcoord

OUTPUT oPrC = result.color;          # output color

TEMP tc0, tc1, tc2, tc3, tc4, tc5, tc6, tc7, tc8;

ADD tc0, iTC0, program.local[0];
ADD tc1, iTC0, program.local[1];
ADD tc2, iTC0, program.local[2];
ADD tc3, iTC0, program.local[3];
ADD tc4, iTC0, program.local[4];
ADD tc5, iTC0, program.local[5];
ADD tc6, iTC0, program.local[6];
ADD tc7, iTC0, program.local[7];
ADD tc8, iTC0, program.local[8];
TEX tc0, tc0, texture[0], 2D;
TEX tc1, tc1, texture[0], 2D;
TEX tc2, tc2, texture[0], 2D;
TEX tc3, tc3, texture[0], 2D;
TEX tc4, tc4, texture[0], 2D;
TEX tc5, tc5, texture[0], 2D;
TEX tc6, tc6, texture[0], 2D;
TEX tc7, tc7, texture[0], 2D;
TEX tc8, tc8, texture[0], 2D;

MAX tc0, tc0, tc1;
MAX tc0, tc0, tc2;
MAX tc0, tc0, tc3;
MAX tc0, tc0, tc4;
MAX tc0, tc0, tc5;
MAX tc0, tc0, tc6;
MAX tc0, tc0, tc7;
MAX oPrC, tc0, tc8;

END
