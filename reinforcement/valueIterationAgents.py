# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        x = self.iterations
        while x > 0:
            iter = util.Counter()
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    iter[state] = 0
                    continue
                maxVal = -9999999
                for action in self.mdp.getPossibleActions(state):
                    val = self.computeQValueFromValues(state, action)
                    maxVal = max(maxVal, val)
                iter[state] = maxVal
            self.values = iter
            x -= 1




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        newStatesAndTransitions = self.mdp.getTransitionStatesAndProbs(state, action)
        sum = 0
        for st in newStatesAndTransitions:
            newState = st[0]
            prob = st[1]
            reward = self.mdp.getReward(state, action, newState)
            sum += prob * (reward + self.discount * self.getValue(newState))
        return sum

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        actions = util.Counter()
        for action in self.mdp.getPossibleActions(state):
            actions[action] = self.computeQValueFromValues(state, action)
        return actions.argMax()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)


    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        x = self.iterations
        counter = 0
        index = 0
        iter = util.Counter()
        while counter < self.iterations:
            if index == len(self.mdp.getStates()):
                index = 0

            state = self.mdp.getStates()[index]
            index += 1
            counter += 1
            if self.mdp.isTerminal(state):
                continue
            maxVal = -9999999
            for action in self.mdp.getPossibleActions(state):
                val = self.computeQValueFromValues(state, action)
                maxVal = max(maxVal, val)
            iter[state] = maxVal
            self.values = iter


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors = {}
        for state in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(state):
                for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    if state not in predecessors:
                        s = set()
                        s.add(nextState)
                        predecessors[state] = s
                    else:
                        predecessors[state].add(nextState)
        pQueue = util.PriorityQueue()

        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state):
                continue
            diff = self.getValue(state)
            maxVal1 = -99999999
            for action in self.mdp.getPossibleActions(state):
                val = self.computeQValueFromValues(state, action)
                maxVal1 = max(maxVal1, val)
            diff = abs(diff - maxVal1)
            pQueue.push(state, -1 * diff)
        iter = util.Counter()
        for i in range(0, self.iterations):
            if pQueue.isEmpty():
                break
            state= pQueue.pop()
            if not self.mdp.isTerminal(state):

                maxVal2 = -9999999
                for action in self.mdp.getPossibleActions(state):
                    val = self.computeQValueFromValues(state, action)
                    maxVal2 = max(maxVal2, val)
                iter[state] = maxVal2

                for predecessor in predecessors[state]:
                    diff = self.getValue(predecessor)
                    maxVal3 = -9999999
                    for action in self.mdp.getPossibleActions(predecessor):
                        val = self.computeQValueFromValues(predecessor, action)
                        maxVal3 = max(maxVal3, val)
                    diff = abs(diff - maxVal3)
                    if diff > self.theta:
                        pQueue.update(predecessor, -1 * diff)
        self.values = iter






