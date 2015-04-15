// RestlessLeg.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>



//#define WIN32_LEAN_AND_MEAN
//#define _WIN32_WINNT 0x0500

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <conio.h>
#include <string.h>
#include <windows.h>


#define X 123
#define Y 123
#define SCREEN_WIDTH 1024
#define SCREEN_HEIGHT 800


void MouseSetup(INPUT *buffer)
{
    buffer->type = INPUT_MOUSE;
    buffer->mi.dx = (0 * (0xFFFF / SCREEN_WIDTH));
    buffer->mi.dy = (0 * (0xFFFF / SCREEN_HEIGHT));
    buffer->mi.mouseData = 0;
    buffer->mi.dwFlags = MOUSEEVENTF_ABSOLUTE;
    buffer->mi.time = 0;
    buffer->mi.dwExtraInfo = 0;
}


void MouseMoveAbsolute(INPUT *buffer, int x, int y)
{
    buffer->mi.dx = (x * (0xFFFF / SCREEN_WIDTH));
    buffer->mi.dy = (y * (0xFFFF / SCREEN_HEIGHT));
    buffer->mi.dwFlags = (MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE);

    SendInput(1, buffer, sizeof(INPUT));
}

void MouseMoveDummy(INPUT *buffer, int x, int y)
{
	//POINT currentCursorPos;
	//GetCursorPos(&currentCursorPos);
	//printf("px = %d\n", currentCursorPos.x);
	//printf("py = %d\n", currentCursorPos.y);

	//printf("mouse dx = %d\n", buffer->mi.dx);
	buffer->mi.dx = 1;
    //buffer->mi.dy = (currentCursorPos.y * (0xFFFF / SCREEN_HEIGHT));
    //buffer->mi.dwFlags = (MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE);
    buffer->mi.dwFlags = (MOUSEEVENTF_MOVE);
    SendInput(1, buffer, sizeof(INPUT));

    Sleep(10);

    buffer->mi.dx = -1;
   // buffer->mi.dy = (currentCursorPos.y * (0xFFFF / SCREEN_HEIGHT));
//    buffer->mi.dwFlags = (MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE);
    buffer->mi.dwFlags = (MOUSEEVENTF_MOVE);
    SendInput(1, buffer, sizeof(INPUT));

}

void MouseClick(INPUT *buffer)
{
    buffer->mi.dwFlags = (MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_LEFTDOWN);
    SendInput(1, buffer, sizeof(INPUT));

    Sleep(10);

    buffer->mi.dwFlags = (MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_LEFTUP);
    SendInput(1, buffer, sizeof(INPUT));
}





/*int _tmain(int argc, _TCHAR* argv[])
{
	//printf("hello!");


    INPUT buffer[1];

    MouseSetup(&buffer[0]);

    //MouseMoveAbsolute(&buffer[0], X, Y);
    MouseMoveDummy(&buffer[0], X, Y);
    //MouseClick(&buffer[0]);

	while(1) {
		//printf("move\n");
		MouseMoveDummy(&buffer[0], X, Y);

		Sleep(1000*60); //1min
	}
    
	return 0;
}*/

int APIENTRY  WinMain(HINSTANCE hInstance,
            HINSTANCE hPrevInstance, 
            LPSTR    lpCmdLine, 
            int       cmdShow)
    {
    INPUT buffer[1];

    MouseSetup(&buffer[0]);

    //MouseMoveAbsolute(&buffer[0], X, Y);
    MouseMoveDummy(&buffer[0], X, Y);
    //MouseClick(&buffer[0]);

	while(1) {
		//printf("move\n");
		MouseMoveDummy(&buffer[0], X, Y);

		Sleep(1000*60); //1min
	}
    
	return 0;
}