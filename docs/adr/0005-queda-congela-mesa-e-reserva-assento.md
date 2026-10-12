# Queda de jogador congela a mesa e reserva o assento

A vaza exige as quatro cartas, então um assento mudo trava o jogo: quando uma conexão cai, o servidor avisa a mesa, congela o jogo e reserva o assento; reconectar com o mesmo nome devolve o jogador ao assento com um snapshot. O nome é a identidade, e um nome já sentado e ativo é recusado com "nome em uso". Rejeitamos desistência por timer e bot substituto: exigem relógio no servidor, regra para a vaza interrompida e um jogador virtual inteiro — ficam para quando houver mais de uma mesa.
