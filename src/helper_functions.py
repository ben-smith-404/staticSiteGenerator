import os
import shutil

from text_functions import extract_title, markdown_to_html_node

def copy_directory_to_new_dest(source, destination):
    if os.path.exists(source) == False:
        raise Exception("Source does not exist")
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Removing old {destination}")
    os.mkdir(destination)
    print(f"Creating new {destination}")

    for item in os.listdir(source):
        src = os.path.join(source, item)
        dst = os.path.join(destination, item)
        if os.path.isfile(src):
            print(f"Copy {src} to {dst}")
            shutil.copy(src, dst)
        else: #item is dir
            print(f"Recursion time for {src}")
            copy_directory_to_new_dest(src, dst)

def generate_page(from_path, template_path, dest_path, basepath):
    path = os.getcwd()
    from_path = os.path.join(path, from_path)
    dest_path = os.path.join(path, dest_path)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = get_file_content(from_path)
    template = get_file_content(template_path)

    nodes = markdown_to_html_node(markdown)
    html_content = nodes.to_html()
    title = extract_title(markdown)

    template = template.replace('{{ Title }}', title)
    template = template.replace("{{ Content }}", html_content)
    template = template.replace("href=\"/", f"href=\"{basepath}")
    template = template.replace("src=\"/", f"src=\"{basepath}")
    make_file(dest_path, template)

def get_file_content(file_path):
    f = open(file_path)
    contents = f.read()
    f.close()
    return contents

def make_file(file_path, content):
    f = open(file_path, "w")
    f.write(content)
    f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        new_dir_path_content = os.path.join(dir_path_content, item)
        new_dest_dir_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(new_dir_path_content):
            # swap ".md" for ".html"
            new_dest_dir_path = new_dest_dir_path.rstrip(".md")
            new_dest_dir_path = f"{new_dest_dir_path}.html"
            # If it's a file, make a file
            generate_page(new_dir_path_content, template_path, new_dest_dir_path, basepath)
        else:
            # create a dir if not exists
            if os.path.isdir(new_dest_dir_path) == False:
                os.mkdir(new_dest_dir_path)
            # jump into this dir and loop through
            generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path, basepath)