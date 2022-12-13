import random

class cell:
    def __init__(self,x,y):
        #Each cell object has a sense of position in the 2D Array 
        #that represents "world" in simulateWorld class
        self.x_pos = x
        self.y_pos = y
        #self.character is the character to be displayed
        self.character = 'x'
        #variable that helps identify with a string, could easily
        #use int, float or other assignment that can be compared
        #but used string for readability 
        self.identifier = "Basic Cell"
        
    def updateCoordinates(x,y):
        x_pos = x
        y_pos = y
    
class life(cell):
    #life class inherits all cell attributes but is unique as a child
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.character = "L"
        self.identifier = "Life"
        
    def move(self):
        #Move method that the life object has access to
        #A random number between one and four is chosen
        random_direction = random.randint(1,4)
        
        #random_direction containing n anywhere from (1,4)
        #n is associated with a certain graphical direction
        #Inversed directions as this 2D Array "world" navigates differently
        #than a 2D graph
        if random_direction == 1:
            #Move south
            self.y += 1
            print(f'moved south from {self.y-1} to {self.y}')
        if random_direction == 2:
            #Move north 
            self.y -= 1
            print(f'moved north from {self.y+1} to {self.y}')
        if random_direction == 3:
            #Move west 
            self.x += 1
            print(f'moved east from {self.x-1} to {self.x}')
        if random_direction == 4:
            #Move east
            self.x -= 1
            print(f'moved west from {self.x+1} to {self.x}')
        #all of these conditionals use a print statement to help verify
        #the direction of the "life" object
    
    def withinRange(self,target):
        #method that the life object has access to
        #returns boolean depending on the location
        #of fruit. if it exists within
        #range of fruit n-1 or n+1 with the other axis being equal
        if (self.x + 1 == target.x or self.x - 1 == target.x) and self.y ==target.y:
            return True
        elif(self.y+1 == target.y or self.y -1 == target.y) and self.x == target.x:
            return True
        return False
        
class fruit(cell):
    #fruit object 
    def __init__(self, x, y):
        super().__init__(x, y)
        self.character = "A"
        self.identifier = "Fruit"

class simulate_world:
    #2DArray representing world
    world = []
    #value to track 
    win = False
    #count variable for each world update()
    global_count = 0
    
    def __init__(self,n):
        #constructor that populates array n length
        #then spawns life & fruit on the map
        self.populate(n)
        self.spawn_life()   
        self.spawn_fruit()   
        
    def populate(self,n):
        #populates world with parameter n rows
        for i in range(n):
            self.world.append([])
        #for n columns fill row with blank 'terrain'
        for i in range(len(self.world)):
            for j in range(n*2):
                #n*2 to expand the range of life object on the map
                cell_to_populate = cell(j,i)
                self.world[i].append(cell_to_populate)
    
    def spawn_life(self):
        #spawns a random life cell at [x][y] in world
        random_x_value = random.randint(0,len(self.world)-1)
        random_y_value = random.randint(0,len(self.world)-1)
        
        #tracking initial values of life on the map.
        #used to verify location
        print(f'spawn_life(): @ x : {random_x_value}spawn_life(): @ y : {random_y_value}')
        
        #this line of code creates a new life object at the randomly selected
        #coordinates
        ###fun fact: array[i][j] does not correlate to (x,y) coordinates pairs.
        ###it's reversed! i almost became apoplectic because of this small error
        ###:o)
        self.world[random_y_value][random_x_value] = life(random_x_value,random_y_value)
        
    def spawn_fruit(self):
        #spawns a random fruit cell at [x][y] in world
        random_x_value = random.randint(0,len(self.world)-1)
        random_y_value = random.randint(0,len(self.world)-1)
        
        #checking to see if location equals L so it doesn't spawn on top
        #which would cause the game to break almost before it begins
        if(self.world[random_y_value][random_x_value].character == "L"):
            #cheeky bit of recursion ;)
            self.spawn_fruit()
        else:
            #same structure as spawn_life segment. just reversing order and verifying coordinates
            self.world[random_y_value][random_x_value] = fruit(random_x_value,random_y_value)
            print(f'spawn_fruit(): @x : {random_x_value} spawn_fruit(): @y : {random_y_value}')
           

    def display(self):
        #OK so basically i don't feel like explaining this one.
        #standard boilerplate toString that is modified slightly
        #displays reflecting that of a graph for the self.world 2D array
        
        #master string returned at end of function 
        s = ""
        
        for i in range(len(self.world)):
            #string per row
            str = ""
            for j in range(len(self.world[i])):
                #adding character to string for basic layout
                str+=f"{self.world[i][j].character}"
            #string magicks - just adding newline
            s+=str+" "+"\n"
        return(s)
    
    def update(self):
        #update self.world by one tick,
        
        #identified fruit and life to be assigned after checking self.world
        identified_life = None
        identified_fruit = None
        for i in range(len(self.world)):
            #you get the idea basic traversal of 2D array
            for j in range(len(self.world[0])):
                #since the objects have a sense of position
                #we can easily identify and store positon vlaues
                # for life and fruit
                if self.world[i][j].identifier == "Life":
                    identified_life = self.world[i][j]
                    identified_life.x = j
                    identified_life.y = i
                if self.world[i][j].identifier == "Fruit":
                    identified_fruit = self.world[i][j]
                    identified_fruit.x = j
                    identified_fruit.y = i
        #pass these varaibles to life_logic
        
        self.life_logic(identified_life,identified_fruit) 
        
        
        #count++ .. not in python. WHY? just to be different? 
        #and contrarian? no python. staticly typed languages 
        #that aren't interpreted and take forever to run
        #are better anyways
        self.global_count += 1
        
        
    def life_logic(self,life,target):
        #every tick, life has the option to either move or eat fruit
        #if it is within the range of fruit it simply eats it
        #if not, move the life in a random direction
        if life.withinRange(target):
            #PER each tick, for life find any fruit within
            #range of (target), if so eat, and win 
            self.win = True
        else:
            #pass through to move method in life -- see above in life class
            life.move()
            
            
            for i in range(len(self.world)):
                for j in range(len(self.world[0])):
                    if self.world[i][j].identifier == "Life":
                        #quickly grab and identify if cell at i,j is life
                        #if so, first set it to a variable so it can be
                        #reused, and then set cell i,j to a new cell
                        #instance that is NOT alive
                        tagged_life = self.world[i][j]
                        self.world[i][j] = cell(j,i)
                        #verifies that the life's location is within
                        #the bounds of the array according to 
                        ## 0 <= x < len(self.world) 
                        if(tagged_life.y > len(self.world)-1):
                            tagged_life.y -= 1
                        if(tagged_life.x > len(self.world[0])-1):
                            tagged_life.x -= 1
                        if(tagged_life.x < 0):
                            tagged_life.x += 1
                        if(tagged_life.y < 0):
                            tagged_life.y += 1
                        #after life.move(), check new coordiantes and 
                        #fill self.world accordingly. reverse x,y
                        self.world[tagged_life.y][tagged_life.x] = tagged_life
                        print(f'index of life at {tagged_life.x},{tagged_life.y}')
                        
                        #!!
                        #OKAY... i can explain. this is the very last piece of code
                        #i could not, for the life of me, figure out how to break
                        #from this loop immediately, break keyword did not exit entire looping structure
                        #!!
                        
                        #so why not return 0??? works like a charm :)
                        return 0
                    
