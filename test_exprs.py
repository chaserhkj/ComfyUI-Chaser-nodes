from sexpdata import loads, Symbol
from exprs_eval import eval_s_expr

def expect_result(result, expr_str, inst=None):
    assert eval_s_expr(loads(expr_str), inst) == result


expect_result(3,"(+ 1 2)") 
expect_result(6,"(+ 1 2 3)") 
expect_result(4,"(+ 1 2 (- 5 4))") 
expect_result(4,"(+ 1 2 (sub 5 4))") 
expect_result(4,"(add 1 2 (sub 5 4))") 
expect_result(8,"(* 2 4)") 
expect_result(6.0,"(* 1.5 4)") 
expect_result(3.5,"(/ 7 2)") 
expect_result(3,"(floor (/ 7 2))") 
expect_result(14.0,"(float (* 7 2))") 
expect_result(14.0,"(float (* 7 arg0))", {Symbol("arg0"):2}) 
expect_result(10,"(up-bound 10 (* 7 arg0))", {Symbol("arg0"):2}) 
expect_result(14,"(low-bound 10 (* 7 arg0))", {Symbol("arg0"):2}) 
expect_result(20,"(low-bound 20 (* 7 arg0))", {Symbol("arg0"):2}) 
