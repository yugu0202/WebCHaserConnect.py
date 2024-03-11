import phxsocket
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

class Client:
  def __init__(self, name, host=None, secure=True, port=443):
    self.host = host if host else input("接続先IPアドレスを入力してください: ")
    self.port = port
    self.token = input("トークンを入力してください: ")
    self.name = name
    self.is_ready = False

    self.socket = phxsocket.Client(f"ws{"s" if secure else ""}://{self.host}:{self.port}/client/websocket", {"token": self.token})
    if self.socket.connect():
      self.channel = self.socket.channel(f"client:lobby")
      resp = self.channel.join()
      print(resp)
      self.client_topic = resp["subtopic"]
      self.channel.leave()
      self.client_channel = self.socket.channel(f"client:{self.client_topic}")
      self.client_channel.join()

    self.client_channel.on("match", self.match)
    self.match_topic = None

    self.wait_for_match()

    self.match_channel = self.socket.channel(f"match:{self.match_topic}")
    self.match_channel.join()

    print("connected")
    
    self.socket.is_end = False

    self.match_channel.on("ready", self.ready)

    self.socket.on_close = lambda: print("close")

    self.matching()

  def send(self, data):
    print(f"{self.name}は{data["action"]}を送信しました")
    message = self.match_channel.push("call", data, reply=True)
    return message.wait_for_response()


  def matching(self):
    self.match_channel.push("call", {"action": "matching"})

  def getReady(self):
    self.wait_for_ready()
    return self.send({"action": "getready"})["response"]["data"]

  #walk
  def walkUp(self):
    return self.send({"action": "walkup"})["response"]["data"]

  def walkRight(self):
    return self.send({"action": "walkright"})["response"]["data"]
  
  def walkDown(self):
    return self.send({"action": "walkdown"})["response"]["data"]
  
  def walkLeft(self):
    return self.send({"action": "walkleft"})["response"]["data"]

  #look
  def lookUp(self):
    return self.send({"action": "lookup"})["response"]["data"]

  def lookRight(self):
    return self.send({"action": "lookright"})["response"]["data"]
  
  def lookDown(self):
    return self.send({"action": "lookdown"})["response"]["data"]
  
  def lookLeft(self):
    return self.send({"action": "lookleft"})["response"]["data"]

  #search
  def searchUp(self):
    return self.send({"action": "searchup"})["response"]["data"]
  
  def searchRight(self):
    return self.send({"action": "searchright"})["response"]["data"]
  
  def searchDown(self):
    return self.send({"action": "searchdown"})["response"]["data"]
  
  def searchLeft(self):
    return self.send({"action": "searchleft"})["response"]["data"]

  #put
  def putUp(self):
    return self.send({"action": "putup"})["response"]["data"]
  
  def putRight(self):
    return self.send({"action": "putright"})["response"]["data"]
  
  def putDown(self):
    return self.send({"action": "putdown"})["response"]["data"]
  
  def putLeft(self):
    return self.send({"action": "putleft"})["response"]["data"]

  #ready callback
  def ready(self, _payload):
    print(_payload)
    self.is_ready = True

  #wait ready callback
  def wait_for_ready(self):
    while not self.is_ready:
      pass
    self.is_ready = False

  def match(self, payload):
    print(payload)
    self.match_topic = payload["subtopic"]

  def wait_for_match(self):
    while not self.match_topic:
      pass
