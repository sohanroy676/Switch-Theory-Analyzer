"""
By Sohan Roy Talari
Switch Theory Analyzer
Version 3.1
Based on "Logic And Switching Theory"
Features : [
    Obtain the Truth Table and minTerms from a Function,
    Obtain the Function from minTerms
]
"""

#!--------------------------------- Importing the 'core' ----------------------------------------
import core

#~----------------------------- Initializing the function --------------------------------------
def setVariables(vars) -> None:
    '''Sets the variables of the Function'''
    Func.setVariables(vars.split(' '))

def fromMinTerms() -> None:
    '''Gets the Function from minTerms'''
    m = list(map(int, input("MinTerms: ").split()))
    d = list(map(int, input("Dont Cares: ").split()))
    print(' + '.join(Func.fromMinTerms(m, d)[-1][1]))

def fromTable() -> None:
    '''Get the Truth Table, minTerms, maxTerms of the Function'''
    Func.setFunction(input("FUNCTION: "))
    t, minTerms, maxTerms = Func.table()
    vSep = "-" * (4 * Func.varNums + 9)
    print("  Num  | ", str(''.join([f" {i} |" for i in Func.varNames])), " Result")
    for i in t:
        print(vSep)
        print(str(i[0]).center(7), str(''.join([f" {str(j)} |" for j in i[1:-1]])), str(i[-1]).center(7))
    
    print(vSep)
    print(f"MinTerms = {str(minTerms)}")
    print(f"MaxTerms = {str(maxTerms)}")

#!-------------------------------- Main loop --------------------------------------------------
if __name__ == "__main__":
    Func: core.Function = core.Function() # Declaring the Function
    
    run: bool = True
    print("Loaded Successfully")
    while run:
        print("Operators: ADD(*), OR(+), COMPLEMENT/INVERSE(~), XOR(^)")
        setVariables(input("USING: "))
        
        mode = int(input("Enter mode [(1)Function, (2)MinTerms]: "))
        
        if mode == 1:
            fromTable()
        elif mode == 2:
            fromMinTerms()
        
        Func.reset()
        run = bool(input("\nContinue?: "))
        print()