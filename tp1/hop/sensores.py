from abc import ABCMeta, abstractmethod

from estados import EstadoSuelo, EstadoMeteorologico

UNIDADES = MILILITROS, LUMENS, PH = range(3)


class Medida:
    def __init__(self, cantidad, unidad):
        self._cantidad = cantidad
        self._unidad = unidad

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def unidad(self):
        return self._unidad

    # para que sean comparables:
    def __lt__(self, other):
        self.verificar_unidad(other)
        return self.cantidad < other.cantidad

    def __le__(self, other):
        self.verificar_unidad(other)
        return self.cantidad <= other.cantidad

    def __eq__(self, other):
        self.verificar_unidad(other)
        return self.cantidad == other.cantidad

    def __ge__(self, other):
        self.verificar_unidad(other)
        return self.cantidad >= other.cantidad

    def __gt__(self, other):
        self.verificar_unidad(other)
        return self.cantidad > other.cantidad

    def __ne__(self, other):
        self.verificar_unidad(other)
        return self.cantidad != other.cantidad

    def verificar_unidad(self, other):
        if self.unidad != other.unidad:
            raise TypeError("Intentando comparar medidas de unidades distintas")


class InterfazSensor:

    def __init__(self):
        pass

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


class MockSensorSuelo:
    def __init__(self, humedad_percibida, PH_percibido, temperatura_percibida):
        self._estado = EstadoSuelo(humedad_percibida, PH_percibido, temperatura_percibida)

    @property
    def estado(self):
        return self._estado


class MockCentralMeteorologica:
    def __init__(self, temperatura_percibida, humedad_percibida, luz_percibida, hora_oficial,
                 estimaciones_temperatura, estimaciones_humedad, estimaciones_luz):
        self._estado = EstadoMeteorologico(temperatura_percibida, humedad_percibida, luz_percibida)
        self._estimaciones = [EstadoMeteorologico(estimaciones_temperatura[i],
                                                 estimaciones_humedad[i],
                                                 estimaciones_luz[i])
                             for i in range(len(estimaciones_temperatura))]
        self._hora_oficial = hora_oficial

    @property
    def estado_actual(self):
        return self._estado

    @property
    def estimacion_estados_futuros(self):
        return self._estimaciones

    @property
    def hora_oficial(self):
        return self._hora_oficial
