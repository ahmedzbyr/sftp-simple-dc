import textwrap
import pysftp
import argparse
import datetime
import logging
import os
import shutil
import re


def get_connection(host_name, username, password):
    # Connection
    try:
        srv = pysftp.Connection(host=host_name, username=username, password=password)
        return srv
    except:
        logging.error("Connection Failed to Host :" + host_name + " Exiting Now!!!")
        exit()


def get_listing_from_server(srv, directory_name):
    # Change directory to a test DIR
    """

    :param srv:
    :param directory_name:
    :return:
    """
    srv.chdir(directory_name)

    # Get the directory and file listing
    data = srv.listdir()

    #
    return data


def pattern_date(date_pattern):
    # Date pattern
    """

    :param date_pattern:
    :return:
    """
    logging.debug("Date Information :" + str(date_pattern))

    # Fetch file from date_hour
    if date_pattern is None:
        fmt = '%Y%m%d_%H'
        current_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        date_split = current_time.strftime(fmt).split('_')
        src_date = date_split[0]
        src_hour = date_split[1]
    else:
        date_split = str(date_pattern).split('_')
        src_date = date_split[0]
        src_hour = date_split[1]

    # Filename : FILE_1215.20141008_2255+0200
    get_file_reg_ex = src_date + '_' + src_hour
    logging.debug("File RegEx to pick from Source Location :" + get_file_reg_ex)

    return get_file_reg_ex


def set_directory(cd_directory):
    # Change location
    """

    :param cd_directory:
    :return:
    """
    if not cd_directory:
        current_dir = '.'
    else:
        current_dir = cd_directory

    return current_dir


def create_temp_directory():
    # Create a Temp Directory
    """


    :return:
    """
    temp_directory_store = "~/files_from_src"
    temp_directory_store = os.path.expanduser(temp_directory_store)
    if not os.path.exists(temp_directory_store):
        os.makedirs(temp_directory_store)

    # Return newly created Directory
    return temp_directory_store


def get_file_from_src(src_host_name_args, dest_host_name_args, src_username_args, src_password_args,
                      dest_username_args, dest_password_args, pattern_in_file,
                      cd_src_directory_args=False, cd_dest_directory_args=False):
    #
    # Init Values
    #
    """

    :param src_host_name_args:
    :param dest_host_name_args:
    :param src_username_args:
    :param src_password_args:
    :param dest_username_args:
    :param dest_password_args:
    :param pattern_in_file:
    :param cd_src_directory_args:
    :param cd_dest_directory_args:
    """
    src_host_name = src_host_name_args
    dest_host_name = dest_host_name_args

    src_username = src_username_args
    src_password = src_password_args

    dest_username = dest_username_args
    dest_password = dest_password_args

    get_file_reg_ex = pattern_in_file
    logging.info("RegEx : " + get_file_reg_ex)

    current_src_dir = set_directory(cd_src_directory_args)
    current_dest_dir = set_directory(cd_dest_directory_args)

    logging.debug("Change Source Directory Information :" + current_src_dir)
    logging.debug("Change Destination Directory Information :" + current_dest_dir)

    #
    # Connections and Listing
    #

    conn_src_descriptor = get_connection(src_host_name, src_username, src_password)
    src_listing = get_listing_from_server(conn_src_descriptor, current_src_dir)
    conn_dest_descriptor = get_connection(dest_host_name, dest_username, dest_password)

    logging.info("Listing : " + str(src_listing))

    # Change directory for Destination
    conn_dest_descriptor.chdir(current_dest_dir)

    # Change to temp dir
    temp_dir = create_temp_directory()
    os.chdir(temp_dir)


    # Read from the list and download
    for file_from_src in src_listing:
        if get_file_reg_ex in file_from_src:
            logging.info("GET'ting file from source : " + file_from_src)
            conn_src_descriptor.get(file_from_src)

            logging.info("Sending file to Destination Location : " + str(conn_dest_descriptor))
            conn_dest_descriptor.put(file_from_src)

            logging.info("File Sent to Destination")

    # removing temp directory
    shutil.rmtree(temp_dir)

    logging.debug("Disconnecting From SRC and DEST servers")
    conn_src_descriptor.close()
    conn_dest_descriptor.close()

    logging.debug("Data Collection Complete")


# --------------------------------------------------------
# Process
# --------------------------------------------------------
if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''

    SFTP Data Collector.
    ----------------------

    This script can be used, if the source device/server is unable to "get" file recursively.
    To use password from environment, set values for :

        PASS_SRC for source.
        PASS_DEST for destination.

    Steps in this script:

        1. "get" listing of the files present.
        2. select files required from the list using a reg_ex or a pattern. (currently this is yyyymmdd_hh)
        3. Download select files.

    ----------------------'''))

    group_env_src = parser.add_mutually_exclusive_group(required=True)
    group_env_dest = parser.add_mutually_exclusive_group(required=True)

    group_pattern = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument('-sh', '--src-host-name', help='Source Host name to get Files from.', required=True)
    parser.add_argument('-su', '--src-username', help='Source Host - Username.', required=True)
    group_env_src.add_argument('-sp', '--src-password', help='Source Host - Password.')
    group_env_src.add_argument('-es', '--src-env-password',
                               help='Source Host - Password. Pick From Environment Variable PASS_SRC',
                               action="store_true")

    parser.add_argument('-dh', '--dest-host-name', help='Destination Host name to send Files to.', required=True)
    parser.add_argument('-du', '--dest-username', help='Destination Host - Username.', required=True)
    group_env_dest.add_argument('-dp', '--dest-password', help='Destination Host - Password.')
    group_env_dest.add_argument('-ed', '--dest-env-password',
                                help='Destination Host - Password. Pick From Environment Variable PASS_DEST',
                                action="store_true")

    parser.add_argument('-c', '--cd-src-directory', metavar="SRC_DIRECTORY",
                        help='Source Directory, If not provided then "."', default=False)

    parser.add_argument('-y', '--cd-dest-directory', metavar="DEST_DIRECTORY",
                        help='Destination Directory, If not provided then "."', default=False)

    group_pattern.add_argument('-t', '--date-hour', metavar="YYYYMMDD_HH", help='Enter date_hour in yyyymmdd_hh format,'
                                                                                ' File has date_hour pattern in the filename',
                               default=None)

    group_pattern.add_argument('-p', '--pattern-in-file', help="Enter pattern in filename which needs "
                                                               "to be collected from sFTP server.", default=None)

    parser.add_argument('-d', '--debug', help='Running Debug mode - More Verbose', action="store_true")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')

    # command_string = "-sh localhost -su ahmed -sp ahmed -dh localhost -du ahmed -dp ahmed -c src_dir -y dest_dir -p 20141013_-_1144".split()
    #    command_string_env = "-sh localhost -su ahmed -es -dh localhost -du ahmed -ed -c src_dir -y dest_dir -t 20141013_-_11 --debug".split()
    #    args = parser.parse_args(command_string)

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.dest_env_password:
        try:
            dest_passwd = os.environ['PASS_DEST']
        except:
            logging.error("Environment PASS_DEST not set\n")
            parser.print_help()
            exit()
    else:
        dest_passwd = args.dest_password

    if args.src_env_password:
        try:
            src_passwd = os.environ['PASS_SRC']
        except:
            logging.error("Environment PASS_SRC not set\n")
            parser.print_help()
            exit()
    else:
        src_passwd = args.src_password

    if args.pattern_in_file is None:
        check_pattern = re.findall('\d\d\d\d[0-1][0-2][0-3]\d_[0-2]\d', args.date_hour)
        if not check_pattern:
            logging.error("'-t' Option requires information to be in YYYYMMDD_HH format. Please check the format.\n")
            parser.print_usage()
            exit()
        else:
            pattern = pattern_date(check_pattern)
    else:
        pattern = args.pattern_in_file

    get_file_from_src(args.src_host_name, args.dest_host_name, args.src_username, src_passwd,
                      args.dest_username, dest_passwd, pattern, cd_src_directory_args=args.cd_src_directory,
                      cd_dest_directory_args=args.cd_dest_directory)