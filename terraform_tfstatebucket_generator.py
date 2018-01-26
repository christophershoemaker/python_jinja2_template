import jinja2
import yaml
import os
import sys, getopt

# Could be dev or prod. Default is set to dev
account = 'dev'

try:
  opts, args = getopt.getopt(sys.argv[1:],"ha:",["account="])
except getopt.GetoptError:
  print 'terraform_tfstatebucket_generator.py -a <account>'
  sys.exit(2)
for opt, arg in opts:
  if opt == '-h':
    print 'terraform_tfstatebucket_generator.py -a <account>'
    sys.exit()
  elif opt in ("-a", "--account"):
    account = arg

print 'Account is "', account

template_file = "backend_s3/statebucket.j2"
mgmt_yml_config_file = "backend_s3/config/mgmt/" + account + ".yml"
proxy_yml_config_file = "backend_s3/config/proxy/" + account + ".yml"

# output directories
mgmt_output_directory = os.getenv("HOME")
proxy_output_directory = os.getenv("HOME")

# read the content from the YML config file
print("Read YML config file...")
mgmt_config = yaml.load(open(mgmt_yml_config_file, 'r'))
proxy_config = yaml.load(open(proxy_yml_config_file, 'r'))

# print both configs
#print "MGMT config:" + mgmt_config
#print "PROXY config:" + proxy_config

print("Create Jinja2 environment...")
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."),
                         trim_blocks=True,
                         lstrip_blocks=True)
template = env.get_template(template_file)

# make sure that the output directory exists
if not os.path.exists(mgmt_output_directory):
    os.mkdir(mgmt_output_directory)

if not os.path.exists(proxy_output_directory):
    os.mkdir(proxy_output_directory)

# create terraform backend s3 MGMT from template
print("Create terraform backend s3 MGMT...")
result = template.render(mgmt_config)
f = open(os.path.join(mgmt_output_directory, "statebucket_mgmt.tf"), "w")
f.write(result)
f.close()
print("Terraform backend for state '%s' created..." % ("statebucket_mgmt.tf"))

# create terraform backend s3 PROXY from template
print("Create terraform backend s3 PROXY...")
result = template.render(proxy_config)
f = open(os.path.join(proxy_output_directory, "statebucket_proxy.tf"), "w")
f.write(result)
f.close()
print("Terraform backend for state '%s' created..." % ("statebucket_proxy.tf"))
