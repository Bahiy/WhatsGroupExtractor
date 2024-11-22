import json
import os
import time
import tkinter as tk
from tkinter import messagebox

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


def group_access(driver, group_name):
    try:
        if wait_element(driver, xpath="//button//div//div[contains(text(), 'Grupos')]", timeout=1, click=True):
            print_dev_mode("Encontrou botão de grupo")
            # Clica no grupo desejado
            wait_element(driver, xpath=f"//span[contains(text(), '{group_name}')]", click=True)
            print_dev_mode("Encontrou Grupo")
    except Exception as e:
        print('Erro ao encontrar o Botão do grupo: ', e)


def scroll_div_dynamically(driver, div_xpath, element_xpath, scroll_increment=1500):
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
            time.sleep(2)
            print(f"Rolando a div, número de elementos encontrados: {current_elements_count}")


        # Se a composição não aumentar, significa que não há mais nada a carregar
        if current_elements_count == last_elements_count:
            print("Não há mais elementos a carregar.")
            break

        last_elements_count = current_elements_count


# def get_group_name():
def get_group_name():
    group_name = entry_group_name.get().strip()
    if group_name:
        print(f'Grupo Inserido: {group_name}')
        window.quit()
        return group_name
    else:
        messagebox.showerror("Erro", "Por favor, insira um nome válido!")


def on_close():
    os._exit(0)  # Força o encerramento total da aplicação


window = tk.Tk()
window.title("Extrair Números de Grupo")
window.geometry("350x200")
window.configure(bg="#ffffff")
window.protocol("WM_DELETE_WINDOW", on_close)

# Centralizar a janela na tela
window.eval('tk::PlaceWindow . left')

# Estilo
label_font = ("Poppins", 13)
entry_font = ("Poppins", 12)
button_font = ("Poppins", 13, "bold")
bg_color = "#ffffff"
fg_color = "#333333"
button_color = "#2fb490"

# Frame para os campos de entrada
form_frame = tk.Frame(window, bg=bg_color)
form_frame.pack(pady=10, padx=40, fill="both", expand=True)

# Nome do cliente
tk.Label(form_frame, text="Insira o nome do Grupo:", font=label_font, bg=bg_color, fg=fg_color).pack(expand=True)
entry_group_name = tk.Entry(form_frame, font=entry_font)
entry_group_name.pack(anchor="w", pady=5, fill="x")

# Botão de enviar
submit_button = tk.Button(window, text="Enviar", font=button_font, bg=button_color, fg="white", command=get_group_name)
submit_button.pack(pady=10)

# Executar o loop principal
window.mainloop()


def get_member_list(driver, group_name):
    try:
        # Clica nos detalhes do grupo
        wait_element(driver, xpath=f"//header//span[contains(text(), '{group_name}')]", click=True)
        print_dev_mode("Acessou detalhes do grupo: ")

        # Acessa a lista de contatos que participam desse grupo
        wait_element(driver, xpath="//div[contains(text(), 'Ver tudo')]", click=True)
        print_dev_mode("Acessou membros do grupo")
    except Exception as e:
        print('Erro ao acessar Lista de Membros do Grupo: ', e)


def scrape_number(driver, group_name):
    contacts = []
    group_access(driver, group_name)
    get_member_list(driver, group_name)
    while True:
        elements = driver.find_elements(By.XPATH,
                                        "(//div[contains(@role, 'listitem')]/../../../..)[1]//span[contains(.,'+')]")

        if not wait_element(driver, "//button[contains(., 'Mostrar membros anteriores')]", timeout=1):
            for element in elements:
                contacts.append(element.text)
                print(len(contacts))
                print('Contato a ser adicionado: ', element.text)
            scroll_div_dynamically(driver, "(//div[contains(@role, 'listitem')]/../../../..)[1]",
                                   "//div[contains(@style, 'pointer-events: auto;')]//span[contains(@title, '+55')]")
        else:
            removed_duplicated_contacts = list(set(contacts))
            save_contacts_to_json(removed_duplicated_contacts, 'contacts.json')
            break


def main():
    inicio = time.perf_counter()
    # Initialize the driver
    profile_path = os.path.join(os.getcwd(), "chrome_profile")
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)

    options = uc.ChromeOptions()
    options.add_argument(argument="--headless=new")
    options.add_argument(argument='--no-sandbox')
    options.add_argument(argument="--start-maximized")
    options.add_argument(argument='--disable-dev-shm-usage')
    options.add_argument(argument='--lang=pt-BR')
    options.add_argument(argument=f'--user-data-dir={profile_path}')

    # Create the driver
    driver = uc.Chrome(options=options, version_main=131)

    group_name = get_group_name()
    window.destroy()
    print(group_name)

    # Access WhatsApp Web
    driver.get(url='https://web.whatsapp.com/')
    driver.execute_script("document.body.style.zoom='25%'")

    wait_element(driver, xpath="//button[@aria-label='Pesquisar ou começar uma nova conversa']")
    scrape_number(driver, group_name)

    # Close the driver
    driver.quit()

    tempo_total = time.perf_counter() - inicio
    print(f"Tempo de execução: {tempo_total:.2f} segundos")

if __name__ == "__main__":
    main()
