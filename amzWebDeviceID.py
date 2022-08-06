
# Importing the flask module
from flask import Flask
from amzGetDeviceID import getDeviceID
 
# Create a flask object named app
app = Flask(__name__)
 
# Once you enter the IP address of Raspberry Pi in the browser, below code will$
@app.route("/")
def main():
    
    return "Device ID: {}".format(getDeviceID())
 
#if code is run from terminal
if __name__ == "__main__":
    # Server will listen to port 80 and will report any errors.
   app.run(host='0.0.0.0', port=80, debug=True)


