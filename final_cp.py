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


#### Простой стековый интерпретатор
class Number(int): ...
class Sol_result(Number): ...


class Interpreter:

    ### конструктор класса должен принимать код в виде строки
    def __init__(self, expression):
        # data = Stack()
        # for elem in expression[::-1]:
        #     data.push(elem)
        #self.__expression = data
        self.__expression = '(' + expression + ')'
        self.__numbers = Stack()
        self.__operators = Stack()

    #Выражения
    # +: сложение
    # -: вычитание
    # *: умножение
    # /: деление
    # ^: возведение в степень


    # +: сложение
    def __add(item1:Number, item2:Number) -> Number:
        return item1 + item2

    # -: вычитание
    def __sub(item1:Number, item2:Number) -> Number:
        return item1 - item2

    # *: умножение
    def __mul(item1:Number, item2:Number) -> Number:
        return item1 * item2

    # /: деление
    def __div(item1:Number, item2:Number) -> Number:
        if item2 == 0: raise 'Нельзя делить на ноль!'
        return item1 / item2

    # ^: возведение в степень
    def __exp(item1:Number, item2:Number) -> Number:
        return item1 ^ item2

    
    #словарь с операторами
    #self.__dOperators.get( /char/, error)(item1, item2) # - вызовет функцию и передаст параметры
    __dOperators = {
    '+' : __add, 
    '-' : __sub, 
    '*' : __mul, 
    '/' : __div, 
    '^' : __exp
    }

    ### evaluate единственный публичный метод
    # Он должен вернуть результат выражения
    def evaluate(self) -> Sol_result:
        skobki = Stack()

        for index, char in enumerate (self.__expression):
            if char != ')':
                if char == '(': 
                    skobki.push(char)
                    continue
                if char == ' ': continue
                if char.isdigit():
                    self.__numbers.push(int(char))
                elif char in '+-*/^':
                    self.__operators.push(char)
                else:
                    raise Exception(f'В выражении обнаружен неизвестный символ!\nСимвол: {char}\tПозиция: {index}')
            else:
                if skobki.is_empty():
                    raise Exception(f'Ошибка растановки скобок в выражении!\nПозиция: {index}')
                skobki.pop()
                operator = self.__operators.pop() 
                item1, item2 = self.__numbers.pop(), self.__numbers.pop()
                # res = self.__dOperators.get(operator, self.__error_operator)(item1, item2)
                # self.__numbers.push( res )
                self.__numbers.push( self.__dOperators.get(operator, self.__error_operator)(item1, item2))
        if not skobki.is_empty():
                    raise Exception(f'Ошибка растановки скобок в выражении!')
        return self.__numbers.pop()
    
    def __error_operator(self, *items):
        raise Exception(f'Непредвиденная ошибка вызова оператора!')
    
interpreter = Interpreter('1+((2+3)*(4*5))')
print('Ответ: ', interpreter.evaluate())
interpreter = Interpreter('(1+1)+(1+1)')
print('Ответ: ', interpreter.evaluate())
interpreter = Interpreter('1 + ((2 + 3) * (4 * 5))')
print('Ответ: ', interpreter.evaluate())
interpreter = Interpreter('(1 + 1) + ( 1 + 1)')
print('Ответ: ', interpreter.evaluate())
interpreter = Interpreter('(1 + 1) + ( 1 + 1)')
print('Ответ: ', interpreter.evaluate())
interpreter = Interpreter('(1 + 1) + ))( 1 + 1)')
print('Ответ: ', interpreter.evaluate())