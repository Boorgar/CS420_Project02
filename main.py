import Room
import Algorithm

def main(): 
    room = Room.room("test.txt")

    path, score, action, map, score_history = Algorithm.Solution(room).get_solution()
    print(f"path: {path}")
    print(f"total score: {score}")
    print(f"action list: {action}")
    print(f"map history: {map}")
    print(f"score history: {score_history}")
  
if __name__=="__main__": 
    main() 