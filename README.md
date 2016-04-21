# Logstash client Ansible role
Ansible role for shipping logs and metrics to an ELK logserver.
Uses [filebeat] and [topbeat], not the deprecated logstash-forwarder.
Intended for use with the [freedomofpress.elk] role.

Requirements
------------
* an ELK logserver to ship to (see the [freedomofpress.elk] role)

Role Variables
--------------
You'll need an SSL cert to encrypt logs in transit to the logserver.
**If you don't specify an SSL cert, SSL will be disabled.**
The [freedomofpress.elk] role will automatically generated a self-signed
SSL cert and use that when configuring the filebeat and topbeat integrations.

```yaml
# The libbeat packages to install. Options: filebeat, topbeat, packetbeat.
logstash_client_beats_packages:
  - filebeat
  - topbeat

logstash_client_ssl_certificate_base_directory: /etc/pki/tls/certs

# Set to a cert filepath in order to copy to host and enable TLS
# for shipping logs. TLS is disabled by default.
logstash_client_ssl_certificate: ""
logstash_client_ssl_certificate_fullpath: >-
  "{{ logstash_client_ssl_certificate_base_directory }}/{{ logstash_client_ssl_certificate | basename }}"

# Sane default of localhost. Override to set to the IP address of the Logstash server.
# You can also inspect group membership, e.g.:
# logstash_client_logserver_ip_address: "{{ hostvars[groups.logserver.0].ansible_default_ipv4.address }}"
logstash_client_logserver_ip_address: "127.0.0.1"

# Base logfiles that should be tracked on all hosts.
logstash_client_logfiles:
  - paths:
      - /var/log/syslog
      - /var/log/auth.log
    document_type: syslog

  - paths:
      - /var/log/dpkg.log
    document_type: dpkg

  - paths:
      - /var/log/tor/info.log
      - /var/log/tor/notice.log
      - /var/log/tor/log
    document_type: tor

  - paths:
      - /var/log/mysql/mysql.log
      - /var/log/mysql/error.log
    document_type: mysql

  - paths:
      - /var/www/redmine/log/production.log
    document_type: redmine

  - paths:
      - /var/log/apache2/*log
    document_type: apache

  - paths:
      - /var/log/ufw.log
    document_type: ufw

# To send additional logfiles, override the following list.
# Make sure each item has "path" and "type" attributes.
logstash_client_extra_logfiles: []

logstash_client_combined_logfiles: "{{ logstash_client_logfiles + logstash_client_extra_logfiles }}"
```

Example Playbook
----------------

```
- name: Configure Logstash clients.
  hosts: logclients
  roles:
    - role: freedomofpress.logstash-client
  tags: clients
```

Contributions
-------------
The following resources were invaluable in creating this role.

* [geerlingguy.logstash](https://github.com/geerlingguy/ansible-role-logstash)
* [DigitalOcean's ELK guide](https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-logstash-and-kibana-4-on-ubuntu-14-04)
* [topbeat configuration guide](https://www.elastic.co/guide/en/beats/topbeat/current/topbeat-configuration-options.html)
* [filebeat configuration guide](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-configuration-details.html)

License
-------

MIT

[freedomofpress.elk]: https://github.com/freedomofpress/ansible-role-elk
[filebeat]: https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-overview.html
[topbeat]: https://www.elastic.co/guide/en/beats/topbeat/current/_overview.html
