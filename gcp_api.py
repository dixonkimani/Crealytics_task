#!/usr/bin/python3
import googleapiclient.discovery
from flask import Flask
from flask import jsonify
import time
import os

app = Flask(__name__)

compute = googleapiclient.discovery.build('compute', 'v1')

#Healthcheck route
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    result = "OK"
    return result

@app.route('/v1/instances/create/<project>/<zone>/<name>', methods=['POST'])
def create_instance(project,zone,name):
    image_response = compute.images().getFromFamily(project='ubuntu-os-cloud', family='ubuntu-1604-lts').execute()
    source_disk_image = image_response['selfLink']
    startup_script = open('startup.sh').read()

    config = {
        'name': name,
        'machineType': "zones/%s/machineTypes/g1-small" % zone,
        'disks': [{
            'boot': True,
            'autoDelete': True,
            'initializeParams': {
                    'sourceImage': source_disk_image,
                }
        }],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [{
                    'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'
                    }]
        }],
        'metadata': {
            'items': [{
                'key': 'startup-script',
                'value': startup_script
            }]
        }
    }

    operation = compute.instances().insert(project=project,zone=zone,body=config).execute()

    #Wait for the instance to finish and output to public IP
    while True:
        result = compute.zoneOperations().get(project=project,zone=zone,operation=operation['name']).execute()
        if result['status'] == 'DONE':
            instanceresult = compute.instances().get(project=project, zone=zone, instance=name).execute()
            if 'error' in result:
                raise Exception(result['error'])
            return jsonify(instanceresult["networkInterfaces"][0]["accessConfigs"][0]["natIP"])
        time.sleep(5)

if __name__ == '__main__':
    app.run(debug=False)

#https://cloud.google.com/sdk/downloads#linux
#https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
#https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/compute/api/create_instance.py
