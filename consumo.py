import requests

BASE_URL = "https://flaskapi-g3n8.onrender.com/"

def get_books():
    response = requests.get(BASE_URL + 'items')
    if response.status_code == 200:
        print("Lista de livros:")
        print(response.json())
    else:
        print(f"Erro ao buscar livros: {response.status_code}")

def get_book(book_id):
    response = requests.get(BASE_URL + f'items/{book_id}')
    if response.status_code == 200:
        print(f"Livro {book_id}:")
        print(response.json())
    else:
        print(f"Erro ao buscar o livro: {response.status_code}")

def add_book():
    new_book = {
        "title": "Novo Livro",
        "authors": "Autor Exemplo",
        "average_rating": 4.7,
        "language_code": "pt",
        "num_pages": 300,
        "text_reviews_count": 25
    }
    response = requests.post(BASE_URL + 'items', json=new_book)
    if response.status_code == 201:
        print("Livro adicionado com sucesso:")
        print(response.json())
    else:
        print(f"Erro ao adicionar livro: {response.status_code}")

def update_book(book_id):
    updated_info = {
        "title": "Título Atualizado",
        "authors": "Autor Atualizado",
        "average_rating": 4.9
    }
    response = requests.put(BASE_URL + f'items/{book_id}', json=updated_info)
    if response.status_code == 200:
        print(f"Livro {book_id} atualizado com sucesso:")
        print(response.json())
    else:
        print(f"Erro ao atualizar o livro: {response.status_code}")

def delete_book(book_id):
    response = requests.delete(BASE_URL + f'items/{book_id}')
    if response.status_code == 200:
        print(f"Livro {book_id} deletado com sucesso:")
        print(response.json())
    else:
        print(f"Erro ao deletar o livro: {response.status_code}")