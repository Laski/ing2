from abc import ABCMeta, abstractmethod


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


class PlanDeSuministros:
    def __init__(self, plan_maestro, suministros):
        self.plan_maestro = plan_maestro
        self.suministros = suministros

    def que_hacer(self, plan_maestro, estadio_fenologico):
        estado_deseado = self.plan_maestro.estado_deseado(estadio_fenologico)
        acciones_recomendadas = None
        #TODO: implementar logica
        return acciones_recomendadas


class Accion(metaclass=ABCMeta):
    def __init__(self, suministro):
        self.suministro = suministro

    @abstractmethod
    def ejecutar(self):
        pass


class AccionSuministrar(Accion):
    def ejecutar(self):
        suministro.suministrar()


class AccionAumentar(Accion):
    def ejecutar(self):
        suministro.aumentar()


class AccionMantener(Accion):
    def ejecutar(self):
        pass


class AccionDisminuir(Accion):
    def ejecutar(self):
        suministro.disminuir()
