import index
#Arquivo, confianca=None, DesvioPadrao=None, N=1
valor1,valor2 = index.IntervaloDeConfiancaFile("ExemploDados.txt", 0.99)
print(str(valor1)+" - "+ str(valor2))
