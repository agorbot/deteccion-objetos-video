import os
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("--porcentaje", type=str, default=0.9, help="procentaje entrenamiento y test.")
parser.add_argument("--directorio_origen", type=str, default="data/custom/images", help="Directorio donde se encuentran todas las imagenes y las etiquetas")
parser.add_argument("--directorio_destino", type=str, default="data/custom", help="directorio donde se escribira train y test txt")
opt = parser.parse_args()

path = opt.directorio_origen

files = os.listdir(path)
random.shuffle(files)
train = files[:int(len(files)*opt.porcentaje)]
val = files[int(len(files)*opt.porcentaje):]



with open('{}/train.txt'.format(opt.directorio_destino), 'w') as f:
    for item in train:
        f.write("{}/{} \n".format(path, item))

with open('{}/valid.txt'.format(opt.directorio_destino), 'w') as f:
    for item in val:
        f.write("{}/{} \n".format(path, item))