<h1 align="center">Tangram AI</h1>


<p align="center">
 <img width="50%" src="https://github.com/timothewt/TangramAI/blob/master/assets/introduction.png" alt="Tangram Main Img">
</p>

<!-- Table of Contents -->
# Table of Contents
- [About the Project](#about-the-project)
  * [Context](#context)
  * [Made with](#made-with)
  * [Features](#features)
- [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
- [Usage](#usage)
  * [Commands](#commands)
  * [Use the editor](#use-the-editor)
- [Examples](#examples)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgments)
  
# About the project
 
 ## Context
 
 ## Made with 

  This project has been made 100% in python.
 
 ## Features
 
 This program is able to solve mutliple tangrams puzzles in matters of seconds. It includes a built-in tangram editor allowing the user to create its own tangram puzzles and use the program to solve them. 
 
 You can save the results of the execution of the program. This saved data includes the position of the solved piece on the 800x700px canvas, the execution time of the program and the differents steps to complete the tangram : 
 
<p align="center">
 <img width="100%" src="https://github.com/timothewt/TangramAI/blob/master/assets/step_by_step.png" alt="Step by step tangram solving">
</p>
 
 
# Getting Started 

 ## Prerequisites
 
 In order to use the program you will need to have a python 3.X interpretor installed. 
 The required libraries are listed in the [requirements.txt](https://github.com/timothewt/TangramAI/blob/master/requirements.txt) file. 
 ## Installation 
 
# Usage 

 ## Commands
 
  A simple use of the program to save the results of the solver is to execute this line in the terminal :
  
  ```console 
  py main.py --saveData True
  ```
  
  The arguments available to use the program are : 
   - ```imagePath``` : Allow the user to use the solver on an prebuilt image (if no path is provided the program will use the built-in editor) 
   - ```saveData ```  : Allow the user to save the data of the execution in a .json file and the steps as .png files. (By default False) 
 
 ## Use the editor
 This program includes a built-in editor that lets you design your own tangram puzzles. 
 You can select the piece you want to use using the numbers keys :
 * <kbd>1</kbd> Large triangle n°1 
 * <kbd>2</kbd> Large triangle n°2
 * <kbd>3</kbd> Medium Triangle
 * <kbd>4</kbd> Parallelogram
 * <kbd>5</kbd> Square
 * <kbd>6</kbd> Small triangle n°1
 * <kbd>7</kbd> Small triangle n°2
 
 When a piece is selected you can :
  - Press <kbd>F</kbd> to flip the active piece (useful when dealing with the parallelogram) 
  - Press <kbd>R</kbd> to rotate the active piece
  - Press <kbd>N</kbd> to change the active piece's corner held by the mouse cursor
 
# Examples

# License 

# Contact 

# Acknowledgments 

 
