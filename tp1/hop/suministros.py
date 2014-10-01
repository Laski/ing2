from abc import ABCMeta, abstractmethod


SUMINISTROS = AGUA, LUZ, FERTILIZANTE, ANTIBIOTICOS = range(4)
SUMINISTROS_TEXTO = "Agua", "Luz", "Fertilizante", "Antibióticos"
ACCIONES = REGAR, AUMENTAR_LUZ, DISMINUIR_LUZ, AGREGAR_FERTILIZANTE, AGREGAR_ANTIBIOTICOS = range(5)
ACCIONES_TEXTO = "Regar", "Aumentar luz", "Disminuir luz", "Agregar fertilizante", "Agregar antibióticos"


class Actuador(metaclass=ABCMeta):
    def __init__(self, accion):
        self.nombre = ACCIONES_TEXTO[accion]

    @abstractmethod
    def ejecutar(self, medida):
        pass


class MockActuador(Actuador):
    def ejecutar(self, medida):
        pass


ACTUADORES = {}
for accion in ACCIONES:
    ACTUADORES[accion] = MockActuador(accion)