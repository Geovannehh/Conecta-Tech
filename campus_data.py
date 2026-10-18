"""Conteúdo institucional demonstrativo do Conecta Campus."""

HELP_ITEMS = [
    {
        "id": "acesso-sistema",
        "title": "Não consigo acessar o sistema acadêmico",
        "summary": "Recupere seu acesso e descubra quem procurar se o problema continuar.",
        "category": "Tecnologia",
        "profiles": ["calouro", "professor"],
        "sector": "Central de Tecnologia",
        "location": "Bloco A · Sala 105",
        "contact": "suporte@universidade.edu.br · Ramal 2105",
        "steps": [
            "Confirme se está usando o e-mail institucional completo.",
            "Use a opção “Esqueci minha senha” e verifique sua caixa de entrada.",
            "Se o erro continuar, leve um documento com foto à Central de Tecnologia.",
        ],
        "tags": ["senha", "login", "portal", "sistema", "acesso", "email"],
    },
    {
        "id": "documentos-matricula",
        "title": "Tenho dúvidas sobre matrícula e documentos",
        "summary": "Confira pendências, prazos e o canal correto para regularizar sua matrícula.",
        "category": "Acadêmico",
        "profiles": ["calouro"],
        "sector": "Secretaria Acadêmica",
        "location": "Bloco Central · Térreo",
        "contact": "secretaria@universidade.edu.br · Ramal 2001",
        "steps": [
            "Consulte a área de pendências no portal acadêmico.",
            "Separe documento de identificação e comprovante de matrícula.",
            "Procure a Secretaria Acadêmica dentro do prazo exibido no portal.",
        ],
        "tags": ["matricula", "documento", "declaração", "histórico", "prazo"],
    },
    {
        "id": "financeiro",
        "title": "Preciso falar sobre mensalidade ou bolsa",
        "summary": "Encontre orientações sobre boletos, bolsas, descontos e negociação.",
        "category": "Financeiro",
        "profiles": ["calouro"],
        "sector": "Atendimento Financeiro",
        "location": "Bloco Central · Sala 012",
        "contact": "financeiro@universidade.edu.br · Ramal 2012",
        "steps": [
            "Consulte a situação financeira no portal do aluno.",
            "Tenha em mãos o número da matrícula e o documento do responsável financeiro.",
            "Para bolsas e descontos, solicite atendimento antes do vencimento.",
        ],
        "tags": ["boleto", "bolsa", "desconto", "mensalidade", "pagamento"],
    },
    {
        "id": "biblioteca",
        "title": "Como usar a biblioteca?",
        "summary": "Faça seu cadastro, encontre materiais e conheça os espaços de estudo.",
        "category": "Biblioteca",
        "profiles": ["calouro", "professor"],
        "sector": "Biblioteca Central",
        "location": "Bloco B · 1º andar",
        "contact": "biblioteca@universidade.edu.br · Ramal 2200",
        "steps": [
            "Apresente seu cartão institucional no balcão para ativar o cadastro.",
            "Acesse o catálogo on-line com as mesmas credenciais do portal.",
            "Reserve salas de estudo com antecedência pelo sistema da biblioteca.",
        ],
        "tags": ["livro", "emprestimo", "estudo", "acervo", "artigo"],
    },
    {
        "id": "localizacao",
        "title": "Não encontro uma sala ou setor",
        "summary": "Use os pontos de referência do campus e peça apoio na recepção.",
        "category": "Localização",
        "profiles": ["calouro", "professor"],
        "sector": "Recepção e Apoio ao Campus",
        "location": "Entrada principal · Térreo",
        "contact": "recepcao@universidade.edu.br · Ramal 2000",
        "steps": [
            "Confira o bloco e o andar no seu horário ou comunicado.",
            "Procure as placas coloridas de cada bloco.",
            "Apresente o código da sala na recepção para receber a rota mais curta.",
        ],
        "tags": ["sala", "bloco", "mapa", "laboratorio", "coordenação"],
    },
    {
        "id": "apoio-docente",
        "title": "Preciso de apoio para preparar ou ministrar aulas",
        "summary": "Conheça os recursos pedagógicos e tecnológicos disponíveis ao professor.",
        "category": "Docência",
        "profiles": ["professor"],
        "sector": "Núcleo de Apoio Pedagógico",
        "location": "Bloco C · Sala 204",
        "contact": "apoio.docente@universidade.edu.br · Ramal 2304",
        "steps": [
            "Consulte o guia docente e o calendário acadêmico.",
            "Reserve equipamentos e laboratórios pelo portal do professor.",
            "Agende uma orientação com o Núcleo de Apoio Pedagógico.",
        ],
        "tags": ["aula", "projetor", "laboratorio", "plano", "avaliação", "diário"],
    },
    {
        "id": "internet-campus",
        "title": "A internet do campus não funciona",
        "summary": "Configure a rede institucional ou abra um atendimento técnico.",
        "category": "Tecnologia",
        "profiles": ["calouro", "professor"],
        "sector": "Central de Tecnologia",
        "location": "Bloco A · Sala 105",
        "contact": "suporte@universidade.edu.br · Ramal 2105",
        "steps": [
            "Selecione a rede institucional e informe seu usuário acadêmico.",
            "Remova redes antigas salvas e tente conectar novamente.",
            "Registre o bloco e a sala onde ocorreu a falha ao pedir suporte.",
        ],
        "tags": ["wifi", "internet", "rede", "conexão", "senha"],
    },
]

JOURNEYS = {
    "calouro": [
        {"number": "01", "title": "Confirme sua matrícula", "text": "Confira documentos, turma, horários e pendências no portal acadêmico."},
        {"number": "02", "title": "Ative seus acessos", "text": "Entre no e-mail institucional, no ambiente virtual e na rede do campus."},
        {"number": "03", "title": "Conheça seus lugares", "text": "Localize coordenação, biblioteca, laboratórios, atendimento e espaços de convivência."},
        {"number": "04", "title": "Organize sua vida acadêmica", "text": "Salve o calendário, entenda avaliações e conheça os canais oficiais."},
        {"number": "05", "title": "Construa sua rede de apoio", "text": "Descubra projetos, monitorias, apoio estudantil e atividades de integração."},
    ],
    "professor": [
        {"number": "01", "title": "Regularize seu vínculo", "text": "Confirme cadastro, documentação, horários e contatos institucionais."},
        {"number": "02", "title": "Ative os sistemas docentes", "text": "Acesse diário, ambiente virtual, e-mail e solicitações internas."},
        {"number": "03", "title": "Prepare sua infraestrutura", "text": "Conheça salas, laboratórios, equipamentos e canais de suporte."},
        {"number": "04", "title": "Alinhe sua prática acadêmica", "text": "Consulte calendário, plano de ensino, avaliações e normas essenciais."},
        {"number": "05", "title": "Conheça sua rede de apoio", "text": "Conecte-se à coordenação, ao apoio pedagógico e aos serviços do campus."},
    ],
}

CATEGORIES = ["Todos", "Acadêmico", "Tecnologia", "Financeiro", "Biblioteca", "Localização", "Docência"]

SECTORS = [
    "Secretaria Acadêmica",
    "Central de Tecnologia",
    "Biblioteca Central",
    "Atendimento Financeiro",
    "Núcleo de Apoio Pedagógico",
    "Recepção e Apoio ao Campus",
]
