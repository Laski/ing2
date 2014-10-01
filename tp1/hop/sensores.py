from abc import ABCMeta, abstractmethod
from estados import Medida, MOCK_ESTADO_SUELO, MOCK_ESTADO_METEOROLOGICO, PORCIENTO, LUMENS

LLUVIA = Medida(100.0, PORCIENTO)     # qué porcentaje de humedad se considera lluvia
SOL    = Medida(100.0, LUMENS)        # qué cantidad de luz se considera sol
MEDICIONES = HUMEDAD, PH, TEMPERATURA, HORA = range(4)

class InterfazSensor(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def medir(self):
        # devuelve una Medida
        pass


class InterfazCentralMeteorologica(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def estado_actual(self):
        # devuelve un EstadoMeteorologico
        pass

    @abstractmethod
    def estimacion_estados_futuros(self):
        # devuelve una lista de 24 objetos EstadoMeteorologico
        pass

    @abstractmethod
    def hora_oficial(self):
        pass

    def va_a_llover(self):
        return LLUVIA in [estado.humedad for estado in self.estimacion_estados_futuros()]

    def va_a_salir_el_sol(self):
        return SOL in [estado.luz for estado in self.estimacion_estados_futuros()]


class MockSensor(InterfazSensor):
    def __init__(self, medida):
        super().__init__(self)
        self.medida = medida

    def medir(self):
        return self.medida


class MockSensorHora(InterfazSensor):
    def __init__(self, central_meteorologica):
        super().__init__(self)
        self.central_meteorologica = central_meteorologica

    def medir(self):
        return self.central_meteorologica.hora_oficial()


class MockCentralMeteorologica(InterfazCentralMeteorologica):
    def __init__(self, estado_percibido, hora_oficial, estimaciones):
        super().__init__(self)
        self._estado = estado_percibido
        self._estimaciones = estimaciones
        self._hora_oficial = hora_oficial

    def estado_actual(self):
        return self._estado

    def estimacion_estados_futuros(self):
        return self._estimaciones

    def hora_oficial(self):
        return self._hora_oficial



MOCK_CENTRAL_METEOROLOGICA = MockCentralMeteorologica(MOCK_ESTADO_METEOROLOGICO, 12)    # son las doce. siempre.

MOCK_SENSORES = {HUMEDAD: MockSensor(MOCK_ESTADO_SUELO.humedad),
                 PH: MockSensor(MOCK_ESTADO_SUELO.PH),
                 TEMPERATURA: MockSensor(MOCK_ESTADO_SUELO.temperatura),
                 HORA: MockSensorHora(MOCK_CENTRAL_METEOROLOGICA)}
