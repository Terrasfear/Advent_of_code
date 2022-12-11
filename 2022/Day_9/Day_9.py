class Snake:
    s_pos = [0, 0]

    grid_limits = [[0, 5], [0, 5]]
    trail = set()

    def __init__(self, snake_length=2):
        self.snake = [self.s_pos.copy() for _ in range(snake_length)]

        self.trail.add(tuple(self.snake[-1]))

    def up(self):
        self.snake[0][0] = self.snake[0][0] + 1
        self.check_tail()
        self.check_limits()

    def down(self):
        self.snake[0][0] = self.snake[0][0] - 1
        self.check_tail()
        self.check_limits()

    def right(self):
        self.snake[0][1] = self.snake[0][1] + 1
        self.check_tail()
        self.check_limits()

    def left(self):
        self.snake[0][1] = self.snake[0][1] - 1
        self.check_tail()
        self.check_limits()

    def check_limits(self):
        if self.snake[0][0] < self.grid_limits[0][0]:
            self.grid_limits[0][0] = self.snake[0][0]
        if self.snake[0][0] > self.grid_limits[0][1]:
            self.grid_limits[0][1] = self.snake[0][0]
        if self.snake[0][1] < self.grid_limits[1][0]:
            self.grid_limits[1][0] = self.snake[0][1]
        if self.snake[0][1] > self.grid_limits[1][1]:
            self.grid_limits[1][1] = self.snake[0][1]

    def check_tail(self):
        for head_idx in range(len(self.snake)-1):
            self.check_section(head_idx)
        self.trail.add(tuple(self.snake[-1]))

    def check_section(self, head_idx):
        # within 1 spot
        if self.snake[head_idx+1][0] in range(self.snake[head_idx][0]-1, self.snake[head_idx][0]+2) and self.snake[head_idx+1][1] in range(self.snake[head_idx][1]-1, self.snake[head_idx][1]+2):
            # print("within 1")
            return

        if self.snake[head_idx+1][0] < self.snake[head_idx][0]:
            # print("head north")
            ns_step = 1
        elif self.snake[head_idx+1][0] > self.snake[head_idx][0]:
            # print("head south")
            ns_step = -1
        else:
            ns_step = 0

        if self.snake[head_idx+1][1] < self.snake[head_idx][1]:
            # print("head east")
            ew_step = 1
        elif self.snake[head_idx+1][1] > self.snake[head_idx][1]:
            # print("head west")
            ew_step = -1
        else:
            ew_step = 0

        self.snake[head_idx+1][0] = self.snake[head_idx+1][0] + ns_step
        self.snake[head_idx+1][1] = self.snake[head_idx+1][1] + ew_step


    def plot(self):
        # make grid
        grid = [['.']*len(range(self.grid_limits[1][0], self.grid_limits[1][1]+1)) for _ in range(self.grid_limits[0][0], self.grid_limits[0][1]+1)]

        # place trail
        for step in self.trail:
            grid[self.grid_limits[0][1] - step[0]][-self.grid_limits[1][0] + step[1]] = '#'

        # place start
        grid[self.grid_limits[0][1] - self.s_pos[0]][-self.grid_limits[1][0] + self.s_pos[1]] = 's'

        # place snake
        for idx, section in reversed(list(enumerate(self.snake))):
            if idx == 0:
                mark = 'H'
            elif idx == len(self.snake)-1:
                mark = "T"
            else:
                mark = idx

            grid[self.grid_limits[0][1] - section[0]][-self.grid_limits[1][0] + section[1]] = mark

        for row in grid:
            for elem in row:
                print(f"{elem}", end='')
            print('')
        print('')


file = open("input", 'r')
lines = file.readlines()

snake = Snake(10)

snake.check_tail()
snake.plot()

for line in lines:
    direction = line[0]
    number = int(line[2:-1])

    print(line)

    for _ in range(number):
        if direction == "R":
            snake.right()
        if direction == "L":
            snake.left()
        if direction == "U":
            snake.up()
        if direction == "D":
            snake.down()

snake.plot()

print(f"Q9: {len(snake.trail)}")