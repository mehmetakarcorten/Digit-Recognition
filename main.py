import pygame
import sys
import math
import numpy as np
import model
import pip
from time import sleep

pip.main(['install','-r','requirements.txt'])

clamp = lambda a,b,c : min(max(a,b),c)

pygame.init()
pygame.font.init()

class Information:
	version = 0.1
	fps = 120
	windowSize = (800,600)
	pause = 0
	exit = 0

class Text(pygame.Surface):
	def __init__(self,text="~",size=6,font="Courier",bold=False,italic=False,colour="white"):
		font = pygame.font.SysFont(font,size,bold,italic)
		lines = [font.render(i,False,colour) for i in text.replace("\t","    ").split("\n")]
		height = 0
		width = 0
		for i in range(len(lines)):
			height += lines[i].get_height()
			width = max(width,lines[i].get_width())

		super(Text,self).__init__((width,height))
		self.set_colorkey((0,0,0))
		for i in range(len(lines)):
			self.blit(lines[i],(0,i*int(height/len(lines))))
	def run(self):
		return self


class Renderer:
	def __init__(self, width=800,height=600):
		self.clock = pygame.time.Clock()
		self.value = '''{
			"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,
			"7":0,"8":0,"9":0}'''
		pygame.display.set_caption("Digit Recognition")
		self.window = pygame.display.set_mode((width,height),0,16)
		icon = pygame.image.load('handwritten.png')
		pygame.display.set_icon(icon)

		self.positions = []
		self.frameArray = [[0]*28 for i in range(28)]
		self.frame = pygame.Surface((28,28))


		self.runtime(width=width,height=height)

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Information.exit = 1
			keys = pygame.key.get_pressed()
			mouse = pygame.mouse.get_pressed()

			if keys[pygame.K_ESCAPE]:
				Information.pause = 1-Information.pause
			if not Information.pause:
				if mouse[0]:
					pos = list(pygame.mouse.get_pos())
					pos[0] = int(pos[0]*(28/800))
					pos[1] = int(pos[1]*(28/600))
					if pos not in self.positions: self.positions.append(pos)
				else:
					self.value = predictModel.predict(array=np.array([self.frameArray]))
				if keys[pygame.K_c]:
					self.frameArray = [[0]*28 for i in range(28)]
					self.positions = []
				

	def runtime(self,width,height):
		while not Information.exit:
			if not Information.pause:
				self.frame.fill((0,0,0))

				for i in self.positions:
					self.frame.set_at(i,(255,255,255))

				for y in range(28):
					for x in range(28):
						col = self.frame.get_at((x,y))
						if col == (255,255,255,255):
							self.frameArray[y][x] = 255


				scaled = pygame.transform.scale(self.frame,(width,height))
				self.window.blit(scaled,(0,0))
				self.value = self.value.replace(",","\n")

				txt = Text(text=f"{self.value}",size=15).run()
				self.window.blit(txt,(800-(txt.get_width()),0))

			self.events()

			pygame.display.update()
			self.clock.tick(Information.fps)
			pygame.display.flip()

		predictModel.close()
		pygame.quit()
		sys.exit()

if __name__ == "__main__":
	
	predictModel = model.Model()
	render = Renderer(Information.windowSize[0],Information.windowSize[1])
