# a*b+c = ab*c+
# a+b*c=abc*+
# (c+v+b+n/a)*(s-d-f+r+t*y+u*k+p+z)
alphabet = [chr(i) for i in range (97, 123)] + [chr(i) for i in range (65, 91)]
numbers = [str(i) for i in range(0,10)] 
operations = {'+':[2, lambda x,y: x + y],'-':[2, lambda y,x: x - y],'~':[0, lambda x: -x],'/':[1, lambda y,x: x / y if y!=0 else 'error'],'*':[1, lambda x,y: x * y]}
# надо получить формулу, где все разделено пробелами

# Получаем строку с разделеными пробелами символами  
def translate(formula):
    formula = formula.split()
    stack = []
    poliz = []
    for s in formula:
        if s in alphabet:
            poliz.append(f'{s} ')
        elif s in operations:
            while stack and stack[-1] in operations and operations[stack[-1]][0] <= operations[s][0]:
                poliz.append(f'{stack.pop()} ')
            stack.append(s)
        elif s =='(':
            stack.append(s)
        elif s ==')':
            while len(stack)!=0 and stack[-1] != '(' :
                poliz.append(f'{stack.pop()} ')
            stack.pop()
        else:
            poliz.append(f'{s} ')
    while stack:
        poliz.append(f'{stack.pop()} ')
    poliz = ''.join(poliz)
    return poliz

def form_values(string):
    values = {}
    for s in string:
        if s in alphabet:
            if s not in values:
                values[s] = int(input(f'Введите значение переменной {s}'))
    return values  

def solution(poliz,values):
    stack = []
    poliz = poliz.split()
    for s in poliz:
        if s in alphabet:
            stack.append(float(values[s]))
        elif s in operations:
            if s == '~':
                stack.append(operations[s][1](stack.pop()))
            else:
                result = operations[s][1](stack.pop(),stack.pop())
                if result == 'error':
                    return 'Деление на ноль'
                else:
                    stack.append(result)
        else:
            stack.append(float(s))
    return stack.pop()

#Проверка скобок
def chek_sk(formula):
    stack = []
    for s in formula:
        if s == '(':
            stack.append(s)
        if s == ')':
            if stack:
                stack.pop()
            else:
                print('Ошибка со скобками')
    if stack:
        print ('Ошибка со скобками')
    return formula

def check(formula):
    # Используем регулярное выражение для поиска букв, чисел, знаков и скобок
    pattern = r'(\d+\.\d+|\d+|\w+|\S)'
    tmp = re.findall(pattern, formula)
    if tmp[0] == '-':
        tmp[0] = '~'
    for i in range(1,len(tmp)):
        if tmp[i] == "-" and (tmp[i-1] not in alphabet and tmp[i-1] not in numbers):
            tmp[i] = '~'
    formula = ' '.join(tmp)
    
    return formula

def is_valid(s):
    if re.search(r"[^0-9a-z+*/().-]+", s) or re.fullmatch(r".*[+*/.-]", s) or re.fullmatch(r"[+*/.].*", s) \
    or re.fullmatch(r".*[+*/.-][+*/.-].*", s) or re.fullmatch(r".*\.-.*", s) or re.fullmatch(r".*[0-9a-z.][a-z].*", s) \
    or re.fullmatch(r".*[a-z][0-9a-z.].*", s) or re.fullmatch(r".*[+*/.-]-[a-z].*", s) or re.fullmatch(r".*--.*", s)\
    or re.fullmatch(r".*[0-9]+\.[0-9]+\.[0-9]+.*", s) or re.fullmatch(r".*\)[^+*/-].*", s) \
    or re.fullmatch(r".*[0-9a-b]\(.*", s):
        return False
    if not chek_sk(s):
        return False
    return True

def calculation(formula,values):
    for s,val in values.items():
        formula = formula.replace(s,str(val))
    try:
        return eval(formula)
    except:
        return 'Деление на ноль'

formula = ''
while True:
    formula = input('Введите выражение в инфиксной форме / Для завершения работы введите stop ')
    if formula == 'stop':
        break
    else:
        formula = formula.replace(' ','')
        if not is_valid(formula):
            print('В формуле ошибка')
        else:
            formula = check(formula)
            poliz = translate(formula)
            print(f'ПОЛИз: {poliz}')
            values = form_values(formula)
            print(f'Значение выражения, посчитанное в постфиксной форме {solution(poliz,values)}')
            print(f'Значение выражения, посчитанное в инфиксной форме {calculation(formula,values)}')
