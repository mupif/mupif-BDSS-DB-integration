#Common configuration for running examples in local, ssh or VPN mode
import sys, os, os.path
import Pyro4
import logging
log = logging.getLogger()

class config(object):
    """
    Auxiliary class holding configuration variables for local, ssh, or VPN connection.
    Used mainly in mupif/examples/*
    Numerical value of parameter -m sets up internal variables.
    Typically, -m0 is local configuration, -m1 is ssh configuration, -m2 is VPN configuration, -m3 is VPN emulated as local
    """
    
    def __init__(self,mode):
        self.mode = mode
        if mode not in [0,2]:
           log.error("Unknown mode -m %d" % mode)
       
        Pyro4.config.SERIALIZER="pickle"
        Pyro4.config.PICKLE_PROTOCOL_VERSION=2 #to work with python 2.x and 3.x
        Pyro4.config.SERIALIZERS_ACCEPTED={'pickle'}
        Pyro4.config.SERVERTYPE="multiplex"

        #Absolute path to mupif directory - used in JobMan2cmd
#        mupif_dir = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
 #       sys.path.append(mupif_dir)
  #      mupif_dir = os.path.abspath(os.path.join(os.getcwd(), "../.."))
   #     sys.path.append(mupif_dir)
        
        #commmon attributes
        #Password for accessing nameServer and applications
        self.hkey = 'mupif-secret-key'
        #Name of job manager
        self.jobManName='Mupif.JobManager@Example'
        #Name of first application
        self.appName = 'MuPIFServer'

        #Jobs in JobManager
        #Range of ports to be assigned on the server to jobs
        self.portsForJobs=( 9000, 9100 )
        #NAT client ports used to establish ssh connections
        self.jobNatPorts = list(range(6000, 6100))

        #Maximum number of jobs
        self.maxJobs=20
        #Auxiliary port used to communicate with application daemons on a local computer
        self.socketApps=10000
        #Main directory for transmitting files
        self.jobManWorkDir='.'
        #Path to JobMan2cmd.py 
        self.jobMan2CmdPath = "../../mupif.git/mupif/tools/JobMan2cmd.py"
        
        if self.mode == 0:#localhost. Jobmanager uses NAT with ssh tunnels
            #NAME SERVER
            #IP/name of a name server
            self.nshost = '127.0.0.1'
            #self.nshost = '147.32.130.71'
            #Port of name server
            self.nsport = 9090

            #SERVER for a single job or for JobManager
            #IP/name of a server's daemon
            self.server = '127.0.0.1'
            #self.server = '147.32.130.71'
            #Port of server's daemon
            self.serverPort = 44382
            #Nat IP/name (necessary for ssh tunnel)
            self.serverNathost = None
            #Nat port (necessary for ssh tunnel)
            self.serverNatport = None

            #SECOND SERVER for another application on remote computer
            self.server2 = self.server
            self.serverPort2 = 44385
            self.serverNathost2 = self.server
            self.serverNatport2 = 5558
            self.appName2 = 'MuPIFServer2'

            self.server3 = '127.0.0.1'
            self.serverPort3 = 44386
        else:
            #NAME SERVER
            #IP/name of a name server
            self.nshost = '172.30.0.1'
            #self.nshost = '172.30.0.6'
            #Port of name server
            self.nsport = 9090
            
            #SERVER for a single job or for JobManager
            #IP/name of a server's daemon
            #self.server = '172.30.0.6'
            self.server = '192.168.0.80'
            #Port of server's daemon
            self.serverPort = 44382
            #Nat IP/name
            self.serverNathost = None
            #Nat port
            self.serverNatport = None
            self.jobNatPorts = [None]
            
            #SECOND SERVER for another application (usually runs locally)
            self.server2 = '127.0.0.1'
            self.serverPort2 = 44383
            self.serverNathost2 = None
            self.serverNatport2 = None
            #self.appName2 = 'MuPIFServer2'
            
            #third SERVER - an application running on local computer in VPN
            #this server can be accessed only from script from the same computer
            #otherwise the server address has to be replaced by vpn local adress
            self.server3 = '127.0.0.1'
            self.serverPort3 = 44386
    

        self.sshHost = ''
        self.sshClient='manual'
        self.options = ''
