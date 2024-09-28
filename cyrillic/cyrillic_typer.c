#include <windows.h>
#include <stdio.h>
#include <stdbool.h>

#define BUFFER_SIZE 256

HHOOK keyboardHook;
bool cyrillicMode = false;
char inputBuffer[BUFFER_SIZE] = {0};
int bufferIndex = 0;

// Cyrillic mapping
const char* cyrillicMap[] = {
    "a", "а", "b", "б", "v", "в", "g", "г", "d", "д", "e", "е", "zh", "ж",
    "z", "з", "i", "и", "j", "й", "k", "к", "l", "л", "m", "м", "n", "н",
    "o", "о", "p", "п", "r", "р", "s", "с", "t", "т", "u", "у", "f", "ф",
    "h", "х", "ts", "ц", "ch", "ч", "sh", "ш", "sht", "щ", "y", "ы", "yu", "ю",
    "ya", "я", "e", "э", "yo", "ё", NULL
};

void ToggleCyrillicMode() {
    cyrillicMode = !cyrillicMode;
    char* message = cyrillicMode ? "Cyrillic input is ON" : "Cyrillic input is OFF";
    MessageBoxA(NULL, message, "Cyrillic Typer", MB_OK | MB_ICONINFORMATION);
}

void SendUnicodeChar(wchar_t ch) {
    INPUT input = {0};
    input.type = INPUT_KEYBOARD;
    input.ki.wScan = ch;
    input.ki.dwFlags = KEYEVENTF_UNICODE;
    SendInput(1, &input, sizeof(INPUT));

    input.ki.dwFlags |= KEYEVENTF_KEYUP;
    SendInput(1, &input, sizeof(INPUT));
}

void ProcessBuffer() {
    if (bufferIndex == 0) return;

    for (int i = 0; i < bufferIndex; i++) {
        bool found = false;
        for (int j = 0; cyrillicMap[j] != NULL; j += 2) {
            if (strncmp(inputBuffer + i, cyrillicMap[j], strlen(cyrillicMap[j])) == 0) {
                SendUnicodeChar(cyrillicMap[j + 1][0]);
                i += strlen(cyrillicMap[j]) - 1;
                found = true;
                break;
            }
        }
        if (!found) {
            SendUnicodeChar(inputBuffer[i]);
        }
    }

    bufferIndex = 0;
}

LRESULT CALLBACK KeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode >= 0) {
        KBDLLHOOKSTRUCT* kbdStruct = (KBDLLHOOKSTRUCT*)lParam;
        
        if (wParam == WM_KEYDOWN || wParam == WM_SYSKEYDOWN) {
            if ((kbdStruct->vkCode == VK_SPACE) && (GetAsyncKeyState(VK_LWIN) & 0x8000)) {
                ToggleCyrillicMode();
                return 1;
            }

            if (cyrillicMode) {
                if (kbdStruct->vkCode == VK_SPACE) {
                    ProcessBuffer();
                    return 1;
                } else if (kbdStruct->vkCode == VK_BACK) {
                    if (bufferIndex > 0) bufferIndex--;
                    return 1;
                } else if ((kbdStruct->vkCode >= 'A' && kbdStruct->vkCode <= 'Z') || 
                           (kbdStruct->vkCode >= '0' && kbdStruct->vkCode <= '9')) {
                    if (bufferIndex < BUFFER_SIZE - 1) {
                        inputBuffer[bufferIndex++] = tolower(kbdStruct->vkCode);
                    }
                    return 1;
                }
            }
        }
    }
    return CallNextHookEx(keyboardHook, nCode, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    keyboardHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardProc, NULL, 0);
    if (keyboardHook == NULL) {
        MessageBoxA(NULL, "Failed to install keyboard hook!", "Error", MB_ICONERROR);
        return 1;
    }

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    UnhookWindowsHookEx(keyboardHook);
    return 0;
}
