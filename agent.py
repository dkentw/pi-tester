"""[Agent Mode]

Usage:
  agent.py

Options:
  -h --help        Show help messages.
  --version        Show version.
  -s --server      Setup server IP.
  -p --port        Port number
"""
__VERSION__ = '1.0.1'
from optparse import OptionParser
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import socket
import subprocess
from subprocess import PIPE


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

#----Supported functions
def exec_command_async(commands, shell_flag, cwd=None):
    try:
        p = subprocess.Popen(commands, shell=shell_flag, stdout=PIPE, stderr=PIPE, cwd=cwd)
        result = True
    except OSError as e:
        result = e
    except ValueError as e:
        result = e
    return result

def exec_command_sync(commands, shell_flag, cwd=None):
    try:
        p = subprocess.Popen(commands, shell=shell_flag, stdout=PIPE, stderr=PIPE, cwd=cwd)
        (output, error_msg) = p.communicate()
    except OSError as e:
        output = e
    except ValueError as e:
        output = e
    return output

def receive_file(data, filename, path):
    file_path = path + '/' + filename
    try:
        with open(file_path, 'wb') as fh:
            fh.write(data.data)
        return True
    except:
        return False
    
def ping():
    return 'pong'
    
#-----------------------------------------------------------

def create_server(server_ip, port):
    server_ip = socket.gethostbyname(socket.gethostname())
    server = SimpleXMLRPCServer((server_ip, int(port)), requestHandler=RequestHandler)
    server.register_introspection_functions()
    print "[INFO] The server IP is: " + server_ip

    # register function
    server.register_function(exec_command_async, 'exec_command_async')
    server.register_function(exec_command_sync, 'exec_command_sync')
    server.register_function(receive_file, 'receive_file')
    server.register_function(ping, 'ping')

    
    server.serve_forever()
    
def main():
    usage = "usage: %prog [options] arg1"
    parser = OptionParser(usage="usage: %prog [options][arg]")
    parser.add_option('-s', '--server',
                      action='store', 
                      type='string', 
                      dest='server_ip',
                      default='localhost',
                      help='Setup the server ip.')

    parser.add_option('-p', '--port',
                      action='store', 
                      type='string', 
                      dest='port',
                      default='8000',
                      help='Setup the port of server. Default is 8000.')
    (options, args) = parser.parse_args()
    
    create_server(options.server_ip, options.port)

if __name__ == '__main__':
    print "[INFO] Agent version is %s" % __VERSION__
    print "[INFO] Start the Agent Mode...(Ctrl-C for exit)"
    try:
        main()
    except:
        print 'Bye!Bye!'