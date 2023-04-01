from antlr4 import *
from os import sys
from funxLexer import funxLexer
from funxParser import funxParser
from funxVisitor import funxVisitor

from flask import Flask, render_template, request, redirect

#Funcions aritmetiques basiques (ampliar si cal)
def suma(x, y): return x + y
def resta(x, y): return x - y
def mul(x, y): return x * y
def div(x, y):
    if y == 0:
        raise Exception("Error: Divisió per 0")
    else:
        return x // y 
def power(x, y): return x ** y
def mod(x, y): return x % y

#Condicionals
def menor(x, y): return int(x < y)	
def menorI(x, y): return int(x <= y)
def mayor(x, y): return int(x > y)
def mayorI(x, y): return int(x >= y)
def igual(x, y): return int(x == y)
def nIgual(x, y): return int(x != y)


conditions = {'<': menor, '<=': menorI, '>': mayor,
              '>=': mayorI, '=': igual, '!=': nIgual}
              
arithmeticOp = {'+': suma, '-': resta, '*': mul, '/': div, '**': power, '%': mod}

app = Flask(__name__)

entry = []
result = []
functions = {}
counter = 0


@app.route("/", methods=['POST', 'GET'])  # templates
def funx_app():
    global counter
    if request.method == 'POST':
        counter += 1 #Número de operacion para mostrar en la interfaz
        input_stream = request.form.to_dict()
        entry.append(input_stream['content'])
        lexer = funxLexer(InputStream(input_stream['content']))
        token_stream = CommonTokenStream(lexer)
        parser = funxParser(token_stream)
        tree = parser.root()
        print("hola")
        if (parser.getNumberOfSyntaxErrors() > 0): #errors gramatica
            result.append("Error: Funcion o expresion mal definida")
        else:   
            try:
                visitor.visit(tree)
            except Exception as error:  #Error en el input
                result.append(error)

        # llamar otra vez al app route pero entrará al else
        return redirect("/")
    else:
        functionsShow = {}
        for i in functions:
            argu = ""
            for arg in functions[i].arguments:
                argu += arg + " "
            functionsShow[functions[i].name] = argu
        if (counter <= 5):
            counterJ = 0
        else:
            counterJ = counter - 5
        return render_template('base.html', func=functionsShow, ent=entry, res=result, count=counterJ)


class MyFunction:
    def __init__(self, name, arguments, instructions):
        self.name = name
        self.arguments = arguments
        self.instructions = instructions


class TreeVisitor(funxVisitor):

    def __init__(self):
        self.vars = {}
        self.stack = []

    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        output = "None"
        for f in l:
            if (f == ctx.expr()):
                output = self.visit(f)
            else:
                out = self.visit(f)
                if (out != None):
                    output = out
        result.append(output)

    def visitArith(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            return self.visit(l[0])
        else:
            operation = arithmeticOp[l[1].getText()]
            return operation(self.visit(l[0]), self.visit(l[2]))

    def visitIfcondition(self, ctx):
        l = list(ctx.getChildren())
        if (self.visit(l[1])):  # condition
            return self.visit(l[3])
        elif (len(l) == 6):  # si tenim else condition
            return self.visit(l[5])

    def visitElsecondition(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[2])

    def visitWhilecondition(self, ctx):
        l = list(ctx.getChildren())
        while (self.visit(l[1])):  # condition
            i = 3
            while (l[i].getText() != "}"):
                self.visit(l[i])
                i = i + 1

    def visitCondition(self, ctx):
        l = list(ctx.getChildren())
        condition = conditions[l[1].getText()]
        return condition(self.visit(l[0]), self.visit(l[2]))

    def visitFunction(self, ctx):
        l = list(ctx.getChildren())
        name = l[0].getText()
        if name in functions:
            raise Exception("Error: Funcion ya existe")  # exception
        argu = []
        inst = []
        i = 1
        while (l[i].getText() != "{"):
            argu.append(l[i].getText())
            i = i + 1
        i = i + 1
        while (l[i].getText() != "}"):
            inst.append(l[i])
            i = i + 1
        functions[name] = MyFunction(name, argu, inst)

    def visitFunctioncall(self, ctx):
        l = list(ctx.getChildren())
        argum = []
        name = l[0].getText()
        for i in range(1, len(l)):
            argum.append(self.visit(l[i]))
        return self.functionExecution(name, argum)

    def visitValor(self, ctx):
        l = list(ctx.getChildren())
        return int(l[0].getText())

    def visitVar(self, ctx):
        l = list(ctx.getChildren())
        if (l[0].getText() in self.vars):
            return int(self.vars[l[0].getText()])
        else:
            raise Exception("Error: Variable no existe")
            #return 0 variables sin valor = 0

    def visitPar(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    def visitExpresion(self, ctx):
        l = list(ctx.getChildren())
        value = str(self.visit(l[0]))
        return value

    def visitAssign(self, ctx):
        l = [i for i in ctx.getChildren()]
        self.vars[l[0].getText()] = self.visit(l[2])

    def functionExecution(self, name, arguments):
        if name not in functions:
            raise Exception("Error: Funció no existeix")

        elif len(arguments) != len(functions[name].arguments):
            raise Exception("Error: Arguments erronis")
        else:
            vars = {}
            for i in range(0, len(arguments)):
                argId = functions[name].arguments[i]
                vars[argId] = arguments[i]
            self.stack.append(self.vars)
            self.vars = vars
            i = 0
            retorno = None
            while (i != len(functions[name].instructions) and retorno == None):
                retorno = self.visit(functions[name].instructions[i])
                i = i + 1
            self.vars = self.stack.pop()
            return retorno


if __name__ == '__main__':
    visitor = TreeVisitor()
    app.run(debug=True)
