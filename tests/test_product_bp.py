import unittest
from app import create_app

class ProductBlueprintTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_products_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ноутбук".encode('utf-8'), response.data)
        self.assertIn("Смартфон".encode('utf-8'), response.data)


if __name__ == "__main__":
    unittest.main()
