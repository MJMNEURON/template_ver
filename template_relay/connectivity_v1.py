########################################################################
###### this script:
###### 1. specifies connectivity between LGN-PGN cells
###### USE $ nrngui -python filename.py TO RUN
########################################################################
###### import things
from neuron import h
import random
from random import randint
from random import shuffle
import matplotlib.pylab as plt
# h.load_file("RE_preserved.tem")
# cell=h.TCcell()
# print "soma_tc.v =", cell.soma_tc(0.5).v
########################################################################
file = open("relay.hoc").read()
file = file.replace('ncells=5', 'ncells=3')
f = open("relay.hoc", 'w')
f.write(file)
f.close()
########################################################################
h.load_file("relay.hoc")
########################################################################
###### making a dictionary contains secname() for proximal_tc/distal_tc...
record = {
	'soma_tc0': ['[0].soma_tc'],
	'dend_tc_receiver': ['TCcell[1].dend_tc3[16]', 'TCcell[2].dend_tc3[16]']
#	'dend_tcceiver2': ['TCcell[2].dend_tc4', 'TCcell[2]']
}
relay = {
	'soma_tc':['[0].soma_tc'], 
#	'proximal_tc':['TCcell[0].dend_tc1[2]', 'TCcell[0].dend_tc2[2]', '[0].soma_tc'], 
	'proximal_tc':['[0].soma_tc'], 
	'distal_tc':['[1].dend_tc4[2]', '[2].dend_tc4[2]']
}
#print 'proximal_tc =', relay['proximal_tc']
########################################################################
###### create a list contains proximal_tc dendrites of relay cell
proximal_tc = []
proximalname_tc =[]
for prox_tc in h.allsec(): # print prox_tc.name() # gives out TCcell[0].soma_tc......
	if any(s in prox_tc.name() for s in relay['proximal_tc']):
		proximal_tc.append(prox_tc)
		proximalname_tc.append(prox_tc.name())
print "PROXI_NAME", proximalname_tc
selprox_tc = random.sample(proximal_tc,  1)
selproxname_tc = random.sample(proximalname_tc,  1)

#print 's.sec: ', proximal_tc, '\n'
print 's.name: ', proximalname_tc, '\n'
print 'proximal_tc dendrites:', selprox_tc, '\n', selproxname_tc
print '------------------------------------------------------'
###### create a list contains distal_tc dendrites of relay cell
distal_tc = []
distalname_tc=[]
for dist_tc in h.allsec():
	if any(s in dist_tc.name() for s in relay['distal_tc']):
		distal_tc.append(dist_tc)
		distalname_tc.append(dist_tc.name())

seldist_tc = random.sample(distal_tc, 2)  # Choose n elements
seldistname_tc = random.sample(distalname_tc,  2)
#print 'r.sec: ',distal_tc
print 'r.name: ',distalname_tc, '\n'
print 'distal_tc dendrites: ', seldist_tc, '\n', seldistname_tc
print '------------------------------------------------------'
#print seldistname_tc[1]
########################################################################
###### randomly selecting n secs from the list of secs
send = []
receive = []
syn = []
nc = []
vec = {}
for counter in range (0, 3): # (0, how many secs to take)
	nprox = randint(0, len(selprox_tc)-1)	
	send.append(selprox_tc[nprox])
	ndist = randint(0, len(seldist_tc)-1)
	receive.append(seldist_tc[ndist])
	syni = h.AMPA(0.5, sec = receive[counter])
	syn.append(syni)
	nci=h.NetCon(send[counter](0.5)._ref_v, syni, sec=send[counter])
	nci.weight[0] = 0.2
	nc.append(nci)

	#print selprox_tc[nprox]
	print "sender[counter] = ", send[counter].name()
	print "receiver[counter] = ", receive[counter].name()

	#selprox_tc.remove(selprox_tc[nprox])
	#seldist_tc.remove(seldist_tc[ndist])

#	h.run()
########################################################################
'''
soma=[]
for recs in h.allsec():
	if any(s in recs.name() for s in record['soma_tc0']):
		soma.append(recs)
#print soma[0].name()

dend=[]
seldend=[]
for recd in h.allsec():
#	dend.append(recd)
#	shuffle(dend)
	if any(s in recd.name() for s in record['dend_tc_tcceiver']):
		seldend.append(recd)
		shuffle(seldend)
#print dend[0].name()

for var in 'v_sender', 'v_tcceiver', 'i_syn', 't':
	vec[var] = h.Vector()


vec['v_sender'].record(soma[0](0.5)._tcf_v)
vec['v_tcceiver'].record(seldend[0](0.5)._tcf_v)
vec['i_syn'].record(syn[0]._tcf_i)
vec['t'].record(h._tcf_t)

h.load_file("stdrun.hoc")
h.init()
h.tstop = 2400
h.run()


plt.xlabel('t (ms)')
plt.ylabel('v (mV)')                       
plt.subplot(2,2,1)
plt.plot(vec['t'], vec['v_sender'], label=soma[0].name() )
plt.plot(vec['t'], vec['v_tcceiver'], 'r', label = seldend[0].name())
plt.legend(loc='upper left')
plt.subplot(2,2,3)
plt.plot(vec['t'], vec['i_syn'])
plt.ylim(-5, 2.0)	

vec['v_sender'].record(soma[0](0.5)._tcf_v)
vec['v_tcceiver'].record(seldend[1](0.5)._tcf_v)
vec['i_syn'].record(syn[0]._tcf_i)
vec['t'].record(h._tcf_t)

h.load_file("stdrun.hoc")
h.init()
h.tstop = 2400
h.run()

plt.xlabel('t (ms)')
plt.ylabel('v (mV)')                       
plt.subplot(2,2,2)
plt.plot(vec['t'], vec['v_sender'], label=soma[0].name() )
plt.plot(vec['t'], vec['v_tcceiver'], 'r', label = seldend[1].name())
plt.legend(loc='upper left')
plt.subplot(2,2,4)
plt.plot(vec['t'], vec['i_syn'])
plt.ylim(-5, 2.0)	
plt.show()
'''