from abc import ABCMeta, abstractmethod

from estados import EstadoSuelo, EstadoMeteorologico


class SensorSuelo(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @property   # para que sea de solo lectura
    @abstractmethod
    def estado(self):
        # devuelve un EstadoSuelo
        pass


class CentralMeteorologica(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @property
    @abstractmethod
    def estado(self):
        # devuelve un EstadoMeteorologico
        pass

    @property
    @abstractmethod
    def estimacion_estados_futuros(self):
        # debería devolver una lista de 24 objetos EstadoMeteorologico
        pass

    @property
    @abstractmethod
    def hora_oficial(self):
        pass


class MockSensorSuelo(SensorSuelo):
    def __init__(self, humedad_percibida, PH_percibido, temperatura_percibida):
        self._estado = EstadoSuelo(humedad_percibida, PH_percibido, temperatura_percibida)

    @property
    def estado(self):
        return self._estado


class MockCentralMeteorologica(CentralMeteorologica):
    def __init__(self, temperatura_percibida, humedad_percibida, luz_percibida, hora_oficial,
                 estimaciones_temperatura, estimaciones_humedad, estimaciones_luz):
        self._estado = EstadoMeteorologico(temperatura_percibida, humedad_percibida, luz_percibida)
        self._estimaciones = [EstadoMeteorologico(estimaciones_temperatura[i],
                                                 estimaciones_humedad[i],
                                                 estimaciones_luz[i])
                             for i in range(len(estimaciones_temperatura))]
        self._hora_oficial = hora_oficial

    @property
    def estado(self):
        return self._estado

    @property
    def estimacion_estados_futuros(self):
        return self._estimaciones

    @property
    def hora_oficial(self):
        return self._hora_oficial