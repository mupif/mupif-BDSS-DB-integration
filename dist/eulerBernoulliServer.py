import os,sys
sys.path.extend(['..','../../commit','../../..'])
from mupif import *
Util.changeRootLogger('BDSS.log')

import argparse
#Read int for mode as number behind '-m' argument: 0-local (default), 1-ssh, 2-VPN 
mode = argparse.ArgumentParser(parents=[Util.getParentParser()]).parse_args().mode
from eulerBernoulliServerConfig import serverConfig
cfg = serverConfig(mode)



#locate nameserver
ns = PyroUtil.connectNameServer(nshost=cfg.nshost, nsport=cfg.nsport, hkey=cfg.hkey)

#Run a daemon for jobMamager on this machine
daemon = PyroUtil.runDaemon(host=cfg.server, port=cfg.serverPort, nathost=cfg.serverNathost, natport=cfg.serverNatport, hkey=cfg.hkey)

#Run job manager on a server
jobMan = SimpleJobManager.SimpleJobManager2(daemon, ns, cfg.applicationClass, cfg.jobManName, cfg.portsForJobs, cfg.jobManWorkDir, os.getcwd(), 'serverConfig', mode, cfg.jobMan2CmdPath, cfg.maxJobs, cfg.socketApps)

PyroUtil.runJobManagerServer(server=cfg.server, port=cfg.serverPort, nathost=cfg.serverNathost, natport=cfg.serverNatport, nshost=cfg.nshost, nsport=cfg.nsport, appName=cfg.jobManName, hkey=cfg.hkey, jobman=jobMan, daemon=daemon)
