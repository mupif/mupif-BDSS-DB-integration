#Static analysis for cantilever beam loaded by a uniform vertical distributed load.
#A user enters beam length, height and E modulus as three parameters. The
#other parametes are fixed.
#Created 03/2018.
#Need to set up path to mupif/examples/Example10-stacTM-local

import sys
sys.path.extend(['../','../../mp.git'])
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

#Compulsory parameters for the simulation
thickness=0.01    #Beam (plane) thickness (m)
height=1.0        #Beam height (m)
length=5.0        #Beam length (m)
Emodulus=30.0e+9  #E modulus (Pa)
PoissonRatio=0.25 #Poisson's ratio (-)
distribLoad=2e+2  #Distributed vertical load (N/m)

#Optional parameters for meshing and input filename
numX=20 #Number of finite elements in X direction
numY=8 #Number of finite elements in Y direction

fileName1 = 'workFlow1.in'
fileName2 = 'workFlow2.in'


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
            else:
                log.debug("Connection to server failed, exiting")


    def solveStep(self, istep, stageID=0, runInBackground=False):
        #Input data for app1 are in cantilever1.in
        log.info("Uploading input files to servers")
        self.createAppInputFile(self.length,self.height,self.Emodulus)       
        pf = self.jobMan.getPyroFile(self.solver.getJobID(), fileName1, 'wb')
        PyroUtil.uploadPyroFile(fileName1, pf, cfg.hkey)
        
        print(self.Emodulus)
        self.solver.solveStep(istep)
        f = self.solver.getField(FieldID.FID_Displacement, self.solver.getAssemblyTime(istep))
        #log.info("URI of tthe problem's field is " + str(uri) )
        #f = Pyro4.Proxy(uri)
        f.field2VTKData().tofile('workFlow1.vtk')
        self.maxDeflection = -f.evaluate((self.length,0.,0)).getValue()[1]


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
            else:
                log.debug("Connection to server failed, exiting")

    def createAppInputFile(self,b, h, L, E, f):
        inFile = open(fileName2,'w') 
        inFile.write('%f %f %f\n' %(b,h, L))
        inFile.write('%f\n' %(E))
        inFile.write('%f\n' %(f))


    def solveStep(self, istep, stageID=0, runInBackground=False):
        log.info("Uploading input files to servers")
        self.createAppInputFile(thickness, self.height, self.length, self.Emodulus, distribLoad)      
        pf = self.jobMan.getPyroFile(self.solver.getJobID(), fileName2, 'wb')
        PyroUtil.uploadPyroFile(fileName2, pf, ebsc.hkey)
        self.solver.solveStep(istep)
        self.maxDeflection = self.solver.getField(FieldID.FID_Displacement, istep.getTargetTime())


        
        
