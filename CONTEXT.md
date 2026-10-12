# Sueca

Jogo de cartas para duplas, em que o objetivo é somar mais que os 60 pontos de uma mão. Este contexto existe para fixar o vocabulário das regras — as ambiguidades do português ("rodada", "partida", "cortar") são fonte de bug quando viram nomes de estado.

## Mesa

**Mesa**:
Os quatro jogadores sentados de uma vez, e o Jogo que acontece entre eles. Uma mesa por servidor.
_Avoid_: sala, lobby, room

**Assento**:
Uma das quatro posições da mesa, em ordem de jogo: 0 → 1 → 2 → 3. Assentos de mesma paridade (0 e 2, 1 e 3) formam dupla. A, B, C e D no README são os assentos 0, 1, 2 e 3.
_Avoid_: lugar, slot, posição

## Baralho

**Carta**:
A combinação de um naipe e um valor.
_Avoid_: —

**Naipe**:
Paus, copas, espadas ou ouros. São quatro.
_Avoid_: —

**Valor**:
A força de pontuação de uma carta: Ás (11), Sete (10), Rei (4), Valete (3), Dama (2), Seis a Dois (0).
_Avoid_: força, peso

**Baralho**:
As 40 cartas de um jogo de quatro pessoas. Jogos de 6 ou 8 pessoas usam dois baralhos.
_Avoid_: deck

**Trunfo**:
O naipe da carta puxada na preparação da mão. Supera os outros três, e o Ás de trunfo é a carta mais forte do jogo. A carta do trunfo fica com o dador.

## Vaza

**Vaza**:
As quatro cartas jogadas, uma por jogador, a partir de uma carta puxada. Quem jogou a maior carta leva a vaza e passa a puxar a seguinte.
_Avoid_: rodada

**Puxar**:
Jogar a primeira carta de uma vaza, definindo o naipe que os demais devem seguir.
_Avoid_: sair, abrir, liderar

**Trunfar**:
Jogar trunfo por não ter o naipe puxado.
_Avoid_: cortar (reservado para o baralho)

## Mão

**Mão**:
Uma distribuição completa: embaralhar, cortar o baralho, puxar o trunfo, dez cartas para cada jogador, dez vazas, e a contagem dos pontos.
_Avoid_: rodada, partida

**Embaralhador**:
Quem embaralha a mão e puxa a sua primeira vaza. Na primeira mão é sorteado; nas seguintes, o papel anda um assento.
_Avoid_: dador

**Cortar o baralho**:
Dividir o baralho embaralhado antes da distribuição. Feito pelo parceiro do embaralhador.
_Avoid_: cortar para trunfar

**Dador**:
Quem distribui as dez cartas de cada jogador e pergunta ao parceiro se a carta puxada é a de cima ou a de baixo. A carta puxada é uma das dez cartas do dador, e fica com ele.
_Avoid_: distribuidor, carteador, dealer, dador de cartas

**Dupla**:
Os dois jogadores frente a frente, que somam os pontos em conjunto.
_Avoid_: equipe, time, par

## Pontuação

**Ponto**:
O valor somado das cartas conquistadas numa mão. O total é 120 por baralho.
_Avoid_: —

**Partida**:
A unidade de vitória ganha ao vencer uma mão: 1 numa vitória normal (61 a 90 pontos), 2 no quilo, 4 na bandeira. Uma mão de 60 a 60 não dá partida a ninguém.
_Avoid_: ponto

**Quilo**:
Vencer a mão com 91 a 119 pontos → 2 partidas.
_Avoid_: 2 quilos

**Bandeira**:
Vencer a mão com os 120 pontos → 4 partidas.
_Avoid_: —

**Jogo**:
A corrida até 4 partidas, entre as mesmas duas duplas de uma mesa. Bandeira e quilo encerram o jogo na hora.
_Avoid_: sessão, match
