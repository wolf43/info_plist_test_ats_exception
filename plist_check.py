"""This module checks the info.plist files for Apple app bundles."""
import os
import plistlib
import argparse
import json
from datetime import datetime


def get_cl_arguments():
    """Get the command line arguments passed by user."""
    parser = argparse.ArgumentParser(prog='ATS exception checking tool', description='Checks ATS NSAllowsArbitraryLoads in Info.plist files')
    parser.add_argument('-d', '--input_dir', nargs='?', help='Input directory to scan for Info.plist files, app buldles are directories')
    args = parser.parse_args()
    return vars(args)['input_dir']


def find_all_files_with_name(name, path):
    """Walk the directory and get all files with name."""
    files_list = []
    for root, _, files in os.walk(path):
        if name in files:
            files_list.append(os.path.join(root, name))
    return files_list


def write_output_to_file(file_name, results_dict):
    """Write input list to a file."""
    with open(file_name, "w") as file_handle:
        json.dump(results_dict, file_handle)
    print("Results stored in ", file_name)


def print_not_passed(results_dict):
    """Print all the domains that didn't pass ATS exception test."""
    count_not_passed = 0
    print('Number of Info.plist files tested:', len(results_dict))
    print('-----Domains failing ATS exception test-----')
    for key, value in results_dict.items():
        if 'Passed' not in value:
            count_not_passed += 1
            print(key, ' - ', value)
    print("Number of Info.plist files that didn't pass ATS test:", count_not_passed)


def ats_exception_test(info_plist_file):
    """Check NSAllowsArbitraryLoads exception in Info.plist files in files_list."""
    pl_dict = plistlib.readPlist(info_plist_file)
    try:
        item = pl_dict['NSAppTransportSecurity']
        try:
            if item['NSAllowsArbitraryLoads'] is True:
                # print("Arbitrary loads allowed in ", info_plist_file)
                return "Failed: NSAllowsArbitraryLoads exception is allowed"
            else:
                return "Passed: NSAllowsArbitraryLoads is not allowed"
        except KeyError:
            return "Passed: NSAllowsArbitraryLoads is not set"
    except KeyError:
        # print("NSAppTransportSecurity not present in ", info_plist_file)
        return "Error: NSAppTransportSecurity is not present"


def main():
    """The main function."""
    dir_to_scan = get_cl_arguments()
    info_plist_file_list = find_all_files_with_name('Info.plist', dir_to_scan)
    results_dict = {}
    for info_plist_file in info_plist_file_list:
        result = ats_exception_test(info_plist_file)
        print(info_plist_file, ' - ', result)
        results_dict[info_plist_file] = result
    output_filename = "".join((str(datetime.now().date()), '_ats_exceptions_results.json'))
    write_output_to_file(output_filename, results_dict)
    print_not_passed(results_dict)

if __name__ == '__main__':
    main()
