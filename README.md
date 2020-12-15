# Deteccion de objetos en video 

Proyecto basado en el repositorio de [Alejandro Puig](https://github.com/puigalex/deteccion-objetos-video), esta construido usando Pytorch y usa como redes CNN la red YOLO y DARKNET53. YOLO es una red ya entrenada y detecta 80 distintos objetos, la lista de estos se encuentra en el archivo [data/coco.names](https://github.com/puigalex/deteccion-objetos-video/blob/master/data/coco.names), en cambio DARNEKT53 es una red que es buena para detectar sombras, bordes etc. ( No detecta objetos)

Como el entrenamiento y el testeo del proyecto requieren paralelismo, resulta indispensable usar GPU para ejecutar el proyecto (los tiempos de simulación pasan de 4 horas a 10 minutos). Por ende se generaron 2 Jupiter Notebooks en Google Colabs. 

* [Notebook Entrenamiento](https://colab.research.google.com/drive/1mKD2hDbshoCVdZk9PNJp4fbGBHLs8kPu?usp=sharing)
* [Notebook Prueba](https://colab.research.google.com/drive/1qQzednUVwfmnWuzd97zvnvnAGEdKq-cO?usp=sharing)

RECOMENDACIONES: 

1. Usar Google Drive o AWS S3 para los archivos de imagenes, modelos y pesos.
2. No olvidad de cambiar el setup de la session de colab. Usar siempre GPU y no CPU.


De Todas Formas se describen los pasos para ejecutar el programa.

# Crear ambiente
Para tener en orden nuestras paqueterias de python primero vamos a crear un ambiente llamado "deteccionobj" el cual tiene la version 3.6 de python
``` 
conda create -n deteccionobj python=3.6
```

Activamos el ambiente deteccionobj para asegurarnos que estemos en el ambiente correcto al momento de hacer la instalación de todas las paqueterias necesarias
```
source activate deteccionobj
```

# Instalación de las paqueterias
Estando dentro de nuestro ambiente vamos a instalar todas las paqueterias necesarias para correr nuestro detector de objetos en video, la lista de los paqueter y versiones a instalar están dentro del archivo requirements.txt por lo cual instalaremos haciendo referencia a ese archivo
```
pip install -r requirements.txt
```

# Descargar los pesos del modelo entrenado 
Para poder correr el modelo de yolo tendremos que descargar los pesos de la red neuronal, los pesos son los valores que tienen todas las conexiones entre las neuronas de la red neuronal de YOLO, este tipo de modelos son computacionalmente muy pesados de entrenar desde cero por lo cual descargar el modelo pre entrenado es una buena opción.

```
bash weights/download_weights.sh
```

Movemos los pesos descargados a la carpeta llamada weights
```
mv yolov3.weights weights/
```

# Correr el detector de objetos en video 
Por ultimo corremos este comando el cual activa la camara web para poder hacer deteccion de video sobre un video "en vivo"
```
python deteccion_video.py
```

# Modificaciones
Si en vez de correr detección de objetos sobre la webcam lo que quieres es correr el modelo sobre un video que ya fue pre grabado tienes que cambiar el comando para correr el codigo a:

```
python deteccion_video.py --webcam 0 --directorio_video <directorio_al_video.mp4>
```

# Entrenamiento 

Ahora, si lo que quieres es entrenar un modelo con las clases que tu quieras y no utilizar las 80 clases que vienen por default podemos entrenar nuestro propio modelo. Estos son los pasos que deberás seguir:

Primero deberás etiquetar las imagenes con el formato VOC, luego mediante un script generar la imagenes en formato YOLO. Ver [repositorio](https://github.com/fbarriosr/labelsImg.git) 

Desde la carpeta config correremos el archivo create_custom_model para generar un archivo .cfg el cual contiene información sobre la red neuronal para correr las detecciones
```
cd config
bash create_custom_model.sh <Numero_de_clases_a_detectar>
cd ..
```
Descargamos la estructura de pesos de YOLO para poder hacer transfer learning sobre esos pesos

```
cd weights
bash download_darknet.sh
cd ..
```

## Poner las imagenes y archivos de metadata en las carpetar necesarias

Las imagenes etiquetadas tienen que estar en el directorio **data/custom/images** mientras que las etiquetas/metadata de las imagenes tienen que estar en **data/custom/labels**.
Por cada imagen.jpg debe de existir un imagen.txt (metadata con el mismo nombre de la imagen)

El archivo ```data/custom/classes.names``` debe contener el nombre de las clases, como fueron etiquetadas, un renglon por clase. NO OLVIDAR QUE DEBE HABER UN \N AL FINAL DE LA ULTIMA CLASE.

Los archivos ```data/custom/valid.txt``` y ```data/custom/train.txt``` deben contener la dirección donde se encuentran cada una de las imagenes. Estos se pueden generar con el siguiente comando (estando las imagenes ya dentro de ```data/custom/images```). NO OLVIDES RENOMBRAR LOS ARCHIVOS DE valid2.txt A valid.txt Y train2.txt A train.txt.

```
python split_train_val.py
 ```

## Entrenar

 ```
 python train.py --model_def config/yolov3-custom.cfg --data_config config/custom.data --pretrained_weights weights/darknet53.conv.74 --batch_size 2
 ```
 EL PROGRAMA GUARDA 1 CKECKPOINT POR CADA EPOCA, POR ENDE PARA EVITAR LLENAR EL DISCO DURO ELIMINA TODOS LOS CHECKPOINTS MENOS EL UTIMO
 
 ```
 %cd /content/deteccion-objetos-video/checkpoints/
!ls -1t |awk 'NR>=2 { print $ 0; }' | xargs rm
!ls
 ```
 

## Correr deteccion de objetos en video con nuestras clases
```
python deteccion_video.py --model_def config/yolov3-custom.cfg --checkpoint_model checkpoints/yolov3_ckpt_99.pth --class_path data/custom/classes.names  --weights_path checkpoints/yolov3_ckpt_99.pth  --conf_thres 0.85
```

