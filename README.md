'''# GitHub User Sorter (Ordenador de Usuários do GitHub)

Este projeto demonstra o consumo da API REST do GitHub, especificamente o endpoint `/users`, e a aplicação de métodos de ordenação local nos dados de resposta, já que o endpoint em questão não oferece suporte nativo para ordenação.

## Contexto

O endpoint `GET /users` retorna uma lista de usuários na ordem em que se inscreveram no GitHub. Para aplicar qualquer outro tipo de ordenação (por exemplo, por nome de login ou ID), é necessário buscar os dados e processá-los localmente.

## Funcionalidades

1.  **Consumo da API:** Busca uma lista de usuários do GitHub.
2.  **Tratamento de Dados:** Extrai campos relevantes (`login`, `id`, `type`) da resposta JSON da API.
3.  **Implementação de Ordenação:** Demonstra três métodos de ordenação local usando a função `sorted()` do Python, que utiliza o algoritmo **Timsort** (eficiente para dados do mundo real).

## Métodos de Ordenação Implementados

O código (`main.py`) demonstra as seguintes ordenações:

| Método de Ordenação | Chave de Ordenação | Algoritmo | Descrição |
| :--- | :--- | :--- | :--- |
| **Ordenação por ID** | `id` (Numérico) | Timsort (Python `sorted()`) | Ordena os usuários pelo ID numérico de forma crescente. |
| **Ordenação por Login** | `login` (Alfabético) | Timsort (Python `sorted()`) | Ordena os usuários pelo nome de login de forma alfabética crescente. |
| **Ordenação Composta** | `type` e depois `id` | Timsort (Python `sorted()`) | Ordena primeiro pelo `type` (colocando 'Organization' antes de 'User', por exemplo, dependendo da ordem alfabética) e, em seguida, pelo `id` para desempate. |

## Como Executar

### Pré-requisitos

*   Python 3.x
*   O pacote `requests` do Python.

### Instalação

1.  Clone o repositório (ou crie a estrutura de arquivos se estiver seguindo manualmente):

    ```bash
    # Se você estiver no diretório raiz
    git clone [URL_DO_REPOSITORIO]
    cd github_sorter
    ```

2.  Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

### Execução

Execute o script principal:

```bash
python main.py
```

O script irá imprimir no console:

1.  A lista bruta dos 50 primeiros usuários (extraídos apenas `login`, `id` e `type`).
2.  A lista ordenada por **ID (crescente)**.
3.  A lista ordenada por **Login (alfabética crescente)**.
4.  A lista com a **Ordenação Composta** (por `type` e depois por `id`).

## Arquivos do Projeto

*   `main.py`: O código principal com a lógica de consumo da API, tratamento de dados e ordenação.
*   `requirements.txt`: Lista de dependências do projeto (`requests`).
*   `README.md`: Este arquivo.
'''
