import sys
import mypycustom
import mypy
# import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
from mypy.plugin import CheckerPluginInterface
import mypy.type_visitor
import mypy.types

result: mypy.build.BuildResult = mypycustom.main(["--show-traceback",
                                                  #  "--verbose",
                                                  "--custom-typeshed", "./typeshed",
                                                  "ex1.py"])


class MyVisitor(mypy.visitor.NodeVisitor[None]):
    type_checker: mypy.checker.TypeChecker

    def __init__(self, checker: mypy.checker.TypeChecker):
        self.type_checker = checker

    def visit_func_def(self, defn: mypy.nodes.FuncDef) -> None:
        defn.body.accept(self)

    def visit_block(self, b: mypy.nodes.Block) -> None:
        print("visit block")
        for s in b.body:
            s.accept(self)

    def visit_return_stmt(self, s: mypy.nodes.ReturnStmt) -> None:
        print("visit return stmt")
        print(s.expr.accept(self.type_checker.expr_checker))
        t: mypy.types.Type = s.expr.accept(
            self.type_checker.expr_checker)  # たとえば t = rstr[A] なら
        print("printing class of:" + str(t))
        print(type(t))  # mypy.types.Instance

        if isinstance(t, mypy.types.Instance):
            print("printing class of t.args:" + str(t.args))
            print(type(t.args))
        pass


if result is None:
    sys.exit(1)

src = result.graph["ex1"]

for d in src.tree.defs:
    v = MyVisitor(src.type_checker())
    d.accept(v)
    if isinstance(d, mypy.types.Instance):
        pass
