from flask import Flask,jsonify
import datetime
import hashlib
import json
import pytz
from flask_cors import CORS,cross_origin


class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof=100 , previous_hash='0')

    def create_block(self,proof,previous_hash):
        block={
            'index':len(self.chain)+1,
            'timestamp': str(datetime.datetime.now(pytz.timezone('Asia/Calcutta'))),
            'proof': proof,
            'previous_hash': previous_hash,
            }
        self.chain.append(block)

        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_op = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_op[:4]=='0000':
                check_proof=True
            else:
                new_proof += 1
        return new_proof

    def hash(self,block):
        encoded_block=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_validity(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block=chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return [False,'error1']
            previous_proof = previous_block['proof']
            proof=block['proof']
            hash_op=hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_op[0:4] != '0000':
                print(hash_op)
                return [False ,'error2']
            previous_block=block
            block_index += 1
        return [True]


app = Flask(__name__)
CORS(app, support_credentials=True)

blockchain = Blockchain()


@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    block=blockchain.create_block(proof,previous_hash)
    chain1={
        'message': 'Block successfully mined',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(chain1), 200


@app.route('/get_chain',methods = ['GET'])
def get_chain():
    response={'chain':blockchain.chain,
              'length': len(blockchain.chain)
              }
    return jsonify(response),200


@app.route('/is_it_valid',methods=['GET'])
def is_valid():
    x=blockchain.chain_validity(blockchain.chain)
    if(len(x)==1):
        answer=x[0]
    else:
        answer=x[0]
        err=x[1]

    if answer:
        response={'message': 'All good Captain! The chain remains toit'
                  }
    else:
        response={'message': 'Houston, there is slight problem! You have been defrauded. Ok bye! ',
                  'err': err}

    return jsonify(response),200


if __name__ == '__main__':
    app.run()
