import requests
import pytest
from requests.api import request
from werkzeug.datastructures import Headers
import test_bwtier_api
import json
from test_bwtier_api import BW_TIER_DATA

def test_get():
    '''This function is used to test fetching of bandwidth tier API data'''
    url= "http://127.0.0.1:5000/bwtier"
    resp = requests.get(url)
    resp_data = resp.json()
    print("**********************")
    print(url)
    print(resp_data)
    print("**********************")
    print('')
    assert resp.status_code == 200, "Response code does not match"



def test_post():
    ''' This function is used to test creation of bandwidth data'''
    BASE_URL = 'http://127.0.0.1:5000/bwtier'
    #base_url = request.url
    url = BASE_URL + '/create'
    data = json.dumps(test_bwtier_api.BW_TIER_DATA)
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    resp = requests.post(url,data,headers)
    resp_data = resp.json()
    print("**********************")
    print(url)
    print(resp_data)
    print("**********************")
    print('')
    assert resp.status_code == 200
    


#@pytest.fixture
def test_put():
    ''' This function is used to test updation of bandwidth data'''
    url = 'http://127.0.0.1:5000/bwtier/0'
    #url = BASE_URL + BW_TIER_DATA['bwtier_id']
    data = json.dumps(test_bwtier_api.BW_TIER_DATA)
    #headers = {'Accept':'application/json','Content-Type':'application/json'}
    resp = requests.put(url,data)
    resp_data = resp.json()
    print("**********************")
    print(url)
    print(resp_data)
    print("**********************")
    print('')
    assert resp.status_code == 200,"Updation of Bandwidth tier failed"

#@pytest.fixture
def test_delete():
    ''' This function is used to test deletion of bandwidth data'''
    url = 'http://127.0.0.1:5000/bwtier/1'
   
    #url = BASE_URL + '/bwtier_id'
    data = json.dumps(test_bwtier_api.BW_TIER_DATA)
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    resp = requests.delete(url)
    resp_data = resp.json()
    print("**********************")
    print(url)
    print(resp_data)
    print("**********************")
    print('')
    assert resp.status_code == 200,"Deletion of Bandwidth tier failed"