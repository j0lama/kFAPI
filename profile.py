#!/usr/bin/env python

kube_description= \
"""
Testing
"""
kube_instruction= \
"""
To be done
"""

#
# Standard geni-lib/portal libraries
#
import geni.portal as portal
import geni.rspec.pg as PG
import geni.rspec.emulab as elab
import geni.rspec.igext as IG
import geni.urn as URN



#
# PhantomNet extensions.
#
import geni.rspec.emulab.pnext as PN



#
# This geni-lib script is designed to run in the PhantomNet Portal.
#
pc = portal.Context()
rspec = PG.Request()

#
# Profile parameters.
#

pc.defineParameter("computeNodeCount", "Number of slave/compute nodes",
                   portal.ParameterType.INTEGER, 1)

pc.defineParameter("Hardware", "EPC hardware",
                   portal.ParameterType.STRING,"d430",[("d430","d430"),("d710","d710"), ("d820", "d820"), ("pc3000", "pc3000")])


pc.defineParameter("cores", "Number of cores",
                   portal.ParameterType.STRING,"4",[("4","4"),("6","6"), ("8", "8"), ("10", "10"), ("12", "12")],
                   longDescription="Number of cores of each Nervion node.",
                   advanced=True)
pc.defineParameter("ram", "RAM size",
                   portal.ParameterType.STRING,"4",[("4","4"),("8","8"), ("12", "12"), ("16", "16"), ("20", "20"), ("24", "24"), ("32", "32")],
                   longDescription="RAM size (GB)",
                   advanced=True)


params = pc.bindParameters()

#
# Give the library a chance to return nice JSON-formatted exception(s) and/or
# warnings; this might sys.exit().
#
pc.verifyParameters()


tour = IG.Tour()
tour.Description(IG.Tour.TEXT,kube_description)
tour.Instructions(IG.Tour.MARKDOWN,kube_instruction)
rspec.addTour(tour)

# Network
netmask="255.255.255.0"
network = rspec.Link("Backhaul")
network.link_multiplexing = True
network.vlan_tagging = True
network.best_effort = True


# Core
epc = rspec.RawPC("epc")
epc.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
epc.addService(PG.Execute(shell="sh", command="/usr/bin/sudo /local/repository/scripts/core_setup.sh"))
epc.hardware_type = params.Hardware
epc.Site('Core')
iface = epc.addInterface()
iface.addAddress(PG.IPv4Address("192.168.1.1", netmask))
network.addInterface(iface)



# K8s Master
kube_m = rspec.XenVM('master')
kube_m.cores = 4
kube_m.ram = 1024 * 8
#kube_m = rspec.RawPC("master")
#kube_m.hardware_type = params.Hardware
kube_m.routable_control_ip = True
kube_m.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
kube_m.Site('Nervion')
iface = kube_m.addInterface()
iface.addAddress(PG.IPv4Address("192.168.1.2", netmask))
network.addInterface(iface)
kube_m.addService(PG.Execute(shell="bash", command="/local/repository/scripts/master.sh"))

# Nervion Slaves
for i in range(0,params.computeNodeCount):
    kube_s = rspec.XenVM('slave'+str(i))
    kube_s.cores = int(params.cores)
    kube_s.ram = 1024 * int(params.ram)
    #kube_s = rspec.RawPC('slave'+str(i))
    #kube_s.hardware_type = params.Hardware
    kube_s.routable_control_ip = True
    kube_s.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
    kube_s.Site('Nervion')
    iface = kube_s.addInterface()
    iface.addAddress(PG.IPv4Address("192.168.1." + str(i+3), netmask))
    network.addInterface(iface)
    kube_s.addService(PG.Execute(shell="bash", command="/local/repository/scripts/slave.sh"))



#
# Print and go!
#
pc.printRequestRSpec(rspec)
