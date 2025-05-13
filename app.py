from flask import Flask, jsonify, request, render_template
import hashlib
import json
from datetime import datetime

app = Flask(__name__)

blockchain = []

def create_genesis_block():
    return {
        'index': 0,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': 'Genesis Block',
        'previous_hash': '0',
        'hash': ''
    }

def hash_block(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

# Create genesis block
genesis = create_genesis_block()
genesis['hash'] = hash_block(genesis)
blockchain.append(genesis)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain)

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.json['data']
    prev_block = blockchain[-1]
    new_block = {
        'index': len(blockchain),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Fixed here
        'data': data,
        'previous_hash': prev_block['hash'],
    }
    new_block['hash'] = hash_block(new_block)
    blockchain.append(new_block)
    return jsonify(new_block), 201

if __name__ == '__main__':
    app.run(debug=True)
