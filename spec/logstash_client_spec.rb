describe package('filebeat') do
  it { should be_installed }
  its('version') { should eq '1.1.0' }
end

describe package('topbeat') do
  it { should be_installed }
  its('version') { should eq '1.1.0' }
end

describe apt('http://packages.elasticsearch.org/logstashforwarder/debian') do
  it { should_not exist }
  it { should_not be_enabled }
end
describe package('logstash-forwarder') do
  it { should_not be_installed }
end

describe apt('http://packages.elastic.co/beats/apt') do
  it { should exist }
  it { should be_enabled }
end


describe command('apt-key adv --fingerprint --list-keys --keyring /etc/apt/trusted.gpg 46095ACC8548582C1A2699A9D27D666CD88E42B4') do
  its('exit_status') { should eq 0 }
  elasticsearch_gpg_fingerprint = <<FINGERPRINT
pub   2048R/D88E42B4 2013-09-16
      Key fingerprint = 4609 5ACC 8548 582C 1A26  99A9 D27D 666C D88E 42B4
uid                  Elasticsearch (Elasticsearch Signing Key) <dev_ops@elasticsearch.org>
sub   2048R/60D31954 2013-09-16
FINGERPRINT
  its('stdout') { should include elasticsearch_gpg_fingerprint }
end


describe file('/etc/topbeat/topbeat.yml') do
  it { should be_owned_by('root') }
  it { should be_grouped_into('root') }
  its('mode') { should eq 0644 }
end

describe command('topbeat -configtest -c /etc/topbeat/topbeat.yml') do
  its('exit_status') { should eq 0 }
end

describe command('filebeat -configtest -c /etc/filebeat/filebeat.yml') do
  its('exit_status') { should eq 0 }
end

describe service('filebeat') do
  it { should be_running }
end

describe service('topbeat') do
  it { should be_running }
end
