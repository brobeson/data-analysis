"""Generate data OTB can use to generate graphs."""

import argparse
import os.path

# import sys

import analysis_tools

# import data_sets

__version__ = "0.0.0"


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate data OTB can use to generate graphs."
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
    arguments = parser.parse_args()
    arguments.experimental_root = os.path.expanduser(
        arguments.experimental_root
    )
    arguments.ground_truth_root = os.path.expanduser(
        arguments.ground_truth_root
    )
    arguments.output_root = os.path.expanduser(arguments.output_root)
    return arguments


def _main():
    arguments = _parse_arguments()
    exp_boxes = analysis_tools.read_bounding_boxes(arguments.experimental_root)
    gt_boxes = analysis_tools.read_bounding_boxes(arguments.ground_truth_root)
    # exp_dataset = data_sets.determine_data_set(exp_boxes.keys)
    # gt_dataset = data_sets.determine_data_set(gt_boxes.keys)
    # if exp_dataset is None:
    #    sys.exit(
    #        "error: Could not determine which data set the experimental data is from."
    #    )
    # if gt_dataset is None:
    #    sys.exit(
    #        "error: Could not determine which data set the ground truth data is from."
    #    )
    # if exp_dataset != gt_dataset:
    #    sys.exit(
    #        "error: Experimental and ground truth data appear to be from different data sets."
    #    )
    common = _find_common_sequences(gt_boxes.keys(), exp_boxes.keys())
    new_dict = {}
    for k in exp_boxes:
        if k in common:
            new_dict[k] = exp_boxes[k]
    exp_boxes = new_dict
    new_dict.clear()
    for k in gt_boxes:
        if k in common:
            new_dict[k] = gt_boxes[k]
    gt_boxes = new_dict

    file_contents = {
        "name": "test",
        "desc": "a test file",
        "tracker": "dMDNet",
        "evalType": "OPE",
        "seqs": exp_boxes.keys(),
        "overlap": 0.0,
        "error": 0.0,
        "overlapScores": [],
        "errorNum": [],
        "successRateList": [],
        "precisionList": [],
    }
    analysis_tools.write_otb_data(file_contents)


# ------------------------------------------------------------------------------
#                                                         temporary operations
# ------------------------------------------------------------------------------
def _find_common_sequences(data_set_1, data_set_2):
    return [s for s in data_set_1 if s in data_set_2]


if __name__ == "__main__":
    _main()
