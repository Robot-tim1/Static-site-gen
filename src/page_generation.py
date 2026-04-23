import os
import shutil

from textnode import *
from htmlnode import *

def static_to_public(static_dir=os.path.join('.', 'static'), public_dir=os.path.join('.', 'public'), next_dir=None):
    if next_dir:
        static_dir = os.path.join(static_dir, next_dir)
        public_dir = os.path.join(public_dir, next_dir)
    directory_list = []

    static_list = os.listdir(static_dir)
    for file in static_list:
        file_static = os.path.join(static_dir, file)
        file_public = os.path.join(public_dir, file)
        if os.path.isfile(file_static):
            shutil.copy(file_static, public_dir)
        else:
            os.mkdir(file_public)
            directory_list.append(file)

    for directory in directory_list:
        static_to_public(static_dir, public_dir, directory)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith('# '):
            return block[2:].strip()
    raise Exception('No h1 header')

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        text = file.read()
    with open(template_path) as file:
        template = file.read()
    content = markdown_to_html_node(text).to_html()
    title = extract_title(text)
    html = template.replace('{{ Title }}', title).replace('{{ Content }}', content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(html)