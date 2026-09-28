# L7 - Uso di un modulo scritto da noi
# Il file attivazioni.py deve trovarsi nella stessa cartella di questo file.
import attivazioni
from attivazioni import neurone, gradino

print(attivazioni.sigmoide(0))
print(attivazioni.relu(-3), attivazioni.relu(3))

# Neurone OR
for x1 in [0, 1]:
    for x2 in [0, 1]:
        print(x1, x2, "->", neurone([x1, x2], [1, 1], -0.5, gradino))
