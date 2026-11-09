import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PLANTAO ZERO | Central de Verificacao")
clock = pygame.time.Clock()

FONT_XL = pygame.font.SysFont("arial", 48, bold=True)
FONT_LG = pygame.font.SysFont("arial", 30, bold=True)
FONT_MD = pygame.font.SysFont("arial", 22, bold=True)
FONT_SM = pygame.font.SysFont("arial", 17)
FONT_XS = pygame.font.SysFont("arial", 14)

BG = (13, 22, 35)
PANEL = (24, 38, 56)
PANEL_LIGHT = (34, 52, 73)
WHITE = (239, 244, 250)
MUTED = (160, 177, 194)
CYAN = (68, 205, 220)
GREEN = (83, 195, 139)
YELLOW = (245, 190, 77)
RED = (239, 100, 105)
PURPLE = (164, 137, 232)

# Casos ficticios criados para fins educativos. Nao representam noticias reais.
CASES = [
    {
        "tag": "SAUDE PUBLICA",
        "headline": "Mensagem afirma que postos do bairro vao fechar amanha",
        "origin": "Encaminhada muitas vezes em um grupo de mensagens",
        "clues": [
            "A mensagem nao informa quem publicou o aviso originalmente.",
            "Nao apresenta data, documento ou link da prefeitura.",
            "O perfil oficial da unidade nao publicou nenhum comunicado."
        ],
        "best": "INVESTIGAR",
        "why": "Sem autoria e sem confirmacao oficial, nao compartilhe. Procure os canais oficiais ou telefone para a unidade."
    },
    {
        "tag": "SERVICO PUBLICO",
        "headline": "Prefeitura anuncia mudanca no horario de coleta",
        "origin": "Pagina oficial da prefeitura, com data e comunicado",
        "clues": [
            "O aviso esta no dominio oficial do municipio.",
            "A publicacao informa bairros, datas e horarios.",
            "O mesmo comunicado aparece nos canais oficiais verificados."
        ],
        "best": "COMPARTILHAR",
        "why": "Ha autoria identificavel, informacao completa e confirmacao em canais oficiais. Compartilhe mantendo o contexto."
    },
    {
        "tag": "SEGURANCA",
        "headline": "Video mostra suposto acidente ocorrido hoje na avenida central",
        "origin": "Video curto sem legenda original",
        "clues": [
            "O video nao mostra placas ou pontos reconheciveis do local.",
            "Uma busca pela data revela que o mesmo video circulou ha dois anos.",
            "Nao ha registro atual que confirme a legenda."
        ],
        "best": "NAO COMPARTILHAR",
        "why": "O video antigo foi apresentado como se fosse atual. Nao compartilhe uma legenda enganosa; procure a origem antes de republicar."
    },
    {
        "tag": "EDUCACAO",
        "headline": "Escola informa alteracao no calendario de provas",
        "origin": "Imagem recortada enviada por um contato",
        "clues": [
            "O nome da escola aparece, mas nao ha assinatura ou data.",
            "A imagem esta cortada e nao mostra o restante do comunicado.",
            "A secretaria da escola ainda nao confirmou a mudanca."
        ],
        "best": "INVESTIGAR",
        "why": "A imagem pode ser verdadeira ou estar desatualizada. Confirme com a escola antes de agir ou repassar."
    },
    {
        "tag": "CONSUMO",
        "headline": "Loja oferece premio em dinheiro para quem clicar em um link",
        "origin": "Perfil desconhecido com endereco encurtado",
        "clues": [
            "O perfil imita o nome de uma marca conhecida.",
            "O link pede dados pessoais para liberar o premio.",
            "A promocao nao aparece no site oficial da empresa."
        ],
        "best": "NAO COMPARTILHAR",
        "why": "Ha sinais de golpe e coleta indevida de dados. Nao clique nem encaminhe; denuncie a mensagem na plataforma."
    },
    {
        "tag": "CLIMA",
        "headline": "Alerta de chuva forte para a regiao nesta tarde",
        "origin": "Defesa Civil municipal, publicado hoje",
        "clues": [
            "O alerta tem horario de emissao e area de abrangencia.",
            "A Defesa Civil confirma a informacao em seu canal oficial.",
            "A orientacao inclui medidas praticas de seguranca."
        ],
        "best": "COMPARTILHAR",
        "why": "Um alerta confirmado pode proteger pessoas. Compartilhe a orientacao completa e preserve a fonte e o horario."
    },
    {
        "tag": "TECNOLOGIA",
        "headline": "Aplicativo popular vai comecar a cobrar todos os usuarios amanha",
        "origin": "Postagem sem link para anuncio da empresa",
        "clues": [
            "O texto usa urgencia, mas nao cita uma fonte.",
            "Nao ha anuncio correspondente na central de ajuda do aplicativo.",
            "Uma mudanca desse tipo precisaria de comunicacao oficial aos usuarios."
        ],
        "best": "INVESTIGAR",
        "why": "Ausencia de fonte nao prova que a alegacao e falsa. Procure o comunicado oficial antes de concluir ou compartilhar."
    },
    {
        "tag": "COMUNIDADE",
        "headline": "Campanha de arrecadacao divulga local e horario de entrega",
        "origin": "Organizacao comunitaria identificada",
        "clues": [
            "A organizacao informa responsaveis e meios de contato.",
            "O endereco e o horario foram confirmados em mais de um canal da entidade.",
            "A publicacao explica como os itens arrecadados serao utilizados."
        ],
        "best": "COMPARTILHAR",
        "why": "A campanha tem responsaveis identificados e informacoes verificaveis. Compartilhe sem alterar os dados da organizacao."
    }
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

def panel(rect, color=PANEL, radius=18, border=None):
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(screen, border, rect, 2, border_radius=radius)

def button(rect, label, color, hotkey=None):
    panel(rect, color, 13)
    shown = label if not hotkey else f"{label}  [{hotkey}]"
    draw_text(shown, FONT_MD, BG, rect.centerx, rect.centery, True)

def header(kicker, title):
    draw_text(kicker, FONT_XS, CYAN, 42, 28)
    draw_text(title, FONT_LG, WHITE, 42, 52)
    pygame.draw.line(screen, PANEL_LIGHT, (42, 102), (958, 102), 2)

def intro():
    while True:
        screen.fill(BG)
        header("SIMULADOR DE REDACAO • TREINAMENTO", "PLANTAO ZERO")
        draw_text("CENTRAL DE VERIFICACAO", FONT_LG, CYAN, 500, 180, True)
        paragraph("Uma informacao urgente acabou de chegar. Antes de agir, avalie a origem, procure evidencias e decida o que fazer.",
                  FONT_MD, WHITE, 180, 240, 640, 10)
        panel((175, 365, 650, 115), PANEL)
        draw_text("OBJETIVO", FONT_SM, YELLOW, 205, 385)
        paragraph("Proteja a confianca da comunidade: compartilhe o que foi confirmado, investigue o que ainda nao tem provas e nao espalhe conteudo enganoso.",
                  FONT_SM, MUTED, 205, 415, 585, 4)
        button(pygame.Rect(360, 535, 280, 62), "INICIAR PLANTAO", GREEN)
        draw_text("ENTER para iniciar  •  ESC para sair", FONT_XS, MUTED, 500, 625, True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_RETURN:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(360, 535, 280, 62).collidepoint(event.pos):
                    return
        clock.tick(60)

def play_case(case, number, total):
    selected = None
    while selected is None:
        screen.fill(BG)
        header(f"PLANTAO • CASO {number:02d}/{total:02d}", case["tag"])
        panel((42, 125, 916, 130))
        draw_text("INFORMACAO RECEBIDA", FONT_XS, CYAN, 68, 146)
        paragraph(case["headline"], FONT_LG, WHITE, 68, 178, 850, 4)

        panel((42, 275, 916, 72), PANEL_LIGHT)
        draw_text("ORIGEM INFORMADA", FONT_XS, YELLOW, 66, 290)
        paragraph(case["origin"], FONT_SM, WHITE, 66, 316, 850, 2)

        draw_text("PISTAS PARA SUA ANALISE", FONT_MD, WHITE, 48, 372)
        y = 414
        for idx, clue in enumerate(case["clues"], 1):
            pygame.draw.circle(screen, PURPLE, (62, y + 10), 12)
            draw_text(str(idx), FONT_XS, BG, 62, y + 10, True)
            paragraph(clue, FONT_SM, MUTED, 88, y, 850, 2)
            y += 48

        draw_text("QUAL E A SUA DECISAO?", FONT_MD, WHITE, 48, 555)
        button(pygame.Rect(42, 590, 285, 58), "COMPARTILHAR", CYAN, "A")
        button(pygame.Rect(357, 590, 285, 58), "INVESTIGAR", YELLOW, "S")
        button(pygame.Rect(672, 590, 286, 58), "NAO COMPARTILHAR", RED, "D")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "SAIR"
                if event.key == pygame.K_a:
                    selected = "COMPARTILHAR"
                elif event.key == pygame.K_s:
                    selected = "INVESTIGAR"
                elif event.key == pygame.K_d:
                    selected = "NAO COMPARTILHAR"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(42, 590, 285, 58).collidepoint(event.pos):
                    selected = "COMPARTILHAR"
                elif pygame.Rect(357, 590, 285, 58).collidepoint(event.pos):
                    selected = "INVESTIGAR"
                elif pygame.Rect(672, 590, 286, 58).collidepoint(event.pos):
                    selected = "NAO COMPARTILHAR"
        clock.tick(60)
    return selected

def feedback(case, selected):
    correct = selected == case["best"]
    while True:
        screen.fill(BG)
        header("ANALISE DE DECISAO", "RESULTADO DO CASO")
        panel((55, 135, 890, 125), PANEL)
        draw_text("SUA DECISAO", FONT_XS, MUTED, 82, 157)
        draw_text(selected, FONT_LG, GREEN if correct else RED, 82, 190)
        panel((55, 285, 890, 205), PANEL_LIGHT)
        draw_text("POR QUE ESSA ERA A MELHOR ESCOLHA?", FONT_SM, YELLOW, 82, 310)
        paragraph(case["why"], FONT_MD, WHITE, 82, 350, 820, 10)
        if correct:
            draw_text("+100 CONFIANCA PUBLICA", FONT_MD, GREEN, 500, 535, True)
        else:
            draw_text("A confianca da comunidade foi afetada.", FONT_MD, RED, 500, 535, True)
        draw_text("ENTER para continuar", FONT_SM, MUTED, 500, 620, True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                return correct
            if event.type == pygame.MOUSEBUTTONDOWN:
                return correct
        clock.tick(60)

def ending(score, total):
    while True:
        screen.fill(BG)
        header("PLANTAO ENCERRADO", "BALANCO DA REDACAO")
        panel((190, 155, 620, 250))
        draw_text(f"{score} / {total}", FONT_XL, CYAN, 500, 235, True)
        draw_text("DECISOES RESPONSAVEIS", FONT_MD, WHITE, 500, 295, True)
        if score == total:
            message = "Excelente! Voce protegeu a confianca da comunidade."
        elif score >= total // 2:
            message = "Bom trabalho. Continue verificando antes de compartilhar."
        else:
            message = "A pressa pode espalhar erros. Investigue as fontes."
        paragraph(message, FONT_MD, MUTED, 250, 355, 500, 6)
        panel((190, 445, 620, 95), PANEL_LIGHT)
        paragraph("Lembrete: ausencia de prova nao e prova de falsidade. Procure contexto, autoria, data e confirmacao independente.",
                  FONT_SM, WHITE, 220, 468, 560, 5)
        button(pygame.Rect(355, 570, 290, 58), "REINICIAR", GREEN)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_RETURN:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(355, 570, 290, 58).collidepoint(event.pos):
                    return
        clock.tick(60)

def main():
    while True:
        intro()
        score = 0
        for index, case in enumerate(CASES, 1):
            decision = play_case(case, index, len(CASES))
            if decision == "SAIR":
                pygame.quit(); sys.exit()
            if feedback(case, decision):
                score += 1
        ending(score, len(CASES))

if __name__ == "__main__":
    main()
