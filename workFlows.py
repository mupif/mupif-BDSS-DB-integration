#Static analysis for cantilever beam loaded by a uniform vertical distributed load.
#A user enters geometry, meshing details, material properties and distributed load.
#App1 uses 2D plane stress model.
#App2 uses simple Euler-Bernoulli beam model neglecting shear deformation.
#Created 03/2018
#Need to set up path to mupif/examples/Example10-stacTM-local

import sys
sys.path.extend(['../mupif.git'])
from mupif import *
import mupif.Physics.PhysicalQuantities as PQ
import mechModels
import time
import logging
log = logging.getLogger()

#Variable input parameters (coming from BDSS or database)
length = 4.5 #m
height = 0.4 #m
EModulus = 30. #GPa



#FE model as workflow 1
wf1 = mechModels.WorkFlow1(targetTime=PQ.PhysicalQuantity(1.,'s'))

#Set three variable properties
wf1.setProperty(Property.ConstantProperty(length, PropertyID.PID_Length, ValueType.Scalar, 'm'))
wf1.setProperty(Property.ConstantProperty(height, PropertyID.PID_Height, ValueType.Scalar, 'm'))
wf1.setProperty(Property.ConstantProperty(EModulus, PropertyID.PID_EModulus, ValueType.Scalar, 'GPa'))

#Solve equations
wf1.solve()

#Get maximum deflection as KPI
maxDeflection1 = wf1.getProperty(PropertyID.PID_Deflection, wf1.targetTime)
log.info("WorkFlow1 finished with maximum deflection %g m", maxDeflection1 )




#Second physical model Euler-Bernoulli beam as workflow 2
wf2 = mechModels.WorkFlow2(targetTime=PQ.PhysicalQuantity(1.,'s'))

#Set three variable properties
wf2.setProperty(Property.ConstantProperty(length, PropertyID.PID_Length, ValueType.Scalar, 'm'))
wf2.setProperty(Property.ConstantProperty(height, PropertyID.PID_Height, ValueType.Scalar, 'm'))
wf2.setProperty(Property.ConstantProperty(EModulus, PropertyID.PID_EModulus, ValueType.Scalar, 'GPa'))

#Calculate formula
wf2.solve()

#Get maximum deflection as KPI
maxDeflection2 = wf2.getProperty(PropertyID.PID_Deflection, wf1.targetTime)
log.info("WorkFlow2 finished with maximum deflection %g m", maxDeflection2 )
