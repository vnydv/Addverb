from util import Sim, Pos, Box, Crate

LOG = True

# algo to iter through boxes and place them
def PlaceMaximumBoxes(asim):
    # Place the maximum number of boxes onto the crate in the order they are given
    max_boxes_placed = 0  # Track the maximum number of boxes placed
    placed_boxes = []  # Track the positions of the placed boxes

    def backtrack(index):
        nonlocal max_boxes_placed
        if index == len(asim.boxes):
            # All boxes have been considered, update the maximum number of boxes placed
            if len(asim.crate.boxes) > max_boxes_placed:
                max_boxes_placed = len(asim.crate.boxes)
                placed_boxes.clear()
                placed_boxes.extend(asim.crate.boxes)
            return

        box = asim.boxes[index]
        for rotation in range(4):
            if rotation % 2 == 0:
                # Try placing the box in its original orientation
                if tryPlacingBox(box, index, rotation):
                    backtrack(index + 1)
                    if asim.crate.boxes: asim.crate.boxes.pop()
            else:
                # Try placing the box after rotating horizontally or vertically
                box.rotH() if rotation == 1 else box.rotV()
                if tryPlacingBox(box, index, rotation):
                    backtrack(index + 1)
                    if asim.crate.boxes: asim.crate.boxes.pop()
                # Rotate the box back to its original orientation
                box.rotH() if rotation == 1 else box.rotV()

        # Skip the current box
        backtrack(index + 1)

    def tryPlacingBox(box, index, rotation):
        for x in range(asim.crate.l - box.l + 1):
            for y in range(asim.crate.b - box.b + 1):
                for z in range(asim.crate.h - box.h + 1):
                    vpos = Pos(x, y, z)
                    if asim.isValidPlacement(box, vpos):
                        asim.doBox(box, vpos)
                        return True
        return False

    backtrack(0)

    # Update the crate with the maximum number of placed boxes
    asim.crate.boxes.clear()
    asim.crate.boxes.extend(placed_boxes)
    asim.score = max_boxes_placed * Sim.add_score + (len(asim.boxes) - max_boxes_placed) * Sim.skip_score



sim = Sim(Pos(100,100,100), Pos(40,40,40), 5)

PlaceMaximumBoxes(sim)

sim.getResult()