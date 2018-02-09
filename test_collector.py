import sftp_data_collector

# This is a test collector.

# Host information
#
src_host_name = 'localhost'
dest_host_name = 'localhost'

#
# Source username/password
# password here can be put in the environment variable if required.
#
src_username = 'ahmed'
src_passwd = 'ahmed'

#
# Destination username / password
# password here can be put in the environment variable if required
#
dest_username = 'ahmed'
dest_passwd = 'ahmed'

#
# pattern which is assumed to ne in the filename which we are trying to collect.
#
pattern = '20141013_-_13'

#
# Change directory information - We need to 'cd' in src and dest if required.
# If this information is not given then assumed to be the root directory to collect data (.)
#
current_dir_src = 'src_dir'
current_dir_dest = 'dest_dir'

#
# Call function with parameters.
# Might want to do a check for the pattern here.
# 
sftp_data_collector.get_file_from_src (src_host_name, dest_host_name, src_username, src_passwd,
                      dest_username, dest_passwd, pattern,
                      cd_src_directory_args=current_dir_src, cd_dest_directory_args=current_dir_dest)