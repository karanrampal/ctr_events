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

    # extract event information
    events = event_name_df[["pmEvent Name",
                            "Event Id",
                            "Event Type",
                            "Event Description and Trigger"]]
    events = events[events["Event Id"].isin(event_id_list)]

    # re-order the events according to event_id_list
    events = events.set_index("Event Id")
    events = events.reindex(event_id_list).reset_index()

    # extract param information
    params = param_name_df[["pmEvent Name", "Event Parameter Name"]]
    params = params[params["pmEvent Name"].isin(events["pmEvent Name"])]

    # extract param description
    desc = param_desc_df[["Event Parameter Name", "Parameter Description"]]
    desc = desc.drop_duplicates("Event Parameter Name")

    # combine all the information into one dataframe
    tmp = pd.merge(params, desc, on="Event Parameter Name", how="left")
    output = pd.merge(events, tmp, on="pmEvent Name", how="left").set_index("pmEvent Name")

    # write to excel file
    utils.safe_makedir(os.path.dirname(args.output_path))
    writer = pd.ExcelWriter(args.output_path)
    output.to_excel(writer, "Sheet1")
    writer.save()


if __name__ == "__main__":
    main()
