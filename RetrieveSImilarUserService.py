
from flask import Flask, json, request
import pickle

app = Flask(__name__)

@app.route('/usersimilarity/<userhandle>', methods = ['GET'])
def retrieveSimilarUsers(userhandle):
    try:
        limit = int(request.args.get('limit', 10)) #default limit of 10
        userhandleId = int(userhandle)
        filename = '/home/SriGorti/mysite/result_indices.pkl'
        infile = open(filename, 'rb')
        similarityMatrix = pickle.load(infile)
        infile.close()
        return json.dumps(similarityMatrix[userhandleId][0:limit].tolist())
    except :
        return json.dumps("Unexpected Error")

@app.route('/', methods = ['GET'])
def initialFunction():
    return json.dumps('Welcome to user-similarity API, pls route to /usersimilarity/userHandleId for results')
