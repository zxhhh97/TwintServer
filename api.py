#encoding: utf-8
from coreweb import app
from flask import request
import requests,json
from src.twint_utils import TwintSearch
#from config import configs
#注意每个客户端同时操作 session['user']的返回结果都是不一样的

@app.route('/index')
def example():
    return 'Hello World!'
        
@app.after_request
def after_request(resp):
    source="*"
    if request.origin:
        source=request.origin
    elif request.headers.get('source'):
        source=request.headers.get('source')
    resp.headers['Access-Control-Allow-Origin'] = source
    resp.headers['Access-Control-Allow-Headers'] = "source" 
    resp.headers['Access-Control-Allow-Credentials'] = "true"
    return resp


def to_jsonstr(json_data,message = ""):
    json_obj = {}
    json_obj['data'] = json_data
    if message != 'ok':
        json_obj['type'] = "error"
        json_obj['message'] = message
    json_str = json.dumps(json_obj, ensure_ascii=False)
    return json_str


@app.route('/search/tweets/new',methods=['POST',"GET"]) 
def api_search_tweets(*args,**kw):
    kw = request.values.to_dict()
    print(kw)
    
    t = TwintSearch()
    res = t.search_username_tweets(kw)
    if  'Error' in res :
        result = {"type":"error",
                "message":res["Error"],
                "data":[],
                **kw
        }
        print(result)
        return result
    res = res.to_dict(orient="records")
    res = to_jsonstr(res,message = "ok")
    return res


def main():
    app.run(host='0.0.0.0',port=8900,debug=True)
    
    
if __name__ == "__main__":
    main()
