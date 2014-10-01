from responsables import ResponsableUsuario, ResponsableCentralMeteorologica
from suministros import SUMINISTROS, ACTUADORES, AGREGAR_FERTILIZANTE
from sensores import MOCK_SENSORES
from estados import ETAPAS, MOCK_ESTADO_SUELO


class PlanMaestro:
    def __init__(self, estados_deseados):
        # estados_deseados debe ser un diccionario (Etapa -> EstadoSuelo) que represente el estado
        # deseado del suelo para cada estadío fenológico principal
        self.estados_deseados = estados_deseados

    def estado_deseado(self, etapa):
        return self.estados_deseados[etapa]

    def humedad_deseada(self, etapa):
        return self.estado_deseado(etapa).humedad

    def ph_deseado(self, etapa):
        return self.estado_deseado(etapa).ph

    def temperatura_deseada(self, etapa):
        return self.estado_deseado(etapa).temperatura


class PlanDeSuministros:
    def __init__(self, actuadores_por_hora):
        # actuadores_por_hora debería ser una lista de 0 a 23 elementos, cada uno con un conjunto de actuadores que
        # deberia ejecutarse en ese momento
        self.actuadores_por_hora = actuadores_por_hora


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


class Reloj(Observable):
    def tick(self):         # abstraccion del reloj real, cada vez que cambie va a ser una hora nueva
        self.notificar()


class BuilderSupervisores:
    def __init__(self, plan_maestro, plan_de_suministros, sensores, actuadores):
        self.plan_maestro = plan_maestro
        self.sensores = sensores
        self.actuadores = actuadores
        self.suministradores = {}
        for suministro in SUMINISTROS:
            self.suministradores[suministro] = Suministrador()
        self.supervisores = []
        self.cambio_la_etapa(ETAPAS[0], plan_de_suministros)

    def cambio_la_etapa(self, etapa, plan_de_suministros):
        self.supervisores.clear()   # borro los supervisores anteriores
        # hay que mantener los estados
        estado_deseado = self.plan_maestro.estado_deseado(etapa)
        for actuador in self.actuadores:
            self.suministradores =


MOCK_PLAN_MAESTRO = PlanMaestro({etapa: MOCK_ESTADO_SUELO for etapa in ETAPAS})     # el estado deseado es el mismo para cualquier etapa
MOCK_PLAN_SUMINISTROS = [[AGREGAR_FERTILIZANTE] for i in range(24)]                 # se agrega fertilizante todas las horas
MOCK_BUILDER = BuilderSupervisores(MOCK_PLAN_MAESTRO, MOCK_PLAN_SUMINISTROS, MOCK_SENSORES, ACTUADORES)