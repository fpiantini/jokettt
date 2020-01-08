# JokeTTT: a Tic Tac Toe game developed by joke

JokeTTT is a library providing tic tac toe structures useful to develop games based on several kind of players.
It was developed just for fun and to learn Python and some concepts of machine learning.

## Project setup

The project has been tested only with python3 on Ubuntu Linux. If you have python3 installed in your machine, just install the package with the usual ```pip``` command.

To avoid the usual problems with messy Python configurations (python 2 vs. 3, packages to install, etc.), conda is used for development.

For those that wants to do the same and does not know conda, this is a a quick reference:

- [TDHopper article on python environment with conda]
- [Get your computer ready for machine learning using *conda]

If you have conda installed, enter the project directory (the one with the environment.yml file) and enter the following command:

```bash
conda env create
```

This shall be done only the one time. After this the ```jokettt``` conda environment is created. It can be activated with the command:

```bash
conda activate jokettt
```

To update the conda environment every time that the ```environment.yml``` is changed, enter the command:

```bash
conda env update
```

## Demo programs

For example of simple applications that uses the jokettt classes, see the [jokettt_demo] repository.

## Credits

- A.L. Aradhya [Minimax introduction article] (and all the following) in geeksforgeeks.org for implementation of the minimax player
- T. Simonini "[An introduction to reinforcement learning]" for introduction theory on value function and for directing me to the Sutton and Barto book.

[TDHopper article on python environment with conda]: https://tdhopper.com/blog/my-python-environment-workflow-with-conda/
[Get your computer ready for machine learning using *conda]: https://towardsdatascience.com/get-your-computer-ready-for-machine-learning-how-what-and-why-you-should-use-anaconda-miniconda-d213444f36d6
[Minimax introduction article]: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
[An introduction to reinforcement learning]: https://medium.com/free-code-camp/an-introduction-to-reinforcement-learning-4339519de419

[jokettt_demo]: https://github.com/fpiantini/jokettt_demo