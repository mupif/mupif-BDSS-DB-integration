#Static analysis for cantilever beam loaded by a uniform vertical distributed load.
#A user enters beam length, height and E modulus as three parameters. The
#other parametes are fixed.
#Created 03/2018.
#Need to set up path to mupif/examples/Example10-stacTM-local

import sys
sys.path.extend(['../mupif.git', '../mupif.git/mupif/examples/Example10-stacTM-local'])
import demoapp
import meshgen
from mupif import *
import mupif.Physics.PhysicalQuantities as PQ
import time
import logging
log = logging.getLogger()

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
fileName = 'workFlow1.in'


#Plane stress solution using finite elements
class WorkFlow1(Workflow.Workflow):
    def __init__ (self, targetTime=PQ.PhysicalQuantity('0 s')):
        super(WorkFlow1, self).__init__(file='', workdir='', targetTime=targetTime)
        self.length = 3.
        self.height = 4.
        self.Emodulus = 5.
        self.maxDeflection = 0.

    def setProperty(self, property, objectID=0):
        if (property.getPropertyID() == PropertyID.PID_Length):
            self.length = property.getValue(unit='m')
        if (property.getPropertyID() == PropertyID.PID_Height):
            self.height = property.getValue(unit='m')
        if (property.getPropertyID() == PropertyID.PID_EModulus):
            self.Emodulus = property.getValue(unit='Pa')
    
    def getProperty(self, propID, time, objectID=0):
        if (propID == PropertyID.PID_Deflection):
            return Property.ConstantProperty(self.maxDeflection, PropertyID.PID_Deflection, ValueType.Scalar, 'm', time, 0).getValue(time)
    
    def createAppInputFile(self,length,height,Emodulus):
        inFile = open(fileName,'w') 
        inFile.write('%f %f\n' %(length,height))
        inFile.write('%d %d\n' %(numX,numY))
        inFile.write('%f\n' %(thickness))
        inFile.write('%e %f\n' %(Emodulus,PoissonRatio))
        inFile.write('0.0\n')
        inFile.write('1 N\n2 N\n3 C 0. %f\n4 D\n' %(-distribLoad))
        inFile.close() 
    
    def solveStep(self, istep, stageID=0, runInBackground=False):
        #Input data for app1 are in cantilever1.in
        self.createAppInputFile(self.length,self.height,self.Emodulus)
        app1 = demoapp.mechanical(fileName, '.')
        sol = app1.solveStep(istep) 
        f = app1.getField(FieldID.FID_Displacement, istep.getTargetTime())
        f.field2VTKData().tofile('workFlow1.vtk')
        #f.field2Image2D(fieldComponent=1, title='Displacement', fileName='workFlow1.png')
        #right bottom point
        #time.sleep(2)
        self.maxDeflection = -f.evaluate((app1.xl,0.,0)).getValue()[1]

    def getCriticalTimeStep(self):
        # determine critical time step
        return PQ.PhysicalQuantity('1 s')



#Euler-Bernoulli beam with analytical solution
class WorkFlow2(WorkFlow1):
    def solveStep(self, istep, stageID=0, runInBackground=False):
        #Input data for app2 are computed on the fly
        app2 = demoapp.EulerBernoulli(b=thickness, h=self.height, L=self.length, E=self.Emodulus, f=distribLoad)
        sol = app2.solveStep(istep) 
        self.maxDeflection = app2.getField(FieldID.FID_Displacement, istep.getTargetTime())
