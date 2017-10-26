import os  
from flask import Flask
import threading
from MLWorker import worker
from MLWorker.settings import MONGO_HOST, MONGO_PORT, MONGO_USERNAME, MONGO_PASSWORD, MONGO_DBNAME, WORKER_ID, SLEEP_TIME

app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"
 
 
def runWorker():
    mongo_uri = "mongodb://{username}:{password}@{host}:{port}/{database}".format(
            username=MONGO_USERNAME, password=MONGO_PASSWORD, host=MONGO_HOST, port=MONGO_PORT, database=MONGO_DBNAME)
    w = worker.Worker(mongo_uri=mongo_uri, db=MONGO_DBNAME, worker_id=WORKER_ID)
    w.run()
 
if __name__ == "__main__":
    t = threading.Thread(target=runWorker)
    t.daemon = True
    print ("*** about to start worker ***")
    t.start()
    
    port = int(os.environ.get('PORT', 5000)) 
    app.run(host='0.0.0.0', port=port)