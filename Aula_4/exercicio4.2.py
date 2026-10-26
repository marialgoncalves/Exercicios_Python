import numpy as np
from sklearn.ensemble import IsolationForest

acessos = np.array([
    [9, 1, 200],
    [10, 1, 500],
    [14, 2, 300],
    [11, 1, 250],
    [16, 1, 400],
    [3, 40, 900000],   
    [10, 1, 350],
    [15, 2, 280],
    [2, 55, 800000],    
])

modelo = IsolationForest(
    contamination=0.25,
    random_state=42
)

modelo.fit(acessos)

previsoes = modelo.predict(acessos)

for i, (acesso, previsao) in enumerate(zip(acessos, previsoes)):
    if previsao == -1:
        print(f"Amostra {i}: {acesso} -> ANOMALIA")
    else:
        print(f"Amostra {i}: {acesso} -> Normal")