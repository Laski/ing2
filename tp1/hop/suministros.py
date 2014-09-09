from abc import ABCMeta, abstractmethod


class Suministro(metaclass=ABCMeta):
    def __init__(self, nombre, actuador):
        self.nombre = nombre
        self.actuador = actuador


class RecursoAdministrable(Suministro):
    def suministrar(self):
        self.actuador.suministrar()


class RecursoRegulable(Suministro):
    def aumentar(self):
        self.actuador.agregar()

    def disminuir(self):
        self.actuador.disminuir()


class ActuadorRecursoAdministrable(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def suministrar(self):
        pass


class ActuadorRecursoRegulable(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def aumentar(self):
        pass

    @abstractmethod
    def disminuir(self):
        pass


class MockActuadorRecursoAdministrable(ActuadorRecursoAdministrable):
    def __init__(self):
        pass

    def suministrar(self):
        pass


class MockActuadorRecursoRegulable(ActuadorRecursoRegulable):
    def __init__(self):
        pass

    def aumentar(self):
        pass

    def disminuir(self):
        pass


SUMINISTROS=[Suministro("Agua", MockActuadorRecursoAdministrable()),
             Suministro("Luz y calor", MockActuadorRecursoRegulable()),
             Suministro("Fertilizante", MockActuadorRecursoAdministrable()),
             Suministro("Antibióticos", MockActuadorRecursoAdministrable())]