from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."
    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()
        
net = None
class MyTopo(Topo):

    def build(self):   
        H1=self.addHost('H1', cls=LinuxRouter, ip='170.1.1.1/16')
        R1=self.addHost('R1', cls=LinuxRouter, ip='170.1.1.2/16')
        R2=self.addHost('R2', cls=LinuxRouter, ip='173.1.1.1/16')
        R3=self.addHost('R3', cls=LinuxRouter, ip='174.1.1.1/16')
        R4=self.addHost('R4', cls=LinuxRouter, ip='175.1.1.2/16')
        H2=self.addHost('H2', cls=LinuxRouter, ip='175.1.1.1/16')
        
        self.addLink(H1,R1)
        self.addLink(R4,H2)
        self.addLink(R2,R4)
        self.addLink(R3,R4)
        self.addLink(R1,R2)
        self.addLink(R1,R3)
    
def run():
    topo = MyTopo()
    net = Mininet(topo)
    net.start()
    
    net.get("R1").cmd("ifconfig R1-eth1 171.1.1.1") 
    net.get("R1").cmd("ifconfig R1-eth2 172.1.1.1")
    net.get("R2").cmd("ifconfig R2-eth1 171.1.1.2") 
    net.get("R3").cmd("ifconfig R3-eth1 172.1.1.2")
    net.get("R4").cmd("ifconfig R4-eth1 173.1.1.2")
    net.get("R4").cmd("ifconfig R4-eth2 174.1.1.2")
    
    net.get("H1").cmd("route add default gw 170.1.1.0")
    net.get("H2").cmd("route add default gw 175.1.1.0")
    
    net.get("R1").cmd("ip route add 175.1.1.0/16 via 171.1.1.2")
    net.get("R1").cmd("ip route add 173.1.1.0/16 via 171.1.1.2")
    net.get("R1").cmd("ip route add 174.1.1.0/16 via 172.1.1.2")
    
    net.get("R2").cmd("ip route add 170.1.1.0/16 via 171.1.1.1")
    net.get("R2").cmd("ip route add 172.1.1.0/16 via 171.1.1.1")
    net.get("R2").cmd("ip route add 174.1.1.0/16 via 173.1.1.2")
    net.get("R2").cmd("ip route add 175.1.1.0/16 via 173.1.1.2")
   
    net.get("R3").cmd("ip route add 170.1.1.0/16 via 172.1.1.1")
    net.get("R3").cmd("ip route add 171.1.1.0/16 via 172.1.1.1")
    net.get("R3").cmd("ip route add 173.1.1.0/16 via 174.1.1.2")
    net.get("R3").cmd("ip route add 175.1.1.0/16 via 174.1.1.2")
    
    net.get("R4").cmd("ip route add 170.1.1.0/16 via 173.1.1.1")
    net.get("R4").cmd("ip route add 171.1.1.0/16 via 173.1.1.1")
    net.get("R4").cmd("ip route add 172.1.1.0/16 via 174.1.1.1")

    info('** Running CLI\n')
    CLI(net)
    net.stop()
      
if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
