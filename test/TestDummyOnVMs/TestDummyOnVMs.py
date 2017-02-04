import subprocess
import logging
import traceback
logger = logging.getLogger(__name__)
import time

import TestLibs.VMRUN as vmrun

vmrunner = vmrun.VMRUNNer('10.1.25.55', 'root', 'toolqa#!')

GUEST_NAME = 'Administrator'
GUEST_PASSWORD = '1111' 

class TestDummyOnVMs_000001:
    '''
    Setup Clone_SANDBOX_22
    '''    
    def __init__(self):
        self.vm_path = [
                        "[datastore1] Clone_SANDBOX_22/Clone_SANDBOX_22.vmx",
                        "[datastore1] Clone_SANDBOX_23/Clone_SANDBOX_23.vmx",]
        self.send_file_cmd_list = [
                                     (r'D:\inter_gitsource\pi-tester\Tools\7za.exe', r'C:\7za.exe'),
                                     (r'D:\inter_gitsource\pi-tester\Tools\setupssh.exe', r'C:\setupssh.exe'),
                                     (r'D:\inter_gitsource\pi-tester\Tools\pi-tester.zip', r'C:\pi-tester.zip')
                                   ]
        pass
    def run(self):
        # send file
        for vm_guest in self.vm_path:
            try:
                vm = vmrunner.connect_to_vm(vm_guest)
                vm.login_in_guest(GUEST_NAME, GUEST_PASSWORD)
            except:
                logger.error(traceback.format_exc())
                logger.error('VM Guest: ' + vm_guest)
                
            for cmd in self.send_file_cmd_list:
                try:
                    vm.send_file(cmd[0], cmd[1])
                except:
                    logger.error(traceback.format_exc())
                    
                time.sleep(3)
            
            if 0:
                try:
                    vm.start_process('C:\\7za.exe', args=['x', 'pi-tester.zip', '-oC:\\pi-tester', '-y'], cwd="C:\\")
                    pass
                except:
                    logger.error(traceback.format_exc())

        return True, 'test send file'
    
class TestDummyOnVMs_000002:
    '''
    Execute the Dummy test suites
    '''    
    def __init__(self):
        self.vm_path = '[datastore1] Clone_SANDBOX_22/Clone_SANDBOX_22.vmx'
    def run(self):
        vm = vmrunner.connect_to_vm(self.vm_path)
        vm.login_in_guest('Administrator','1111')
        time.sleep(3)
        pid = vm.start_process('notepad.exe' , args=[], cwd="C:\\")
        pid = vm.start_process('C:\\python27\\python.exe' , args=['C:\\pi-tester\\pi_tester.py', '-c', 'Dummy'], cwd="C:\\pi-tester\\")
        return True, str(pid)
    