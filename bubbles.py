#!/usr/bin/python
#coding: utf-8

#       CopyRight 2014 Allan Psicobyte (psicobyte@gmail.com)
#
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys, os, math, Image, ImageDraw

# Dimensiones para la imagen

WIDTH= 2000
HEIGHT= 2000


class Circle():
    '''
        Crea cada uno de las "burbujas" en función de los dígitos que se le suministran

        "angle" es el ángulo en el que está rotada respeto a la burbuja padre.
        "color" es el color que tendrá
        "sons" es el número de hijos (0 = 10)
    '''

    def __init__(self, angle, color, sons, parent= None):

        self.Parent = parent

        self.Sons = sons

        if self.Sons == 0: self.Sons = 10

        #Si es el primer círculo...
        if  self.Parent is None:

            self.CoorX = WIDTH / 2
            self.CoorY = HEIGHT / 2

            self.Radius =  HEIGHT / 4

            self.Generation = 0

        else:

            # Los círculos pares se dibujan fuera del padre, los impares dentro
            if angle % 2 == 0:
                multiplicador = 0.6666

            else:
                multiplicador = 1.3333

            self.CoorX = self.Parent.CoorX + (math.cos(math.pi * angle / 5) * self.Parent.Radius * multiplicador)
            self.CoorY = self.Parent.CoorY + (math.sin(math.pi * angle / 5) * self.Parent.Radius * multiplicador)

            self.Radius =  self.Parent.Radius / 3

            self.Generation = self.Parent.Generation + 1

        self.Color = set_color(color,self.Generation)

    def Draw(self,draw):

        inicioX = self.CoorX - self.Radius
        inicioY = self.CoorY - self.Radius
        finX = self.CoorX + self.Radius
        finY = self.CoorY + self.Radius

        draw.ellipse([(inicioX, inicioY), (finX, finY)], outline= "#000000", fill= self.Color)


def descendence(father):
    global array_digits, array_circles

    i = 0

    while i < father.Sons:

        angle= int(array_digits.pop(0))
        color= int(array_digits.pop(0))
        sons= int(array_digits.pop(0))

        array_circles.append(Circle(angle,color,sons,father))

        i = i + 1


def set_color(num,gen):

    hue= num * 36
    saturation= 25 + (gen * 10)
    lightness = 50 + (gen * 5)
    color = "hsl(" + str(hue) + ", " + str(saturation) + "%, " + str(lightness) + "%)"

    return color


def main():
    global array_digits, array_circles

    if len(sys.argv) > 2:

        numbers_file= os.path.abspath(sys.argv[1])
        image_file= os.path.abspath(sys.argv[2])

        try:
            fichero = open(numbers_file)
        except IOError:
            print "No se ha encontrado el archivo de dígitos en " +  numbers_file   
            sys.exit()

        cadena= fichero.read()
        fichero.close()

        array_digits = list(cadena)

        array_circles= []

        angle= int(array_digits.pop(0))
        color= int(array_digits.pop(0))
        sons= int(array_digits.pop(0))

        array_circles.append(Circle(angle,color,sons))

        iterations = 5

        i = 0

        while i < iterations:
            for elemento in array_circles:
                if elemento.Generation == i:
                    descendence(elemento)
            i = i + 1

        img = Image.new("RGB", (WIDTH, HEIGHT), "#000000")

        draw = ImageDraw.Draw(img)

        for elemento in array_circles:
            elemento.Draw(draw)

        img.save(image_file, "PNG")

    else:
        print "Modo de uso: " + __file__ + " archivo_numeros imagen_resultante"
        print "Ejemplo:     " + __file__ + " digitsofpi.txt picture.png"


main()

