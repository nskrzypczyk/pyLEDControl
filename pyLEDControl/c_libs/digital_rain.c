#include <stdint.h>
#include <stdlib.h>

#define WIDTH 64
#define HEIGHT 64
#define CHANNELS 3

#define IDX(x,y,c) (((y)*WIDTH + (x))*CHANNELS + (c))

static int drops[WIDTH];

// Initialization
void init() {
    for (int i = 0; i < WIDTH; i++) {
        drops[i] = rand() % HEIGHT;
    }
}

// Fade (Trail-effect)
void fade(uint8_t *state) {
    for (int i = 0; i < WIDTH * HEIGHT * CHANNELS; i++) {
        state[i] = (uint8_t)(state[i] * 0.6);
    }
}

// Set Pixel
void set_pixel(uint8_t *state, int x, int y, uint8_t r, uint8_t g, uint8_t b) {
    if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) return;

    state[IDX(x,y,0)] = r;
    state[IDX(x,y,1)] = g;
    state[IDX(x,y,2)] = b;
}

// Main function to update the state
void step(uint8_t *state) {
    fade(state);

    for (int x = 0; x < WIDTH; x++) {
        int y = drops[x];

        set_pixel(state, x, y, 180, 255, 180);

        set_pixel(state, x, y-1, 0, 200, 0);
        set_pixel(state, x, y-2, 0, 120, 0);
        set_pixel(state, x, y-3, 0, 60, 0);

        drops[x]++;

        if (drops[x] >= HEIGHT || (rand() % 20 == 0)) {
            drops[x] = 0;
        }
    }
}