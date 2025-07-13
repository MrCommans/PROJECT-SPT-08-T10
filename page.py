from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import helpers
import data


class UrbanRoutesPage:
    # Locators existentes
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.XPATH, '//button[contains(text(), "Chamar um táxi")]')

    # Locators ajustados
    plan_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')  # Plano "Comfort"
    add_phone_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]')  # Adicionar telefone
    phone_field = (By.XPATH, '//*[@id="phone"]')  # Campo de telefone no modal
    phone_display = (By.XPATH,
                     '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div')  # Número exibido após confirmação
    next_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')  # Próximo
    sms_code_field = (By.XPATH, '//*[@id="code"]')  # Campo de código SMS
    confirm_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')  # Confirmar

    # Locators para métodos de pagamento
    payment_method_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')  # Método de Pagamento
    add_card_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]')  # Adicionar Cartão
    card_number_field = (By.XPATH,
                         '//*[@id="root"]/div/div[2]/div[2]/div[2]/form//input[@id="number"]')  # Campo de número do cartão no modal
    card_code_field = (By.XPATH,
                       '//*[@id="root"]/div/div[2]/div[2]/div[2]/form//input[@id="code"]')  # Campo de CVV no modal
    add_card_submit_button = (By.XPATH,
                              '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')  # Botão Adicionar no modal
    close_card_confirmation_button = (By.XPATH,
                                      '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')  # Botão 'x' para fechar a página de confirmação
    card_number_display = (By.XPATH,
                           '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]')  # Elemento que indica o cartão adicionado

    comment_field = (By.XPATH, '//*[@id="comment"]')  # Campo de comentário
    blanket_checkbox = (By.XPATH,
                        '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div')  # Checkbox para cobertor
    blanket_status = (By.XPATH,
                      '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div')  # Label para verificar estado
    requirements_section = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]')  # Seção de requisitos
    ice_cream_plus_button = (By.XPATH,
                             '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')  # Botão + sorvete
    ice_cream_counter = (By.XPATH,
                         '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]')  # Contador de sorvetes
    search_car_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')  # Atualizado para um XPath mais genérico
    car_model_modal = (By.CLASS_NAME, 'order-body')  # Modal de busca de carros

    def __init__(self, driver):
        self.driver = driver

    def _wait_for_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.visibility_of_element_located(locator)
        )

    def _wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.element_to_be_clickable(locator)
        )

    def _wait_for_enabled(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.visibility_of_element_located(locator) and
            expected_conditions.element_to_be_clickable(locator)
        )

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        self.click_call_taxi()

    def set_from(self, from_address):
        self._wait_for_visible(self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self._wait_for_visible(self.to_field).send_keys(to_address)

    def get_from(self):
        return self._wait_for_visible(self.from_field).get_property('value')

    def get_to(self):
        return self._wait_for_visible(self.to_field).get_property('value')

    def click_call_taxi(self):
        self._wait_for_clickable(self.call_taxi_button).click()

    def select_plan(self, plan_name):
        plan_locator = (self.plan_button[0], self.plan_button[1])
        element = self._wait_for_visible(plan_locator)
        if "active" not in element.get_attribute("class"):
            self._wait_for_clickable(plan_locator).click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: "active" in self.driver.find_element(*plan_locator).get_attribute("class"),
            "Plano Comfort não foi selecionado."
        )
        # Adiciona atraso para garantir que a seção de requisitos carregue
        import time
        time.sleep(2)

    def is_plan_selected(self, plan_name):
        plan_locator = (self.plan_button[0], self.plan_button[1])
        element = self._wait_for_visible(plan_locator)
        return "active" in element.get_attribute("class")

    def fill_phone_number(self, phone_number):
        print("Iniciando o método fill_phone_number...")
        add_phone_button = self._wait_for_clickable(self.add_phone_button, timeout=15)
        print("Botão 'Adicionar telefone' clicável.")
        add_phone_button.click()
        phone_element = self._wait_for_enabled(self.phone_field, timeout=15)
        if phone_element.is_enabled():
            phone_element.clear()
            phone_element.send_keys(phone_number)
            print(f"Número de telefone inserido: {phone_number}")
        else:
            raise Exception("O campo de telefone não está habilitado para edição.")
        next_button = self._wait_for_clickable(self.next_button, timeout=15)
        next_button.click()
        print("Botão 'Próximo' clicado.")
        sms_code = helpers.retrieve_phone_code(self.driver)
        print(f"Código SMS obtido: {sms_code}")
        sms_code_element = self._wait_for_enabled(self.sms_code_field, timeout=15)
        if sms_code_element.is_enabled():
            if sms_code_element.get_attribute("value"):
                sms_code_element.clear()
            sms_code_element.send_keys(sms_code)
            print(f"Código SMS inserido: {sms_code}")
        else:
            raise Exception("O campo de código SMS não está habilitado para edição.")
        confirm_button = self._wait_for_clickable(self.confirm_button, timeout=15)
        confirm_button.click()
        print("Botão 'Confirmar' clicado.")
        WebDriverWait(self.driver, 15).until(
            expected_conditions.invisibility_of_element_located(self.confirm_button),
            "Modal de confirmação de telefone não foi fechado."
        )
        print("Modal de confirmação fechado.")
        # Aguarda a exibição do número na página principal
        try:
            self._wait_for_visible(self.phone_display, timeout=10)
            print("Número de telefone visível na página principal.")
        except Exception as e:
            print(f"Erro ao aguardar exibição do número: {e}")

    def get_phone_number(self):
        try:
            phone_element = self._wait_for_visible(self.phone_display, timeout=20)
            phone_value = phone_element.text.strip() or phone_element.get_attribute('value')
            print(f"Número de telefone encontrado: {phone_value}")
            print(f"Tag do elemento: {phone_element.tag_name}")
            print(f"Atributos do elemento: {phone_element.get_attribute('outerHTML')}")
            return phone_value
        except Exception as e:
            print(f"Erro ao obter o número de telefone: {e}")
            return ""

    def fill_card(self, card_details):
        print("Iniciando o método fill_card...")
        self.click_payment_method()
        print("Botão 'Método de Pagamento' clicado.")
        self.click_add_card()
        print("Botão 'Adicionar Cartão' clicado.")
        card_number = self._wait_for_enabled(self.card_number_field, timeout=15)
        if card_number.is_enabled():
            card_number.clear()
            card_number.send_keys(card_details['number'])
            print(f"Número do cartão inserido: {card_details['number']}")
        else:
            raise Exception("O campo de número do cartão não está habilitado.")
        card_code = self._wait_for_enabled(self.card_code_field, timeout=15)
        if card_code.is_enabled():
            card_code.clear()
            card_code.send_keys(card_details['code'])
            print(f"Código do cartão inserido: {card_details['code']}")
        else:
            raise Exception("O campo de código do cartão não está habilitado.")
        card_code.send_keys(Keys.TAB)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.add_card_submit_button),
            "Botão de adicionar cartão não está clicável."
        )
        self._wait_for_clickable(self.add_card_submit_button).click()
        print("Botão 'Adicionar' clicado.")
        self._wait_for_clickable(self.close_card_confirmation_button).click()
        print("Botão de fechar modal clicado.")
        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located(self.close_card_confirmation_button),
            "Modal de confirmação de cartão não foi fechado."
        )
        print("Modal de confirmação de cartão fechado.")
        # Verifica a exibição do cartão na página principal
        try:
            card_display = self._wait_for_visible(self.card_number_display, timeout=15)
            print(f"Texto do cartão visível na página principal: {card_display.text}")
        except Exception as e:
            print(f"Erro ao aguardar exibição do cartão: {e}")

    def get_card_details(self):
        try:
            # Verifica a presença do elemento que indica o cartão adicionado
            card_display = self._wait_for_visible(self.card_number_display, timeout=15)
            card_text = card_display.text.strip() or card_display.find_element(By.CLASS_NAME,
                                                                               'pp-value-text').text.strip()
            print(f"Texto do cartão encontrado: {card_text}")
            print(f"Tag do elemento: {card_display.tag_name}")
            print(f"Atributos do elemento: {card_display.get_attribute('outerHTML')}")

            # Retorna um dicionário indicando apenas a presença do cartão
            return {
                'added': card_text == "Cartão",
                'number': '',  # Não disponível
                'code': ''  # Não disponível
            }
        except Exception as e:
            print(f"Erro ao obter detalhes do cartão: {e}")
            return {'added': False, 'number': '', 'code': ''}

    def add_comment(self, comment):
        comment_field = self._wait_for_clickable(self.comment_field, timeout=10)
        if comment_field.is_enabled():
            comment_field.clear()
            comment_field.send_keys(comment)
            print(f"Comentário inserido: {comment}")
        else:
            raise Exception("O campo de comentário não está habilitado.")

    def get_comment(self):
        return self._wait_for_visible(self.comment_field, timeout=10).get_property('value')

    def order_blanket_and_handkerchiefs(self):
        print("Iniciando o método order_blanket_and_handkerchiefs...")
        # Aguarda a seção de requisitos estar visível
        try:
            self._wait_for_visible(self.requirements_section, timeout=20)
            print("Seção de requisitos visível.")
        except Exception as e:
            print(f"Erro ao aguardar seção de requisitos: {e}")

        # Tenta localizar o checkbox
        print("Tentando localizar o checkbox do cobertor...")
        try:
            blanket = self._wait_for_clickable(self.blanket_checkbox, timeout=20)
            print("Checkbox encontrado.")
            print(f"Tag do checkbox: {blanket.tag_name}")
            print(f"Atributos do checkbox: {blanket.get_attribute('outerHTML')}")

            if not blanket.is_selected():
                print("Checkbox não está selecionado, clicando...")
                try:
                    blanket.click()
                    print("Clique padrão executado.")
                except Exception as e:
                    print(f"Clique padrão falhou: {e}. Tentando clique via JavaScript...")
                    self.driver.execute_script("arguments[0].click();", blanket)
                    print("Clique via JavaScript executado.")

                # Aguarda até que o checkbox esteja marcado
                try:
                    WebDriverWait(self.driver, 20).until(
                        lambda driver: driver.find_element(*self.blanket_checkbox).get_attribute("checked") == "true",
                        "Checkbox do cobertor não foi marcado após o clique."
                    )
                    print("Checkbox marcado com sucesso.")
                except Exception as e:
                    print(f"Erro na espera após clique: {e}")
                    # Loga o texto do status para depuração
                    try:
                        status_element = self._wait_for_visible(self.blanket_status, timeout=5)
                        status = status_element.text.lower()
                        print(f"Texto do status do cobertor (depuração): {status}")
                    except Exception as e:
                        print(f"Erro ao obter texto do status: {e}")
            else:
                print("Checkbox já está selecionado.")
        except Exception as e:
            print(f"Erro ao localizar ou interagir com o checkbox: {e}")
            # Depuração: lista todos os checkboxes na seção de requisitos
            try:
                checkboxes = self.driver.find_elements(By.XPATH,
                                                       '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]//input[@type="checkbox"]')
                for i, cb in enumerate(checkboxes, 1):
                    print(f"Checkbox {i}: {cb.get_attribute('outerHTML')}")
            except Exception as e:
                print(f"Erro ao listar checkboxes: {e}")
        print("Concluído o método order_blanket_and_handkerchiefs.")

    def is_blanket_ordered(self):
        try:
            checkbox = self._wait_for_visible(self.blanket_checkbox, timeout=20)
            print(f"Tag do checkbox: {checkbox.tag_name}")
            print(f"Atributos do checkbox: {checkbox.get_attribute('outerHTML')}")
            is_checked = checkbox.get_attribute("checked") == "true"
            print(f"Checkbox marcado (atributo 'checked'): {is_checked}")
            if not is_checked:
                try:
                    status_element = self._wait_for_visible(self.blanket_status, timeout=5)
                    status = status_element.text.lower()
                    print(f"Texto do status do cobertor: {status}")
                    is_checked = any(text in status for text in
                                     ["cobertor e lençóis", "cobertor e lenços", "selecionado", "selected"])
                except Exception as e:
                    print(f"Erro ao obter texto do status: {e}")
            return is_checked
        except Exception as e:
            print(f"Erro ao verificar o estado do cobertor: {e}")
            # Depuração: lista todos os checkboxes na seção de requisitos
            try:
                checkboxes = self.driver.find_elements(By.XPATH,
                                                       '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]//input[@type="checkbox"]')
                for i, cb in enumerate(checkboxes, 1):
                    print(f"Checkbox {i}: {cb.get_attribute('outerHTML')}")
            except Exception as e:
                print(f"Erro ao listar checkboxes: {e}")
            return False

    def order_ice_cream(self, quantity=1):
        max_attempts = 10
        attempt = 0
        while attempt < max_attempts:
            current_count = self.get_ice_cream_count()
            if current_count >= quantity:
                break
            self._wait_for_clickable(self.ice_cream_plus_button, timeout=10).click()
            WebDriverWait(self.driver, 10).until(
                lambda driver: self.get_ice_cream_count() > current_count,
                f"Contador de sorvetes não foi incrementado após tentativa {attempt + 1}."
            )
            attempt += 1
        if attempt >= max_attempts:
            print(f"Falha ao atingir {quantity} sorvetes após {max_attempts} tentativas.")

    def get_ice_cream_count(self):
        try:
            text = self._wait_for_visible(self.ice_cream_counter, timeout=10).text
            print(f"Texto do contador de sorvetes: {text}")
            import re
            match = re.search(r'\d+', text)
            return int(match.group()) if match else 0
        except Exception as e:
            print(f"Erro ao obter contador de sorvetes: {e}")
            return 0

    def search_car(self, driver_message):
        self.add_comment(driver_message)
        self._wait_for_clickable(self.search_car_button, timeout=10).click()
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.car_model_modal),
            "Modal de busca de carros não apareceu."
        )

    def is_car_model_visible(self):
        return self._wait_for_visible(self.car_model_modal, timeout=10).is_displayed()

    def click_payment_method(self):
        self._wait_for_clickable(self.payment_method_button).click()

    def click_add_card(self):
        self._wait_for_clickable(self.add_card_button).click()