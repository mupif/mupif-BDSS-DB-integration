import os,sys
#Import example-wide configuration
sys.path.extend(['..', '../Example10-stacTM-local'])
from Config import config
import demoapp

class serverConfig(config):
    def __init__(self, mode):
        #inherit necessary variables: nshost, nsport, hkey, server, serverNathost  
        super(serverConfig, self).__init__(mode)

        self.applicationClass = demoapp.EulerBernoulli
        self.applicationInitialFile = 'input.in' #dummy file
        self.jobManName='Mupif.JobManager@BDSSDemoEB'#Name of job manager
        self.jobManWorkDir=os.path.abspath(os.path.join(os.getcwd()))
        self.sshHost = '192.168.0.80'
        #147.32.130.14'
        self.serverPort = 45520
        self.serverNatport = None
        self.serverNathost = None
        self.portsForJobs=( 9810, 9900 )
        self.jobNatPorts = [None] if self.jobNatPorts[0]==None else list(range(7310, 7400))
        self.serverUserName = os.getenv('USER')
