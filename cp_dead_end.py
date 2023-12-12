class Node:
    
    def __init__(self, data):
        self.__data = data
        self.__next = None

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    data = property(get_data, set_data)


    def get_next(self):
        return self.__next

    def set_next(self, node):
        self.__next = node

    next = property(get_next, set_next)

class LinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__length = 0
    
    def is_empty(self):
        return self.__head is None #== вначале делает проверку is, а None один в памяти, поэтому is проще
    
    def add(self, item):
        node = Node(item)
        node.next = self.__head
        self.__head = node
        if self.__length == 0:
            self.__tail = node
        self.__length += 1
    
    #размер массива
    def size(self):
        return self.__length
    
    #есть элемент в списке или нет
    def search(self, item):
        if self.is_empty(): return False
        current = self.__head
        
        while not current is None:
            if current.data == item:
                return True
            current = current.next
        return False
    
    #удаление элемента из списка по значению
    def remove(self, item):
        if self.is_empty(): return False
        current = self.__head
        previous = None
        while not current is None:
            #если текущий элемент - искомый элемент, то меняем ссылки
            if current.data == item:
                #"удаляем" узел заменой ссылок: предыдущий элемент до узла ссылается на следущий элемент после узла
                if previous:
                    previous.next = current.next
                    #если текущий элемент - хвост, то хвостом становится предыдущий элемент
                    if current == self.__tail:
                        self.__tail = previous
                else:
                    #если текущий элемент - голова, то следущий элемент становится головой
                    self.__head = current.next
                #убираем 1 ед. длины
                self.__length -= 1

                #вернем значение узла, чтобы пользователь понял, что мы его нашли
                return current.data
            #для того, чтобы бежать по циклу
            previous = current
            current = current.next
        return False
    
    def append(self, item):
        if self.is_empty(): return False
        node = Node(item)
        node.next = None
        #теперь узел хвоста ссылается на новый узел
        self.__tail.next = node
        #новый узел - хвост
        self.__tail = node
    
    def pop(self):
        if self.is_empty(): return False

        current = self.__head
        while not current.next == self.__tail:
            current = current.next
        
        to_return = self.__tail.data

        current.next = None
        self.__tail = current

        return to_return
    
    #чтобы увидеть результаты работы методов
    def __str__(self):
        to_return = ''
        current = self.__head
        while not current is None:
            to_return += f'{current.data} --> '
            current = current.next
        
        to_return += 'None'
        
        return to_return

    def get(self, index):
        if self.is_empty(): return None
        if index >= self.size(): return None
        if index < 0: return None
        if index == 0: return self.__head.data
        current = self.__head
        cnt = 1
        while cnt < self.size():
            current = current.next
            if index == cnt:
                return current.data
            cnt += 1
        return None

    #итерабильность
    def __getitem__(self, index):
        if index >= self.size(): raise IndexError()
        return self.get(index)
    
    def shift(self):
        if self.__head is None: return None
        node = self.__head
        self.__head = node.next
        node.next = None
        self.__length -= 1
        return node.data

class Stack:
    def __init__(self):
        self.__data = LinkedList()
    
    def push(self, item):
        self.__data.add(item)
    
    def pop(self):
        return self.__data.shift()
    
    def top(self):
        return self.__data.get(0)
    
    def is_empty(self):
        return self.__data.is_empty()
    
    def size(self):
        return self.__data.size()
    
    def clear(self):
        self.__data = LinkedList()

#####   Функции

#Добавляем элемент или элементы в стэк
def push_to_stack(stack_obj, items):
    for elem in items[::-1]:
        stack_obj.push(elem)

# К тупику со стороны Пути 1 подъехал поезд.
# Необходимо сделать так, чтобы вагоны поезда попали на Путь 2 по порядку
# (сначала первый, потом второй и т.д., считая от головы поезда,
#  едущего по пути 2 в сторону от тупика).

# При этом известно, в каком порядке изначально идут вагоны поезда.

#   Переменные
dead_end = Stack()
way_input = Stack()
way_output = Stack()

# К тупику со стороны Пути 1 подъехал поезд.
input_data:list[int] = list(map(int, input().split()))
push_to_stack(way_input, input_data)

# Необходимо сделать так, чтобы вагоны поезда попали на Путь 2 по порядку
# (сначала первый, потом второй и т.д., считая от головы поезда,
#  едущего по пути 2 в сторону от тупика).

ch = 1 # номер ожидаемого вагона

assert way_input.is_empty() == False

result = True
actions = ''

while ((not way_input.is_empty()) or (not dead_end.is_empty())) and result:
    counter_in = 0

    if way_input.is_empty():
        result = False
        break

    while not dead_end.top() == ch:
        dead_end.push(way_input.pop())
        counter_in += 1
    
    actions += f'Ввели: {counter_in}\n'

    counter_out = 0

    while dead_end.top() == ch:
        way_output.push(dead_end.pop())
        counter_out += 1
        ch += 1
    
    actions += f'Вывели: {counter_out}\n'
    
if not result:
    print('Не получилось')
else:
    print(actions.rstrip('\n'))