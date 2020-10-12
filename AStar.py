'''
    goal state is
        1 | 2 | 3 
        ---------
        8 | _ | 4
        ---------
        7 | 6 | 5

    _: in this case, is represented by 9
'''

class State:
    def __init__(self, state = 0, array = []):
        self.state = state
        if state == 0:
            self.setState(array)

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, obj):
        return isinstance(obj, State) and obj.state == self.state

    def setState(self, array):
        """
        sau đó chuyển từ array (lưu các số trong state) sang state
        ex: array = [1,2,3,4,5,6] -> state = 123456
        """
        for i in array:
            self.state = self.state * 10 + i

    def getArrayFromState(self):
        """
        chuyển từ state sang array (mảng lưu các số trong state)
        ex: state = 123456 -> array = [1,2,3,4,5,6]
        """
        state = self.state
        array = []
        while state != 0:
            array.insert(0, state % 10)
            state = state // 10 
        return array

    def getZeroPos(self):
        """
        trả về vị trí của ô trống trong mảng 1 chiều
        """
        array = self.getArrayFromState()
        zeroPos = None
        for i in range(len(array)):
            if array[i] == 9:
                zeroPos = self.convert1Dto2D(i)
                break
        return zeroPos

    def convert1Dto2D(self, index):
        """
        chuyển đổi vị trí trên mảng 1 chiều thành vị trí trên mảng 2 chiều kích thước 3*3
        ex: 7 -> (2,1)
        """
        return (index // 3, index % 3)

    def convert2Dto1D(self, pos):
        """
        chuyển đổi vị trí trên mảng 2 chiều kích thước 3*3 thành vị trí trên mảng 1 chiều 
        ex: (2,1) -> 7
        """
        return pos[0] * 3 + pos[1]

    def swapAndReturnState(self, pos1, pos2):
        """
        swap 2 vị trí pos1 và pos2
        trả về 1 array mới
        """
        index1 = self.convert2Dto1D(pos1)
        index2 = self.convert2Dto1D(pos2)
        array = self.getArrayFromState()

        temp = array[index1]
        array[index1] = array[index2]
        array[index2] = temp

        return State(array=array)

    def getDirection(self):
        """
        trả về list trạng thái, trong đó, ô trống swap vị trí với 1 trong 4 ô xung quanh nó
        """
        array = self.getArrayFromState()
        zeroPos = self.getZeroPos()

        rs = []
        if zeroPos[0] > 0:
            rs.append(self.swapAndReturnState(zeroPos, (zeroPos[0] - 1, zeroPos[1])))
        if zeroPos[0] < 2:
            rs.append(self.swapAndReturnState(zeroPos, (zeroPos[0] + 1, zeroPos[1])))
        if zeroPos[1] > 0:
            rs.append(self.swapAndReturnState(zeroPos, (zeroPos[0], zeroPos[1] - 1)))
        if zeroPos[1] < 2:
            rs.append(self.swapAndReturnState(zeroPos, (zeroPos[0], zeroPos[1] + 1)))

        return rs

    def printState(self):
        array = self.getArrayFromState()

        count = 0
        for i in array:
            if i == 9:
                print('_', end = ' ')
            else:
                print(i, end = ' ')
            count += 1
            if count == 3:
                count = 0
                print()

class SolveEightPuzzle:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def getHeuristic2(self, state):
        """
        nhận vào 1 state
        trả về heuristic (là tổng delta(x,y)) của state đó
        tại ô (x,y): nếu ô đó đang ở đúng vị trí so với goal thì delta(x,y) = 0, ngược lại bằng 1
        """
        goalArray = self.goal.getArrayFromState()
        stateArray = state.getArrayFromState()
        h = 0

        for i in range(len(goalArray)):
            if goalArray[i] != stateArray[i]:
                h += 1
        return h

    def getHeuristic1(self, state):
        """
        nhận vào 1 state
        trả về heuristic (là khoảng cách Manhattan) cho state đó
        """
        goalArray = self.goal.getArrayFromState()
        stateArray = state.getArrayFromState()
        h = 0

        for i in range(len(goalArray)):
            for j in range(len(stateArray)):
                if stateArray[j] == goalArray[i]:
                    curPos = self.goal.convert1Dto2D(j)
                    goalPos = self.goal.convert1Dto2D(i)
                    h += abs(curPos[0] - goalPos[0]) + abs(curPos[1] - goalPos[1])
        return h

    def getMinState(self, d, isVisited):
        """
        nhận vào 1 mảng d với d[i] = số bước đi từ trạng thái đầu tiên đến trạng thái i
        trả về 1 trạng thái với d[i] + heuristic(i) min. trong đó heuristic(i) đánh giá độ gần với đích của trạng thái i
        """
        min = 1000
        keyMin = None
        for state in d:
            if d[state] + self.getHeuristic2(state) < min and isVisited.get(state) is None:
                min = d[state] + self.getHeuristic2(state)
                keyMin = state
        return keyMin

    def AStar(self):
        isVisited = {}
        parent = {self.start: -1}
        d = {self.start: 0}

        current = self.start
        while current != self.goal:
            current = self.getMinState(d, isVisited)
            isVisited[current] = True

            newPos = current.getDirection()
            for pos in newPos:
                if pos is not None and isVisited.get(pos) is None:
                    if d.get(pos) is None or d[pos] > d[current] + 1:
                        d[pos] = d[current] + 1
                        parent[pos] = current

        self.printPath(parent, self.goal)

    def printPath(self, parent, goal):
        """
        sử dụng con trỏ quay lui để in ra đường đi
        """
        if parent[goal] == -1:
            goal.printState()
            print()
            return
        self.printPath(parent, parent[goal])
        goal.printState()
        print()


def main():
    s = SolveEightPuzzle(State(state=521743986), State(state=123456789))
    s.AStar()

if __name__ == '__main__':
    main()

