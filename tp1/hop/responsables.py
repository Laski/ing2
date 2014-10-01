from abc import ABCMeta, abstractmethod
from sensores import MOCK_CENTRAL_METEOROLOGICA
from suministros import ACTUADORES, REGAR, AUMENTAR_LUZ

RESPUESTAS = SI, NO, TIMEOUT = range(3)


class Responsable(metaclass=ABCMeta): # interfaz
    @abstractmethod
    def debo_cancelar_suministro(self, suministrador):
        pass


class ResponsableUsuario(Responsable):
    def __init__(self, interfaz_usuario):
        self.interfaz_usuario = interfaz_usuario

    def debo_cancelar_suministro(self, suministrador):
        actuador = suministrador.actuador
        cantidad = suministrador.medida
        return self.interfaz_usuario.consultar(actuador.nombre, cantidad)


class ResponsableCentralMeteorologica(Responsable):
    def __init__(self, interfaz_central):
        self.interfaz_central = interfaz_central

    def debo_cancelar_suministro(self, suministrador):
        actuador = suministrador.actuador
        if actuador == ACTUADORES[REGAR] and self.interfaz_central.va_a_llover():
            return SI
        elif actuador == ACTUADORES[AUMENTAR_LUZ] and self.interfaz_central.va_a_salir_el_sol():
            return SI
        else:
            return TIMEOUT  # paso la responsabilidad al que siga


class MockInterfazUsuario:
    def consultar(self, nombre, cantidad):
        return TIMEOUT      # usuario que no hace nada


MOCK_RESPONSABLE_USUARIO = ResponsableUsuario(MockInterfazUsuario())
MOCK_RESPONSABLE_CENTRAL_METEOROLOGICA = ResponsableCentralMeteorologica(MOCK_CENTRAL_METEOROLOGICA)
