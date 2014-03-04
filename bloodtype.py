import numpy as np
import matplotlib.pyplot as plt

def blood_type(n_people,n_gen,O_p,A_p,B_p):
  BT = np.zeros((n_people,n_gen,2))
  BT[:O_p*n_people,0,:]=0
  BT[O_p*n_people:(O_p*n_people+A_p*n_people),0,:]=1
  BT[(O_p*n_people+A_p*n_people):,0,:]=2
  for t in range(1,n_gen):
    for j in range(n_people):
        for k in range(2):
            indj = np.random.randint(n_people)
            indk = np.random.randint(2)
            BT[j,t,k] = BT[indj,t-1,indk]
  countO = np.zeros(n_gen)
  countA = np.zeros(n_gen)
  countB = np.zeros(n_gen)
  for t in range(n_gen):
    for j in range(n_people):
        if BT[j,t,0] == 0 and BT[j,t,1] == 0:
            countO[t] += 1
        if BT[j,t,0] == 1 or BT[j,t,1] == 1:
            countA[t] += 1
        if BT[j,t,0] == 2 or BT[j,t,1] == 2:
            countB[t] += 1
  plt.clf()
  plt.plot(range(n_gen),countO/n_people,range(n_gen),countA/n_people,range(n_gen),countB/n_people)
  plt.xlabel('Generation')
  plt.ylabel('Population Percentage')
  plt.legend(['O Blood Type','A Allele', 'B Allele'])
  plt.savefig('bloodtypes.png')
