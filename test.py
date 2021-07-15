class Teste:
    var_1 = 0

    def __init__(self, var_2):
        self.var_2 = var_2

    def alter_var_2(self, valor):
        self.var_2 = valor


a = Teste(2)
print(a.var_2)
a.alter_var_2(15)
print(a.var_2)
