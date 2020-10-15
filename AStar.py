import State

class SolveEightPuzzle:
    def __init__(self, start, goal):
        self.start = start
        self.start.setF(0, goal)
        self.goal = goal

    def heapify(self, array, index):
        """
        cân bằng lại cây heap
        """
        while index < len(array):
            min = index
            left = 2*index + 1
            right = 2*index + 2

            if left < len(array) and array[left].f < array[min].f:
                min = left
            if right < len(array) and array[right].f < array[min].f:
                min = right

            if min != index:
                array[index], array[min] = array[min], array[index]
            else:
                break

    def push(self, array, state):
        """
        đẩy trạng thái state vào mảng heap f
        """
        array.insert(0, state)
        self.heapify(array, 0)

    def getMinState(self, array):
        """
        lấy phần tử đầu tiên của cây minHeap ra 
        sau đó cân bằng lại 
        """
        rs = array[0]
        if len(array) != 1:
            array[0] = array.pop()
            self.heapify(array, 0)
        else:
            array.pop()
        return rs

    def AStar(self):
        isVisited = {}
        parent = {self.start: -1}

        # f là 1 mảng heap
        # dùng lưu các state dưới dạng heap của chi phí đường đi từ start đến state đó + heuristic
        f = [self.start]

        current = self.start
        while current != self.goal:
            current = self.getMinState(f)
            isVisited[current] = True

            newPos = current.getDirection()
            for pos in newPos:
                if pos is not None and isVisited.get(pos) is None:
                    if pos.g > current.g + 1:
                        pos.g = current.g + 1
                        parent[pos] = current
                        self.push(f, pos)

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
    s = SolveEightPuzzle(State.State(state=987654321), State.State(state=123456789))
    s.AStar()

if __name__ == '__main__':
    main()

