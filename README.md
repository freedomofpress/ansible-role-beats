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
documentation output guides to add those options via variable.

```yaml
---

#### PACKAGING #################################################################

# The libbeat packages to install.
# Options: www.elastic.co/guide/en/beats/libbeat/master/installing-beats.html
beats_client_beats_packages:
  - filebeat
  - metricbeat

beats_client_version: 5.5.0
# The apt repo URL pegs minor versions (e.g. 5.x) to avoid unexpected upgrades
beats_client_major_version_abbreviated: 5.x

beats_client_beats_prereq:
  - apt-transport-https

# Elastic's PGP key for signing their repository
beats_client_elastic_pgp_key: "46095ACC8548582C1A2699A9D27D666CD88E42B4"
beats_client_keyserver: pgp.mit.edu

# Elastic's beats debian repository
beats_client_elastic_repo_url: "deb https://artifacts.elastic.co/packages/{{ beats_client_major_version_abbreviated }}/apt stable main"

#### FILEBEAT ##################################################################


# Sane default of localhost. Override to set to the IP address/DNS of the Logstash server.
beats_client_logserver: "127.0.0.1"
beats_client_port: 5000

# Controls how often Topbeat reports stats (in seconds)
beats_client_topbeat_period: 10

beats_client_logfiles:
  - paths:
      - /var/log/syslog
      - /var/log/auth.log
    tags: ['syslog']

  - paths:
      - /var/log/dpkg.log
    tags: ['dpkg']

  - paths:
      - /var/log/apache2/*log
    tags: ['apache']

  - paths:
      - /var/log/mail.info
      - /var/log/mail.warn
      - /var/log/mail.err
    tags: ['postfix']

# To send additional logfiles, override the following list.
# See
# https://www.elastic.co/guide/en/beats/filebeat/current/configuration-filebeat-options.html#_literal_tags_literal
beats_client_extra_logfiles: []

beats_client_filebeat_combined_logfiles: "{{ beats_client_logfiles + beats_client_extra_logfiles }}"

beats_client_filebeat_logging:
  level: warning
  to_files: true
  to_syslog: false
  files:
    path: /var/log/
    name: filebeat.log
    keepfiles: 2

beats_client_filebeat_config:
  filebeat.prospectors: "{{ beats_client_filebeat_combined_logfiles }}"
  output: "{{ beats_client_output }}"
  logging: "{{ beats_client_filebeat_logging }}"
  setup: "{{ beats_client_filebeat_setup }}"

#### METRICBEAT ##################################################################
# See: www.elastic.co/guide/en/beats/metricbeat/master/metricbeat-configuration-options.html

# See: www.elastic.co/guide/en/beats/metricbeat/master/metricbeat-modules.html
beats_client_metricbeat_modules:
  - module: system
    metricsets:
      - cpu
      - load
      - diskio
      - filesystem
      - fsstat
      - memory
      - network
      - process
      - socket
    enabled: true
    period: "{{ beats_client_topbeat_period }}s"
    processes: ['.*']

beats_client_metricbeat_logging:
  level: warning
  to_files: true
  to_syslog: false
  files:
    path: /var/log/
    name: metricbeat.log
    keepfiles: 2

beats_client_metricbeat_config:
  metricbeat.modules: "{{ beats_client_metricbeat_modules }}"
  output: "{{ beats_client_output }}"
  logging: "{{ beats_client_metricbeat_logging }}"
  setup: "{{ beats_client_metricbeat_setup }}"

#### PACKETBEAT ##################################################################
# See: www.elastic.co/guide/en/beats/packetbeat/master/configuring-packetbeat.html
beats_client_packetbeat_config: {}

#### HEARTBEAT ##################################################################
beats_client_heartbeat_config: {}

#### KIBANA ##################################################################

# Default dashboard export only works in this role with the 5.x series
# for 6.x you can now export through the respective config files directly
beats_client_kibana_export: no

beats_client_kibana_url_base: http://localhost:9200
beats_client_kibana_url: "{{ beats_client_kibana_url_base }}/.kibana"
beats_client_kibana_indices:
  metricbeat: metrics-logstash-*
  filebeat: syslog-*
beats_client_kibana_dash_search:
  metricbeat: Metricbeat*
  filebeat: Filebeat*
# Only applicable to beats <5.x you can now setup the dashboards
# via configuration setup.dashboards per client.
beats_client_kibana_export_parameters: "-only-dashboards -es {{beats_client_kibana_url_base}}"

#### SHARED ##################################################################

# Note that SSL is disabled here by default, you'll need to override this
# variable using attributes from
# www.elastic.co/guide/en/beats/metricbeat/master/logstash-output.html
beats_client_output:
  logstash:
    enabled: true
    hosts:
      - "{{ beats_client_logserver }}:{{ beats_client_port }}"

# Added in 6.x series for among other things,
# dashboard setup
# https://www.elastic.co/guide/en/beats/filebeat/current/configuration-dashboards.html
beats_client_filebeat_setup: {}
beats_client_metricbeat_setup: {}

# Master config dictionary variable.
beats_clients_configs:
  filebeat: "{{ beats_client_filebeat_config }}"
  metricbeat: "{{ beats_client_metricbeat_config }}"
  packetbeat: "{{ beats_client_packetbeat_config }}"
  heartbeat: "{{ beats_client_heartbeat_config }}"
```

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
