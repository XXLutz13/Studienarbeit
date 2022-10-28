# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 11:18:40 2022

@author: Stefan.Bauer
@Start on RPI : python3.7 Cobotta_Rest_API_v03.py 10.50.12.87

"""
import sys
from argparse import ArgumentParser

from flask import Flask, jsonify
from flask_restful import Resource, Api, request


import pybcapclient.bcapclient as bcapclient

print ("Number of arguments:", len(sys.argv), "arguments.")
print ("Argument List:", str(sys.argv))

parser = ArgumentParser()
parser.add_argument("IP_C")
args = parser.parse_args()
print(args.IP_C)

# set IP Address , Port number and Timeout of connected RC8
host = args.IP_C
port = 5007
timeout = 2000

# Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
print("Open Connection")

# start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

# set Parameter
Name = ""
Provider = "CaoProv.DENSO.VRC"
Machine = args.IP_C
Option = ""

# Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connect RC8")


c_var =""

app = Flask(__name__)
api = Api(app)

class Cobotta(Resource):
    def get(self):
        return {'about': 'Cobotta Rest API',
                'Cobotta IP:': args.IP_C,
                'Get': 'http://x.x.x.x:5000/Cobotta_var_get/J0',
                'Put one value': 'http://x.x.x.x:5000/Cobotta_var_put?var_id=F1&value=45.8',
                'Put more values': 'http://x.x.x.x:5000/Cobotta_var_put?var_id=J0&value=1.1,3.2,3.3,4.4,5.5,6.6,0,0' 
                }
    
    def post(self):
        some_json = request.get_json()
        return {'you send': some_json},201

class Cobotta_var_put(Resource):    #http://127.0.0.1:5000/Cobotta_var_put?var_id=F1&value=4.5
    def get(self):
        var_cobotta = request.args.get('var_id')
        value = request.args.get('value')
        #print("Data:", value)
        #value = [1.1, 5.2, 3.3, 4.4, 5.5, 6.6, 0]
        Handl = 0
        Handl = m_bcapclient.controller_getvariable(hCtrl, var_cobotta, "")
        #ret_value = m_bcapclient.variable_getvalue(Handl)
        if var_cobotta[0] == 'J':
            new_value = value.split(',')
        else:
            new_value = value
        m_bcapclient.variable_putvalue(Handl,new_value)
        m_bcapclient.variable_release(Handl)
        #return (value)
        return jsonify({var_cobotta: new_value})
        #http://127.0.0.1:5000/Cobotta_var_put?var_id=F1&value=45.6
        #return '''Variable ID: {} value:{}'''.format(var_cobotta).format(value)
        #some_json = request.get_json()
        #return {'you send': some_json}
        #return{'result': 42}

class Cobotta_var_get(Resource):
    def get(self,c_var):
        Handl = 0
        Handl = m_bcapclient.controller_getvariable(hCtrl, c_var, "")
        # read value of c_var
        retI = m_bcapclient.variable_getvalue(Handl)
        m_bcapclient.variable_release(Handl)
        return{'result': retI}

class Cobotta_shutdown(Resource):
    def get(self):
        m_bcapclient.service_stop()
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('Not running werkzeug')
        shutdown_func()
        return{'result': 'Shutdown'}
        



api.add_resource(Cobotta, '/')
api.add_resource(Cobotta_shutdown, '/Shutdown')
api.add_resource(Cobotta_var_get, '/Cobotta_var_get/<string:c_var>')
api.add_resource(Cobotta_var_put, '/Cobotta_var_put')



    
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
