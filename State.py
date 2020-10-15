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
        self.f = 0
        self.g = 10000
        if state == 0:
            self.setState(array)

    def getHeuristic2(self, goal):
        """
        nhận vào goal
        trả về heuristic (là tổng delta(x,y)) của state hiện tại
        tại ô (x,y): nếu ô đó đang ở đúng vị trí so với goal thì delta(x,y) = 0, ngược lại bằng 1
        """
        goalArray = goal.getArrayFromState()
        stateArray = self.getArrayFromState()
        h = 0

        for i in range(len(goalArray)):
            if goalArray[i] != stateArray[i]:
                h += 1
        return h

    def getHeuristic1(self, goal):
        """
        nhận vào goal
        trả về heuristic (là khoảng cách Manhattan) cho state hiện tại
        """
        goalArray = goal.getArrayFromState()
        stateArray = self.getArrayFromState()
        h = 0

        for i in range(len(goalArray)):
            for j in range(len(stateArray)):
                if stateArray[j] == goalArray[i]:
                    curPos = goal.convert1Dto2D(j)
                    goalPos = goal.convert1Dto2D(i)
                    h += abs(curPos[0] - goalPos[0]) + abs(curPos[1] - goalPos[1])
        return h

    def setF(self, g, goal, kind=1):
        """
        nhận vào goal state
        set self.f: tổng của heuristic (khoảng cách Manhattan) và số bước để đi đến trạng thái đó tính từ start
        f(x) = g(x) + h(x)
        h(x) có thể tính bằng 2 cách: kind = 1 or kind = 2
        """
        h = 0
        self.g = g
        if kind == 1:
            h = self.getHeuristic1(goal)
        else:
            h = self.getHeuristic2(goal)
        self.f = h + self.g

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, obj):
        return isinstance(obj, State) and obj.state == self.state

    def __lt__(self, other):
        return self.f < other.f

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
