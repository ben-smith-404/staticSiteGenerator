import sys
from helper_functions import copy_directory_to_new_dest, generate_page, generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 2:
        basepath = sys.argv[1]

    copy_directory_to_new_dest("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()