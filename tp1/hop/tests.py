#!/usr/bin/python3
import unittest
from unittest.mock import MagicMock, patch

from estados import Medida, GRADOS, PORCIENTO
from sensores import MOCK_SENSORES, PH, TEMPERATURA, HUMEDAD
from builder import Reloj, MOCK_COORDINADOR
from supervisores import SupervisorMinMax, SuministradorNulo
from suministros import DISMINUIR_LUZ, ACTUADORES, REGAR


#class Test(unittest.TestCase):
    #def setUp(self):
        #humedad_ejemplo             =   55.0
        #PH_ejemplo                  =   7.1
        #temperatura_ejemplo         =   23.0
        #luz_ejemplo                 =   99.1
        #hora_ejemplo                =   datetime.now().time()
        #estimaciones_temperatura    =   [temperatura_ejemplo    for _ in range(24)]
        #estimaciones_humedad        =   [humedad_ejemplo        for _ in range(24)]
        #estimaciones_luz            =   [luz_ejemplo            for _ in range(24)]

        #self.mock_sensor_suelo = MockSensorSuelo(humedad_ejemplo, PH_ejemplo, temperatura_ejemplo)
        #self.mock_central_meteorologica = MockCentralMeteorologica(temperatura_ejemplo, humedad_ejemplo,
                                                                           #luz_ejemplo, hora_ejemplo,
                                                                           #estimaciones_temperatura,
                                                                           #estimaciones_humedad, estimaciones_luz)
        #self.estado_suelo_ejemplo = EstadoSuelo(humedad_ejemplo, PH_ejemplo, temperatura_ejemplo)

    #def test_puedo_definir_un_plan_maestro(self):
        #estados_deseados = {}
        #for estadio_principal in ESTADIOS_PRINCIPALES.values():
            #estados_deseados[estadio_principal] = self.estado_suelo_ejemplo
        #plan_maestro = PlanMaestro(estados_deseados)

        #estadio_prueba = ESTADIOS_PRINCIPALES[0]
        #self.assertTrue(plan_maestro.humedad_deseada(estadio_prueba) == self.estado_suelo_ejemplo.humedad)

    #def test_puedo_obtener_el_estado_actual(self):
        #estado = self.mock_sensor_suelo.estado
        #self.assertTrue(estado.humedad == self.estado_suelo_ejemplo.humedad)


class TestUS79ComoBotanicoQuieroProgramarSuministrosDeInsumos(unittest.TestCase):

    def setUp(self):
        self.actuador_lampara = ACTUADORES[DISMINUIR_LUZ]
        self.actuador_regar = ACTUADORES[REGAR]
        self.coordinador = MOCK_COORDINADOR
        self.sensor_temp = MOCK_SENSORES[TEMPERATURA]
        self.sensor_humedad = MOCK_SENSORES[HUMEDAD]
        self.reloj = self.coordinador.reloj

    def test_se_disminuye_la_intensidad_de_la_lampara(self):

        medida_buena = Medida(21, GRADOS)
        self.sensor_temp.medir = MagicMock(return_value=medida_buena)

        self.reloj.tick()
        self.assertFalse(self.actuador_lampara.ejecuto)

        medida_peligrosa = Medida(28, GRADOS)
        self.sensor_temp.medir = MagicMock(return_value=medida_peligrosa)
        self.assertFalse(self.actuador_lampara.ejecuto)
        self.reloj.tick()
        self.assertTrue(self.actuador_lampara.ejecuto)

    def test_se_suministra_agua_si_la_humedad_es_moderada_en_el_estadio_germinacion(self):

        humedad_esperada = Medida(50, PORCIENTO)
        self.sensor_humedad.medir = MagicMock(return_value=humedad_esperada)

        self.reloj.tick()

        self.assertFalse(self.actuador_regar.ejecuto)

        humedad_moderada = Medida(44, PORCIENTO)
        self.sensor_humedad.medir = MagicMock(return_value=humedad_moderada)
        self.reloj.tick()

        self.assertTrue(self.actuador_regar.ejecuto)


class TestUS75ComoJardineroQuieroVisualizarElEstadoDeLosSensores(unittest.TestCase):

    def setUp(self):
        self.reloj = Reloj()
        # aca falta ver como el sensor se subscribe al timer
        self.sensor_humedad = MOCK_SENSORES[PH]
        self.suministrador_defecto = SuministradorNulo()
        self.suministrador_exceso = SuministradorNulo()

        minimo = Medida(70, "%")
        maximo = Medida(90, "%")
        self.supervisor_suelo = SupervisorMinMax(self.sensor_humedad, self.suministrador_defecto, self.suministrador_exceso, self.reloj, minimo, maximo)
        self.reloj.subscribir(self.supervisor_suelo)

    def test_se_mide_humedad_65_se_ejecuta_el_suminsitrador_por_defecto(self):

        humedad_baja = Medida(65, '%')
        self.sensor_humedad.medir = MagicMock(return_value=humedad_baja)

        with patch.object(self.suministrador_defecto, 'alerta') as mock_suministrador:
            self.reloj.tick()
            self.assertFalse(mock_suministrador.alerta.called)


#class TestUS84ComoBotanicoQuieroDeclararUnPlanMaestroDeCultivo(unittest.TestCase):
    #pass


#class TestUS82ComoJardineroQuieroIngresarEstadosDefenologia(unittest.TestCase):
    #pass


#if __name__ == '__main__':
    #unittest.main()
