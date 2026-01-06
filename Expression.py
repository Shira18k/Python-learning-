import math
from abc import ABC, abstractmethod

# Part 1 - "Interface" (ABC - in python)
class Expression(ABC):

    @abstractmethod
    def variables(self):
        pass

    @abstractmethod
    def evaluate(self, env):
        pass

    @abstractmethod
    def assign(self, var, expr):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def differentiate(self, var: str) -> "Expression":
        pass

    @abstractmethod
    def simplify(self) -> "Expression":
        pass

    def __add__(self, other: "Expression") -> "Expression":
        return Add(self, ensure_expr(other))

    def __sub__(self, other: "Expression") -> "Expression":
        return Sub(self, ensure_expr(other))

    def __mul__(self, other: "Expression") -> "Expression":
        return Mul(self, ensure_expr(other))

    def __truediv__(self, other: "Expression") -> "Expression":
        return Div(self, ensure_expr(other))

    def __pow__(self, other: "Expression") -> "Expression":
        return Pow(self, ensure_expr(other))

    def __neg__(self) -> "Expression":
        return Neg(self)

    # recommendation
    def __radd__(self, other):
        return Add(ensure_expr(other), self)

    def __rmul__(self, other):
        return Mul(ensure_expr(other), self)

    def __rsub__(self, other):
        return Sub(ensure_expr(other), self)

    def __rpow__(self, other):
        return Pow(ensure_expr(other), self)

# Part 5 - help to use the "magical methods"
def ensure_expr(value: Expression | float | int) -> Expression:
    if isinstance(value, Expression):
        return value
    return Num(float(value))

# Part 2 - different types of expr - "Intermediate classes"
class UnaryOp(Expression):

    def __init__(self, expr):
        self.expr = expr

    def variables(self):
        return self.expr.variables()

    def assign(self, var, repl):
        return self.__class__(self.expr.assign(var, repl))


class BinaryOp(Expression):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def variables(self):
        return self.left.variables() | self.right.variables()

    def assign(self, var, repl):
        return self.__class__(self.left.assign(var, repl), self.right.assign(var, repl))



# Part 3 - the types of expression component
class Num(Expression):
    def __init__(self, num):
        self.num = num

    def variables(self):
        return set()            # no vars to show...

    def assign(self, num, repl):
        return self                # there is no change

    def evaluate(self, env=None):
        return self.num          #itself

    def __str__(self):
        return f"({self.num})"

    def differentiate(self, var: str) -> "Expression":
        return Num(0)

    def simplify(self):
        return self      # No further simplification possible for a number

class Var(Expression):
    def __init__(self, name):
        self.name = name

    def variables(self):
        return {self.name}

    def assign(self, name, repl):
        if self.name == name:
            return repl
        return self

    def evaluate(self, env=None):
        if env is not None and self.name in env:
            return env[self.name]

        raise ValueError(f"Variable {self.name} not found in environment")

    def __str__(self):
        return f"({self.name})"

    def differentiate(self, var: str) -> "Expression":
        if self.name == var:
            return Num(1.0)
        else:
            return Num(0.0)

    def simplify(self):
        return self                # No further simplification possible for a variable

# Part 4 - mathematical operations

class Neg(UnaryOp):
    def evaluate(self, env=None):
        return -self.expr.evaluate(env)

    def __str__(self):
        return f"(-{self.expr})"

    def differentiate(self, var):
        return Neg(self.expr.differentiate(var))

    def simplify(self):
        inside = self.expr.simplify()

        if isinstance(inside, Num):
            return Num(-inside.num)

        elif isinstance(inside, Neg):
            return inside.expr  #מדלג את דאבל neg ומחזיר מה שהיה בפנים - הולך לתנאי אם num ומחזיר נקי

        return Neg(inside)


class Sin(UnaryOp):
    def evaluate(self, env =None):
        return math.sin(self.expr.evaluate(env))

    def __str__(self):
        return f"SIN{self.expr}"

    def differentiate(self, var: str) -> "Expression":
        left = Cos(self.expr)
        right = self.expr.differentiate(var)
        return Mul(left, right)

    def simplify(self):
        inside = self.expr.simplify()
        if isinstance(inside , Num):
            return Num(math.sin(inside.num))

        return Sin(inside)

class Cos(UnaryOp):
    def evaluate(self, env = None):
        return math.cos(self.expr.evaluate(env))
    def __str__(self):
        return f"COS{self.expr}"

    def differentiate(self, var: str) -> "Expression":
        left = Neg(Sin(self.expr))
        right = self.expr.differentiate(var)
        return Mul(left, right)

    def simplify(self):
        inside = self.expr.simplify()
        if isinstance(inside, Num):
            return Num(math.cos(inside.num))

        return Cos(inside)

class Add(BinaryOp):
    def evaluate(self, env=None):
        return self.left.evaluate(env) + self.right.evaluate(env)

    def __str__(self):
        return f"({self.left} + {self.right})"

    def differentiate(self, var: str) -> "Expression":
        return Add(self.left.differentiate(var), self.right.differentiate(var))

    def simplify(self):
        inside_left = self.left.simplify()
        inside_right =self.right.simplify()

        if isinstance(inside_left , Num) and isinstance(inside_right , Num):
            return Num((inside_left.num + inside_right.num))

        elif isinstance(inside_left, Num) and inside_left.num == 0:
            return inside_right

        elif isinstance(inside_right, Num) and inside_right.num == 0:
            return inside_left     # just a simplify var

        return Add(inside_left , inside_right)


class Sub(BinaryOp):
    def evaluate(self, env=None):
        return self.left.evaluate(env) - self.right.evaluate(env)
    def __str__(self):
        return f"({self.left} - {self.right})"

    def differentiate(self, var: str) -> "Expression":
        return Sub(self.left.differentiate(var), self.right.differentiate(var))

    def simplify(self):
        inside_left = self.left.simplify()
        inside_right = self.right.simplify()

        if isinstance(inside_left, Num) and isinstance(inside_right, Num):
            return Num((inside_left.num - inside_right.num))

        elif isinstance(inside_left, Var) and isinstance(inside_right, Var):
            if (inside_left.name == inside_right.name):
                return Num(0.0)

        elif isinstance(inside_left ,Num) and inside_left.num == 0 : # 0-x = -x!
            return Neg(inside_right)

        elif isinstance(inside_right ,Num) and inside_right.num == 0 :
                return inside_left

        return Sub(inside_left, inside_right)


class Mul(BinaryOp):
    def evaluate(self, env=None):
        return self.left.evaluate(env) * self.right.evaluate(env)

    def __str__(self):
        return f"({self.left} * {self.right})"

    def differentiate(self, var: str) -> "Expression":
        left = Mul(self.left.differentiate(var), self.right)
        right = Mul(self.left, self.right.differentiate(var))
        return Add(left, right)

    def simplify(self):
        inside_left = self.left.simplify()
        inside_right = self.right.simplify()
        if isinstance(inside_left, Num) and isinstance(inside_right, Num):
            return Num(inside_left.num * inside_right.num)

        elif isinstance(inside_left, Num):
            if inside_left.num == 0 :
                return Num(0.0)
            if inside_left.num == 1:
                return inside_right

        elif isinstance(inside_right , Num):
            if inside_right.num == 0 :
                return Num(0.0)
            if inside_right.num == 1:
                return inside_left

        return Mul(inside_left, inside_right)

class Div(BinaryOp):
    def evaluate(self, env=None):
        if (self.right.evaluate(env) == 0):
            raise ValueError(f"Illegal!! - Division by zero")
        else:
            return self.left.evaluate(env) / self.right.evaluate(env)
    def __str__(self):
        return f"({self.left} : {self.right})"

    def differentiate(self, var: str) -> "Expression":
        left = Mul(self.left.differentiate(var), self.right)
        right = Mul(self.left, self.right.differentiate(var))
        numerator = Sub(left,right)
        denominator = Mul(self.right, self.right)
        return Div(numerator , denominator )

    def simplify(self):
        inside_left = self.left.simplify()
        inside_right = self.right.simplify()
        if isinstance(inside_left ,Num) and isinstance(inside_right ,Num):
            return Num(inside_left.num / inside_right.num)
        elif isinstance(inside_right ,Num) and inside_right.num ==1:
            return inside_left
        elif isinstance(inside_left, Var) and isinstance(inside_right, Var):
            if (inside_left.name == inside_right.name):
                return Num(1.0)

        return Div(inside_left, inside_right)

class Pow(BinaryOp):
    def evaluate(self, env =None):
        if (self.right.evaluate(env) == 0):      # in retrospect unnecessary  - python know it...
            return Num(1.0)
        else:
            return self.left.evaluate(env) ** self.right.evaluate(env)
    def __str__(self):
        return f"{self.left}^{self.right}"

    def differentiate(self, var: str) -> "Expression":
        if (isinstance(self.right, Num)):
            n = self.right
            left = Mul(n , Pow(self.left, Sub(n, Num(1.0))))
            return Mul(left, self.left.differentiate(var))
        else:
            ln = Log(Var("e"), self.left)
            left_in = Mul(self.right.differentiate(var),ln)
            div_part = Div(self.left.differentiate(var) , self.left)
            right_in = Mul(self.right , div_part)
            right = Add(left_in, right_in)
            left = Pow(self.left , self.right)
            return Mul(left, right)

    def simplify(self):
        inside_left = self.left.simplify()
        inside_right = self.right.simplify()
        if isinstance(inside_left, Num) and isinstance(inside_right, Num):
            return Num(inside_left.num ** inside_right.num)
        elif isinstance(inside_right , Num):
            if inside_right.num ==0:
                return Num(1.0)
            if inside_right.num ==1:
                return inside_left

        return Pow(inside_left, inside_right)

class Log(BinaryOp):
    def evaluate(self, env=None):
        base_val = self.left.evaluate(env)
        expr_val = self.right.evaluate(env)
        return math.log(expr_val, base_val)

    def __str__(self):
        return f"log({self.left}, {self.right})"

    def differentiate(self, var: str) -> "Expression":
        ln_u = Log(Var("e"), self.right)
        ln_base = Log(Var("e"), self.left)
        term1 = Div(self.right.differentiate(var), Mul(self.right, ln_base))
        term2 = Div(Mul(self.left.differentiate(var), ln_u), Mul(self.left, Pow(ln_base, Num(2.0))))

        return Sub(term1, term2)

    def simplify(self):
        inside_left = self.left.simplify()
        inside_right = self.right.simplify()
        if isinstance(inside_left, Num) and isinstance(inside_right, Num):
            return Num(math.log(inside_left.num , inside_right.num))
        elif isinstance(inside_left, Var) and isinstance(inside_right, Var):
            if (inside_left.name  == inside_right.name):
                return Num(1.0)

        return Log(inside_left, inside_right)


# expressions_demo.py
if __name__ == "__main__":
    # Define variables
    x = Var("x")
    y = Var("y")

    # Define a multi-variable function: f(x, y) = (x^2 * y) + sin(y)
    f = (x ** 2 * y) + Sin(y)

    print(f"--- Multi-Variable Test for: {f} ---")
    print("-" * 80)

    # 1. Partial Derivative with respect to x (y is treated as a constant)
    # Expected result: (2*x * y) + 0 = 2xy
    df_dx_raw = f.differentiate("x")
    df_dx_simple = df_dx_raw.simplify()

    print(f"df/dx (Raw):        {df_dx_raw}")
    print(f"df/dx (Simplified): {df_dx_simple}")
    print(f"Interpretation:     Differentiating by 'x' correctly turned 'y' and 'Sin(y)' into constants/zero.")
    print("-" * 80)

    # 2. Partial Derivative with respect to y (x is treated as a constant)
    # Expected result: (x^2 * 1) + cos(y) = x^2 + cos(y)
    df_dy_raw = f.differentiate("y")
    df_dy_simple = df_dy_raw.simplify()

    print(f"df/dy (Raw):        {df_dy_raw}")
    print(f"df/dy (Simplified): {df_dy_simple}")
    print(f"Interpretation:     Differentiating by 'y' correctly kept 'x^2' as a coefficient.")
    print("-" * 80)

    # 3. Evaluation with two variables
    # f(2, 0) = (2^2 * 0) + sin(0) = 0
    env = {"x": 2.0, "y": 0.0}
    result = f.evaluate(env)
    print(f"Evaluation at {env}: Result = {result} (Expected: 0.0)")