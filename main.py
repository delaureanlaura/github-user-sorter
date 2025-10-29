import requests
import json
from typing import List, Dict, Any

# URL base da API do GitHub
GITHUB_API_URL = "https://api.github.com"
# Endpoint para listar usuários
USERS_ENDPOINT = f"{GITHUB_API_URL}/users"

def get_github_users(since_id: int = 0, per_page: int = 30) -> List[Dict[str, Any]]:
    """
    Consome a API do GitHub para obter uma lista de usuários.
    O endpoint /users não suporta ordenação nativa, mas é usado para obter os dados.
    
    Args:
        since_id: O ID do usuário a partir do qual a lista deve começar (para paginação).
        per_page: O número de usuários por página (máximo 100).
        
    Returns:
        Uma lista de dicionários, onde cada dicionário representa um usuário.
    """
    params = {
        "since": since_id,
        "per_page": per_page
    }
    
    # Cabeçalhos recomendados pela documentação do GitHub
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        print(f"Buscando usuários a partir do ID {since_id}...")
        response = requests.get(USERS_ENDPOINT, headers=headers, params=params)
        response.raise_for_status() # Levanta exceção para códigos de status HTTP ruins (4xx ou 5xx)
        
        users_data = response.json()
        print(f"Sucesso! {len(users_data)} usuários obtidos.")
        return users_data
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do GitHub: {e}")
        return []

def extract_relevant_data(users_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extrai um subconjunto de dados relevantes para a ordenação.
    
    Args:
        users_data: Lista de dicionários de usuários da API.
        
    Returns:
        Lista de dicionários com apenas os campos 'login' e 'id'.
    """
    extracted_data = []
    for user in users_data:
        # Os campos 'login' (string) e 'id' (inteiro) são ideais para demonstração de ordenação.
        extracted_data.append({
            "login": user.get("login"),
            "id": user.get("id"),
            "type": user.get("type") # Adiciona o tipo para possível ordenação ou filtro
        })
    return extracted_data

def sort_users(users: List[Dict[str, Any]], key: str, reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Implementa um método de ordenação customizado para a lista de usuários.
    
    Args:
        users: Lista de usuários a ser ordenada.
        key: A chave do dicionário a ser usada para ordenação (ex: 'login', 'id').
        reverse: Booleano para ordenação decrescente (True) ou crescente (False).
        
    Returns:
        Lista de usuários ordenada.
    """
    print(f"\n--- Ordenando por '{key}' (Reversa: {reverse}) ---")
    
    # Usamos o método sort() do Python, que é uma implementação de Timsort,
    # um algoritmo de ordenação híbrido eficiente (Merge Sort + Insertion Sort).
    # O Timsort tem complexidade O(n log n).
    
    # A feature da API do GitHub que estamos usando para ordenação é o campo
    # 'id' (numérico) e 'login' (alfabético).
    
    # A ordenação é feita localmente, pois o endpoint /users não oferece
    # parâmetros de ordenação.
    
    try:
        sorted_users = sorted(users, key=lambda user: user[key], reverse=reverse)
        return sorted_users
    except KeyError:
        print(f"Erro: Chave de ordenação '{key}' não encontrada nos dados do usuário.")
        return users

def main():
    # 1. Consumir a API (obtendo 50 usuários para ter uma amostra maior)
    raw_users = get_github_users(per_page=50)
    
    if raw_users:
        # 2. Tratar os dados de resposta
        processed_users = extract_relevant_data(raw_users)
        
        print("\n--- Dados Brutos (Apenas Login, ID e Tipo) ---")
        for user in processed_users:
            print(f"Login: {user['login']}, ID: {user['id']}, Tipo: {user['type']}")
        
        # 3. Implementar e demonstrar métodos de ordenação
        
        # Método 1: Ordenação por ID (Numérico)
        sorted_by_id = sort_users(processed_users, key="id", reverse=False)
        print("\n--- Ordenação por ID (Crescente) ---")
        for user in sorted_by_id:
            print(f"ID: {user['id']}, Login: {user['login']}")
            
        # Método 2: Ordenação por Login (Alfabética)
        sorted_by_login = sort_users(processed_users, key="login", reverse=False)
        print("\n--- Ordenação por Login (Alfabética Crescente) ---")
        for user in sorted_by_login:
            print(f"Login: {user['login']}, ID: {user['id']}")
            
        # Método 3: Ordenação por Tipo e depois por Login (Ordenação de Múltiplas Chaves)
        # Primeiro, ordenamos pelo login, depois pelo tipo.
        # Note: A ordenação é estável, então a segunda ordenação mantém a ordem da primeira.
        # Para ordenar por múltiplas chaves, o Python permite passar uma tupla de chaves.
        # Neste exemplo, faremos uma ordenação composta:
        
        print("\n--- Ordenação Composta: Tipo (User/Organization) e depois por ID ---")
        
        # A ordenação por múltiplas chaves é feita passando uma tupla de valores para a chave `key`.
        sorted_compound = sorted(processed_users, key=lambda user: (user['type'], user['id']), reverse=False)
        
        for user in sorted_compound:
            print(f"Tipo: {user['type']}, ID: {user['id']}, Login: {user['login']}")

if __name__ == "__main__":
    main()
