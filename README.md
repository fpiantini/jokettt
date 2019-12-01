# JokeTTT: a Tic Tac Toe game developed by joke

JokeTTT is a tic tac toe game developed just for fun and to learn Python and some concepts of machine learning.

## Project setup

The project has been tested only with python3 on Ubuntu Linux. If you have python3 installed in your machine, just try the code entering the command:

```bash
./play.py
```

To avoid the usual problems with messy Python configurations (python 2 vs. 3, packages to install, etc.), I use conda during development.

For those that wants to do the same and does not know conda, this is a a quick reference:

- [TDHopper article on python environment with conda]
- [Get your computer ready for machine learning using *conda]

If you have conda installed, enter the project directory (the one with the environment.yml file) and enter the following command:

```bash
conda env create
```

Then activate the jokettt conda environment with the command:

```bash
conda activate jokettt
```

## Credits

- A.L. Aradhya [Minimax introduction article] (and all the following) in geeksforgeeks.org for implementation of the minimax player




[TDHopper article on python environment with conda]: https://tdhopper.com/blog/my-python-environment-workflow-with-conda/
[Get your computer ready for machine learning using *conda]: https://towardsdatascience.com/get-your-computer-ready-for-machine-learning-how-what-and-why-you-should-use-anaconda-miniconda-d213444f36d6
[Minimax introduction article]: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/