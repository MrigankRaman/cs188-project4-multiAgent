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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

#         "*** YOUR CODE HERE ***"
#         print(newPos)
#         print(newFood)
#         for item in newGhostStates:
#             print(item.getPosition())
        print(newScaredTimes)
        ans = 0
        for item in newGhostStates:
            ans = ans + (util.manhattanDistance(newPos,item.getPosition()))
        ans =  ans + sum(newScaredTimes)
        if(len(newFood.asList())>0):
            ldist = util.manhattanDistance(newFood.asList()[0],newPos)
            for item in newFood.asList():
                if(util.manhattanDistance(item,newPos)<ldist):
                    ldist = util.manhattanDistance(item,newPos)
            ans = ans - 4*ldist
        if len(currentGameState.getFood().asList())-len(newFood.asList()) > 0:
             ans = ans + 100
        else:
            ans = ans-100
        capsuleplaces =   successorGameState.getCapsules()  
        if successorGameState.getPacmanPosition() in capsuleplaces:
            ans += 120
        if action == Directions.STOP:
            ans -= 4    
        return ans + successorGameState.getScore()

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
        def maxValue(gameState,depth,numGhosts):
            if depth==0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = -(float("inf"))
            for action in gameState.getLegalActions(0):
                nextState = gameState.generateSuccessor(0,action)
                v = max(v,minValue(nextState,depth-1,numGhosts,1))
            return v
       
        
        def minValue(gameState,depth,numGhosts,index):
            if depth==0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = (float("inf"))
            for action in gameState.getLegalActions(index):
                nextState = gameState.generateSuccessor(index,action)
                if index < numGhosts:
                    v = min(v,minValue(nextState,depth-1,numGhosts,index+1))
                elif index == numGhosts:
                    v= min(v,maxValue(nextState,depth-1,numGhosts))
            return v
        depth = gameState.getNumAgents()*self.depth
        legalActions = (gameState.getLegalActions(0))
        numGhosts =  gameState.getNumAgents()-1
        bestAction = Directions.STOP
        #value = -(float("inf"))
        value = maxValue(gameState,depth,numGhosts)
        for action in legalActions:
           
            nextState = gameState.generateSuccessor(0,action)
            if minValue(nextState,depth-1,numGhosts,1) == value :
                return action
#             preValue = value
#             value = max(value,minValue(nextState,depth-1,numGhosts,1))
#             if value > preValue:
#                 bestAction = action
                                            
#         return bestAction
        util.raiseNotDefined()
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState,depth,numGhosts,alpha,beta):
            if depth==0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = -(float("inf"))
            for action in gameState.getLegalActions(0):
                nextState = gameState.generateSuccessor(0,action)
                v = max(v,minValue(nextState,depth-1,numGhosts,1,alpha,beta))
                if v>beta:
                    return v
                alpha = max(alpha,v)
            return v
       
        
        def minValue(gameState,depth,numGhosts,index,alpha,beta):
            if depth==0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = (float("inf"))
            legalActions = gameState.getLegalActions(index)
            if index == numGhosts:     
                for action in legalActions:
                    v = min(v, maxValue(gameState.generateSuccessor(index, action), depth-1,numGhosts, alpha, beta))
                    if v < alpha:
                        return v
                    beta = min(beta, v)
            else:
                for action in legalActions:
                    v = min(v, minValue(gameState.generateSuccessor(index, action), depth-1,numGhosts, index + 1, alpha, beta))
                    if v < alpha:
                        return v
                    beta = min(beta, v)
            return v
        depth = gameState.getNumAgents()*self.depth
        legalActions = (gameState.getLegalActions(0))
        numGhosts =  gameState.getNumAgents()-1
        bestAction = Directions.STOP
        alpha = -(float("inf"))
        beta = (float("inf"))
        value = -(float("inf"))
        for action in legalActions:
            nextState = gameState.generateSuccessor(0,action)
            preValue = value
            value = max(value,minValue(nextState,depth-1,numGhosts,1,alpha,beta))
            if value>preValue:
                bestAction = action
            if value > beta:
                return bestAction
            alpha = max(alpha,value)
        return bestAction
        util.raiseNotDefined()

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
        def maxValue(gameState,depth,numGhosts):
            if depth==0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = -(float("inf"))
            for action in gameState.getLegalActions(0):
                nextState = gameState.generateSuccessor(0,action)
                v = max(v,expValue(nextState,depth-1,numGhosts,1))
            return v
         
        def expValue(gameState,depth,numGhosts,index):
            if depth==0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = 0
            for action in gameState.getLegalActions(index):
                nextState = gameState.generateSuccessor(index,action)
                if index < numGhosts:
                    v = v+(expValue(nextState,depth-1,numGhosts,index+1))
                elif index == numGhosts:
                    v= v + (maxValue(nextState,depth-1,numGhosts))
            return v/len(gameState.getLegalActions(index))
        depth = gameState.getNumAgents()*self.depth
        legalActions = (gameState.getLegalActions(0))
        numGhosts =  gameState.getNumAgents()-1
        bestAction = Directions.STOP
        #value = -(float("inf"))
        value = maxValue(gameState,depth,numGhosts)
        for action in legalActions:
           
            nextState = gameState.generateSuccessor(0,action)
            if expValue(nextState,depth-1,numGhosts,1) == value :
                return action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return - float("inf")

    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    Pos = currentGameState.getPacmanPosition()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    capsulePlaces =   currentGameState.getCapsules()
    ans = 0
    if(len(Food.asList())>0):
        ldist = util.manhattanDistance(Food.asList()[0],Pos)
        for item in Food.asList():
            if(util.manhattanDistance(item,Pos)<ldist):
                ldist = util.manhattanDistance(item,Pos)
        ans = ans - 1.5*ldist
#     if(len(capsulePlaces)>0):
#         capdist = util.manhattanDistance(capsulePlaces[0],Pos)
#         for item in capsulePlaces:
#             if(util.manhattanDistance(item,Pos)<capdist):
#                 capdist = util.manhattanDistance(item,Pos)
#         ans = ans - capdist
    numghosts = len(GhostStates)    
    i = 1
    disttoghost = float("inf")
    while i <= numghosts:
        xy1 = currentGameState.getPacmanPosition()
        xy2 = currentGameState.getGhostPosition(i)
        nextdist1 = ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5
        nextdist2 = util.manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(i))
        if nextdist1 > nextdist2:
            nextdist = nextdist1 - nextdist2
        else:
            nextdist = nextdist2 - nextdist1
        disttoghost = min(disttoghost, nextdist)
        i += 1
    ans = ans + max(disttoghost,4)*2    
    ans = ans - 4*len(Food.asList())
    ans = ans - 3.5*len(capsulePlaces)
    return ans + currentGameState.getScore()                   
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
