import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas


# Cores exatas da imagem de referência
HEADER_BLUE = colors.HexColor("#1A3A8A")       # Azul escuro superior
SECTION_TITLE_BLUE = colors.HexColor("#1A3A8A") # Azul para "Detalhamento por Disciplina"
BOX_BORDER_BLUE = colors.HexColor("#D2E1F8")    # Borda azul clara dos cards
BOX_BG_BLUE = colors.HexColor("#F0F5FD")        # Fundo do card "Dados do Aluno"

# Cores dos cards de métricas
CARD_BG_BLUE = colors.HexColor("#EFF5FC")       # Fundo azul bem claro
CARD_BORDER_BLUE = colors.HexColor("#D8E6F8")   # Borda suave

CARD_BG_GREEN = colors.HexColor("#EBF9F0")      # Fundo verde claro
CARD_BORDER_GREEN = colors.HexColor("#CEEED9")  # Borda verde suave

CARD_BG_PURPLE = colors.HexColor("#F3F0FD")     # Fundo lilás claro
CARD_BORDER_PURPLE = colors.HexColor("#E2D9FC") # Borda lilás suave

TEXT_LABEL_GRAY = colors.HexColor("#5A6A85")    # Cinza do texto do label superior dos cards
TEXT_DARK = colors.HexColor("#1E293B")          # Cinza escuro / preto para texto

# Cores dos números dos cards
COLOR_NUM_BLUE = colors.HexColor("#1A56DB")     # Azul do número 3
COLOR_NUM_DARK = colors.HexColor("#2D3748")     # Escuro do número 7
COLOR_NUM_GREEN = colors.HexColor("#16A34A")    # Verde do número 5
COLOR_NUM_PURPLE = colors.HexColor("#6D28D9")   # Roxo de 71.43%

# Cores da tabela
TH_BLUE = colors.HexColor("#1E429F")            # Azul do cabeçalho da tabela
ROW_BORDER = colors.HexColor("#E5EDF9")         # Linha divisória fina azulada


def generate_report_pdf(data: dict) -> bytes:
    """Gera o PDF com visual fiel ao design do EduTrack AI."""
    buffer = io.BytesIO()
    width, height = LETTER  # 612 x 792 pontos
    c = canvas.Canvas(buffer, pagesize=LETTER)
    c.setTitle("EduTrack AI - Relatório de Desempenho Acadêmico")

    user = data.get("user", {})
    issued_at = data.get("issued_at", datetime.now().strftime("%d/%m/%Y %H:%M"))
    indicators = data.get("indicators", {})
    subjects = data.get("subjects", [])

    margin = 36
    usable_w = width - (2 * margin)

    # ==============================================================
    # 1. HEADER BANNER (Faixa Azul Escura Superior)
    # ==============================================================
    banner_h = 100
    banner_y = height - banner_h
    c.setFillColor(HEADER_BLUE)
    c.rect(0, banner_y, width, banner_h, fill=1, stroke=0)

    # Título Principal
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(margin, banner_y + 54, "EduTrack AI")

    # Subtítulo
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, banner_y + 26, "Relatório de Desempenho Acadêmico")

    # Data/Hora no canto direito
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.drawRightString(width - margin, banner_y + 26, f"Emitido em: {issued_at}")

    # ==============================================================
    # 2. CARD "DADOS DO ALUNO"
    # ==============================================================
    card_student_h = 70
    card_student_y = banner_y - 25 - card_student_h

    # Fundo e Borda
    c.setFillColor(BOX_BG_BLUE)
    c.setStrokeColor(BOX_BORDER_BLUE)
    c.setLineWidth(1)
    c.roundRect(margin, card_student_y, usable_w, card_student_h, 3, fill=1, stroke=1)

    # Título do Card
    c.setFillColor(HEADER_BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin + 16, card_student_y + card_student_h - 20, "Dados do Aluno")

    # Linha: Nome e Matrícula / ID
    nome = user.get("name") or "Aluno"
    user_id = user.get("id") or 101

    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin + 16, card_student_y + card_student_h - 40, "Nome: ")
    nome_w = c.stringWidth("Nome: ", "Helvetica-Bold", 10)
    c.setFont("Helvetica", 10)
    c.drawString(margin + 16 + nome_w, card_student_y + card_student_h - 40, str(nome))

    # Matrícula / ID alinhado à direita
    id_text = f"Matricula / ID: #{user_id}"
    c.setFont("Helvetica", 10)
    c.setFillColor(TEXT_DARK)
    c.drawRightString(width - margin - 20, card_student_y + card_student_h - 40, id_text)

    # Linha: E-mail
    email = user.get("email") or "aluno@edutrack.ai"
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(TEXT_LABEL_GRAY)
    c.drawString(margin + 16, card_student_y + card_student_h - 58, "E-mail: ")
    email_w = c.stringWidth("E-mail: ", "Helvetica-Bold", 9)
    c.setFont("Helvetica", 9)
    c.drawString(margin + 16 + email_w, card_student_y + card_student_h - 58, str(email))

    # ==============================================================
    # 3. CARDS DE INDICADORES (4 Colunas)
    # ==============================================================
    cards_gap = 12
    card_w = (usable_w - (3 * cards_gap)) / 4
    card_h = 75
    cards_y = card_student_y - 20 - card_h

    metric_cards = [
        ("Disciplinas", str(indicators.get("subjects", 0)), CARD_BG_BLUE, CARD_BORDER_BLUE, COLOR_NUM_BLUE),
        ("Total Tarefas", str(indicators.get("total_tasks", 0)), CARD_BG_BLUE, CARD_BORDER_BLUE, COLOR_NUM_DARK),
        ("Concluidas", str(indicators.get("completed", 0)), CARD_BG_GREEN, CARD_BORDER_GREEN, COLOR_NUM_GREEN),
        ("Progresso Geral", f"{indicators.get('overall_progress', 0.0)}%", CARD_BG_PURPLE, CARD_BORDER_PURPLE, COLOR_NUM_PURPLE),
    ]

    for i, (label, val, bg_c, border_c, num_c) in enumerate(metric_cards):
        cx = margin + i * (card_w + cards_gap)
        c.setFillColor(bg_c)
        c.setStrokeColor(border_c)
        c.setLineWidth(1)
        c.roundRect(cx, cards_y, card_w, card_h, 3, fill=1, stroke=1)

        # Label superior
        c.setFillColor(TEXT_LABEL_GRAY)
        c.setFont("Helvetica", 9)
        c.drawCentredString(cx + (card_w / 2), cards_y + card_h - 22, label)

        # Valor centralizado
        c.setFillColor(num_c)
        c.setFont("Helvetica-Bold", 19)
        c.drawCentredString(cx + (card_w / 2), cards_y + 18, val)

    # ==============================================================
    # 4. TABELA: DETALHAMENTO POR DISCIPLINA
    # ==============================================================
    curr_y = cards_y - 32
    c.setFillColor(SECTION_TITLE_BLUE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, curr_y, "Detalhamento por Disciplina")

    # Linha sublinhada azul suave abaixo do título
    c.setStrokeColor(SECTION_TITLE_BLUE)
    c.setLineWidth(1)
    title_w = c.stringWidth("Detalhamento por Disciplina", "Helvetica-Bold", 13)
    c.line(margin, curr_y - 2, margin + title_w, curr_y - 2)

    curr_y -= 14

    # Larguras das Colunas (soma = usable_w)
    # Disciplina | Total | Concluidas | Pendentes | Progresso (%)
    col_w = [
        usable_w * 0.44,  # Disciplina
        usable_w * 0.14,  # Total
        usable_w * 0.14,  # Concluidas
        usable_w * 0.14,  # Pendentes
        usable_w * 0.14,  # Progresso (%)
    ]
    th_h = 24
    row_h = 24

    # Cabeçalho da Tabela
    curr_y -= th_h
    c.setFillColor(TH_BLUE)
    c.rect(margin, curr_y, usable_w, th_h, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    th_labels = ["Disciplina", "Total", "Concluidas", "Pendentes", "Progresso (%)"]
    
    # Posições X
    x_positions = [margin]
    for w_col in col_w[:-1]:
        x_positions.append(x_positions[-1] + w_col)

    # Desenhar labels do header
    c.drawString(x_positions[0] + 10, curr_y + 8, th_labels[0])
    for j in range(1, 5):
        c.drawString(x_positions[j] + 8, curr_y + 8, th_labels[j])

    # Linhas de Dados
    c.setFont("Helvetica", 9)
    if not subjects:
        curr_y -= row_h
        c.setFillColor(colors.white)
        c.rect(margin, curr_y, usable_w, row_h, fill=1, stroke=0)
        c.setFillColor(TEXT_LABEL_GRAY)
        c.drawString(margin + 10, curr_y + 7, "Nenhuma disciplina cadastrada.")
        c.setStrokeColor(ROW_BORDER)
        c.setLineWidth(0.8)
        c.line(margin, curr_y, margin + usable_w, curr_y)
    else:
        for i, s in enumerate(subjects):
            curr_y -= row_h

            # Se passar da margem inferior da página
            if curr_y < 40:
                c.showPage()
                curr_y = height - 50

            # Fundo branco com linha divisória sutil
            c.setFillColor(colors.white)
            c.rect(margin, curr_y, usable_w, row_h, fill=1, stroke=0)

            c.setStrokeColor(ROW_BORDER)
            c.setLineWidth(0.8)
            c.line(margin, curr_y, margin + usable_w, curr_y)

            # Nome da Disciplina
            subj_name = str(s.get("name") or "")
            if len(subj_name) > 34:
                subj_name = subj_name[:32] + "..."
            c.setFillColor(TEXT_DARK)
            c.setFont("Helvetica", 9)
            c.drawString(x_positions[0] + 10, curr_y + 7, subj_name)

            # Total
            c.setFillColor(TEXT_DARK)
            c.drawString(x_positions[1] + 8, curr_y + 7, str(s.get("total_tasks", 0)))

            # Concluídas (Verde)
            c.setFillColor(COLOR_NUM_GREEN)
            c.drawString(x_positions[2] + 8, curr_y + 7, str(s.get("completed", 0)))

            # Pendentes (Laranja / Vermelho suave)
            c.setFillColor(colors.HexColor("#D9534F"))
            c.drawString(x_positions[3] + 8, curr_y + 7, str(s.get("pending", 0)))

            # Progresso (%) (Azul escuro em negrito)
            c.setFillColor(TH_BLUE)
            c.setFont("Helvetica-Bold", 9)
            prog = s.get("progress", 0.0)
            c.drawString(x_positions[4] + 8, curr_y + 7, f"{prog}%")

    # Contorno externo / inferior suave na tabela
    c.setStrokeColor(ROW_BORDER)
    c.setLineWidth(1)
    c.line(margin, curr_y, margin + usable_w, curr_y)

    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
