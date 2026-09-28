# L8 - Esempi: classi e oggetti


class Rettangolo:
    """Un rettangolo definito da base e altezza."""

    def __init__(self, base, altezza):
        self.base = base            # attributo
        self.altezza = altezza      # attributo

    def area(self):
        return self.base * self.altezza

    def perimetro(self):
        return 2 * (self.base + self.altezza)

    def scala(self, fattore):
        """Modifica le dimensioni del rettangolo."""
        self.base = self.base * fattore
        self.altezza = self.altezza * fattore


r1 = Rettangolo(8, 5)      # prima istanza
r2 = Rettangolo(2, 3)      # seconda istanza, indipendente dalla prima

print("r1:", r1.base, r1.altezza, "area", r1.area(), "perimetro", r1.perimetro())
print("r2:", r2.base, r2.altezza, "area", r2.area())

r1.scala(2)
print("r1 dopo scala(2):", r1.base, r1.altezza, "area", r1.area())
print("r2 non cambia:", r2.base, r2.altezza)

print(type(r1))


class Contatore:
    """Un oggetto con uno stato che cambia nel tempo."""

    def __init__(self):
        self.valore = 0

    def incrementa(self):
        self.valore = self.valore + 1


c = Contatore()
for _ in range(3):
    c.incrementa()
print("contatore:", c.valore)
