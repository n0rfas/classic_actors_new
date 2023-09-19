import heapq

h = []

heapq.heapify(h)  # преобразуем в кучу
print(heapq.heappop(h))  # IndexError: index out of range
