import os,sys
#Import example-wide configuration
sys.path.extend(['..', '../Example10-stacTM-local'])
from Config import config
import demoapp

class serverConfig(config):
    def __init__(self, mode):
        #inherit necessary variables: nshost, nsport, hkey, server, serverNathost  
        super(serverConfig, self).__init__(mode)

        self.applicationClass = demoapp.mechanical
        self.applicationInitialFile = 'workFlow1.in' #dummy file
        self.jobManName='Mupif.JobManager@BDSSDemo'#Name of job manager
        self.jobManWorkDir=os.path.abspath(os.path.join(os.getcwd(), 'MechanicalWorkDir'))
        self.sshHost = '172.30.0.1'
        #147.32.130.14'
        self.serverPort = 44550
        self.serverNatport = None
        self.serverNathost = None
        self.portsForJobs=( 9720, 9800 )
        self.serverUserName = os.getenv('USER')
