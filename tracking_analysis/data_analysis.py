#!/usr/bin/env python3

"""Generate graphs of IoU data."""

import argparse
import json
import os.path
import sys

import matplotlib.pyplot as plt

__version__ = "0.0.0"

BACKGROUND_CLUTTER = "background_clutter"
DEFORMATION = "deformation"
FAST_MOTION = "fast_motion"
ILLUMINATION_VARIATION = "illumination_variation"
IN_PLANE_ROTATION = "in_plane_rotation"
LOW_RESOLUTION = "low_resolution"
MOTION_BLUR = "motion_blur"
OCCLUSION = "occlusion"
OUT_OF_PLANE_ROTATION = "out_of_plane_rotation"
OUT_OF_VIEW = "out_of_view"
SCALE_VARIATION = "scale_variation"

ATTRIBUTES = [
    BACKGROUND_CLUTTER,
    DEFORMATION,
    FAST_MOTION,
    ILLUMINATION_VARIATION,
    IN_PLANE_ROTATION,
    LOW_RESOLUTION,
    MOTION_BLUR,
    OCCLUSION,
    OUT_OF_PLANE_ROTATION,
    OUT_OF_VIEW,
    SCALE_VARIATION,
]


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze bounding box data for overlap."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Display the version, and exit.",
    )
    parser.add_argument(
        "--experimental-root",
        default="~/data/py-MDNet/results",
        help="The root directory which contains the experimental sequence "
        "data. This directory should have each sequence as a subdirectory. "
        "Within each sequence subdirectory should be a file with the "
        "experimental bounding box data.",
        nargs="?",
    )
    parser.add_argument(
        "--control-root",
        default="~/data/py-MDNet/control",
        help="The root directory which contains the control sequence "
        "data. This directory should have each sequence as a subdirectory. "
        "Within each sequence subdirectory should be a file with the "
        "control bounding box data.",
        nargs="?",
    )
    parser.add_argument(
        "--ground-truth-root",
        default="~/Videos/otb",
        help="The root directory which contains the ground truth sequence "
        "data. This directory should have each sequence as a subdirectory. "
        "Within each sequence subdirectory should be a file with the "
        "ground truth bounding box data.",
        nargs="?",
    )
    parser.add_argument(
        "--output-root",
        default=os.getcwd(),
        help="The root directory to which the graphs should be written.",
        nargs="?",
    )
    parser.add_argument(
        "sequences",
        help="The sequences to analyze. If omitted, all sequences are "
        "analyzed.",
        nargs="*",
    )
    return parser.parse_args()


def _validate_arguments(arguments):
    arguments.experimental_root = os.path.expanduser(
        arguments.experimental_root
    )
    arguments.control_root = os.path.expanduser(arguments.control_root)
    arguments.ground_truth_root = os.path.expanduser(
        arguments.ground_truth_root
    )
    arguments.output_root = os.path.expanduser(arguments.output_root)
    if not os.path.isdir(arguments.experimental_root):
        sys.exit(f"{arguments.experimental_root} is not a directory.")
    if not os.path.isdir(arguments.control_root):
        sys.exit(f"{arguments.control_root} is not a directory.")
    if not os.path.isdir(arguments.ground_truth_root):
        sys.exit(f"{arguments.ground_truth_root} is not a directory.")
    if not os.path.isdir(arguments.output_root):
        sys.exit(f"{arguments.output_root} is not a directory.")


def _get_all_sequences(ground_truth_root):
    return next(os.walk(ground_truth_root))[1]


def _make_bounding_box_from_text(string):
    values = string.strip().rsplit(",")
    return {
        "x": float(values[0]),
        "y": float(values[1]),
        "width": float(values[2]),
        "height": float(values[3]),
    }


def _read_bounding_boxes_from_text(filename):
    with open(filename) as f:
        lines = f.readlines()
    return [_make_bounding_box_from_text(line) for line in lines]


def _make_bounding_box_from_json(entry):
    return {"x": entry[0], "y": entry[1], "width": entry[2], "height": entry[3]}


def _read_bounding_boxes_from_json(filename):
    with open(filename) as f:
        document = json.load(f)["res"]
        return [_make_bounding_box_from_json(entry) for entry in document]


def _read_bounding_boxes(filename):
    if os.path.exists(filename):
        _, extension = os.path.splitext(filename)
        if extension == ".txt":
            return _read_bounding_boxes_from_text(filename)
        if extension == ".json":
            return _read_bounding_boxes_from_json(filename)
    print(f"error: {filename} does not exist")
    return None


def _read_attributes(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            return [l.strip() for l in f.readlines()]
    return None


def _calculate_iou(gt, tracking):  # pylint: disable=C0103
    left = max(gt["x"], tracking["x"])
    right = min(gt["x"] + gt["width"], tracking["x"] + tracking["width"])
    top = max(gt["y"], tracking["y"])
    bottom = min(gt["y"] + gt["height"], tracking["y"] + tracking["height"])
    intersection = max(0, right - left) * max(0, bottom - top)
    union = (
        gt["width"] * gt["height"]
        + tracking["width"] * tracking["height"]
        - intersection
    )
    return intersection / union


def _calculate_ious(ground_truth_data, tracking_data):
    assert len(ground_truth_data) == len(tracking_data)
    return [
        _calculate_iou(gt, tracking)
        for gt, tracking in zip(ground_truth_data, tracking_data)
    ]


def _make_symlinks(
    sequence, output_root, mean_control, mean_experimental, attributes
):
    if mean_control <= mean_experimental:
        os.symlink(
            f"../{sequence}.svg",
            os.path.join(output_root, "better", f"{sequence}"),
        )
    else:
        os.symlink(
            f"../{sequence}.svg",
            os.path.join(output_root, "worse", f"{sequence}"),
        )
    if attributes is not None:
        for attribute in attributes:
            os.symlink(
                f"../{sequence}.svg",
                os.path.join(output_root, attribute, f"{sequence}"),
            )


def _graph_ious(
    sequence,
    control_ious,
    control_mean,
    experimental_ious,
    experimental_mean,
    output_root,
):
    plt.clf()
    plt.suptitle(sequence)
    plt.plot(range(len(control_ious)), control_ious, "b.")
    plt.ylabel("Overlap")
    plt.xlabel("Frame")
    plt.axhline(y=control_mean, color="blue")
    plt.plot(range(len(experimental_ious)), experimental_ious, "r.")
    plt.axhline(y=experimental_mean, color="red")
    plt.legend([None, "control", None, "experimental"])
    plt.savefig(os.path.join(output_root, f"{sequence}.svg"))


def _make_subdirectories(output_root):
    os.makedirs(os.path.join(output_root, "better"), exist_ok=True)
    os.makedirs(os.path.join(output_root, "worse"), exist_ok=True)
    for attribute in ATTRIBUTES:
        os.makedirs(os.path.join(output_root, attribute), exist_ok=True)


def _clean_up_sequence(output_root, sequence):
    if os.path.islink(os.path.join(output_root, "better", f"{sequence}")):
        os.unlink(os.path.join(output_root, "better", f"{sequence}"))
    if os.path.islink(os.path.join(output_root, "worse", f"{sequence}")):
        os.unlink(os.path.join(output_root, "worse", f"{sequence}"))
    for attribute in ATTRIBUTES:
        if os.path.islink(os.path.join(output_root, attribute, f"{sequence}")):
            os.unlink(os.path.join(output_root, attribute, f"{sequence}"))
    if os.path.exists(os.path.join(output_root, f"{sequence}.svg")):
        os.remove(os.path.join(output_root, f"{sequence}.svg"))


def _main():
    arguments = _parse_arguments()  # pylint: disable=C0103
    _validate_arguments(arguments)
    if not arguments.sequences:
        arguments.sequences = _get_all_sequences(arguments.ground_truth_root)
    arguments.sequences.sort()
    _make_subdirectories(arguments.output_root)
    BAD_SEQUENCES = ["David", "Diving", "Football1", "Freeman3", "Freeman4"]
    for sequence in arguments.sequences:
        if sequence not in BAD_SEQUENCES:
            print(f"Analyzing {sequence}")
            _clean_up_sequence(arguments.output_root, sequence)
            attributes = _read_attributes(
                os.path.join(
                    arguments.ground_truth_root, sequence, "attributes.txt"
                )
            )
            ground_truth_data = _read_bounding_boxes(
                os.path.join(
                    arguments.ground_truth_root,
                    sequence,
                    "groundtruth_rect.txt",
                )
            )
            control_data = _read_bounding_boxes(
                os.path.join(arguments.control_root, sequence, "result.json")
            )
            experimental_data = _read_bounding_boxes(
                os.path.join(
                    arguments.experimental_root, sequence, "result.json"
                )
            )
            if (
                ground_truth_data is not None
                and control_data is not None
                and experimental_data is not None
            ):
                control_ious = _calculate_ious(ground_truth_data, control_data)
                experimental_ious = _calculate_ious(
                    ground_truth_data, experimental_data
                )
                control_mean = sum(control_ious) / len(control_ious)
                experimental_mean = sum(experimental_ious) / len(
                    experimental_ious
                )
                _graph_ious(
                    sequence,
                    control_ious,
                    control_mean,
                    experimental_ious,
                    experimental_mean,
                    arguments.output_root,
                )
                _make_symlinks(
                    sequence,
                    arguments.output_root,
                    control_mean,
                    experimental_mean,
                    attributes,
                )


if __name__ == "__main__":
    _main()
