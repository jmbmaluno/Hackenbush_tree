from fractions import Fraction
from turtle import Turtle
import tkinter as tk
from tkinter import font

#retirar todo o caminho que tem depois da posição retirada junto com seus filhos
def retirar_pos(string, i):
    saida = ""
    pilha = ['(']
    cont = 0

    for j in range(len(string)):
        if j == i:
            saida = saida + ' '
        else:
            if j > i:
                if cont == 0:
                    if string[j] == '(':
                        pilha.append('(')

                    elif string[j] == ')':
                        pilha.pop()
                        if len(pilha) == 0:
                            cont = 1
                    
                    if len(pilha) == 0:
                        saida = saida + string[j]
                    else:
                        saida = saida + ' '
                
                else:
                    saida = saida + string[j]
                
            else:   
                saida = saida + string[j]
    
    sem_vazios = ""

    saida = saida.replace(' ', '')

    j = 0
    while j <  (len(saida)):
        if saida[j] == '(' and saida[j+1] == ')':
            j = j + 1
        else:
            sem_vazios = sem_vazios + saida[j]
        
        j = j + 1

    
    return sem_vazios
    


def calcular_caminho(caminho):

    caminho = caminho.replace(' ', '')
    caminho = caminho.replace(')', '')
    caminho = caminho.replace('(', '')

    valor = 0
    cor_anterior = ''
    base = 2

    for cor in (caminho):
        if cor_anterior == '' or cor == cor_anterior:
            cor_anterior = cor

            if cor == 'B':
                valor = valor + 1
            elif cor == 'R':
                valor = valor - 1

        else:
            cor_anterior = "N" #não é levada mais em consideração

            if cor == "B":
                valor = valor + 1/base
            elif cor == 'R':
                valor = valor - 1/base
            
            base = base * 2

    return valor

#Se a árvore tiver apenas um filho e seu filho tiver apenas um filho e assim por diante também devo considerar como caminho
def tem_subarvore(string):
    cont = 0

    pilha = []
    i = 0
    
    while i < len(string) and string[i] != 'R' and string[i] != 'B':
        i = i + 1

    if i == len(string):
        return False

    i = 0

    while i < len(string):

        if string[i] == '(':
            i = i + 1

            filho = ""
            pilha.append('(')

            while(len(pilha) > 0):
                
                if(string[i] == '('):
                    pilha.append('(')
                
                elif(string[i] == ')'):
                    pilha.pop()

                    if len(pilha) == 0:
                        cont = cont + 1

                if len(pilha) > 0:
                    filho = filho + string[i]

                i = i + 1
            
            if tem_subarvore(filho) == True:
                return True
        
        i = i + 1
        
    if cont <= 1:
        return False
    
    return True


def obter_red_blue(arvore):
    qtde_red = 0
    qtde_blue = 0

    blue = []
    red = []

    qtde_blue = arvore.count('B')
    qtde_red = arvore.count('R')
    
    tamanho = len(arvore)

    i = tamanho - 1

    while qtde_blue != 0:
        sub = arvore[:]
        while i >= 0 and arvore[i] != 'B':
            i = i - 1

        sub = retirar_pos(sub, i)
        i = i - 1

        blue.append(calcular_arvore(sub)) 
    
        qtde_blue = qtde_blue - 1


    while qtde_red != 0:
        i = tamanho - 1
        
        while i >= 0 and arvore[i] != 'R':
            i = i - 1

        sub = retirar_pos(arvore, i)

        red.append(calcular_arvore(sub)) 
        
        qtde_red = qtde_red - 1

    return red, blue


def calcular_arvore(arvore):

    if tem_subarvore(arvore) == False:
        return calcular_caminho(arvore)
    
    red,blue = obter_red_blue(arvore)

    if len(red) == 0:
        return max(blue) + 1
    
    if len(blue) == 0:
        return min(red) - 1


    if abs(min(red) - max(blue)) > 1:
        if abs(min(red)) < abs(max(blue)):
            return min(red) + 1
        else:
            return int(max(blue)) + 1

    else:
        return (max(blue)+min(red))/2



######################
# DESENHAR A ARVORE  #
######################

#Ajeitar o angulo da turtle
def desenhar(arvore):

    arvore = arvore.replace(' ', '')

    #Configurando turtle
    t = Turtle()
    t.screen.screensize(2000,2000)
    t.hideturtle()

    t.screen.title("Plotando Hackenbush")

    lapis_size = 5
    t.pensize(lapis_size)

    t.penup()
    t.goto(0,-250)
    t.pendown()

    t.color('brown')
    t.forward(200)
    t.backward(400)

    t.penup()
    t.forward(200)
    t.pendown()

    t.left(90)

    pilha= []

    passo = 30
    for i in arvore:
        
        if i == 'B':
            t.dot(lapis_size*2)

            t.penup()
            t.forward(lapis_size)
            t.pendown()

            t.color('blue')
            t.forward(passo)
            

        elif i == 'R':
            t.dot(lapis_size*2)

            t.penup()
            t.forward(lapis_size)
            t.pendown()

            t.color('red')
            t.forward(passo)
            

        elif i == '(':
            pilha.append((t.pos(), t.heading()))
            t.left(30)

        elif i == ')':
            pos,degree = pilha.pop()
            t.setheading(degree)
            t.right(60)
            t.penup()
            t.goto(pos)
            t.pendown()

    
    #Escrevendo resultado
    t.penup()
    t.color('black')
    t.goto(-110,-300)
    t.pendown()
    texto = "Valor da árvore: " + str(Fraction(calcular_arvore(arvore))) + "\n" + "Árvore: " + arvore

    t.write(texto,font = ("Arial", 14, 'normal'), align='center')

    t.screen.mainloop()


arvore = "B B R (R) (B) "


def preencher_string():
    texto_inserido = campo_texto.get()
    texto_preenchido.set(texto_inserido)
    janela.destroy()

# Criar a janela
janela = tk.Tk()
janela.title("Preencher String")
janela.geometry("400x150")


# Variável para armazenar o texto inserido
texto_preenchido = tk.StringVar()

# Criar um rótulo
rotulo = tk.Label(janela, text="Digite sua Hackenbush Tree:", font=8)
rotulo.pack(pady=10)

# Criar um campo de entrada
campo_texto = tk.Entry(janela, font=3)
campo_texto.pack(pady=5)

# Criar um botão
botao = tk.Button(janela, text="Confirmar", command=preencher_string)
botao.pack(pady=10)

# Iniciar a interface gráfica
janela.mainloop()

desenhar(texto_preenchido.get().upper())