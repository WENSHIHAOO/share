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

        h1 = self.addHost( 'H1', ip='170.16.0.1/16', defaultRoute='via 170.16.0.2' )
        r1 = self.addHost( 'R1', cls=LinuxRouter, ip='170.16.0.2/16' )
        r2 = self.addHost( 'R2', cls=LinuxRouter, ip='171.16.0.2/16' )
        r3 = self.addHost( 'R3', cls=LinuxRouter, ip='172.16.0.2/16' )
        r4 = self.addHost( 'R4', cls=LinuxRouter, ip='173.16.0.2/16' )
        h2 = self.addHost( 'H2', ip='173.16.0.1/16', defaultRoute='via 173.16.0.2' )
        # List of Quagga host configs
        
        self.addLink(h1, r1, intfName1='H1-eth0', intfName2='R1-eth0',
                     params1={'ip': '170.16.0.1/16'},params2={'ip': '170.16.0.2/16'}) 
        self.addLink( r1, r2, intfName1='R1-eth1', intfName2='R2-eth0',
                     params1={'ip': '171.16.0.1/16'},params2={'ip': '171.16.0.2/16'})
        self.addLink( r1, r3, intfName1='R1-eth2', intfName2='R3-eth0',
                     params1={'ip': '172.16.0.1/16'},params2={'ip': '172.16.0.2/16'})
        self.addLink( h2, r4, intfName1='H2-eth0', intfName2='R4-eth0',
                     params1={'ip': '173.16.0.1/16'},params2={'ip': '173.16.0.2/16'})
        self.addLink( r4, r2, intfName1='R4-eth1', intfName2='R2-eth1',
                     params1={'ip': '174.16.0.1/16'},params2={'ip': '174.16.0.2/16'})
        self.addLink( r4, r3, intfName1='R4-eth2', intfName2='R3-eth1',
                     params1={'ip': '175.16.0.1/16'},params2={'ip': '175.16.0.2/16'})
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

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
