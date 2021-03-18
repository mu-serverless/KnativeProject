from flask import Flask, request
import numpy as np
import random
import time
from tempfile import TemporaryFile

app = Flask(__name__)

@app.route("/")
def index():
    try:
        memory = max(int(request.args.get('memory')), 0) # size of data to store in RAM in megabytes
  
        duration = max(int(request.args.get('duration')), 0)     # determines how many random numbers are 
    except:
        memory = 0
        duration = 0
                                                     # generated and added for each cell in the array

#    sleep  = int(request.args.get('sleep'))          # the number of seconds the request will go to
                                                     # sleep before returning the result

#    disk   = bool(request.args.get('disk'))          # weather to write the content of array to disk

    if memory > 0:
        arr = np.zeros(memory*1024*1024//32)
    if duration > 0:
        for i in range(duration):
            for j in range(10):
                arr[i] += random.randint(0,arr.shape[0])
                    
#    if disk:
#        file = TemporaryFile()
#        np.save(file,arr)
#        file.close()

#    if sleep > 0:
#        time.sleep(sleep)
    
    return "Memory: %d, duration: %d\n" % (memory, duration)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
