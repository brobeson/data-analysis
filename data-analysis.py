#!/usr/bin/env python3

class BoundingBox:
    def __init__(x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


def _make_bounding_box(string):
    values = string.strip().rsplit(",")
    return BoundingBox(values[0], values[1], values[2], values[3])

def _read_ground_truth():
    with open(os.path.expanduser("~/Videos/otb/KiteSurf/groundtruth_rect.txt"))
    as f:
        lines = f.readlines()
    gt = [_make_bound_box(line) for line in lines]
    return gt
