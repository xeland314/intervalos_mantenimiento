from datetime import date, timedelta

class Intervalo:
    """
    Esta clase representa un intervalo de valores enteros.
    """

    def __init__(self, values: list):
        """
        Inicializa un objeto Intervalo con una lista de valores enteros.
        """
        self.values = values

    def generate_interval(self, index: int) -> list:
        """
        Genera una lista de valores en el intervalo especificado por el índice dado.
        """
        max_value = max(self.values)
        interval = self.values[index]
        result = [i for i in range(0, max_value + 1, interval)]
        return result

    def get_interval_subdivision(self, value: int) -> tuple:
        """
        Obtiene la subdivisión del intervalo que contiene el valor dado.
        """
        if value < 0:
            raise ValueError("Value must be greater than or equal to 0")
        interval = self.values[0]
        max_value = max(self.values)
        if value == 0:
            return (0, interval)
        min_value = (value // interval) * interval
        max_value = min_value + interval
        return (min_value, max_value)

    def get_the_closest_major(self, value: int) -> int:
        """
        Obtiene el mayor submúltiplo más cercano al valor dado.
        """
        subdivision = self.get_interval_subdivision(value)
        max_value = subdivision[1]
        submultiples = [i for i in self.values if max_value % i == 0]
        return max(submultiples)

    def get_the_nearest_minor(self, value: int) -> int:
        """
        Obtiene el menor submúltiplo más cercano al valor dado.
        """
        if value < self.values[0]:
            return None
        subdivision = self.get_interval_subdivision(value)
        min_value = subdivision[0]
        submultiples = [i for i in self.values if min_value % i == 0]
        return max(submultiples)

class IntervaloTiempo:
    """
    Esta clase representa un intervalo de tiempo en días.
    """

    def __init__(self, values: list, start_date: date):
        """
        Inicializa un objeto IntervaloTiempo con una lista de valores enteros y una fecha de inicio.
        """
        self.values = values
        self.start_date = start_date

    def get_interval_subdivision(self, value: date) -> tuple:
        """
        Obtiene la subdivisión del intervalo que contiene la fecha dada.
        """
        interval = self.values[0]
        max_value = max(self.values)
        if value == self.start_date:
            return (self.start_date, self.start_date + timedelta(days=interval))
        min_value = value - timedelta(days=(value - self.start_date).days % interval)
        max_value = min_value + timedelta(days=interval)
        return (min_value, max_value)

    def get_the_closest_major(self, value: date) -> int:
        """
        Obtiene el mayor submúltiplo más cercano a la fecha dada.
        """
        subdivision = self.get_interval_subdivision(value)
        max_value = subdivision[1]
        submultiples = [i for i in self.values if (max_value - self.start_date).days % i == 0]
        if not submultiples:
            raise ValueError("No submultiple found")
        return max(submultiples)

    def get_the_nearest_minor(self, value: date) -> int:
        """
        Obtiene el menor submúltiplo más cercano a la fecha dada.
        """
        if value <= self.start_date + timedelta(self.values[0]):
            return None
        subdivision = self.get_interval_subdivision(value)
        min_value: date = subdivision[0]
        submultiples = [i for i in self.values if (min_value - self.start_date).days % i == 0]
        if not submultiples:
            raise ValueError("No submultiple found")
        return max(submultiples)

def launch_alert(
    intervalo: Intervalo,
    kilometraje_actual: int,
    kilometraje_preventivo: int
) -> None:
    """
    Esta función se le pasa un intervalo de mantenimiento
    y determina si ya es tiempo, en función del kilometraje de advertencia,
    lanzar una alerta de mantenimiento del vehículo.
    """
    closest_major = intervalo.get_the_closest_major(kilometraje_actual)
    if closest_major - kilometraje_preventivo <= kilometraje_actual:
        print(f"Alerta de mantenimiento: el vehículo está a {closest_major - kilometraje_actual} kilómetros del próximo mantenimiento.")

def launch_alert_time(
    intervalo: IntervaloTiempo,
    fecha_actual: date,
    dias_preventivos: int
) -> None:
    """
    Esta función se le pasa un intervaloTiempo de mantenimiento
    y determina si ya es tiempo, en función de los días de advertencia,
    lanzar una alerta de mantenimiento del vehículo.
    """
    closest_major = intervalo.get_the_closest_major(fecha_actual)
    if closest_major - dias_preventivos <= (fecha_actual - intervalo.start_date).days:
        print(f"Alerta de mantenimiento: el vehículo está a {closest_major - (fecha_actual - intervalo.start_date).days} días del próximo mantenimiento.")

def launch_alert_with_compare_intervals(
    intervalo: Intervalo,
    intervalo_tiempo: IntervaloTiempo,
    kilometraje_actual: int,
    kilometraje_preventivo: int,
    fecha_actual: date,
    dias_preventivos: int
) -> None:
    """
    Esta función conjuga launch_alert_time y launch_alert de la siguiente manera:
    lanza la alerta en función del intervalo que esté más cerca de los límites acordados.
    Es decir, ejecuta cada función de alerta y lanza ninguna, una o ambas alertas.
    """
    launch_alert(intervalo, kilometraje_actual, kilometraje_preventivo)
    launch_alert_time(intervalo_tiempo, fecha_actual, dias_preventivos)


if __name__ == "__main__":
    interval1 = Intervalo(
        [50, 150, 300, 1000]
    )
    launch_alert(interval1, 145, 5)
    launch_alert(interval1, 144, 5)
    launch_alert(interval1, 143, 5)
    launch_alert(interval1, 142, 5)
    launch_alert(interval1, 146, 5)
    launch_alert(interval1, 147, 5)

    intervalo_t = IntervaloTiempo(
        [15, 30, 60], date(2022, 1, 1)
    )
    launch_alert_time(intervalo_t, date(2022, 1, 6), 7)
    launch_alert_time(intervalo_t, date(2022, 1, 7), 7)
    launch_alert_time(intervalo_t, date(2022, 1, 8), 7)
    launch_alert_time(intervalo_t, date(2022, 1, 9), 7)
    launch_alert_time(intervalo_t, date(2022, 1, 16), 7)
    launch_alert_time(intervalo_t, date(2022, 1, 21), 7)
    launch_alert_time(intervalo_t, date(2022, 1, 25), 7)
    launch_alert_time(intervalo_t, date(2022, 1, 26), 7)

    launch_alert_with_compare_intervals(
        interval1, intervalo_t, 299, 5, date(2022, 1, 14), 7
    )
