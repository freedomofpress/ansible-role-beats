import os
import json
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

metricbeat_modules = ['cpu',
                      'load',
                      'diskio',
                      'filesystem',
                      'fsstat',
                      'memory',
                      'network',
                      'process',
                      'socket']


def query_elasticsearch(search, host):
    curl_cmd = 'curl -s http://esserver:9200/logstash'+search
    elasticsearch_query = host.check_output(curl_cmd)
    print(elasticsearch_query)

    return json.loads(elasticsearch_query)


def test_filebeats(host):
    """
        Ensure filebeats agent output is making it thru E2E
            filebeat -> logstash -> elasticsearch
    """
    # dpkg seems to be consistently populated and pushed through since we are
    # doing a lot of package management tasks during the installation of the
    # beats agents
    search = '/dpkg/_search?q=*\&pretty'
    results = query_elasticsearch(search, host)

    assert results['hits']['total'] != 0


@pytest.mark.parametrize('module', metricbeat_modules)
def test_metricbeats(host, module):
    """
        Ensure metricbeats agent output is making it thru E2E
            metricbeat -> logstash -> elasticsearch
    """
    # dpkg seems to be consistently populated and pushed through since we are
    # doing a lot of package management tasks during the installation of the
    # beats agents
    search = '/metricsets/_search?q=metricset.name:{}\&pretty'
    results = query_elasticsearch(search.format(module), host)

    assert results['hits']['total'] != 0
