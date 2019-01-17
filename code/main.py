#!/usr/bin/env python3
"""Extract events from PM file"""

import argparse
import sys
import os

import pandas as pd

import utils

def args_parser():
    """Parse command line arguments
    """
    parser = argparse.ArgumentParser(description="Extract PM events from CTR file and save\
                                                  result as excel file")
    parser.add_argument("-d", "--data-path", default="../data/pm_events.xlsx", type=str,
                        help="Directory containing the CTR information file")
    parser.add_argument("-j", "--json-path", default="./params.json", type=str,
                        help="Directory containing the hyper-parameter json file")
    parser.add_argument("-o", "--output-path", default="../output/pm_events_description.xlsx",
                        type=str, help="Directory to store the resultant excel file")
    return parser.parse_args()

def main():
    """Main function
    """
    args = args_parser()

    # read hyper-parameter file
    if os.path.isfile(args.json_path):
        event_id_list = utils.Params(args.json_path).event_id_list
    else:
        sys.exit("No parameters file found at {0}!".format(args.json_path))

    # read the input excel file
    try:
        data = pd.ExcelFile(args.data_path)
    except IOError:
        sys.exit("No PM events file found at {0}!".format(args.data_path))

    event_name_df = data.parse("PmEvents 18.Q2.5", skiprows=3)
    param_name_df = data.parse("PmEventFormat 18.Q2.5", skiprows=3)
    param_desc_df = data.parse("PmEventParams 18.Q2.5", skiprows=3)

    print(event_name_df.head())
    print(param_name_df.head())
    print(param_desc_df.head())
    print(event_id_list)


if __name__ == "__main__":
    main()
