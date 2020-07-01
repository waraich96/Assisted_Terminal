#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Bahawal Waraich


from colorama import *

greenF = Fore.GREEN
redF = Fore.RED
yellowF = Fore.YELLOW
magentaF = Fore.MAGENTA
cyanF = Fore.CYAN
whiteF = Fore.WHITE
resetF = Fore.RESET


greenB = Back.GREEN
redB = Back.RED
yellowB = Back.YELLOW
magentaB = Back.MAGENTA
cyanB = Back.CYAN
whiteB = Back.WHITE
resetB = Back.RESET

bright = Style.BRIGHT
normal = Style.NORMAL



#Foreground Colour
def G(string): return green + bright + string + reset + normal 
def g(string): return green + string + resetF
def B(string): return Fore.BLUE + bright + string + resetF + normal
def b(string): return Fore.BLUE + string + resetF
def R(string): return redF + bright + string + resetF + normal
def r(string): return redF + string + resetF
def Y(string): return yellowF + bright + string + resetF + normal
def y(string): return yellowF + string + resetF
def M(string): return magentaF + bright + string + resetF + normal
def m(string): return magentaF + string + resetF
def C(string): return cyanF + bright + string + resetF + normal
def c(string): return cyanF + string + resetF
def W(string): return whiteF + bright + string + resetF + normal
def w(string): return whiteF + string + resetF 

#Background Colours
def _G(string): return greenB + bright + string + resetB + normal
def _g(string): return greenB + string + resetB
def _B(string): return Back.BLUE + bright + string + resetB + normal
def _b(string): return Back.BLUE + string + resetB
def _R(string): return redB + bright + string + resetB + normal
def _r(string): return redB + string + resetB
def _Y(string): return yellowB + bright + string + resetB + normal
def _y(string): return yellowB + string + resetB
def _M(string): return magentaB + bright + string + resetB + normal
def _m(string): return magentaB + string + resetB
def _C(string): return cyanB + bright + string + resetB + normal
def _c(string): return cyanB + string + resetB
def _W(string): return whiteB + bright + string + resetB + normal
def _w(string): return whiteB + string + resetB 