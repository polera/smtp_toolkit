import socket

# Default timeout
socket.setdefaulttimeout(1.5)

class SMTPServerTest(object):
  PORTS = [25]
  MESSAGE = 'ehlo listbot.org\n'
  
  def __init__(self, server_name, additional_ports=None):
    if additional_ports:
        self.PORTS.extend(additional_ports)
    self.server         = server_name
    self.sock           = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._tried         = False
    self._results       = {}
    self._ehlo_port     = None
    self._ehlo_response = None
    self._conversation  = False

  def get_max_message_size(self):
    size_option = filter(lambda x: x.split(" ")[0] == "250-SIZE",self.ehlo_options)[0]
    size_bytes = size_option.split(" ")[1]
    return long(size_bytes)/1024.0/1024.0
  server_max_message_size = property(get_max_message_size)
    
  def get_server_supports_tls(self):
    return "250-STARTTLS" in self.ehlo_options
  server_supports_tls = property(get_server_supports_tls)
  
  def parse_ehlo(self):
    if not self._ehlo_response:
      self._ehlo_response = self.get_ehlo()
    return filter(lambda x: x[:4] == '250-',self._ehlo_response.split("\r\n"))[1:]
  ehlo_options = property(parse_ehlo)
           
  def get_ehlo(self):
    self.connect()
    try:
      self.sock.send(self.MESSAGE)
      return self.sock.recv(1024)
    except Exception, e:
      print str(e)
      return "ehlo failed."
  ehlo = property(get_ehlo)
  
  def is_open_relay(self):
    if not self._conversation:
      self._conversation = self.get_conversation()
    relay_results = filter(lambda x: x[:4] == '554',self._conversation.split("\r\n"))[1:]
    if relay_results > 0:
      return False
    return True
  open_relay = property(is_open_relay)
  
  def get_conversation(self):
    self._conversation = True
    self.sock.send(self.MESSAGE)
    self.sock.send("mail from: axdjdiai@akxkskd.com\n")
    self.sock.send("rcpt to: aserjslkejrlskj@laslkjelrkjlekj.com\n")
    return self.sock.recv(1024)
  
  def connect(self):
    if self._tried:
        return self._results
    for port in self.PORTS:
      try:
        self.sock.connect((self.server, port))
        self._results[port] = {'connected':True, 'message':unicode(self.sock.recv(1024))}
        self._ehlo_port     = port
      except socket.error:
        self._results[port] = {'connected':False, 'message':u'Connection failed'}
    self._tried = True
    return self._results

  def get_results(self):
      self.connect()
      return self._results
  results = property(connect)
  
if __name__ == "__main__":
  server_list = ['smtp.gmail.com']
  for server in server_list:
    print server
    s = SMTPServerTest(server)
    print s.results
    print("EHLO options %s" % ", ".join(s.ehlo_options))
    print("TLS Supported? %s" % s.server_supports_tls)
    print("Max message size: %d MB" % s.server_max_message_size)
    print("Open relay? %s" % s.open_relay)