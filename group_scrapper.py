import json
import os
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

dev_mode = True


def print_dev_mode(message):
    if dev_mode:
        print("Dev_mode: ", message)
    else:
        pass


def wait_element(driver, xpath, click=False, timeout=False):
    counter = 0
    while True:
        counter += 1
        if counter > timeout and timeout:
            return False
        try:
            element = driver.find_element(By.XPATH, xpath)
            if click:
                element.click()
                print_dev_mode('wait_element click: ' + xpath)
                return True
            print_dev_mode('wait_element: ' + xpath)
            return True
        except:
            time.sleep(1 / 1000)
            continue


def wait_elements(driver, array, click=False, timeout=False):
    counter = 0
    while True:
        counter += 1
        if counter > timeout and timeout:
            return False
        for xpath in array:
            try:
                element = driver.find_element(By.XPATH, xpath)
                if click:
                    element.click()
                    print_dev_mode('wait_elements click: ' + xpath)
                    return True
                print_dev_mode('wait_elements: ' + xpath)
                return True
            except:
                continue
        time.sleep(1 / 1000)


def add_contact(phone, array):
    contact = {
        "Telefone": phone,
    }
    array.append(contact)
    print(f"Contato {phone} adicionado com sucesso.")


def save_contacts_to_json(contacts, filename):
    # Estrutura dos contatos como dicionários com a chave "Telefone"
    contacts_with_key = [{"Telefone": contact} for contact in contacts]

    # Estrutura do JSON com uma chave "contacts"
    data = {
        "contacts": contacts_with_key
    }

    # Salva a estrutura de dados em um arquivo JSON
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Contatos salvos em {filename}")


def group_access(driver):
    try:
        if wait_element(driver, xpath="//button//div//div[contains(text(), 'Grupos')]", timeout=1, click=True):
            print_dev_mode("Encontrou botão de grupo")
            # Clica no grupo desejado
            wait_element(driver, xpath="//span[contains(text(),'DEPARTAMENTO CONTÁBIL')]", click=True)
            print_dev_mode("Encontrou Grupo")
    except Exception as e:
        print('Erro ao encontrar o Botão do grupo: ', e)


def scroll_div_dynamically(driver, div_xpath, element_xpath, scroll_increment=150):
    # Obtém a referência da div que será rolada
    div = driver.find_element(By.XPATH, div_xpath)

    # Inicializa a contagem de elementos
    last_elements_count = 0
    while True:
        # Obter o número atual de elementos dentro da div
        elements = div.find_elements(By.XPATH, element_xpath)
        current_elements_count = len(elements)

        # Se a composição aumentou e atingimos a quantidade esperada, role a div
        if current_elements_count >= last_elements_count:
            # Rolar a div de forma incremental
            driver.execute_script(f"arguments[0].scrollTop += {scroll_increment};", div)
            print(f"Rolando a div, número de elementos encontrados: {current_elements_count}")

        # Se a composição não aumentar, significa que não há mais nada a carregar
        if current_elements_count == last_elements_count:
            print("Não há mais elementos a carregar.")
            break

        last_elements_count = current_elements_count


def get_member_list(driver):
    try:
        # Clica nos detalhes do grupo
        wait_element(driver, xpath="//header//span[contains(text(), 'DEPARTAMENTO')]", click=True)
        print_dev_mode("Acessou detalhes do grupo")

        # Acessa a lista de contatos que participam desse grupo
        wait_element(driver, xpath="//div[contains(text(), 'Ver tudo')]", click=True)
        print_dev_mode("Acessou membros do grupo")
    except Exception as e:
        print('Erro ao acessar Lista de Membros do Grupo: ', e)


def scrape_number(driver):
    contacts = []
    group_access(driver)
    get_member_list(driver)
    time.sleep(1)
    while True:
        elements = driver.find_elements(By.XPATH,
                                        "//div[contains(@style, 'pointer-events: auto;')]//span[contains(@title, '+55')]")
        scroll_div_dynamically(driver,  "(//div[contains(@role, 'listitem')]/../../../..)[1]",
                               "//div[contains(@style, 'pointer-events: auto;')]//span[contains(@title, '+55')]")

        if wait_element(driver, "//button[contains(., 'Mostrar membros anteriores')]", timeout=5):
            removed_duplicated_contacts = list(set(contacts))
            save_contacts_to_json(removed_duplicated_contacts, 'contacts.json')
            break

        for element in elements:
            contacts.append(element.text)
            print(len(contacts))
            print('Contato a ser adicionado: ', element.text)


def main():
    # Initialize the driver
    profile_path = os.path.join(os.getcwd(), "chrome_profile")
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)

    options = uc.ChromeOptions()
    # options.add_argument(argument="--headless=new")
    options.add_argument(argument='--no-sandbox')
    options.add_argument(argument='--disable-dev-shm-usage')
    options.add_argument(argument='--lang=pt-BR')
    options.add_argument(argument=f'--user-data-dir={profile_path}')

    # Create the driver
    driver = uc.Chrome(options=options, version_main=131)


    # Access WhatsApp Web
    driver.get(url='https://web.whatsapp.com/')
    wait_element(driver, xpath="//button[@aria-label='Pesquisar ou começar uma nova conversa']")

    scrape_number(driver)

    # Close the driver
    driver.quit()


if __name__ == "__main__":
    main()
