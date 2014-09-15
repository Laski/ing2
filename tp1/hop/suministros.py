from abc import ABCMeta, abstractmethod

SUMINISTROS = AGUA, LUZ, FERTILIZANTE, ANTIBIOTICOS = range(4)
SUMINISTROS_TEXTO = "Agua", "Luz", "Fertilizante", "Antibióticos"
ACCIONES = AUMENTAR, DISMINUIR = range(2)

ACCIONES_VALIDAS = [(AGUA, AUMENTAR), (LUZ, AUMENTAR), (LUZ, DISMINUIR), (FERTILIZANTE, AUMENTAR), (ANTIBIOTICOS, AUMENTAR)]

ACTUADORES = {AGUA: MockActuador(), LUZ: MockActuador(), FERTILIZANTE: MockActuador(), ANTIBIOTICOS: MockActuador()}

class AccionFactory:
    def __init__(self):
        pass

    def get_accion(recurso, efecto_deseado, cantidad):
        if (recurso, efecto_deseado) not in ACCIONES_VALIDAS:
            raise ValueError("Combinación no válida de acción y recurso")
        if efecto_deseado == AUMENTAR:
            return AccionAumentar(ACTUADORES[recurso])
        elif efecto_deseado == DISMINUIR:
            return AccionDisminuir(ACTUADORES[recurso])
        else:
            raise ValueError("No debería pasar")


class Accion(metaclass=ABCMeta):
    def __init__(self, actuador):
        self.actuador = actuador

    @abstractmethod
    def ejecutar(self):
        pass


class AccionAumentar(Accion):
    def ejecutar(self):
        actuador.aumentar()


class AccionDisminuir(Accion):
    def ejecutar(self):
        actuador.disminuir()


class Actuador(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def aumentar(self):
        pass

    @abstractmethod
    def disminuir(self):
        pass


class MockActuador(Actuador):
    def __init__(self):
        pass

    def aumentar(self):
        pass

    def disminuir(self):
        pass