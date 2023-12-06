#--
#-- ************************************************************************************************************:
#-- *********************************************** SCAN MBTCP PLC *********************************************:
#-- ************************************************************************************************************:
#-- Author:   JBALLARD (JEB)                                                                                    :
#-- Date:     2023.3.01                                                                                         :
#-- Script:   SCADA-PLC.SCAN.py                                                                                 :
#-- Purpose:  A python script that scans the desired PLC via MBTCP.                                             :
#-- Version:  1.0                                                                                               :
#-- ************************************************************************************************************:
#-- ************************************************************************************************************:
#--
#-- *************************************************:
#-- DEFINE PARAMS, PATHS, IMPORT MODULES & CLASSES   :
#-- *************************************************:
import modbus
import s7
import sys
from optparse import OptionParser
import socket
import struct
#--
def status(msg):
    sys.stderr.write(msg[:-1][:39].ljust(39,' ')+msg[-1:])
#--
def get_ip_list(mask):
    try:
        net_addr,mask = mask.split('/')
        mask = int(mask)
        start, = struct.unpack('!L', socket.inet_aton(net_addr))
        start &= 0xFFFFFFFF << (32-mask)
        end = start | ( 0xFFFFFFFF >> mask )
        return [socket.inet_ntoa(struct.pack('!L', addr)) for addr in range(start+1, end)]
    except (struct.error,socket.error):
        return []
#--
def scan(argv):
    parser = OptionParser(
        usage = "USAGE: %prog [options] [ip range]...",
        description = """Scan IP range for PLC devices. Support MODBUS and S7COMM protocols
        """
    )
    parser.add_option("--hosts-list", dest="hosts_file", help="Scan hosts from FILE", metavar="FILE")
    parser.add_option("--ports", dest="ports", help="Scan ports from PORTS", metavar="PORTS", default="102,502")
    parser.add_option("--timeout", dest="connect_timeout", help="Connection timeout (seconds)", metavar="TIMEOUT", type="float", default=1)
    #--
    modbus.AddOptions(parser)
    s7.AddOptions(parser)
    (options, args) = parser.parse_args(argv)
    scan_hosts = []
    #--
    if options.hosts_file:
        try:
            scan_hosts = [file.strip() for file in open(options.hosts_file, 'r')]
        except IOError:
            print "FAILED TO OPEN FILE: %s" % options.hosts_file
    #--
    for ip in args:
        scan_hosts.extend(get_ip_list(ip) if '/' in ip else
            [ip])
    #--
    scan_ports = [int(port) for port in options.ports.split(',')]
    #--
    if not scan_hosts:
        print "0 TARGETS TO SCAN:\n\n"
        parser.print_help()
        exit()
    #--
    status("SCAN START...\n")
    for host in scan_hosts:
        splitted = host.split(':')
        host = splitted[0]
        if len(splitted)==2:
            ports = [int(splitted[1])]
        else:
            ports = scan_ports
        for port in ports:
            status("%s:%d...\r" % (host, port))
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(options.connect_timeout)
                sock.connect((host,port))
                sock.close()
            except socket.error:
                continue

            if port == 10363:
                res = s7.Scan(host, port, options)
            elif port == 10499:
                res = modbus.Scan(host, port, options)
            else:
                res = modbus.Scan(host, port, options) or s7.Scan(host, port, options)

            if not res:
                print "%s:%d unknown protocol" % (host, port)
    status("SCAN COMPLETE\n")
#--
if __name__=="__main__":
    try:
        scan(sys.argv[1:])
    except KeyboardInterrupt:
        status("SCAN TERMINATED\n")
#--
#-- ************************************************:
#-- END OF PYTHON SCRIPT                            :
#-- ************************************************: