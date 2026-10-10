import json

file_path = "prova_objetiva_2__ae834e15.pdf"
source_file = "data/raw/CACD_2011/wayback/prova_objetiva_2__ae834e15.pdf" # matching pattern from prompt or similar

# Constructing JSON Lines for all questions in the provided text.
# Contest: IRBr / CACD (Admissão à Carreira de Diplomata)
# Year: 2011 (deduced from text: "In. The Economist, January 15-21, 2011" and similar)

lines = []

# Helper to build item
def make_ce_item(q_num, item_num, disc, q_text, item_text, page):
    return {
        "contest_id": "CACD_2011",
        "year": 2011,
        "phase": 1,
        "stage": "primeira_fase",
        "discipline": disc,
        "question_number": q_num,
        "item_number": item_num,
        "question_type": "certo_errado",
        "question_text": q_text,
        "item_text": item_text,
        "alternatives": None,
        "answer": None,
        "page": page,
        "caderno": "Segunda Etapa",
        "source_file": "prova_objetiva_2__ae834e15.pdf",
        "source_url": None,
        "confidence": 1.0,
        "notes": None
    }

def make_mc_item(q_num, disc, q_text, alts, page):
    return {
        "contest_id": "CACD_2011",
        "year": 2011,
        "phase": 1,
        "stage": "primeira_fase",
        "discipline": disc,
        "question_number": q_num,
        "item_number": None,
        "question_type": "multipla_escolha",
        "question_text": q_text,
        "item_text": None,
        "alternatives": alts,
        "answer": None,
        "page": page,
        "caderno": "Segunda Etapa",
        "source_file": "prova_objetiva_2__ae834e15.pdf",
        "source_url": None,
        "confidence": 1.0,
        "notes": None
    }

# Data filling based on transcript:

# Text 1: Nobel...
t1 = """Nobel was an ardent advocate of arbitration, though not of disarmament, which he thought a foolish demand for the present. He urged establishment of a tribunal and agreement among nations for a one-year period of compulsory truce in any dispute. He turned up in person, though incognito, at a Peace Congress in Bern in 1892 and told Bertha von Suttner that if she could "inform me, convince me, I will do something great for the cause". The spark of friendship between them had been kept alive in correspondence and an occasional visit over the years and he now wrote her that a new era of violence seemed to be working itself up: "one hears in the distance its hollow rumble already." Two months later he wrote again, "I should like to dispose of my fortune to found a prize to be awarded every five years" to the person who had contributed most effectively to the peace of Europe. He thought that it should terminate after six awards, "for if in thirty years society cannot be reformed we shall inevitably lapse into barbarism". Nobel brooded over the plan, embodied it in a will drawn in 1895 which allowed man a little longer deadline, and died the following year.\nBarbara Tuchman. The proud tower. MacMillan Company, 1966, p. 233 (adapted)."""

# Q29
q29_text = "This text refers to questions from 29 through 31.\n\n" + t1 + "\n\nQUESTÃO 29\nBased on the text, judge if the following items are right (C) or wrong (E)."
lines.append(make_ce_item(29, 1, "Língua Inglesa", q29_text, "It can be inferred from the text that Nobel did a dramatic volte-face concerning his stance on peace or disarmament.", 1))
lines.append(make_ce_item(29, 2, "Língua Inglesa", q29_text, "Nobel predicted that peace would only last thirty years, because violence in Europe was increasing.", 1))
lines.append(make_ce_item(29, 3, "Língua Inglesa", q29_text, "Nobel suggested that ominous signs of impending violence could be discerned in the offing.", 1))
lines.append(make_ce_item(29, 4, "Língua Inglesa", q29_text, "The author puts forward a tentative suggestion that Nobel's continued commitment to the cause of arbitration rendered him impervious to the idea of disarmament.", 1))

# Q30
q30_text = "This text refers to questions from 29 through 31.\n\n" + t1 + "\n\nQUESTÃO 30\nIn the text,"
lines.append(make_ce_item(30, 1, "Língua Inglesa", q30_text, '"brooded over" and "will", both on line 18, mean respectively pondered and an official statement disposing of a person\'s property after his or her death.', 1))
lines.append(make_ce_item(30, 2, "Língua Inglesa", q30_text, 'the pronoun "it" (l.15) refers to Nobel\'s fortune.', 1))
lines.append(make_ce_item(30, 3, "Língua Inglesa", q30_text, 'the word "for" (l.16) can be replaced by since with no change in the original meaning of the sentence.', 1))
lines.append(make_ce_item(30, 4, "Língua Inglesa", q30_text, 'the term "spark" (l.8) is used in its connotative meaning.', 1))

# Q31
q31_text = "This text refers to questions from 29 through 31.\n\n" + t1 + "\n\nQUESTÃO 31\nWhich of the following statements about the verbs in the text is correct?"
alts31 = [
    {"letter": "A", "text": 'The forms "brooded" (l.18), "embodied" (l.18) and "died" (l.19) can be replaced, respectively, by has brooded, has embodied and has died without effecting a significant change in the original meaning of the text.'},
    {"letter": "B", "text": 'In "The spark of friendship between them had been kept alive" (l.8-9), the use of the form "had been" implies the connection between von Suttner and Nobel took place after the Peace Congress.'},
    {"letter": "C", "text": "The verbal form \"should\" (l.13) could be replaced by would without effecting a significant change in the meaning of the text."},
    {"letter": "D", "text": "The use of the form \"to be awarded\" (l.13-14) directs the focus of the sentence to those who award the prize."},
    {"letter": "E", "text": "In \"I will do something great\" (l.7-8), the use of \"will\" conveys the idea of imposition."}
]
lines.append(make_mc_item(31, "Língua Inglesa", q31_text, alts31, 1))

# Text 2: Wikipedia
t2 = """It may not stir up international outrage like its semi-namesake WikiLeaks, but Wikipedia sparks debate. The free online encyclopedia, which celebrates its tenth birthday on January 15th, is a symbol of unpaid collaboration and one of the most popular destinations on the Internet, attracting some 400m visitors a month. It also faces serious charges of elitism.
Wikipedia offers more than 17m articles in 247 languages. Every day thousands of people edit entries or add new ones in return for nothing more than the satisfaction of contributing to the stock of human knowledge. Wikipedia relies on its users' generosity to fill its coffers as well as its pages. Recent visitors to the website were confronted with images of Jimmy Wales, a co-founder, and a request for donations. The campaign was annoying but effective, raising $ 16m in 50 days.
With its emphasis on bottom-up collaboration and the broad dissemination of knowledge, the online encyclopedia is in many ways an incarnation of the fundamental values of the web. But Wikipedia also reveals some of the pitfalls of the increasingly popular "crowdsourcing" model of content creation. One is maintaining accuracy. On the whole, Wikipedia's system of peer reviewing does a reasonable job of policing facts. But it is vulnerable to vandalism. Several politicians and TV personalities have had their deaths announced in Wikipedia while they were still in fine fettle.
Some observers argue the site should start paying expert editors to produce and oversee content, and sell advertising to cover the cost. Problems with accuracy "are an inevitable consequence of a free-labour approach", argues Alex Jannykhin, of WikiExperts, which advises organisations on how to create Wikipedia articles (the very existence of such outfits hints at Wikipedia's importance, as well as its susceptibility to outside influence). The encyclopedia's bosses retort that such concerns are overblown and that taking advertisers would dent its appeal to users.
Wikipedia. The promise and perils of crowdsourcing content. In: The Economist, January 15-21, 2011, p. 69 (adapted)."""

# Q32
q32_text = "This text refers to questions from 32 through 36.\n\n" + t2 + "\n\nQUESTÃO 32\nBased on the text, judge if the items below are right (C) or wrong (E)."
lines.append(make_ce_item(32, 1, "Língua Inglesa", q32_text, "The basic concepts behind Wikipedia are inconsistent with the usefulness of unhindered access to the Internet.", 2))
lines.append(make_ce_item(32, 2, "Língua Inglesa", q32_text, "It is possible to deduce from the text that Wikipedia resorted to an appeal for public monetary contributions.", 2))
lines.append(make_ce_item(32, 3, "Língua Inglesa", q32_text, "One of the major concerns regarding the content of the online encyclopedia is its vulnerability to inclusion of imprecise information.", 2))
lines.append(make_ce_item(32, 4, "Língua Inglesa", q32_text, "Not all articles in Wikipedia must be submitted by personal individual collaborators.", 2))

# Q33
q33_text = "This text refers to questions from 32 through 36.\n\n" + t2 + "\n\nQUESTÃO 33\nAccording to the text, judge if the following items are right (C) or wrong (E)."
lines.append(make_ce_item(33, 1, "Língua Inglesa", q33_text, 'On line 25, "while they were still in fine fettle" can be correctly rewritten as even before their bodies could be prepared for burial, without change in meaning.', 2))
lines.append(make_ce_item(33, 2, "Língua Inglesa", q33_text, 'On line 23, "But it is vulnerable to vandalism" can be correctly replaced by Furthermore, it falls prey to vandalism, without change in meaning.', 2))
lines.append(make_ce_item(33, 3, "Língua Inglesa", q33_text, "From the last paragraph, it is correct to infer that volunteer work is inherently slovenly and deceptive.", 2))
lines.append(make_ce_item(33, 4, "Língua Inglesa", q33_text, 'The terms "stir up" (l.1) and "sparks" (l.2) bear a semantic relationship to the verb to fuel.', 2))

# Q34
q34_text = "This text refers to questions from 32 through 36.\n\n" + t2 + "\n\nQUESTÃO 34\nAccording to what the text states, choose the correct option."
alts34 = [
    {"letter": "A", "text": "Underlying the idea of Wikipedia is the premise of a profitable approach to the compilation and diffusion of human values and customs."},
    {"letter": "B", "text": "Contributions to Wikipedia come both in the form of spontaneous inclusion and reviewing of texts as well as of gifts of money."},
    {"letter": "C", "text": "Advertising would increase the reliability and acceptance of Wikipedia, according to its owners."},
    {"letter": "D", "text": "The bulk of Wikipedia articles deliberately misguide its users as to the actual death of some celebrities."},
    {"letter": "E", "text": "Wikipedia is not free of charge, for it launches aggressive worldwide fund-raising campaigns."}
]
lines.append(make_mc_item(34, "Língua Inglesa", q34_text, alts34, 2))

# Q35
q35_text = "This text refers to questions from 32 through 36.\n\n" + t2 + "\n\nQUESTÃO 35\nIn the text, the word \"overblown\" (l.34) is synonymous with"
alts35 = [
    {"letter": "A", "text": "excessive."},
    {"letter": "B", "text": "widespread."},
    {"letter": "C", "text": "fundamental."},
    {"letter": "D", "text": "grave."},
    {"letter": "E", "text": "mounting."}
]
lines.append(make_mc_item(35, "Língua Inglesa", q35_text, alts35, 2))

# Q36
q36_text = "This text refers to questions from 32 through 36.\n\n" + t2 + "\n\nQUESTÃO 36\nIn the text, the expression \"peer reviewing\" (l.22) refers to"
alts36 = [
    {"letter": "A", "text": "a thorough check of facts and figures carried out by individuals who have spotless academic reputations."},
    {"letter": "B", "text": "an enforcement of rules similar to that performed by police officers."},
    {"letter": "C", "text": "the system used by Wikipedia to minimize the publication of false information."},
    {"letter": "D", "text": "the mounting pressure brought to bear on an individual by his or her colleagues."},
    {"letter": "E", "text": "a friendly way of going over factual research."}
]
lines.append(make_mc_item(36, "Língua Inglesa", q36_text, alts36, 2))

# Text 3: Remembrance
t3 = """Remembrance of things past is often dearest to those who are bored or driven to despair by the world around them. To these the contemplation of times gone by brings surcease from current burdens too heavy to bear. "Take not away from me" implored the Emperor Julian, world-weary monarch in another age of disenchantment, "this mad love for that which no longer is. That which has been is more splendidly beautiful than all that is..." To others, concerned as watchers and movers with the challenge of today and the promise or menace of tomorrow, the tale of many yesterdays, reconstructed by the history and the science of living men and women, has another meaning.
By revealing what has gone before, it illumines the act of the human adventure now being played and suggests the pattern of acts to come. The drama of earthborn and earthbound humanity, despite all its crises and intermissions, is a continuous story. All the characters are prisoners of time. All the problems of the now are forever shaped by the experiences of a then which extends back in unbroken sequence to the origins of life. Each generation has freedom to choose among alternative designs for destiny, and opportunity to win some measure of mastery over its fate, only to the extent of its comprehension of where it stands in the cavalcade of years, decades, centuries, and millennia ticked off by the spinning planet.
Frederick L. Schuman. International politics: the destiny of the Western state system. New York: McGraw-Hill, 1948, p. 1 (adapted)."""

# Q37
q37_text = "This text refers to questions from 37 through 40.\n\n" + t3 + "\n\nQUESTÃO 37\nBased on the text, judge if the items below are right (C) or wrong (E)."
lines.append(make_ce_item(37, 1, "Língua Inglesa", q37_text, "One can infer from the text that backward or nostalgic views of the world have existed for more than a thousand years.", 2))
lines.append(make_ce_item(37, 2, "Língua Inglesa", q37_text, "According to the text, although past events should be taken into consideration, humankind can choose its future and destiny freely.", 2))
lines.append(make_ce_item(37, 3, "Língua Inglesa", q37_text, "The author of the text suggests that nostalgia is the preserve of desperate people.", 2))
lines.append(make_ce_item(37, 4, "Língua Inglesa", q37_text, "The author's clear intention in the first paragraph is to rightly extol the virtues of extreme political reactionarism.", 2))

# Q38
q38_text = "This text refers to questions from 37 through 40.\n\n" + t3 + "\n\nQUESTÃO 38\nAs far as the semantic and grammar features of the text are concerned, judge if the following items are right (C) or wrong (E)."
lines.append(make_ce_item(38, 1, "Língua Inglesa", q38_text, 'The word "and" (l.15) is used as a stylistic device to bring together two synonymous words, "earthborn" (l.15) and "earthbound" (l.16).', 3))
lines.append(make_ce_item(38, 2, "Língua Inglesa", q38_text, 'The pronoun "it" (l.13) refers to "another meaning" (l.11-12).', 3))
lines.append(make_ce_item(38, 3, "Língua Inglesa", q38_text, 'A more up-to-date manner to convey the notion expressed by "illumines" (l.13) is sheds light on.', 3))
lines.append(make_ce_item(38, 4, "Língua Inglesa", q38_text, 'The expression "watchers and movers" (l.8-9) refers to people who play clearly distinct roles as far as political action is concerned.', 3))

# Q39
q39_text = "This text refers to questions from 37 through 40.\n\n" + t3 + "\n\nQUESTÃO 39\nStill in the fields of semantics and grammar of the text, judge if the items below are right (C) or wrong (E)."
lines.append(make_ce_item(39, 1, "Língua Inglesa", q39_text, 'If "ticked off" (l.24) and "spinning" (l.25) were replaced respectively by marked off and rotating, there would occur no grammar mistakes in the sentence.', 3))
lines.append(make_ce_item(39, 2, "Língua Inglesa", q39_text, 'The words "crises" (l.16) and "millennia" (l.24), as well as theses and fulcra, can only be found in their plural forms.', 3))
lines.append(make_ce_item(39, 3, "Língua Inglesa", q39_text, 'In the fragment "All the problems of the now are forever shaped by the experiences of a then" (l.18-19), the words "now" and "then" can be replaced respectively by here and there without effecting changes in the meaning and the grammatical correction of the passage.', 3))
lines.append(make_ce_item(39, 4, "Língua Inglesa", q39_text, 'In the first paragraph, the words "world-weary" (l.5) and "disenchantment" (l.6) establish a semantic relation which reveals the pessimism which was felt by the "monarch" (l.5) and characterized his "age" (l.6).', 3))

# Q40
q40_text = "This text refers to questions from 37 through 40.\n\n" + t3 + "\n\nQUESTÃO 40\nThe particle \"as\" (l.8) is used in the text"
alts40 = [
    {"letter": "A", "text": "to express the idea of in the same way."},
    {"letter": "B", "text": "to describe the purpose or quality of someone or something."},
    {"letter": "C", "text": "to express the idea of because."},
    {"letter": "D", "text": "to express the idea of while."},
    {"letter": "E", "text": "in a comparison to refer to the degree of something."}
]
lines.append(make_mc_item(40, "Língua Inglesa", q40_text, alts40, 3))

# Q41
t41 = """Segundo Frei Vicente do Salvador, em uma das ocasiões em que foi necessário pegar em armas para submeter os gentios da região do Cabo de Santo Agostinho, Duarte de Albuquerque Coelho organizou várias companhias de guerra. Em Olinda, servindo-se de "mercadores e moradores, porque eram de diversas partes do Reino", o donatário "ordenou outras três companhias": "que por capitão dos de Viana do Castelo fosse João Pais, dos do Porto, Bento Dias Santiago e dos de Lisboa, Gonçalo Mendes d'Elvas, mercador".\nLeonor F. Costa. Redes interportuárias nos circuitos do açúcar brasileiro. O trajecto de Gaspar Pacheco, um banqueiro de D. João IV. In: M. Cunha (Coord.). Do Brasil à metrópole. Efeitos sociais (séc. XVII-XVIII). Anais da Universidade de Évora, jul./2001, p. 15 (com adaptações)."""
q41_text = t41 + "\n\nTendo o texto acima como referência inicial, julgue (C ou E) os itens a seguir, relativos à sociedade colonial brasileira."
lines.append(make_ce_item(41, 1, "História do Brasil", q41_text, "A despeito da importância econômica que desempenhavam, comerciantes e mercadores reinóis enfrentavam, no Brasil, grande dificuldade para alcançar representação política.", 3))
lines.append(make_ce_item(41, 2, "História do Brasil", q41_text, "Entre as cláusulas do Pacto Colonial incluía-se a da obrigatoriedade de que os mercadores portugueses, quando solicitados, colaborassem militarmente com as forças da metrópole.", 3))
lines.append(make_ce_item(41, 3, "História do Brasil", q41_text, "A centralização do poder político, refletida na concentração do aparato burocrático do império português em Lisboa, deu origem à monopolização do comércio colonial pelos mercadores lisboetas.", 3))
lines.append(make_ce_item(41, 4, "História do Brasil", q41_text, "As companhias de guerra configuravam soluções econômicas típicas do mercantilismo colonial português, estando as expedições de exploração dos novos territórios associadas à captura de mão de obra escrava indígena.", 3))

# Q42
q42_text = "QUESTÃO 42\nNo que concerne à configuração territorial da América portuguesa, assinale a opção correta."
alts42 = [
    {"letter": "A", "text": "Em oposição às determinações da Coroa portuguesa, ao longo do século XVII, colonos partiram de Piratininga em busca de riquezas pelos sertões afora, o que foi decisivo para a configuração das fronteiras do Brasil e para a consolidação de São Paulo como importante polo econômico no período colonial."},
    {"letter": "B", "text": "As tensões entre castelhanos e portugueses, no Novo Mundo, tiveram início com a decisão, tomada por Portugal, de ocupar vastas extensões de terra na bacia amazônica, já nas primeiras décadas do século XVI, e atingiram dimensão ainda mais violenta na vigência da União Ibérica (1580-1640)."},
    {"letter": "C", "text": "Ponto principal entre as diversas áreas de colonização portuguesa no extremo sul do Novo Mundo, a Colônia de Sacramento foi fundada para servir como base do comércio lusitano na região, e a necessidade de neutralizar a crescente importância econômica dessa colônia levou os espanhóis a fundarem Buenos Aires na outra margem do rio da Prata."},
    {"letter": "D", "text": "A decisão castelhana de invadir a Colônia de Sacramento, motivada por interesses específicos da elite de Buenos Aires, foi tomada quando o estado de hostilidade entre Castela e Portugal, presente em grande parte da segunda metade do século XVIII, sinalizava evidente distensão."},
    {"letter": "E", "text": "No período entre a assinatura dos tratados de Madri (1750) e de Santo Ildefonso (1777), as duas metrópoles ibéricas foram levadas ao confronto bélico na fronteira meridional do Brasil, cujo resultado beneficiou Portugal, que anexou à sua colônia territórios que, pelo disposto no Tratado de Tordesilhas, pertenciam à Espanha."}
]
lines.append(make_mc_item(42, "História do Brasil", q42_text, alts42, 4))

# Q43
q43_text = "QUESTÃO 43\nAssinale a opção correta com relação ao processo de independência do Brasil."
alts43 = [
    {"letter": "A", "text": "Um tipo de conflito de interesses que reapareceria em outros contextos da história do Brasil, centrado nas atribuições do Poder Executivo e do Legislativo, ocasionou a primeira grave crise política do nascente Estado nacional brasileiro e redundou na dissolução da assembleia constituinte encarregada de elaborar a primeira Constituição do país."},
    {"letter": "B", "text": "O reconhecimento da independência brasileira pela Inglaterra ocorreu quase simultaneamente à decisão dos Estados Unidos da América (EUA) de reconhecer o nascimento do Estado brasileiro sob a liderança do antigo príncipe regente português; em ambos os casos, condicionou-se o reconhecimento à abertura do mercado brasileiro ao comércio internacional."},
    {"letter": "C", "text": "Os dois partidos políticos constituídos no início do Primeiro Reinado, o Conservador e o Liberal, ofereceram a Dom Pedro I o apoio e a estabilidade necessários para o seu governo, cenário de estabilidade política que desapareceu em face da violenta repressão do governo central a movimentos separatistas como a Cabanagem e a Sabinada."},
    {"letter": "D", "text": "A emancipação política do Brasil, além de não ensejar grandes alterações na ordem econômica e social, preservou a monarquia, em meio aos vizinhos republicanos, situação somente possível devido à existência de uma elite política homogênea, detentora de sólida base social e de um projeto de nação consensualmente construído."},
    {"letter": "E", "text": "A Cisplatina e a Bahia foram as províncias brasileiras nas quais se manifestou a resistência portuguesa, tendo o governo de Lisboa contratado comandantes militares estrangeiros, como, por exemplo, o oficial francês Pedro Labatut, para liderar as tropas lusas no confronto com as forças leais a Dom Pedro I."}
]
lines.append(make_mc_item(43, "História do Brasil", q43_text, alts43, 4))

# Q44
t44 = """A transição do Império para a República, proclamada em 1889, constituiu a primeira grande mudança de regime político ocorrida desde a Independência. Republicanistas "puros", como Silva Jardim, defendiam uma mudança de regime que, a exemplo da França, tivesse como resultado maior participação da população na vida política nacional. Mas, vitoriosos, os republicanos conservadores, como Campos Sales, mantiveram o modelo de exclusão política e sociocultural sob nova fachada. Ao "Parlamentarismo sem povo" do Segundo Reinado, sucedeu uma República praticamente "sem povo", ou seja, sem cidadania democrática.\nAdriana Lopez e Carlos Guilherme Mota. História do Brasil: uma interpretação. São Paulo: Editora SENAC, 2008, p. 552 (com adaptações)."""
q44_text = t44 + "\n\nTendo o texto acima como referência inicial e considerando aspectos marcantes da história brasileira entre o regime monárquico do século XIX e a Primeira República, julgue (C ou E) os itens seguintes."
lines.append(make_ce_item(44, 1, "História do Brasil", q44_text, "A Revolução de 1930 rompeu com as deterioradas estruturas da República Velha ao encampar a consistente ideologia do tenentismo e alçar ao poder Getúlio Vargas, cuja expressão política se restringia ao Rio Grande do Sul.", 4))
lines.append(make_ce_item(44, 2, "História do Brasil", q44_text, "Apesar de o republicanismo ter sido assimilado e apoiado por grande parte da opinião pública brasileira, fato comprovado com a eleição de significativa bancada de deputados do Partido Republicano nas últimas décadas do Império, a implantação do novo regime ocorreu por golpe de Estado liderado por oficiais do Exército.", 4))
lines.append(make_ce_item(44, 3, "História do Brasil", q44_text, "O caráter excludente da Primeira República, apontado no texto, expressava-se, entre outros aspectos, no sistema eleitoral vigente, marcado pelo reduzido número de eleitores e pelas fraudes recorrentes, como a adulteração de atas eleitorais, problemas estruturais que a reforma constitucional aprovada no governo Artur Bernardes, com a introdução do voto secreto, não foi capaz de tangenciar.", 4))
lines.append(make_ce_item(44, 4, "História do Brasil", q44_text, "Embora com características bastante peculiares, que lhe imprimiram o rótulo de parlamentarismo às avessas, o regime parlamentarista implementado no Brasil, durante o Segundo Reinado, aproximava-se nitidamente do modelo inglês, dada a adoção do Poder Moderador, exercido pelo presidente do Conselho de Ministros.", 4))

# Q45
t45 = """Pode-se considerar a Constituição de 1988 como o marco que eliminou os últimos vestígios formais do regime autoritário, processo de abertura que, iniciado em 1974, levou mais de treze anos para desembocar em um regime democrático. Por que a transição foi tão longa e quais as consequências produzidas pela forma como se realizou? Vale lembrar que a estratégia adotada para a transição foi a de ser "lenta, gradual e segura". Ela só poderia ser modificada, no seu ritmo e na sua amplitude, se a oposição tivesse força suficiente para tanto ou se o desgaste do próprio regime autoritário provocasse seu colapso. Nem uma coisa nem outra aconteceu. Tivemos assim uma longa "transição transada", cheia de limites e incertezas.\nBoris Fausto. História do Brasil. São Paulo: Editora da Universidade de São Paulo, 2008, p. 526 (com adaptações)."""
q45_text = t45 + "\n\nTendo o texto acima como referência inicial e considerando o processo de transição do poder militar ao civil no Brasil contemporâneo, julgue (C ou E) os itens seguintes."
lines.append(make_ce_item(45, 1, "História do Brasil", q45_text, "A Constituição de 1988, marco jurídico-político da nova ordem democrática, promoveu clara valorização do ideal de cidadania, e, após mais de duas décadas de vigência, a Carta é questionada por ter ampliado consideravelmente a autonomia dos entes federados, em especial no que concerne ao campo fiscal, com a redução da área de atuação do poder central nesse importante setor.", 5))
lines.append(make_ce_item(45, 2, "História do Brasil", q45_text, "Dado o desgaste da política econômica conhecida como milagre econômico, o regime militar sofreu derrota nas eleições legislativas de 1974, tendo a oposição consentida, filiada ao MDB, conquistado maioria no Senado.", 5))
lines.append(make_ce_item(45, 3, "História do Brasil", q45_text, "Fundamental para a composição da Aliança Democrática, vitoriosa na eleição presidencial de 1985, a cisão do partido governista levou seus principais dirigentes à aliança formal com o PMDB, da qual surgiu a chapa Tancredo Neves (PMDB) e José Sarney (PDS).", 5))
lines.append(make_ce_item(45, 4, "História do Brasil", q45_text, "O início do processo de abertura política do regime militar associa-se ao governo de Geisel. O processo de distensão, marcado por avanços e recuos, esteve sob ameaça até o final do governo de Figueiredo, como demonstram os ataques a bancas de jornais e o atentado no Riocentro.", 5))

# Q46
q46_text = "QUESTÃO 46\nCom relação ao século XIX e ao movimento liberal, julgue (C ou E) os itens que se seguem."
lines.append(make_ce_item(46, 1, "História Mundial", q46_text, "Bastante singulares, os movimentos liberais dos jovens universitários na Alemanha, em 1820, arrefeceram-se ao longo do século XIX, em favor da superação do dilema entre unidade e liberalismo, como defendeu Bismarck na discussão sobre renúncia às liberdades parlamentares.", 5))
lines.append(make_ce_item(46, 2, "História Mundial", q46_text, "A unificação italiana, de pilar liberal, sob a liderança de Cavour, espraiou-se pela monarquia piemontesa, não tendo essa orientação ideológica, contudo, predominado em toda a península itálica.", 5))
lines.append(make_ce_item(46, 3, "História Mundial", q46_text, "A trajetória do liberalismo, no transcurso do século XIX, caracterizou-se por ambiguidade conceitual e prática, ora defendendo projetos reformistas, ora assumindo posições revolucionárias.", 5))
lines.append(make_ce_item(46, 4, "História Mundial", q46_text, "Na Europa, o liberalismo tomou forma, particularmente na década de 20 do século XIX, nas reformas democráticas e no combate às conspirações militares em defesa do Antigo Regime.", 5))

# Q47
t47 = """A atitude romântica teve, no Romantismo, a sua expressão mais completa, mas não se restringe a ele; o romântico vige até os dias de hoje. Não se trata de fenômeno exclusivamente alemão, mas na Alemanha ganhou marcas tão especiais que, no estrangeiro, volta e meia, confundem-se cultura alemã e atitude romântica.\nRüdiger Safranski. Romantik. Eine deutsche Affäre. München: Carl Hanser, 2007, p. 12 (Trad. com adaptações)."""
q47_text = t47 + "\n\nConsiderando o texto acima como referência inicial, assinale a opção correta a respeito do movimento romântico."
alts47 = [
    {"letter": "A", "text": "Alguns escritores europeus da segunda metade do século XIX, tais como Johann Wolfgang von Goethe, Charles Baudelaire e James Joyce, pertenceram à chamada geração ultrarromântica, marcada por atitude pessimista em relação à vida, gosto pelo macabro e pela vida boêmia."},
    {"letter": "B", "text": "Foi característica marcante do Romantismo literário a simpatia pela Antiguidade Clássica, sobretudo pela cultura latina, cujos padrões estilísticos os escritores oitocentistas procuraram emular."},
    {"letter": "C", "text": "As composições de Wolfgang Amadeus Mozart figuram como exemplos da música romântica, em razão da ênfase na expressão das emoções individuais, da preferência pela música instrumental, da opção frequente por grandes orquestras e da desvalorização da música sacra."},
    {"letter": "D", "text": "Diversos artistas e estetas românticos adotaram uma postura crítica diante do ideário iluminista ao enfatizarem a intuição, os sentimentos individuais, a imaginação, o mistério, em detrimento do racionalismo, do universalismo e do otimismo típicos dos iluministas."},
    {"letter": "E", "text": "Artistas ligados ao Romantismo alemão propunham aproximar dos seus congêneres europeus a literatura, a música e as artes plásticas produzidas nos países de língua alemã, o que, somado à atitude de desligamento em relação ao mundo cotidiano e à política, imunizou esse movimento contra o crescente nacionalismo da cena cultural europeia."}
]
lines.append(make_mc_item(47, "História Mundial", q47_text, alts47, 5))

# Q48
q48_text = "QUESTÃO 48\nNa chamada Era de Bismarck, as relações internacionais dos Estados europeus foram marcadas por concepções políticas e de segurança atribuídas, em parte, a esse chanceler alemão. A respeito desse tema e considerando o contexto europeu no referido período, julgue (C ou E) os itens que se seguem."
lines.append(make_ce_item(48, 1, "História Mundial", q48_text, "Entre 1870 e 1891, as relações internacionais da Europa foram marcadas pela ampliação da rigidez sistêmica e pela formação de bipolaridade de blocos, o que criou antagonismos entre antigas e novas potências.", 6))
lines.append(make_ce_item(48, 2, "História Mundial", q48_text, "O ensaio de uma política de país insatisfeito, ansioso por ampliar sua hegemonia, mesmo por meios semibelicosos, caracterizou a política internacional de Bismarck, o que suscitou fortes reações de potências europeias, em particular da França.", 6))
lines.append(make_ce_item(48, 3, "História Mundial", q48_text, "A política externa de Bismarck foi preferencialmente europeia e voltada para o equilíbrio do continente europeu, que, segundo o chanceler alemão, deveria ser recomposto após a guerra franco-prussiana.", 6))
lines.append(make_ce_item(48, 4, "História Mundial", q48_text, "Bismarck visava, entre outros aspectos, garantir a integridade territorial do recém-criado Estado alemão e o equilíbrio do sistema internacional europeu com a inclusão da Alemanha nesse sistema.", 6))

# Q49
q49_text = "QUESTÃO 49\nO conceito de imperialismo é polissêmico, tendo sido utilizado pela historiografia mundial em referência a diferentes processos históricos. Acerca do imperialismo formal no final do século XIX e início do século XX, julgue (C ou E) os itens subsequentes."
lines.append(make_ce_item(49, 1, "História Mundial", q49_text, "Os indirect rules, forma de ocupação territorial anglo-francesa na Ásia e na África, constituíram o modelo hegemônico de expansão imperialista europeia nas denominadas áreas periféricas.", 6))
lines.append(make_ce_item(49, 2, "História Mundial", q49_text, "Segundo Rosa Luxemburgo e Lênin, o imperialismo representava forma colonial de capitalismo, fusão do capitalismo industrial com a formação de oligopólios.", 6))
lines.append(make_ce_item(49, 3, "História Mundial", q49_text, "Durante o século XIX, o imperialismo europeu na África foi caracterizado pela ocupação gradual de grandes extensões territoriais, diferentemente do que ocorreu, nesse período, na América Latina.", 6))
lines.append(make_ce_item(49, 4, "História Mundial", q49_text, "Ao contrário do que aparentava, o imperialismo formal, que caracterizou o final do século XIX, foi uma continuação histórica de processo anterior, que, já em curso na história do Atlântico Sul desde os tempos do mercantilismo, permitia a acumulação capitalista por meio do mercado de escravos e especiarias.", 6))

# Q50
t50 = """A Revolução de Outubro teve repercussões muito mais profundas e globais que sua ancestral, pois, se as ideias da Revolução Francesa, como é hoje evidente, duraram mais que o bolchevismo, as consequências práticas de 1917 foram maiores e mais duradouras que as de 1789. A Revolução de Outubro produziu, de longe, o mais formidável movimento revolucionário organizado na história moderna. Sua expansão global não tem paralelo desde as conquistas do Islã em seu primeiro século.\nEric Hobsbawm. Era dos extremos. O breve século XX: 1914-1991. São Paulo: Companhia das Letras, 1994, p. 62 (com adaptações)."""
q50_text = t50 + "\n\nTendo o texto acima como referência inicial, julgue (C ou E) os itens seguintes, relativos aos impactos internacionais da Revolução Russa, de 1917."
lines.append(make_ce_item(50, 1, "História Mundial", q50_text, "A adoção da união antifascista permitiu que se rompesse, nos anos 20 e 30 do século XX, parte do isolamento sectário dos comunistas ortodoxos da Europa, propiciando-lhes a busca de apoio de massa tanto entre trabalhadores quanto entre intelectuais.", 6))
lines.append(make_ce_item(50, 2, "História Mundial", q50_text, "Na Ásia e na América Latina, a organização dos partidos comunistas após a Revolução Russa reproduziu, sem adaptações culturais e políticas, o modelo organizacional do Partido Comunista Russo.", 6))
lines.append(make_ce_item(50, 3, "História Mundial", q50_text, "Os impactos da Revolução Russa foram relevantes, mas não a ponto de acarretarem a imposição de uma disciplina de revolucionários profissionais a seus militantes, como evidenciam as resistências, na Terceira Internacional Comunista, ao modelo revolucionário soviético.", 6))
lines.append(make_ce_item(50, 4, "História Mundial", q50_text, "Menos de quarenta anos após a chegada de Lênin ao poder, os modelos socialistas inspirados na Revolução de Outubro fundamentavam os governos aos quais estava submetido aproximadamente um terço da população do mundo.", 6))

# Q51
q51_text = "QUESTÃO 51\nCom relação aos processos políticos, econômicos e sociais das Américas, bem como às relações internacionais nos séculos XIX, XX e XXI, assinale a opção correta."
alts51 = [
    {"letter": "A", "text": "Nos EUA, onde se desenvolveram processos históricos internos muito diversificados ao longo do século XIX, registra-se transformação pouco acentuada na sociedade individualista de pequenos produtores, a qual caracterizou o período que antecedeu e sucedeu a Guerra de Secessão."},
    {"letter": "B", "text": "No século XX, a América Latina moveu-se, de forma pendular, entre autonomia e dependência nas relações com as superpotências globais: em um primeiro momento, com Inglaterra e França e, em um segundo momento, com os EUA e a União das Repúblicas Socialistas Soviéticas (URSS)."},
    {"letter": "C", "text": "A América Latina aderiu aos movimentos não alinhados na Guerra Fria, como os liderados, nas décadas de 60 e 70 do século XX, por Nasser, no Egito, e Tito, na antiga Iugoslávia."},
    {"letter": "D", "text": "Ao conceito de América do Sul, que se sustenta em realidade geográfica e particularidade histórica associada à formação de fronteiras e dos Estados nacionais, vem sendo agregada conotação política, desde a passagem do século XX para o século XXI."},
    {"letter": "E", "text": "Embora bastante diferenciadas em suas formas históricas de colonização, as Américas revelam uma unidade ideológica e política que agrega, ainda hoje, um Norte mais desenvolvido e um Sul em processo de desenvolvimento."}
]
lines.append(make_mc_item(51, "História Mundial", q51_text, alts51, 6))

# Q52
q52_text = "QUESTÃO 52\nA Primeira e a Segunda Guerras Mundiais foram objeto de interpretações historiográficas divergentes, que se estendem aos dias atuais. Acerca desse debate historiográfico, julgue (C ou E) os itens que se seguem."
lines.append(make_ce_item(52, 1, "História Mundial", q52_text, "Em reação às acusações franco-britânicas de que a Alemanha seria a única responsável pela ocorrência dos dois conflitos mundiais do século XX, historiadores alemães defenderam consensualmente, na última década, a tese segundo a qual as provocações feitas pelo czar russo, no início do século XX, teriam assegurado à Alemanha o direito de legítima defesa.", 7))
lines.append(make_ce_item(52, 2, "História Mundial", q52_text, "Após a Segunda Guerra Mundial, surgiram, na historiografia alemã — como a de Fritz Fischer —, acerca da recente história política europeia, interpretações que destacavam a importância, para a eclosão dos dois conflitos mundiais, do desequilíbrio de poder europeu, resultante da ascensão da Alemanha no final do século XIX.", 7))
lines.append(make_ce_item(52, 3, "História Mundial", q52_text, "A chamada linha Maginot, estratégia defensiva posta em prática pela França no período que antecedeu ao início da Primeira Guerra Mundial, embora contestada inclusive por alguns oficiais franceses, contribuiu para retardar a invasão do país pelas tropas alemãs na Segunda Guerra.", 7))
lines.append(make_ce_item(52, 4, "História Mundial", q52_text, "A Primeira e a Segunda Guerras Mundiais foram explicadas fundamentalmente, pelos historiadores do século XX, como resultado exclusivo da atitude belicosa alemã.", 7))

# Q53
q53_text = "QUESTÃO 53\nAssinale a opção correta acerca do processo de independência das colônias de Portugal na África."
alts53 = [
    {"letter": "A", "text": "O poder da Organização das Nações Unidas na administração de conflitos internacionais foi determinante para o fim dos conflitos de independência na chamada África portuguesa."},
    {"letter": "B", "text": "O tardio processo de descolonização das colônias portuguesas na África, ao contrário do que ocorreu em momentos anteriores, como no da independência de países como Nigéria, Senegal e Tanzânia, é atribuído à capacidade militar e estratégica mantida pelos portugueses em suas possessões."},
    {"letter": "C", "text": "No movimento das independências africanas da década de 60 do século XX, as lutas nacionalistas, associadas a fatos novos relacionados à degradação da administração portuguesa na África e à crise do regime político luso, estão entre as causas da ruptura de Angola, Moçambique, Cabo Verde, Guiné-Bissau e São Tomé e Príncipe com a metrópole."},
    {"letter": "D", "text": "O clima de tensão na África austral, resultante da interferência da CIA e das forças soviéticas, além da presença de equipamentos e soldados cubanos na região, levou o Brasil a atuar como mediador das crises e propor a repartição dos Estados recém-nascidos, tornando-os satélites ora de uma superpotência, ora de outra."},
    {"letter": "E", "text": "A Guerra Fria, já em declínio nos anos 70 do século passado, foi fator pouco relevante no contexto da independência das colônias portuguesas na África."}
]
lines.append(make_mc_item(53, "História Mundial", q53_text, alts53, 7))

# Q54
q54_text = "QUESTÃO 54\nJulgue (C ou E) os itens que se seguem, relativos aos impactos da Revolução Russa na América Latina e no Caribe."
lines.append(make_ce_item(54, 1, "História Mundial", q54_text, "A Revolução Cubana já nasceu dirigida por militantes vinculados aos partidos comunistas da Europa oriental e aos interesses estratégicos da URSS na América Latina e no Caribe.", 7))
lines.append(make_ce_item(54, 2, "História Mundial", q54_text, "As lutas do general César Augusto Sandino contra fuzileiros navais norte-americanos, em fins da década de 20 do século passado, base da posterior Revolução Sandinista, na Nicarágua, foram marcadas por forte influência da Internacional Comunista.", 7))
lines.append(make_ce_item(54, 3, "História Mundial", q54_text, "A tensão ideológica e política da Guerra Fria e, em especial, os interesses soviéticos e dos partidos comunistas tiveram grande impacto na América Latina e culminaram na Revolução Cubana.", 7))
lines.append(make_ce_item(54, 4, "História Mundial", q54_text, "Embora tenha existido algum comunismo romântico na América Latina das primeiras décadas do século XX, e mesmo uma revolução social e política do peso da Revolução Mexicana, poucos grupos políticos absorveram o caminho da guerrilha comunista na região naquela quadra histórica.", 7))

# Q55
t55 = """Na pós-modernidade, a cultura expandiu-se a ponto de se tornar praticamente coextensiva à própria economia, não apenas como base sintomática de algumas das maiores indústrias do mundo, mas de maneira muito mais profunda, uma vez que todo objeto material ou serviço imaterial vira, de forma inseparável, uma marca trabalhável ou produto vendável. A cultura, nesse sentido, como inevitável tecido da vida no capitalismo avançado, é agora a nossa segunda natureza. Enquanto o Modernismo extraía seu propósito e energias da persistência do que ainda não era moderno, do legado de um passado ainda pré-industrial, o Pós-modernismo é a superação dessa distância, a saturação de cada poro do mundo com o soro do capital.\nPerry Anderson. As origens da pós-modernidade. Rio de Janeiro: Jorge Zahar, 1999, p. 13 (com adaptações)."""
q55_text = t55 + "\n\nA partir do texto acima, julgue (C ou E) os itens a seguir, relativos à dinâmica cultural dos séculos XX e XXI."
lines.append(make_ce_item(55, 1, "História Mundial", q55_text, "Os teóricos que se dedicam à análise da estética da pós-modernidade consideram-na basicamente um esforço coletivo de retomada da atitude vanguardista de rejeição do mundo da mercadoria e do espetáculo.", 7))
lines.append(make_ce_item(55, 2, "História Mundial", q55_text, "O modernismo europeu é o primeiro movimento estético derivado de vanguardas estéticas organizadas por grupos marginalizados da periferia do capitalismo, tais como aqueles que organizaram, no Brasil, em 1922, a Semana de Arte Moderna.", 7))
lines.append(make_ce_item(55, 3, "História Mundial", q55_text, "Uma faceta do alcance utópico da plasticidade das formas modernistas revela-se na arquitetura, que impõe a experiência estética ao cenário urbano cotidianamente degradado.", 7))
lines.append(make_ce_item(55, 4, "História Mundial", q55_text, "As vanguardas europeias do início do século XX caracterizaram-se pela atitude de rompimento formal com estruturas estéticas cristalizadas da arte ocidental.", 7))

# Q56
q56_text = "QUESTÃO 56\nAcerca da Constituição Federal de 1988 (CF), do controle de constitucionalidade e da personalidade jurídica no direito brasileiro, assinale a opção correta."
alts56 = [
    {"letter": "A", "text": "Dado que a personalidade jurídica é uma medida limitadora da possibilidade de adquirir direitos e contrair obrigações, nem todos os indivíduos a têm na mesma medida."},
    {"letter": "B", "text": "Os atos jurídicos normativos devem estar em conformidade com os preceitos constitucionais. No que diz respeito aos atos jurídicos de efeito concreto, estão sujeitos à autoridade normativa da CF os atos praticados na esfera dos Poderes Legislativo, Executivo e Judiciário, mas não os praticados por particulares."},
    {"letter": "C", "text": "A ação direta de inconstitucionalidade pode ser impetrada contra tratados que versem sobre direitos humanos com status de norma constitucional, contra tratados de direitos humanos que ingressem no ordenamento jurídico com a natureza de norma supralegal e contra os tratados que, não dispondo sobre direitos humanos, adentrem o ordenamento com força de lei ordinária."},
    {"letter": "D", "text": "Editadas unilateralmente pelo presidente da República, as medidas provisórias somente adquirem eficácia e plena aplicabilidade após serem aprovadas nas duas casas do Congresso Nacional e, consequentemente, convertidas em lei."},
    {"letter": "E", "text": "A CF é, quanto à estabilidade, uma constituição semirrígida, pois admite, desde que expressamente declarado, que lei infraconstitucional posterior possa alterá-la."}
]
lines.append(make_mc_item(56, "Direito e Direito Internacional", q56_text, alts56, 8))

# Q57
q57_text = "QUESTÃO 57\nCom relação à organização do Estado brasileiro e à disciplina constitucional sobre os Poderes Legislativo, Executivo e Judiciário, assinale a opção correta."
alts57 = [
    {"letter": "A", "text": "O Supremo Tribunal Federal (STF) é o órgão de cúpula jurisdicional e nacional do Poder Judiciário, mas não o órgão de cúpula administrativa, financeira e de cumprimento dos deveres funcionais dos juízes, papel que compete, conforme dispõe a CF, ao Conselho Nacional de Justiça."},
    {"letter": "B", "text": "Compete à Câmara dos Deputados e ao Senado Federal, em conjunto ou separadamente, a criação das comissões parlamentares de inquérito, que têm poderes de investigação próprios das autoridades judiciais e, portanto, podem impor penalidades ou condenações aos infratores."},
    {"letter": "C", "text": "A iniciativa popular de lei caracteriza-se como forma direta de exercício do poder, dispensado o intermédio de representantes para dar início ao processo legislativo de formação das normas. Nesse sentido, a CF prevê expressamente a iniciativa popular para a apresentação de projeto de lei e de proposta de emenda constitucional."},
    {"letter": "D", "text": "De acordo com a CF, incluem-se entre as competências privativas do presidente da República as de manter relações com Estados estrangeiros, acreditar seus representantes diplomáticos e celebrar tratados, convenções e atos internacionais, sujeitos a referendo do Congresso Nacional."},
    {"letter": "E", "text": "O Estado brasileiro, apesar de adotar o princípio da indissolubilidade do vínculo federativo, caracteriza-se, assim como ocorre com as confederações, pela soberania dual, na qual os entes federados são dotados de soberania, mas convivem com a existência da soberania central, exercida pela União em nome da Federação."}
]
lines.append(make_mc_item(57, "Direito e Direito Internacional", q57_text, alts57, 8))

# Q58
q58_text = "QUESTÃO 58\nPresentes em todos os continentes, as organizações não governamentais (ONGs) desempenham importante papel na defesa de causas de interesse comum da humanidade. Acerca da atuação dessas organizações, julgue (C ou E) os itens que se seguem."
lines.append(make_ce_item(58, 1, "Direito e Direito Internacional", q58_text, "Com características políticas e jurídicas de ONG e desprovido de atributos de personalidade jurídica internacional, o Comitê Internacional da Cruz Vermelha é sujeito apenas aparente de direito internacional público.", 8))
lines.append(make_ce_item(58, 2, "Direito e Direito Internacional", q58_text, "As ONGs que obtiveram reconhecimento da opinião pública mundial após a Segunda Guerra Mundial adquiriram personalidade jurídica de direito internacional público.", 8))
lines.append(make_ce_item(58, 3, "Direito e Direito Internacional", q58_text, "Embora atue em estreita cooperação com a Comissão Europeia e as demais instituições comunitárias do pilar econômico, a Organização de Cooperação e de Desenvolvimento Econômico tem natureza jurídica de ONG.", 8))
lines.append(make_ce_item(58, 4, "Direito e Direito Internacional", q58_text, "Não obstante suas peculiaridades jurídicas, o Greenpeace, além de ter atuado como parte nas negociações do Protocolo de Quioto, firmou e ratificou o referido tratado.", 8))

# Q59
q59_text = "QUESTÃO 59\nAssinale a opção correta a respeito da atuação diplomática brasileira na condução de contenciosos internacionais, em particular no que concerne às controvérsias no âmbito da Organização Mundial do Comércio (OMC)."
alts59 = [
    {"letter": "A", "text": "A cláusula que dispõe sobre a nação mais favorecida, avanço introduzido na transição do Acordo Geral de Tarifas e Comércio para a OMC, constitui um dos princípios diretores do sistema multilateral de comércio."},
    {"letter": "B", "text": "Os relatórios dos painéis, com poder de decisão arbitral, são, além de irrecorríveis, compulsórios a todos os Estados-membros da OMC."},
    {"letter": "C", "text": "No caso das aeronaves regionais, que envolveu a Empresa Brasileira de Aeronáutica e a empresa canadense Bombardier, as partes não exerceram o direito de retaliação que lhes foi garantido pela OMC."},
    {"letter": "D", "text": "Ainda debutante na máxima instância do sistema multilateral de comércio, a China, apesar de sua atuação agressiva na busca de novos mercados e de inserção internacional, ainda não participou de nenhum caso no Órgão de Solução de Controvérsias da OMC."},
    {"letter": "E", "text": "O consenso invertido, regra adotada na instauração da OMC, favoreceu, não obstante seus propósitos de legalidade, a prevalência de decisões políticas sobre decisões jurídicas."}
]
lines.append(make_mc_item(59, "Direito e Direito Internacional", q59_text, alts59, 8))

# Q60
t60 = """Dois ex-empregados da missão diplomática do Estado X situada no Estado Y ajuizaram contra aquele Estado reclamação na justiça trabalhista deste Estado, alegando que alguns de seus salários não haviam sido pagos. Tendo julgado procedente a reclamação, a justiça trabalhista do Estado Y determinou, a fim de satisfazer os créditos dos ex-empregados, a penhora de bens, incluído o próprio prédio da referida missão diplomática."""
q60_text = t60 + "\n\nCom relação a essa situação hipotética, assinale a opção correta."
alts60 = [
    {"letter": "A", "text": "Caso o Estado Y fosse o Brasil, a justiça trabalhista não poderia, de acordo com a jurisprudência do STF, determinar a penhora de bens do Estado X, por gozar o Estado estrangeiro de imunidade de execução."},
    {"letter": "B", "text": "A justiça trabalhista do Estado Y não deveria ter conhecido da ação, pois a Convenção de Viena sobre Relações Diplomáticas estabelece a imunidade de jurisdição do Estado estrangeiro em matéria trabalhista."},
    {"letter": "C", "text": "A justiça trabalhista do Estado Y não deveria ter conhecido da ação, pois casos que envolvam imunidade de jurisdição e execução somente podem ser julgados por tribunais internacionais."},
    {"letter": "D", "text": "Caso a penhora recaísse sobre a residência oficial do embaixador, ela seria considerada lícita perante o direito internacional."},
    {"letter": "E", "text": "Sob o prisma do direito internacional, a penhora do prédio da missão diplomática é lícita."}
]
lines.append(make_mc_item(60, "Direito e Direito Internacional", q60_text, alts60, 9))

# Q61
q61_text = "QUESTÃO 61\nA regulação dos fluxos externos está associada à utilização de instrumentos cambiais ou não considerados mais ou menos eficazes, conforme seus objetivos e suas respectivas circunstâncias. A respeito da utilização de tais instrumentos, julgue (C ou E) os próximos itens."
lines.append(make_ce_item(61, 1, "Economia", q61_text, "A ausência de barreiras, em prol da liberalização das trocas externas, promove, entre outros benefícios, o aumento da autossuficiência dos países no que concerne à disponibilidade de bens e serviços e a redução dos riscos associados às oscilações nas quantidades produzidas e nos preços praticados.", 9))
lines.append(make_ce_item(61, 2, "Economia", q61_text, "A obtenção de economias crescentes de escala é um dos benefícios indiretos do estabelecimento de restrições fitossanitárias, o qual, em razão de sua natureza concreta e objetiva, propicia retaliações internacionais.", 9))
lines.append(make_ce_item(61, 3, "Economia", q61_text, "Um dos argumentos em favor da imposição de barreiras alfandegárias é o de que, com esse procedimento, se evita a exportação de empregos, que, igualmente, tende a ocorrer quando, por efeito da valorização do câmbio, as exportações de um país se tornam menos competitivas.", 9))
lines.append(make_ce_item(61, 4, "Economia", q61_text, "De acordo com a teoria cambial básica, com taxas flutuantes e mercado similar ao de concorrência perfeita, os déficits no balanço de pagamentos provocariam apreciação real da taxa de câmbio, e os superávits, depreciação, o que conduziria ao equilíbrio do balanço de pagamentos.", 9))

# Q62
q62_text = "QUESTÃO 62\nCelso Furtado, ao analisar o desenvolvimento brasileiro da primeira metade do século XX, afirmou que houve um processo de articulação das distintas regiões do país em um sistema com um mínimo de integração. De acordo com esse autor,"
alts62 = [
    {"letter": "A", "text": "o processo de integração, subsequente ao de articulação, deveria ter-se orientado no sentido de exportar produtos antes absorbidos pelas regiões mais prósperas."},
    {"letter": "B", "text": "o processo de industrialização teve início em períodos diferentes nas várias regiões brasileiras, tendo-se dispersado fortemente principalmente no pós-guerra."},
    {"letter": "C", "text": "o fluxo de mão de obra da região de mais baixa produtividade para outra região de produtividade mais alta tendeu a pressionar os níveis salariais desta última, que se mantiveram, então, aquém da elevação da produtividade."},
    {"letter": "D", "text": "os preços dos produtos essenciais eram relativamente baixos nas regiões de mais baixa produtividade, o que resultou em salários monetários relativamente baixos em função da produtividade."},
    {"letter": "E", "text": "o rápido crescimento da economia cafeeira no período entre 1880 e 1930 reduziu significativamente as diferenças regionais de renda per capita."}
]
lines.append(make_mc_item(62, "Economia", q62_text, alts62, 9))

# Q63
q63_text = "QUESTÃO 63\nJulgue (C ou E) os itens subsequentes, relativos a conceitos da economia internacional."
lines.append(make_ce_item(63, 1, "Economia", q63_text, "Os aumentos do imposto sobre operações financeiras incidente sobre os investimentos estrangeiros constituem exemplos de controles de capitais de curto prazo, cujo objetivo é neutralizar os impactos decorrentes da volatilidade dos fluxos desse tipo de capital sobre os mercados cambial e de capitais.", 9))
lines.append(make_ce_item(63, 2, "Economia", q63_text, "A imposição de tarifas, além de transferir recursos dos consumidores para o governo, conduz ao aumento dos preços dos bens domésticos e eleva a ineficiência na economia.", 9))
lines.append(make_ce_item(63, 3, "Economia", q63_text, "Nos sistemas de câmbio fixo, as políticas monetárias expansionistas são particularmente eficazes para elevar a demanda agregada porque, nesses sistemas, o efeito deslocamento é minimizado.", 9))
lines.append(make_ce_item(63, 4, "Economia", q63_text, "Por elevar o custo de oportunidade do consumo, a especialização constitui uma das bases do comércio internacional, o que contradiz a lei das vantagens comparativas.", 9))

# Q64
q64_text = "QUESTÃO 64\nA respeito do Plano Real, que se destacou, na economia brasileira, por ter sido eficaz no combate à inflação, assinale a opção correta."
alts64 = [
    {"letter": "A", "text": "A queda duradoura da inflação foi facilitada pela redução da demanda agregada e pela expansão da entrada de capitais no período de vigência do plano."},
    {"letter": "B", "text": "O sucesso desse plano deveu-se, em parte, à política monetária expansionista combinada com forte ajuste fiscal."},
    {"letter": "C", "text": "Reservas elevadas, abertura comercial e valorização cambial contribuíram para restringir a alta dos preços internos."},
    {"letter": "D", "text": "A política cambial caracterizou-se pela fixação da taxa de câmbio real bem como da taxa de câmbio nominal."},
    {"letter": "E", "text": "O diagnóstico da inflação, no âmbito desse plano, excluía o caráter inercial da alta de preços no Brasil."}
]
lines.append(make_mc_item(64, "Economia", q64_text, alts64, 10))

# Q65
t65 = """Dados relativos às contas brasileiras do setor externo em 2010 (em bilhões de dólares)
superávit do balanço de pagamentos: 49,1
déficit em transações correntes: 47,5
déficit na conta de serviços: 31,1
remessa líquida de renda: 39,6
investimentos estrangeiros diretos: 48,5
investimentos brasileiros diretos no exterior: 11,5
investimentos estrangeiros em carteira: 67,8
saldo de outros investimentos brasileiros no exterior e outros investimentos estrangeiros no país: 2,3
reservas internacionais (em 31/12/2010): 288,6
dívida externa total (em 31/12/2010): 255,7"""
q65_text = t65 + "\n\nA partir dos dados apresentados na tabela acima, divulgados pelo Banco Central do Brasil em 25/1/2011, assinale a opção correta."
alts65 = [
    {"letter": "A", "text": "A principal contribuição para o déficit na conta de serviços provém de lucros e dividendos e, para as remessas líquidas, de aluguel de equipamentos e viagens internacionais."},
    {"letter": "B", "text": "A dívida externa líquida brasileira é de US$ 32,9 bilhões."},
    {"letter": "C", "text": "A balança comercial apresentou déficit no período considerado."},
    {"letter": "D", "text": "Os investimentos estrangeiros diretos compreendem a formação e o aumento do capital de empresas, incluídas as aquisições de ações em bolsa."},
    {"letter": "E", "text": "O Brasil obteve poupança externa no valor de US$ 47,5 bilhões."}
]
lines.append(make_mc_item(65, "Economia", q65_text, alts65, 10))

output_filename = "questoes_transcritas.jsonl"
with open(output_filename, "w", encoding="utf-8") as f:
    for item in lines:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Generated {len(lines)} JSON lines in {output_filename}")