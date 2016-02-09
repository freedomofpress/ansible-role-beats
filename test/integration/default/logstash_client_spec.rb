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
