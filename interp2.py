import random

class Interp:

    def __init__(self, prog):
        self.prog = prog
        self.pc = 0

    def eval(self, expr):
        etype = expr[0]
        if etype == 'INTEG':
            return expr[1]
        elif etype == 'BOOL':
            if expr[1] == 'T':
                return True
            else:
                return False
        elif etype == 'INT':
            if expr[1] in self.vars:
                return self.vars[expr[1]][0][0]
            else:
                print('Uninitialized variable ', expr[1])
                raise RuntimeError
        elif etype == 'BOOLE':
            if expr[1] in self.vars:
                return self.vars[expr[1]][0][0]
            else:
                print('Uninitialized variable ', expr[1])
                raise RuntimeError
        elif etype == 'PROC':
            if expr[1] in self.vars:
                return self.vars[expr[1]][0][0]
            else:
                raise RuntimeError
        elif etype == 'MASPROC':
            if len(expr) == 3:
                if expr[1] in self.vars and 'PROC' in self.vars[expr[1]][1]:
                    return self.vars[expr[1]][0][self.eval(expr[2])]
                else:
                    raise RuntimeError
            else:
                if expr[1] in self.vars and 'PROC' in self.vars[expr[1]][1]:
                    dims = self.list_dim(expr[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(expr[2]))
                    return self.elem(self.vars[expr[1]][0], dims)
                else:
                    raise RuntimeError

        elif etype == 'MASINT':
            if len(expr) == 3:
                if expr[1] in self.vars:
                    if isinstance(self.vars[expr[1]][0][self.eval(expr[2])], int):
                        return self.vars[expr[1]][0][self.eval(expr[2])]
                    else:
                        print('This variable is not int')
                        raise RuntimeError
                else:
                    raise RuntimeError
            else:
                if expr[1] in self.vars:
                    dims = self.list_dim(expr[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(expr[2]))
                    return self.elem(self.vars[expr[1]][0], dims)
                else:
                    raise RuntimeError
        elif etype == 'MASBOOL':
             if len(expr) == 3:
                if expr[1] in self.vars:
                    return self.vars[expr[1]][0][self.eval(expr[2])]
                else:
                    raise RuntimeError
             else:
                if expr[1] in self.vars:
                    dims = self.list_dim(expr[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(expr[2]))
                    return self.elem(self.vars[expr[1]][0], dims)
                else:
                    raise RuntimeError
        elif etype == 'BINOP':
            if expr[1] == ',#':
                self.plus(expr[2])
            else:
                self.minus(expr[2])
        elif etype == 'RELOP':
            self.proced(expr[1])
            self.proced(expr[3])
            if expr[2] == 'EQ':
                if expr[3] != 'NP':
                    if isinstance(self.eval(expr[1]), int) and isinstance(self.eval(expr[3]), int):
                        if self.eval(expr[1]) == self.eval(expr[3]):
                            return True
                        else:
                            return False
                    elif expr[1][0] == 'RELOP' and isinstance(self.eval(expr[3]), bool):
                        if self.relop(expr[1]) == self.eval(expr[3]):
                            return True
                        else:
                            return False
                else:
                    if not (expr[1][1] in self.vars) or ('PROC' in self.vars[expr[1][1]][1] and not ('STATGROUP' in self.vars[expr[1][1]][0])):
                        return True
                    else:
                        return False
            elif expr[2] == 'MO':
                if isinstance(self.eval(expr[1]), int) and isinstance(self.eval(expr[3]), int):
                    if self.eval(expr[1]) > self.eval(expr[3]):
                        return True
                    else:
                        return False
        elif etype == 'LOGIC':
            self.proced(expr[1])
            self.proced(expr[2])
            first = self.eval(expr[1])
            second = self.eval(expr[2])
            if first == True or second == True:
                return True
            else:
                return False
        elif etype == 'PIERCE':
            if self.eval(expr[1]) == True:
                return False
            else:
                return True
        elif etype == 'PIERCES':
            if self.eval(expr[1]) == True:
                return False
            else:
                return True

        elif etype == 'IDENT':
            self.proced(expr[1])
            self.proced(expr[3])
            if expr[2] == '@':
                return self.bind(expr[1], expr[3])
            else:
                return self.unbind(expr[1], expr[3])

        elif etype == 'MOVE':
            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
            if expr[1] == 'MF':
                if self.maze['coord'][2] == 0:
                    if (self.maze['coord'][0] - 1) >= 0 and self.maze['maze'][self.maze['coord'][0] - 1][self.maze['coord'][1]] != 1:
                        self.maze['coord'][0] -= 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 1:
                    if (self.maze['coord'][1] - 1) >= 0 and self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1] - 1] != 1:
                        self.maze['coord'][1] -= 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 2:
                    if len(self.maze['maze']) > self.maze['coord'][0] + 1 and self.maze['maze'][self.maze['coord'][0] + 1][self.maze['coord'][1]] != 1:
                        self.maze['coord'][0] += 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 3:
                    if len(self.maze['maze'][self.maze['coord'][0]]) > self.maze['coord'][1] + 1 and self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1] + 1] != 1:
                        self.maze['coord'][1] += 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.print_maze()
                        return True
                    else:
                        return False
            elif expr[1] == 'ML':
                if self.maze['coord'][2] == 0:
                    if (self.maze['coord'][1] - 1) >= 0 and self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1] - 1] != 1:
                        self.maze['coord'][1] -= 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 1
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 1:
                    if len(self.maze['maze']) > self.maze['coord'][0] + 1 and self.maze['maze'][self.maze['coord'][0] + 1][self.maze['coord'][1]] != 1:
                        self.maze['coord'][0] += 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 2
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 2:
                    if len(self.maze['maze'][self.maze['coord'][0]]) > self.maze['coord'][1] + 1 and self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1] + 1] != 1:
                        self.maze['coord'][1] += 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 3
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 3:
                    if (self.maze['coord'][0] - 1) >= 0 and self.maze['maze'][self.maze['coord'][0] - 1][self.maze['coord'][1]] != 1:
                        self.maze['coord'][0] -= 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 0
                        self.print_maze()
                        return True
                    else:
                        return False
            elif expr[1] == 'MB':
                if self.maze['coord'][2] == 0:
                    if len(self.maze['maze']) > self.maze['coord'][0] + 1 and self.maze['maze'][self.maze['coord'][0] + 1][self.maze['coord'][1]] != 1:
                        self.maze['coord'][0] += 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 2
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 1:
                    if len(self.maze['maze'][self.maze['coord'][0]]) > self.maze['coord'][1] + 1 and self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1] + 1] != 1:
                        self.maze['coord'][1] += 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 3
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 2:
                    if (self.maze['coord'][0] - 1) >= 0 and self.maze['maze'][self.maze['coord'][0] - 1][self.maze['coord'][1]] != 1:
                        self.maze['coord'][0] -= 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 0
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 3:
                    if (self.maze['coord'][1] - 1) >= 0 and self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1] - 1] != 1:
                        self.maze['coord'][0] -= 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 1
                        self.print_maze()
                        return True
                    else:
                        return False
            elif expr[1] == 'MR':
                if self.maze['coord'][2] == 0:
                    if len(self.maze['maze'][self.maze['coord'][0]]) > self.maze['coord'][1] + 1 and self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1] + 1] != 1:
                        self.maze['coord'][1] += 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 3
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 1:
                    if (self.maze['coord'][0] - 1) >= 0 and self.maze['maze'][self.maze['coord'][0] - 1][self.maze['coord'][1]] != 1:
                        self.maze['coord'][0] -= 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 0
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 2:
                    if (self.maze['coord'][1] - 1) >= 0 and self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1] - 1] != 1:
                        self.maze['coord'][1] -= 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 1
                        self.print_maze()
                        return True
                    else:
                        return False
                elif self.maze['coord'][2] == 3:
                    if len(self.maze['maze']) > self.maze['coord'][0] + 1 and self.maze['maze'][self.maze['coord'][0] + 1][self.maze['coord'][1]] != 1:
                        self.maze['coord'][0] += 1
                        if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                            self.maze['success'] = 1
                            print('SUCCESSED!!!')
                        else:
                            self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                        self.maze['coord'][2] = 2
                        self.print_maze()
                        return True
                    else:
                        return False
            elif expr[1] == 'TP':
                if self.maze['tp'] > 0:
                    x = random.randint(0, len(self.maze['maze']) - 1)
                    y = random.randint(0, len(self.maze['maze'][self.maze['coord'][0]]) - 1)
                    i = 1
                    while self.maze['maze'][x][y] == 1 or self.maze['maze'][x][y] == 2:
                        if(i > 50):
                            print('FAILED!!!')
                            return False
                        x = random.randint(0, len(self.maze['maze']) - 1)
                        y = random.randint(0, len(self.maze['maze'][self.maze['coord'][0]]) - 1)
                        i += 1
                    self.maze['coord'][0] = x
                    self.maze['coord'][1] = y
                    if self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] == 5:
                        self.maze['success'] = 1
                        print('SUCCESSED!!!')
                    else:
                        self.maze['maze'][self.maze['coord'][0]][self.maze['coord'][1]] = 2
                    self.maze['tp'] -= 1
                    self.print_maze()
                    print('TELEPORT!!!')
                    return True
                else:
                    self.maze['success'] = -1
                    print('FAILED!!!')
                    return False


    def print_maze(self):
        for i in range(len(self.maze['maze'])):
            print()
            for j in range(len(self.maze['maze'][i])):
                if i == self.maze['coord'][0] and j == self.maze['coord'][1]:
                    print(7, end = '')
                else:
                    print(self.maze['maze'][i][j], end = '')
        print()
        print()

    def bind(self, id, expr):
        if id == expr:
            print('Recursion')
            return False
        elif not (id[1] in self.vars):
            print('Uninitialized variable', id[1])
            return False
        else:
            if expr[0] == 'PROC' or expr[0] == 'MASPROC':
                if id[0] == 'INT':
                    if not ('PROC' in self.ident[id[1]][1] and 'BOOL' in self.ident[id[1]][1]):
                        if len(self.vars[id[1]][0]) == 1:
                            self.ident[id[1]][0][0].append(expr)
                            return True
                        else:
                            print('Its massiv')
                            return False
                    else:
                        print('Error variable')
                        return False
                elif id[0] == 'BOOL':
                    if not ('PROC' in self.ident[id[1]][1] and 'INT' in self.ident[id[1]][1]):
                        if len(self.vars[id[1]][0]) == 1:
                            self.ident[id[1]][0][0].append(expr)
                            return True
                        else:
                            print('Its massiv')
                            return False
                    else:
                        print('Error variable')
                        return False
                elif id[0] == 'PROC':
                    if not ('BOOL' in self.ident[id[1]][1] and 'INT' in self.ident[id[1]][1]):
                        if len(self.vars[id[1]][0]) == 1:
                            self.ident[id[1]][0][0].append(expr)
                            return True
                        else:
                            print('Its massiv')
                            return False
                    else:
                        print('Error variable')
                        return False
                elif id[0] == 'MASINT':
                    if not ('PROC' in self.ident[id[1]][1] and 'BOOL' in self.ident[id[1]][1]):
                        if len(id) == 3:
                            if len(self.ident[id[1]][0]) > self.eval(id[2]):
                                self.ident[id[1]][0][self.eval(id[2])].append(expr)
                                return True
                            else:
                                print('Going out of the array')
                                return False
                        else:
                            pres = self.vars[id[1]][0]
                            dims = self.list_dim(id[3])
                            if isinstance(dims, int):
                                dims = [dims]
                            dims.insert(0, self.eval(id[2]))
                            pr = self.list_mas(pres)
                            if len(pr) == len(dims):
                                for i in range(len(dims)):
                                    if pr[i] < dims[i]:
                                        print('Going out of the array')
                                        return False
                                self.eq_mas2(dims, self.ident[id[1]][0], expr)
                                return True
                            else:
                                print('Going out of the array')
                                return False
                    else:
                        print('Error variable')
                        return False
                elif id[0] == 'MASBOOL':
                    if not ('PROC' in self.ident[id[1]][1] and 'INT' in self.ident[id[1]][1]):
                        if len(id) == 3:
                            if len(self.ident[id[1]][0]) > self.eval(id[2]):
                                self.ident[id[1]][0][self.eval(id[2])].append(expr)
                                return True
                            else:
                                print('Going out of the array')
                                return False
                        else:
                            pres = self.vars[id[1]][0]
                            dims = self.list_dim(id[3])
                            if isinstance(dims, int):
                                dims = [dims]
                            dims.insert(0, self.eval(id[2]))
                            pr = self.list_mas(pres)
                            if len(pr) == len(dims):
                                for i in range(len(dims)):
                                    if pr[i] < dims[i]:
                                        print('Going out of the array')
                                        return False
                                self.eq_mas2(dims, self.ident[id[1]][0], expr)
                                return True
                            else:
                                print('Going out of the array')
                                return False
                    else:
                        print('Error variable')
                        return False
                elif id[0] == 'MASPROC':
                    if not ('INT' in self.ident[id[1]][1] and 'BOOL' in self.ident[id[1]][1]):
                        if len(id) == 3:
                            if len(self.ident[id[1]][0]) > self.eval(id[2]):
                                self.ident[id[1]][0][self.eval(id[2])].append(expr)
                                return True
                            else:
                                print('Going out of the array')
                                return False
                        else:
                            pres = self.vars[id[1]][0]
                            dims = self.list_dim(id[3])
                            if isinstance(dims, int):
                                dims = [dims]
                            dims.insert(0, self.eval(id[2]))
                            pr = self.list_mas(pres)
                            if len(pr) == len(dims):
                                for i in range(len(dims)):
                                    if pr[i] < dims[i]:
                                        print('Going out of the array')
                                        return False
                                self.eq_mas2(dims, self.ident[id[1]][0], expr)
                                return True
                            else:
                                print('Going out of the array')
                                return False
                    else:
                        print('Error variable')
                        return False

    def proced(self, expr):
        etype = expr[0]
        if etype == 'INT':
            if expr[1] in self.vars:
                if len(self.ident[expr[1]][0][0]) != 0:
                    for i in range(len(self.ident[expr[1]][0][0])):
                        self.ex(self.ident[expr[1]][0][0][i])
            else:
                print('Uninitialized variable' , expr[1])
                raise RuntimeError
        elif etype == 'BOOLE':
            if expr[1] in self.vars:
                if len(self.ident[expr[1]][0][0]) != 0:
                    for i in range(len(self.ident[expr[1]][0][0])):
                        self.ex(self.ident[expr[1]][0][0][i])
            else:
                print('Uninitialized variable' , expr[1])
                raise RuntimeError
        elif etype == 'PROC':
            if expr[1] in self.vars:
                if len(self.ident[expr[1]][0][0]) != 0:
                    for i in range(len(self.ident[expr[1]][0][0])):
                        self.ex(self.ident[expr[1]][0][0][i])
            else:
                print('Uninitialized variable' , expr[1])
                raise RuntimeError
        elif etype == 'MASPROC':
            if len(expr) == 3:
                if expr[1] in self.vars and 'PROC' in self.vars[expr[1]][1]:
                    for i in range(len(self.ident[expr[1]][0][self.eval(expr[2])])):
                        self.ex(self.ident[expr[1]][0][0][i])
            else:
                if expr[1] in self.vars and 'PROC' in self.vars[expr[1]][1]:
                    self.proced(expr[2])
                    self.proced(expr[3])
        elif etype == 'MASINT':
            if len(expr) == 3:
                if expr[1] in self.vars:
                    if isinstance(self.vars[expr[1]][0][self.eval(expr[2])], int):
                        for i in range(len(self.ident[expr[1]][0][self.eval(expr[2])])):
                            self.ex(self.ident[expr[1]][0][0][i])
            else:
                if expr[1] in self.vars:
                    self.proced(expr[2])
                    self.proced(expr[3])
        elif etype == 'MASBOOL':
             if len(expr) == 3:
                if expr[1] in self.vars:
                    for i in range(len(self.ident[expr[1]][0][self.eval(expr[2])])):
                        self.ex(self.ident[expr[1]][0][0][i])
                    return self.vars[expr[1]][0][self.eval(expr[2])]
             else:
                if expr[1] in self.vars:
                    self.proced(expr[2])
                    self.proced(expr[3])
        elif etype == 'DIMS':
            self.proced(expr[1])
            self.proced(expr[2])

    def unbind(self, id, expr):
        if id == expr:
            print('Recursion')
            return False
        elif not (id[1] in self.vars):
            print('Uninitialized variable')
            return False
        else:
            if expr[0] == 'PROC' or expr[0] == 'MASPROC':
                if id[0] == 'INT':
                    if not ('PROC' in self.ident[id[1]][1] and 'BOOL' in self.ident[id[1]][1]):
                        if len(self.vars[id[1]][0]) == 1:
                            if expr in  self.ident[id[1]][0][0]:
                                self.ident[id[1]][0][0].remove(expr)
                                return True
                            else:
                                return True
                        else:
                            print('Its massiv')
                            return False
                    else:
                        print('Error variable')
                        return False
                elif id[0] == 'BOOL':
                    if not ('PROC' in self.ident[id[1]][1] and 'INT' in self.ident[id[1]][1]):
                        if len(self.vars[id[1]][0]) == 1:
                            if expr in  self.ident[id[1]][0][0]:
                                self.ident[id[1]][0][0].remove(expr)
                                return True
                            else:
                                return True
                        else:
                            print('Its massiv')
                            return False
                    else:
                        print('Error variable')
                        return False
                elif id[0] == 'PROC':
                    if not ('BOOL' in self.ident[id[1]][1] and 'INT' in self.ident[id[1]][1]):
                        if len(self.vars[id[1]][0]) == 1:
                            if expr in  self.ident[id[1]][0][0]:
                                self.ident[id[1]][0][0].remove(expr)
                                return True
                            else:
                                return True
                        else:
                            print('Its massiv')
                            return False
                    else:
                        print('Error variable')
                        return False
                elif id[0] == 'MASINT':
                    if not ('PROC' in self.ident[id[1]][1] and 'BOOL' in self.ident[id[1]][1]):
                        if len(id) == 3:
                            if len(self.ident[id[1]][0]) > self.eval(id[2]):  
                                if expr in  self.ident[id[1]][0][self.eval(id[2])]:
                                    self.ident[id[1]][0][0].remove(expr)
                                    return True
                                else:
                                    return True
                            else:
                                print('Going out of the array')
                                return False
                        else:
                            pres = self.vars[id[1]][0]
                            dims = self.list_dim(id[3])
                            if isinstance(dims, int):
                                dims = [dims]
                            dims.insert(0, self.eval(id[2]))
                            pr = self.list_mas(pres)
                            if len(pr) == len(dims):
                                for i in range(len(dims)):
                                    if pr[i] < dims[i]:
                                        print('Going out of the array')
                                        return False
                                self.eq_mas3(dims, self.ident[id[1]][0], expr)
                                return True
                            else:
                                print('Going out of the array')
                                return False
                    else:
                        print('Error variable')
                        return False
                elif id[0] == 'MASBOOL':
                    if not ('PROC' in self.ident[id[1]][1] and 'INT' in self.ident[id[1]][1]):
                        if len(id) == 3:
                            if len(self.ident[id[1]][0]) > self.eval(id[2]):
                                if expr in  self.ident[id[1]][0][self.eval(id[2])]:
                                    self.ident[id[1]][0][0].remove(expr)
                                    return True
                                else:
                                    return True
                            else:
                                print('Going out of the array')
                                return False
                        else:
                            pres = self.vars[id[1]][0]
                            dims = self.list_dim(id[3])
                            if isinstance(dims, int):
                                dims = [dims]
                            dims.insert(0, self.eval(id[2]))
                            pr = self.list_mas(pres)
                            if len(pr) == len(dims):
                                for i in range(len(dims)):
                                    if pr[i] < dims[i]:
                                        print('Going out of the array')
                                        return False
                                self.eq_mas3(dims, self.ident[id[1]][0], expr)
                                return True
                            else:
                                print('Going out of the array')
                                return False
                    else:
                        print('Error variable')
                        return False
                elif id[0] == 'MASPROC':
                    if not ('INT' in self.ident[id[1]][1] and 'BOOL' in self.ident[id[1]][1]):
                        if len(id) == 3:
                            if len(self.ident[id[1]][0]) > self.eval(id[2]):
                                if expr in self.ident[id[1]][0][self.eval(id[2])]:
                                    self.ident[id[1]][0][0].remove(expr)
                                    return True
                                else:
                                    return True
                            else:
                                print('Going out of the array')
                                return False
                        else:
                            pres = self.vars[id[1]][0]
                            dims = self.list_dim(id[3])
                            if isinstance(dims, int):
                                dims = [dims]
                            dims.insert(0, self.eval(id[2]))
                            pr = self.list_mas(pres)
                            if len(pr) == len(dims):
                                for i in range(len(dims)):
                                    if pr[i] < dims[i]:
                                        print('Going out of the array')
                                        return False
                                self.eq_mas3(dims, self.ident[id[1]][0], expr)
                                return True
                            else:
                                print('Going out of the array')
                                return False
                    else:
                        print('Error variable')
                        return False
        

    def evproc(self, expr):
        etype = expr[0]
        if etype == 'INT':
            if expr[1] in self.ident:
                return self.ident[expr[1]][0][0]
            else:
                print('Uninitialized variable')
                raise RuntimeError
        elif etype == 'BOOLE':
            if expr[1] in self.ident:
                return self.ident[expr[1]][0][0]
            else:
                print('Uninitialized variable')
                raise RuntimeError
        elif etype == 'PROC':
            if expr[1] in self.ident:
                return self.ident[expr[1]][0][0]
            else:
                print('Uninitialized variable')
                raise RuntimeError
        elif etype == 'MASPROC':
            if len(expr) == 3:
                if expr[1] in self.ident and 'PROC' in self.ident[expr[1]][1]:
                    return self.ident[expr[1]][0][self.eval(expr[2])]
                else:
                    print('Uninitialized variable')
                    raise RuntimeError
            else:
                if expr[1] in self.ident and 'PROC' in self.ident[expr[1]][1]:
                    dims = self.list_dim(expr[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(expr[2]))
                    return self.elem(self.ident[expr[1]][0], dims)
                else:
                    print('Uninitialized variable')
                    raise RuntimeError
        elif etype == 'MASINT':
            if len(expr) == 3:
                if expr[1] in self.ident:
                    if isinstance(self.ident[expr[1]][0][self.eval(expr[2])], int):
                        return self.ident[expr[1]][0][self.eval(expr[2])]
                    else:
                        print('This variable is not int')
                        raise RuntimeError
                else:
                    print('Uninitialized variable')
                    raise RuntimeError
            else:
                if expr[1] in self.ident:
                    dims = self.list_dim(expr[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(expr[2]))
                    return self.elem(self.ident[expr[1]][0], dims)
                else:
                    print('Uninitialized variable')
                    raise RuntimeError
        elif etype == 'MASBOOL':
             if len(expr) == 3:
                if expr[1] in self.ident:
                    return self.ident[expr[1]][0][self.eval(expr[2])]
                else:
                    print('Uninitialized variable')
                    raise RuntimeError
             else:
                if expr[1] in self.ident:
                    dims = self.list_dim(expr[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(expr[2]))
                    return self.elem(self.ident, dims)
                else:
                    print('Uninitialized variable')
                    raise RuntimeError


    def plus(self, expr):
        etype = expr[0]
        if etype == 'INTEG':
            return expr[1] + 1
        elif etype == 'INT':
            if expr[1] in self.vars:
                self.vars[expr[1]][0][0] += 1
                return self.vars[expr[1]][0][0]
            else:
                print('Uninitialized variable')
                raise RuntimeError
        elif etype == 'MASINT':
            if len(expr) == 3:
                if expr[1] in self.vars:
                    dims = []
                    dims.insert(0, self.eval(expr[2]))
                    return self.elem_plus(self.vars[expr[1]][0], dims)
                else:
                    print('Uninitialized variable')
                    raise RuntimeError
            else:
                if expr[1] in self.vars:
                    dims = self.list_dim(expr[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(expr[2]))
                    return self.elem_plus(self.vars[expr[1]][0], dims)
                else:
                    print('Uninitialized variable')
                    raise RuntimeError

    def minus(self, expr):
        etype = expr[0]
        if etype == 'INTEG':
            return expr[1] - 1
        elif etype == 'INT':
            if expr[1] in self.vars:
                self.vars[expr[1]][0][0] -= 1
                return self.vars[expr[1]][0][0]
            else:
                print('Uninitialized variable')
                raise RuntimeError
        elif etype == 'MASINT':
            if len(expr) == 3:
                if expr[1] in self.vars:
                    dims = []
                    dims.insert(0, self.eval(expr[2]))
                    return self.elem_minus(self.vars[expr[1]][0], dims)
                else:
                    print('Uninitialized variable')
                    raise RuntimeError
            else:
                if expr[1] in self.vars:
                    dims = self.list_dim(expr[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(expr[2]))
                    return self.elem_minus(self.vars[expr[1]][0], dims)
                else:
                    print('Uninitialized variable')
                    raise RuntimeError


    def elem(self, mas, dims):
        if len(dims) != 1:
            a = self.elem(mas[dims[0]], dims[1:])
        else:
            if isinstance(mas, int):
                a = mas
            else:
                a = mas[dims[0]]
        return a


    def elem_plus(self, mas, dims):
        if len(dims) > 1:
            a = self.elem_plus(mas[dims[0]], dims[1:])
        else:
            if isinstance(mas, int):
                mas += 1
                a = mas
            elif type(mas[dims[0]]) != list:
                mas[dims[0]] += 1
                a = mas[dims[0]]
            else:
                a = self.elem_plus(mas[dims[0]], [0])
        return a

    def elem_minus(self, mas, dims):
        if len(dims) > 1:
            a = self.elem_plus(mas[dims[0]], dims[1:])
        else:
            if isinstance(mas, int):
                mas -= 1
                a = mas
            elif type(mas[dims[0]]) != list:
                mas[dims[0]] -= 1
                a = mas[dims[0]]
            else:
                a = self.elem_plus(mas[dims[0]], [0])
        return a


    def list_dim(self, dims):
        if dims[0] == 'DIMS':
            a = []
            b = (self.list_dim(dims[1]))
            c = (self.eval(dims[2]))
            if type(b) == list:
                a = b.copy()
            else:
                a.append(b)
            a.append(c)
        else:
            a = (self.eval(dims))
        return a

    def make_mas(self, expr, dims):
        a = []
        if not isinstance(expr, int):
            ex = self.eval(expr) + 1
        else:
            ex = expr + 1
        if type(dims) != list:
            dim = self.list_dim(dims)
        else:
            dim = dims
        for i in range (ex):
            a.append(self.massiv(dim, 0))
        return a

    def make_mas1(self, expr, dims):
        a = []
        if not isinstance(expr, int):
            ex = self.eval(expr) + 1
        else:
            ex = expr + 1
        if type(dims) != list:
            dim = self.list_dim(dims)
        else:
            dim = dims
        for i in range (ex):
            a.append(self.massiv1(dim, 0))
        return a

    def massiv1(self, dims, num):
        a = []
        if type(dims) != list:
            dims = [dims]
        for i in range (dims[num] + 1):
            if num != (len(dims) - 1):
                 a.append(self.massiv1(dims, num + 1))
            else:
                a.append([])
        return a
        
    def massiv(self, dims, num):
        a = []
        if type(dims) != list:
            dims = [dims]
        for i in range (dims[num] + 1):
            if num != (len(dims) - 1):
                 a.append(self.massiv(dims, num + 1))
            else:
                a.append(0)
        return a

    def list_mas(self, mas):
        a = []
        a.append(len(mas) - 1)
        if type(mas[0]) == list:
            b = self.list_mas(mas[0])
            for i in range(len(b)):
                a.append(b[i])
        return a

    def new_list(self, new ,pr):
        pres = self.list_mas(pr)
        a = []
        size = max(len(new), len(pres))
        for i in range (size):
            if i >= len(pres) or (i < len(new) and new[i] > pres[i]):
                a.append(new[i])
            else:
                a.append(pres[i])
        return a

    def make_new_mas(self, new, pres):
        coun = len(pres)
        for i in range(coun):
            if type(new[i]) == list and type(pres[i]) == list:
                new[i] = self.make_new_mas(new[i], pres[i])
            else:
                new[i] = self.make_new_mas2(new[i], pres[i])
        return new


    def make_new_mas2(self, new, pres):
         if type(new) == list and type(pres) != list:
             new[0] = self.make_new_mas2(new[0], pres)
         else:
             new = pres
         return new

    def eq_mas(self, dims, mas, eq):
        if len(dims) != 1:
            mas[dims[0]] = self.eq_mas(dims[1:], mas[dims[0]], eq)
        elif type(mas[dims[0]]) == list:
            mas[dims[0]] = self.eq_mas([0], mas[dims[0]], eq)
        else:
           mas[dims[0]] = eq
        return mas

    def eq_mas1(self, dims, mas, eq):
        if len(dims) != 1:
            mas[dims[0]] = self.eq_mas1(dims[1:], mas[dims[0]], eq)
        elif type(mas[dims[0]]) == list and len(mas[dims[0]]) != 0:
            mas[dims[0]] = self.eq_mas1([0], mas[dims[0]], eq)
        else:
           mas[dims[0]] = eq
        return mas

    def eq_mas2(self, dims, mas, eq):
        if len(dims) != 1:
            mas[dims[0]] = self.eq_mas2(dims[1:], mas[dims[0]], eq)
        else:
           mas[dims[0]].append(eq)
        return mas

    def eq_mas3(self, dims, mas, eq):
        if len(dims) != 1:
            mas[dims[0]] = self.eq_mas3(dims[1:], mas[dims[0]], eq)
        else:
            if eq in mas[dims[0]]:
                mas[dims[0]].remove(eq)
        return mas

    def eq2(self, mas, eq):
        if type(mas) == list:
            mas[0] = self.eq2(mas[0], eq)
        else:
            mas = eq
        return mas

    def test_rec(self, ex1, ex2):
        if ex1 == ex2:
            return False
        if ex1[0] == 'PROC' or ex1[0] == 'INT' or ex1[0] == 'BOOL':
            id1 = self.ident[ex1[1]][0][0]
        else:
            if len(ex1) == 3:
                id1 = self.ident[ex1[1]][0][self.eval(ex1[2])]
            else:
                dims = self.list_dim(ex1[3])
                if isinstance(dims, int):
                    dims = [dims]
                dims.insert(0, self.eval(ex1[2]))
                id1 = self.elem(self.ident[ex1[1]][0], dims)
        if ex2[0] == 'PROC':
            id2 = self.ident[ex2[1]][0][0]
        else:
            if len(ex2) == 3:
                id2 = self.ident[ex2[1]][0][self.eval(ex2[2])]
            else:
                dims = self.list_dim(ex2[3])
                if isinstance(dims, int):
                    dims = [dims]
                dims.insert(0, self.eval(ex2[2]))
                id2 = self.elem(self.ident[ex2[1]][0], dims)
        if len(id1) == 0 and len(id2) == 0:
            return True
        elif len(id1) != 0 and len(id2) == 0:
            return True
        else:
            for i in range(len(id2)):
                if self.test_rec(ex1, id2[i]) == True:
                    return True
                else:
                    return False


    def ex(self, line):
        op = line[0]
        if op == 'ASSINT':
            if len(line) == 3:
                if not (line[1] in self.vars) or 'BOOL' in self.vars[line[1]][1] or 'PROC' in self.vars[line[1]][1]:
                    a = []
                    self.proced(line[2])
                    a.append(self.eval(line[2]))
                    b = []
                    b.append(a)
                    b.append('INT')
                    self.vars[line[1]] = b
                    c = []
                    c.append([])
                    d = []
                    d.append(c)
                    d.append('INT')
                    self.ident[line[1]] = d
                else:
                    self.proced(line[2])
                    self.vars[line[1]][0][0] = self.eval(line[2])
            elif len(line) == 4:
                if not(line[1] in self.vars) or 'BOOL' in self.vars[line[1]][1] or 'PROC' in self.vars[line[1]][1]:
                    a = []
                    c = []
                    j = self.eval(line[2])
                    for i in range(j + 1):
                        if i == j:
                            a.append(self.eval(line[3]))
                            c.append([])
                        else:
                            a.append(0)
                            c.append([])
                    self.proced(line[2])
                    self.proced(line[3])
                    b = []
                    b.append(a)
                    b.append('INT')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('INT')
                    self.ident[line[1]] = d
                else:
                    if len(self.vars[line[1]][0]) >= self.eval(line[2]):
                        self.proced(line[2])
                        self.proced(line[3])
                        self.eq2(self.vars[line[1]][0][self.eval(line[2])], self.eval(line[3]))
                    else:
                        a = []
                        d = []
                        self.proced(line[2])
                        j = self.eval(line[2])
                        c = len(self.vars[line[1]][0])
                        for i in range(j + 1):
                            if i < c:
                                a.append(self.vars[line[1]][0][i])
                                d.append(self.ident[line[1]][0][i])
                            elif i == j:
                                self.proced(line[3])
                                a.append(self.eval(line[3]))
                                d.append([])
                            else:
                                a.append(0)
                                d.append([])
                        b = []
                        b.append(a)
                        b.append('INT')
                        self.vars[line[1]] = b
                        e = []
                        e.append(d)
                        e.append('INT')
                        self.ident[line[1]] = e
            else:
                if not(line[1] in self.vars) or 'BOOL' in self.vars[line[1]][1] or 'PROC' in self.vars[line[1]][1]:
                    a = self.make_mas(line[2], line[3])
                    c = self.make_mas1(line[2], line[3])
                    self.proced(line[2])
                    self.proced(line[3])
                    self.proced(line[4])
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    a = self.eq_mas(dims, a, self.eval(line[4]))
                    c = self.eq_mas1(dims, c, [])
                    b = []
                    b.append(a)
                    b.append('INT')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('INT')
                    self.ident[line[1]] = d
                else:
                    self.proced(line[2])
                    self.proced(line[3])
                    self.proced(line[4])
                    pres = self.vars[line[1]][0]
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    list = self.new_list(dims, pres)
                    new = self.make_mas(list[0], list[1:])
                    a = self.make_new_mas(new, pres)
                    a = self.eq_mas(dims, a, self.eval(line[4]))
                    b = []
                    b.append(a)
                    b.append('INT')
                    self.vars[line[1]] = b
                    pres1 = self.ident[line[1]][0]
                    new1 = self.make_mas1(list[0], list[1:])
                    c = self.make_new_mas(new1, pres1)
                    self.eq_mas1(dims, c, [])
                    d = []
                    d.append(c)
                    d.append('INT')
                    self.ident[line[1]] = d
        elif op == 'ASSBOOL':
            if len(line) == 3:
                if not (line[1] in self.vars):
                    a = []
                    self.proced(line[2])
                    a.append(self.eval(line[2]))
                    b = []
                    b.append(a)
                    b.append('BOOL')
                    self.vars[line[1]] = b
                    c = []
                    c.append([])
                    d = []
                    d.append(c)
                    d.append('BOOL')
                    self.ident[line[1]] = d
                else:
                    self.proced(line[2])
                    self.vars[line[1]][0][0] = self.eval(line[2])
            elif len(line) == 4:
                 if not(line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'PROC' in self.vars[line[1]][1]:
                    a = []
                    c = []
                    j = self.eval(line[2])
                    for i in range(j + 1):
                        if i == self.eval(line[2]):
                            a.append(self.eval(line[3]))
                        else:
                            a.append(0)
                        c.append([])
                    self.proced(line[2])
                    self.proced(line[3])
                    b = []
                    b.append(a)
                    b.append('BOOL')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('BOOL')
                    self.ident[line[1]] = d
                 else:
                    if len(self.vars[line[1]][0]) >= self.eval(line[2]):
                        self.proced(line[2])
                        self.proced(line[3])
                        self.vars[line[1]][0][self.eval(line[2])] = self.eval(line[3])
                    else:
                        a = []
                        d = []
                        self.proced(line[2])
                        j = self.eval(line[2])
                        c = len(self.vars[line[1]][0])
                        for i in range(j + 1):
                            if i < c:
                                a.append(self.vars[line[1]][0][i])
                                d.append(self.ident[line[1]][0][i])
                            elif i == j:
                                self.proced(line[3])
                                a.append(self.eval(line[3]))
                                d.append([])
                            else:
                                a.append(0)
                                d.append([])
                        b = []
                        b.append(a)
                        b.append('BOOL')
                        self.vars[line[1]] = b
                        e = []
                        e.append(d)
                        e.append('BOOL')
                        self.ident[line[1]] = e
            else:
                if not(line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'PROC' in self.vars[line[1]][1]:
                    a = self.make_mas(line[2], line[3])
                    c = self.make_mas1(line[2], line[3])
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    self.proced(line[2])
                    self.proced(line[3])
                    self.proced(line[4])
                    a = self.eq_mas(dims, a, self.eval(line[4]))
                    c = self.eq_mas1(dims, c, [])
                    b = []
                    b.append(a)
                    b.append('BOOL')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('BOOL')
                    self.ident[line[1]] = d
                else:
                    self.proced(line[2])
                    self.proced(line[3])
                    self.proced(line[4])
                    pres = self.vars[line[1]][0]
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    list = self.new_list(dims, pres)
                    new = self.make_mas(list[0], list[1:])
                    a = self.make_new_mas(new, pres)
                    a = self.eq_mas(dims, a, self.eval(line[4])) 
                    b = []
                    b.append(a)
                    b.append('BOOL')
                    self.vars[line[1]] = b
                    pres1 = self.ident[line[1]][0]
                    new1 = self.make_mas1(list[0], list[1:])
                    c = self.make_new_mas(new1, pres1)
                    self.eq_mas1(dims, c, [])
                    d = []
                    d.append(c)
                    d.append('BOOL')
                    self.ident[line[1]] = d
        elif op == 'ASSPROC':
            if len(line) == 3:
                if not (line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'BOOL' in self.vars[line[1]][1]:
                    a = []
                    self.proced(line[2])
                    a.append(line[2])
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    c = []
                    c.append([])
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
                else:
                    self.proced(line[2])
                    self.vars[line[1]][0][0] = line[2]
            elif len(line) == 4:
                if not (line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'BOOL' in self.vars[line[1]][1]:
                    a = []
                    c = []
                    self.proced(line[2])
                    j = self.eval(line[2])
                    for i in range(j + 1):
                        if i == j:
                            a.append(line[3])
                        else:
                            a.append(0)
                        c.append([])
                    self.proced(line[3])
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
                else:
                    if len(self.vars[line[1]][0]) >= self.eval(line[2]):
                        self.proced(line[2])
                        self.proced(line[3])
                        self.vars[line[1]][0][self.eval(line[2])] = line[3]
                    else:
                        a = []
                        d = []
                        self.proced(line[2])
                        self.proced(line[3])
                        j = self.eval(line[2])
                        c = len(self.vars[line[1]][0])
                        for i in range(j + 1):
                            if i < c:
                                a.append(self.vars[line[1]][0][i])
                                d.append(self.ident[line[1]][0][i])
                            elif i == j:
                                a.append(line[3])
                                d.append([])
                            else:
                                a.append(0)
                                d.append([])
                        b = []
                        b.append(a)
                        b.append('PROC')
                        self.vars[line[1]] = b
                        e = []
                        e.append(d)
                        e.append('PROC')
                        self.ident[line[1]] = e
            else:
                if not (line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'BOOL' in self.vars[line[1]][1]:
                    a = self.make_mas(line[2], line[3])
                    c = self.make_mas1(line[2], line[3])
                    self.proced(line[2])
                    self.proced(line[3])
                    self.proced(line[4])
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    a = self.eq_mas(dims, a, line[4])
                    c = self.eq_mas1(dims, c, [])
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
                else:
                    self.proced(line[2])
                    self.proced(line[3])
                    self.proced(line[4])
                    pres = self.vars[line[1]][0]
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    list = self.new_list(dims, pres)
                    new = self.make_mas(list[0], list[1:])
                    a = self.make_new_mas(new, pres)
                    a = self.eq_mas(dims, a, line[4]) 
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    pres1 = self.ident[line[1]][0]
                    new1 = self.make_mas1(list[0], list[1:])
                    c = self.make_new_mas(new1, pres1)
                    self.eq_mas1(dims, c, [])
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
        elif op == 'PRINT':
            if line[1] in self.vars:
                print (self.vars[line[1]][0])
                print(self.ident[line[1]][0])
            else:
                print('Uninitialized variable', line[1])
        elif op == 'PRINTM':
            for i in range(len(self.vars[line[1]][0])):
                for j in range(len(self.vars[line[1]][0][i])):
                    print (self.vars[line[1]][0][i][j], end = '')
                print()
        elif op == 'BOOLE':
            if not (line[1] in self.vars) or 'INT' in self.vars[line[1]][1]:
                a = [0]
                b = []
                b.append(a)
                b.append('BOOL')
                c = []
                c.append([])
                d = []
                d.append(c)
                d.append('BOOL')
                self.vars[line[1]] = b
                self.ident[line[1]] = d
            else:
                self.proced(line)
        elif op == 'INT':
            if not (line[1] in self.vars) or 'BOOL' in self.vars[line[1]][1]:
                a = [0]
                b = []
                b.append(a)
                b.append('INT')
                c = []
                c.append([])
                d = []
                d.append(c)
                d.append('INT')
                self.vars[line[1]] = b
                self.ident[line[1]] = d
            else:
                self.proced(line)
        elif op == 'PROC':
            if not (line[1] in self.vars) or 'BOOL' in self.vars[line[1]][1] or 'INT' in self.vars[line[1]][1] or len(self.vars[line[1]][0]) == 0:
                a = []
                b = []
                a.append(0)
                b.append(a)
                b.append('PROC')
                c = []
                c.append([])
                d = []
                d.append(c)
                d.append('PROC')
                self.vars[line[1]] = b
                self.ident[line[1]] = d
            else:
                self.proced(line)
                self.ex(self.vars[line[1]][0][0])
        elif op == 'MASINT':
            if len(line) == 3:
                if not(line[1] in self.vars) or 'BOOL' in self.vars[line[1]][1] or 'PROC' in self.vars[line[1]][1]:
                    self.proced(line[2])
                    i = self.eval(line[2]) + 1
                    a = []
                    c = []
                    for j in range (i):
                        a.append(0)
                        c.append([])
                    b = []
                    b.append(a)
                    b.append('INT')
                    d = []
                    d.append(c)
                    d.append('INT')
                    self.vars[line[1]] = b
                    self.ident[line[1]] = d
                else:
                    if len(self.vars[line[1]][0]) < self.eval(line[2]):
                        self.proced(line[2])
                        j = self.eval(line[2]) - len(self.vars[line[1]][0])
                        for i in range(j + 1):
                            self.vars[line[1]][0].append(0)
                            self.ident[line[1]][0].append([])
            else:
                if not(line[1] in self.vars) or 'BOOL' in self.vars[line[1]][1] or 'PROC' in self.vars[line[1]][1]:
                    a = self.make_mas(line[2], line[3])
                    c = self.make_mas1(line[2], line[3])
                    self.proced(line[2])
                    self.proced(line[3])
                    b = []
                    b.append(a)
                    b.append('INT')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('INT')
                    self.ident[line[1]] = d
                else:
                    self.proced(line[2])
                    self.proced(line[3])
                    pres = self.vars[line[1]][0]
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    list = self.new_list(dims, pres)
                    new = self.make_mas(list[0], list[1:])
                    a = self.make_new_mas(new, pres)
                    b = []
                    b.append(a)
                    b.append('INT')
                    self.vars[line[1]] = b
                    pres1 = self.ident[line[1]][0]
                    new1 = self.make_mas1(list[0], list[1:])
                    c = self.make_new_mas(new1, pres1)
                    d = []
                    d.append(c)
                    d.append('INT')
                    self.ident[line[1]] = d
        elif op =='MASBOOL':
            if len(line) == 3:
                if not(line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'PROC' in self.vars[line[1]][1]:
                    i = self.eval(line[2]) + 1
                    self.proced(line[2])
                    a = []
                    c = []
                    for j in range (i):
                        a.append(0)
                        c.append([])
                    b = []
                    b.append(a)
                    b.append('BOOL')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('BOOL')
                    self.ident[line[1]] = d
                else:
                    if len(self.vars[line[1]][0]) < self.eval(line[2]):
                        self.proced(line[2])
                        j = self.eval(line[2]) - len(self.vars[line[1]][0])
                        for i in range(j + 1):
                            self.vars[line[1]][0].append(0)
                            self.ident[line[1]][0].append([])
            else:
                if not(line[1] in self.vars) or 'INT' in self.vars[line[1]][1]:
                    self.proced(line[2])
                    self.proced(line[3])
                    a = self.make_mas(line[2], line[3])
                    c = self.make_mas1(line[2], line[3])
                    b = []
                    b.append(a)
                    b.append('BOOL')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('BOOL')
                    self.ident[line[1]] = b
                else:
                    self.proced(line[2])
                    self.proced(line[3])
                    pres = self.vars[line[1]][0]
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    list = self.new_list(dims, pres)
                    new = self.make_mas(list[0], list[1:])
                    a = self.make_new_mas(new, pres)
                    b = []
                    b.append(a)
                    b.append('BOOL')
                    self.vars[line[1]] = b
                    pres1 = self.ident[line[1]][0]
                    new1 = self.make_mas1(list[0], list[1:])
                    c = self.make_new_mas(new1, pres1)
                    d = []
                    d.append(c)
                    d.append('INT')
                    self.ident[line[1]] = d
        elif op == 'MASPROC':
            if len(line) == 3:
                if not (line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'BOOL' in self.vars[line[1]][1]:
                    self.proced(line[2])
                    i = self.eval(line[2]) + 1
                    a = []
                    c = []
                    for j in range (i):
                        a.append(0)
                        c.append([])
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
                else:
                    if len(self.vars[line[1]][0]) < self.eval(line[2]):
                        self.proced(line[2])
                        j = self.eval(line[2]) - len(self.vars[line[1]][0])
                        for i in range(j + 1):
                            self.vars[line[1]][0].append(0)
                            self.ident[line[1]][0].append([])
                    else:
                        l = self.vars[line[1]][0][self.eval(line[2])]
                        if l[0] == 'STATGROUP':
                            self.proced(line[2])
                            self.ex(self.vars[line[1]][0][self.eval(line[2])])
                        else:
                            print('It is not procedure')
            else:
                if not (line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'BOOL' in self.vars[line[1]][1]:
                    a = self.make_mas(line[2], line[3])
                    c = self.make_mas1(line[2], line[3])
                    self.proced(line[2])
                    self.proced(line[3])
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
                else:
                    self.proced(line[2])
                    self.proced(line[3])
                    pres = self.vars[line[1]][0]
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    list = self.new_list(dims, pres)
                    new = self.make_mas(list[0], list[1:])
                    a = self.make_new_mas(new, pres)
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    pres1 = self.ident[line[1]][0]
                    new1 = self.make_mas1(list[0], list[1:])
                    c = self.make_new_mas(new1, pres1)
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
                    l = self.elem(self.vars[line[1]][0], dims)
                    if l != 0:
                        if l[0] == 'STATGROUP':
                            self.ex(l)
                        else:
                            print('It is list, not procedure, or procedure is empty')
        elif op == 'BINOP':
            if line[1] == ',#':
                self.proced(line[2])
                self.plus(line[2])
            else:
                self.proced(line[2])
                self.minus(line[2])
        elif op == 'STATGROUP':
            self.ex(line[1])
            if len(line) == 3:
                self.ex(line[2])
        elif op == 'EQPROC':
            if len(line) == 3:
                self.proced(line[2])
                stat = self.eval(line[2])
                proc = self.evproc(line[2])
                if not (line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'BOOL' in self.vars[line[1]][1]:
                    a = []
                    a.append(stat)
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    c = []
                    c.append(proc)
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
                else:
                    self.vars[line[1]][0][0] = stat
                    self.ident[line[1]][0][0] = proc
            elif len(line) == 4:
                self.proced(line[2])
                self.proced(line[3])
                stat = self.eval(line[3])
                proc = self.evproc(line[3])
                if not (line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'BOOL' in self.vars[line[1]][1]:
                    a = []
                    c = []       
                    j = self.eval(line[2])
                    for i in range(j + 1):
                        if i == j:
                            a.append(stat)
                            c.append(proc)
                        else:
                            a.append(0)
                            c.append([])
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
                else:
                    if len(self.vars[line[1]]) >= self.eval(line[2]):
                        self.vars[line[1]][0][self.eval(line[2])] = stat
                        self.ident[line[1]][0][self.eval(line[2])] = proc
                    else:
                        a = []
                        d = []
                        j = self.eval(line[2])
                        c = len(self.vars[line[1]][0])
                        for i in range(j + 1):
                            if i < c:
                                a.append(self.vars[line[1]][0][i])
                                d.append(self.ident[line[1]][0][i])
                            elif i == j:
                                a.append(stat)
                                d.append(proc)
                            else:
                                a.append(0)
                                d.append([])
                        b = []
                        b.append(a)
                        b.append('PROC')
                        self.vars[line[1]] = b
                        e = []
                        e.append(d)
                        e.append('PROC')
                        self.ident[line[1]] = e
            else:
                self.proced(line[2])
                self.proced(line[3])
                self.proced(line[4])
                stat = self.eval(line[4])
                proc = self.evproc(line[4])
                if not (line[1] in self.vars) or 'INT' in self.vars[line[1]][1] or 'BOOL' in self.vars[line[1]][1]:
                    a = self.make_mas(line[2], line[3])
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    a = self.eq_mas(dims, a, stat)
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    c = self.make_mas1(line[2], line[3])
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    c = self.eq_mas1(dims, c, proc)
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
                else:
                    pres = self.vars[line[1]][0]
                    dims = self.list_dim(line[3])
                    if isinstance(dims, int):
                        dims = [dims]
                    dims.insert(0, self.eval(line[2]))
                    list = self.new_list(dims, pres)
                    new = self.make_mas(list[0], list[1:])
                    a = self.make_new_mas(new, pres)
                    a = self.eq_mas(dims, a, stat) 
                    b = []
                    b.append(a)
                    b.append('PROC')
                    self.vars[line[1]] = b
                    pres1 = self.ident[line[1]][0]
                    new1 = self.make_mas1(list[0], list[1:])
                    c = self.make_new_mas(new1, pres1)
                    c = self.eq_mas1(dims, c, proc) 
                    d = []
                    d.append(c)
                    d.append('PROC')
                    self.ident[line[1]] = d
        elif op == 'IF':
            self.proced(line[1])
            if self.eval(line[1]) == True:
                self.ex(line[2])
        elif op == 'IDENT':
            if len(line) == 5:
                if line[1] == '.':
                    lin1 = ('BOOLE', line[2])
                elif line[1] == ',':
                   lin1 = ('INT', line[2])
                elif line[1] == '$':
                    lin1 = ('PROC', line[2])
                if self.test_rec(lin1, line[4]) == False:
                    print('Recursion')
                    raise RuntimeError
                self.proced(line[4])
                if line[3] == '@':
                    return self.bind(lin1, line[4])
                else:
                    return self.unbind(lin1, line[4])
            elif len(line) == 6:
                if line[1] == '.':
                    lin1 = ('MASBOOL', line[2], line[3])
                elif line[1] == ',':
                   lin1 = ('MASINT', line[2], line[3])
                elif line[1] == '$':
                    lin1 = ('MASPROC', line[2], line[3])
                if self.test_rec(lin1, line[5]) == False:
                    print('Recursion')
                    raise RuntimeError
                self.proced(line[5])
                if line[4] == '@':
                    return self.bind(lin1, line[5])
                else:
                    return self.unbind(lin1, line[5])
            else:
                if line[1] == '.':
                    lin1 = ('MASBOOL', line[2], line[3], line[4])
                elif line[1] == ',':
                   lin1 = ('MASINT', line[2], line[3], line[4])
                elif line[1] == '$':
                    lin1 = ('MASPROC', line[2], line[3], line[4])
                if self.test_rec(lin1, line[6]) == False:
                    print('Recursion')
                    raise RuntimeError
                self.proced(line[6])
                if line[5] == '@':
                    return self.bind(lin1, line[6])
                else:
                    return self.unbind(lin1, line[6])
        elif op == 'LABEL':
            self.label.append(line[1])
        elif op == 'GOLABEL':
            if self.eval(line[1]) == True:
                if line[2] in self.label:
                    flag = 0
                    for lin in self.prog.values():
                        if self.maze['success'] == 1:
                            break
                        elif self.maze['success'] == -1:
                            break
                        if line is None:
                            continue
                        if flag == 0:
                            if lin != ('LABEL', line[2]):
                                continue
                            flag = 1
                            continue
                        else:
                            if lin != line:
                                self.ex(lin)
                            else:
                                self.ex(lin)
                                break
        elif op == 'MOVE':
            return self.eval(line)


                    
    def initmaze(self):
        self.maze['coord'] = [4, 4, 0]
        b = []
        a = [1,1,1,1,1,1,1,1,1,1]
        b.append(a)
        a = [1,0,1,0,0,1,1,0,0,1]
        b.append(a)
        a = [1,0,0,0,0,1,1,0,0,1]
        b.append(a)
        a = [1,0,0,0,0,1,1,0,0,1]
        b.append(a)
        a = [1,0,0,0,0,1,1,0,0,1]
        b.append(a)
        a = [1,0,0,0,0,0,0,0,0,1]
        b.append(a)
        a = [1,0,0,0,0,0,0,0,0,1]
        b.append(a)
        a = [1,1,1,1,1,0,0,5,0,1]
        b.append(a)
        self.maze['maze'] = b
        self.maze['success'] = 0
        self.maze['tp'] = 3


    def run(self):
        self.vars = {}
        self.ident = {}
        self.label = []
        self.maze = {}
        self.initmaze()
        for line in self.prog.values():
            if self.maze['success'] == 1:
                break
            elif self.maze['success'] == -1:
                break
            if line is None:
             continue
         # print(self.vars)
            self.ex(line)