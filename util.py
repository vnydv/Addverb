import random

# assuming natural number sizes
# if the crate is full then all other boxes are skipped
# hence - goal is to place max number of boxes onto crate

class Pos:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class Box:

    def __init__(self, maxDims):
        self.l = random.randint(1,maxDims.x)
        self.b = random.randint(1,maxDims.y)
        self.h = random.randint(1,maxDims.z)

    def rotH(self):
        self.l, self.b = self.b, self.l

    def rotV(self):
        self.b, self.h = self.h, self.b


class Crate:

    def __init__(self, l, b, h):
        self.l = l
        self.b = b
        self.h = h
        
        self.boxes = []

    def checkBoxPlacement(self, box, vpos):
        # x,y,z are box top left corners

        # check overflow
        if ((vpos.x+box.l) > self.l) or ((vpos.y+box.b) > self.b) or ((vpos.z+box.h) > self.h):
            return False

        # Check overlap with existing boxes
        for existing_box, existing_vpos in self.boxes:
            if (vpos.x < (existing_vpos.x + existing_box.l) and
                (vpos.x + box.l) > existing_vpos.x and
                vpos.y < (existing_vpos.y + existing_box.b) and
                (vpos.y + box.b) > existing_vpos.y and
                vpos.z < (existing_vpos.z + existing_box.h) and
                (vpos.z + box.h) > existing_vpos.z):                
                return False

        # since not overlapping, check if place on crate directly
        if vpos.z == 0:
            return True

        # check stability 
        for existing_box, existing_vpos in self.boxes:
            if (vpos.x >= existing_vpos.x and
                (vpos.x + box.l) <= (existing_vpos.x + existing_box.l) and
                vpos.y >= existing_vpos.y and
                (vpos.y + box.b) <= (existing_vpos.y + existing_box.b) and
                (vpos.z + box.h) == existing_vpos.z):
                break
        else:
            return False

        return True


class Sim:

    skip_score = -1
    add_score = 2

    def __init__(self, crateDim, maxBoxDim, nboxes):
        self.score = 0
        self.crate = Crate(crateDim.x, crateDim.y, crateDim.z)
        self.boxes = [Box(maxBoxDim) for i in range(nboxes)]

    
    def isValidPlacement(self, box, vpos):
        return self.crate.checkBoxPlacement(box, vpos)

    def doBox(self, box, vpos, skip=False):        
            self.score += [Sim.add_score, Sim.skip_score][skip]

            if not skip:                
                self.crate.boxes.append((box, vpos))
                

    def getResult(self):
        # Get the result
        print("Maximum number of boxes placed:", len(self.crate.boxes))
        for box, vpos in self.crate.boxes:
            print(f"Box dimensions: {box.l}x{box.b}x{box.h}, Position: ({vpos.x}, {vpos.y}, {vpos.z})")
        print("Score:", self.score)


