#include "../3rd/raylib/include/raylib.h"

auto main(int argc, char **argv) -> int {
    SetTraceLogLevel(LOG_NONE);
    SetConfigFlags(FLAG_WINDOW_RESIZABLE);
    InitWindow(800, 450, "Dewfall");
    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(MAGENTA);
        EndDrawing();
    }

    CloseWindow();
    return 0;
}