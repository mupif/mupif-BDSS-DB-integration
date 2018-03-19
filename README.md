# mupif-BDSS-DB-integration
Minimum working example on integration of BDSS, database and physical models.
Three parameters are considered as variables, i.e. length, height and E modulus
of a cantilever beam.
Other paramters such as thickness, Poisson's ratio, load are fixed.
Maximum deflection is calculated from both models as KPI.

Two physical models are embedded in two workflows:
WorkFlow1 represents 2D plane-stress elastic solution
WorkFlow2 represents Euler-Bernoulli beam analytical solution
They provide similar results, except very slender and high beams.

You need to set up path (relative or absolute) to
mupif/examples/Example10-stacTM-local for accessing demoapp and meshgen modules
Also, path to MuPIF must exists; either as installed module or to its __init__.py

mechModels.py will execute both models with the same input parameters.
