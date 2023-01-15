# pysueca

TUI para jogo de cartas Sueca

## Jogos de cartas/Sueca

Sueca é um jogo de cartas para quatro pessoas, no mínimo. E uma quantidade par de pessoas, no total.

### Regras

Os jogadores dividem-se em duplas. Os parceiros não podem fiucar lado a lado, e ficarão posicionados frente a frente, quando possível.

Para quatro jogadores, usa-se 1 baralho, 6 ou 8 participantes, 2 baralhos, e assim por diante.

As cartas do jogo, dos quatro naipes, somam um total de 120 pontos: Ás (11), Sete (10), Rei (4), Valete(3), Dama (2), Seis, Cinco, Quatro, Três e Dois (0)

O objetivo do jogo é fazer mais pontos.

### Dinâmica

1. Sorteio para quem embaralha
2. Dupla do embaralhador corta o baralho
3. Alguém da outra dupla pergunta para seu parceiro se é para puxar a carta de cima ou a de baixo. O naipe da carta puxada é o trunfo. Vale lembrar que a carta puxada fica com quem a puxou. O naipe de trunfo é o melhor naipe, assim sendo o Ás de trunfo é a melhor carta do jogo.
4. Distribuem-se 10 cartas para cada jogador
	1.  Se a pessoa diz "cima", o indivíduo que perguntou dá as cartas para si primeiro e depois dá para os outros dá direita para a esquerda;
	2.  Se for "baixo" dão-se as cartas da esquerda para a direita deixando a si mesmo por último.
5. A pessoa que cortou (dupla do embaralhador) puxa uma carta e os outros têm que jogar o mesmo naipe. Se algum jogador não tiver o naipe pode jogar o naipe de trunfo se quiser. Quem jogar a carta maior leva a rodada. Quem cortar (com trunfo) maior leva. Se a pessoa tiver o naipe puxado ela não pode jogar outro naipe. Se alguém a pegar fazendo isso essa pessoa perderá o jogo. 
6. Quem leva a rodada puxa outra carta.
7. Quando as cartas acabam contam-se os pontos. O total é de 120 pontos, por baralho usado. 
8. Se alguém fizer o máximo de pontos, ganha de bandeira, que vale 4 partidas. 
9. Se ganhar de mais de 3/4 da pontuação máxima (90/120 pontos), ganha de 2 quilos, que valem duas partidas. 
10. Se fizer mais que metade (60/120), ganha-se normalmente, valendo 1 partida. 
11. Oficialmente jogam-se 4 partidas.

### Desenvolvimento

* Utilizar a biblioteca Textual
* Se possível, não utilizar bibliotecas de terceiros, exceto a própria Textual
* Permitir que seja jogado online entre jogadores em computadores diferentes, usando sockets
