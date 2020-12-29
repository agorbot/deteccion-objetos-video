import os
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("--porcentaje", type=str, default=0.9, help="procentaje entrenamiento y test.")
parser.add_argument("--directorio_origen", type=str, default="data/custom/images", help="Directorio donde se encuentran todas las imagenes y las etiquetas")
parser.add_argument("--directorio_destino", type=str, default="data/custom", help="directorio donde se escribira train y test txt")
opt = parser.parse_args()
print ('origen:',opt.directorio_origen)
print('destino:',opt.directorio_destino)
print('porcentaje:',opt.porcentaje)
path = opt.directorio_origen

files = os.listdir(path)
random.shuffle(files)
porcentaje = float(opt.porcentaje)
train = files[:int(len(files)*porcentaje):]
val = files[int(len(files)*porcentaje):]



with open('{}/train.txt'.format(opt.directorio_destino), 'w') as f:
    for item in train:
        f.write("{}/{} \n".format(path, item))

print('Generando train.txt')
with open('{}/valid.txt'.format(opt.directorio_destino), 'w') as f:
    for item in val:
        f.write("{}/{} \n".format(path, item))
print('Generando valid.txt')