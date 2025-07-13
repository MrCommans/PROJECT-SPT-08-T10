from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from page import UrbanRoutesPage
import data

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert routes_page.get_from() == data.ADDRESS_FROM, "Endereço de origem não foi definido corretamente."
        assert routes_page.get_to() == data.ADDRESS_TO, "Endereço de destino não foi definido corretamente."

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_plan(data.PLAN_NAME)
        assert routes_page.is_plan_selected(data.PLAN_NAME), "Plano Comfort não foi selecionado."

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_plan(data.PLAN_NAME)
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        assert routes_page.get_phone_number() == data.PHONE_NUMBER, "Número de telefone não foi preenchido corretamente."

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_plan(data.PLAN_NAME)
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        routes_page.fill_card(data.CARD_DETAILS)
        card_details = routes_page.get_card_details()
        assert card_details['added'], "Cartão não foi adicionado com sucesso."

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_plan(data.PLAN_NAME)
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        routes_page.fill_card(data.CARD_DETAILS)
        routes_page.add_comment(data.MESSAGE_FOR_DRIVER)
        assert routes_page.get_comment() == data.MESSAGE_FOR_DRIVER, "Comentário para o motorista não foi preenchido corretamente."

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_plan(data.PLAN_NAME)
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        routes_page.fill_card(data.CARD_DETAILS)
        routes_page.add_comment(data.MESSAGE_FOR_DRIVER)
        routes_page.order_blanket_and_handkerchiefs()
        assert routes_page.is_blanket_ordered(), (
            "O cobertor não está marcado como selecionado. "
            "Verifique o locator do checkbox, o comportamento da interface ou o texto do status."
        )

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_plan(data.PLAN_NAME)
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        routes_page.fill_card(data.CARD_DETAILS)
        routes_page.add_comment(data.MESSAGE_FOR_DRIVER)
        routes_page.order_ice_cream(quantity=2)
        assert routes_page.get_ice_cream_count() == 2, "A quantidade de sorvetes não é igual a 2."

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_plan(data.PLAN_NAME)
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        routes_page.fill_card(data.CARD_DETAILS)
        routes_page.add_comment(data.MESSAGE_FOR_DRIVER)
        routes_page.order_blanket_and_handkerchiefs()
        routes_page.order_ice_cream(quantity=2)
        routes_page.search_car(data.MESSAGE_FOR_DRIVER)
        assert routes_page.is_car_model_visible(), "Modal de busca de carros não apareceu."

    @classmethod
    def teardown_class(cls):
        if cls.driver:
            cls.driver.quit()