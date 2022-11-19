"""
Example topology of Quagga routers
"""

from mininet.topo import Topo
class MyTopo(Topo):

    "Creates a topology of Quagga routers"

    def build(self):
        """Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories."""

        # Directory where this file / script is located"


        # List of Quagga host configs
        hosts = []
        hosts.append(self.addHost(name='H1', ip='172.0.1.1/16', loIP='10.0.1.1/24'))
        hosts.append(self.addHost(name='R1', ip='172.0.1.2/16', loIP='10.0.2.1/24'))
        hosts.append(self.addHost(name='R2', ip='173.0.1.2/16', loIP='10.0.3.1/24'))
        hosts.append(self.addHost(name='R3', ip='173.0.1.2/16', loIP=None))
        hosts.append(self.addHost(name='R4', ip='173.0.1.2/16', loIP='10.0.3.1/24'))
        hosts.append(self.addHost(name='H2', ip='173.0.1.1/16', loIP='10.0.3.1/24'))
        #quaggaHosts.append(QuaggaHost(name='R4', ip='177.0.1.1/16',
        #                              loIP='10.0.4.1/24'))
        #quaggaHosts.append(QuaggaHost(name='H2', ip='177.0.1.2/16',
        #                              loIP=None))

        # Add switch for IXP fabric
        # ixpfabric = self.addSwitch('fabric-sw1')
        

            # Add a loopback interface with an IP in router's announced range
            # self.addNodeLoopbackIntf(node=host.name, ip=host.loIP)

            # Configure and setup the Quagga service for this node

        # Attach the quaggaContainer to the IXP Fabric Switch
        self.addLink(hosts[0], hosts[1])
        self.addLink(hosts[5], hosts[4])
        self.addLink(hosts[1], hosts[2])
        self.addLink(hosts[1], hosts[3])
        self.addLink(hosts[2], hosts[4])
        self.addLink(hosts[3], hosts[4])
topos = { 'mytopo': ( lambda: MyTopo() ) }
