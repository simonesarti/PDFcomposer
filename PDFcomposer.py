from PyPDF2 import PdfFileMerger
import argparse
import os
import re


def parse_input(parser):
    parser.add_argument("--fin", nargs="+", help='input file path (<filename_N>@<filepath_N>)', required=True)
    parser.add_argument("--fout", help='output file path', required=True)
    parser.add_argument("--struct", help='new pdf structure: [f1,(page_start,page_stop)]-[f3,pageN]-...-[f2,pageX]',
                        required=True)
    parser.add_argument("--overwrite", type=str, default=False)

    return parser.parse_args()


def check_input_errors(names, paths):
    if len(names) != len(set(names)):
        print("ERROR: Cannot have two files with the same name")
        quit()

    for file_path in paths:

        if not os.path.exists(file_path):
            print(f"ERROR: Invalid input path {file_path}, path not found")
            quit()

        if not file_path.endswith(".pdf"):
            print(f"ERROR: Invalid input, {os.path.split(file_path)[1]} is not a .pdf file")
            quit()


def create_files_dict(inputs):
    names = []
    paths = []
    files_dict = {}

    for fin in inputs:
        split_list = fin.split("@", 1)

        fin_name = split_list[0]
        fin_path = split_list[1]

        names.append(fin_name)
        paths.append(fin_path)

    check_input_errors(names, paths)

    for (file_name, file_path) in zip(names, paths):

        try:
            files_dict[file_name] = open(file_path, "rb")
        except OSError:
            print(f"ERROR: unable to open file in {file_path}")
            quit()

    return files_dict


def close_files(files_dict):
    for key in files_dict:
        files_dict[key].close()


def check_block_structure(blocks_string):
    number = r"[0-9]+"
    name = r"([0-9]|[a-z]|[A-Z])+"
    page_block = r"\[{0},{1}\]".format(name, number)
    interval_block = r"\[{0},\({1},{2}\)\]".format(name, number, number)
    optional_part = r"(\-({0}|{1}))+".format(page_block, interval_block)
    first_part = r"{0}|{1}".format(page_block, interval_block)
    struct_regex = r"{0}({1})*".format(first_part, optional_part)

    if not re.match(struct_regex, blocks_string):
        print("ERROR: incorrect --struct structure")
        quit()


def parse_blocks(blocks_string):
    block_list = []

    blocks_str_list = blocks_string.split("-[")

    for str_block in blocks_str_list:

        str_block = str_block.replace("[", "")
        str_block = str_block.replace("]", "")
        str_block = str_block.replace("(", "")
        str_block = str_block.replace(")", "")
        parts = str_block.split(",")

        name = parts[0]

        if len(parts) == 2:
            pages = (int(parts[1]) - 1, int(parts[1]))
        else:
            pages = (int(parts[1]) - 1, int(parts[2]))

        if pages[0] < 0 or pages[1] < 0:
            print("ERROR: page values must be positive")
            quit()

        if pages[0] >= pages[1]:
            print("ERROR: page ranges must contain values in increasing order")
            quit()

        block = [name, pages]

        block_list.append(block)

    return block_list


def main():
    parser = argparse.ArgumentParser()
    args = parse_input(parser)

    files_dict = create_files_dict(args.fin)

    output_path = args.fout

    if not output_path.endswith(".pdf"):
        print(f"ERROR: output path {output_path} must correspond to a .pdf file")
        quit()
    if os.path.exists(output_path) and not args.overwrite:
        print(f"ERROR: output path {output_path} already exists.")
        print("Set argument --overwite True in input arguments to allow file overwriting")
        quit()

    blocks_string = args.struct
    blocks_list = parse_blocks(blocks_string)

    merger = PdfFileMerger(strict=False)
    print("\nComposing new PDF:")

    for block in blocks_list:
        file_key = block[0]
        page_range = block[1]

        if file_key not in files_dict.keys():
            print(f"ERROR: '{file_key}' doesn't correspond to an input file name")
            quit()

        try:
            merger.append(fileobj=files_dict[file_key], pages=page_range)
        except IndexError:
            print(f"ERROR: make sure that the range {page_range} stays within the range of pages of file '{file_key}'")

    close_files(files_dict)

    # Write to an output PDF document
    output_file = open(output_path, "wb")
    merger.write(output_file)

    # Close File Descriptors
    merger.close()
    output_file.close()

    print("\nDONE")


if __name__ == '__main__':
    main()
