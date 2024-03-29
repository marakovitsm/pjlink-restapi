from flask import Flask, request, jsonify
from pypjlink import Projector

projectorIP = "10.10.90.88"

inputMap = [
    {
        "friendlyName": "Desktop PC",
        "inputName": "HDMI1",
        "inputType": "DIGITAL",
        "inputNumber": 2
    },
    {
        "friendlyName": "AVR",
        "inputName": "HDMI2",
        "inputType": "DIGITAL",
        "inputNumber": 3
    }
]

app = Flask(__name__)

# Endpoint to get the status of the projector
@app.route('/projector/power/status', methods=['GET'])
def get_projector_status():
    projector = Projector.from_address(projectorIP)
    projector.authenticate()
    powerStatus = projector.get_power()
    return jsonify({'status': powerStatus})

# Endpoint to turn on the projector
@app.route('/projector/power/on', methods=['POST'])
def turn_on_projector():
    projector = Projector.from_address(projectorIP)
    projector.authenticate()
    projector.set_power('on')
    return jsonify({'message': 'Projector turned on'})

# Endpoint to turn off the projector
@app.route('/projector/power/off', methods=['POST'])
def turn_off_projector():
    projector = Projector.from_address(projectorIP)
    projector.authenticate()
    projector.set_power('off')
    return jsonify({'message': 'Projector turned off'})

# Endpoint to get the current input of the projector
@app.route('/projector/input/current', methods=['GET'])
def get_projector_input():
    projector = Projector.from_address(projectorIP)
    projector.authenticate()
    powerStatus = projector.get_power()

    if powerStatus == "off":
        return jsonify({'message': 'Projector is off'})
    
    inputStatus = projector.get_input()

    currentInputType = inputStatus[0]
    currentInputNumber = inputStatus[1]

    for input in inputMap:
        if input['inputType'] == currentInputType and input['inputNumber'] == currentInputNumber:
            return jsonify(input)

# Endpoint to get the list of available inputs of the projector
@app.route('/projector/inputs', methods=['GET'])
def get_projector_input_list():
    return jsonify(inputMap)

# Endpoint to set the input of the projector
@app.route('/projector/input/set', methods=['POST'])
def set_projector_input():
    projector = Projector.from_address(projectorIP)
    projector.authenticate()
    powerStatus = projector.get_power()

    if powerStatus == "off":
        return jsonify({'message': 'Projector is off'})
    
    requestInput = request.json['input']
    print(requestInput)

    foundInput = False

    for input in inputMap:
        if input["inputName"] == requestInput:
            foundInput = True
            inputType = input['inputType']
            inputNumber = input['inputNumber']
            break
    
    if not foundInput:
        return jsonify({'message': 'Input not found'})


    projector.set_input(inputType, inputNumber)
    return jsonify({'message': 'Input set to ' + input["inputName"]})        

if __name__ == '__main__':
    app.run(debug=False)