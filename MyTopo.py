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
        
        self.addLink( r1, h1, intfName2='r1-eth0',
                      params2={ 'ip' : '170.16.0.2/16' } ) 
        self.addLink( r1, r2, intfName2='r1-eth1',
                      params2={ 'ip' : '171.16.0.1/16' } )
        self.addLink( r1, r3, intfName2='r1-eth2',
                      params2={ 'ip' : '172.16.0.1/16' } )
        
        self.addLink( r2, r1, intfName2='r2-eth0',
                      params2={ 'ip' : '171.16.0.2/16' } ) 
        self.addLink( r2, r4, intfName2='r2-eth1',
                      params2={ 'ip' : '173.16.0.1/16' } )

        self.addLink( r3, r1, intfName2='r3-eth0',
                      params2={ 'ip' : '172.16.0.2/16' } ) 
        self.addLink( r3, r4, intfName2='r3-eth1',
                      params2={ 'ip' : '174.16.0.1/16' } )
        
        self.addLink( r4, r2, intfName2='r4-eth0',
                      params2={ 'ip' : '173.16.0.2/16' } ) 
        self.addLink( r4, r3, intfName2='r4-eth1',
                      params2={ 'ip' : '174.16.0.2/16' } )
        self.addLink( r4, h2, intfName2='r4-eth2',
                      params2={ 'ip' : '175.16.0.2/16' } )
        
def run():
    "Test linux router"
    topo = MyTopo()
    net = Mininet(topo=topo, waitConnected=True )
    net.start()
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r1' ].cmd( 'route1' ) )
    info( net[ 'r2' ].cmd( 'route2' ) )
    info( net[ 'r3' ].cmd( 'route3' ) )
    info( net[ 'r4' ].cmd( 'route4' ) )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
