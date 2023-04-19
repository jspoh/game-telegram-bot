# pip install selenium
# pip install webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# MAKE IT SO THAT THE SELENIUM BROWSER DOES NOT POP OUT
options = Options()
options.add_argument("--headless")


# unable to run package on vercel
class CausewayCameras:
    def __init__(self):
        self._driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

    def close_driver(self):
        self._driver.close()

    def wdls_to_jb(self):
        img_src = self._driver.find_element(
            By.XPATH, "//img[@alt='View from Woodlands Causeway (Towards Johor)']")
        return img_src.get_attribute('src')

    def wdls_to_bke(self):
        img_src = self._driver.find_element(
            By.XPATH, "//img[@alt='View from Woodlands Checkpoint (Towards BKE)']")
        return img_src.get_attribute('src')

    def view_from_tuas(self):
        img_src = self._driver.find_element(
            By.XPATH, "//img[@alt='View from Tuas Checkpoint']")
        return img_src.get_attribute('src')

    def tuas_second_link(self):
        img_src = self._driver.find_element(
            By.XPATH, "//img[@alt='View from Second Link at Tuas']")
        return img_src.get_attribute('src')

    def all_cameras(self):
        return {'View from Woodlands Causeway (Towards Johor': self.wdls_to_jb(),
                'View from Woodlands Checkpoint (Towards BKE)': self.wdls_to_bke(),
                'View from Tuas Checkpoint': self.view_from_tuas(),
                'View from Second Link at Tuas': self.tuas_second_link()}

    def init(self):
        self._driver.get(
            'https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/woodlands.html')


def test():
    c = CausewayCameras()
    c.init()
    print(c.wdls_to_jb(), c.wdls_to_bke(), c.view_from_tuas(),
          c.tuas_second_link(), c.all_cameras(), sep='\n\n')
    c.close_driver()


if __name__ == '__main__':
    test()
