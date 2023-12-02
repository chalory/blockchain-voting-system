# Install necessary libraries:
# pip install Flask web3 pycryptodome syft

from flask import Flask, request, jsonify
import torch
import syft as sy
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from blockchain import Blockchain
from syft.core.hooks.torch import TorchHook


app = Flask(__name__)

# Initialize PySyft
hook = sy.TorchHook(torch)

# Create virtual workers
alice = sy.VirtualWorker(hook, id="alice")
bob = sy.VirtualWorker(hook, id="bob")

# Create a blockchain instance
blockchain = Blockchain()

# Placeholder for voter registration
registered_voters = set()

# Placeholder for homomorphic encryption
def encrypt_vote(vote, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(vote.encode())

# Placeholder for decryption (assuming the private key is stored securely)
def decrypt_vote(encrypted_vote, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(encrypted_vote).decode()

@app.route('/register', methods=['POST'])
def register_voter():
    data = request.get_json()
    voter_id = data.get('voter_id')

    if not voter_id:
        return jsonify({'error': 'Voter ID is required'}), 400

    registered_voters.add(voter_id)
    return jsonify({'message': 'Voter registered successfully'}), 200

@app.route('/vote', methods=['POST'])
def cast_vote():
    data = request.get_json()
    voter_id = data.get('voter_id')
    candidate = data.get('candidate')

    if not (voter_id and candidate):
        return jsonify({'error': 'Voter ID and candidate are required'}), 400

    if voter_id not in registered_voters:
        return jsonify({'error': 'Voter is not registered'}), 401

    # Placeholder for homomorphic encryption
    public_key = RSA.generate(2048).publickey()
    encrypted_vote = encrypt_vote(candidate, public_key)

    # Placeholder for blockchain transaction
    blockchain.new_transaction(voter_id, candidate, encrypted_vote)

    return jsonify({'message': 'Vote cast successfully'}), 200

@app.route('/get_chain', methods=['GET'])
def get_blockchain():
    chain = []
    for block in blockchain.chain:
        chain.append({
            'index': block.index,
            'transactions': block.transactions,
            'previous_hash': block.previous_hash,
        })
    return jsonify({'chain': chain, 'length': len(chain)}), 200

if __name__ == '__main__':
    app.run(debug=True)
