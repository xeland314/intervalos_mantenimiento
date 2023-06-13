
from datetime import date
import unittest
from main import Intervalo, IntervaloTiempo
# Create your tests here.

class TestIntervalo(unittest.TestCase):

    def setUp(self) -> None:
        self.intervalo = Intervalo([50, 150, 300, 1000])

    def test_generate_interval(self) -> None:
        result1 = self.intervalo.generate_interval(0)
        result2 = self.intervalo.generate_interval(1)
        result3 = self.intervalo.generate_interval(2)
        result4 = self.intervalo.generate_interval(3)
        self.assertListEqual(
            result1,
            [0, 50, 100, 150, 200, 250, 300,
             350, 400, 450, 500, 550, 600,
             650, 700, 750, 800, 850,
             900, 950, 1000]
        )
        self.assertListEqual(
            result2,
            [0, 150, 300, 450,
             600, 750, 900]
        )
        self.assertListEqual(
            result3,
            [0, 300,
             600,
             900]
        )
        self.assertListEqual(
            result4,
            [0,
             1000]
        )

    def test_get_interval_subdivision(self):
        result1 = self.intervalo.get_interval_subdivision(25)
        result2 = self.intervalo.get_interval_subdivision(75)
        result3 = self.intervalo.get_interval_subdivision(125)
        result4 = self.intervalo.get_interval_subdivision(175)
        result5 = self.intervalo.get_interval_subdivision(225)
        result6 = self.intervalo.get_interval_subdivision(275)
        result7 = self.intervalo.get_interval_subdivision(325)
        result8 = self.intervalo.get_interval_subdivision(375)

        self.assertTupleEqual(result1, (0 ,50))
        self.assertTupleEqual(result2, (50 ,100))
        self.assertTupleEqual(result3, (100 ,150))
        self.assertTupleEqual(result4, (150 ,200))
        self.assertTupleEqual(result5, (200 ,250))
        self.assertTupleEqual(result6, (250 ,300))
        self.assertTupleEqual(result7, (300 ,350))
        self.assertTupleEqual(result8, (350 ,400))

    def test_get_the_closest_major(self):
        result1 = self.intervalo.get_the_closest_major(25)
        result2 = self.intervalo.get_the_closest_major(75)
        result3 = self.intervalo.get_the_closest_major(125)
        result4 = self.intervalo.get_the_closest_major(175)
        result5 = self.intervalo.get_the_closest_major(299)

        self.assertEqual(result1, 50)
        self.assertEqual(result2, 50)
        self.assertEqual(result3, 150)
        self.assertEqual(result4, 50)
        self.assertEqual(result5, 300)

    def test_get_the_nearest_minor(self):
        result1 = self.intervalo.get_the_nearest_minor(25)
        result2 = self.intervalo.get_the_nearest_minor(75)
        result3 = self.intervalo.get_the_nearest_minor(125)
        result4 = self.intervalo.get_the_nearest_minor(175)
        result5 = self.intervalo.get_the_nearest_minor(301)

        self.assertEqual(result1, None)
        self.assertEqual(result2, 50)
        self.assertEqual(result3, 50)
        self.assertEqual(result4, 150)
        self.assertEqual(result5, 300)

class TestIntervaloTiempo(unittest.TestCase):

    def setUp(self):
        start_date = date(2022, 1, 1)
        self.intervalo_tiempo = IntervaloTiempo([7, 14, 30], start_date)

    def test_get_interval_subdivision(self):
        result1 = self.intervalo_tiempo.get_interval_subdivision(date(2022, 1, 1))
        result2 = self.intervalo_tiempo.get_interval_subdivision(date(2022, 1, 5))
        result3 = self.intervalo_tiempo.get_interval_subdivision(date(2022, 1, 10))
        result4 = self.intervalo_tiempo.get_interval_subdivision(date(2022, 1, 15))

        self.assertEqual(result1, (date(2022, 1, 1), date(2022, 1, 8)))
        self.assertEqual(result2, (date(2022, 1, 1), date(2022, 1, 8)))
        self.assertEqual(result3, (date(2022, 1, 8), date(2022, 1, 15)))
        self.assertEqual(result4,(date(2022 ,1 ,15),date(2022 ,1 ,22)))

    def test_get_the_closest_major(self):
        result1=self.intervalo_tiempo.get_the_closest_major(date(2022 ,1 ,5))
        result2=self.intervalo_tiempo.get_the_closest_major(date(2022 ,1 ,10))

        self.assertEqual(result1, 7)
        self.assertEqual(result2, 14)

    def test_get_the_nearest_minor(self):
        result1=self.intervalo_tiempo.get_the_nearest_minor(date(2022 ,1 ,5))
        result2=self.intervalo_tiempo.get_the_nearest_minor(date(2022 ,1 ,10))

        self.assertEqual(result1, None)
        self.assertEqual(result2, 7)

class TestSuite(unittest.TestCase):
    """
    Todos los tests agrupados en uno.
    """
    def suite(self):
        """Agrupar tests antes de ejecutar el comando:
            python3 manage.py test

        Returns:
            suite: unittest.TestSuite
        """
        suite = unittest.TestSuite()
        suite.addTest(TestIntervalo('intervalo_test'))
        return suite
