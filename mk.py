import json
H={"X-Correlation-Id":{"description":"Correlation ID for tracing","schema":{"type":"string","format":"uuid"}}}
def err(code,desc): return {str(code):{"description":desc,"headers":H,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/ErrorResponse"},"example":{"code":"ERR","message":desc}}}}}
sec=[{"apiKey":[]}]
def ok(code,desc,ref,extra=None):
    r={"description":desc,"headers":dict(H),"content":{"application/json":{"schema":ref}}}
    if extra: r["headers"].update(extra)
    return {str(code):r}
item={"$ref":"#/components/schemas/Item"}
paths={
"/zz-rich/v1/items":{
 "get":{"tags":["ZzRich/Items"],"summary":"List items","operationId":"zzListItems","security":sec,
  "description":"Returns a page of items.",
  "parameters":[
   {"name":"status","in":"query","required":False,"description":"Restrict to these statuses. Repeatable.","schema":{"type":"array","items":{"type":"string","enum":["ACTIVE","RETIRED"]}},"explode":True},
   {"name":"limit","in":"query","required":False,"description":"Maximum items per page.","schema":{"type":"integer","minimum":1,"maximum":100,"default":20}},
   {"name":"page","in":"query","required":False,"description":"Page number, from 1.","schema":{"type":"integer","minimum":1}}],
  "responses":{**ok(200,"A page of items",{"$ref":"#/components/schemas/ItemPage"}),**err(400,"Bad request"),**err(401,"Unauthorized"),**err(422,"Unprocessable")}},
 "post":{"tags":["ZzRich/Items"],"summary":"Create item","operationId":"zzCreateItem","security":sec,
  "requestBody":{"required":True,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/ItemInput"},"example":{"name":"Alpha","status":"ACTIVE"}}}},
  "responses":{**ok(201,"Created",item,{"Location":{"description":"URL of the new item","schema":{"type":"string"}}}),**err(400,"Bad request"),**err(401,"Unauthorized")}}},
"/zz-rich/v1/items/{id}":{
 "parameters":[{"name":"id","in":"path","required":True,"description":"Item id.","schema":{"type":"string","format":"uuid"}}],
 "get":{"tags":["ZzRich/Items"],"summary":"Get item","operationId":"zzGetItem","security":sec,
  "responses":{**ok(200,"The item",item),**err(401,"Unauthorized"),**err(404,"Not found")}},
 "put":{"tags":["ZzRich/Items"],"summary":"Edit item","operationId":"zzEditItem","security":sec,
  "requestBody":{"required":True,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/ItemInput"}}}},
  "responses":{**ok(200,"Updated",item),**err(400,"Bad request"),**err(404,"Not found")}},
 "delete":{"tags":["ZzRich/Items"],"summary":"Delete item","operationId":"zzDeleteItem","security":sec,
  "responses":{"204":{"description":"Deleted","headers":dict(H)},**err(404,"Not found")}}},
"/zz-rich/v1/owners":{
 "get":{"tags":["ZzRich/Owners"],"summary":"List owners","operationId":"zzListOwners","security":[{"oauth2":["read"]}],
  "responses":{**ok(200,"Owners",{"type":"array","items":{"$ref":"#/components/schemas/Owner"}}),**err(401,"Unauthorized")}}},
"/zz-rich/v1/owners/{id}":{
 "parameters":[{"name":"id","in":"path","required":True,"description":"Owner id.","schema":{"type":"string","format":"uuid"}}],
 "get":{"tags":["ZzRich/Owners"],"summary":"Get owner","operationId":"zzGetOwner","security":[{"oauth2":["read"]}],
  "responses":{**ok(200,"The owner",{"$ref":"#/components/schemas/Owner"}),**err(404,"Not found")}}}}
schemas={
"ErrorResponse":{"type":"object","required":["code","message"],"properties":{"code":{"type":"string"},"message":{"type":"string"}}},
"Meta":{"type":"object","properties":{"total":{"type":"integer"},"page":{"type":"integer"}}},
"Owner":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}},
"ItemInput":{"type":"object","required":["name"],"properties":{"name":{"type":"string","maxLength":80},"status":{"type":"string","enum":["ACTIVE","RETIRED"]}}},
"Item":{"allOf":[{"$ref":"#/components/schemas/ItemInput"},{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"owner":{"allOf":[{"$ref":"#/components/schemas/Owner"}],"nullable":True},"tags":{"type":"array","items":{"type":"string"}},"score":{"type":"number","nullable":True,"example":12.5}}}]},
"ItemPage":{"type":"object","properties":{"data":{"type":"array","items":{"$ref":"#/components/schemas/Item"}},"meta":{"$ref":"#/components/schemas/Meta"}}}}
spec={"openapi":"3.0.3","info":{"title":"Zz Rich toy","version":"1"},"servers":[{"url":"https://api.example.com"}],
"tags":[{"name":"ZzRich/Items"},{"name":"ZzRich/Owners"}],"paths":paths,
"components":{"schemas":schemas,"securitySchemes":{"apiKey":{"type":"apiKey","in":"header","name":"API-KEY"},"oauth2":{"type":"oauth2","flows":{"clientCredentials":{"tokenUrl":"https://auth.example.com/token","scopes":{"read":"Read access"}}}}}}}
json.dump(spec,open("contracts/rich.json","w"),indent=2)
print(len(paths),"paths")
