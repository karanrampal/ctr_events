#!/usr/bin/env python3
"""Extract events from PM file"""

import argparse
import sys

import pandas as pd


def args_parser():
    """Parse command line arguments
    """
    parser = argparse.ArgumentParser(description="Extract PM events from CTR file and save\
                                                  result as excel file")
    parser.add_argument("-d", "--data-path", default="../pm_events.xlsx", type=str,
                        help="Directory containing the CTR information file")
    parser.add_argument("-o", "--output-path", default="../pm_events_description.xlsx", type=str,
                        help="Directory to store the resultant excel file")
    return parser.parse_args()

def main():
    """Main function
    """
    args = args_parser()

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


if __name__ == "__main__":
    main()
