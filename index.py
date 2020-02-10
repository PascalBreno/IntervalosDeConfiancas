import math


# region Tabelas
def TabelaNormal(confianca):
    confianca = confianca / 2
    confianca = float(confianca)

    # region Criação da Tabela para analisar a confiança
    import scipy.stats as st
    Cima = ['0', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    file = open("Tabela.txt", 'r')
    dados = {}
    i = 0
    valor = None
    for index, number in enumerate(file):
        linha = number.split(" ")
        if (index != 0):
            for i, numero in enumerate(linha):
                if (i == 0):
                    dados[str(numero + Cima[i])] = 0
                    Valor = numero
                else:
                    dados[str(Valor + Cima[i])] = numero
    # endregion

    # region Verificação na tabela para saber qual o valor resgatar
    menor = 10
    for key in dados:
        if (abs(float(dados[key]) - confianca) < menor):
            x = key
            menor = abs(float(dados[key]) - confianca)
    confianca = float(x)
    # endregion

    return confianca


def TabelaStuden(p, confianca):
    Cima = ['0', '0.95', '0.90', '0.80', '0.70', '0.60', '0.50', '0.40', '0.30', '0.20', '0.10', '0.05', '0.02 ',
            '0.01', '0.001']
    file = open("TabelaTStudent.txt", 'r')
    dados = {}
    i = 0
    valor = None
    for index, number in enumerate(file):
        linha = number.split(" ")
        if (index != 0):
            for i, numero in enumerate(linha):
                if (i == 0):
                    dados[str(numero + Cima[i])] = 0
                    Valor = numero
                else:
                    dados[str(Valor + Cima[i])] = numero

    # region Verificar qual numero retornar da TabelaTStudent
    # endregion
    return float(dados[(str(confianca) + str(p))])


# endregion

# region Frequencia e Somatorios
def Frequencia(dados):
    newDados = {}
    for item in dados:
        if item in newDados:
            newDados[item] = newDados[item] + 1
        else:
            newDados[item] = 1
    return newDados


def SomatorioFrequencia(dados):
    total = 0
    for key in dados:
        total = total + float(key) * dados[key]
    return total


def SomatorioMediaAmostra(dados, media):
    total = 0
    for key in dados:
        total = total + dados[key] * ((float(key) - media) ** 2)
    return total


# endregion

def IntervaloDeConfiancaFile(Arquivo, confianca=None, DesvioPadrao=None, N=1):
    import statistics

    # region Coleta de dados
    dados = []
    file = open(Arquivo, 'r')
    for number in file:
        dados.append(float(number))
    x = float(statistics.mean(dados))
    n = len(dados)
    # endregion

    dadosF = Frequencia(dados)
    if (len(dadosF) == 2):
        # Verifica-se que os dados são apenas binários, ou seja, sucesso e falhas. Sendo assim, se utilizará do método para proporção populacional
        p = dadosF[1.0] / len(dados)
        q = dadosF[0.0] / len(dados)
        if (len(dados)) * p >= 5 and (len(dados) * q) >= 5:
            # Utilizar a tabela normal
            fatordeCorrecao=1
            if(N!=1 and (len(dados)/N)>0.05):
                fatordeCorrecao = math.sqrt((N-n/N-1))
            Erro = TabelaNormal(confianca)*(math.sqrt(p*(1-p)/len(dados))*fatordeCorrecao)

        else:
            print('Faz outro algo')
        ICMais=p+Erro
        ICMenos=p-Erro
        return ICMais, ICMenos
    else:
        # region IC média com desvio padrão
        if (DesvioPadrao):
            Z = TabelaNormal(confianca)
            Erro = Z * (DesvioPadrao / (math.sqrt(n)))
            ICMais = x + Erro
            ICMenos = x - Erro
        # endregion

        # region IC média sem desvio padrão
        else:
            MediaAmostral = SomatorioFrequencia(dadosF) / len(dados)
            VariancaAmostral = math.sqrt((SomatorioMediaAmostra(dadosF, MediaAmostral)) / (len(dados) - 1))
            p = round(1 - confianca, 2)
            grauDeLiberdade = len(dados) - 1
            Tcritico = TabelaStuden(p, grauDeLiberdade)
            ICMais = MediaAmostral + Tcritico * VariancaAmostral / math.sqrt(n)
            ICMenos = MediaAmostral - Tcritico * VariancaAmostral / math.sqrt(n)
        # endregion

        return ICMais, ICMenos


def IntervaloDeConfiancaComDesvio(x, n, DesvioPadrao, confianca):
    # region IC média com DesvioPadrao
    Z = TabelaNormal(confianca)
    Erro = Z * (DesvioPadrao / (math.sqrt(n)))
    ICMais = x + Erro
    ICMenos = x - Erro
    # endregion
    return ICMais, ICMenos


def IntervaloDeConfiancaSemDesvio(x, n, confianca):
    # region IC média sem DesvioPadrao
    Z = TabelaStuden(confianca)
    Erro = Z * (DesvioPadrao / (math.sqrt(n)))
    ICMais = x + Erro
    ICMenos = x - Erro
    # endregion
    return ICMais, ICMenos
