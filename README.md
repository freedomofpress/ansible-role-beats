# logstash-client
Barebones Ansible role for configuring servers to send logs
to an ELK logserver. Requires an ELK logserver.

Requirements
------------
An ELK logserver to ship to.
If your Ansible inventory has a hostgroup `logserver`,
the first member of that group will be considered the logserver.
Its `eth0` ipv4 address will be used to target logs, over the default
logstash port of `5000`.

Role Variables
--------------
You'll need an SSL cert to encrypt logs in transit to the logserver.
If you don't specify an SSL cert, SSL will be disabled.

```
logstash_client_ssl_certificate_base_directory: /etc/pki/tls/certs
logstash_client_ssl_certificate_basename: logstash-client
```

```
logstash_client_logserver_ip_address: "{{ hostvars[groups['logserver'][0]]['ansible_default_ipv4']['address'] }}"
```

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - name: configure logstash clients
      hosts: logclients
      roles:
        - role: logstash-client
          # generate a self-signed SSL cert elsewhere
          logstash_client_ssl_certificate: files/logstash-client.crt

Contributions
-------------
The following resources were invaluable in creating this role.

* [geerlingguy.logstash](https://github.com/geerlingguy/ansible-role-logstash)
* [DigitalOcean's ELK guide](https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-logstash-and-kibana-4-on-ubuntu-14-04)

License
-------

MIT
