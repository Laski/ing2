from abc import ABCMeta, abstractmethod
from responsables import SI, NO, TIMEOUT


class Supervisor(metaclass=ABCMeta):  # ex-filtro
    def __init__(self, sensor, suministrador_defecto, suministrador_exceso, observable):
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
    def __init__(self, sensor, suministrador_defecto, suministrador_exceso, observable, minimo, maximo):
        super().__init__(sensor, suministrador_defecto, suministrador_exceso, observable)
        if minimo > maximo:
            raise ValueError("Mínimo es mayor que máximo")
        self.minimo = minimo
        self.maximo = maximo

    def falta(self, medida):
        return medida < self.minimo

    def sobra(self, medida):
        return medida > self.maximo


class SupervisorHora(Supervisor):
    def __init__(self, sensor, suministrador, horas, observable):
        super().__init__(sensor, suministrador, SuministradorNulo(), observable)
        self.horas = horas

    def falta(self, hora):
        return hora in self.horas

    def sobra(self, hora):
        # siempre "falta", la logica de aumentar o disminuir esta en el actuador
        return False


class Suministrador:
    def __init__(self, actuador, medida, responsables):
        self.actuador = actuador
        self.medida = medida
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
        self.actuador.ejecutar(self.medida.cantidad)


class SuministradorNulo(Suministrador):
    def alerta(self):
        pass
