import hashlib
import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold

X = np.array([
    [500, 80, 0.1],
    [1200, 80, 0.5],
    [64, 22, 0.02],
    [64000, 4444, 10.0],
    [45000, 8080, 15.0],
    [60000, 31337, 20.0],
    [800, 443, 0.3],
    [300, 53, 0.05],
    [55000, 9999, 18.0],
    [200, 25, 0.2],
    [700, 443, 0.2],
    [52000, 6666, 17.0],
    [150, 53, 0.03],
    [58000, 4444, 19.0],
    [900, 80, 0.4],
])

y = np.array([
    0, 0, 0, 1, 1, 1, 0, 0, 1, 0,
    0, 1, 0, 1, 0
])

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(random_state=42))
])

grade = {
    "clf__n_estimators": [50, 100, 200],
    "clf__max_depth": [None, 5, 10]
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

busca = GridSearchCV(
    pipeline,
    param_grid=grade,
    cv=cv,
    scoring="accuracy"
)

busca.fit(X, y)
modelo = busca.best_estimator_

arquivo_modelo = "modelo_seguranca.pkl"

# Salva o modelo treinado
joblib.dump(modelo, arquivo_modelo)
print(f"Modelo salvo: {arquivo_modelo}")


def calcular_hash(caminho):
    sha256 = hashlib.sha256()

    with open(caminho, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(4096), b""):
            sha256.update(bloco)

    return sha256.hexdigest()


# Calcula e guarda o hash original
hash_original = calcular_hash(arquivo_modelo)
print(f"Hash SHA-256: {hash_original}")

# Recarrega e verifica a integridade
print("\nRecarregando e verificando integridade...")
modelo_carregado = joblib.load(arquivo_modelo)
hash_atual = calcular_hash(arquivo_modelo)

if hash_original == hash_atual:
    print("Hash confere: modelo íntegro.")

    amostra = np.array([[60000, 31337, 20.0]])
    previsao = modelo_carregado.predict(amostra)
    print(f"Previsão de teste: {previsao}")
else:
    print("ALERTA: arquivo do modelo foi modificado!")