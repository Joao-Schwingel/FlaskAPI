from flask import Flask, jsonify, request
import pandas as pd
import csv

app = Flask(__name__)

class Book:
    def __init__(self, bookID, title, authors, average_rating, language_code, num_pages, text_reviews_count):
        self.bookID = bookID
        self.title = title
        self.authors = authors
        self.average_rating = average_rating
        self.language_code = language_code
        self.num_pages = num_pages
        self.text_reviews_count = text_reviews_count

df = pd.read_csv('booksAPI.csv')

books_list = [
    Book(row['bookID'], row['title'], row['authors'], row['average_rating'], row['language_code'], row['num_pages'], row['text_reviews_count'])
    for _, row in df.iterrows()
]

def book_to_dict(book):
    return {
        'bookID': book.bookID,
        'title': book.title,
        'authors': book.authors,
        'average_rating': book.average_rating,
        'language_code': book.language_code,
        'num_pages': book.num_pages,
        'text_reviews_count': book.text_reviews_count
    }

data = [book_to_dict(book) for book in books_list]

def append_to_csv(book):
    with open('booksAPI.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=book_to_dict(book).keys())
        writer.writerow(book_to_dict(book))

def save_to_csv():
    df = pd.DataFrame([book_to_dict(book) for book in books_list])
    df.to_csv('booksAPI.csv', index=False)

@app.route('/', methods=['GET'])
def welcome():
    return "Bem-vindo à API de Livros!", 200

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    book = next((b for b in books_list if b.bookID == item_id), None)
    if book is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(book_to_dict(book))

@app.route('/items', methods=['POST'])
def add_item():
    item = request.json
    new_book = Book(
        bookID=len(data) + 1,
        title=item['title'],
        authors=item['authors'],
        average_rating=item['average_rating'],
        language_code=item['language_code'],
        num_pages=item['num_pages'],
        text_reviews_count=item['text_reviews_count']
    )
    books_list.append(new_book)
    data.append(book_to_dict(new_book))
    append_to_csv(new_book)
    return jsonify(book_to_dict(new_book)), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    book = next((b for b in books_list if b.bookID == item_id), None)
    if book is None:
        return jsonify({'error': 'Item not found'}), 404
    
    item = request.json
    book.title = item.get('title', book.title)
    book.authors = item.get('authors', book.authors)
    book.average_rating = item.get('average_rating', book.average_rating)
    book.language_code = item.get('language_code', book.language_code)
    book.num_pages = item.get('num_pages', book.num_pages)
    book.text_reviews_count = item.get('text_reviews_count', book.text_reviews_count)
    
    index = books_list.index(book)
    data[index] = book_to_dict(book)
    
    return jsonify(book_to_dict(book))

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    book = next((b for b in books_list if b.bookID == item_id), None)
    if book is None:
        return jsonify({'error': 'Item not found'}), 404
    
    books_list.remove(book)
    data.remove(book_to_dict(book))

    return jsonify(book_to_dict(book))

if __name__ == '__main__':
    app.run(debug=True)
