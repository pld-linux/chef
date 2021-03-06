log_level          :info
log_location       STDOUT
ssl_verify_mode    :verify_none
chef_server_url    'http://chef.example.com:4000'

signing_ca_path    '/var/lib/chef/ca'
couchdb_database   'chef'

cookbook_path      [ '/var/lib/chef/cookbooks', '/var/lib/chef/site-cookbooks' ]

file_cache_path    '/var/cache/chef'
node_path          '/var/lib/chef/nodes'
openid_store_path  '/var/lib/chef/openid/store'
openid_cstore_path '/var/lib/chef/openid/cstore'
search_index_path  '/var/lib/chef/search_index'
role_path          '/var/lib/chef/roles'

validation_client_name 'chef-validator'
validation_key         '/etc/chef/validation.pem'
client_key             '/etc/chef/client.pem'
web_ui_client_name     'chef-webui'
web_ui_key             '/etc/chef/webui.pem'

web_ui_admin_user_name 'admin'
web_ui_admin_default_password 'somerandompasswordhere'

supportdir = '/srv/chef/support'
solr_jetty_path File.join(supportdir, 'solr', 'jetty')
solr_data_path  File.join(supportdir, 'solr', 'data')
solr_home_path  File.join(supportdir, 'solr', 'home')
solr_heap_size  '256M'

umask 0022

Mixlib::Log::Formatter.show_time = false
