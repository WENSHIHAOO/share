from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSController
import atexit
from mininet.util import dumpNodeConnections

net = None
class MyTopo(Topo):

    "Creates a topology of Quagga routers"

    def build(self):
        """Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories."""
        
        # Directory where this file / script is located"
        quaggaHosts = []
        quaggaHosts.append(self.addHost(name='h1', ip='192.0.1.1/24',loIP=None))
        quaggaHosts.append(self.addHost(name='r1', ip='192.0.1.2/24',loIP=None))
        quaggaHosts.append(self.addHost(name='r2', ip='195.0.1.1/24',loIP=None))
        quaggaHosts.append(self.addHost(name='r3', ip='196.0.1.1/24',loIP=None))
        quaggaHosts.append(self.addHost(name='r4', ip='197.1.1.2/24',loIP=None))
        quaggaHosts.append(self.addHost(name='h2', ip='197.1.1.1/24',loIP=None))

        hostlist=[]
        # Setup each Quagga router, add a link between it and the IXP fabric
        for host in quaggaHosts:

            # Create an instance of a host, called a quaggaContainer
            quaggaContainer = self.addHost(name=host.name,
                                           ip=host.ip,
                                           hostname=host.name,
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True)

            # Add a loopback interface with an IP in router's announced range
            self.addNodeLoopbackIntf(node=host.name, ip=host.loIP)
            hostlist.append(quaggaContainer)
            
        self.addLink(hostlist[0],hostlist[1])
        self.addLink(hostlist[4],hostlist[5])
        self.addLink(hostlist[2],hostlist[4])
        self.addLink(hostlist[3],hostlist[4])
        self.addLink(hostlist[1],hostlist[2])
        self.addLink(hostlist[1],hostlist[3])
    
def run():
    "Test linux router"
    topo = MyTopo()
    net = Mininet(topo, controller=OVSController)
    net.start()

    dumpNodeConnections(net.hosts)
    
    net.get("r1").cmd("sysctl net.ipv4.ip_forward=1")
    net.get("r2").cmd("sysctl net.ipv4.ip_forward=1")
    net.get("r3").cmd("sysctl net.ipv4.ip_forward=1")
    net.get("r4").cmd("sysctl net.ipv4.ip_forward=1")
    net.get("r4").cmd("sysctl net.ipv4.ip_forward=1")
    net.get("h1").cmd("sysctl net.ipv4.ip_forward=1") 
    net.get("h2").cmd("sysctl net.ipv4.ip_forward=1")
    
    net.get("r1").cmd("ifconfig r1-eth1 193.0.1.1") 
    net.get("r1").cmd("ifconfig r1-eth2 194.0.1.1")
    net.get("r2").cmd("ifconfig r2-eth1 193.0.1.2") 
    net.get("r3").cmd("ifconfig r3-eth1 194.0.1.2")
    net.get("r4").cmd("ifconfig r4-eth1 195.0.1.2")
    net.get("r4").cmd("ifconfig r4-eth2 196.0.1.2")
    
    net.get("h1").cmd("route add default gw 192.0.1.2")
    net.get("h2").cmd("route add default gw 197.1.1.2")
    net.get("r1").cmd("ip route add 197.1.1.0/24 via 193.0.1.2")
    net.get("r1").cmd("ip route add 195.0.1.0/24 via 193.0.1.2")
    net.get("r2").cmd("ip route add 197.1.1.0/24 via 195.0.1.2")
    net.get("r4").cmd("ip route add 193.0.1.0/24 via 195.0.1.1")
    net.get("r4").cmd("ip route add 192.0.1.0/24 via 195.0.1.1")
    net.get("r2").cmd("ip route add 192.0.1.0/24 via 193.0.1.1")
   
    net.get("r1").cmd("ip route add 196.0.1.0/24 via 194.0.1.2")
    net.get("r3").cmd("ip route add 197.1.1.0/24 via 196.0.1.2")
    net.get("r4").cmd("ip route add 194.0.1.0/24 via 196.0.1.1")
    net.get("r3").cmd("ip route add 192.0.1.0/24 via 194.0.1.1")

    net.get("r3").cmd("ip route add 195.0.1.0/24 via 196.0.1.2")
    net.get("r2").cmd("ip route add 194.0.1.0/24 via 193.0.1.1")
    net.get("r3").cmd("ip route add 193.0.1.0/24 via 194.0.1.1")
    net.get("r2").cmd("ip route add 196.0.1.0/24 via 195.0.1.2")

    info('** Testing network connectivity\n')
    net.ping(net.hosts)

    info('** Dumping host processes\n')

    for host in net.hosts:
        host.cmdPrint("ps aux")

    info('** Running CLI\n')
    CLI(net)
    net.stop()
    
def stopNetwork():
    "stops a network (only called on a forced cleanup)"

    if net is not None:
        info('** Tearing down Quagga network\n')
        net.stop()
        
if __name__ == '__main__':
    atexit.register(stopNetwork)
    setLogLevel( 'info' )
    run()
