# L4 - Il neurone a soglia
# Il neurone riceve due ingressi (0 oppure 1), li moltiplica per i pesi,
# somma i risultati e confronta la somma con una soglia:
# se la somma raggiunge la soglia l'uscita vale 1, altrimenti 0.

w1 = 1      # peso del primo ingresso
w2 = 1      # peso del secondo ingresso
soglia = 1.5

# Tabella di verità: le quattro combinazioni degli ingressi.
# caso vale 0, 1, 2, 3; x1 e x2 si ricavano con // e %:
# caso 0 -> (0, 0), caso 1 -> (0, 1), caso 2 -> (1, 0), caso 3 -> (1, 1)
print("x1 x2 | somma | y")
caso = 0
while caso < 4:
    x1 = caso // 2
    x2 = caso % 2
    somma = w1 * x1 + w2 * x2
    if somma >= soglia:
        y = 1
    else:
        y = 0
    print(f" {x1}  {x2} |  {somma:3}  | {y}")
    caso = caso + 1
