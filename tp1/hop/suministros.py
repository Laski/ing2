from abc import ABCMeta, abstractmethod
from estados import Medida, MILILITROS, LUMENS, CM3


class Suministro:
    def __init__(self, nombre, medida_minima):
        self.nombre = nombre
        self.medida_minima = medida_minima


class Actuador(metaclass=ABCMeta):
    def __init__(self, nombre, suministro):
        self.nombre = nombre
        self.suministro = suministro

    def __hash__(self):
        return hash(self.nombre)

    @property
    def medida_minima(self):
        return self.suministro.medida_minima

    @abstractmethod
    def ejecutar(self, medida):
        pass


class MockActuador(Actuador):

    def __init__(self, nombre, suministro):
        super().__init__(nombre, suministro)
        self.ejecuto = False

    def ejecutar(self, medida):
        self.ejecuto = True
        print ('El actuador {0} se ejecuto con medida {1}'.format(self.nombre, medida))


AGUA = Suministro("Agua", Medida(5, MILILITROS))
LUZ = Suministro("Luz", Medida(5, LUMENS))
FERTILIZANTE = Suministro("Fertilizante", Medida(5, CM3))
ANTIBIOTICOS = Suministro("Antibióticos", Medida(5, CM3))
SUMINISTROS = AGUA, LUZ, FERTILIZANTE, ANTIBIOTICOS

ACCIONES            = REGAR,   AUMENTAR_LUZ,   DISMINUIR_LUZ,   AGREGAR_FERTILIZANTE,   AGREGAR_ANTIBIOTICOS = range(5)
ACCIONES_TEXTO      = "Regar", "Aumentar luz", "Disminuir luz", "Agregar fertilizante", "Agregar antibióticos"
ACCIONES_SUMINISTRO = AGUA,    LUZ,            LUZ,             FERTILIZANTE,           ANTIBIOTICOS
ACTUADORES = {}
for accion in ACCIONES:
    ACTUADORES[accion] = MockActuador(ACCIONES_TEXTO[accion], ACCIONES_SUMINISTRO[accion])
