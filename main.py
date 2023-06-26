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
    
def map_values(value):
    if value == "NULL":
        return "None"
    return value

def get_data(type, id):
    body = {}
    body["nftType"]=type
    body["withGene"]=True
    body["tokenIds"]=[id]#
    response = requests.request("POST", url, headers=headers, data=str(json.dumps(body)))
    pe = json.loads(response.text)
    genes = pe[0]["championRecessiveGene"]
    genes = dict((k, map_values(v)) for k,v in genes.items())
    for key in list(genes.keys()):
        if "warPaint" in key:
            key_new=key.replace("warPaint", "warpaint")
            genes[key_new] = genes.pop(key)
    purity=0
    for attribute in pe[0]["contentMetadata"]["attributes"]:
        if attribute["trait_type"] == "Purity":
            purity=attribute["value"]
    genes["purity"]=int(purity)
    return genes

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True, use_reloader=False)

