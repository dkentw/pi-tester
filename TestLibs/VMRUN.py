import pprint
from optparse import OptionParser

from pysphere import VIServer

class VMRUNNer:
    def __init__(self, hostname, username, password):
        self.server = VIServer()         
        self.server.connect(hostname, username, password)

    def get_vm(self, vm_path_name):
        self.vm = self.server.get_vm_by_path(vm_path_name)
        return self.vm
    
    def list_vms(self):
        vmlist = self.server.get_registered_vms()
        for vm in vmlist:
            print vm    
        return vmlist

    def get_vmserver_version(self):
        type = self.server.get_server_type()
        version = self.server.get_api_version()
        print 'Server Type: ' + type
        print 'Server API Version: ' + version 

# ======== for debug ============    
def connect_to_vmserver(): 
    server = VIServer()
    server.connect('10.1.25.55', 'root', 'toolqa#!')
    return server

def list_vms():
    server = connect_to_vmserver()
    vmlist = server.get_registered_vms()
    for vm in vmlist:
        print vm
        
def get_vmserver_version():
    server = connect_to_vmserver()
    print 'Server Type: ' + server.get_server_type()
    print 'Server API Version: ' + server.get_api_version() 

def power_on_sync(vm_path_name):
    server = connect_to_vmserver()
    vm1 = server.get_vm_by_path(vm_path_name)
    vm1.power_on()

def power_off_sync(vm_path_name):
    server = connect_to_vmserver()
    vm1 = server.get_vm_by_path(vm_path_name)
    vm1.power_off()

# ==================================================
def main():
    parser = OptionParser( usage="usage: %prog [options]" )
    parser.add_option('-l', '--list',
                      action='store_true', 
                      default=False, 
                      dest='list_flag',
                      help='List all vms on the server')
    parser.add_option('-v', '--version', 
                      action='store_true', 
                      default=False, 
                      dest="version_flag", 
                      help="Display the information of VM server.")
    parser.add_option("-o", "--power_on", 
                      action='store',
                      type='string', 
                      dest="vm_path_name",
                      help="Power on the specific VM by VM path")
    parser.add_option("-f", "--power_off", 
                      action='store',
                      type='string', 
                      dest="off_vm_path_name",
                      help="Power off the specific VM by VM path")
    parser.add_option("-i", "--host_ip", 
                      action='store',
                      type='string', 
                      dest="host_ip",
                      help="The EXSI server address")

    (options, args) = parser.parse_args()
    
    if options.host_ip and options.list_flag:
        if options.host_ip in ['10.1.127.174']:
            username = 'root'
            passwd = 'virusqa@11'
            vmrunner = VMRUNNer(options.host_ip, username, passwd)
            
            vmlist = vmrunner.list_vms()
            pprint.pprint(vmlist)
    
    elif options.list_flag:    
        vmlist = vmrunner.list_vms()
        print vmlist
        
    elif options.version_flag:
        # get vm server info
        get_vmserver_version()
    elif options.vm_path_name:
        # power on the vm
        power_on_async(options.vm_path_name)
    elif options.off_vm_path_name:
        # power on the vm
        power_off_async(options.off_vm_path_name)
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()