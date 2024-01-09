## 補助関数の集合ファイル
import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
import mypy.type_visitor
from projection import *
import help_func

def get_typename(t:mypy.types.Type) -> str:
    #print(type(t))
    if isinstance(t,mypy.types.Instance):
        #print("t.name = " +t.type.defn.name)
        return t.type.defn.name
    elif isinstance(t,mypy.types.UnboundType):
        #print("t.name = " + t.name)
        return t.name
    else:
        raise Exception
    
def get_typearg(t:mypy.types.ProperType,i:int) -> str:
    if isinstance(t,mypy.types.Instance):
        return get_typename(t.args[i])
    elif isinstance(t,mypy.types.UnboundType):
        return get_typename(t.args[i])
    else:
        raise Exception

# rolesOf(e) -> str
def rolesOf(n:mypy.nodes.Expression, typeChecker:mypy.checker.TypeChecker) -> list[str]:
    t0 = help_func.get_type(typeChecker, n)
    # t0 = n.accept(typeChecker.expr_checker) #nの型情報を取得する
    print(t0)
    if isinstance(t0,mypy.types.ProperType):
        if get_typename(t0) == "At":
            return [get_typearg(t0,1)]
        elif get_typename(t0) == "Channel":
            return [get_typearg(t0,1),get_typearg(t0,2)]
        else:
            raise Exception
    else:
        raise Exception
# rolesOf(type) -> str
def rolesOf_t(n:mypy.types.Type | None, typeChecker:mypy.checker.TypeChecker) -> list[str]:
    if isinstance(n,mypy.types.ProperType):
        if get_typename(n) == "At":
            return [get_typearg(n,1)]
        elif get_typename(n) == "Channel":
            return [get_typearg(n,1),get_typearg(n,2)]
        else:
            raise Exception
    else:
        raise Exception

# 構文木の情報から値だけを取り出す関数nameExpr
def nameExpr(e:mypy.nodes.Expression) -> str:
    if isinstance(e,mypy.nodes.NameExpr):
        print("e.name = " + e.name)
        return e.name
    elif isinstance(e,mypy.nodes.CallExpr):
        #print("e.callee = "+str(e.callee))
        return nameExpr(e.callee)
    else:
        raise Exception
    
def isNone(n:mypy.nodes.Node):
    if n is None:
        raise Exception
    else:
        pass

# listの[]を省略する関数 (list -> string)
def list_to_str(list:list) -> str:
    str_list = ','.join(str(x) for x in list)
    return str_list


# importからas部分をなくす
def get(tlist:list[tuple[str,str|None]]) -> list[str]:
    str_list:list[str] = []
    for tuple in tlist:
        str_list.append(tuple[0])
    return str_list

# merging
# 同じstm,expはそのまま残す,後に続くStmも同じでないとマージされない
def merge(s1:Stmt, s2:Stmt) -> Stmt: 
    # Block (list[stm])
    if isinstance(s1,Block) and isinstance(s2,Block):
        #merge_list:list[Stmt] = []
        # listの要素にマージの再帰を定義する
        # s=[s1, s2, s3 ...]  s'=[s1', s2', s3' ...]のとき
        # s ⊔ s' = [s1 ⊔ s1', s2 ⊔ s2', s3 ⊔ s3', ...]
        for t1 in s1.body:
            for t2 in s2.body:
                ms = merge(t1,t2)
        return ms
                #merge_list += [merge(t1,t2)]
        #return merge_list    
    # return
    elif isinstance(s1,Return) and isinstance(s2,Return):
        if s1.expr == s2.expr:
            return s1
        else:
            raise Exception
    # AsgOp
    elif isinstance(s1,OpAsg) and isinstance(s2,OpAsg):
        if s1.lvalue == s2.lvalue and s1.rvalue == s2.rvalue:
            return OpAsg(s1.lvalue,s1.rvalue,s1.op)
        else:
            raise Exception #merge(s1.stmt,s2.stmt)
    # e;s
    elif isinstance(s1,Es) and isinstance(s2,Es):
        if s1.expr == s2.expr:
            return s1
        else:
            raise Exception
    # if
    elif isinstance(s1,If) and isinstance(s2,If):
        #exps:list[str] = []
        #stms:list[Block] = []
        assert len(s1.expr) == len(s2.expr)# if文に直す
        if len(s1.expr) == 0:
            else_stm = Block([merge(s1.else_body,s2.else_body)],4)
        else:# len(s1.expr) != 0
            #for i in range(len(s1.expr)):
            #    exp1 = s1.expr[i]
            #    exp2 = s2.expr[i]
            #    stm1 = s1.body[i]
            #    stm2 = s2.body[i]
            #    exps += [merge_exp(exp1,exp2)]
            #    stms += [Block([merge(normalize(stm1),normalize(stm2))],4)]
            stm1 = s1.body.body[0]
            stm2 = s2.body.body[0]
            stms = Block([merge(normalize(stm1),normalize(stm2))],4)
        return If(s1.expr,stms,else_stm)
    # match
    elif isinstance(s1,Match) and isinstance(s2,Match):
        # guards:list[expression]
        # bodies: list[statement]
        # guardsが被ったらbodiesをマージして、被ってないならlistに加える
        # -> 新たなguards,bodiesとして定義し直せばいい
        if s1.subject == s2.subject:
            stm_list:list[Block] = [] # merge後のbodies
            newpatterns:list[str] = [] #merge後のpatterns
            # s1の各patternとs2のpatternを比較する
            for i in range(len(s1.patterns)):
                pat1 = s1.patterns[i]
                for j in range(len(s2.patterns)):
                    pat2 = s2.patterns[j]
                    if pat1 == pat2: #同じpatternならStmをmergeする
                        mbodies = merge(s1.bodies[i],s2.bodies[j])
                        stm_list += [Block([mbodies],2)]
                        newpatterns += [pat1]
                        # mergeしたものの元の要素は削除
                        s1.patterns.remove(pat1)
                        s1.bodies.remove(s1.bodies[i])
                        s2.patterns.remove(pat2)
                        s2.bodies.remove(s1.bodies[j])
            # patternが一致しなくて残ったものをリストに加える
            all_patterns = newpatterns + s1.patterns + s2.patterns
            all_stm = stm_list + s1.bodies + s2.bodies
            return Match(s1.subject,all_patterns,all_stm) 
        else:
            raise Exception
    # Raise
    elif isinstance(s1,Raise) and isinstance(s2,Raise):
        if s1.expr == s2.expr:
            return s1
        else:
            raise Exception
    #others
    else:
        raise Exception
            
def merge_exp(e1:str,e2:str) -> str:
    if e1 == e2:
        return e1
    else:
        raise Exception
    

# Noop
def noop(exp:str):# 射影後のExpression(String型)
    if "Unit.id" in exp:
        return "" # blank
    else:
        return exp # そのまま値を返す

#normalizing
def normalize(s:Stmt) -> Stmt: 
    if isinstance(s, Pass): # pass
        return s
    elif isinstance(s, Return): # return 
        return s
    elif isinstance(s, Es): # expressionStmt
        # ここでは stmt.expr が削る対象だったら s.stmt を return する
        return Es("")
    elif isinstance(s,OpAsg): # operator assignment
        print("get")
        if noop(s.lvalue) == noop(s.rvalue) == "":
            return OpAsg("","","")
        elif noop(s.lvalue) == "" and noop(s.rvalue) != "":
            return Es(s.rvalue)
        elif noop(s.lvalue) != "" and noop(s.rvalue) == "":
            return Es(s.lvalue)
        else: # noop(s.lvalue) != "" and noop(s.rvalue) != "":
            return s
    elif isinstance(s,Block):
        return normalize(s.body[0])
    #elif isinstance(s,If):
    #elif isinstance(s,Match):
    #elif isinstance(s,OpAsg):
    #    if noop(s.rvalue)
    # elif...
    assert False


def get_type(tc:mypy.checker.TypeChecker, expr:mypy.nodes.Expression) -> mypy.types.Type :
    try:
        return tc.lookup_type(expr)
    except KeyError as e:
        print("type not known:" + str(expr))
        raise e
