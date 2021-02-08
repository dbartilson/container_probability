import numpy as np
import math
import matplotlib.pyplot as plt; plt.rcdefaults()

# User-variables #############################################################

d = 16                  # Number of items to get (transfer states)
c = 4                   # Exchange rate
n_v = np.arange(1,c*d)  # Number of attempts to test

k_0 = 0                 # Starting number of items
dup_0 = 0               # Starting number of duplicates

# Main #######################################################################

M = np.zeros((d+1,d+1)) # Markov transition matrix

# Probability to transition from state i to i (not get unique item)
# is along main diagonal, p(i|i) = (i-1)/d
for i in range(d+1):
    M[i,i] = i/d

# Probability to transition from state i to i+1 (get unique item) is along 
# lower diagonal, p(i+1|i) = (d-i+1)/d
for i in range(d):
    M[i+1,i] = (d-i)/d

# Set up initial state (100% initial probability of 0 items)
p_0 = np.zeros(d+1)
p_0[k_0] = 1.0

# Set up probability of completion for each number of attempts
p = np.zeros(len(n_v))

# For each number of attempts
for i in range(len(n_v)):
    # Set up dummy variable for current number of attempts
    n = n_v[i]
    
    # Use Markov chain logic to get probability distribution of n unique items 
    # given r tries (p_n = M^r * p_0)
    p_n = np.linalg.matrix_power(M,n) @ p_0
    
    # Calculate probablity of NOT getting the requisite number of items given
    # n tries
    
    # Set up the list of states (# unique items)
    k = list(range(d+1)) 
    
    # Modify this with the number of unique items after processing duplicates
    if c > 0:
        for j in range(len(k)):
            # Get the most unique items you could exchange. Total number of draws
            # = n + k_0 + dup_0. Number of unique = k[j]. So duplicates =
            # n+k_0+dup_0-k[j]. Then we divide by c and round down to exchange
            # for unique items
            k[j] = k[j] + math.floor((n+k_0+dup_0-k[j])/c)
    
    # Now get the probability of completion (achieving d items) by subtracting
    # the summed probability of failed states (n < d) 
    p[i] = 1.0
    for j in range(len(p_n)):
        if k[j] < d:
           p[i] = p[i] - p_n[j]
        else:
            break

# Plot #######################################################################

plt.bar(n_v,p)
# Set upper and lower limits @ points where probability = 0.001 and 0.999
xll = n_v[np.argwhere(p > 1e-2)[0]] - 0.5
xul = n_v[np.argwhere(p > 1-1e-2)[0]] + 0.5
axes = plt.gca()
axes.set_xlim([xll,xul])

if k_0 == 0 and dup_0 == 0:
    plt.xlabel('n (Number of containers)')
    plt.ylabel('p(d|n)  (Probability of finishing collection)')
    plt.title('d (Number of items in collection) = %d, c (Exchange rate) = %d:1' %(d,c))
else:
    plt.xlabel('n (Number additional of containers)')
    plt.ylabel('p(d|n)  (Probability of finishing collection)')
    plt.title('d (Number of items in collection) = %d, c (Exchange rate) = %d:1 \
          \n Starting with %d unique and %d duplicates' %(d,c,k_0,dup_0))

plt.show()
plt.savefig('figure.png')