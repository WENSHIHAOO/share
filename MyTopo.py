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
    
class MyTopo(Topo):

    "Creates a topology of Quagga routers"

    def build(self):
        """Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories."""

        # Directory where this file / script is located"

        h1 = self.addHost( 'H1', ip='170.16.0.1/16', defaultRoute='via 170.16.0.2/16' )
        r1 = self.addNode( 'R1', cls=LinuxRouter, ip='170.16.0.2/16' )
        r2 = self.addNode( 'R2', cls=LinuxRouter, ip='171.16.0.2/16' )
        r3 = self.addNode( 'R3', cls=LinuxRouter, ip='172.16.0.2/16' )
        r4 = self.addNode( 'R4', cls=LinuxRouter, ip='175.16.0.2/16' )
        h2 = self.addHost( 'H2', ip='175.16.0.1/16', defaultRoute='via 175.16.0.2/16' )
        # List of Quagga host configs
        
        self.addLink( h1, r1, intfName2='H1-R1') 
        self.addLink( r1, r2, intfName2='R1-R2')
        self.addLink( r1, r3, intfName2='R1-R3')
        self.addLink( r2, r4, intfName2='R2-R4')
        self.addLink( r3, r4, intfName2='R3-R4')
        self.addLink( h2, r4, intfName2='H2-R4')
def run():
    "Test linux router"
    topo = MyTopo()
    net = Mininet(topo=topo, waitConnected=True )
    net.start()
    info( '*** Routing Table on Router:\n' )
    info( net[ 'R1' ].cmd( 'route' ) )
    info( net[ 'R2' ].cmd( 'route' ) )
    info( net[ 'R3' ].cmd( 'route' ) )
    info( net[ 'R4' ].cmd( 'route' ) )
    
    net.get('H1').cmd('ifconfig H1-eth0 170.16.0.1/16')
    net.get('R1').cmd('ifconfig R1-eth0 170.16.0.2/16')
    net.get('R1').cmd('ifconfig R1-eth1 171.16.0.1/16')
    net.get('R1').cmd('ifconfig R1-eth2 172.16.0.1/16')
    net.get('R2').cmd('ifconfig R2-eth0 171.16.0.2/16')
    net.get('R2').cmd('ifconfig R2-eth1 173.16.0.1/16')
    net.get('R3').cmd('ifconfig R3-eth0 172.16.0.2/16')
    net.get('R3').cmd('ifconfig R3-eth1 174.16.0.1/16')
    net.get('R4').cmd('ifconfig R4-eth0 173.16.0.2/16')
    net.get('R4').cmd('ifconfig R4-eth1 174.16.0.2/16')
    net.get('R4').cmd('ifconfig R4-eth2 175.16.0.2/16')
    net.get('H2').cmd('ifconfig H2-eth0 175.16.0.1/16')
    
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
