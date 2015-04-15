
#include "stdafx.h"
#include <Windows.h>


#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <conio.h>
#include <string.h>


/* this bit is stollen from the Web */
void GenerateKey(int vk, BOOL bExtended) {

    KEYBDINPUT  kb = {0};
    INPUT       Input = {0};

    /* Generate a "key down" */
    if (bExtended) { kb.dwFlags  = KEYEVENTF_EXTENDEDKEY; }
    kb.wVk  = vk;
    Input.type  = INPUT_KEYBOARD;
    Input.ki  = kb;
    SendInput(1, &Input, sizeof(Input));

    /* Generate a "key up" */
    ZeroMemory(&kb, sizeof(KEYBDINPUT));
    ZeroMemory(&Input, sizeof(INPUT));
    kb.dwFlags  =  KEYEVENTF_KEYUP;
    if (bExtended) { kb.dwFlags |= KEYEVENTF_EXTENDEDKEY; }
    kb.wVk = vk;
    Input.type = INPUT_KEYBOARD;
    Input.ki = kb;
    SendInput(1, &Input, sizeof(Input));

    return;
}


int APIENTRY  WinMain(HINSTANCE hInstance,
            HINSTANCE hPrevInstance, 
            LPSTR    lpCmdLine, 
            int       cmdShow)
    {

	//printf("hello!\n");
	//GenerateKey('I', FALSE);
	GenerateKey(0x5b, FALSE); /* LWIN */
	GenerateKey(0x5C, FALSE); /* RWIN */
    //GenerateKey(0x0D, FALSE); /* enter key */

	//SendKeys::SendWait( "{VK_ENTER}" );
	//keybd_event(VkKeyScan('H'),0,0,0);
	return 0;
}