import time

from selenium.webdriver.common.by import By

import data
import helpers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from page import UrbanRoutesPage


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):

        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(5)

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.ADDRESS_FROM
        address_to = data.ADDRESS_TO
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_plan(self):

        print("Função criada para selecionar o plano")
        pass

    def test_fill_phone_number(self):

        print("Função criada para preencher o número de telefone")
        pass

    def test_fill_card(self):

        print("Função criada para preencher o cartão")
        pass

    def test_comment_for_driver(self):

        print("Função criada para adicionar comentário ao motorista")
        pass

    def test_order_blanket_and_handkerchiefs(self):

        print("Função criada para pedir cobertor e lenços")
        pass

    def test_order_2_ice_creams(self):

        print("Função criada para pedir sorvete")
        for i in range(2):

            pass

    def test_car_search_model_appears(self):

        print("Função criada para verificar se o modelo do carro aparece")
        pass
