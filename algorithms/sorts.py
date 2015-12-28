import random

import pygame

from algorithms.colors import *

def draw_array(array, nome, frame):

    DISPLAY.fill(BLACK)

    aux_surf = DISPLAY_FONT.render(nome+ ' - ' + str(frame), True, WHITE)
    aux_rect = aux_surf.get_rect()
    aux_rect.topleft = (10,  10)

    DISPLAY.blit(aux_surf, aux_rect)
    for idx, value in enumerate(array):
        x = 10 + idx * 2
        pygame.draw.line(DISPLAY, WHITE, (x, WINDOW_HEIGHT-10), (x, WINDOW_HEIGHT - value - 10), 1)

    CLOCK.tick(FPS)
    pygame.display.update()

def selection_sort():
    frame = 0
    lista = list(range(0, 500))
    random.shuffle(lista)

    for i in range( len(lista) ):
        frame += 1
        draw_array(lista, 'Selection Sort', frame)
        menor = i
        for k in range( i + 1 , len(lista) ):
            if lista[k] < lista[menor]:
                menor = k
        lista[menor],lista[i]=lista[i],lista[menor]

def bubble_sort():
    frame = 0
    badList = list(range(0, 500))
    random.shuffle(badList)

    length = len(badList)

    for i in range(0,length):
        frame += 1
        draw_array(badList, 'Bubble Sort', frame)
        swapped = False
        for element in range(0, length-i-1):
            if badList[element] > badList[element + 1]:
                hold = badList[element + 1]
                badList[element + 1] = badList[element]
                badList[element] = hold
                swapped = True
        if not swapped: break

def heapsort():
    frame = 0
    lst = list(range(0, 501))
    random.shuffle(lst)

    for start in range(int((len(lst)-2)/2), -1, -1):
        frame += 1
        draw_array(lst, 'Heap Sort', frame)
        siftdown(lst, start, len(lst)-1)

    for end in range(len(lst)-1, 0, -1):
        frame += 1
        draw_array(lst, 'Heap Sort', frame)
        lst[end], lst[0] = lst[0], lst[end]
        siftdown(lst, 0, end - 1)
    return lst

def siftdown(lst, start, end):
    root = start
    while True:
        child = root * 2 + 1
        if child > end: break
        if child + 1 <= end and lst[child] < lst[child + 1]:
            child += 1
        if lst[root] < lst[child]:
            lst[root], lst[child] = lst[child], lst[root]
            root = child
        else:
            break

def gnome():
    frame = 0
    lista = list(range(0, 100))
    random.shuffle(lista)
    pivot = 0

    lista_length = len(lista)
    while pivot < lista_length - 1:
        frame += 1
        draw_array(lista, 'Gnome Sort', frame)

        if lista[pivot] > lista[pivot + 1]:
            lista[pivot + 1], lista[pivot] = lista[pivot], lista[pivot + 1]
            if pivot > 0:
                pivot -= 2
        pivot += 1



if __name__ == '__main__':
    pygame.init()

    CLOCK = pygame.time.Clock()

    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 600

    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    DISPLAY.fill(BLACK)

    pygame.font.init()
    DISPLAY_FONT = pygame.font.SysFont('couriernew', 36)

    pygame.display.set_caption("Sort Tests")

    FPS = 60

    selection_sort()
    bubble_sort()
    heapsort()
    gnome()





