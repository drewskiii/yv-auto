import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class YVScriptTest(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = webdriver.Chrome()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self) -> None:
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

