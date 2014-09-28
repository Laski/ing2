from abc import ABCMeta, abstractmethod
from suministros import SUMINISTROS
import interfaz_usuario


class Supervisor(metaclass=ABCMeta):  # ex-filtro
    def __init__(self, sensor, suministrador_exceso, suministrador_defecto):
        self.sensor = sensor
        self.suministrador_exceso = suministrador_exceso
        self.suministrador_defecto = suministrador_defecto

    def tick(self):
        medida = self.sensor.medir()
        if self.falta(medida):
            self.suministrador_defecto.alertar()
        elif self.sobra(medida):
            self.suministrador_exceso.alertar()

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


class Suministrador:
    def __init__(self, actuador, medida_minima, responsable_secundario):
        self.actuador = actuador
        self.medida_minima = medida_minima
        self.responsable_secundario = responsable_secundario

    def alertar(self):
        respuesta_usuario = interfaz_usuario.ejecutar_intervencion()
        if respuesta_usuario == interfaz_usuario.NO:
            return
        elif respuesta_usuario == interfaz_usuario.TIMEOUT:
            if self.responsable_secundario.debo_cancelar_suministro():
                return
        self.actuador.ejecutar(self.medida_minima.cantidad)


class PlanMaestro:
    def __init__(self, estados_deseados):
        # estados_deseados debe ser un diccionario (EstadioPrincipal -> EstadoSuelo) que represente el estado
        # deseado del suelo para cada estadío fenológico principal
        self.estados_deseados = estados_deseados

    def estado_deseado(self, estadio):
        return self.estados_deseados[estadio]

    def humedad_deseada(self, estadio):
        return self.estado_deseado(estadio).humedad

    def ph_aceptado(self, estadio):
        return self.estado_deseado(estadio).ph

    def temperatura_aceptada(self, estadio):
        return self.estado_deseado(estadio).temperatura
