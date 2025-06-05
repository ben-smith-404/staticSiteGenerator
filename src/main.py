from helper_functions import copy_directory_to_new_dest, generate_page, generate_pages_recursive


def main():
    copy_directory_to_new_dest("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()