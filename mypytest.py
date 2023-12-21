import sys
import mypycustom
#import mypy
import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
#from mypy.plugin import CheckerPluginInterface
#from typing import Optional, cast
import mypy.type_visitor
#import help_func
#import pro_e
import pro_s
import pro_class
import pro_all

# result <- ASTが保存されている
result : mypy.build.BuildResult | None = mypycustom.main([
    "--show-traceback", 
    #"--verbose",
    "--custom-typeshed", "./typeshed",
    "ex.py"
    ])

if result is None: # Noneを省く
    sys.exit(1)

src = result.graph["ex"] #木構造
typechecker = src.type_checker()

if src.tree is None: # Noneを省く
    sys.exit(1)

# projectionを読み込む
for stm in pro_all.projection_all(src.tree.defs,"A",typechecker):
    print(stm)

#for stm in pro_class.projection_class(src.tree.defs,"A",typechecker):
#    print(stm)


#print(pro_s.projection_block(src.tree.defs,"A",typechecker))

#for d in src.tree.defs:
#    v = MyVisitor(src.type_checker())
#    d.accept(v)
#    if isinstance(d,mypy.types.Instance):
#       pass
#for d in src.tree.defs:
#    pro_s.projection_block(src.tree.defs,r:str,tc:mypy)