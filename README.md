smtp_toolkit
==
The goal of smtp_toolkit is to provide a set of classes that facilitate testing email servers with Python.

Author
==
James Polera <james@listbot.org>

Usage
==

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