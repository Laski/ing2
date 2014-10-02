UNIDADES = MILILITROS, LUMENS, CM3, PH_U, GRADOS, PORCIENTO = range(6)


class Medida:
    def __init__(self, cantidad, unidad):
        self._cantidad = cantidad
        self._unidad = unidad

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def unidad(self):
        return self._unidad

    # para que sean comparables:
    def __lt__(self, other):
        self.verificar_unidad(other)
        return self.cantidad < other.cantidad
    def __le__(self, other):
        self.verificar_unidad(other)
        return self.cantidad <= other.cantidad
    def __eq__(self, other):
        self.verificar_unidad(other)
        return self.cantidad == other.cantidad
    def __ge__(self, other):
        self.verificar_unidad(other)
        return self.cantidad >= other.cantidad
    def __gt__(self, other):
        self.verificar_unidad(other)
        return self.cantidad > other.cantidad
    def __ne__(self, other):
        self.verificar_unidad(other)
        return self.cantidad != other.cantidad
    def verificar_unidad(self, other):
        if self.unidad != other.unidad:
            raise TypeError("Intentando comparar medidas de unidades distintas")


class Etapa:
    def __init__(self, nombre):
        self.nombre = nombre

    def __hash__(self):
        # para poder usarlo como clave de diccionarios
        return hash(self.nombre)


ETAPAS = {}   # diccionario (número de estadío -> Etapa)
datos_etapas = [(0, "Germinación"),
                (1, "Desarrollo de las hojas"),
                (2, "Formación de brotes laterales"),
                (5, "Aparición del órgano floral"),
                (6, "Floración"),
                (7, "Formación del fruto"),
                (8, "Maduración"),
                (9, "Senescencia")]
for (numero, nombre) in datos_etapas:
    ETAPAS[numero] = Etapa(nombre)


class EstadoSuelo:
    def __init__(self, humedad, ph, temperatura):
        self.humedad = humedad
        self.ph = ph
        self.temperatura = temperatura


class EstadoMeteorologico:
    def __init__(self, temperatura, humedad, luz):
        self.temperatura = temperatura
        self.humedad = humedad
        self.luz = luz


MOCK_ESTADO_SUELO = EstadoSuelo(humedad=Medida(50.0, PORCIENTO), ph=Medida(7.0, PH_U), temperatura=Medida(20.0, GRADOS))
MOCK_ESTADO_METEOROLOGICO = EstadoMeteorologico(temperatura=Medida(20.0, GRADOS), humedad=Medida(50.0, PORCIENTO),
                                                luz=Medida(100.0, LUMENS))
