#!/usr/bin/python3
import sys
import os
import unittest


class Test(unittest.Testcase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_una_planta_nueva_esta_germinando(self):
        api.nueva_planta()
        estado = api.get_estado_planta()
        self.assertTrue(estado.fenologia == estados.germinacion)
