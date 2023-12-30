import Room
import Algorithm

def main(): 
    room = Room.room("test.txt")

    path, score = Algorithm.Solution(room).get_solution()
    print(f"path: {path}")
    print(f"total score: {score}")
  
if __name__=="__main__": 
    main() 