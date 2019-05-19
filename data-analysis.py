#!/usr/bin/env python3

import argparse
import os.path

__version__="0.0.0"

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
    with open(os.path.expanduser("~/Videos/otb/KiteSurf/groundtruth_rect.txt")) as f:
        lines = f.readlines()
    gt = [_make_bound_box(line) for line in lines]
    return gt


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze bounding box data for overlap."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Display the version, and exit."
    )
    parser.add_argument(
        "--experimental-root",
        default="~/data/py-MDNet/results",
        help="The root directory which contains the experimental sequence "
            "data. This directory should have each sequence as a subdirectory. "
            "Within each sequence subdirectory should be a file with the "
            "experimental bounding box data.",
        nargs="?"
    )
    parser.add_argument(
        "--control-root",
        default="~/data/py-MDNet/control",
        help="The root directory which contains the control sequence "
            "data. This directory should have each sequence as a subdirectory. "
            "Within each sequence subdirectory should be a file with the "
            "control bounding box data.",
        nargs="?"
    )
    parser.add_argument(
        "--ground-truth-root",
        default="~/data/py-MDNet/results",
        help="The root directory which contains the ground truth sequence "
            "data. This directory should have each sequence as a subdirectory. "
            "Within each sequence subdirectory should be a file with the "
            "ground truth bounding box data.",
        nargs="?"
    )
    parser.add_argument(
        "--sequence",
        help="The sequence to analyze. If omitted, all sequences are analyzed.",
        nargs="?"
    )
    return parser.parse_args()


if __name__ == "__main__":
    ARGUMENTS = _parse_arguments()
