## 📋 Nome do Projeto
**WhatsApp Group Number Extractor**

## 📄 Descrição
O **WhatsApp Group Number Extractor** é um script Python que automatiza o processo de extração de números de telefone dos membros de um grupo de WhatsApp. Utilizando Selenium com o **undetected_chromedriver**, ele acessa o WhatsApp Web, navega até o grupo especificado e coleta todos os números de telefone exibidos, salvando-os em um arquivo JSON.

## 🚀 Funcionalidades
- Acesso automatizado ao WhatsApp Web.
- Navegação até o grupo especificado.
- Rolagem dinâmica para carregar todos os membros do grupo.
- Extração dos números de telefone dos membros.
- Salvamento dos números extraídos em um arquivo JSON.
- Opção para operar em modo headless (sem interface gráfica).

## 🛠️ Tecnologias Utilizadas
- **Python 3.13**
- **Selenium** com **undetected_chromedriver**
- **XPath** para localização de elementos
- **JSON** para armazenamento dos contatos

## 📦 Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/WhatsApp-Group-Number-Extractor.git
   cd WhatsApp-Group-Number-Extractor
   ```

2. **Instale as dependências:**
   ```bash
   pip install undetected-chromedriver
   ```

3. **Crie um perfil do Chrome para armazenar o login do WhatsApp Web:**
   O script utiliza um perfil personalizado para evitar a necessidade de login em cada execução.

## 🔧 Configuração

- Altere o nome do grupo no código para o grupo que deseja acessar:
  ```python
  wait_element(driver, xpath="//span[contains(text(),'PROMO 42')]", click=True)
  ```

- O arquivo JSON com os contatos será salvo como `contacts.json` na pasta raiz do projeto.

## ▶️ Como Executar

1. **Inicie o script:**
   ```bash
   python main.py
   ```

2. **Escaneie o código QR no WhatsApp Web** (apenas na primeira execução ou se não houver perfil salvo).

3. **O script irá:**
   - Acessar o grupo especificado.
   - Rolar a lista de membros para carregar todos os contatos.
   - Salvar os números extraídos em um arquivo `contacts.json`.

## 📝 Estrutura do Arquivo JSON

O arquivo `contacts.json` será gerado com a seguinte estrutura:
```json
{
    "contacts": [
        {
            "Telefone": "+55 11 91234-5678"
        },
        {
            "Telefone": "+55 21 99876-5432"
        }
    ]
}
```

## ⚠️ Aviso Legal

Este projeto é apenas para fins educacionais. O uso do script para coletar dados de contatos sem permissão pode violar os **termos de serviço do WhatsApp**. Utilize-o de forma responsável e apenas em grupos onde você tem permissão para extrair os dados.

## 🛠️ Modo de Desenvolvimento
Se o `dev_mode` estiver ativado, o script exibirá mensagens adicionais de depuração:
```python
dev_mode = True
```

Para desativar o modo de desenvolvimento, defina:
```python
dev_mode = False
```

## 💡 Possíveis Problemas e Soluções
- **Problema:** O script não consegue localizar o grupo especificado.
  - **Solução:** Verifique se o nome do grupo está correto e se é idêntico ao exibido no WhatsApp Web.

- **Problema:** O script não carrega todos os membros.
  - **Solução:** Ajuste o `scroll_increment` na função `scroll_div_dynamically` para rolar mais ou menos pixels.

## 📜 Licença
Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
