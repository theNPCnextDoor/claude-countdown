from django.test import SimpleTestCase

from .solver import solve


class SolverTests(SimpleTestCase):
    def test_exact(self) -> None:
        r = solve([25, 50, 75, 100, 3, 6], 952)
        self.assertTrue(r["exact"])
        self.assertEqual(r["steps"][-1]["result"], 952)

    def test_shortest(self) -> None:
        # 153 s'obtient avec 4 nombres (ex. 50×3 + 6÷2) ; aucune solution à 3 nombres.
        r = solve([50, 9, 6, 3, 4, 2], 153)
        self.assertTrue(r["exact"])
        self.assertEqual(r["steps"][-1]["result"], 153)
        self.assertEqual(len(r["steps"]), 3)  # 3 opérations = 4 nombres utilisés

    def test_closest(self) -> None:
        # Avec six 1, le plus grand résultat possible est (1+1+1)×(1+1+1) = 9.
        r = solve([1, 1, 1, 1, 1, 1], 999)
        self.assertFalse(r["exact"])
        self.assertEqual(r["value"], 9)
        self.assertEqual(r["difference"], 990)

    def test_api_validation(self) -> None:
        resp = self.client.post("/api/solve/", {"numbers": [1], "target": 5},
                                content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_api_small_number_max_twice(self) -> None:
        resp = self.client.post("/api/solve/", {"numbers": [3, 3, 3, 25, 50, 75], "target": 500},
                                content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_api_small_number_twice_ok(self) -> None:
        resp = self.client.post("/api/solve/", {"numbers": [3, 3, 7, 25, 50, 75], "target": 500},
                                content_type="application/json")
        self.assertEqual(resp.status_code, 200)

    def test_api_large_number_max_once(self) -> None:
        resp = self.client.post("/api/solve/", {"numbers": [25, 25, 7, 3, 50, 75], "target": 500},
                                content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_api_large_numbers_all_distinct_ok(self) -> None:
        resp = self.client.post("/api/solve/", {"numbers": [25, 50, 75, 100, 7, 3], "target": 500},
                                content_type="application/json")
        self.assertEqual(resp.status_code, 200)
