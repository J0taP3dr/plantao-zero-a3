# Plantão Zero — Central de Verificação

Jogo educativo em **Python + Pygame** sobre combate à desinformação. O jogador atua em uma central comunitária de verificação e precisa decidir como lidar com mensagens recebidas.

## Objetivo social

Incentivar o pensamento crítico e a responsabilidade digital: verificar autoria, data, contexto e evidências antes de compartilhar informações. Os oito casos são **fictícios**, criados para a atividade acadêmica.

## Como jogar

Em cada caso, leia a mensagem, observe a origem e as três pistas e escolha:

- **Compartilhar**: há confirmação suficiente e a informação pode ser divulgada com contexto.
- **Investigar**: faltam evidências para confirmar a informação.
- **Não compartilhar**: há sinais de golpe, manipulação ou contexto enganoso.

Depois da escolha, o jogo explica o resultado. Cada resposta correta vale **100 pontos de confiança**; ao final são exibidos os acertos entre os oito casos e o total de pontos. A opção de reiniciar permite jogar novamente.

## Executar

É necessário ter o Python 3 instalado e um ambiente com suporte a janelas gráficas.

```bash
python -m pip install -r requirements.txt
python main.py
```

## Controles

| Tecla | Ação |
| --- | --- |
| `A` | Compartilhar |
| `S` | Investigar |
| `D` | Não compartilhar |
| `Enter` | Iniciar, continuar ou reiniciar |
| `Esc` | Sair (na tela de decisão, encerra o plantão) |
| Mouse | Clicar nos botões |

## Implementação e game loop

O projeto usa Pygame para desenhar as telas e ler eventos de teclado e mouse. Cada tela segue o ciclo **input → update → draw**:

1. **Input:** captura eventos (teclado, mouse e fechamento da janela).
2. **Update:** interpreta a ação, define a decisão ou avança de tela e atualiza o resultado/pontuação.
3. **Draw:** desenha a interface e atualiza a janela.

O arquivo `main.py` contém as funções `intro()` (abertura), `play_case()` (análise de cada mensagem), `feedback()` (explicação do resultado), `ending()` (balanço final) e `main()` (sequência dos oito casos). Essa divisão mantém a apresentação e o código simples.

## Integrantes

- Charlen Rogrigues da Silva — RA: 326137850
- Cristiano Coelho Fonseca Junker — RA: 32617935
- Gustavo Barboza Lage — RA: 326128126
- João Pedro Cassiano dos Santos — RA: 324127678

## Uso de inteligência artificial

Em 11/08/2026, o ChatGPT (OpenAI) foi utilizado como ferramenta de apoio à concepção e ao desenvolvimento inicial do Plantão Zero. Sua utilização envolveu a análise dos requisitos da atividade, a definição da proposta do jogo com foco no combate à desinformação, a estruturação das mecânicas e a elaboração inicial do código em Python com a biblioteca PyGame.

A ferramenta também auxiliou na organização dos arquivos do projeto, na elaboração do README, na divisão sugerida das responsabilidades entre os integrantes e na preparação do roteiro de apresentação e demonstração.

O conteúdo produzido com auxílio da IA deverá ser revisado, compreendido, testado e validado pelos integrantes do grupo, que permanecem responsáveis pelo resultado final do projeto.
