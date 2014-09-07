class PlanMaestro:
    def __init__(self, plan):
        self.plan = plan

    def programar_plan(self, plan):
        self.plan = plan

    def humedad_aceptada(self, estado):
        return self.plan[estado].humedad

    def ph_aceptado(self, estado):
        return self.plan[estado].ph

    def temperatura_aceptada(self, estado):
        return self.plan[estado].ph


class PlanDeSuministros:
    def __init__(self, plan, suministros):
        self.plan = plan
        self.suministros = suministros

    def reprogramar_plan(self, plan):
        self.plan = plan

    def que_hacer(self, plan_maestro, estado):
        pass
