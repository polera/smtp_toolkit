import socket

# Default timeout
socket.setdefaulttimeout(1.5)

class SMTPServerTest(object):
  PORTS = [25,]
  MESSAGE = 'ehlo'
  
  def __init__(self, server_name, additional_ports=None):
    if additional_ports:
        self.PORTS.extend(additional_ports)
    self.server = server_name
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._tried = False
    self._results = {}
     
  def connect(self):
    if self._tried:
        return self._results
    for port in self.PORTS:
      try:
        self.sock.connect((self.server, port))
        self.sock.send(self.MESSAGE)
        self._results[port] = {'connected':True, 'message':unicode(self.sock.recv(1024))}
      except socket.error:
        self._results[port] = {'connected':False, 'message':u'Connection failed'}
      self.sock.close()
    self._tried = True
    return self._results

  def get_results(self):
      self.connect()
      return self._results
  results = property(connect)
  
if __name__ == "__main__":
  server_list = ['mail.uncryptic.com',
                 'smtp.gmail.com']
  for server in server_list:
    print server
    s = SMTPServerTest(server)
    print s.results
