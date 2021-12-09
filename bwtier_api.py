from flask import Flask
from flask import json
from flask.json import jsonify
import pytest
import requests

BW_TIER_DATA = [{
    "bwtier_id":"0",
    "name":"DATA_1000M_BW_TEST",
    "downstreamPir":400000,
    "downstreamCir":200000,
    "upstreamCir":200000,
    "upstreamPir":400000
},
{
    "bwtier_id":"1",
    "name":"DATA_2000M_BW_TEST",
    "downstreamPir":400000,
    "downstreamCir":200000,
    "upstreamCir":200000,
    "upstreamPir":400000
},
{
    "bwtier_id":"2",
    "name":"DATA_3000M_BW_TEST",
    "downstreamPir":400000,
    "downstreamCir":200000,
    "upstreamCir":200000,
    "upstreamPir":400000
}]

app = Flask(__name__)    
        

@app.route('/')
def test_home_bwtier():
    return "This API is created for BW Tier profile testing"

@app.route('/bwtier/',methods=['GET'])
def get():
    #bwtier_data = open("bwtier_data.json","r").read()
    #data = json.loads(BW_TIER_DATA)
    #return jsonify({"BW TIER":BW_TIER_DATA})
    return json.dumps(BW_TIER_DATA)
    #return jsonify({BW_TIER_DATA})

# GET API call for fetching all BW_TIER data
@app.route('/bwtier/<int:bwtier_id>',methods=['GET'])
def get_bwtier(bwtier_id):
    # url = "http://localhost/5000/bwtier/"
    # resp = requests.get(url)
    # assert resp.status_code==200,"Response code does not match"
    return jsonify({'id':BW_TIER_DATA[bwtier_id]})

# POST API Call for creating a new BW_TIER_DATA
@app.route('/bwtier/create',methods=['POST'])
def create():
    new_bw_tier =[{
        "bwtier_id":"3",
        "name":"DATA_4000M_BW_TEST",
        "downstreamPir":400000,
        "downstreamCir":200000,
        "upstreamCir":200000,
        "upstreamPir":400000
    }]
    BW_TIER_DATA.append(new_bw_tier)
    #return jsonify({'BW TIER': new_bw_tier})
    return json.dumps(new_bw_tier)

# PUT API Call to update an existing BW_TIER_DATA
@app.route("/bwtier/update/<int:bwtier_id>",methods=['PUT'])
def bwtier_update(bwtier_id):
     BW_TIER_DATA[bwtier_id]['name']="XYZ"
     BW_TIER_DATA.append(BW_TIER_DATA[bwtier_id]) #updating the list after appending
     return json.dumps(BW_TIER_DATA[bwtier_id])


# DELETE API call to delete an existing BW_TIER_DATA
@app.route("/bwtier/delete/<int:bwtier_id>",methods= ['DELETE'])
def bwtier_delete(bwtier_id):
    #BW_TIER_DATA.remove(BW_TIER_DATA[bwtier_id])
    if(BW_TIER_DATA[bwtier_id] in BW_TIER_DATA):
        BW_TIER_DATA.remove(BW_TIER_DATA[bwtier_id])
    return json.dumps(BW_TIER_DATA)


if __name__ == "__main__":
    app.run(debug=True)

