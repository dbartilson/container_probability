# container_probability : Calculate probability of completing collections in simple Python

This simple Python script implements a Markov chain method for calculating the probability of getting a certain number of unique items from a given number of random draws where one can exchange duplicates for unique items at a specified rate. This avoids the costly and less accurate method of Monte Carlo simulation.

This was originally developed for calculating the number of 'containers' needed to complete 'collections' in World of Warships.

**License:** MIT

# Introductory Example to Markov Chains

You have zero items to start with and want to see what your probability is of having 2 unique items after drawing 2 containers. Let's say there are only 2 unique items that can be dropped. We lay out the probabilities:

* Probability of 'transitioning' to 1 unique item given you have zero: p(1|0) = 100%
* Probability of 'transitioning' to still having 1 unique item given that you have 0: p(1|1) = 50%
* Probability of 'transitioning' to 2 unique items give that you have 1 p(2|1) = 50%

We have a 100% chance of getting a unique item in the first step since our first draw has to be unique. We have a 50/50 chance of getting a duplicate or getting a unique on the second draw since there are 2 unique items to draw. We can't lose items (p(0|1) = 0%) and we can't get 2 items on one draw (p(2|0) = 0%).
We can write this as a matrix

| p(1\|0) = 1 | p(1\|1) = 0.5 |
|-------------|---------------|
| p(2\|0) = 0 | p(2\|1) = 0.5 |

Now we can start 'simulating'. We set an initial 'state' with 100% probability of having zero items, and our state after one draw is then:

p(1 item after 1 draw) = p(1|0)\*p(0) + p(1|1)\*p(1) = 1\*1 + 0.5*0= 100% probability

We can now set this as our current state (p(1) = 100%) and look at the next draw

p(1 item after another draw) = p(1|0)\*p(0) + p(1|1)\*p(1) = 1\*0 + 0.5\*1= 50% probability

p(2 items after another draw) = p(2|0)\*p(0) + p(2|1)\*p(1) = 0\*0 + 0.5\*1= 50% probability

This example is overly simple, but it hopefully gets across the point that we can calculate the probability of transitioning from having n to n+1 containers pretty simply. If we write this in a matrix (above, let's call it M) and vector form, where each vector holds the state probabilities (basically just a stack of p(0), p(1), p(2), ...) then we can write

**p**_1 = **M** \* **p**_0

**p**_2 = **M** \* **p**_1 = **M**^2 \* **p**_0

...

**p**_n = **M**^n \* **p**_0

where **p**_n is the vector of state probabilities (basically, the vector of probabilities of having some number of unique items) after n containers have been drawn.  **p**_0 represents our initial state, which is 100% chance of having 0 items (p(0) = 1) and all others are zero.

This gets us most of what we want: We can get the probability of having k unique items after drawing from n containers. The difference between n and k (n-k) is our number of duplicates. For an exchange rate of "c" duplicates for one unique item, then we get an additional (n-k)/c items (rounding down, of course).

So here's the algorithm:

1. Establish our parameters (number of needed items d, exchange rate c)
2. Set up state transition matrix M given that p(i|i) = (i-1)/d and p(i+1|i) = 1-p(i|i)
3. Set up a range of n (number of containers) to test, loop over that range
 1. Calculate the state probabilities after n draws: p_n = M^n * p_0
 2. Calculate the number of duplicates and exchanged uniques: (n-k)/c for each state
 3. Sum the 'drawn' uniques with the 'exchanged' uniques k' = k + floor((n-k)/c)  for each state
 4. Sum the state probabilities that didn't get enough items : sum components of p_n with k' < d
 5. The probability of getting enough items given n draws is 1 - (the result from the previous step)
