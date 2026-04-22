import os
import shutil

from textnode import *
from htmlnode import *
from page_generation import *

def main():
    if os.path.exists('public'):
        shutil.rmtree('public')
        os.mkdir('public')
    else:
        os.mkdir('public')
    static_to_public()

main()