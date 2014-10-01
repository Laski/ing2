from abc import ABCMeta, abstractmethod
from suministros import ACTUADORES, REGAR, AUMENTAR_LUZ

SI, NO, TIMEOUT = range(3)


class Responsable(metaclass=ABCMeta): # interfaz
    @abstractmethod
    def debo_cancelar_suministro(self, suministrador):
        pass


class ResponsableUsuario(metaclass=ABCMeta):
    def __init__(self, interfaz_usuario):
        self.interfaz_usuario = interfaz_usuario

    def debo_cancelar_suministro(self, suministrador):
        actuador = suministrador.actuador
        cantidad = suministrador.medida_minima
        return self.interfaz_usuario.consultar(actuador.nombre, cantidad)


class ResponsableCentralMeteorologica(metaclass=ABCMeta):
    def __init__(self, interfaz_central):
        self.interfaz_central = interfaz_central

    def debo_cancelar_suministro(self, suministrador):
        actuador = suministrador.actuador
        if actuador == ACTUADORES[REGAR] and self.interfaz_central.va_a_llover():
            return True
        elif actuador == ACTUADORES[AUMENTAR_LUZ] and self.interfaz_central.va_a_salir_el_sol():
            return True
        else:
            return False