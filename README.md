# Chess Game

## Overview
This is an implementation of a chess game in Python using the Pygame library.

## Features
- Player vs. Player mode
- Classic chess rules and moves
- Basic piece capturing
- Check/Check mate 
- Stalemate
- En passant and Castling under correct conditions
- Pawn promotion
- UI indications for possible moves for each piece on-click
- UI to show captured pieces and game over
- UI flashing king square when in check
- UI button to start new game

## Prerequisites
- Python 3.3

## Setup the project

- Clone the repository: `git clone https://github.com/akshith-katuri/chess-game.git`
- Update pip - `pip install --upgrade pip`
- Install Virtualenv which is a tool to set up your Python environments: `pip install virtualenv`
- Create virtual environment: `python3.8 -m venv venv`
- activate virtual environment: 
 `env/Scripts/activate.bat` //In CMD
 `env/Scripts/Activate.ps1` //In Powershel
- pip list
- Install Pygame library - `pip install pygame`
- Navigate to the project directory: `cd chess-game`

## How to Play
- Start the game by running `python chess_game.py`

## Controls
- Click on a piece to select it. Then, you will see all possible moves of the selected piece
- Click on a valid square to move the selected piece.

## Game Rules
- Follows standard chess rules
