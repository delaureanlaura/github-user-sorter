import requests
import json
from typing import List, Dict, Any


GITHUB_API_URL = "https://api.github.com"

USERS_ENDPOINT = f"{GITHUB_API_URL}/users"

def get_github_users(since_id: int = 0, per_page: int = 30) -> List[Dict[str, Any]]:
 
    params = {
        "since": since_id,
        "per_page": per_page
    }
    

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

    extracted_data = []
    for user in users_data:
        
        extracted_data.append({
            "login": user.get("login"),
            "id": user.get("id"),
            "type": user.get("type") 
        })
    return extracted_data

def sort_users(users: List[Dict[str, Any]], key: str, reverse: bool = False) -> List[Dict[str, Any]]:

    print(f"\n--- Ordenando por '{key}' (Reversa: {reverse}) ---")
    

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

        print("\n--- Ordenação Composta: Tipo (User/Organization) e depois por ID ---")
        
        # A ordenação por múltiplas chaves é feita passando uma tupla de valores para a chave `key`.
        sorted_compound = sorted(processed_users, key=lambda user: (user['type'], user['id']), reverse=False)
        
        for user in sorted_compound:
            print(f"Tipo: {user['type']}, ID: {user['id']}, Login: {user['login']}")

if __name__ == "__main__":
    main()
