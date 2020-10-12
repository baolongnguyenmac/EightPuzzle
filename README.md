# EightPuzzle  

- Sử dụng một vài phương pháp tìm kiếm Heuristic để giải quyết bài toán  
- Tìm kiếm Heuristic dựa vào 1 thông tin khi tìm kiếm. Đó là Heuristic  
- Heuristic cho biết gần đúng mức độ gần đích của trạng thái đang xét  
- Heuristic is admissible: ![](https://latex.codecogs.com/svg.latex?0\leq&space;h(x)\leq&space;h'(x))  

## Thuật giải A*  

- Chọn 1 bước kế tiếp dựa vào hàm `f(x)`  
- ![](https://latex.codecogs.com/svg.latex?f(x)&space;=&space;g(x)&space;&plus;&space;h(x))  
- Với:
  - `g(x)` là hàm cho biết số bước đi tính từ root đến trạng thái hiện tại  
  - `h(x)` là hàm cung cấp Heuristic. Trong bài có trình bày 2 cách tính Heuristic  
    - Áp dụng khoảng cách Manhattan: ![](https://latex.codecogs.com/svg.latex?\inline&space;h_{1}(x)=\sum_{i=1}^{2}|state_{i}&space;-&space;goal_{i}|)  
    - Tính ![](https://latex.codecogs.com/svg.latex?\inline&space;h_{2}(x)=\sum_{i=1}^{8}\delta&space;(state_{i},&space;goal_{i})) với ![](https://latex.codecogs.com/svg.latex?\inline&space;\delta&space;(state_{i},&space;goal_{i})=0,&space;if&space;state_{i}\equiv&space;goal_{i}) ; ![](https://latex.codecogs.com/svg.latex?\inline&space;\delta&space;(state_{i},&space;goal_{i})=1,&space;if&space;state_{i}\not\equiv&space;goal_{i})  
