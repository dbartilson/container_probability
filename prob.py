import numpy as np
import math
import matplotlib.pyplot as plt; plt.rcdefaults()

# User-variables #############################################################

d = 16                  # Number of items to get (transfer states)
r_v = np.arange(1,72)   # Number of attempts to test
c = 4                   # Exchange rate

# Main #######################################################################

M = np.zeros((d+1,d+1)) # Markov transition matrix

# Probability to transition from state i to i (not get unique item)
# is along main diagonal, p(i|i) = (i-1)/d
for i in range(d):
    M[i,i] = i/d

# Probability to transition from state i to i+1 (get unique item) is along 
# lower diagonal, p(i+1|i) = (d-i+1)/d
for i in range(d-1):
    M[i+1,i] = (d-i)/d

# Set up initial state (100% initial probability of 0 items)
p_0 = np.zeros(d+1)
p_0[1] = 1.0

# Set up probability of completion for each number of attempts
p_i = np.zeros(len(r_v))

# For each number of attempts
for i in range(len(r_v)):
    # Set up dummy variable for current number of attempts
    r = r_v[i]
    
    # Use Markov chain logic to get probability distribution of n unique items 
    # given r tries (p_n = M^r * p_0)
    p_n = np.linalg.matrix_power(M,r) @ p_0
    
    # Calculate probablity of NOT getting the requisite number of items given
    # r tries
    
    # First set up the list of states (# unique items)
    n = list(range(d+1))
    
    # Modify this with the number of unique items after processing duplicates
    for j in range(len(n)):
        # Get the most unique items you could exchange with r-n duplicates at 
        # an exhange rate of one unique item per c duplicates
        n[j] = n[j] + math.floor((r-n[j])/c)
    
    # Now get the probability of completion (achieving d items) by subtracting
    # the summed probability of failed states (n < d) 
    p_i[i] = 1.0
    for j in range(len(p_n)):
        if n[j] < d:
           p_i[i] = p_i[i] - p_n[j]

# Plot #######################################################################
plt.bar(r_v,p_i)
# Set upper and lower limits @ points where probability = 0.001 and 0.999
xll = r_v[np.argwhere(p_i > 1e-3)[0]]- 0.5
xul = r_v[np.argwhere(p_i < 1-1e-3)[-1]] + 0.5
axes = plt.gca()
axes.set_xlim([xll,xul])
plt.xlabel('r  (Number of total items drawn)')
plt.ylabel('p(d|r)  (Probability of d items given r draws)')
plt.title('d (Number of items to get) = %d, c (Exchange rate) = %d:1' %(d,c))

