import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

X = np.array([
    [1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [2, 1, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [8, 1, 1, 1, 5],
    [12, 0, 1, 1, 8],
    [6, 1, 1, 1, 3],
    [10, 1, 1, 1, 6],
    [0, 0, 0, 0, 0],
    [15, 1, 1, 1, 9],
])

# 0 = legítimo
# 1 = phishing
y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1])

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

modelo = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

acuracia = accuracy_score(y_test, y_pred)

print("Acurácia:", acuracia)
print("\nRelatório de classificação:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Legítimo", "Phishing"],
        zero_division=0
    )
)

# Teste 
novo_email = np.array([[11, 1, 1, 1, 7]])
previsao = modelo.predict(novo_email)

print("\nCaso novo [11, 1, 1, 1, 7]:")

if previsao[0] == 1:
    print("Phishing")
else:
    print("Legítimo")