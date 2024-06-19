import pygame
import random
import math

pygame.init()

class DrawInformation:# CONTAINS THE INFORMATION ABOUT THE SCREEN SIZE AND COLOUR OF THE THINGS USED IN PYGAME
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    RANDOM_C=random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)
    BACKGROUND_COLOR = (random.randint(1, 255),random.randint(0, 255),random.randint(0, 255))

    GRADIENTS = [
        (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)),
        (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    ]

    FONT= pygame.font.SysFont('comicsans',20) 
    LARGE_FONT= pygame.font.SysFont('comicsans',30) 

    SIDE_PAD = 100  # TOTAL PADDING ON RIGHT AS WEEL AS LEFT
    TOP_PAD = 150 

    def __init__(self, width, height, lst):
        self.height = height
        self.width = width

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round(self.width - self.SIDE_PAD) / len(lst)
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val)
        )
        self.start_x = self.SIDE_PAD // 2

# SETTING THE DISPLAY
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    
    title = draw_info.LARGE_FONT.render(f"{algo_name}-{'Ascending' if ascending else 'Decending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))


    controls = draw_info.FONT.render("R - RESET | SPACE - Start Sorting | A - Acending | D - Decending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | Q - Quick Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    merge = draw_info.FONT.render("M - Merge Sort", 1, draw_info.BLACK)
    draw_info.window.blit(merge, (draw_info.width/2 - sorting.get_width()/2+250, 105))

    draw_list(draw_info)
    pygame.display.update()

# FOR THE RECTANGLES DRAWN AND RESETTING THE SCREEN AFTER EACH PASS
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst= draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2,draw_info.TOP_PAD, draw_info.width-draw_info.SIDE_PAD, draw_info.height- draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x= draw_info.start_x + i * draw_info.block_width
        y=draw_info.height- (val-draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i%3]
        if i  in color_positions:
            color= color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x,y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update() 
        
# FOR GENERATING RANDOM LIST OF NUMBERS
def generate_starting_list(n, min_val, max_val):
    lst=[]
    for _ in range(n):
        val=random.randint(min_val,max_val)
        lst.append(val)

    return lst

# SORTING METHODS
def bubble_sort(draw_info, ascending = True):
    lst= draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-i-1):
            num1=lst[j]
            num2=lst[j+1]

            if(num1>num2 and ascending) or (num1<num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1],lst[j]
                draw_list(draw_info, {j:draw_info.GREEN, j+1: draw_info.RED},True)
                yield True
    return lst     
       
def insertion_sort(draw_info, ascending= True):
    lst = draw_info.lst
    
    for i in range(1,len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            decending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not decending_sort:
                break
            lst[i]= lst[i-1]
            i=i-1
            lst[i]= current
            draw_list(draw_info,{i-1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    
    for i in range(n - 1):
        extreme_index = i
        
        for j in range(i + 1, n):
            if (ascending and lst[j] < lst[extreme_index]) or (not ascending and lst[j] > lst[extreme_index]):
                extreme_index = j

        lst[i], lst[extreme_index] = lst[extreme_index], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, extreme_index: draw_info.RED}, True)
        yield True
    
    return lst

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def partition(low, high):
        pivot = lst[high]
        i = low - 1

        for j in range(low, high):
            if (ascending and lst[j] <= pivot) or (not ascending and lst[j] >= pivot):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True

        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
        yield True

        return i + 1

    def quicksort_recursive(low, high):
        if low < high:
            pivot_index = yield from partition(low, high)
            yield from quicksort_recursive(low, pivot_index - 1)
            yield from quicksort_recursive(pivot_index + 1, high)

    yield from quicksort_recursive(0, len(lst) - 1)
    return lst

def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge(left, right, l_start):
        merged = []
        while left and right:
            if (ascending and left[0] <= right[0]) or (not ascending and left[0] >= right[0]):
                merged.append(left.pop(0))
            else:
                merged.append(right.pop(0))

        merged.extend(left if left else right)
        for i, val in enumerate(merged):
            lst[l_start + i] = val
            draw_list(draw_info, {l_start + i: draw_info.GREEN}, True)
            yield True

        return merged

    def merge_sort_recursive(start, end):
        if end - start <= 1:
            return lst[start:end]

        mid = (start + end) // 2
        left_half = yield from merge_sort_recursive(start, mid)
        right_half = yield from merge_sort_recursive(mid, end)
        
        merged = yield from merge(left_half, right_half, start)
        return merged

    lst[:] = yield from merge_sort_recursive(0, len(lst))
    return lst


# MAIN DRIVER CODE
def main():
    run = True
    clock=pygame.time.Clock()

    n=50
    min_val=0
    max_val=100

    lst=generate_starting_list(n,min_val,max_val)
    draw_info=DrawInformation(1000,600,lst)
    sorting = False
    ascending = True


    sorting_algorithm = bubble_sort
    sorting_algo_name="Bubble Sort"
    sorting_algorithm_generator= None
    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else: 
            draw(draw_info, sorting_algo_name, ascending)

        draw(draw_info, sorting_algo_name, ascending)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type != pygame.KEYDOWN:
                continue
            # KEY SETTING
            if event.key == pygame.K_r:
                lst = generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm= insertion_sort
                sorting_algo_name="Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm= bubble_sort
                sorting_algo_name="Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm= selection_sort
                sorting_algo_name="Selection Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm= quick_sort
                sorting_algo_name="Quick Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm= merge_sort
                sorting_algo_name="Merge Sort"
            
    pygame.quit()


if __name__=="__main__":
    main()


