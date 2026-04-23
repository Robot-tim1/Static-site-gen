import os
import shutil

from page_generation import *

def main():
    if os.path.exists('public'):
        shutil.rmtree('public')
    os.mkdir('public')
    static_to_public()
    generate_page(os.path.join('content', 'index.md'), 'template.html', os.path.join('public', 'index.html'))

main()