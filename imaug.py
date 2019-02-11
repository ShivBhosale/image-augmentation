# CLI tool for augmenting images to create a bigger image dataset

import argparse
import os
import json
from augs.functions import apply_transformations, commit, routine_1
import cv2 as cv
from PIL import Image
parser = argparse.ArgumentParser(description='Augment your image data fast')

parser.add_argument("--input", '-i', help="path to input image or input directory")
parser.add_argument("--config", '-c', 
                    help="path to config JSON", 
                    default="config.json")
parser.add_argument("--out", '-o', help="path to output of transformation", default="out")

args = parser.parse_args()

# we gotta have that bad boy config file
assert(os.path.exists(args.config)), "No config file found at: "+args.config
CONFIG = json.load(open(args.config, "r"))

if os.path.isfile(args.input):
    routine_1(args.input, CONFIG, args)
elif os.path.isdir(args.input):
    for dirname, subdirlist, filelist in os.walk(args.input):
        file_name = dirname+"/{}"
        for file in filelist:
            ffname = file_name.format(file)
            routine_1(ffname, CONFIG, args)
else:print("sad")

