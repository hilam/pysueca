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

#### Roteiro de quatro terminais

Em um terminal, suba a mesa:

```bash
uv run pysueca-servidor
```

Nos outros quatro terminais, sente um jogador em cada um:

```bash
uv run pysueca Ana
uv run pysueca Bia
uv run pysueca Caio
uv run pysueca Duda
```

A ordem de conexão define os assentos 0 a 3 e, portanto, as duplas (0, 2) e (1, 3). Os defaults são `127.0.0.1:8765`; `--host` e `--porta` valem para os dois lados.

#### Duas máquinas

Na máquina da mesa, descubra o endereço dela na rede local:

```bash
hostname -I                  # Linux: o primeiro endereço é o da rede local
ipconfig getifaddr en0       # macOS
ipconfig                     # Windows: procure o "Endereço IPv4"
```

Suba o servidor aceitando conexão de fora (o `0.0.0.0` escuta em todas as interfaces; sem ele o bind é `127.0.0.1` e só a própria máquina conecta):

```bash
uv run pysueca-servidor --host 0.0.0.0
```

Em cada máquina, sente dois jogadores apontando para o endereço descoberto — troque `192.168.0.10` por ele:

```bash
uv run pysueca Ana --host 192.168.0.10
uv run pysueca Caio --host 192.168.0.10
```

```bash
uv run pysueca Bia --host 192.168.0.10
uv run pysueca Duda --host 192.168.0.10
```

O firewall da máquina da mesa pode bloquear a porta 8765: libere o `pysueca-servidor` na rede local ou a porta TCP de entrada.

#### O que o v1 entrega

- quatro jogadores em mesa, cada um no seu cliente Textual, na mesma máquina ou em duas;
- uma série até 4 partidas por mesa — bandeira vale 4 e encerra na hora, e as duplas são (0, 2) e (1, 3);
- uma mesa por servidor: mesa nova é reiniciar o servidor;
- a queda de um jogador congela a mesa e a reconexão com o mesmo nome traz o jogador de volta.

Fica fora do v1: recomeçar a série sem reiniciar o servidor, autenticação, TLS, mais de uma mesa por servidor e modo imagem.
