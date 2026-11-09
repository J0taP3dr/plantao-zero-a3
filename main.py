"""Plantão Zero — jogo educativo sobre verificação de informações."""

import sys

import pygame


pygame.init()

WIDTH, HEIGHT = 1000, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PLANTÃO ZERO | Central de Verificação")
clock = pygame.time.Clock()

FONT_XL = pygame.font.SysFont("arial", 48, bold=True)
FONT_LG = pygame.font.SysFont("arial", 30, bold=True)
FONT_MD = pygame.font.SysFont("arial", 22, bold=True)
FONT_BTN = pygame.font.SysFont("arial", 20, bold=True)
FONT_SM = pygame.font.SysFont("arial", 17)
FONT_XS = pygame.font.SysFont("arial", 14)

BG = (13, 22, 35)
PANEL = (24, 38, 56)
PANEL_LIGHT = (34, 52, 73)
BORDER = (57, 78, 101)
WHITE = (239, 244, 250)
MUTED = (166, 185, 202)
CYAN = (68, 205, 220)
GREEN = (83, 195, 139)
YELLOW = (245, 190, 77)
RED = (239, 100, 105)
PURPLE = (164, 137, 232)

# Casos fictícios criados para fins educativos; não representam notícias reais.
CASES = [
    {
        "tag": "SAÚDE PÚBLICA",
        "headline": "Mensagem afirma que postos do bairro vão fechar amanhã",
        "origin": "Encaminhada muitas vezes em um grupo de mensagens",
        "clues": [
            "A mensagem não informa quem publicou o aviso originalmente.",
            "Não apresenta data, documento ou link da prefeitura.",
            "O perfil oficial da unidade não publicou nenhum comunicado.",
        ],
        "best": "INVESTIGAR",
        "why": "Sem autoria e sem confirmação oficial, não compartilhe. Procure os canais oficiais ou telefone para a unidade.",
    },
    {
        "tag": "SERVIÇO PÚBLICO",
        "headline": "Prefeitura anuncia mudança no horário de coleta",
        "origin": "Página oficial da prefeitura, com data e comunicado",
        "clues": [
            "O aviso está no domínio oficial do município.",
            "A publicação informa bairros, datas e horários.",
            "O mesmo comunicado aparece nos canais oficiais verificados.",
        ],
        "best": "COMPARTILHAR",
        "why": "Há autoria identificável, informação completa e confirmação em canais oficiais. Compartilhe mantendo o contexto.",
    },
    {
        "tag": "SEGURANÇA",
        "headline": "Vídeo mostra suposto acidente ocorrido hoje na avenida central",
        "origin": "Vídeo curto sem legenda original",
        "clues": [
            "O vídeo não mostra placas ou pontos reconhecíveis do local.",
            "Uma busca pela data revela que o mesmo vídeo circulou há dois anos.",
            "Não há registro atual que confirme a legenda.",
        ],
        "best": "NÃO COMPARTILHAR",
        "why": "O vídeo antigo foi apresentado como se fosse atual. Não compartilhe uma legenda enganosa; procure a origem antes de republicar.",
    },
    {
        "tag": "EDUCAÇÃO",
        "headline": "Escola informa alteração no calendário de provas",
        "origin": "Imagem recortada enviada por um contato",
        "clues": [
            "O nome da escola aparece, mas não há assinatura ou data.",
            "A imagem está cortada e não mostra o restante do comunicado.",
            "A secretaria da escola ainda não confirmou a mudança.",
        ],
        "best": "INVESTIGAR",
        "why": "A imagem pode ser verdadeira ou estar desatualizada. Confirme com a escola antes de agir ou repassar.",
    },
    {
        "tag": "CONSUMO",
        "headline": "Loja oferece prêmio em dinheiro para quem clicar em um link",
        "origin": "Perfil desconhecido com endereço encurtado",
        "clues": [
            "O perfil imita o nome de uma marca conhecida.",
            "O link pede dados pessoais para liberar o prêmio.",
            "A promoção não aparece no site oficial da empresa.",
        ],
        "best": "NÃO COMPARTILHAR",
        "why": "Há sinais de golpe e coleta indevida de dados. Não clique nem encaminhe; denuncie a mensagem na plataforma.",
    },
    {
        "tag": "CLIMA",
        "headline": "Alerta de chuva forte para a região nesta tarde",
        "origin": "Defesa Civil municipal, publicado hoje",
        "clues": [
            "O alerta tem horário de emissão e área de abrangência.",
            "A Defesa Civil confirma a informação em seu canal oficial.",
            "A orientação inclui medidas práticas de segurança.",
        ],
        "best": "COMPARTILHAR",
        "why": "Um alerta confirmado pode proteger pessoas. Compartilhe a orientação completa e preserve a fonte e o horário.",
    },
    {
        "tag": "TECNOLOGIA",
        "headline": "Aplicativo popular vai começar a cobrar todos os usuários amanhã",
        "origin": "Postagem sem link para anúncio da empresa",
        "clues": [
            "O texto usa urgência, mas não cita uma fonte.",
            "Não há anúncio correspondente na central de ajuda do aplicativo.",
            "Uma mudança desse tipo precisaria de comunicação oficial aos usuários.",
        ],
        "best": "INVESTIGAR",
        "why": "Ausência de fonte não prova que a alegação é falsa. Procure o comunicado oficial antes de concluir ou compartilhar.",
    },
    {
        "tag": "COMUNIDADE",
        "headline": "Campanha de arrecadação divulga local e horário de entrega",
        "origin": "Organização comunitária identificada",
        "clues": [
            "A organização informa responsáveis e meios de contato.",
            "O endereço e o horário foram confirmados em mais de um canal da entidade.",
            "A publicação explica como os itens arrecadados serão utilizados.",
        ],
        "best": "COMPARTILHAR",
        "why": "A campanha tem responsáveis identificados e informações verificáveis. Compartilhe sem alterar os dados da organização.",
    },
]


def draw_text(text, font, color, x, y, center=False):
    image = font.render(text, True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def wrap(text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(text, font, color, x, y, max_width, line_gap=6):
    for line in wrap(text, font, max_width):
        draw_text(line, font, color, x, y)
        y += font.get_linesize() + line_gap
    return y


def panel(rect, color=PANEL, radius=16, border=None):
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(screen, border, rect, 2, border_radius=radius)


def button(rect, label, color, hotkey=None):
    hovered = rect.collidepoint(pygame.mouse.get_pos())
    panel(rect, color, 13, WHITE if hovered else None)
    shown = label if not hotkey else f"{label}  [{hotkey}]"
    font = FONT_BTN if FONT_BTN.size(shown)[0] <= rect.width - 22 else FONT_SM
    draw_text(shown, font, BG, rect.centerx, rect.centery, True)


def header(kicker, title, progress=None):
    draw_text(kicker, FONT_XS, CYAN, 42, 24)
    draw_text(title, FONT_LG, WHITE, 42, 49)
    if progress:
        number, total = progress
        draw_text(f"CASO {number:02d} DE {total:02d}", FONT_SM, MUTED, 800, 34)
        pygame.draw.rect(screen, BORDER, (800, 76, 156, 6), border_radius=3)
        pygame.draw.rect(screen, CYAN, (800, 76, int(156 * number / total), 6), border_radius=3)
    pygame.draw.line(screen, BORDER, (42, 101), (958, 101), 1)


def intro():
    while True:
        # INPUT: ler teclado, mouse ou fechamento da janela.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(350, 529, 300, 62).collidepoint(event.pos):
                    return

        # DRAW: desenhar a tela inicial após tratar as ações.
        screen.fill(BG)
        header("SIMULADOR DE REDAÇÃO • TREINAMENTO", "PLANTÃO ZERO")
        draw_text("CENTRAL DE VERIFICAÇÃO", FONT_LG, CYAN, 500, 169, True)
        paragraph(
            "Uma informação urgente acabou de chegar. Antes de agir, avalie a origem, procure evidências e decida o que fazer.",
            FONT_MD, WHITE, 170, 223, 680, 10,
        )
        panel((168, 351, 664, 137), PANEL, 18, BORDER)
        pygame.draw.rect(screen, YELLOW, (168, 367, 5, 101), border_radius=2)
        draw_text("OBJETIVO", FONT_SM, YELLOW, 199, 376)
        paragraph(
            "Proteja a confiança da comunidade: compartilhe informações confirmadas, investigue dúvidas e evite espalhar conteúdo enganoso.",
            FONT_SM, WHITE, 199, 409, 602, 6,
        )
        button(pygame.Rect(350, 529, 300, 62), "INICIAR PLANTÃO", GREEN)
        draw_text("ENTER para iniciar  •  ESC para sair", FONT_XS, MUTED, 500, 630, True)
        pygame.display.flip()
        clock.tick(60)


def play_case(case, number, total):
    while True:
        # INPUT e UPDATE: a escolha do jogador define a próxima tela.
        selected = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "SAIR"
                if event.key == pygame.K_a:
                    selected = "COMPARTILHAR"
                elif event.key == pygame.K_s:
                    selected = "INVESTIGAR"
                elif event.key == pygame.K_d:
                    selected = "NÃO COMPARTILHAR"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(42, 590, 285, 58).collidepoint(event.pos):
                    selected = "COMPARTILHAR"
                elif pygame.Rect(357, 590, 285, 58).collidepoint(event.pos):
                    selected = "INVESTIGAR"
                elif pygame.Rect(672, 590, 286, 58).collidepoint(event.pos):
                    selected = "NÃO COMPARTILHAR"
        if selected is not None:
            return selected

        # DRAW: notícias, pistas e opções, sem alterar a ordem dos casos.
        screen.fill(BG)
        header("PLANTÃO • ANÁLISE DE INFORMAÇÕES", case["tag"], (number, total))
        panel((42, 120, 916, 133), PANEL, 17, BORDER)
        draw_text("INFORMAÇÃO RECEBIDA", FONT_XS, CYAN, 67, 138)
        paragraph(case["headline"], FONT_LG, WHITE, 67, 176, 855, 4)

        panel((42, 267, 916, 76), PANEL_LIGHT, 15)
        draw_text("ORIGEM INFORMADA", FONT_XS, YELLOW, 67, 279)
        paragraph(case["origin"], FONT_SM, WHITE, 67, 310, 849, 2)

        draw_text("PISTAS PARA SUA ANÁLISE", FONT_MD, WHITE, 47, 363)
        for index, clue in enumerate(case["clues"], 1):
            y = 400 + (index - 1) * 48
            panel((42, y, 916, 43), PANEL, 11)
            pygame.draw.circle(screen, PURPLE, (68, y + 21), 12)
            draw_text(str(index), FONT_XS, BG, 68, y + 21, True)
            draw_text(clue, FONT_SM, WHITE, 94, y + 10)

        draw_text("QUAL É A SUA DECISÃO?", FONT_MD, WHITE, 47, 551)
        button(pygame.Rect(42, 590, 285, 58), "COMPARTILHAR", CYAN, "A")
        button(pygame.Rect(357, 590, 285, 58), "INVESTIGAR", YELLOW, "S")
        button(pygame.Rect(672, 590, 286, 58), "NÃO COMPARTILHAR", RED, "D")
        pygame.display.flip()
        clock.tick(60)


def feedback(case, selected):
    correct = selected == case["best"]
    while True:
        # INPUT: avançar somente após o jogador ver a explicação.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                return correct
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return correct

        # DRAW: manter o feedback educativo, destacando a resposta correta.
        screen.fill(BG)
        header("ANÁLISE DE DECISÃO", "RESULTADO DO CASO")
        panel((54, 130, 892, 131), PANEL, 18, BORDER)
        draw_text("SUA DECISÃO", FONT_XS, MUTED, 83, 153)
        draw_text(selected, FONT_LG, GREEN if correct else RED, 83, 188)
        draw_text("ACERTO" if correct else "REVEJA AS PISTAS", FONT_SM,
                  GREEN if correct else YELLOW, 728, 157)

        panel((54, 280, 892, 217), PANEL_LIGHT, 17)
        draw_text("POR QUE ESSA É A MELHOR ESCOLHA?", FONT_SM, YELLOW, 83, 304)
        paragraph(case["why"], FONT_MD, WHITE, 83, 347, 819, 9)
        if not correct:
            draw_text(f"DECISÃO RECOMENDADA: {case['best']}", FONT_SM, GREEN, 83, 456)

        draw_text("+100 PONTOS DE CONFIANÇA" if correct else "SEM PONTOS NESTA RODADA",
                  FONT_MD, GREEN if correct else RED, 500, 540, True)
        draw_text("ENTER ou clique para continuar", FONT_SM, MUTED, 500, 619, True)
        pygame.display.flip()
        clock.tick(60)


def ending(score, total):
    while True:
        # INPUT: reiniciar o plantão ou encerrar.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(355, 569, 290, 58).collidepoint(event.pos):
                    return

        # DRAW: balanço final das oito decisões.
        screen.fill(BG)
        header("PLANTÃO ENCERRADO", "BALANÇO DA REDAÇÃO")
        panel((188, 144, 624, 260), PANEL, 18, BORDER)
        draw_text(f"{score} / {total}", FONT_XL, CYAN, 500, 221, True)
        draw_text("DECISÕES RESPONSÁVEIS", FONT_MD, WHITE, 500, 276, True)
        draw_text(f"{score * 100} PONTOS DE CONFIANÇA", FONT_SM, GREEN, 500, 314, True)
        if score == total:
            message = "Excelente! Você protegeu a confiança da comunidade."
        elif score >= total // 2:
            message = "Bom trabalho. Continue verificando antes de compartilhar."
        else:
            message = "A pressa pode espalhar erros. Investigue as fontes."
        paragraph(message, FONT_SM, MUTED, 255, 358, 505, 5)
        panel((188, 429, 624, 107), PANEL_LIGHT, 16)
        paragraph(
            "Lembrete: ausência de prova não é prova de falsidade. Procure contexto, autoria, data e confirmação independente.",
            FONT_SM, WHITE, 219, 455, 561, 5,
        )
        button(pygame.Rect(355, 569, 290, 58), "REINICIAR", GREEN)
        draw_text("ENTER para reiniciar  •  ESC para sair", FONT_XS, MUTED, 500, 647, True)
        pygame.display.flip()
        clock.tick(60)


def main():
    while True:
        intro()
        score = 0
        for index, case in enumerate(CASES, 1):
            decision = play_case(case, index, len(CASES))
            if decision == "SAIR":
                pygame.quit()
                sys.exit()
            if feedback(case, decision):
                score += 1
        ending(score, len(CASES))


if __name__ == "__main__":
    main()
