import os
import shutil
import sys

from page_generation import *

basepath = '/'

if len(sys.argv) > 1:
    basepath = sys.argv[1]

def main():
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.mkdir('docs')
    static_to_docs()
    generate_pages_recursive('content', 'template.html', 'docs', basepath)

main()