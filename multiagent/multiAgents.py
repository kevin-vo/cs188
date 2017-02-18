# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newGhostPositions = successorGameState.getGhostPositions()
        foodEaten = currentGameState.getNumFood() - successorGameState.getNumFood()
        win = 0
        lose = 0
        if successorGameState.isWin():
            win = 9999
        if successorGameState.isLose():
            lose = -99999

        minFoodDist = 0
        dist = 0
        sizeX = 0
        sizeY = 0
        for i in newFood:
            sizeY = len(i)
            sizeX += 1
        for i in range(0, sizeX):
            for j in range(0, sizeY):
                if newFood[i][j] == True:
                    dist = abs(newPos[1] - j) + abs(newPos[0] - i)
                    if minFoodDist == 0:
                        minFoodDist = dist
                    else:
                        minFoodDist = min(minFoodDist, dist)

        minGhostDist = 0
        for i in newGhostPositions:
            dist = abs(newPos[1] - i[1]) + abs(newPos[0] - i[0])
            if minGhostDist == 0:
                minGhostDist = dist
            else:
                minGhostDist = min(minGhostDist, dist)
        closeGhost = 0
        if minGhostDist <= 2:
            closeGhost = -99999
        return win + lose + closeGhost + foodEaten * 1000 - minFoodDist

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        MinimaxAgent.actionList = []
        x = self.value(0, gameState, self.depth)
        return MinimaxAgent.actionList[len(MinimaxAgent.actionList) - 1]


    # def value(self, agentIndex, gameState, depth):
    #     if gameState.isWin() or gameState.isLose() or depth == 0:
    #         return self.evaluationFunction(gameState)
    #     elif agentIndex == 0:
    #         return self.maxValue(agentIndex, gameState, depth)
    #     else:
    #         return self.minValue(agentIndex, gameState, depth)
    #
    # actionList = []
    # def maxValue(self, agentIndex, gameState, depth):
    #     v = -9999999
    #     action = "Stop"
    #     for act in gameState.getLegalActions(agentIndex):
    #         successor = gameState.generateSuccessor(agentIndex, act)
    #         for i in range(1, gameState.getNumAgents()):
    #             x = self.value(i, successor, depth)
    #             if x > v:
    #                 v = x
    #                 action = act
    #             #v = max(v, self.value(i, successor, depth - i))
    #     MinimaxAgent.actionList.append(action)
    #     return v
    #
    # def minValue(self, agentIndex, gameState, depth):
    #     v = 9999999
    #     for act in gameState.getLegalActions(agentIndex):
    #         successor = gameState.generateSuccessor(agentIndex, act)
    #         v = min(v, self.value(0, successor, depth - 1))
    #     return v

    def value(self, agentIndex, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        elif agentIndex == 0:
            return self.maxValue(agentIndex, gameState, depth)
        else:
            return self.minValue(agentIndex, gameState, depth)

    actionList = []
    def maxValue(self, agentIndex, gameState, depth):
        v = -9999999
        action = "Stop"
        for act in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, act)
            x = self.value(1, successor, depth)
            if x > v:
                v = x
                action = act
                #v = max(v, self.value(i, successor, depth - i))
        MinimaxAgent.actionList.append(action)
        return v

    def minValue(self, agentIndex, gameState, depth):
        v = 9999999
        for act in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, act)
            if agentIndex == gameState.getNumAgents() - 1:
                v = min(v, self.value(0, successor, depth - 1))
            else:
                v = min(v, self.value(agentIndex + 1, successor, depth))
        return v





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        AlphaBetaAgent.actionList = []
        x = self.value(0, gameState, self.depth, -9999999, 9999999)
        print(x)
        return AlphaBetaAgent.actionList[len(AlphaBetaAgent.actionList) - 1]

    def value(self, agentIndex, gameState, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        elif agentIndex == 0:
            return self.maxValue(agentIndex, gameState, depth, alpha, beta)
        else:
            return self.minValue(agentIndex, gameState, depth, alpha, beta)

    actionList = []
    def maxValue(self, agentIndex, gameState, depth, alpha, beta):
        v = -9999999
        action = "Stop"
        for act in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, act)
            x = self.value(1, successor, depth, alpha, beta)
            if x > v:
                v = x
                action = act
            if v > beta:
                return v
            else:
                AlphaBetaAgent.actionList.append(action)
            alpha = max(alpha, v)
        return v

    def minValue(self, agentIndex, gameState, depth, alpha, beta):
        v = 9999999
        for act in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, act)
            if agentIndex == gameState.getNumAgents() - 1:
                v = min(v, self.value(0, successor, depth - 1, alpha, beta))
            else:
                v = min(v, self.value(agentIndex + 1, successor, depth, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        ExpectimaxAgent.actionList = []
        x = self.value(0, gameState, self.depth)
        return ExpectimaxAgent.actionList[len(ExpectimaxAgent.actionList) - 1]

    def value(self, agentIndex, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        elif agentIndex == 0:
            return self.maxValue(agentIndex, gameState, depth)
        else:
            return self.minValue(agentIndex, gameState, depth)

    actionList = []

    def maxValue(self, agentIndex, gameState, depth):
        v = -9999999.0
        action = "Stop"
        for act in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, act)
            x = self.value(1, successor, depth) + 0.0
            if x > v:
                v = x
                action = act
        ExpectimaxAgent.actionList.append(action)
        return v

    def minValue(self, agentIndex, gameState, depth):
        v = 0.0
        count = 0.0
        for act in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, act)
            if agentIndex == gameState.getNumAgents() - 1:
                v += self.value(0, successor, depth - 1)
            else:
                v += self.value(agentIndex + 1, successor, depth)
            count += 1.0
        return v / count


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: I wanted winning to be REALLY good and losing to be REALLY bad.
      I used my reflex evaluation function to determine important values such as
      the number of food left, the distance to the closest food, and the distance
      of the closest ghost. I put a hard cap on the ghost distance because I did not
      want my agent to be super obsessed with maximizing survivability since time is
      deducted from score. The rest was just adjusting weights correspondingly.
    """
    "*** YOUR CODE HERE ***"
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    newGhostPositions = successorGameState.getGhostPositions()
    food = currentGameState.getNumFood()

    if successorGameState.isWin():
        return 9999999
    if successorGameState.isLose():
        return -9999999

    minFoodDist = 0
    dist = 0
    sizeX = 0
    sizeY = 0
    for i in newFood:
        sizeY = len(i)
        sizeX += 1
    for i in range(0, sizeX):
        for j in range(0, sizeY):
            if newFood[i][j] == True:
                dist = abs(newPos[1] - j) + abs(newPos[0] - i)
                if minFoodDist == 0:
                    minFoodDist = dist
                else:
                    minFoodDist = min(minFoodDist, dist)

    minGhostDist = 0
    for i in newGhostPositions:
        dist = abs(newPos[1] - i[1]) + abs(newPos[0] - i[0])
        if minGhostDist == 0:
            minGhostDist = dist
        else:
            minGhostDist = min(minGhostDist, dist)

    if minGhostDist > 5:
        minGhostDist = 5

    return scoreEvaluationFunction(currentGameState) - minFoodDist - food * 5 - 3 * len(currentGameState.getCapsules()) + minGhostDist

# Abbreviation
better = betterEvaluationFunction

