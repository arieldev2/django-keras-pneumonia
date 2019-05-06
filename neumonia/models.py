from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from tensorflow.python.keras.models import load_model, model_from_json
from django.urls import reverse
from tensorflow.python.keras.initializers import glorot_uniform
from keras.utils import CustomObjectScope
from PIL import Image
from keras.applications import imagenet_utils
from keras import applications
import keras
from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input, decode_predictions
import tensorflow as tf
from keras import backend as K
import cv2
from django.core.files.base import ContentFile
from neumonia_project.settings import MEDIA_URL
from PIL import Image
import os
from os.path import abspath, join, dirname






class Paciente(models.Model):

	s = (
		('Femenino', 'Femenino'),
		('Masculino', 'Masculino')
		)


	nombre = models.CharField(max_length=250) 
	primer_apellido = models.CharField(max_length=250) 
	segundo_apellido = models.CharField(max_length=250)
	sexo = models.CharField(max_length=250, choices=s, default='Femenino')
	edad = models.IntegerField()
	correo = models.CharField(max_length=250)
	author = models.ForeignKey(User, on_delete=models.CASCADE)


	def __str__(self):
		return self.author

	def __str__(self):
		return self.id



	@property
	def NombreCompleto(self):
		return '{} {} {}'.format(self. nombre, self.primer_apellido, self.segundo_apellido)

	def __str__(self):
		return '{} {} {}'.format(self.nombre, self.primer_apellido, self.segundo_apellido)


	def get_absolute_url(self):
		return reverse('paciente-detalles', kwargs={'pk': self.pk})






class Clasificacion(models.Model):
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	clave_ex = models.CharField(max_length=250)
	img = models.ImageField(upload_to='pictures_xray')
	prediccion = models.CharField(max_length=250)
	nota = models.CharField(max_length=500, blank=True)
	fecha = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)


	def __str__(self):
		return self.author

	def __str__(self):
		return self.paciente.id
	
	
	

	

	def predict(self):
	
		K.reset_uids()

		classes = ['Normal', 'Neumonia']
			
		modelo = 'neumonia/model/model_neumonia_v41.json'
		pesos = 'neumonia/model/weights_neumonia_v41.h5'

		with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
			with open(modelo, 'r') as f:
				model = model_from_json(f.read())
				model.load_weights(pesos)

		img = image.load_img(self.img, target_size=(150,150))
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0) 
		x = preprocess_input(x)
		preds = model.predict(x)
		resultado = preds[0] #solo una dimension

		porcentaje = np.round(resultado*100,2)
		porcentaje = list(porcentaje)
		
		respuesta = np.argmax(resultado) # el valor mas alto de resultado

		for i in range(len(classes)):
			res = classes[i]

			if i == respuesta:
				return 'Resultado: {:.4}% {}'.format(round(max(porcentaje),2), res)

		
	
		



	def save(self, *args, **kwargs):
		self.prediccion = self.predict()
		super().save(*args, **kwargs)

	@property
	def NombreCompleto(self):
		return '{} {} {}'.format(self.paciente.nombre, self.paciente.primer_apellido, self.paciente.segundo_apellido)


	def __str__(self):
		return '{} {} {}'.format(self.paciente.nombre, self.paciente.primer_apellido, self.paciente.segundo_apellido)

	def get_absolute_url(self):
		return reverse('clasificacion-detalles', kwargs={'pk': self.pk})




