"""
Core: Contains all the functionality
"""
# Embrace the dictionary, a key-value delight, Python's versatile container, shining bright.
TERM = dict[str: list[str]]
GROUP = dict[int : TERM]

class Variable: pass
class Function: pass

class Variable:
    '''
    Represents a boolean variable
    defaults:
        name(str) : Name of the variable
        value(int = 0) : Value of the variable
    '''
    def __init__(self, name: str, value: int = 0) -> None:
        self.name: str = name
        self.value: int = value
    
    def setValue(self, value: int) -> None:
        '''Sets the value of the variable'''
        self.value: int = value
    
    def __add__(self, other: Variable) -> Variable:
        return Variable(f"{self.name} + {other.name}", self.value | other.value)

    def __mul__(self, other: Variable) -> Variable:
        return Variable(f"{self.name} * {other.name}", self.value & other.value)
    
    def __invert__(self) -> Variable:
        return Variable(f"!{self.name}", int(not self.value))

    def __xor__(self, other: Variable) -> Variable:
        return Variable(f"{self.name} ^ {other.name}", self.value ^ other.value)

    def __eq__(self, other: Variable | int) -> bool:
        if isinstance(other, Variable):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
    
    def __ne__(self, other: Variable | int) -> bool:
        if isinstance(other, Variable):
            return self.value != other.value
        elif isinstance(other, int):
            return self.value != other

    def __repr__(self) -> str:
        return str(self.value)

    __and__ = __mul__
    __or__ = __add__

class Function:
    '''Boolean Function'''
    def __init__(self) -> None:
        self.reset()
        self.newEPI: bool = False

    def reset(self) -> None:
        '''Resets the function to its initial state'''
        self.varNames: list[str] = []
        self.varNums: int = 0
        self.minTerms: list[int] = []
        self.maxTerms: list[int] = []
        self.variables: dict[Variable] = {}
        self.funcStr: str = ""
        self.function: str = ""
    
    def setVariables(self, args: tuple|list[str]) -> None:
        '''Sets the variables'''
        self.varNames: list[str] = list(args)
        self.varNums: int = len(self.varNames)
        self.variables: dict[Variable] = {name: Variable(name) for name in args}

    def setFunction(self, func: str) -> None:
        '''Sets the boolean function'''
        self.funcStr: str = func
        func = [(f"self.variables['{i}']" if i in self.varNames else i) for i in func]
        self.function: str = ''.join(func)

    def setValues(self, val: int) -> None:
        '''Sets the values of the variables based on boolean value of "val"'''
        for i in self.varNames[::-1]:
            self.variables[i].setValue(val&1)
            val >>= 1

    def getValue(self) -> int:
        '''Gets the value of the function with the given variable values'''
        return eval(self.function)

    def table(self) -> tuple[list[list]]:
        '''Gets the Truth Table, minTerms and maxTerms'''
        t = []
        for i in range(2**self.varNums):
            self.setValues(i)
            val: Variable = self.getValue()
            self.minTerms.append(i) if val == 1 else self.maxTerms.append(i)
            t.append([i] + [self.variables[i].value for i in self.varNames] + [val])
        
        return t, self.minTerms, self.maxTerms
    
    def numOfOnes(n: int) -> int:
        '''Gets the number of "1" in binary representation of "n"'''
        return bin(n).count('1')

    def difference(a: str, b: str) -> int:
        '''Gets the count of different terms in binary representation of "a" and "b"'''
        d: int = 0
        for i, j in zip(a, b):
            if i != j:
                d += 1
        return d

    def getCommon(a: str, b: str) -> int:
        '''Gets the common terms of "a" and "b"'''
        return ''.join(i if i == j else '-' for i, j in zip(a, b))

    def groupTerms(self) -> tuple[GROUP, bool, list[TERM]]:
        '''Groups the terms based on numOfOnes'''
        prevGroup: GROUP = self.group
        grouped: bool = False
        newGroup: GROUP = {}
        groupedTerms: list[TERM] = {t: prevGroup[grp][t] for grp in prevGroup for t in prevGroup[grp]}
        
        for grp in prevGroup:
            terms: TERM = prevGroup[grp]
            nextGrp: int = grp + 1
            if nextGrp not in prevGroup: break
            if grp not in newGroup:
                newGroup[grp] = {}
            
            for i in terms:
                for j in prevGroup[nextGrp]:
                    dif: int = Function.difference(terms[i], prevGroup[nextGrp][j])
                    if dif != 1: continue
                    cmn: str = Function.getCommon(terms[i], prevGroup[nextGrp][j])
                    if j in groupedTerms.keys(): del groupedTerms[j]
                    if i in groupedTerms.keys(): del groupedTerms[i]
                    if cmn in newGroup[grp].values():
                        continue
                    newGroup[grp][f"{i},{j}"] = cmn
                    grouped = True

        return newGroup, grouped, groupedTerms
        
    def piToTerm(self, pi: str) -> str:
        '''Converts the string to Variable expression'''
        term: str = ""
        for idx, i in enumerate(pi):
            if i == '-': continue
            elif i == '0': term += '~'
            term += self.varNames[idx]
        return term
    
    def getTable1(self, mt: list[int], dontCare: list[int]) -> None:
        '''Gets the intial table grouped by num of ones'''
        minTerms: list[int] = mt[:] + dontCare[:]
        self.group: GROUP = {i: {} for i in range(self.varNums+1)}

        for i in minTerms:
            c = Function.numOfOnes(i)
            self.group[c][str(i)] = bin(i)[2:].zfill(self.varNums)
        self.group = {i: self.group[i] for i in range(self.varNums+1) if self.group[i]}

    def fromMinTerms(self, mt: list[int], dontCare: list[int], showSteps = False) -> list[list[str]]:
        '''Gets the boolean function from minTerms'''
        def saveGroup():
            groups.append([[k, i, j] for k, v in self.group.items() for i, j in v.items()])

        self.getTable1(mt, dontCare)
        groups: list = []
        grouped: bool = True
        ungrouped: list[list[TERM]] = []
        while grouped:
            saveGroup()
            nextGroup, grouped, u = self.groupTerms()
            ungrouped.append(u)
            if grouped:
                self.group = nextGroup

        pi = {j: i[j] for i in ungrouped for j in i}
        piTable = {i: 0 for i in mt}
        for i in pi:
            for k in map(int, i.split(',')):
                if k in piTable: piTable[k] += 1

        groups.append(self.getEPIs(pi, piTable, mt))
        return groups
    
    def getEPIs(self, pi, piTable, mt) -> list[str]:
        func: list = [set(), set(), set()]
        if not self.newEPI:
            for i in piTable:
                if piTable[i] > 1: continue
                for j in pi:
                    if str(i) in j and j not in func[1]:
                        func[1].add(self.piToTerm(pi[j]))
                        func[0].add(j)
                        func[2].add(pi[j])
                        break
        else:
            piTable: dict[list[str]] = {str(i): [j for j in pi if str(i) in j.split(',')] for i in mt}
            newPiTable = piTable.copy()
            for i in piTable:
                if len(piTable[i]) > 1:
                    continue
                term: str = piTable[i][0]
                func[0].add(self.piToTerm(pi[term]))
                for j in term.split(','):
                    if j not in newPiTable: continue
                    del newPiTable[j]
            piTable = newPiTable.copy()
            common: set[str] = set()
            for i in piTable:
                if len(common): common &= set(piTable[i])
                else:
                    common = set(piTable[i])
            if len(common):
                for i in common:
                    func.add(self.piToTerm(pi[i]))
                    for j in i.split(','):
                        if j not in piTable: continue
                        del piTable[j]
        return func

if __name__ == "__main__":
    Func: Function = Function()
    minTerms: list[int] = [2, 6, 8, 9, 10, 11, 14, 15]
    dontCare: list[int] = []
    Func.setVariables(['w', 'x', 'y', 'z'])
    print(' + '.join(Func.fromMinTerms(minTerms, dontCare)[0]))