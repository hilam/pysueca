# pysueca

TUI para jogo de cartas Sueca

## Jogos de cartas/Sueca

Sueca é um jogo de cartas para quatro pessoas, no mínimo. E uma quantidade par de pessoas, no total.

### Regras

Os jogadores dividem-se em duplas. Os parceiros não podem ficar lado a lado: sentam-se frente a frente.

Para quatro jogadores usa-se 1 baralho; para 6 ou 8 participantes, 2 baralhos, e assim por diante.

As cartas do jogo, dos quatro naipes, somam um total de 120 pontos: Ás (11), Sete (10), Rei (4), Valete (3), Dama (2), Seis, Cinco, Quatro, Três e Dois (0)

O objetivo é fazer mais pontos que a dupla adversária.

#### Unidades do jogo

- **Vaza**: as quatro cartas jogadas, uma por jogador. Quem joga a maior carta leva a vaza e puxa a seguinte.
- **Mão**: uma distribuição completa — embaralhar, cortar o baralho, puxar o trunfo, dez cartas para cada um, dez vazas e a contagem dos pontos.
- **Partida**: o que se ganha ao vencer uma mão — 1 numa vitória normal, 2 num quilo, 4 numa bandeira.
- **Jogo**: a corrida até 4 partidas. A bandeira, que vale 4, encerra o jogo na hora.

### Dinâmica

Sentando os jogadores em círculo na ordem A → B → C → D, com as duplas (A, C) e (B, D):

1. Sorteia-se quem embaralha. Na primeira mão, é A.
2. O parceiro do embaralhador (C) corta o baralho.
3. O dador (D), adversário do embaralhador, pergunta ao seu parceiro (B) se é para puxar a carta de cima ou a de baixo. Quem responde é B.
4. O naipe da carta puxada é o trunfo, e a carta fica com o dador. O naipe de trunfo é o melhor naipe, assim sendo o Ás de trunfo é a melhor carta do jogo.
5. Distribuem-se 10 cartas para cada jogador, começando ou terminando pelo dador:
	1.  Se a resposta foi "cima", o dador dá as cartas para si primeiro e depois dá para os outros da direita para a esquerda;
	2.  Se foi "baixo", dão-se as cartas da esquerda para a direita, deixando a si mesmo por último.

	A carta do trunfo é a primeira (cima) ou a última (baixo) carta que o dador recebe.
6. O embaralhador (A) puxa a primeira vaza: joga uma carta, e os outros têm que jogar o mesmo naipe, se o tiverem.
7. Quem não tiver o naipe puxado pode jogar qualquer outra carta, inclusive trunfo — é o que se chama **trunfar**. Quem tem o naipe puxado é obrigado a jogá-lo.
8. Quem jogou a maior carta leva a vaza e puxa a seguinte. Trunfo supera os outros três naipes; entre trunfos, vale a maior carta de trunfo.
9. Quando as cartas acabam, contam-se os pontos: somam-se os valores das cartas de cada dupla. O total é de 120 pontos, por baralho usado.
10. Na mão seguinte, cada papel anda um assento: B embaralha e puxa a primeira vaza, D corta, A é o dador e C responde.

### Pontuação

| Pontos da dupla | Resultado | Partidas |
| --- | --- | --- |
| 120 | **Bandeira** | 4 |
| 91 a 119 | **Quilo** | 2 |
| 61 a 90 | vitória normal | 1 |
| 60 (empate) | ninguém vence a mão | 0 |

Ganha o jogo a dupla que fizer 4 partidas primeiro. A bandeira vale 4 e encerra o jogo na hora.

### Desenvolvimento

* Utilizar a biblioteca Textual
* Se possível, não utilizar bibliotecas de terceiros, exceto a própria Textual
* Permitir que seja jogado online entre jogadores em computadores diferentes, usando sockets

No jogo online, uma jogada ilegal (não seguir o naipe puxado) é simplesmente **rejeitada pelo servidor** — ela nem chega à mesa. A regra de "perder o jogo" por ser pego existe só para o jogo de mesa, onde não há árbitro.
