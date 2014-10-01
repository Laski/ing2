from abc import ABCMeta, abstractmethod
from responsables import SI, NO, TIMEOUT


class Observable(metaclass=ABCMeta):
    def __init__(self):
        self.observers = []

    def subscribir(self, observer):
        self.observers.append(observer)

    def desubscribir(self, observer):
        self.observers.remove(observer)

    def notificar(self):
        for observer in self.observers:
            observer.notificar()


class Supervisor(metaclass=ABCMeta):  # ex-filtro
    def __init__(self, sensor, suministrador_exceso, suministrador_defecto, observable):
        self.sensor = sensor
        self.suministrador_exceso = suministrador_exceso
        self.suministrador_defecto = suministrador_defecto
        observable.subscribir(self)

    def notificar(self):
        medida = self.sensor.medir()
        if self.falta(medida):
            self.suministrador_defecto.alerta()
        elif self.sobra(medida):
            self.suministrador_exceso.alerta()

    @abstractmethod
    def falta(self, medida):
        pass

    @abstractmethod
    def sobra(self, medida):
        pass


class SupervisorMinMax(Supervisor):
    def __init__(self, sensor, suministrador_exceso, suministrador_defecto, minimo, maximo):
        super().__init__(sensor, suministrador_exceso, suministrador_defecto)
        if minimo > maximo:
            raise ValueError("Mínimo es mayor que máximo")
        self.minimo = minimo
        self.maximo = maximo

    def falta(self, medida):
        return medida < self.minimo

    def sobra(self, medida):
        return medida > self.maximo


class SupervisorHora(Supervisor):
    def __init__(self, sensor, suministrador_exceso, suministrador_defecto, horas_aumento, horas_disminucion):
        super().__init__(sensor, suministrador_exceso, suministrador_defecto)
        self.horas_aumento = horas_aumento
        self.horas_disminucion = horas_disminucion

    def falta(self, hora):
        return hora in self.horas_aumento

    def sobra(self, hora):
        return hora in self.horas_disminucion


class Suministrador:
    def __init__(self, actuador, medida_minima, responsables):
        self.actuador = actuador
        self.medida_minima = medida_minima
        self.responsables = responsables

    def alerta(self):
        for responsable in self.responsables:
            respuesta = responsable.debo_cancelar_suministro(self)
            if respuesta == SI:
                return
            elif respuesta == NO:
                break
            elif respuesta == TIMEOUT:
                pass
            else:
                raise ValueError("Respuesta inválida de un responsable")
        self.actuador.ejecutar(self.medida_minima.cantidad)