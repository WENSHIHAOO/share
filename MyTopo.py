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
 
        hostlist=[]
        quaggaContainer=self.addHost('H1',ip='192.0.1.1/24')
        hostlist.append(quaggaContainer);
        quaggaContainer=self.addHost('R1',ip='192.0.1.2/24')
        hostlist.append(quaggaContainer);
        quaggaContainer=self.addHost('R2',ip='195.0.1.1/24',)
        hostlist.append(quaggaContainer);
        quaggaContainer=self.addHost('R3',ip='196.0.1.1/24',)
        hostlist.append(quaggaContainer);
        quaggaContainer=self.addHost('R4',ip='197.1.1.2/24',)
        hostlist.append(quaggaContainer);
        quaggaContainer=self.addHost('H2',ip='197.1.1.1/24')
        hostlist.append(quaggaContainer);
       
        # Setup each Quagga router, add a link between it and the IXP fabric
            
        self.addLink(hostlist[0],hostlist[1])
        self.addLink(hostlist[4],hostlist[5])
        self.addLink(hostlist[2],hostlist[4])
        self.addLink(hostlist[3],hostlist[4])
        self.addLink(hostlist[1],hostlist[2])
        self.addLink(hostlist[1],hostlist[3])
    
def run():
    "Test linux router"
    topo = MyTopo()
    net = Mininet(topo)
    net.start()
    
    net.get("r1").cmd("sysctl net.ipv4.ip_forward=1")
    net.get("r2").cmd("sysctl net.ipv4.ip_forward=1")
    net.get("r3").cmd("sysctl net.ipv4.ip_forward=1")
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

    info('** Running CLI\n')
    CLI(net)
    net.stop()
       
if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
