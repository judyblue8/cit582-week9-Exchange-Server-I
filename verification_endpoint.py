from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)
    signature=content.get("sig")
    pload=content.get("payload")
    pk=pload.get("pk")
    platform=pload.get("platform")
    message=json.dumps(pload)
    result=False
    if platform=="Ethereum":
        eth_encoded_msg =eth_account.messages.encode_defunct(text=message)
        if eth_account.Account.recover_message(eth_encoded_msg ,signature=signature)==pk:
            print("Eth sig verifies!")
            result=True
    elif platform =="Algorand":
        #algo_sk = 't0oauFzGhzUxkgKboxhxlpgTQoHgE0y5/uzz/zr1jnimyyZnoLkmCJgqmY5+ntM7WFhLxAr8u7bCd1wmgX4OgA=='
        #algo_pk = 'U3FSMZ5AXETARGBKTGHH5HWTHNMFQS6EBL6LXNWCO5OCNAL6B2AFXLZMTY'
        #algo_sig_str = algosdk.util.sign_bytes(pload.encode('utf-8'), algo_sk)
        if algosdk.util.verify_bytes(message.encode('utf-8'), signature, pk):
            print("Algo sig verifies!")
            result=True
            
    #Check if signature is valid
    # result = True #Should only be true if signature validates
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
