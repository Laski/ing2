# -*- coding: utf-8 -*-


class EstadioPrincipal:
    def __init__(self, nombre):
        self.nombre = nombre

    def __hash__(self):
        # para poder usarlo como clave de diccionarios
        return hash(self.nombre)


ESTADIOS_PRINCIPALES = {}   # diccionario (número de estadío -> EstadioPrincipal)
datos_estadios_principales = [(0, "Germinación"),
                              (1, "Desarrollo de las hojas"),
                              (2, "Formación de brotes laterales"),
                              (5, "Aparición del órgano floral"),
                              (6, "Floración"),
                              (7, "Formación del fruto"),
                              (8, "Maduración"),
                              (9, "Senescencia")]
for (numero, nombre) in datos_estadios_principales:
    ESTADIOS_PRINCIPALES[numero] = EstadioPrincipal(nombre)


class EstadoSuelo:
    def __init__(self, humedad=50.0, PH=7.0, temperatura=20.0):
        self.humedad = humedad
        self.PH = PH
        self.temperatura = temperatura


class EstadoMeteorologico:
    def __init__(self, temperatura=20.0, humedad=50.0, luz=100.0):
        self.temperatura = temperatura
        self.humedad = humedad
        self.luz = luz


class EstadoFenologico:     # quizás no hace falta
    def __init__(self, estadio_principal=ESTADIOS_PRINCIPALES[0], altura=0, cantidad_hojas=0,
                 cantidad_brotes=0, cantidad_flores=0, cantidad_frutos=0, porcentaje_frutos_maduros=0.0):
        self.estadio_principal = estadio_principal
        self.altura = altura
        self.cantidad_hojas = cantidad_hojas
        self.cantidad_brotes = cantidad_brotes
        self.cantidad_flores = cantidad_flores
        self.cantidad_frutos = cantidad_frutos
        self.porcentaje_frutos_maduros = porcentaje_frutos_maduros
