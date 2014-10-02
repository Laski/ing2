from abc import ABCMeta

from suministros import ACTUADORES, ACCIONES, REGAR, AUMENTAR_LUZ, DISMINUIR_LUZ, AGREGAR_FERTILIZANTE, AGREGAR_ANTIBIOTICOS
from sensores import MOCK_SENSORES, HUMEDAD, TEMPERATURA, HORA
from estados import ETAPAS, MOCK_ESTADO_SUELO, CM3, Medida
from responsables import MOCK_RESPONSABLE_USUARIO, MOCK_RESPONSABLE_CENTRAL_METEOROLOGICA
from supervisores import Suministrador, SupervisorMinMax, SupervisorHora, SuministradorNulo


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
    def tick(self):         # abstraccion del reloj real, cada vez que se llame va a ser una hora nueva
        self.notificar()


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
    def __init__(self, actuadores_por_hora, medida_por_actuador):
        # actuadores_por_hora debería ser una lista de 24 elementos, cada uno con una lista de actuadores que
        # deberia ejecutarse en ese momento
        self.actuadores_por_hora = actuadores_por_hora
        self.medida_por_actuador = medida_por_actuador

    def horas_para(self, actuador):
        return [i for i in range(len(self.actuadores_por_hora)) if actuador in self.actuadores_por_hora[i]]

    def medida_para(self, actuador):
        return self.medida_por_actuador[actuador]

    def actuadores_programados(self):
        return self.actuadores_por_hora


class Coordinador:
    def __init__(self, plan_maestro, plan_de_suministros, sensores, actuadores, responsables):
        self.plan_maestro = plan_maestro
        self.sensores = sensores
        self.actuadores = actuadores
        self.responsables = responsables
        self.supervisores = []          # van variando por etapa
        self.suministradores = {}
        self.reloj = Reloj()
        for accion in ACCIONES:
            # tengo que tener minimo un suministrador por cada accion posible
            actuador = self.actuadores[accion]
            self.suministradores[accion] = Suministrador(actuador, actuador.medida_minima, self.responsables)
        self.cambio_la_etapa(ETAPAS[0], plan_de_suministros)

    def cambio_la_etapa(self, etapa, nuevo_plan_de_suministros):
        self.supervisores.clear()   # borro los supervisores anteriores
        self.plan_de_suministros = nuevo_plan_de_suministros
        # hay que mantener los estados deseados y ejecutar los suministros programados

        # primero intento mantener los estados deseados con Supervisores MinMax
        estado_deseado = self.plan_maestro.estado_deseado(etapa)

        self.crear_min_max(HUMEDAD, estado_deseado.humedad, self.suministradores[REGAR], SuministradorNulo)
        self.crear_min_max(TEMPERATURA, estado_deseado.temperatura, self.suministradores[AUMENTAR_LUZ],
                           self.suministradores[DISMINUIR_LUZ])

        # ahora los suministros programados con Supervisores Hora
        for actuadores_hora in self.plan_de_suministros.actuadores_programados():
            for actuador in actuadores_hora:
                self.crear_programado(self.plan_de_suministros.horas_para(actuador),
                                      self.plan_de_suministros.medida_para(actuador),
                                      actuador)

    def crear_min_max(self, medicion, deseada, suministrador_defecto, suministrador_exceso):
        min_ = Medida(deseada.cantidad * 0.9, deseada.unidad)        # con _ al final para que no tape a la funcion min()
        max_ = Medida(deseada.cantidad * 1.1, deseada.unidad)        # idem
        supervisor = SupervisorMinMax(sensor=self.sensores[medicion],
                                      suministrador_defecto=suministrador_defecto,
                                      suministrador_exceso=suministrador_exceso,
                                      observable=self.reloj,
                                      minimo=min_,
                                      maximo=max_)
        self.supervisores.append(supervisor)

    def crear_programado(self, horas, medida, actuador):
        suministrador = Suministrador(actuador, medida, self.responsables)
        supervisor = SupervisorHora(sensor=self.sensores[HORA],
                                    suministrador=suministrador,
                                    horas=horas,
                                    observable=self.reloj)
        self.supervisores.append(supervisor)


# el estado deseado es el mismo para cualquier etapa
MOCK_PLAN_MAESTRO = PlanMaestro({etapa: MOCK_ESTADO_SUELO for etapa in ETAPAS.values()})
# se agrega fertilizante todas las horas pares, antibioticos las impares
lista_plan_suministros = [[ACTUADORES[AGREGAR_FERTILIZANTE]] if i % 2 == 0 else [ACTUADORES[AGREGAR_ANTIBIOTICOS]] for i in range(24)]
medidas_plan_suministros = {
    ACTUADORES[AGREGAR_FERTILIZANTE]: Medida(50.0, CM3),
    ACTUADORES[AGREGAR_ANTIBIOTICOS]: Medida(50.0, CM3),
    ACTUADORES[REGAR]: Medida(1, CM3),
    ACTUADORES[AUMENTAR_LUZ]: True,
    ACTUADORES[DISMINUIR_LUZ]: False,
}
MOCK_PLAN_SUMINISTROS = PlanDeSuministros(lista_plan_suministros, medidas_plan_suministros)
MOCK_RESPONSABLES = [MOCK_RESPONSABLE_USUARIO, MOCK_RESPONSABLE_CENTRAL_METEOROLOGICA]
MOCK_COORDINADOR = Coordinador(MOCK_PLAN_MAESTRO, MOCK_PLAN_SUMINISTROS, MOCK_SENSORES, ACTUADORES, MOCK_RESPONSABLES)
