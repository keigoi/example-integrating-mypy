from mypy.plugin import Plugin, MethodSigContext, MethodContext, FunctionSigContext, FunctionContext, AttributeContext, AnalyzeTypeContext, ClassDefContext
from mypy.types import FunctionLike, Type
from typing import Callable


def f(x: MethodSigContext) -> FunctionLike:
    return


class CustomPlugin(Plugin):
    def get_class_attribute_hook(self, fullname: str) -> Callable[[AttributeContext], Type] | None:
        if fullname.endswith("__matmul__"):
            print("get_class_attribute_hook: " + fullname)
        return None

    def get_attribute_hook(self, fullname: str) -> Callable[[AttributeContext], Type] | None:
        if fullname.endswith("__matmul__"):
            print("get_attribute_hook: " + fullname)
        return None

    def get_method_hook(self, fullname: str) -> Callable[[MethodContext], Type] | None:
        if fullname.endswith("__matmul__"):
            print("method_hook: " + fullname)
        return None

    def get_method_signature_hook(self, fullname: str) -> Callable[[MethodSigContext], FunctionLike] | None:
        if fullname.endswith("__matmul__"):
            print("method_signature_hook: " + fullname)
        return None

    def get_function_signature_hook(
        self, fullname: str
    ) -> Callable[[FunctionSigContext], FunctionLike] | None:
        if fullname.endswith("__matmul__"):
            print("function_signature_hook: " + fullname)
        return None

    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        if fullname.endswith("__matmul__"):
            print("function_hook: " + fullname)
        return None

    def get_type_analyze_hook(self, fullname: str) -> Callable[[AnalyzeTypeContext], Type] | None:
        return None

    def get_base_class_hook(self, fullname: str) -> Callable[[ClassDefContext], None] | None:
        return None

def make_objtyp(ctx:ClassDefContext) -> None:
    print(ctx.cls)

def plugin(version: str):
    print("plugin loading")
    return CustomPlugin
