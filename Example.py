import random, math, os, sys,json
from tkinter import *
from tkinter.filedialog import *
from decimal import *
getcontext().prec = 100


from load import *
from track import *
from lr_utils import *


tk=Tk()
trk = askopenfilename(title='Select a Linerider Track', filetypes = (("trk files","*.trk"),("all files","*.*")))
tk.destroy()


#track = Track()
track = LoadTrack(trk, trk)

import pygame, math
import random
from pygame.locals import *
import time
pygame.init()
pygame.display.init()
import pygame
SIZE = (600, 600)
screen = pygame.display.set_mode(SIZE)
running = 1
screen.fill((248,248,255))
zoom = 1
FPS = 60
camera = [SIZE[0]/2,SIZE[1]/2]
clock = pygame.time.Clock()
dragging = False

colors = [
	[0,255,0],
	[0,0,255],
	[255,0,0]

]

while running:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = 0
	#pygame camera movement stuff:
	elif event.type == pygame.MOUSEBUTTONDOWN:
		start_x,start_y = 0,0
		if event.button == 1:		
			dragging = True
			old_mouse_x, old_mouse_y = event.pos
			#print(event.pos)
			offset_x = 0
			offset_y = 0
		if event.button == 4:
			zoom += zoom *0.1
		if event.button == 5:
			zoom += -(zoom *0.1)
		if event.button == 3:
			start_x,start_y = event.pos
			mouse_x,mouse_y = event.pos
			selecting = True
			true_start = (mouse_x/zoom-camera[0]),(-mouse_y/zoom-camera[1])
		#print(zoom)
	elif event.type == pygame.MOUSEBUTTONUP:
		if event.button == 1:			
			dragging = False
		if event.button == 3:
			selecting = False
			start_x,start_y = 0,0
	elif event.type == pygame.MOUSEMOTION:
		if dragging:
			mouse_x, mouse_y = event.pos
			camera[0] = camera[0] + (mouse_x - old_mouse_x) / zoom
			camera[1] = camera[1] + (mouse_y - old_mouse_y) / zoom
			old_mouse_x, old_mouse_y = mouse_x, mouse_y
	

	# Code to display lines:
	screen.fill((248,248,255))		
	for c,line in enumerate(track.lines):
		if line.type == LineType.Scenery:
			pygame.draw.line(screen, colors[line.type] ,
				[(line.point1.x + camera[0]) * zoom, (line.point1.y + camera[1]) * zoom], 
				[(line.point2.x + camera[0]) * zoom, (line.point2.y + camera[1]) * zoom],
				round(line.width*zoom))
		elif line.type == LineType.Blue:
			pygame.draw.line(screen, colors[line.type] ,
				[(line.point1.x + camera[0]) * zoom, (line.point1.y + camera[1]) * zoom], 
				[(line.point2.x + camera[0]) * zoom, (line.point2.y + camera[1]) * zoom],
				round(1*zoom))
		elif line.type == LineType.Red:
			pygame.draw.line(screen, colors[line.type] ,
				[(line.point1.x + camera[0]) * zoom, (line.point1.y + camera[1]) * zoom], 
				[(line.point2.x + camera[0]) * zoom, (line.point2.y + camera[1]) * zoom],
				round(1*zoom))
	pygame.display.flip()
	clock.tick(FPS)
