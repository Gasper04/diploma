from cube.face import Face
from dataclasses import dataclass

# face orientation

# the F, R, B and L faces are orianted so their "top" is at the contact with the U face

# the U is orientet with B at its top

# the D is oriented with F at its top

@dataclass
class Facelet:
    face: Face
    i: int
    j: int

def get_touching_facelets(facelet: Facelet, n: int):
    
    faces = []
    if facelet.face == Face.U:
        if facelet.i == 1:
            faces.append(Facelet(face=Face.B, i=1, j=n-facelet.j+1))
        if facelet.i == n:
            faces.append(Facelet(face=Face.F, i=1, j=facelet.j))
        if facelet.j == 1:
            faces.append(Facelet(face=Face.L, i=1, j=facelet.i))
        if facelet.j == n:
            faces.append(Facelet(face=Face.R, i=1, j=n-facelet.i+1))

    elif facelet.face == Face.D:
        if facelet.i == 1:
            faces.append(Facelet(face=Face.F, i=n, j=facelet.j))
        if facelet.i == n:
            faces.append(Facelet(face=Face.B, i=n, j=n-facelet.j+1))
        if facelet.j == 1:
            faces.append(Facelet(face=Face.L, i=n, j=n-facelet.i+1))
        if facelet.j == n:
            faces.append(Facelet(face=Face.R, i=n, j=facelet.i))

    elif facelet.face == Face.F:
        if facelet.i == 1:
            faces.append(Facelet(face=Face.U, i=n, j=facelet.j))
        if facelet.i == n:
            faces.append(Facelet(face=Face.D, i=1, j=facelet.j))
        if facelet.j == 1:
            faces.append(Facelet(face=Face.L, i=facelet.i, j=n))
        if facelet.j == n:
            faces.append(Facelet(face=Face.R, i=facelet.i, j=1))

    elif facelet.face == Face.B:
        if facelet.i == 1:
            faces.append(Facelet(face=Face.U, i=1, j=n-facelet.j+1))
        if facelet.i == n:
            faces.append(Facelet(face=Face.D, i=n, j=n-facelet.j+1))
        if facelet.j == 1:
            faces.append(Facelet(face=Face.R, i=facelet.i, j=n))
        if facelet.j == n:
            faces.append(Facelet(face=Face.L, i=facelet.i, j=1))

    elif facelet.face == Face.R:
        if facelet.i == 1:
            faces.append(Facelet(face=Face.U, i=n-facelet.j+1, j=n))
        if facelet.i == n:
            faces.append(Facelet(face=Face.D, i=facelet.j, j=n))
        if facelet.j == 1:
            faces.append(Facelet(face=Face.F, i=facelet.i, j=n))
        if facelet.j == n:
            faces.append(Facelet(face=Face.B, i=facelet.i, j=1))

    elif facelet.face == Face.L:
        if facelet.i == 1:
            faces.append(Facelet(face=Face.U, i=facelet.j, j=1))
        if facelet.i == n:
            faces.append(Facelet(face=Face.D, i=n-facelet.j+1, j=1))
        if facelet.j == 1:
            faces.append(Facelet(face=Face.B, i=facelet.i, j=n))
        if facelet.j == n:
            faces.append(Facelet(face=Face.F, i=facelet.i, j=1))

    return faces