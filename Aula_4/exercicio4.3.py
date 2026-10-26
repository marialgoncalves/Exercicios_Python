from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score
)

y_verdadeiro = [0,0,0,0,0,0,0,0,1,1]
y_previsto   = [0,0,0,0,0,0,0,0,0,1]

matriz = confusion_matrix(y_verdadeiro, y_previsto)

precisao = precision_score(y_verdadeiro, y_previsto)
recall = recall_score(y_verdadeiro, y_previsto)
f1 = f1_score(y_verdadeiro, y_previsto)
acuracia = accuracy_score(y_verdadeiro, y_previsto)

print("Matriz:")
print(matriz)
print(f"Precisão: {precisao:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1: {f1:.2f}")
print(f"Acurácia: {acuracia:.2f}")
print("\nInterpretação:")
print("A acurácia de 90% parece boa, mas pode esconder ataques que foram classificados como normais.")
print("O recall de 50% mostra que metade dos ataques não foi detectada pelo modelo.")
print("Em um SOC, detectar os ataques é mais importante, então o recall deve ser priorizado.")