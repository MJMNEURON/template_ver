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
# cell=h.REcell()
# print "soma_re.v =", cell.soma_re(0.5).v
########################################################################
file = open("reticular.hoc").read()
file = file.replace('ncells=2', 'ncells=3')
f = open("reticular.hoc", 'w')
f.write(file)
f.close()
########################################################################
h.load_file("reticular.hoc")
########################################################################
###### making a dictionary contains secname() for proximal_re/distal_re...
record = {
	'soma_re0': ['[0].soma_re'],
	'dend_re_receiver': ['REcell[1].dend_re3[16]', 'REcell[2].dend_re3[16]']
#	'dend_receiver2': ['REcell[2].dend_re4', 'REcell[2]']
}
reticular = {
	'soma_re':['[0].soma_re'], 
#	'proximal_re':['REcell[0].dend_re1[2]', 'REcell[0].dend_re2[2]', '[0].soma_re'], 
	'proximal_re':['[0].soma_re'], 
	'distal_re':['[1].dend_re4[2]', '[2].dend_re4[2]']
}
#print 'proximal_re =', reticular['proximal_re']
########################################################################
###### create a list contains proximal_re dendrites of reticular cell
proximal_re = []
proximalname_re =[]
for prox_re in h.allsec(): # print prox_re.name() # gives out REcell[0].soma_re......
	if any(s in prox_re.name() for s in reticular['proximal_re']):
		proximal_re.append(prox_re)
		proximalname_re.append(prox_re.name())
print "PROXI_NAME", proximalname_re
selprox_re = random.sample(proximal_re,  1)
selproxname_re = random.sample(proximalname_re,  1)

#print 's.sec: ', proximal_re, '\n'
print 's.name: ', proximalname_re, '\n'
print 'proximal_re dendrites:', selprox_re, '\n', selproxname_re
print '------------------------------------------------------'
###### create a list contains distal_re dendrites of reticular cell
distal_re = []
distalname_re=[]
for dist_re in h.allsec():
	if any(s in dist_re.name() for s in reticular['distal_re']):
		distal_re.append(dist_re)
		distalname_re.append(dist_re.name())

seldist_re = random.sample(distal_re, 2)  # Choose n elements
seldistname_re = random.sample(distalname_re,  2)
#print 'r.sec: ',distal_re
print 'r.name: ',distalname_re, '\n'
print 'distal_re dendrites: ', seldist_re, '\n', seldistname_re
print '------------------------------------------------------'
#print seldistname_re[1]
########################################################################
###### randomly selecting n secs from the list of secs
send = []
receive = []
syn = []
nc = []
vec = {}
for counter in range (0, 3): # (0, how many secs to take)
	nprox = randint(0, len(selprox_re)-1)	
	send.append(selprox_re[nprox])
	ndist = randint(0, len(seldist_re)-1)
	receive.append(seldist_re[ndist])
	syni = h.AMPA(0.5, sec = receive[counter])
	syn.append(syni)
	nci=h.NetCon(send[counter](0.5)._ref_v, syni, sec=send[counter])
	nci.weight[0] = 0.2
	nc.append(nci)

	#print selprox_re[nprox]
	print "sender[counter] = ", send[counter].name()
	print "receiver[counter] = ", receive[counter].name()

	#selprox_re.remove(selprox_re[nprox])
	#seldist_re.remove(seldist_re[ndist])

#	h.run()
########################################################################
'''
soma=[]
for recs in h.allsec():
	if any(s in recs.name() for s in record['soma_re0']):
		soma.append(recs)
#print soma[0].name()

dend=[]
seldend=[]
for recd in h.allsec():
#	dend.append(recd)
#	shuffle(dend)
	if any(s in recd.name() for s in record['dend_re_receiver']):
		seldend.append(recd)
		shuffle(seldend)
#print dend[0].name()

for var in 'v_sender', 'v_receiver', 'i_syn', 't':
	vec[var] = h.Vector()


vec['v_sender'].record(soma[0](0.5)._ref_v)
vec['v_receiver'].record(seldend[0](0.5)._ref_v)
vec['i_syn'].record(syn[0]._ref_i)
vec['t'].record(h._ref_t)

h.load_file("stdrun.hoc")
h.init()
h.tstop = 2400
h.run()


plt.xlabel('t (ms)')
plt.ylabel('v (mV)')                       
plt.subplot(2,2,1)
plt.plot(vec['t'], vec['v_sender'], label=soma[0].name() )
plt.plot(vec['t'], vec['v_receiver'], 'r', label = seldend[0].name())
plt.legend(loc='upper left')
plt.subplot(2,2,3)
plt.plot(vec['t'], vec['i_syn'])
plt.ylim(-5, 2.0)	

vec['v_sender'].record(soma[0](0.5)._ref_v)
vec['v_receiver'].record(seldend[1](0.5)._ref_v)
vec['i_syn'].record(syn[0]._ref_i)
vec['t'].record(h._ref_t)

h.load_file("stdrun.hoc")
h.init()
h.tstop = 2400
h.run()

plt.xlabel('t (ms)')
plt.ylabel('v (mV)')                       
plt.subplot(2,2,2)
plt.plot(vec['t'], vec['v_sender'], label=soma[0].name() )
plt.plot(vec['t'], vec['v_receiver'], 'r', label = seldend[1].name())
plt.legend(loc='upper left')
plt.subplot(2,2,4)
plt.plot(vec['t'], vec['i_syn'])
plt.ylim(-5, 2.0)	
plt.show()
'''