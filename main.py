import Room
import Algorithm
import Graphic

def main(): 
    # room = Room.room("test.txt")

    # path, score, action, map, score_history = Algorithm.Solution(room).get_solution()
    # print(f"path: {path}")
    # print(f"total score: {score}")
    # print(f"action list: {action}")
    # # print(f"map history: {map}")
    # print(f"score history: {score_history}")
    # print(len(map))
    # print(len(action))
    # # print(len(path))
    # print(len(score_history))
    # c = 0
    # for i in action:
    #     if "Turn" in i:
    #         continue
    #     c += 1
    # print(c)
    
    graphic = Graphic.Graphic()
    graphic.run()
    
if __name__=="__main__": 
    main() 