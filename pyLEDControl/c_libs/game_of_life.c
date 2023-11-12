#include <stdio.h>
#include <stdlib.h>

int** create_grid(int rows, int cols) {
    int** grid = (int**)malloc(rows * sizeof(int*));
    for (int i = 0; i < rows; i++) {
        grid[i] = (int*)malloc(cols * sizeof(int));
        for (int j = 0; j < cols; j++) {
            grid[i][j] = rand() % 2;
        }
    }
    return grid;
}

void free_grid(int** grid, int rows) {
    for (int i = 0; i < rows; i++) {
        free(grid[i]);
    }
    free(grid);
}

int count_neighbors(int** grid, int rows, int cols, int x, int y) {
    int count = 0;
    for (int i = -1; i <= 1; i++) {
        for (int j = -1; j <= 1; j++) {
            int ni = x + i;
            int nj = y + j;
            if (ni >= 0 && ni < rows && nj >= 0 && nj < cols && !(i == 0 && j == 0)) {
                count += grid[ni][nj];
            }
        }
    }
    return count;
}

int** update_grid(int** grid, int rows, int cols) {
    int** newGrid = create_grid(rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            int neighbors = count_neighbors(grid, rows, cols, i, j);
            if (grid[i][j] == 1) {
                if (neighbors < 2 || neighbors > 3) {
                    newGrid[i][j] = 0;
                } else {
                    newGrid[i][j] = 1;
                }
            } else {
                if (neighbors == 3) {
                    newGrid[i][j] = 1;
                } else {
                    newGrid[i][j] = 0;
                }
            }
        }
    }
    return newGrid;
}