import numpy as np
import sys
from numbers import Number
from .Variable import Variable, Struct


class parentOperator:
    arglen = None
    arg_example = "this is a bug!"  # Should be set if arglen is not None
    null_value = 0  # default for add

    def __init__(self, *init_structure):
        self.init(init_structure)

    def init(self, *init_structure):
        self.original_structure = list(init_structure)
        self.structure = Struct({"number": self.null_value})

        for obj in self.original_structure:
            self.append_to_structure(obj)

        self = self.validate_init_structure()

    def append_to_structure(self, obj):
        if isinstance(obj, Number):
            self.structure["number"] = type(self).call(
                self, self.structure["number"], obj
            )
        elif obj in self.structure:
            self.structure[obj] += 1
        else:
            self.structure[obj] = 1

    def __call__(self, **kwargs):
        res = self.null_value

        for thing, coeff in self.structure.items():
            if isinstance(thing, parentFunction):
                res = self.call(thing(kwargs), coeff=coeff, res=res)
            elif isinstance(thing, Variable):
                if Variable in kwargs:
                    res = self.call(kwargs[thing], coeff=coeff, res=res)
                else:
                    """
                    This is for multivariable functions where variables should be set in call
                    f(a=2,r=4, x=np.linspace(0,1,11))
                    Could also be used for implisit variable calling, one or two
                    variable functions where we dont bother typing f(x=1,y=2)

                    For now defaults all variables to value of first val in kwargs
                    """
                    var = list(kwargs.values())[0]
                    res = self.call(var, coeff=coeff, res=res)
            elif thing == "number":
                res = self.call(coeff, res=res)
        return res


    def __str__(self):
        return "YEETING: Youshua-Elizian Extra-Terrestrial Inpastic-Normalized Graphisoding"
        if "string" in dir(self):
            if self.init_structure_are_numbers():
                return f"{self.call(self.init_structure)}"
            else:
                if len(self.init_structure) == 1:
                    return self.string(str(self.init_structure[0]))
                else:
                    return self.string([str(obj) for obj in self.init_structure])

        else:
            return f"this function does not have string support yet"


    def validate_init_structure(self):
        n = len(self.original_structure)
        if self.arglen is not None:

            msg = (
                f"{self.__class__} takes {self.arglen} arguments, but {n} were given. "
            )
            for l in range(
                97, 97 + self.arglen
            ):  # add n letter from a to msg: a,b,c,...
                msg += f"{chr(l)},"
            msg = msg[:-1] + " -> " + self.arg_example
            assert n == self.arglen, msg
        else:

            assert n > 1, f"{self.__class__} takes at least two arguments"

    def init_structure_are_numbers(self):
        # returns True if all the values in init_structure are numbers
        return (
            False in [isinstance(obj, Number) for obj in self.original_structure]
        ) is False


class add(parentOperator):
    arglen = None

    def call(self, *args, **kwargs):
        if "res" not in kwargs:
            res = self.null_value
        else:
            res = kwargs["res"]
        if "coeff" not in kwargs:
            coeff = 1
        else:
            coeff = kwargs["coeff"]
        for obj in args:
            res += obj * coeff

        return res

    def string(self, *args):
        print("NOPE")
        return "Leslie"
        resdic = {"number": 0}
        structure = self.init_structure

        while structure != []:
            obj = structure[0]

            if isinstance(obj, Variable):
                if obj not in resdic:
                    resdic[obj] = 1
                else:
                    resdic[obj] += 1
            elif isinstance(obj, number):
                resdic["number"] += obj
            elif isinstance(obj, parentOperator):
                if obj not in resdic:
                    resdic[obj] = 1
                else:
                    resdic[obj] += 1
                for obj2 in resdic:
                    pass

            structure = structure[1:]
        print(resdic)
        res = ""
        for thing, num in resdic.items():
            if thing == "number" and num != 0:
                res += f"{num} + "
            else:
                if num != 1:
                    res += f"{num}{str(thing)} + "
                else:
                    res += f"{str(thing)}"

        return res[:-3]
gad 

class sub(add):
    arglen = 2
    arg_example = "a - b"

    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "sub takes two arguments a,b -> a - b"
        return args[0] - args[1]


class mul(parentOperator):
    arglen = None
    null_value = 1

    def call(self, *args, **kwargs):
        if "res" not in kwargs:
            res = self.null_value
        else:
            res = kwargs["res"]
        if "coeff" not in kwargs:
            coeff = 1
        else:
            coeff = kwargs["coeff"]
        for obj in args:
            res *= obj ** coeff

        return res

    def string(self, *args):
        return "Yop"
        resdic = {"number": 0}
        structure = self.structure

        while structure != []:
            obj = structure[0]

            if isinstance(obj, Variable) or isinstance(obj, parentOperator):
                if obj not in resdic:
                    resdic[obj] = 1
                else:
                    resdic[obj] += 1
            elif isinstance(obj, number):
                resdic["number"] += obj

            structure = structure[1:]

        res = ""
        for thing, num in resdic.items():
            if thing == "number" and num != 1:
                res += f"{num} * "
            else:
                if num != 1:

                    res += f"{str(thing)}^{num} * "
                else:

                    res += f"{str(thing)} * "

        return res[:]


class div(parentOperator):
    arglen = 2
    arg_example = "a / b"

    def call(self, *args):
        args = args[0]
        # assert len(args) == 2, "div takes two arguments a,b -> a/b"
        return args[0] / args[1]

    def string(self, *args):
        return "TEMPORARY DIV STRING"

class pow(parentOperator):
    arglen = 2
    arg_example = "a^b"

    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "pow takes two arguments a,b -> a^b"
        return args[0] ** args[1]

    def string(self, string_arg):
        return f"{string_arg[0]}^{string_arg[1]}"


class sqrt(parentOperator):
    arglen = 1
    arg_example = "sqrt(a)"

    def call(self, *args):
        args = args[0]
        assert len(args) == 1, "pow takes one argument a -> sqrt(a)"
        return args[0] ** (1 / 2)

    def string(self, string_arg):
        return f"sqrt({string_arg})"