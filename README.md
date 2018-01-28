pyrebind
========

pyrebind is a very simple DNS server written in Python for testing software against DNS rebinding vulnerabilities. The server responds to queries by randomly selecting one of the IP addresses specified in the requested domain name and returning it as the answer with the lowest possible TTL=1.

https://en.wikipedia.org/wiki/DNS_rebinding

For example, to switch between `127.0.0.1` and `10.10.10.10` you would need to encode them like this:

```
127-0-0-1.10-10-10-10.any.domain
```

Here is how it looks in action:

```
$ host 127-0-0-1.10-10-10-10.any.domain
127-0-0-1.10-10-10-10.any.domain has address 127.0.0.1
$ host 127-0-0-1.10-10-10-10.any.domain
127-0-0-1.10-10-10-10.any.domain has address 127.0.0.1
$ host 127-0-0-1.10-10-10-10.any.domain
127-0-0-1.10-10-10-10.any.domain has address 127.0.0.1
$ host 127-0-0-1.10-10-10-10.any.domain
127-0-0-1.10-10-10-10.any.domain has address 10.10.10.10
$ host 127-0-0-1.10-10-10-10.any.domain
127-0-0-1.10-10-10-10.any.domain has address 10.10.10.10
$ host 127-0-0-1.10-10-10-10.any.domain
127-0-0-1.10-10-10-10.any.domain has address 127.0.0.1
$ host 127-0-0-1.10-10-10-10.any.domain
127-0-0-1.10-10-10-10.any.domain has address 127.0.0.1
$ host 127-0-0-1.10-10-10-10.any.domain
127-0-0-1.10-10-10-10.any.domain has address 10.10.10.10
$ host 127-0-0-1.10-10-10-10.any.domain
127-0-0-1.10-10-10-10.any.domain has address 10.10.10.10
```

Constraints
-----------

This implementation aims to be as simple as possible and therefore it supports only standard `IN A` queries - other are simply ignored. Also keep in mind it requires high privileges to bind port 53/udp and lacks proper error handling. With that said, it is highly recommended to not use it for anything important.
