from responsables import ResponsableUsuario, ResponsableCentralMeteorologica
from suministros import ACTUADORES, REGAR, AUMENTAR_LUZ, DISMINUIR_LUZ, AGREGAR_FERTILIZANTE, AGREGAR_ANTIBIOTICOS
from estados import ETAPAS

class PlanMaestro:
    def __init__(self, estados_deseados):
        # estados_deseados debe ser un diccionario (Etapa -> EstadoSuelo) que represente el estado
        # deseado del suelo para cada estadío fenológico principal
        self.estados_deseados = estados_deseados

    def estado_deseado(self, etapa):
        return self.estados_deseados[etapa]

    def humedad_deseada(self, etapa):
        return self.estado_deseado(etapa).humedad

    def ph_aceptado(self, etapa):
        return self.estado_deseado(etapa).ph

    def temperatura_aceptada(self, etapa):
        return self.estado_deseado(etapa).temperatura


class PlanDeSuministros:
    def __init__(self, actuadores_por_hora):
        # actuadores_por_hora debería ser una lista de 0 a 23 elementos, cada uno con un conjunto de actuadores que
        # deberia ejecutarse en ese momento
        self.actuadores_por_hora = actuadores_por_hora


class BuilderSupervisores:
    def __init__(self, plan_maestro, plan_de_suministros):
        self.plan_maestro = plan_maestro
        self.plan_de_suministros = plan_de_suministros
        self.cambio_la_etapa(ETAPAS[0])
        self.sensores =
        self.supervisores = []

    def cambio_la_etapa(self, etapa):
        estado_deseado = self.plan_maestro.estado_deseado(etapa)
