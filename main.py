#!/bin/env python3
from flask import Flask
from flask import request
import requests
import json

app = Flask(__name__)
   
url = "https://champions.io/api/nft-metadata"

headers = {
  'Content-Type': 'text/plain'
}

@app.after_request
def apply_caching(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.route('/prime/<id>', methods=['GET'])
def get_prime_data(id):
    return get_data("PrimeEternalChampion", id)

@app.route('/elemental/<id>', methods=['GET'])
def get_elemental_data(id):
    return get_data("ElementalChampion", id)
    
def get_data(type, id):
    body = {}
    body["nftType"]=type
    body["withGene"]=True
    body["tokenIds"]=[id]#
    response = requests.request("POST", url, headers=headers, data=str(json.dumps(body)))
    pe = json.loads(response.text)
    genes = pe[0]["championRecessiveGene"]
    return genes

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True, use_reloader=False)

