from random import Random
from tkinter import Tk, Button, Entry, Label, Text, END, Canvas, LAST
from tkinter.messagebox import showinfo
import math
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import random

CENTER_X, CENTER_Y = 750, 200  # Center of the large circular path, players are going to be placed along it

class LinkedList:           #Implementing Linked list
    def __init__(self, val, next = None):
        self.val = val
        self.next = next

    def addLink(self, node):
        self.next = node

class gameInfo:
    def __init__(self, countValue = -1, currHead = LinkedList(0), playerList = [], eliminationButton = None, playerButtons = {}, roundCount = 1):
        self.countValue = countValue
        self.playerList = playerList
        self.playerButtons = playerButtons
        self.eliminationButton = eliminationButton
        self.roundCount = roundCount
        self.currHead = currHead

    def print_Players(self):   #prints each player's name in a console
        for player in self.playerList:
            print(f"Player: {player}")

    def updateCurrHead(self, head):
        self.currHead = head    #update the head of a Linked List

    def initPlayerButtons(self):    #Create a list of player buttons to display
        for player in self.playerList:
            currPlayerButton = Button(root, text = player, font = appFont)
            self.playerButtons[player] = currPlayerButton

    def initEliminationButton(self, x_pos, y_pos):  #Placing a button to eliminate players (play a round)
        self.eliminationButton = Button(root, text = "Eliminate\na player", command = self.playARound, font = appFont)
        self.eliminationButton.place(x = x_pos, y = y_pos)

    def playARound(self):   #playing a round of a game
        res = deleteNodeHead(self.currHead, self.countValue)    #Deling the kth node starting from the current head
        self.playerList[self.playerList.index(res)] = -1    #Deleting an eliminated player from the list
        self.playerButtons[res].destroy()   #Erase the button representing an eliminated player
        if self.checkIfTheGameEnded():  #Checking if the game ended this round
            outText.insert(END, f"Winner: {self.currHead.val}\n")
            self.eliminationButton.config(text = "Reset\nthe game", command = self.resetTheGame)
            return  # Add end game features later
        outText.insert(END, f"Round {self.roundCount}: {res} is eliminated\nCurrent head: {self.currHead.val}\n")
        self.roundCount += 1    #Increasing the round count

    def checkIfTheGameEnded(self):  #Checking if the game ended
        if self.currHead.next == self.currHead or self.currHead == None:    #If there is only one node in a Linked List, the game ended
            showinfo("WE HAVE A WINNER!!!", message="Winner " + str(self.currHead.val))
            return True
        return False

    def resetTheGame(self): #Reset the game
        self.playerButtons[self.currHead.val].destroy() #Destroying the winner's button
        outText.delete(1.0, END)    #Erasing text from the textBox
        Game.eliminationButton.destroy()    #Erasing the eliminate (play a round) button
        del self



def fullGame(n, k): #Play a full game automatically
    head = initLinkedListFullgame(n)    #Initialize a linked list for a full game
    while True:
        tempHead = deleteNodeHeadforFullGame(head, k)  #Delete the k-th Node from the Linked List
        if tempHead == None:        #If the next node is the only node, break from the loop
            break
        head = tempHead             #Change the head to the nextNode
    return head

def deleteNodeHeadforFullGame(head, k):        #Delete the k-node starting from head
    node = head
    if node.next == node:           #If the next node points to the same node, there is only one node left
        node.next = None
        return node.next
    for i in range(k - 2):
        node = node.next            #Get to the node previous to which we want to delete
    node.next = node.next.next      #Delete the node next to our current node
    return node.next

def initLinkedListFullgame(n):          #Initialize a Linked List for a game
    firstNode = LinkedList(0)
    previousNode = firstNode
    for i in range(1, n - 1):
        currNode = LinkedList(i)
        previousNode.next = currNode
        previousNode = currNode
    lastNode = LinkedList(n - 1, firstNode)
    previousNode.next = lastNode
    return firstNode


def remove_punct(s):    #Remove punctuation from an input box
    punct = [",", ".", ";", ":", "/"]
    return ''.join(c for c in s if c not in punct)


def deleteNodeHead(head, k):  # Delete the k-node starting from head
    node = head
    if node.next == node:  # If the next node points to the same node, there is only one node left
        node.next = None
        return node.next
    for i in range(k - 2):
        node = node.next  # Get to the node previous to which we want to delete
    deletedNode = node.next.val
    node.next = node.next.next  # Delete the node next to our current node
    Game.currHead = node.next  #Set currHead to the new Head
    return deletedNode

def printLLItter(head, first, bSome = False):         #Print Linked List
    while head != head.next and head != first or bSome == False:
        outText.insert(END, f"Head val: {head.val} points to {head.next.val}; ")
        head = head.next
        bSome = True
    outText.insert(END, "\n")

def initLinkedList(players):    #Initialize a Linked List for a manual game
    firstNode = LinkedList(players[0])
    previousNode = firstNode
    for player in players[1:-1]:
        currNode = LinkedList(player)
        previousNode.next = currNode
        print(f"CurrentNode = {previousNode.val}, points to: {currNode.val}")
        previousNode = currNode
    lastNode = LinkedList(players[len(players) - 1], firstNode)
    previousNode.next = lastNode
    print(f"CurrentNode = {lastNode.val}, points to: {lastNode.next.val}")
    return firstNode

def initPlayers():  #Initialize a list of players from the input Box
    Game.playerList = remove_punct(playersNames.get(1.0, END)).split()

def makeACircle(n): #Put Player Buttons in a circular path
    radius = 165  # Radius of the large circular path, players are going to stand along this path

    for i in range(n):
        angle = 2 * math.pi * i / n # Calculate the angle for each button. Divide 2 pi by the player's width to player's number ratio
        button_x = CENTER_X + radius * math.cos(angle) - 20 # Calculate the x, y position for each button
        button_y = CENTER_Y + radius * math.sin(angle) - 10

        # Create a button and place it at the calculated position
        Game.playerButtons[Game.playerList[i]].place(x = button_x, y = button_y)

def startTheGame():     #Start the manual game
    count = int(entryCount.get())   #Get the k value
    if count == "": #Check if the entry for the k value is empty
        showinfo("Error", message="Please fill in all the boxes")
        return
    Game.countValue = count #Update the count value for the game
    initPlayers()   #Initialize a list of players
    if len((Game.playerList)) > 12 or len((Game.playerList)) < 2:   #Check if the number of players is in acceptable range
        showinfo("Error", message = "Number of players should be between 2 and 12")
        return
    outText.delete(1.0, END)    #Delete previous text from the textBox
    Game.updateCurrHead(initLinkedList(Game.playerList))    #Update the current head for the game
    Game.print_Players()    #Print players' names into console
    Game.initPlayerButtons()    #Initialize players' Buttons
    makeACircle(len(Game.playerList))   #Display players' Buttons in a circular path
    Game.initEliminationButton(CENTER_X - 50, CENTER_Y - appFont[1])    #Initialize and place the Elimination (play a round) button in the center of a circular path
    print(Game.currHead.val)


def randomizeTheGame(): #Play a randomized version of the game that automatically plays itself for a set amount of times
    playersList = remove_punct(playersNames.get(1.0, END)).split()  #Initialize a players' list
    if len(playersList) > 12 or len(playersList) < 2:   #Check if the number of players is in acceptable range
        showinfo("Error", message = "Number of players should be between 2 and 12")
        return

    numCases = int(numTestCasesEntry.get()) #Get the number of test cases from an Entry
    if numCases < 0:    #If the Number of cases is less than 0, raise an error
        showinfo("Error", "Please enter a valid number of cases")
        return

    resDF = pd.DataFrame(0, index=playersList, columns=["Wins"])    #Create a pandas dataframe to track players and how many rounds they won

    for i in range (numCases):  #Play the game a set amount of test cases
        k = random.randint(1, len(playersList) * 20)    #Randomize the k value
        winner = fullGame(len(playersList), k)  #Find a winner of a current round
        print(f" K: {k} Winner: {winner.val}")  #Print a winner of a current round
        resDF.at[playersList[winner.val], "Wins"] += 1  #Add a victory to a player that won a current round

    print("\n", resDF, "\n") #Print a resulting dataframe into the console
    print(f"\nWinner: Name: {resDF["Wins"].idxmax()}, Num of Wins: {resDF["Wins"].max()}\n")   #Print the winner in the console
    names = resDF.index.tolist()   #Make a list of players' names from the dataframe
    values = resDF["Wins"].tolist() #Make a list of players' rounds won from the dataframe

    plt.bar(names, values, color = "maroon", width = 0.4)   #Create a bar chart
    plt.annotate("Winner", arrowprops = dict(facecolor = "green"),
                 xy = (values.index(resDF["Wins"].max()), resDF["Wins"].max()),
                 xytext = (values.index(resDF["Wins"].max()) + 1, resDF["Wins"].max()))
    plt.xlabel("Number of wins")    #X-axis represents the number of wins of each player
    plt.ylabel("Names")     #Y-axis represents the names of each player
    plt.title("Wins per person")  #Set a title for a plot
    plt.grid(linestyle = "--", color = "blue", axis = "y")  #add a grid
    plt.show()  #Show the plot window



root = Tk() #Create a window app
root.title("Andrii Fil Elimination game")   #Set a title
root.geometry("1000x800")
appFont = ("Arial", 18)

Game = gameInfo()

labelNText = "Enter players' names (2 - 12 players)"
labelKText = "Enter the number of counts to eliminate\nthe player:"
labelRandText = "Randomize the results"
labelTestCases = "Enter the Number of Test Cases:"
labelXPadding, labelYPadding = 10, 20

labelPlayers = Label(root, text = labelNText, font = appFont)
labelPlayers.place(x = labelXPadding, y = labelYPadding)

playersNames = Text(master = root, width = 30, height = 2, font = appFont)
playersNames.place(x = labelXPadding, y = labelYPadding + appFont[1] * 3)

labelCount = Label(root, text = labelKText, font = appFont, anchor = "w", justify = "left")
labelCount.place(x = labelXPadding, y = labelYPadding + appFont[1] * 7)

entryCount = Entry(root, font = appFont, width = 3)
entryCount.place(x = labelXPadding + appFont[1] * 7, y = labelYPadding + appFont[1] * 9 - 8)

startTheGameButton = Button(root, text = "Start the Game", command = startTheGame, font = appFont)  #Create a start game button
startTheGameButton.place(x = labelXPadding + 100, y = labelYPadding + appFont[1] * 11)

outText = Text(root, height = 8, width = 41, font = appFont)
outText.insert(END, "Information about the game is going to be placed here")
outText.place(x = 0, y = labelYPadding + appFont[1] * 15)

labelRand = Label(root, text = labelRandText, font = appFont)
labelRand.place(x = labelXPadding + 100, y = labelYPadding + appFont[1] * 30)

labelCases = Label(root, text = labelTestCases, font = appFont)
labelCases.place(x = labelXPadding, y = labelYPadding + appFont[1] * 33)

numTestCasesEntry = Entry(root, font = appFont, width = 7)
numTestCasesEntry.place(x = labelXPadding + appFont[1] * (len(labelTestCases) - 11), y = labelYPadding + appFont[1] * 33)

buttonRandomize = Button(root, text = "Randomize", command = randomizeTheGame, font = appFont)
buttonRandomize.place(x = labelXPadding + 100,  y = labelYPadding + appFont[1] * 37)

root.mainloop()