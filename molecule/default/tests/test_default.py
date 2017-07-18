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

beat_dash_type = ['Filebeat*', 'Metricbeat*']


def query_elasticsearch(search, host, index_name="logstash"):
    curl_cmd = 'curl -s http://esserver:9200/{}/{}\&pretty'.format(
                                                            index_name, search)
    elasticsearch_query = host.check_output(curl_cmd)

    return json.loads(elasticsearch_query)


def test_filebeats(host):
    """
        Ensure filebeats agent output is making it thru E2E
            filebeat -> logstash -> elasticsearch
    """
    # dpkg seems to be consistently populated and pushed through since we are
    # doing a lot of package management tasks during the installation of the
    # beats agents
    search = 'dpkg/_search?q=*'
    results = query_elasticsearch(search, host)

    assert results['hits']['total'] != 0


@pytest.mark.parametrize('module', metricbeat_modules)
def test_metricbeats(host, module):
    """
        Ensure metricbeats agent output is making it thru E2E
            metricbeat -> logstash -> elasticsearch
    """
    search = 'metricsets/_search?q=metricset.name:{}'
    results = query_elasticsearch(search.format(module), host)

    assert results['hits']['total'] != 0


@pytest.mark.parametrize('beat_dashboard_type', beat_dash_type)
def test_kibana_dashboard_inject(host, beat_dashboard_type):
    """
        Ensure beats dashboard injection is making it into elasticsearch
    """
    search = '_search?q=title:{}'.format(beat_dashboard_type)
    results = query_elasticsearch(search, host, index_name=".kibana")

    assert results['hits']['total'] != 0
