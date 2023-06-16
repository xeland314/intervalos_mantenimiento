from datetime import datetime, timedelta
from enum import Enum

class Kilometraje:
    def __init__(self, valor, unidad, fecha=None):
        self.valor = valor
        self.unidad = unidad
        self.fecha = datetime.now() if fecha is None else fecha

class Vehiculo:
    def __init__(self, nombre, kilometraje):
        self.nombre = nombre
        self.kilometraje = kilometraje
        self.bitacora = []
        self.bitacora.append(kilometraje)

    def agregar_kilometraje(self, valor, unidad, fecha=None):
        """
        Agrega un nuevo registro de kilometraje a la bitácora del vehículo.

        Args:
            valor (float): El valor del kilometraje.
            unidad (str): La unidad de medida del kilometraje.
            fecha (datetime, optional): La fecha y hora en que se registró el kilometraje.
            Si no se especifica, se usa la fecha y hora actual.
        """
        self.bitacora.append(Kilometraje(valor, unidad, fecha))

    @property
    def ultimo_kilometraje(self):
        if not self.bitacora:
            return None
        return max(self.bitacora, key=lambda x: x.fecha)

    @property
    def primer_kilometraje(self):
        if not self.bitacora:
            return None
        return min(self.bitacora, key=lambda x: x.fecha)

class Tareas(Enum):
    A = "Ajustar"
    I = "Inspeccionar"
    R = "Reparacion"
    T = "Ajustar Torque"
    L = "Lubricar o engrasar"

class Sistemas(Enum):
    FRENOS = "Frenos"
    MOTOR = "Motor"
    LLANTAS = "Llantas"

class Operacion:
    def __init__(self, tarea, sistema):
        self.tarea = tarea
        self.sistema = sistema

    def __repr__(self) -> str:
        return f"<{self.sistema} - {self.tarea}>"

class OperacionKilometraje(Operacion):
    def __init__(self, tarea, sistema, kilometraje):
        super().__init__(tarea, sistema)
        self.kilometraje = kilometraje

    def __str__(self) -> str:
        return f"{self.sistema} - {self.tarea} - {self.kilometraje}"

class OperacionTiempo(Operacion):
    def __init__(self, tarea, sistema, tiempo):
        super().__init__(tarea, sistema)
        self.tiempo = tiempo

    def __str__(self) -> str:
        return f"{self.sistema} - {self.tarea} - {self.tiempo}"

class HojaMantenimiento:
    def __init__(self, vehiculo):
        self.vehiculo = vehiculo
        self.operaciones = []

    def agregar_operacion(self, operacion):
        self.operaciones.append(operacion)

    def hallar_ultimas_inspecciones_kilometraje(self, operacion):
        if not isinstance(operacion, OperacionKilometraje):
            raise ValueError("La operación debe ser de tipo OperacionKilometraje")
        ultimo_kilometraje = self.vehiculo.ultimo_kilometraje
        if ultimo_kilometraje is None:
            return []
        intervalo_kilometraje = range(
            0,
            int(ultimo_kilometraje.valor) + 1,
            operacion.kilometraje,
        )
        return list(intervalo_kilometraje)

    def hallar_ultimas_inspecciones_tiempo(self, operacion):
        if not isinstance(operacion, OperacionTiempo):
            raise ValueError("La operación debe ser de tipo OperacionTiempo")
        primer_kilometraje = self.vehiculo.primer_kilometraje
        if primer_kilometraje is None:
            return []
        fecha_inicial = primer_kilometraje.fecha
        fecha_final = datetime.now()
        dias_totales = (fecha_final - fecha_inicial).days
        intervalo_tiempo = range(0,dias_totales + 1,operacion.tiempo)
        fechas_inspeccion = [(fecha_inicial + timedelta(days=d)) for d in intervalo_tiempo]
        return fechas_inspeccion

    def hallar_proxima_inspeccion_kilometraje(self, operacion):
        if not isinstance(operacion, OperacionKilometraje):
            raise ValueError("La operación debe ser de tipo OperacionKilometraje")
        ultimo_kilometraje = self.vehiculo.ultimo_kilometraje
        if ultimo_kilometraje is None:
            return None
        proximo_kilometraje = ((ultimo_kilometraje.valor // operacion.kilometraje) + 1) * operacion.kilometraje
        return proximo_kilometraje

    def hallar_proxima_inspeccion_tiempo(self, operacion):
        if not isinstance(operacion, OperacionTiempo):
            raise ValueError("La operación debe ser de tipo OperacionTiempo")
        primer_kilometraje = self.vehiculo.primer_kilometraje
        if primer_kilometraje is None:
            return None
        fecha_inicial = primer_kilometraje.fecha
        fecha_final = datetime.now()
        dias_totales = (fecha_final - fecha_inicial).days
        proxima_fecha = fecha_inicial + timedelta(days=((dias_totales // operacion.tiempo) + 1) * operacion.tiempo)
        return proxima_fecha

    def hallar_ultima_inspeccion_kilometraje(self, operacion):
        if not isinstance(operacion, OperacionKilometraje):
            raise ValueError("La operación debe ser de tipo OperacionKilometraje")
        ultimo_kilometraje = self.vehiculo.ultimo_kilometraje
        if ultimo_kilometraje is None:
            return None
        ultima_inspeccion = (ultimo_kilometraje.valor // operacion.kilometraje) * operacion.kilometraje
        return ultima_inspeccion

    def hallar_ultima_inspeccion_tiempo(self, operacion):
        if not isinstance(operacion, OperacionTiempo):
            raise ValueError("La operación debe ser de tipo OperacionTiempo")
        primer_kilometraje = self.vehiculo.primer_kilometraje
        if primer_kilometraje is None:
            return None
        fecha_inicial = primer_kilometraje.fecha
        fecha_final = datetime.now()
        dias_totales = (fecha_final - fecha_inicial).days
        ultima_fecha = fecha_inicial + timedelta(days=(dias_totales // operacion.tiempo) * operacion.tiempo)
        return ultima_fecha

if __name__ == "__main__":
    mi_vehiculo = Vehiculo("Mi auto", Kilometraje(0, "km", datetime(2023, 4, 1)))
    mi_vehiculo.agregar_kilometraje(1000, "km")
    mi_hoja_mantenimiento = HojaMantenimiento(mi_vehiculo)
    mi_hoja_mantenimiento.agregar_operacion(
        OperacionKilometraje(Tareas.I.value,Sistemas.FRENOS.value, 100
    ))
    mi_hoja_mantenimiento.agregar_operacion(
        OperacionTiempo(Tareas.L.value, Sistemas.MOTOR.value, 30
    ))
    inspecciones_kilometraje = mi_hoja_mantenimiento.hallar_ultimas_inspecciones_kilometraje(
        mi_hoja_mantenimiento.operaciones[0]
    )
    inspecciones_tiempo = mi_hoja_mantenimiento.hallar_ultimas_inspecciones_tiempo(
        mi_hoja_mantenimiento.operaciones[1]
    )
    print(inspecciones_kilometraje)
    print(inspecciones_tiempo)
    print(mi_hoja_mantenimiento.hallar_proxima_inspeccion_kilometraje(
        mi_hoja_mantenimiento.operaciones[0]
    ))
    print(mi_hoja_mantenimiento.hallar_proxima_inspeccion_tiempo(
        mi_hoja_mantenimiento.operaciones[1]
    ))

    ultima_inspeccion_kilometraje = mi_hoja_mantenimiento.hallar_ultima_inspeccion_kilometraje(
        mi_hoja_mantenimiento.operaciones[0]
    )
    ultima_inspeccion_tiempo = mi_hoja_mantenimiento.hallar_ultima_inspeccion_tiempo(
        mi_hoja_mantenimiento.operaciones[1]
    )
    print(ultima_inspeccion_kilometraje)
    print(ultima_inspeccion_tiempo)
