import timeit
import subprocess
from flask import Flask, request, jsonify
import os

# Clarifai API
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

is_set_api_key = True

if os.getenv('CLARIFAI_API_KEY') is None:
    print("Set the value CLARIFAI_API_KEY")
    print("export CLARIFAI_API_KEY='YOUR_CLARIFAI_API_KEY'")
    is_set_api_key = False

if is_set_api_key:
    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
    metadata = (('authorization', 'Key ' + os.getenv('CLARIFAI_API_KEY')),)

app = Flask(__name__)

def detect_person(image_name):
    if is_set_api_key:
        return False
    person_like_names = ['Human', 'Person']

    with open(image_name, "rb") as f:
        file_bytes = f.read()

    request = service_pb2.PostModelOutputsRequest(
        model_id='9f54c0342741574068ec696ddbebd699', # General Detection V2
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                    )
                )
            )
        ]
    )
    response = stub.PostModelOutputs(request, metadata=metadata)
    for regions in response.outputs[0].data.regions:
        lower_name = regions.data.concepts[0].name.lower()
        for person_like_name in person_like_names:
            if lower_name.count(person_like_name.lower()) > 0:
                return True

    return False

@app.route('/', methods = ['GET'])
def index():
    return 'Hello, this is image-detect-server'

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        image_file_name = 'image_temp.png'

        # save the file
        f.save('./' + image_file_name)

        # detect a person
        start_time = timeit.default_timer()
        print('Processing image...')
        is_there_anyone = detect_person(image_file_name)
        print('Processing completed')
        terminate_time = timeit.default_timer()
        print("Process Time : %fs" % (terminate_time - start_time))

        # Returns HTTP Response with {"is_there_anyone": boolean}
        return jsonify(is_there_anyone=is_there_anyone)
