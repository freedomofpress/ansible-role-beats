# logstash-client
Barebones Ansible role for configuring servers to send logs
to an ELK logserver. Requires an ELK logserver.

Requirements
------------
Make sure your Ansible inventory has a hostgroup `logserver`.
The first member of that hostgroup will be considered the logserver.
Its `eth1` ipv4 address will be used to target logs, over the default
logstash port of `5000`. The default value of `eth1` assumes
a private networking interface on a secondary interface.

Role Variables
--------------
You'll need an SSL keypair to encrypt logs in transit to the logserver.
The default filepaths are below. Make sure to use the concatenated
`logstash_forwarder_certificate_fullpath` variable for convenience.

```
ssl_certificate_base_directory: /etc/pki/tls/certs
ssl_certificate_basename: logstash-client
logstash_forwarder_certificate_fullpath: "{{ ssl_certificate_base_directory }}/{{ ssl_certificate_basename }}.crt"
```

Add your ELK logserver to the hostgroup `logserver` and make sure `eth1` is
is available over port `5000`.
```
elk_logserver_ip_address: "{{ hostvars[groups['logserver'][0]]['ansible_eth1']['ipv4']['address'] }}"
```
A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.


example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - name: configure logstash clients
      hosts: logclients
      roles:
        - { role: logstash-client,
          }

Contributions
-------------
The following resources were invaluable in creating this role.

* [geerlingguy.logstash](https://github.com/geerlingguy/ansible-role-logstash)
* [DigitalOcean's ELK guide](https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-logstash-and-kibana-4-on-ubuntu-14-04)

License
-------

MIT
