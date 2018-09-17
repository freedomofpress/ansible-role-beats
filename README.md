# Beats client Ansible role
[![CircleCI](https://circleci.com/gh/freedomofpress/ansible-role-beats.svg?style=svg&circle-token=b25fb9659801486c2a4da5a3c047bfb019a59699)](https://circleci.com/gh/freedomofpress/ansible-role-beats)

Ansible role for installing and configuring elastic beats clients. Primarily
used for shipping logs and metrics to an ELK stack.
By default, this role will ship to logstash on the same box using [filebeat] and [metricbeat].

Requirements
------------
* someplace to ship data to - as of the beats 5.x series this includes shipping to
  `file`, `kafka`, `redis`, `console`, `elasticsearch`, and/or `logstash`

Role Variables
--------------
You'll need an SSL cert to encrypt logs in transit to the
logstash/elasticsearch. This logic is not provided by this role and encryption
is not enabled by default. You'll need to reference the official beats
documentation output guides to add those options via variables.

Example Playbook
----------------

```
- name: Configure beats clients.
  hosts: clients
  roles:
    - role: freedomofpress.beats
  tags: clients
```

Running the tests
-----------------

This role uses [Molecule] and [Testinfra] for testing. To use it:

```
pip install -r requirements.txt
molecule test
```

You can also run selective commands:

```
molecule idempotence
molecule verify
```

To fire up an elasticsearch UI for debugging, run:

```bash
make elastic-ui
```

See the [Molecule] docs for more info.

Contributions
-------------
The following resources were invaluable in creating this role.

* [geerlingguy.logstash](https://github.com/geerlingguy/ansible-role-logstash)
* [DigitalOcean's ELK guide](https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-logstash-and-kibana-4-on-ubuntu-14-04)
* [filebeat configuration guide](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-configuration-details.html)

License
-------

MIT

[Molecule]: http://molecule.readthedocs.org/en/master/
[Testinfra]: https://testinfra.readthedocs.io/en/latest/
[filebeat]: https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-overview.html
[metricbeat]: https://www.elastic.co/guide/en/beats/metricbeat/current/index.html
