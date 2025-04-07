class Formula:
    def calculate(self, values):
        pass

    def __add__(self, other):
        return And(self, other)
    
    def __mul__(self, other):
        return Or(self, other)
    
    def __str__(self):
        pass
    
    def is_tautology(self):
        variables = list(set(self.get_variables()))
        num_variables = len(variables)
        for i in range(2**num_variables):
            values = {}
            for j in range(num_variables):
                values[variables[j]] = bool(i & (1 << j)) # j-th bit in i set to 1 or 0
            if not self.calculate(values):
                return False
        return True

    def get_variables(self):
        return []
    
    def simplify(self):
        variables = list(set(self.get_variables()))
        num_variables = len(variables)
        last_result = None

        for i in range(2**num_variables):
            values = {}
            for j in range(num_variables):
                values[variables[j]] = bool(i & (1 << j))
            act_result = self.calculate(values)
            if act_result != last_result and last_result != None:
                return self
            last_result = act_result
        return Constant(last_result)

class Constant(Formula):
    def __init__(self, value):
        if value != True and value != False:
            raise ValueNotValidException("Constant must be True or False")
        self.value = value

    def calculate(self, values):
        return self.value

    def __str__(self):
        return str(self.value)

    def is_tautology(self):
        return self.value

class Variable(Formula):
    def __init__(self, name):
        if not isinstance(name, str):
            raise ValueNotValidException("Name must be a string")
        self.name = name

    def calculate(self, values):
        return values[self.name]
    
    def __str__(self):
        return self.name
    
    def is_tautology(self):
        return False
    
    def get_variables(self):
        return [self.name]

class Not(Formula):
    def __init__(self, V):
        if not isinstance(V, Formula):
            raise ValueNotValidException("V must be a Formula")
        self.V = V
    
    def calculate(self, values):
        return not self.V.calculate(values)
    
    def __str__(self):
        return f'(¬{self.V.__str__()})'

    def get_variables(self):
        return self.V.get_variables()

class And(Formula):
    def __init__(self, L, R):
        if not isinstance(L, Formula) or not isinstance(R, Formula):
            raise ValueNotValidException("L and R must be Formulas")
        self.L = L
        self.R = R
    
    def calculate(self, values):
        return self.L.calculate(values) and self.R.calculate(values)
    
    def __str__(self):
        return f'({self.L.__str__()} ∧ {self.R.__str__()})'
    
    def is_tautology(self):
        if self.L.is_tautology() and self.R.is_tautology():
            return True
        return False
        
    def get_variables(self):
        return self.L.get_variables() + self.R.get_variables()
    
    def simplify(self):
        sup = super().simplify()
        if sup != self:
            return sup
        
        L = self.L.simplify()
        R = self.R.simplify()
        if isinstance(L, Constant):
            if L.calculate({}):
                return R
            else:
                return L
        if isinstance(R, Constant):
            if R.calculate({}):
                return L
            else:
                return R
            
        return self

class Or(Formula):
    def __init__(self, L, R):
        if not isinstance(L, Formula) or not isinstance(R, Formula):
            raise ValueNotValidException("L and R must be Formulas")
        self.L = L
        self.R = R
    
    def calculate(self, values):
        return self.L.calculate(values) or self.R.calculate(values)
    
    def __str__(self):
        return f'({self.L.__str__()} V {self.R.__str__()})'

    def get_variables(self):
        return self.L.get_variables() + self.R.get_variables()
    
    def simplify(self):
        sup = super().simplify()
        if sup != self:
            return sup
        
        L = self.L.simplify()
        R = self.R.simplify()
        if isinstance(L, Constant):
            if L.calculate({}):
                return L
            else:
                return R
        if isinstance(R, Constant):
            if R.calculate({}):
                return R
            else:
                return L
            
        return self

class ValueNotValidException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message) 

print()
print(Or(Not(Variable("x")), And(Variable("y"), Constant(True))))

print("\n---- TAUTOLOGY ----")
print(And(Or(Variable('p'), Not(Variable('p'))), And(Or(Variable('v'), Not(Variable('v'))), Or(Variable('r'), Not(Variable('r'))))).is_tautology())
print(Or(Not(Variable("x")), And(Variable("y"), Constant(True))).is_tautology())

print("\n---- SIMPLIFIED ----")
print(And(Variable('p'), Not(Variable('p'))).simplify())
print(Or(Not(Variable("x")), And(Variable("y"), Constant(True))).simplify())

print("------------------")
print(f'{And(Variable("p"), Constant(False))} ≡ {And(Variable("p"), Constant(False)).simplify()}')
print(f'{Or(Variable("p"), Constant(False))} ≡ {Or(Variable("p"), Constant(False)).simplify()}')


print("\n---- ADD-MUL ----")
print(Variable("w1") + Variable("w2"))
print(Variable("w1") * Variable("w2"))


#v = Not("p")
#v1 = Constant("v")
#v2 = Variable(True)
#v3 = And("p", True)
#v4 = Or(False, False)