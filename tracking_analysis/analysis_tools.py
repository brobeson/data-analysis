"""Utility functions for analyzing data."""

import json
import math
import os.path


def read_bounding_boxes(data_root):
    """
    Read bounding box data for a data set.

    Each sequence in the data set is an entry in a dict. The key is the sequence
    name. The value a list of dicts. Each dict in the list is a bounding box.
    The bounding box keys are "x", "y", "width", and "height".

    Parameters:
    data_root (string): The root directory of the data set.

    Returns:
    dict: The returned data has the following form:
    { sequence : [ { x: y: width: height: }, ... ], ... }
    """
    sequences = next(os.walk(data_root))[1]
    sequences.sort()
    boxes = {}
    for sequence in sequences:
        if os.path.exists(os.path.join(data_root, sequence, "result.json")):
            boxes[sequence] = _read_bounding_boxes_from_json(
                os.path.join(data_root, sequence, "result.json")
            )
        elif os.path.exists(
            os.path.join(data_root, sequence, "groundtruth_rect.txt")
        ):
            boxes[sequence] = _read_bounding_boxes_from_text(
                os.path.join(data_root, sequence, "groundtruth_rect.txt")
            )
        else:
            print("error: bounding box data not found in", sequence)
    return boxes


def write_otb_data(content):
    """
    Write OTB data to a JSON file.

    Parameters:
    content (dict): The data to write to the file.
    """
    with open("file.json", "w") as f:
        json.dump(content, f, indent=2)


def calcualte_center_error(exp_data, gt_data):
    """Calculate the center error for a set of bounding box data.

    Parameters:
    exp_data (dict): The experimental bounding box data for a data set.
    gt_data (dict): The ground truth bounding box data for a data set.

    Returns:
    dict: A dictionary of the following form
    { sequence: [ error, ... ], ... }
    For each sequence, there is a list of distances between the centers of the
    experimental and ground truth bounding boxes. Each distance corresponds to
    one frame from the sequence.
    """
    errors = {}
    for sequence in exp_data:
        errors[sequence] = []
        exp_boxes = exp_data[sequence]
        gt_boxes = gt_data[sequence]
        for exp_box, gt_box in zip(exp_boxes, gt_boxes):
            exp_center = _calculate_center(exp_box)
            gt_center = _calculate_center(gt_box)
            errors[sequence].append(_calculate_distance(exp_center, gt_center))
    return errors


# ------------------------------------------------------------------------------
#                                                      internal implementation
# ------------------------------------------------------------------------------
def _read_bounding_boxes_from_json(filename):
    with open(filename) as f:
        document = json.load(f)["res"]
        return [_make_bounding_box_from_json(entry) for entry in document]


def _make_bounding_box_from_json(entry):
    return {"x": entry[0], "y": entry[1], "width": entry[2], "height": entry[3]}


def _read_bounding_boxes_from_text(filename):
    with open(filename) as f:
        lines = f.readlines()
    return [_make_bounding_box_from_text(line) for line in lines]


def _make_bounding_box_from_text(string):
    values = string.strip().rsplit(",")
    return {
        "x": float(values[0]),
        "y": float(values[1]),
        "width": float(values[2]),
        "height": float(values[3]),
    }


def _calculate_center(box):
    return (box["x"] + 0.5 * box["width"], box["y"] + 0.5 * box["height"])


def _calculate_distance(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[0] - q[0]) ** 2)
