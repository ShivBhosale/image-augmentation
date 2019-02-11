'''
transformation functions that I've used so far
'''
from PIL import Image, ImageFilter
import os

def flip(img):
    im2 = img.transpose(Image.FLIP_TOP_BOTTOM)
    return [(im2, "_flip")]

def mirror(img):
    im2 = img.transpose(Image.FLIP_LEFT_RIGHT)
    return [(im2, "_mirror")]

def rotate(img):
    im_neg = img.rotate(-10)
    im_pos = img.rotate(10)
    return [(im_neg, "_neg10"), (im_pos, "_pos10")]

def scale(img):
    h,w = img.size
    factor = .80
    im_down = (int(h*factor), int(w*factor))
    im_up = (int(h/factor), int(w/factor))
    im_ups = img.resize(im_up)
    im_downs = img.resize(im_down)
    return [(im_ups, "_upsamp"), (im_downs, "_downsamp")]

def noise(img):
    im2 = img.filter(ImageFilter.MedianFilter)
    return [(im2, '_noise')]

function_map = {
    "flip" : flip,
    "mirror": mirror,
    "rotate":rotate,
    "scale":scale,
    "noise":noise
}

def routine_1(name, config, args):
    image = Image.open(name)
    transformed = apply_transformations(image, config["transforms"] ,os.path.basename(name))
    commit(transformed, args.out)

def apply_transformations(image, transforms, name):
    global function_map
    name, ext = name.split('.')
    file_name = name+"{}."+ext
    transformed = [(image, file_name.format(""))]
    for t in transforms:
        transformed.extend([(im, file_name.format(t_name)) for im, t_name in function_map[t](image)])
    return transformed

def commit(transformed, outpath):
    assert(os.path.exists(outpath)), "Output path not found!"
    if outpath[-1] != '/': outpath+='/'
    out_file = outpath+"{}"
    for img, name in transformed:
        img.save(out_file.format(name))
    print(len(transformed), " images commited")
