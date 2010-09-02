smtp_toolkit
==
The goal of smtp_toolkit is to provide a set of classes that facilitate testing email servers with Python.

Author
==
James Polera <james@listbot.org>

Usage
==

Talking to the server
--
    from smtp_toolkit import SMTPServerTest

    server_list = ['smtp.gmail.com']
  
    for server in server_list:
      print(server)
      s = SMTPServerTest(server)
      print(s.results)
      print("EHLO options %s" % ", ".join(s.ehlo_options))
      print("TLS Supported? %s" % s.server_supports_tls)
      print("Max message size: %d MB" % s.server_max_message_size)


Testing a server for a response on port 25 (standard SMTP)
--

    from smtp_toolkit import SMTPServerTest
    server = SMTPServerTest('your.server.com')
    print(server.results)
    
Testing a server for a response on port 25 + additional ports
--

    from smtp_toolkit import SMTPServerTest
    server = SMTPServerTest('your.server.com',[587,987,])
    print(server.results)
    