from typing import Callable
from sexpdata import Symbol

class UnknownSymbolException(Exception):
    pass

SExpr = list['SExpr']|Symbol|int|float
ValueType = int|float

class Instantiation(dict[Symbol, ValueType]):
    def eval(self, expr: SExpr) -> ValueType:
        if isinstance(expr, int) or isinstance(expr, float):
            return expr
        if isinstance(expr, list):
            if isinstance(expr[0], Symbol):
                op = self.eval_func(expr[0])
                return op(expr[1:])
            else:
                raise TypeError(f"Head element of type {type(expr)} is not a symbol")
        if isinstance(expr, Symbol):
            if expr in self:
                return self[expr]
            raise TypeError(f"Symbol type {expr} cannot be evaluated to result")
        raise TypeError(f"Unhandled type in S-Expr: {type(expr)}")

    def eval_func(self, symbol: Symbol, args:list[ValueType]|None=None) -> Callable[[list[SExpr]], ValueType]:
        if symbol == Symbol("+") or symbol == Symbol("add"):
            def func(l):
                acc = 0
                _ = [acc := acc + self.eval(i)for i in l]
                return acc
            return func
        if symbol == Symbol("-") or symbol == Symbol("sub"):
            def func(l):
                assert len(l) == 2, "sub takes exactly two arguments"
                return self.eval(l[0]) - self.eval(l[1])
            return func
        if symbol == Symbol("*") or symbol == Symbol("mul"):
            def func(l):
                acc = 1
                _ = [acc := acc * self.eval(i )for i in l]
                return acc
            return func
        if symbol == Symbol("/") or symbol == Symbol("div"):
            def func(l):
                assert len(l) == 2, "div takes exactly two arguments"
                return self.eval(l[0]) / self.eval(l[1])
            return func
        # Conversion of float to int
        if symbol == Symbol("int") or symbol == Symbol("floor"):
            def func(l):
                assert len(l) == 1, "floor takes exactly one arguments"
                return int(self.eval(l[0]))
            return func
        # Conversion of int to float
        if symbol == Symbol("float"):
            def func(l):
                assert len(l) == 1, "float takes exactly one arguments"
                return float(self.eval(l[0]))
            return func
        # (up-bound bnd value): return bnd if value > bnd else return value
        if symbol == Symbol("up-bound"):
            def func(l):
                assert len(l) == 2, "up-bound takes exactly two arguments"
                bnd = self.eval(l[0])
                value = self.eval(l[1])
                return bnd if value > bnd else value
            return func
        # (low-bound bnd value): return bnd if value < bnd else return value
        if symbol == Symbol("low-bound"):
            def func(l):
                assert len(l) == 2, "low-bound takes exactly two arguments"
                bnd = self.eval(l[0])
                value = self.eval(l[1])
                return bnd if value < bnd else value
            return func
            
        raise TypeError(f"Unknown function {symbol}")

def eval_s_expr(expr: SExpr, inst: dict[Symbol, ValueType]|None = None) -> ValueType:
    if inst is None:
        inst = Instantiation()
    else:
        inst = Instantiation(inst)
    return inst.eval(expr)