# -*- coding: utf-8 -*-
print '************* ------ Script Init  ------ *************'
print 'Importando librerias...'
import numpy as np
from PIL import Image
import sys, getopt
#import exifread
import matplotlib.pyplot as plt
import matplotlib.colors as colors
print '\tLibrerias importadas correctamente'

#Obtiene la matriz con 1/2 y -1/2
#inv:  Booleno que decide si se hace la transformada inversa (True) o normal (False)
def get_matriz_transformada_inversa(V_mul, inv):
	shape_mul = V_mul.shape
	diagonal = np.zeros_like(V_mul)
	x=0
	y=0
	while y < shape_mul[1]-1:
		while x < shape_mul[0]-1:
			if inv:
				diagonal[x][y] = 1
				diagonal[x][y+(shape_mul[0])/2] = 1
			else:	
				diagonal[x][y] = 0.5
				diagonal[x][y+(shape_mul[0])/2] = 0.5
			if not x == shape_mul[0]-1:
				if inv:
					diagonal[x+1][y] = 1
					diagonal[x+1][y+(shape_mul[0])/2] = -1
				else:
					diagonal[x+1][y] = 0.5
					diagonal[x+1][y+(shape_mul[0])/2] = -0.5
				x=x+2
				break
		y=y+1
	return diagonal


def divide_componentes(transformada):
	mitad = transformada.shape[0]/2
	ca = transformada[0:mitad,0:mitad].copy()
	ch = transformada[0:mitad,mitad:].copy()
	cv = transformada[mitad:,0:mitad].copy()
	cd = transformada[mitad:,mitad:].copy()
	return ca, ch, cv, cd
#Obtiene los componenetes de la banda aplicandole la transformada
#banda: matriz a la cual se le aplica la transformada
#transformada: matriz con los valores para aplicar la transformada
#nivel: las veces que se le va a aplicar la transformada
def get_componentes(banda, diagonal, nivel):
	if nivel is not 0:
		#obtengo la transformada
		transformada = np.multiply(banda, diagonal)
		#optengo los componentes
		ca, ch, cv, cd = divide_componentes(transformada)
		#hago el siguiente nivel con los nuevos componentes
		diagonal_ca = get_matriz_transformada_inversa(ca, False)
		ca = get_componentes(ca, diagonal_ca, nivel-1)
		# uno los 4 componentes
		new_ca = np.concatenate((np.concatenate((ca, ch), axis=1), np.concatenate((cv, cd), axis=1)), axis=0)
		# les hago transformada inversa a la union de los componentes
		diagonal_inv_new_ca = get_matriz_transformada_inversa(new_ca, True)
		transformada_inv_new_ca = np.multiply(new_ca, diagonal_inv_new_ca)
		print '\t\ttransformada nivel %s aplicada' % (nivel)
		return transformada_inv_new_ca
	else:
		return banda
		

def main():
	input_mul = sys.argv[1]
	input_pan = sys.argv[2]
	nivel = int(sys.argv[3])
	output_fus = sys.argv[4]

	# (1) Leer las imagenes
	print 'Leyendo las imagenes...'
	image_mul = plt.imread(input_mul)
	shape_mul = image_mul.shape
	if shape_mul[2]:
		print '\tla imagen multiespectral tiene '+str(shape_mul[2])+' bandas y tamaño '+str(shape_mul[0])+'x'+str(shape_mul[1])
	else:
		print '\tla primera imagen no es multiespectral'
	image_pan = plt.imread(input_pan)
	shape_pan = image_pan.shape
	if len(shape_pan) == 2:
		print '\tla imagen Pancromatica tiene tamaño '+str(shape_pan[0])+'x'+str(shape_pan[1])
	else:
		print '\tla segunda imagen no es pancromatica'
	# (2) convertir la imagen a HSV
	print 'Conviertiendo RGB to HSV...'
	hsv_mul = colors.rgb_to_hsv(image_mul / 255.)
	plt.imshow(hsv_mul)
	plt.show()
	print '\timagen convertida a HSV satisfactoriamente...'
	H_mul = hsv_mul[:,:,0]
	S_mul = hsv_mul[:,:,1]
	V_mul = hsv_mul[:,:,2]
	plt.imshow(H_mul)
	plt.show()
	plt.imshow(S_mul)
	plt.show()
	plt.imshow(V_mul)
	plt.show()
	# (3) obtener los componentes del value y de la pancro
	print 'Aplicando la transformada...'
	diagonal = get_matriz_transformada_inversa(V_mul, False) # False: para hacer la transformada normal
	#print(np.matrix(diagonal))
	#obtengo los componentes de la pancromatica
	print '\ttransformada pan:'
	componentes_pan = get_componentes(image_pan, diagonal, 1) 
	cap, chp, cvp, cdp = divide_componentes(componentes_pan)
	print '\ttransformada val:'
	#obtengo los componentes del Value
	componentes_V = get_componentes(V_mul, diagonal, nivel)
	cav, chv, cvv, cdv = divide_componentes(componentes_V)
	# (4) combino los componentes adecuados de la pan y del value
	new_cav = np.concatenate((np.concatenate((cav, chp), axis=1), np.concatenate((cvp, cdp), axis=1)), axis=0)
	# (5) tranformada a los nuevos componentes para obtener new_V
	diagonal = get_matriz_transformada_inversa(new_cav, True)
	new_V = np.multiply(new_cav, diagonal)
	plt.imshow(new_V)
	plt.show()
	# (6) combino new_V con H y S
	hsv_mul[:,:,2] = new_V
	# (7) HSV_to_RGB
	new_RGB = colors.hsv_to_rgb(hsv_mul*255.)
	# (8) guardo la nueva imagen y tales
	#print(np.matrix(V_mul))
	#print(np.matrix(transformada))

print '************* ------ Script Exit  ------ *************'

'''
for y  in range(0,shape_mul[1]):
	for x  in range(0,shape_mul[0]):
		diagonal[x][y] = 0.5
		if not x == shape_mul[0]-1:
			diagonal[x+1][y] = -0.5
			x=x+2
		break




def getH(r, g, b, I):
    Min = r
    flag = 'r'
    if g < Min:
        Min = g
        flag = 'g'    
    if b < Min:
        Min = b
        flag = 'b'
        if g < b:
            Min = g
            flag = 'g'
    if flag == 'r':
        h = (b-r)/(I-765*r) + 255
    elif flag == 'g':
		h = (r - g) / (I - 765*g) + 510
    elif flag == 'b':
    	h = (g - b) / (I - 765*b)
    return h


def getS(r, g, b, I, H):
	if 0<=H<=255:
		s = (I - 765*b) /I
	elif 255<H<=510:
		s = (I - 765*r) /I
	elif 510<H<=765:
		s = (I - 765*g) /I
	else:
		pass


def RGB2IHS(r,g,b):
	# segun la toria de http://ij.ms3d.de/pdf/ihs_transforms.pdf
	# los valores de RGB deben estar entre 0 y 1
	r = [x + 1 for x in r]
	g = [x + 1 for x in g]
	b = [x + 1 for x in b]
	I = [x + y + z for x, y, z in zip(r, g, b)]
	H = [getH(x, y, z, a) for x, y, z, a in zip(r, g, b, I)]
	S = [getS(x, y, z, a, b) for x, y, z, a, b in zip(r, g, b, I, H)]
	return I, H, S


input_mul = sys.argv[1]
input_pan = sys.argv[2]
output_fus = sys.argv[3]

img = Image.open(input_mul)
print 'la imagen tiene '+str(len(img.getbands()))+' banda(s): '+str(img.getbands())
if len(img.getbands()) == 4:
	r, g, b, a = img.split()
else:
	r, g, b = img.split()
#print str(r)
r_list = list(r.getdata())
g_list = list(g.getdata())
b_list = list(b.getdata())

I, H, S = RGB2IHS(r_list,g_list,b_list)
'''

main()