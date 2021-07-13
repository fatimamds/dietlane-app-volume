import argparse
import torch
import cv2
import os
import torch.nn.parallel
import numpy as np
import loaddata_demo as loaddata
import pdb
import argparse
import json
import modules, net, senet         # removed densenet & resnet
from volume import get_volume
from mask import get_mask
from palette import getnutrients

import matplotlib.image
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='KD-network')
parser.add_argument('--img', metavar='DIR',default="./input/test.png",
                    help='img to input')
parser.add_argument('--json', metavar='DIR',default="./input/test.json",
                    help='json file to input')
parser.add_argument('--output', metavar='DIR',default="./output",
                    help='dir to output')

args=parser.parse_args()

def define_model(is_resnet, is_densenet, is_senet):
    """
    if is_resnet:
        original_model = resnet.resnet50(pretrained = True)
        Encoder = modules.E_resnet(original_model) 
        model = net.model(Encoder, num_features=2048, block_channel = [256, 512, 1024, 2048])
    if is_densenet:
        original_model = densenet.densenet161(pretrained=True)
        Encoder = modules.E_densenet(original_model)
        model = net.model(Encoder, num_features=2208, block_channel = [192, 384, 1056, 2208])
    """
    if is_senet:
        original_model = senet.senet154(pretrained='imagenet')
        Encoder = modules.E_senet(original_model)
        model = net.model(Encoder, num_features=2048, block_channel = [256, 512, 1024, 2048])

    return model
   

def main():
    if (not os.path.exists(args.output)):
        print("Output directory doesn't exist! Creating...")
        os.makedirs(args.output)

    model = define_model(is_resnet=False, is_densenet=False, is_senet=True)
    model = torch.nn.DataParallel(model).cuda()
    model.load_state_dict(torch.load('./pretrained_model/model_senet'))
    model.eval()
    print
    img = cv2.imread(args.img)

    nyu2_loader = loaddata.readNyu2(args.img)
  
    test(nyu2_loader, model, img.shape[1], img.shape[0])


def test(nyu2_loader, model, width, height):
    for i, image in enumerate(nyu2_loader):     
        image = torch.autograd.Variable(image, volatile=True).cuda()
        out = model(image)
        out = out.view(out.size(2),out.size(3)).data.cpu().numpy()
        max_pix = out.max()
        min_pix = out.min()
        out = (out-min_pix)/(max_pix-min_pix)*255
        out = cv2.resize(out,(width,height),interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(os.path.join(args.output, "out_grey.png"),out)
        out_grey = cv2.imread(os.path.join(args.output, "out_grey.png"),0)
        out_color = cv2.applyColorMap(out_grey, cv2.COLORMAP_JET)
        cv2.imwrite(os.path.join(args.output, "out_color.png"),out_color)
        get_mask(out_grey, args.json)  #get_mask(out_grey, args.json, args.output)
        vol = get_volume(out_grey, args.json)
        print("Volume:")
        print(vol)
        print("unit: cm^3")

        # OUTPUT JSON FILE
        output_json = []
        for i in vol:
            nutrients = getnutrients(i)  # [calories(kcal), protein(g), fats(g), carbs(g), fiber(g)] per 100gms
            for nutrient in nutrients:
                nutrient = (nutrient/100) * vol[i]
            vol_obj = {
                "name": i,       # each key in 'vol', ie name of item
                "measure": vol[i], # value for each key in 'vol', ie volume of item
                "calories": nutrients[0],
                "proteins": nutrients[1],
                "fats": nutrients[2],
                "carbs": nutrients[3],
                "fiber": nutrients[4]
                }
            output_json.append(vol_obj)
        # python dump to json:
        with open(os.path.join(args.output, "volume.json"), "w") as write_file:
            json.dump(output_json, write_file, indent=4)

        
        """
        # OUTPUT TEXT FILE
        out_file = open(os.path.join(args.output, "out.txt"), "w")
        out_file.write("Volume:\n")
        out_file.write(str(vol))
        out_file.write("\n")
        out_file.write("unit: cm^3")
        out_file.close()
        """
        
if __name__ == '__main__':
    main()
