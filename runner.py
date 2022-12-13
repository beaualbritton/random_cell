import time
import cell
if __name__ == "__main__":
    running = True
    while running:
        world_running = True
        time.sleep(1)
        hello = input("Welcome to Random Cell Simulation. "
        "Press the Enter to continue. Enter E to exit")
        if hello.lower() == 'e':
            break
        size = int(input("Please enter world size. " 
        "Note, the bigger the world, the longer a simulation takes: "))
        this = cell.simulate_world(size)
        print(this)
        print(this.display())
        while world_running:
            print(this.display())
            this.update()
            if this.win:
                print(f"Life has found the fruit."
                f"This run took {this.global_count} repetitions at length {size}")
                time.sleep(5)
                world_running = False
            time.sleep(0.5)
        answer = input("Continue? Y/N")
        if answer.lower == 'n':
            break
            
        
            
            
            
            
            
            