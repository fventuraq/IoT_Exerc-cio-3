#python server.py 192.168.0.35 5050

from threading import Thread
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP

import sys
import copy

class Atuador(Resource):
  def __init__(self,name="Atuador",coap_server=None):
    super(Atuador,self).__init__(name,coap_server,visible=True,observable=True,allow_children=True)
    self.payload = ["0" for _ in range(64)]
    self.resource_type = "rt1"
    self.content_type = "application/json"
    self.interface_type = "if1"

  def render_GET(self,request):
    newobj = copy.copy(self)
    newobj.payload = ''.join(newobj.payload)
    return newobj

  def render_POST(self, request):
    print "post"
    try:
      aux = request.payload.split("-")
      request.payload = self.payload
      i = int(aux[0])
      request.payload[i] = aux[1]
      seres = self.init_resource(request, Atuador())
      return seres
    except:
        print('Error')
        print request

  def render_PUT(self, request):
    print "update"
    try:
      aux = request.payload.split("-")
      request.payload = self.payload
      i = int(aux[0])
      request.payload[i] = aux[1]
      self.edit_resource(request)
      print request
      return self
    except:
        print('Error')
        print request

class Sensor(Resource):
  def __init__(self,name="Sensor",coap_server=None):
    super(Sensor,self).__init__(name,coap_server,visible=True,observable=True,allow_children=True)
    self.payload = ""
    self.resource_type = "rt1"
    self.content_type = "application/json"
    self.interface_type = "if1"

  def render_GET(self,request):
    # print self.payload
    # aux = self.payload.split("-")
    # obj = lambda: None
    # obj.temp = aux[0]
    # obj.pres = aux[1]
    # self.payload = obj
    return self

  def render_POST(self, request):
    seres = self.init_resource(request, Sensor())
    return seres

  def render_PUT(self, request):
      self.edit_resource(request)
      return self

class CoAPServer(CoAP):
  def __init__(self, host, port, multicast=False):
    CoAP.__init__(self,(host,port),multicast)
    self.add_resource('atuador/',Atuador())
    self.add_resource('s1/',Sensor())
    print "CoAP server started on {}:{}".format(str(host),str(port))
    print self.root.dump()

def pollUserInput(server):
  while 1:
    user_input = raw_input("Add New Sensor: ")
    print user_input
    server.add_resource(user_input, Sensor())

def main():
  ip = sys.argv[1] #localhost or IP
  port = int(sys.argv[2]) #5683
  multicast=False

  server = CoAPServer(ip,port,multicast)
  thread = Thread(target = pollUserInput, args=(server,))
  thread.setDaemon(True)
  thread.start()

  try:
    server.listen(10)
    print "executed after listen"
  except KeyboardInterrupt:
    print server.root.dump()
    server.close()
    sys.exit()

if __name__=="__main__":
  main()