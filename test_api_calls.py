import requests
import pytest
from requests.api import request
from werkzeug.datastructures import Headers
import bwtier_api
import json
from bwtier_api import BW_TIER_DATA
from configparser import ConfigParser
file = "config.ini"
config = ConfigParser()
config.read(file)

def test_get():
    '''This function is used to test fetching of bandwidth tier API data'''
    url_get = config['URL']['get']
    resp = requests.get(url_get)
    resp_data = resp.json()
    print("**********  GET URL  ************")
    print(url_get)
    print('\n')
    print(resp_data)
    print("**********************")
    print('')
    assert resp.status_code == 200, "Response code does not match"



def test_post():
    ''' This function is used to test creation of bandwidth data'''
    url_post = config['URL']['post']
    data = json.dumps(bwtier_api.BW_TIER_DATA)
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    resp = requests.post(url_post,data,headers)
    resp_data = resp.json()
    
    print(url_post)
    print("**********************")
    print('')
    url_get = config['URL']['get']
    resp_after_post = requests.get(url_get)
    post_data = resp_after_post.json()
    #print(post_data)
    '''Reversing the list so that comparison is made on the first index itself'''
    post_data.reverse()
    # print(resp_data)
    # print("**********************")
    # print('\n')
    # print(post_data[0])
    if resp_data == post_data[0]:
        # assert True
        print(resp_data)
        print('\n')
        print('****************MATCHES*************')
        print('\n')
        print(post_data[0])
    else:
        assert False
    
    assert resp.status_code == 200,"POST Operation Failed"
    


#@pytest.fixture
def test_put():
    ''' This function is used to test updation of bandwidth data'''
    url_put = config['URL']['put']
    
    data = json.dumps(bwtier_api.BW_TIER_DATA)
    resp = requests.put(url_put,data)
    resp_data = resp.json()
    print(url_put)
    print("**********************")
    print('\n')
    print("************* UPDATED DATA **********")
    print(resp_data)
    print("**********************")
    print('')
    url_get = config['URL']['get']
    resp_after_put = requests.get(url_get)
    put_data = resp_after_put.json()
    '''Reversing the list so that comparison is made on the first index itself'''
    put_data.reverse()
    if resp_data == put_data[0]:
        print(resp_data)
        print('\n')
        print('****************MATCHES*************')
        print('\n')
        print(put_data[0])
    else:
        assert False
    assert resp.status_code == 200,"Updation of Bandwidth tier failed"

#@pytest.fixture
def test_delete():
    ''' This function is used to test deletion of bandwidth data'''
    #url = 'http://127.0.0.1:5000/bwtier/1'
    url_delete = config['URL']['delete']
    resp = requests.delete(url_delete)
    resp_data = resp.json()
    print("**********************")
    print(url_delete)
    print('\n')
    #print(resp_data)
    # url_get = config['URL']['get']
    # resp_after_delete = requests.get(url_get)
    # data_after_delete = resp_after_delete.json()
    #print(data_after_delete)
    print("Requested data has been deleted")
    print("**********************")
    print('')
    print(resp_data)
    assert resp.status_code == 200,"Deletion of Bandwidth tier failed"
    
