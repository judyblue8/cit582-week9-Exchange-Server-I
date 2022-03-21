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
    payload=content.get("payload")
    pk=payload.get("pk")
    platform=payload.get("platform")
    msg=json.dumps(payload)
    result=False
    if platform=="Ethereum":
        eth_encoded_msg =eth_account.messages.encode_defunct(text=msg)
        if eth_account.Account.recover_message(eth_encoded_msg ,signature=signature)==pk:
            print("Eth sig verifies!")
            result=True
    elif platform =="Algorand":
        #algo_sk = 'VDw/rBQ6ETI8kkpsXa3KQ7q3FFVKdNgL9Oem59c2Nixe4LyxB6otPKwHKpcWcJ2QxrBjPVj1XgON58ssS7I/JA=='
        #algo_pk = 'L3QLZMIHVIWTZLAHFKLRM4E5SDDLAYZ5LD2V4A4N47FSYS5SH4SAFAIYVQ'
        #algo_sig_str = algosdk.util.sign_bytes(payload.encode('utf-8'), algo_sk)
        if algosdk.util.verify_bytes(msg.encode('utf-8'), signature, pk):
            print("Algo sig verifies!")
            result=True
            
    #Check if signature is valid
    # result = True #Should only be true if signature validates
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
