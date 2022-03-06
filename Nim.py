from anytree import Node, RenderTree, NodeMixin
import os


class Tree(NodeMixin):   #ADD NODE FEATURE
    def __init__(self, state, level, dep, parent=None, children=None, heuristic=None):
        super(Tree, self).__init__()
        self.state = state
        self.level = level
        self.dep = dep
        self.parent = parent
        self.heuristic = heuristic
        if children:
            self.children = children
        
def minimax(node):
    if node.is_leaf:
        return node.heuristic
    if node.level == 'Max':    #FOR MAXIMIZING PLAYER
        maxEva = -1000
        for child in node.children:
            node.heuristic = minimax(child)
            maxEva = max(maxEva,node.heuristic)   #GIVES MAXIMUM OF THE VALUES
        return maxEva  
    else:   #FOR MINIMIZING PLAYER
        minEva = 1000
        for child in node.children:
            node.heuristic = minimax(child)
            minEva = min(minEva,node.heuristic)   #GIVES MINIIMUM OF THE VALUES
        return minEva   
        
def heuristicgenerator(node): #SET HEURISTIC FOR EVERY LEAF NODE
    for child in node.children:
        if child.is_leaf:
            if child.level == 'Min':
                child.heuristic = 1
            elif child.level == 'Max':
                child.heuristic = 0
        heuristicgenerator(child)

def movegenerator(number):  #SPLITS NUMBER TO POSSIBLE MOVES
    moves = []
    for i in range(number):
       for j in range(int((number+1)/2)):
            if i+j == number and i != j:
                moves.append([i, j])
    return moves

def buildingtree(node): #GENERATES A TREE WITH ALL POSSIBLE OUTCOMES
        for move in node.state:
            if move > 2:
                moves = movegenerator(move) 
                for i, j in moves:  #FOR EVERY MOVE
                    newstate = node.state[:]
                    index = newstate.index(move)
                    newstate[index] = i
                    newstate.append(j)
                    newstate = sorted(newstate)
                    if node.level == 'Max': #CREATE A CHILD
                        Tree(newstate, 'Min', node.dep+1, parent=node)
                    else:
                        Tree(newstate, 'Max', node.dep+1, parent=node)
        for child in node.children: #FOR EVERY CHILD
            buildingtree(child) #RECURSIVELY CALL FUNCTION

def game(clear, pause, node):   #DISPLAYS GAME
    while not node.is_leaf:
        clear()
        print(f'\nCurrent State:    {node.state}')
        print('\nMoves:',end="  ")
        i = 1
        for child in node.children:
            print(f'{i}. {child.state}', end="    ")
            i = i + 1
        if node.level == 'Min':     #PLAYER'S TURN
            print("\n\nSelect Your Move:", end=" ")
            choice=int(input())
            choice = choice - 1
            if choice > len(node.children) or choice < 0:
                print("\nInvalid Input")
                pass
            else:
                node = node.children[choice]
        else:       #AI'S TURN
            for child in node.children:
                if child.heuristic == 1:
                    print(f"\n\nAI chooses: {child.state}",end="    ")
                    print('\n')
                    node = child
                    break
                elif len(node.children) == 1: #IF ONLY ONE MOVE IS POSSIBLE
                    print(f"\n\nAI chooses: {node.children[0].state}",end="    ")
                    print('\n')
                    node = node.children[0]
                    break
            
            pause()

    if node.heuristic == 1:
        print('\n\nAI wins\n\n')
    else:
        print('\n\nYou win\n\n')
    
def main():

    clear = lambda: os.system('cls')
    pause = lambda: os. system("pause")
    num = []
    print("Enter Number of Sticks: ")
    num.append(int(input()))
    root = Tree(num, 'Min', 0)
    buildingtree(root)
    heuristicgenerator(root)
    root.heuristic = minimax(root)
    game(clear, pause, root)



if __name__ == "__main__":
    main()