import socket

# Default timeout
socket.setdefaulttimeout(2.5)

class SMTPConnectionFailed(Exception):
    pass

class SMTPServer(object):

    def __init__(self, server_name, port=587, message='ehlo polera.org\r\n', ipv6=False):
        self.server = server_name
        self.port = port
        self.ipv6 = ipv6
        self._tried_connection = False
        self._connection_results = None
        self._ehlo_port = None
        self._ehlo_response = None
        self._conversation = None
        self._message = message
        self._socket = None
        self._connected = False

    def get_ip_version(self):
        if self.ipv6:
            return "IPv6"
        else:
            return "IPv4"
    ip_version = property(get_ip_version)
    
    def get_socket(self):
        if self._socket:
            return self._socket
        else:
            if self.ipv6:
                self._socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            else:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return self._socket
    sock = property(get_socket)
    
    def get_max_message_size(self):
      try:
          size_option = filter(lambda x: x.split(" ")[0] == "250-SIZE",self.ehlo_options)[0]
          splitter = "250-SIZE"
      except IndexError:
          try:
              size_option = filter(lambda x: x.split("250 SIZE")[0] == "",self.ehlo_options)[0]
              splitter = "250 SIZE"
          except IndexError:
              return 0
      size_bytes = size_option.split(splitter)[1]
      return long(size_bytes)/1024.0/1024.0
    server_max_message_size = property(get_max_message_size)

    def get_server_supports_tls(self):
      return "250-STARTTLS" in self.ehlo_options
    server_supports_tls = property(get_server_supports_tls)

    def parse_ehlo(self):
      if not self._ehlo_response:
        self._ehlo_response = self.get_ehlo()
      return filter(lambda x: x[:3] == '250',self._ehlo_response.split("\r\n"))
    ehlo_options = property(parse_ehlo)

    def get_ehlo(self):
      if not self._connected:
        self.connect()
      try:
        self.sock.send(self._message)
        return self.sock.recv(1024)
      except Exception, e:
        print str(e)
        return "ehlo failed."
    ehlo = property(get_ehlo)

    def is_open_relay(self):
      if not self._conversation:
        self._conversation = self.have_relay_conversation()
      relay_results = filter(lambda x: x.replace("-"," ").lower().find('250 ok') != -1,self._conversation.split("\r\n"))[1:]
      self.close()
      if len(relay_results) > 0:
        return True
      return False
    open_relay = property(is_open_relay)

    def have_relay_conversation(self):
      if not self._connected:
          self.connect()
      self._conversation = True
      self.sock.send(self._message)
      self.sock.send("mail from: axdjdiai@akxkskd.com\n")
      self.sock.send("rcpt to: aserjslkejrlskj@laslkjelrkjlekj.com\n")
      return self.sock.recv(1024)

    def connect(self):
        if not self._connected:
            try:
              self.sock.connect((self.server, self.port))
              self._connection_results = {'connected':True, 'message':unicode(self.sock.recv(1024))}
              self._ehlo_port          = self.port
              self._connected = True
            except socket.error:
              self._connection_results = {'connected':False, 'message':u'Connection failed'}
              self._socket = None
              raise(SMTPConnectionFailed('Connection failed'))
        return self._connection_results

    def close(self):
        self.sock.send("quit")
        self._socket = None
        self._connected = False
        return True

    def get_results(self):
        self.connect()
        self.close()
        return self._connection_results
    results = property(get_results)


if __name__ == "__main__":
  server_list = [{'server_name':'mail.optonline.net','port':25, 'try_v6':False},
                 {'server_name':'smtp.gmail.com','port':587, 'try_v6':False},
                 {'server_name':'he.net', 'port':25, 'try_v6':True}]
  for server in server_list:
    print("Attepmting to connect to %s on port %d" % (server['server_name'],server['port']))
    s = SMTPServer(server['server_name'], server['port'], ipv6=server['try_v6'])
    try:
        print("Open relay? %s" % s.open_relay)
        print("EHLO options: %s" % ",".join(s.ehlo_options))
        print("TLS Supported? %s" % s.server_supports_tls)
        print("Max message size: %d MB" % s.server_max_message_size)
        print s.results, "\n"
    except SMTPConnectionFailed as error:
        print("""Error connection failed.  This means that the server is down, or your ISP does not allow you to
                 connect to other SMTP servers on the specified port (%d) (over %s)""" % (s.port, s.ip_version))
