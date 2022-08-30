<h1 align="center">
    Minesweeper game in Python
</h1>

<h2>Quick tour</h2>
<hr>
<h3>Normal mode</h3>
<p>This is the standard game mode, in which each unrevealed cell will be displayed as a "*" symbol. When you click on a cell, it will expand. If it is a black hole, you will lose the game, otherwise, the revealed cell will show you how many mines are around it. Also, if a cell has zero neighboring black holes, it unblocks all neighbors until it reaches those with non-zero neighboring black holes.</p>
<img src="https://github.com/niksyromyatnikov/Minesweeper/blob/master/docs/img/1.png?raw=true" alt="Normal mode">
<hr>
<h3>Debug mode</h3>
<p>The debug mode is the same as a normal one, except for the board display. This mode allows you to see the content of each cell (number - empty cell with %number% adjacent black holes; H - black hole, R - for revealed cells). </p>
<img src="https://github.com/niksyromyatnikov/Minesweeper/blob/master/docs/img/2.png?raw=true" alt="Debug mode">
<p>There is no flag functionality, so after unblocking W cells, where W =  total number of cells - number of black holes, you win.</p>
<img src="https://github.com/niksyromyatnikov/Minesweeper/blob/master/docs/img/3.png?raw=true" alt="Debug mode #2">