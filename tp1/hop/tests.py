#!/usr/bin/python3
import unittest
from unittest.mock import MagicMock, patch

from estados import Medida
from sensores import MOCK_SENSORES, PH
from builder import Reloj
from supervisores import SupervisorMinMax, SuministradorNulo


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


#class TestUS79ComoBotanicoQuieroProgramarSuministrosDeInsumos(unittest.TestCase):

    #def setUp(self):
        #self.humedad = SensorSuelo()
        #self.luz = SensorLuz()
        #self.gotero = ActuadorGotero()
        #self.lampara = ActuadorLampara()
        #self.reloj = Timer()
        #estados_deseados = {
            #'germinacion': {},
        #}
        #self.una_centra = CentralMetereologica(estados_deseados=estados_deseados)

        #self.hop = BuilderGerminacion()\
            #.con_timer(self.reloj)\
            #.con_plan_maestro(self.estados_deseados)\
            #.con_supervisor_para(self.humedad)\
            #.con_supervisor_para(self.luz)\
            #.agregar_actuador_para(self.gotero)\
            #.agregar_actuador_para(self.lampara)\
            #.con_responsables([self.una_interfaz_de_usuario, self.una_central])\
            #.crear()

    #def test_se_disminuye_la_intensidad_de_la_lampara(self):
        #apagar_luz = 1

        #medida_buena = Medida(25, 'C')
        #self.luz.medir = MagicMock(return_value=medida_buena)

        #with patch.object(self.lampara, 'ejecutar') as mock_lampara:
            #self.reloj.tick()

        #self.assertFalse(mock_lampara.ejecutar.called)

        #medida_peligrosa = Medida(30, 'C')
        #self.luz.medir = MagicMock(return_value=medida_peligrosa)

        #with patch.object(self.lampara, 'ejecutar') as mock_lampara:
            #self.reloj.tick()

        #mock_lampara.ejecutar.assert_called_with(apagar_luz)

    #def test_se_suministra_agua_si_la_humedad_es_moderada_en_el_estadio_germinacion(self):
        #suministrar_agua = 1

        #humedad_esperada = Medida(90, '%')
        #self.humedad.medir = MagicMock(return_value=humedad_esperada)

        #with patch.object(self.gotero, 'ejecutar') as mock_gotero:
            #self.reloj.tick()

        #self.assertFalse(mock_gotero.ejecutar.called)

        #humedad_moderada = Medida(60, '%')
        #self.humedad.medir = MogicMock(return_value=humedad_moderada)

        #with pathc.object(self.gotero, 'ejecutar') as mock_gotero:
            #self.reloj.tick()

        #mock_gotero.ejecutar.assert_called_with(suministrar_agua)

    #def test_se_informa_necesidad_suministros_abono(self):
        #pass


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
