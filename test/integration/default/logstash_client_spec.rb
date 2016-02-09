describe package("filebeat") do
  it { should be_installed }
  its("version") { should eq "1.1.0" }
end
