import sys
import mypycustom
import mypy
# import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
from mypy.plugin import CheckerPluginInterface
import mypy.type_visitor

result : mypy.build.BuildResult = mypycustom.main(["--show-traceback", "--verbose", "ex1.py"])

class MyVisitor(mypy.visitor.NodeVisitor[None]):
    type_checker : mypy.checker.TypeChecker

    def __init__(self, checker:mypy.checker.TypeChecker):
        print("init success")
        self.type_checker = checker
    
    def visit_func_def(self, defn: mypy.nodes.FuncDef) -> None:
        defn.body.accept(self)

    def visit_block(self, b: mypy.nodes.Block) -> None:
        print("visit block")
        for s in b.body:
            s.accept(self)

    def visit_return_stmt(self, s :mypy.nodes.ReturnStmt) -> None:
        print("visit return stmt")
        print(s.expr.accept(self.type_checker.expr_checker))
        pass

src = result.graph["ex1"]

for d in src.tree.defs:
    v = MyVisitor(src.type_checker())
    d.accept(v)
