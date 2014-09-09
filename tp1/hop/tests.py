#!/usr/bin/python3
import unittest
from datetime import datetime

from estados import ESTADIOS_PRINCIPALES, EstadoSuelo
from planes import PlanMaestro
from sensores import MockSensorSuelo, MockCentralMeteorologica


class Test(unittest.TestCase):
    def setUp(self):
        humedad_ejemplo             =   55.0
        PH_ejemplo                  =   7.1
        temperatura_ejemplo         =   23.0
        luz_ejemplo                 =   99.1
        hora_ejemplo                =   datetime.now().time()
        estimaciones_temperatura    =   [temperatura_ejemplo    for _ in range(24)]
        estimaciones_humedad        =   [humedad_ejemplo        for _ in range(24)]
        estimaciones_luz            =   [luz_ejemplo            for _ in range(24)]

        self.mock_sensor_suelo = MockSensorSuelo(humedad_ejemplo, PH_ejemplo, temperatura_ejemplo)
        self.mock_central_meteorologica = MockCentralMeteorologica(temperatura_ejemplo, humedad_ejemplo,
                                                                           luz_ejemplo, hora_ejemplo,
                                                                           estimaciones_temperatura,
                                                                           estimaciones_humedad, estimaciones_luz)
        self.estado_suelo_ejemplo = EstadoSuelo(humedad_ejemplo, PH_ejemplo, temperatura_ejemplo)

    def test_puedo_definir_un_plan_maestro(self):
        estados_deseados = {}
        for estadio_principal in ESTADIOS_PRINCIPALES.values():
            estados_deseados[estadio_principal] = self.estado_suelo_ejemplo
        plan_maestro = PlanMaestro(estados_deseados)

        estadio_prueba = ESTADIOS_PRINCIPALES[0]
        self.assertTrue(plan_maestro.humedad_deseada(estadio_prueba) == self.estado_suelo_ejemplo.humedad)


    def test_puedo_obtener_el_estado_actual(self):
        estado = self.mock_sensor_suelo.estado
        self.assertTrue(estado.humedad == self.estado_suelo_ejemplo.humedad)



if __name__ == '__main__':
    unittest.main()
