#Static analysis for cantilever beam loaded by a uniform vertical distributed load.
#A user enters beam length, height and E modulus as three parameters. The
#other parametes are fixed.
#Created 03/2018.
#Need to set up path to mupif/examples/Example10-stacTM-local

import sys
sys.path.extend(['../','../../mp.git', '../../mp.git/mupif/examples/Example10-stacTM-local'])
import demoapp
import meshgen
from mupif import *
import mupif.Physics.PhysicalQuantities as PQ
import time
import logging
import mechModels
log = logging.getLogger()



import argparse
#Read int for mode as number behind '-m' argument: 0-local (default), 1-ssh, 2-VPN 
mode = argparse.ArgumentParser(parents=[Util.getParentParser()]).parse_args().mode
from mechanicalServerConfig import serverConfig
cfg = serverConfig(mode)

from eulerBernoulliServerConfig import serverConfig
ebsc = serverConfig(mode)



fileName = 'workFlow1.in'


#Plane stress solution using finite elements
class WorkFlow1_dist(mechModels.WorkFlow1):
    def __init__ (self, targetTime=PQ.PhysicalQuantity('0 s')):
        super(WorkFlow1_dist, self).__init__(targetTime=targetTime)
 #locate nameserver
        ns = PyroUtil.connectNameServer(nshost=cfg.nshost, nsport=cfg.nsport, hkey=cfg.hkey)
        #connect to JobManager running on (remote) server
        self.jobMan = PyroUtil.connectJobManager(ns, cfg.jobManName, cfg.hkey)
        self.solver = None
        #allocate the application instances
        try:
            self.solver = PyroUtil.allocateApplicationWithJobManager( ns, self.jobMan, cfg.jobNatPorts[0], cfg.hkey, PyroUtil.SSHContext(sshClient=cfg.sshClient, options=cfg.options, sshHost=cfg.sshHost) )
            log.info('Job has been created')
        except Exception as e:
            log.exception(e)
        else:
            if ((self.solver is not None)):
                solverSignature=self.solver.getApplicationSignature()
                log.info("Working solver on server " + solverSignature)
                log.info("Uploading input files to servers")
                self.createAppInputFile(self.length,self.height,self.Emodulus)
       
                pf = self.jobMan.getPyroFile(self.solver.getJobID(), fileName, 'wb')
                PyroUtil.uploadPyroFile(fileName, pf, cfg.hkey)
            else:
                log.debug("Connection to server failed, exiting")


    def solveStep(self, istep, stageID=0, runInBackground=False):
        #Input data for app1 are in cantilever1.in
        self.solver.solveStep(istep)
        f = self.solver.getField(FieldID.FID_Displacement, self.solver.getAssemblyTime(istep))
        #log.info("URI of tthe problem's field is " + str(uri) )
        #f = Pyro4.Proxy(uri)
        f.field2VTKData().tofile('workFlow1.vtk')
        self.maxDeflection = -f.evaluate((1,0.,0)).getValue()[1]


class WorkFlow2_dist(mechModels.WorkFlow2):
    def __init__ (self, targetTime=PQ.PhysicalQuantity('0 s')):
        super(WorkFlow2_dist, self).__init__(targetTime=targetTime)
 #locate nameserver
        ns = PyroUtil.connectNameServer(nshost=ebsc.nshost, nsport=ebsc.nsport, hkey=ebsc.hkey)
        #connect to JobManager running on (remote) server
        self.jobMan = PyroUtil.connectJobManager(ns, ebsc.jobManName, ebsc.hkey)
        self.solver = None
        #allocate the application instances
        try:
            self.solver = PyroUtil.allocateApplicationWithJobManager( ns, self.jobMan, ebsc.jobNatPorts[0], ebsc.hkey, PyroUtil.SSHContext(sshClient=ebsc.sshClient, options=ebsc.options, sshHost=ebsc.sshHost) )
            log.info('Job has been created')
        except Exception as e:
            log.exception(e)
        else:
            if ((self.solver is not None)):
                solverSignature=self.solver.getApplicationSignature()
                log.info("Working solver on server " + solverSignature)
                log.info("Uploading input files to servers")
                self.createAppInputFile(self.length,self.height,self.Emodulus)
       
                pf = self.jobMan.getPyroFile(self.solver.getJobID(), fileName, 'wb')
                PyroUtil.uploadPyroFile(fileName, pf, cfg.hkey)

            else:
                log.debug("Connection to server failed, exiting")


    def solveStep(self, istep, stageID=0, runInBackground=False):
        self.solver.solveStep(istep)

        
        
