#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import with_statement # This isn't required in Python 2.6
from Mouse import Mouse
from Keyboard import Keyboard

try:
  import json
except ImportError:
  try:
    import simplejson as json
  except ImportError:
    raise ImportError

import sys, traceback


def start():
    print """
           *** I am human ***
           par martin trigaux
            
    Merci d'utiliser mon programme, j'espère que vous allez le trouver utile
    Si vous avez un commentaire, n'hésitez pas à m'en faire part

        [1] créer une nouvelle liste
        [2] charger et exécuter une liste existante
        [?] a propos
        [x] quitter
        """
    return raw_input("Que voulez vous faire ? ")

def createList():
    
    fileName=raw_input("Enter le nom de votre nouvelle liste : ")
    
    listAction=[]
    print """
voici les commandes disponibles :
move, x, y                    # bouge la souris en x, y (position [0;0] est
                              #   ...dans le coin supérieur droit)
moveEasy, x, y, vitesse       # bouge la souris progressivement, la vitesse
                              #   ...est facultative (defaut 1, décimal)
clic, x, y, bouton            # clic en x, y
pressButton, x,y, bouton      # presse le bouton en x, y
releaseButton, x, y, bouton   # lâche le bouton en x, y
write, "quelque chose"        # écrit "quelque chose" (sans les guillemets) 
                              #   ...fonctionne sur les OS linux uniquement
wait, n                       # attendre n secondes (décimal pour millisecondes)
"""

    cmd=raw_input("enter la commande (sans les paramèters, 'x' pour quitter) : ")
    poss_cmd=['move', 'moveEasy', 'clic', 'pressButton', 'releaseButton', 'write', 'writeEasy', 'wait']

    while (cmd != 'x'):
        if (cmd not in poss_cmd):
            print "choix invalide, merci de choisir parmis : \n", poss_cmd
            cmd=raw_input("Que voulez vous faire ? ")
            
        else:
            valid=True
            currentAction={}
            if (cmd in [x for x in poss_cmd if x not in ['write', 'writeEasy', 'wait']]):
                x=raw_input("entez la coordonnée X : ")
                (x, valid) = isValidInt(x, valid)
                
                if valid:
                    y=raw_input("enter the Y coordinate : ")
                    (y, valid) = isValidInt(y, valid)
                    
                if valid:
                    if (cmd in ['clic', 'pressButton', 'releaseButton']):
                        button = raw_input("enter le numero du bouton (defaut 1) : ")
                        if button=="":
                            currentAction={"name":cmd, "args":[x, y]}
                        else:
                            (button, valid) = isValidInt(button, valid)
                            currentAction={"name":cmd, "args":[x, y, button]}
                    elif (cmd == 'moveEasy'):
                        speed = raw_input("enter la vitesse (defaut 1) : ")
                        if speed=="":
                            currentAction={"name":cmd, "args":[x, y]}
                        else:
                            (speed, valid) = isValidFloat(speed, valid)
                            currentAction={"name":cmd, "args":[x, y, speed]}
                    else:
                        currentAction={"name":cmd, "args":[x, y]}

            elif (cmd in ['write', 'writeEasy']):
                txt=raw_input("enter ce que vous voulez écrire : ")
                currentAction={"name":cmd, "args":[txt]}
            elif (cmd=='wait'):
                sec=raw_input("entrez le temps que vous voulez attendre : ")
                (sec, valid) = isValidFloat(sec, valid)
                currentAction={"name":cmd, "args":[sec]}
            
            if valid:
                listAction.append(currentAction)
            else:
                print "action invalide"
                    
            cmd=raw_input("\nQue voulez vous faire ? ")
            
    if listAction!=[]:
        with open("script/"+fileName+".json", 'w') as f:
            f.writelines(json.dumps(listAction, indent=4))
            f.flush()


def loadList():
    fileName=raw_input("Enter the name of your list : ")
    with open("script/"+fileName+".json") as f:
        listAction=json.load(f)
    
    mouse_function = { 
        'move': move_valid,
        'moveEasy': moveEasy_valid,
        'clic' : clic_valid
    }
    
    keyboard_function = {
        'write' : write_valid
    }
    
    m = Mouse()
    k = Keyboard()
    for cmd in listAction:
        # cmd contient {'name':'fonction1', 'args':['123', '456', 'abc']} par exemple
        try:
            funcname = cmd['name']
        except:
            print "...erreur il manque le nom de la méthode..."
        
        try:
            params = cmd['args']
        except:
            params=""

        try:
            func = (mouse_function[ funcname ] | keyboard_function [ funcname ] )
        except:
            print "...erreur fonction inconnue..."
        try:
            func( m, *params )
        except:
            print "...erreur à la fonction "+str(funcname)
            traceback.print_exc(file=sys.stdout)
        

def move_valid(m, x=None,y=None):
    m.move(x,y)

def moveEasy_valid(m, x=None,y=None, speed=1):
    m.moveEasy(x,y,speed)

def clic_valid(m, x=None, y=None, button=1):
    m.clic(x,y,button)
    
def write_valid(m):
    pass
    
def wait_valid(u, s):
    valid=True
    if s==None:
        valid=False
    else:
        (s, valid) = isValidFloat(s,valid)

    if valid:
        u.wait(s)
    else:
        print "fonction invalide"    

def isValidInt(n, valid):
    try:
        n=int(n)
        if n<0:
            print "pas de nombre négatif"
            valid=False
    except:
        print n, "n'est pas un entier valide"
        valid=False
    return (n, valid)

def isValidFloat(n, valid):
    try:
        n=float(n)
        if n<0:
            print "pas de nombre négatif"
            valid=False
    except:
        print n, "n'est pas un nombre valide"
        valid=False
    return (n, valid)

if __name__ == '__main__':
    choice = start()
    
    poss=tuple(('1', '2', '?', 'x'))
    while (choice not in poss):
        print "choix invalide, merci de choisir parmis \n", poss
        choice = raw_input("que voulez vous faire ? ")
    
    if (choice=='1'):
        createList()
    elif (choice=='2'):
        loadList()
    elif (choice=='?'):
        print "not yet implemented"
    
    print "see you soon"
