import json

# Definição do contexto fixo
contest_id = "CACD_2013"
year = 2013
phase = 1
stage = "primeira_fase"
caderno = "TARDE"
source_file = "prova_objetiva_2__7f084ea4.pdf"

# Lista completa de objetos transcritos
data = [
    # QUESTÃO 29
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 29, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "According to the text,",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "both environmentalists and economists agree that consumption is at the heart of the current financial and environmental crises."},
            {"letter": "B", "text": "the need to understand the current capitalist crisis is urging environmentalists and economists to launch publications on the issue."},
            {"letter": "C", "text": "financial and environmental debts have been primarily affecting wealthy countries due to their reckless consumption attitude."},
            {"letter": "D", "text": "business and finance experts had warned Greenpeace activists about the financial consequences of natural resource shortages."},
            {"letter": "E", "text": "the synergetic link between economy and environment points to the need to tackle financial issues ahead of environmental ones."}
        ],
        "answer": null, "page": 1, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 30
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 30, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Based on the text, choose the correct answer.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "The expression \"consumer binge\" (l.35) is used as an antonym for the expression \"reckless consumption\" (l.33)."},
            {"letter": "B", "text": "The word \"cogent\" (l.12) suggests that the argument put forward by Amy Larkin is ill-founded."},
            {"letter": "C", "text": "If the verb \"catching up with\" (l.14) is replaced by stemming from, the meaning of the sentence remains unaltered."},
            {"letter": "D", "text": "The word \"looming\" (l.21) is used as a synonym for unlikely."},
            {"letter": "E", "text": "The words \"crunch\" (l.22) and \"crunches\" (l.29) are used as synonyms for crisis and crises, respectively."}
        ],
        "answer": null, "page": 1, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 31
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 31, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "The sentence \"By ransacking global (...) credit card draws down financial credit\" (l.25-28) means that,",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "by ignoring the need to protect the environment, our society is increasingly focused on profit rather than quality of life."},
            {"letter": "B", "text": "due to our reckless behavior towards the environment, less financial support has been assigned to nature-saving projects."},
            {"letter": "C", "text": "due to the scarcity of environmental fund-raising actions, mankind is making the exploitation of natural resources financially unviable."},
            {"letter": "D", "text": "by tampering with the world biomass, we are affecting investments in the area as much as economic problems affect us."},
            {"letter": "E", "text": "by destroying nature, we are reducing our environmental funds just like too many debts reduce our financial credibility."}
        ],
        "answer": null, "page": 1, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 32
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 32, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "Based on the text, judge if the items below are right (C) or wrong (E).",
        "item_text": "Wall Street and the City experts foresee a complete market breakdown.",
        "alternatives": null, "answer": null, "page": 1, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 32, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "Based on the text, judge if the items below are right (C) or wrong (E).",
        "item_text": "As far as the main issue of the text is concerned, the two economists of the Swiss bank are of the same opinion as the ecologist-author.",
        "alternatives": null, "answer": null, "page": 1, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 32, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "Based on the text, judge if the items below are right (C) or wrong (E).",
        "item_text": "Several bank owners claim the economic crisis should be solved first.",
        "alternatives": null, "answer": null, "page": 1, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 32, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "Based on the text, judge if the items below are right (C) or wrong (E).",
        "item_text": "Amy Larkin believes the worldwide scarcity of resources is affecting the world's economy.",
        "alternatives": null, "answer": null, "page": 1, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 33
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 33, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Based on the text, choose the correct statement.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "The cities that host G8 summits generally profit from the presence of presidents and ministers."},
            {"letter": "B", "text": "The reasons for young people's frustrations include political, financial and economic issues."},
            {"letter": "C", "text": "In the 39th G8 Summit meeting, empty promises will give room to debates on the global crises."},
            {"letter": "D", "text": "Young people are planning demonstrations to show their dissatisfaction to the G8 Summit leaders."},
            {"letter": "E", "text": "The actions taken for international cooperation are condemned by the new Facebook generation leaders."}
        ],
        "answer": null, "page": 2, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 34
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 34, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "In the text, \"that need\" (l.6) refers to",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "convening in Ireland."},
            {"letter": "B", "text": "measuring progress."},
            {"letter": "C", "text": "engaging in dialogue."},
            {"letter": "D", "text": "facing global crises."},
            {"letter": "E", "text": "making promises."}
        ],
        "answer": null, "page": 2, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 35
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 35, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "According to the author,",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "common language opposes poetry."},
            {"letter": "B", "text": "diplomacy is related to persuasion."},
            {"letter": "C", "text": "ideas last less than material things."},
            {"letter": "D", "text": "language is a demagogical expression."},
            {"letter": "E", "text": "ideologies require a proper language."}
        ],
        "answer": null, "page": 2, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 36
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 36, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "In relation to the pronouns shown in bold in the text above, judge if the items below are right (C) or wrong (E).",
        "item_text": "The pronoun \"that\" (l.21) refers to \"language\" (l.20).",
        "alternatives": null, "answer": null, "page": 2, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 36, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "In relation to the pronouns shown in bold in the text above, judge if the items below are right (C) or wrong (E).",
        "item_text": "The pronoun \"theirs\" (l.5) refers to \"others\" (l.4).",
        "alternatives": null, "answer": null, "page": 2, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 36, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "In relation to the pronouns shown in bold in the text above, judge if the items below are right (C) or wrong (E).",
        "item_text": "The pronoun \"It\" (l.5) refers to \"diplomacy\" (l.2).",
        "alternatives": null, "answer": null, "page": 2, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 36, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "In relation to the pronouns shown in bold in the text above, judge if the items below are right (C) or wrong (E).",
        "item_text": "The pronoun \"they\" (l.13) refers to \"Ideas\" (l.11).",
        "alternatives": null, "answer": null, "page": 2, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 37
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 37, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "The words \"poised\" (l.19) and \"yields\" (l.47 and 53) mean, respectively,",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "etiolated and profits."},
            {"letter": "B", "text": "shaken and gains."},
            {"letter": "C", "text": "ready and risks."},
            {"letter": "D", "text": "bolstered and outlay."},
            {"letter": "E", "text": "on the verge and returns."}
        ],
        "answer": null, "page": 3, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 38
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 38, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "According to the text, judge if the following items are right (C) or wrong (E).",
        "item_text": "According to at least one financial adviser, it's naïve to correlate bonds with interest rates.",
        "alternatives": null, "answer": null, "page": 3, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 38, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "According to the text, judge if the following items are right (C) or wrong (E).",
        "item_text": "The main contention of the article is that investors should be skeptical about Bernanke's remark in relation to the effects of the American economic recovery.",
        "alternatives": null, "answer": null, "page": 3, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 38, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "According to the text, judge if the following items are right (C) or wrong (E).",
        "item_text": "The bond market is in such a predicament due to misjudgment on the part of the American central bank's chairperson.",
        "alternatives": null, "answer": null, "page": 3, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 38, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "According to the text, judge if the following items are right (C) or wrong (E).",
        "item_text": "In general, bonds provide stability to an investor's portfolio.",
        "alternatives": null, "answer": null, "page": 3, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 39
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 39, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "Regarding the text, judge if the items below are right (C) or wrong (E).",
        "item_text": "The word \"from\" in the excerpt \"Making a bet on interest rates is no different from trying to predict the next big drop in stocks, or jumping into the market when it appears to be poised to surge higher.\" (l.27-29) may be replaced by the word then with no interference in the grammar correction of the sentence.",
        "alternatives": null, "answer": null, "page": 3, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 39, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "Regarding the text, judge if the items below are right (C) or wrong (E).",
        "item_text": "In the sentence \"Their cue came from the Federal Reserve chairman, Ben Bernanke, who recently suggested that the economic recovery might allow the central bank to ease its efforts to stimulate the economy.\" (l.14-17) the relative pronoun \"who\" may be replaced by whom in more formal contexts.",
        "alternatives": null, "answer": null, "page": 3, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 39, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "Regarding the text, judge if the items below are right (C) or wrong (E).",
        "item_text": "In the sentence \"That includes scaling back its bond-buying program beginning later this year.\" (l.17-18), the pronoun \"its\" refers to \"economy\", in the previous sentence.",
        "alternatives": null, "answer": null, "page": 3, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 39, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "Regarding the text, judge if the items below are right (C) or wrong (E).",
        "item_text": "In the sentence \"United States government notes with maturities of 10 years or longer, however, lost an average of 10.8 percent over the same period.\" (l.24-26), the adverb \"however\" may be moved to the beginning of the sentence without interfering in the meaning.",
        "alternatives": null, "answer": null, "page": 3, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 40
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Língua Inglesa", "question_number": 40, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Each of the options below presents an excerpt taken from the text and a version of the same excerpt. Choose the one which has retained most of the original meaning found in the text.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "\"In the year following the disclosure about his relatives, the files speak of Minor's having started to take walks out on the Terrace in all weathers, angrily denouncing those who tried to persuade him to come back in...\" (l.36-39) / In the year after the revelation about his relatives, the archives show that Minor had started to take walks out on the Terrace during any kind of weather, angrily extolling people who tried to convince him to come back in..."},
            {"letter": "B", "text": "\"He was replaced by Doctor Brayn, a man selected (...) by a Home Office that felt a stricter regime needed to be employed at the asylum.\" (l.5-8) / He was substituted by Doctor Brayn, a man picked over (...) by a Home Office who believed a more rigid regimen needed to be established at the asylum."},
            {"letter": "C", "text": "\"Brayn was indeed a martinet, a jailer of the old school who would have done well at any prison farm\" (l.9-10) / Brayn was really punctilious, a traditional jailer who would have been successful working at any prison farm."},
            {"letter": "D", "text": "\"There were no escapes during his term of office (...), and in the first year two hundred thousand hours of solitary confinement were logged by the more fractious inmates.\" (l.11-15) / No one escaped while he was in office (...), and in the first year of his mandate two hundred thousand hours of solitary confinement were registered by the more ingratiating prisoners."},
            {"letter": "E", "text": "\"One curious snippet of information came from the United States later that same year, when it was noted rather laconically that two of Minor's family had recently killed themselves...\" (l.19-22) / One odd piece of information came from the United States later that same year, when it was noted rather verbosely that two of Minor's relatives had recently killed themselves..."}
        ],
        "answer": null, "page": 4, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 41
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 41, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Assinale a opção correta a respeito do processo de independência do Brasil.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "O movimento republicano secessionista no norte do Brasil, em 1820, propiciou a conscientização da elite do sudeste da necessidade da independência, a fim de se impedir que regiões brasileiras a fizessem autonomamente e se desintegrassem do território nacional."},
            {"letter": "B", "text": "Embora o exclusivismo comercial tenha acabado em 1808, com a abertura dos portos às nações amigas, somente em 7 de setembro de 1822, o Brasil deixou de ser colônia política."},
            {"letter": "C", "text": "A Revolução Liberal do Porto, em 1820, criou, tanto em Portugal quanto no Brasil, um clima de liberdade, que favoreceu a discussão de novas ideias políticas."},
            {"letter": "D", "text": "A tentativa das Cortes de Lisboa de impor à colônia brasileira a condição de Reino Unido, por acarretar impostos adicionais à elite local, foi o fato desencadeador da Proclamação da Independência do Brasil."},
            {"letter": "E", "text": "A derrota portuguesa da tentativa de ocupar a Banda Oriental desmoralizou D. João perante as elites brasileiras e contribuiu para o surgimento do projeto de rompimento dos laços coloniais."}
        ],
        "answer": null, "page": 4, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 42
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 42, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "No que concerne ao período regencial no Brasil, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "O regresso conservador alterou a política externa, ao priorizar a contenção de Rosas, líder da Confederação Argentina."},
            {"letter": "B", "text": "O período regencial iniciou-se na abdicação de Pedro I ao trono, em decorrência de pressões diplomáticas britânicas e da oposição das elites escravocratas."},
            {"letter": "C", "text": "Durante o avanço liberal, o Senado foi extinto como resultado da ação dos exaltados contra o que classificavam como reduto caramuru."},
            {"letter": "D", "text": "No período regencial no Brasil, houve fraca coesão entre as elites e importante participação dos setores populares no processo político."},
            {"letter": "E", "text": "O Ato Adicional de 1834 fortaleceu o Exército, que teve ampliado seu efetivo, oportunidade de profissionalização de seus membros e assegurou importância política."}
        ],
        "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 43
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 43, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "Acerca da configuração territorial da América portuguesa, julgue (C ou E) os seguintes itens.",
        "item_text": "O Tratado de Madri tinha como princípio principal, quanto à definição de fronteiras, o uti possidetis e como argumento subsidiário, aplicável à foz do Amazonas e ao Rio da Prata, o mare liberum.",
        "alternatives": null, "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 43, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "Acerca da configuração territorial da América portuguesa, julgue (C ou E) os seguintes itens.",
        "item_text": "A expansão territorial para o sul, para que o Rio da Prata fosse limite natural, resultou na fundação de Montevidéu em 1680.",
        "alternatives": null, "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 43, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "Acerca da configuração territorial da América portuguesa, julgue (C ou E) os seguintes itens.",
        "item_text": "No século XVII, os portugueses conquistaram o litoral nordestino e a foz do rio Amazonas.",
        "alternatives": null, "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 43, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "Acerca da configuração territorial da América portuguesa, julgue (C ou E) os seguintes itens.",
        "item_text": "A criação de gado foi a primeira atividade produtiva promotora da interiorização mais profunda da colonização.",
        "alternatives": null, "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 44
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 44, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Acerca da política externa adotada pelo governo brasileiro no período entre 1930 e 1945, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "A demonstração de simpatia do presidente Getúlio Vargas pelos regimes totalitários europeus e o incremento do comércio entre Brasil e Alemanha justificavam a intensa campanha governista de nacionalização dos imigrantes residentes na Região Sul e a proibição de propaganda e organização de partidos políticos."},
            {"letter": "B", "text": "Em que pesem as pressões dos Estados Unidos da América (EUA), o Brasil aceitou manter relações comerciais com a Alemanha baseadas em moeda não conversível, denominada marco de compensação."},
            {"letter": "C", "text": "A nomeação de Osvaldo Aranha para o Ministério das Relações Exteriores em 1938 introduziu rupturas fundamentais no encaminhamento da ação internacional do Brasil, que passou a desenvolver estratégia de barganha com os EUA e a Alemanha."},
            {"letter": "D", "text": "Na fase inicial desse período, a política externa adquiriu um tom francamente belicoso e expansionista, como demonstram as ações de intervenção do Brasil em assuntos internos dos países vizinhos, ao tomar partido nos conflitos, como na Guerra do Chaco, entre a Bolívia e o Paraguai, e na Questão de Letícia, entre o Peru e a Colômbia."},
            {"letter": "E", "text": "O Itamaraty, na VII Conferência Internacional Americana, realizada em Montevidéu, em 1933, reiterou a repulsa do governo brasileiro a alianças como a do Pacto Briand-Kellog."}
        ],
        "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 45
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 45, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "A revolução de 1930 introduziu mudanças políticas, econômicas, sociais e na política externa. A respeito dessas mudanças, julgue (C ou E) os itens a seguir.",
        "item_text": "O Estado empreendeu, a partir de 1930, ação determinante na educação, com o intuito de criar um sistema nacional, esforço que envolveu educadores de diferentes correntes, como a dos reformadores liberais e a dos católicos, e também a própria elite cultural.",
        "alternatives": null, "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 45, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "A revolução de 1930 introduziu mudanças políticas, econômicas, sociais e na política externa. A respeito dessas mudanças, julgue (C ou E) os itens a seguir.",
        "item_text": "O poder estatal tratou, a partir de 1930, de promover alianças de classes, garantindo direitos sociais e mecanismos de proteção aos trabalhadores urbanos.",
        "alternatives": null, "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 45, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "A revolução de 1930 introduziu mudanças políticas, econômicas, sociais e na política externa. A respeito dessas mudanças, julgue (C ou E) os itens a seguir.",
        "item_text": "Afastadas do núcleo central do Estado, as Forças Armadas foram substituídas, em suas funções de garantidoras da ordem interna, por novos aparelhos repressivos, que reproduziam os criados pelo fascismo europeu.",
        "alternatives": null, "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História do Brasil", "question_number": 45, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "A revolução de 1930 introduziu mudanças políticas, econômicas, sociais e na política externa. A respeito dessas mudanças, julgue (C ou E) os itens a seguir.",
        "item_text": "Sem ruptura com a política que vinha sendo implementada, a política externa do governo revolucionário caracterizou-se pelo protagonismo no plano regional e pela centralidade do relacionamento com os EUA.",
        "alternatives": null, "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 46
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 46, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "A execução de Carlos I, em 30 de janeiro de 1649, foi decisão do Parlamento inglês que simbolizou o fim do absolutismo na Inglaterra e comprometeu o mito da identificação entre poder real e sua origem divina. Manifestação inicial da crise do Antigo Regime, a Revolução Inglesa do século XVII foi o ponto de partida da Era das Revoluções, que, entre fins do século XVIII e primeira metade do século XIX, iria desvelar o mundo contemporâneo. Relativamente a esse processo histórico, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "A Revolução Francesa de 1789 marcou o perfil ideológico das revoluções burguesas, dado seu caráter liberal e pioneiramente democrático, que acompanhou todo o processo revolucionário, da queda da Bastilha à ascensão de Napoleão Bonaparte ao poder."},
            {"letter": "B", "text": "A Revolução Puritana de 1640 e a Revolução Gloriosa de 1688, ainda que integrantes de um mesmo contexto, são distintas nos propósitos e nos meios utilizados, visto que a segunda se insurgiu contra o Parlamento, mas procurou manter incólume o poder monárquico."},
            {"letter": "C", "text": "Dois motivos excluem a Revolução Industrial do conjunto de revoluções burguesas que sepultaram o Antigo Regime: ter mantido em aberto o processo de transição do feudalismo ao capitalismo e ter exercido diminuta influência na transformação política dos países que se industrializavam."},
            {"letter": "D", "text": "Chamados iluministas, pensadores europeus do século XVIII – especialmente franceses – revolucionaram intelectualmente o mundo moderno ao atacarem com vigor a injustiça, a intolerância religiosa e os privilégios, preparando o terreno para as revoluções que destruiriam o Antigo Regime."},
            {"letter": "E", "text": "Considerada a primeira revolução americana, a independência das 13 colônias inglesas da América do Norte foi facilitada pela homogeneidade da colonização e pela decisão da Inglaterra de não reagir militarmente ao movimento separatista, para assegurar a continuidade dos negócios na região."}
        ],
        "answer": null, "page": 5, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 47
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 47, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "A partir de meados do século XIX, acompanhando o processo de desenvolvimento da industrialização, o proletariado buscou desenvolver formas de solidariedade. Nessa perspectiva, surgiram cooperativas, associações de ajuda mútua e, por fim, sindicatos. Muitos governos chegaram a desenvolver políticas sociais, provavelmente para enquadrar o movimento operário, como evidencia a avançada política habitacional na Alemanha de Bismarck. Relativamente a esse cenário, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "Surgida em 1864, a Associação Internacional dos Trabalhadores, ou I Internacional, pretendia articular a luta do movimento operário em escala mundial."},
            {"letter": "B", "text": "Ao longo do século XIX, o movimento operário europeu foi marcadamente ideológico e, na maioria absoluta dos casos, plenamente identificado com o socialismo."},
            {"letter": "C", "text": "Presa às circunstâncias históricas do passado, a Igreja Católica mostrou-se insensível à questão social, vindo a se manifestar sobre esse tema apenas no século XX."},
            {"letter": "D", "text": "Com o apoio das tropas prussianas, a Comuna de Paris logrou assumir o controle da capital francesa e nela implantou o modelo anarquista de administração pública."},
            {"letter": "E", "text": "Apesar da acirrada oposição de Marx e Engels, o avanço do movimento operário sustentou-se em aguda radicalização política e ideológica."}
        ],
        "answer": null, "page": 6, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 48
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 48, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "A Segunda Guerra Mundial (1939-1945) é, geralmente, considerada o grande momento de inflexão do século XX. Decorrência de duas décadas de instabilidade política, comoção social e crise económica, ela foi o mais universalizado dos conflitos e, ao chegar ao fim, gerou uma ordem internacional que se afastava dos padrões vigentes, a rigor, desde a Idade Moderna. Relativamente aos fatores que determinaram o início de hostilidades e às conferências que estabeleceram as balizas do novo cenário mundial, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "A Conferência de Potsdam definiu a internacionalização de Berlim e a divisão da Alemanha em duas áreas de influência: a área sob influência da União Soviética e a sob influência dos EUA."},
            {"letter": "B", "text": "Embora combatido por liberais, trotskistas e social-democratas, o Pacto de Não-Agressão Germano-Soviético foi fundamental para retardar o início da Segunda Guerra Mundial."},
            {"letter": "C", "text": "A política da Paz Armada desencadeada por Hitler, ainda que não necessariamente expansionista, abriu o caminho para a guerra, por gerar desconfiança e temor generalizados."},
            {"letter": "D", "text": "A Liga das Nações condenou a anexação da Áustria pela Alemanha nazista, tendo sido veemente o protesto da França e da Inglaterra, que romperam relações diplomáticas com Berlim."},
            {"letter": "E", "text": "Em face de sua contribuição na luta contra o Reich nazista, a União Soviética teve o reconhecimento internacional reforçado na Conferência de Teerã e, em Yalta, assegurou sua influência no Leste Europeu."}
        ],
        "answer": null, "page": 6, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 49
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 49, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Rússia e China protagonizaram as duas mais importantes revoluções socialistas que o século XX conheceu, cujos passos, na América Latina do pós-Segunda Guerra Mundial, foram seguidos por Cuba. Relativamente aos processos revolucionários que exerceram considerável impacto na história do mundo contemporâneo, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "Tão logo se tornou vitoriosa, em 1959, a Revolução Cubana definiu-se como marxista. A despeito do contexto de coexistência pacífica que vigorava então nas relações internacionais, a presença de um regime socialista nas Américas repercutiu nos demais países do continente, cujos governos, majoritariamente, apoiavam as iniciativas de Fidel Castro."},
            {"letter": "B", "text": "Dada a sua participação na Grande Guerra de 1914, a Rússia czarista enfrentou efeitos devastadores, tais como sublevações nas províncias muçulmanas da Ásia Central, revoltas camponesas e desintegração do próprio exército. Esses e outros fatores foram essenciais para os dois movimentos revoltosos que, em 1917, derrubaram a tricentenária dinastia dos Romanov e instituíram a república socialista."},
            {"letter": "C", "text": "Reforma agrária e nacionalização de indústrias e bancos incluem-se nas primeiras decisões tomadas pelo governo bolchevique de Lênin, as quais foram mantidas, sem retrocesso, ao longo da experiência socialista da União Soviética, aprofundadas sob Stálin e apenas amainadas com o advento da perestroika, já em meados dos anos 80."},
            {"letter": "D", "text": "Sob a liderança de Mao Zedong, o objetivo da Revolução Chinesa era implantar as concepções marxistas em uma das mais antigas civilizações do mundo, seguindo como modelo – praticamente sem alterações substanciais – a experiência soviética, o que explica a permanente aliança entre China e União Soviética, apenas desfeita quando o reformista Gorbatchev assumiu o poder em Moscou."},
            {"letter": "E", "text": "Os bons resultados dos planos econômicos implantados por Mao Zedong nos anos 50 do século passado criaram condições para que o \"grande timoneiro\" flexibilizasse o regime político que comandava, abertura política que se concretizou na Revolução Cultural e permitiu à China usufruir, a partir de 1966 e durante uma década, de certos padrões de democracia."}
        ],
        "answer": null, "page": 6, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 50
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 50, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "Por volta de 1860, uma nova palavra entrou no vocabulário econômico e político do mundo: \"capitalismo\". O triunfo global do capitalismo é o tema mais importante da história nas décadas que sucederam 1848. Foi o triunfo de uma sociedade que acreditou que o crescimento repousava na competição da livre iniciativa privada, no sucesso de comprar tudo no mercado mais barato (inclusive trabalho) e vender no mais caro.\nEric J. Hobsbawm. A Era do Capital (1848-1875). Rio de Janeiro: Paz e Terra, 1982, p. 21 (com adaptações)\nTendo o texto acima como referência inicial e considerando o significado histórico da Revolução Industrial, julgue (C ou E) os itens a seguir.",
        "item_text": "A competição citada no texto, razão de ser de crescimento econômico que não teria fim, como se acreditava à época, circunscreveu-se à iniciativa privada. A triunfante sociedade burguesa, defensora intransigente dos princípios liberais, impediu que a ação dos Estados nacionais interferisse na economia, o que resultou em clima de paz e de rivalidades amortecidas, que perdurou até meados do século XX.",
        "alternatives": null, "answer": null, "page": 7, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 50, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "Por volta de 1860, uma nova palavra entrou no vocabulário econômico e político do mundo: \"capitalismo\". O triunfo global do capitalismo é o tema mais importante da história nas décadas que sucederam 1848. Foi o triunfo de uma sociedade que acreditou que o crescimento repousava na competição da livre iniciativa privada, no sucesso de comprar tudo no mercado mais barato (inclusive trabalho) e vender no mais caro.\nEric J. Hobsbawm. A Era do Capital (1848-1875). Rio de Janeiro: Paz e Terra, 1982, p. 21 (com adaptações)\nTendo o texto acima como referência inicial e considerando o significado histórico da Revolução Industrial, julgue (C ou E) os itens a seguir.",
        "item_text": "Entre os diversos elementos que se conjugam para a conceituação mais abrangente da Revolução Industrial, destacam-se a substituição das ferramentas pelas máquinas, da energia humana pela motriz e da forma doméstica de produção pelo sistema fabril.",
        "alternatives": null, "answer": null, "page": 7, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 50, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "Por volta de 1860, uma nova palavra entrou no vocabulário econômico e político do mundo: \"capitalismo\". O triunfo global do capitalismo é o tema mais importante da história nas décadas que sucederam 1848. Foi o triunfo de uma sociedade que acreditou que o crescimento repousava na competição da livre iniciativa privada, no sucesso de comprar tudo no mercado mais barato (inclusive trabalho) e vender no mais caro.\nEric J. Hobsbawm. A Era do Capital (1848-1875). Rio de Janeiro: Paz e Terra, 1982, p. 21 (com adaptações)\nTendo o texto acima como referência inicial e considerando o significado histórico da Revolução Industrial, julgue (C ou E) os itens a seguir.",
        "item_text": "No período de tempo mencionado no texto, a partir de meados do século XIX, a Revolução Industrial deixa de ser um acontecimento essencialmente inglês e tende a se disseminar. Nesse processo de universalização da moderna indústria, assinalada pela expansão imperialista, verifica-se a consolidação do capitalismo como sistema econômico dominante.",
        "alternatives": null, "answer": null, "page": 7, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 50, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "Por volta de 1860, uma nova palavra entrou no vocabulário econômico e político do mundo: \"capitalismo\". O triunfo global do capitalismo é o tema mais importante da história nas décadas que sucederam 1848. Foi o triunfo de uma sociedade que acreditou que o crescimento repousava na competição da livre iniciativa privada, no sucesso de comprar tudo no mercado mais barato (inclusive trabalho) e vender no mais caro.\nEric J. Hobsbawm. A Era do Capital (1848-1875). Rio de Janeiro: Paz e Terra, 1982, p. 21 (com adaptações)\nTendo o texto acima como referência inicial e considerando o significado histórico da Revolução Industrial, julgue (C ou E) os itens a seguir.",
        "item_text": "Assentada na notável evolução tecnológica que a caracterizou, a Revolução Industrial alterou radicalmente o sistema produtivo, ampliando, de maneira inédita, o volume da produção e os mercados consumidores. Essa transformação, contudo, foi insuficiente para determinar novos padrões de pensamento e de comportamento da sociedade, que ainda permanecia presa a ideias e valores do passado rural.",
        "alternatives": null, "answer": null, "page": 7, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 51
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 51, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "O colapso econômico de 1929 foi único em termos de profundidade e amplitude. Já houvera crises cíclicas antes, mas nunca como essa. A economia dos países industrializados permaneceu desintegrada por mais de cinco anos, com redução de um quinto na produção e desemprego que atingiu um quarto da força de trabalho. Crises financeiras e cambiais se reproduziram no mundo todo em um intervalo de semanas, fazendo que economias inteiras afundassem juntas. Nenhuma das principais nações foi poupada.\nJeffry A. Frieden. Capitalismo global: história económica e política do século XX. Rio de Janeiro: Jorge Zahar Ed., 2008, p. 191 (com adaptações)\nTendo o texto acima como referência inicial e considerando as múltiplas implicações do tema nele abordado, além do contexto histórico que lhe serve de moldura, julgue (C ou E) os itens seguintes.",
        "item_text": "A Grande Depressão dos anos 30 do século XX selou o fracasso da ordem econômica clássica, que não trouxera paz nem cooperação; ao contrário, provavelmente tenha acirrado os conflitos entre as nações. Entende-se a relação entre a crise de 1930 e a Segunda Guerra Mundial ao considerar que a recuperação econômica dos países, sobretudo os da Europa, assentou-se, em larga medida, na corrida armamentista, como foi o caso da Alemanha nazista.",
        "alternatives": null, "answer": null, "page": 7, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 51, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "O colapso econômico de 1929 foi único em termos de profundidade e amplitude. Já houvera crises cíclicas antes, mas nunca como essa. A economia dos países industrializados permaneceu desintegrada por mais de cinco anos, com redução de um quinto na produção e desemprego que atingiu um quarto da força de trabalho. Crises financeiras e cambiais se reproduziram no mundo todo em um intervalo de semanas, fazendo que economias inteiras afundassem juntas. Nenhuma das principais nações foi poupada.\nJeffry A. Frieden. Capitalismo global: história económica e política do século XX. Rio de Janeiro: Jorge Zahar Ed., 2008, p. 191 (com adaptações)\nTendo o texto acima como referência inicial e considerando as múltiplas implicações do tema nele abordado, além do contexto histórico que lhe serve de moldura, julgue (C ou E) os itens seguintes.",
        "item_text": "Com a quebra da Bolsa de Valores de Nova Iorque em outubro de 1929, iniciou-se a maior crise que o moderno capitalismo conhecera até então. Embora rapidamente disseminada, devido à vigorosa presença dos EUA no cenário econômico mundial pós-Primeira Guerra, a crise passou ao largo de países com pouca ou nenhuma industrialização, como os de grande parte da Ásia e os da América Latina.",
        "alternatives": null, "answer": null, "page": 7, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 51, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "O colapso econômico de 1929 foi único em termos de profundidade e amplitude. Já houvera crises cíclicas antes, mas nunca como essa. A economia dos países industrializados permaneceu desintegrada por mais de cinco anos, com redução de um quinto na produção e desemprego que atingiu um quarto da força de trabalho. Crises financeiras e cambiais se reproduziram no mundo todo em um intervalo de semanas, fazendo que economias inteiras afundassem juntas. Nenhuma das principais nações foi poupada.\nJeffry A. Frieden. Capitalismo global: história económica e política do século XX. Rio de Janeiro: Jorge Zahar Ed., 2008, p. 191 (com adaptações)\nTendo o texto acima como referência inicial e considerando as múltiplas implicações do tema nele abordado, além do contexto histórico que lhe serve de moldura, julgue (C ou E) os itens seguintes.",
        "item_text": "Em 1933, no auge da crise, Roosevelt e Hitler chegaram ao poder, e seus governos notabilizaram-se por oferecer respostas contundentes ao caos social e político em que se encontravam EUA e Alemanha. Com o New Deal, de Roosevelt, ainda que preservada a democracia, amplia-se a presença do Estado na economia, em contraste com as práticas econômicas ultraliberais que haviam levado ao colapso do sistema.",
        "alternatives": null, "answer": null, "page": 7, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 51, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "O colapso econômico de 1929 foi único em termos de profundidade e amplitude. Já houvera crises cíclicas antes, mas nunca como essa. A economia dos países industrializados permaneceu desintegrada por mais de cinco anos, com redução de um quinto na produção e desemprego que atingiu um quarto da força de trabalho. Crises financeiras e cambiais se reproduziram no mundo todo em um intervalo de semanas, fazendo que economias inteiras afundassem juntas. Nenhuma das principais nações foi poupada.\nJeffry A. Frieden. Capitalismo global: história económica e política do século XX. Rio de Janeiro: Jorge Zahar Ed., 2008, p. 191 (com adaptações)\nTendo o texto acima como referência inicial e considerando as múltiplas implicações do tema nele abordado, além do contexto histórico que lhe serve de moldura, julgue (C ou E) os itens seguintes.",
        "item_text": "O New Deal promoveu uma radical transformação na organização e no funcionamento do capitalismo nos EUA: os setores financeiro e industrial passaram a ser fiscalizados vigorosamente pelo governo federal, que optou por não se envolver na recuperação de áreas mais debilitadas, como a agricultura e a organização do trabalho.",
        "alternatives": null, "answer": null, "page": 7, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 52
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "História Mundial", "question_number": 52, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "No que concerne à unificação da Itália e suas consequências, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "A questão romana e do pontificado somente seria resolvida em 1929, no Tratado de Locarno, em que se estabeleceu a criação do Estado do Vaticano."},
            {"letter": "B", "text": "O Romantismo literário, o republicanismo revolucionário e o historicismo que enfatizava a singularidade nacional inspiraram o processo de unificação da Itália."},
            {"letter": "C", "text": "O processo de unificação da Itália iniciou-se nos Condados de Nice e de Savoia, que comandavam a guerra contra a Áustria e conseguiram amalgamar os movimentos secessionistas que começaram a eclodir em 1859."},
            {"letter": "D", "text": "A deposição de Napoleão III na França liquidou as garantias de que gozava o Papa, que assistiu à invasão dos Estados Pontificais pelas forças unionistas e à conversão de Roma em capital da Itália unificada."},
            {"letter": "E", "text": "A unificação italiana teve consequências diretas no equilíbrio da política europeia, em especial, na intensificação da política denominada isolamento esplêndido (splendid isolation), implementada pela Inglaterra."}
        ],
        "answer": null, "page": 8, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 53
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Política Internacional", "question_number": 53, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Assinale a opção correta a respeito da integração econômica nas Américas.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "Programa formado pelos doze países da América do Sul, a Iniciativa para a Integração da Infraestrutura Regional Sul-Americana (IIRSA) tem como objetivo buscar condições para o incremento da integração física dessa região."},
            {"letter": "B", "text": "Primeiro mecanismo de integração econômica formalizado na América do Sul, o Pacto de Não Agressão, Consulta e Arbitragem, firmado entre Argentina, Brasil e o Chile em 1915, foi motivado pela pretensão dos governos desses três países de buscarem formas de compensação para a crescente influência econômica dos EUA na região."},
            {"letter": "C", "text": "Incentivada pelos EUA, que visavam à contenção da influência de Cuba, a criação, em 1971, da Caricom (Comunidade do Caribe) teve motivações exclusivamente relacionadas à concertação política de alto nível e à estabilidade da região."},
            {"letter": "D", "text": "Criada em 1960, a Associação Latino-Americana de Livre-Comércio (ALALC) inscreve-se nos esforços de disseminação do crescimento econômico por meio de instrumentos liberais preconizados pelos EUA na Aliança para o Progresso."},
            {"letter": "E", "text": "Firmada pelos presidentes José Sarney e Raúl Alfonsín, em 1985, a Declaração de Iguaçu constituiu o Mercado Comum do Sul, ao qual aderiram, pelo Tratado de Assunção, de 1991, o Uruguai e o Paraguai."}
        ],
        "answer": null, "page": 8, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 54
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Política Internacional", "question_number": 54, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Acerca da coexistência pacífica que caracterizou as relações entre as superpotências na segunda metade dos anos 50 do século passado e em parte da década de 60, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "A morte de Joseph Stalin, em 1953, e a ascensão de Kruschev ao ápice do poder favoreceram o tratamento mais flexível das relações entre a União Soviética e os EUA."},
            {"letter": "B", "text": "A reconstrução da Europa Ocidental nos anos 50 resultou de um processo marginal das dinâmicas de estabelecimento da coexistência pacífica entre as superpotências mundiais."},
            {"letter": "C", "text": "A permanência do purismo ideológico ao longo da segunda metade da década de 50 nos EUA retardou o surgimento do padrão da coexistência pacífica entre as superpotências mundiais."},
            {"letter": "D", "text": "O início da desintegração do bloco comunista, com a descaracterização da unidade na Europa Oriental, na década de 50 e o conflito sino-soviético do início dos anos 60 são resultados indiretos da coexistência pacífica entre as superpotências mundiais."},
            {"letter": "E", "text": "O estancamento do processo de descolonização nos anos 60, com o congelamento do status quo colonial, postergou o enfrentamento das superpotências na Ásia e na África e favoreceu o entendimento entre Moscou e Washington."}
        ],
        "answer": null, "page": 8, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 55
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Política Internacional", "question_number": 55, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "A Guerra Fria constitui um dos fenômenos mais importantes da História Contemporânea. Acerca de sua fase inicial, julgue (C ou E) os itens a seguir.",
        "item_text": "O bloqueio de Berlim e a imediata construção do muro que dividiu a cidade em duas zonas, em 1948, constituem a resposta da União Soviética à política de contenção estabelecida pelos EUA.",
        "alternatives": null, "answer": null, "page": 8, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Política Internacional", "question_number": 55, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "A Guerra Fria constitui um dos fenômenos mais importantes da História Contemporânea. Acerca de sua fase inicial, julgue (C ou E) os itens a seguir.",
        "item_text": "Com o fim da Segunda Guerra Mundial, a política externa dos EUA passou a sustentar-se na ideia de ação de longo prazo vinculada à necessidade de contenção das tendências expansionistas da União Soviética.",
        "alternatives": null, "answer": null, "page": 8, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Política Internacional", "question_number": 55, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "A Guerra Fria constitui um dos fenômenos mais importantes da História Contemporânea. Acerca de sua fase inicial, julgue (C ou E) os itens a seguir.",
        "item_text": "Considerada uma atualização da Doutrina Monroe, a Doutrina Truman foi a primeira formulação política com caráter universal a esboçar-se na política externa norte-americana.",
        "alternatives": null, "answer": null, "page": 8, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Política Internacional", "question_number": 55, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "A Guerra Fria constitui um dos fenômenos mais importantes da História Contemporânea. Acerca de sua fase inicial, julgue (C ou E) os itens a seguir.",
        "item_text": "O Plano Marshall foi peça fundamental da estratégia norte-americana na Guerra Fria, configurando-se como tradução econômica da Doutrina Truman.",
        "alternatives": null, "answer": null, "page": 8, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 56
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Direito e Direito Internacional", "question_number": 56, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "No que concerne a controle de constitucionalidade, organização do Estado e dos poderes e processo legislativo no Brasil, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "Como forma de prestigiar a autoridade e a prevalência de seu texto, a Constituição dispõe que matéria constante de uma proposta de emenda constitucional rejeitada constitua objeto de nova proposta na mesma sessão legislativa somente se for reapresentada pela maioria absoluta dos membros de qualquer das Casas do Congresso Nacional."},
            {"letter": "B", "text": "O Supremo Tribunal Federal exerce o controle concentrado de constitucionalidade das leis e dos atos normativos federais e estaduais na via de ação, mas não o controle difuso, realizado por juízes e tribunais no caso concreto."},
            {"letter": "C", "text": "A federação como forma de Estado e a república como forma de governo são expressamente consideradas cláusulas pétreas da Constituição, as quais, portanto, não podem ser abolidas nem por proposta de emenda constitucional."},
            {"letter": "D", "text": "Por abranger toda a ordem jurídica do Estado Federal brasileiro, a União é pessoa jurídica de direito público internacional que se confunde com a República Federativa do Brasil."},
            {"letter": "E", "text": "Compete exclusivamente ao Congresso Nacional resolver definitivamente sobre tratados, acordos ou atos internacionais; entretanto, a competência para autorizar operações externas de natureza financeira de interesse da União, dos estados, do Distrito Federal, dos territórios e dos municípios pertence, em caráter privativo, ao Senado Federal."}
        ],
        "answer": null, "page": 9, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 57
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Direito e Direito Internacional", "question_number": 57, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Considerando a classificação das constituições, os princípios e direitos fundamentais e a responsabilidade civil do Estado, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "É objetiva a responsabilidade civil das pessoas jurídicas de direito público, as quais respondem pelos danos causados por seus agentes, independentemente de dolo ou culpa, regra que não se aplica às pessoas jurídicas de direito privado prestadoras de serviços públicos, as quais estão sujeitas à responsabilidade subjetiva comum do direito civil."},
            {"letter": "B", "text": "A Constituição de 1988 é classificada, quanto à origem, como promulgada; quanto à extensão, como analítica; quanto à estabilidade, como semirrígida e, quanto ao modo de elaboração, como histórica."},
            {"letter": "C", "text": "Pelo princípio da moralidade, os atos da administração pública devem ser praticados em consonância com a moral e o senso de honestidade. Em que pesem a importância e o alcance desse princípio, a moralidade administrativa não pode ser objeto de controle jurisdicional, pois este é um controle de legalidade em que se examina apenas a conformação do ato com a lei."},
            {"letter": "D", "text": "O catálogo de direitos e garantias fundamentais previstos na Constituição Federal não é exaustivo, pois inclui outros direitos, de envergadura constitucional, decorrentes do regime e dos princípios por ela adotados, ou dos tratados internacionais em que a República Federativa do Brasil seja parte."},
            {"letter": "E", "text": "Os brasileiros, natos e naturalizados, e os estrangeiros residentes no país são igualmente destinatários dos direitos e garantias fundamentais. Apenas os estrangeiros não residentes que estejam em trânsito pelo território nacional não dispõem de meios jurisdicionais para assegurar a validade e o gozo desses direitos."}
        ],
        "answer": null, "page": 9, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 58
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Direito e Direito Internacional", "question_number": 58, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Acerca de atuação de tribunais internacionais e de suas instâncias destinadas à solução de controvérsias, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "O Brasil se submete à atuação contenciosa do Tribunal Permanente de Revisão do MERCOSUL (TPR), embora não se submeta à sua atuação consultiva, ainda não regulamentada pelo Supremo Tribunal Federal."},
            {"letter": "B", "text": "Tanto Estados como organizações internacionais, incontestáveis sujeitos de direito internacional, estão habilitados a comparecer como autores ou como réus perante a Corte Internacional de Justiça."},
            {"letter": "C", "text": "No que se refere à Corte Internacional de Justiça, a manifestação facultativa de jurisdição obrigatória, que leva o nome de cláusula Raul Fernandez, em homenagem ao brasileiro que a concebeu, conforma prática internacional reiterada e uniforme, de natureza consuetudinária."},
            {"letter": "D", "text": "O Tribunal de Justiça das Comunidades Europeias é a única instância aplicadora do direito comunitário europeu."},
            {"letter": "E", "text": "As decisões formuladas no sistema de solução de controvérsias da Organização Mundial do Comércio sujeitam-se ao duplo grau de julgamento, sendo prevista uma segunda instância revisora."}
        ],
        "answer": null, "page": 9, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 59
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Direito e Direito Internacional", "question_number": 59, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "Julgue (C ou E) os itens seguintes, a respeito da forma, do alcance e da abrangência das decisões tomadas pela Organização das Nações Unidas (ONU) e de sua instância jurídica, a Corte Internacional de Justiça.",
        "item_text": "Ao tornar-se signatário da Carta de São Francisco, o Estado coobriga-se, também, à jurisdição da Corte Internacional de Justiça.",
        "alternatives": null, "answer": null, "page": 9, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Direito e Direito Internacional", "question_number": 59, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "Julgue (C ou E) os itens seguintes, a respeito da forma, do alcance e da abrangência das decisões tomadas pela Organização das Nações Unidas (ONU) e de sua instância jurídica, a Corte Internacional de Justiça.",
        "item_text": "As decisões da Assembleia Geral da ONU devem, obrigatoriamente, ser acatadas por todos os membros da comunidade internacional.",
        "alternatives": null, "answer": null, "page": 9, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Direito e Direito Internacional", "question_number": 59, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "Julgue (C ou E) os itens seguintes, a respeito da forma, do alcance e da abrangência das decisões tomadas pela Organização das Nações Unidas (ONU) e de sua instância jurídica, a Corte Internacional de Justiça.",
        "item_text": "Conforme a Carta da ONU, respaldada pela jurisprudência internacional, as resoluções do Conselho de Segurança acerca de questões destinadas à manutenção da paz e ao seu restabelecimento são de caráter vinculante.",
        "alternatives": null, "answer": null, "page": 9, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Direito e Direito Internacional", "question_number": 59, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "Julgue (C ou E) os itens seguintes, a respeito da forma, do alcance e da abrangência das decisões tomadas pela Organização das Nações Unidas (ONU) e de sua instância jurídica, a Corte Internacional de Justiça.",
        "item_text": "À Corte Internacional de Justiça faculta-se julgar casos que lhe sejam submetidos também por equidade, se as partes com isto concordarem.",
        "alternatives": null, "answer": null, "page": 9, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 60
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Direito e Direito Internacional", "question_number": 60, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "É agência especializada da ONU",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "o Comitê Internacional da Cruz Vermelha."},
            {"letter": "B", "text": "a Organização Mundial do Comércio."},
            {"letter": "C", "text": "o Tribunal Penal Internacional."},
            {"letter": "D", "text": "a Organização para a Cooperação e Desenvolvimento Econômico."},
            {"letter": "E", "text": "a Organização Internacional do Trabalho."}
        ],
        "answer": null, "page": 9, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 61
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 61, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Com relação ao conceito de meios de pagamento (M1), que corresponde ao estoque de moeda disponível para uso da coletividade, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "O valor do multiplicador da base monetária varia na razão inversa da taxa de reservas dos bancos comerciais e na razão direta da taxa de retenção da moeda pelo público."},
            {"letter": "B", "text": "O saldo de M1 é composto pelo saldo da moeda em poder do público somado ao saldo dos depósitos à vista e aos depósitos de poupança."},
            {"letter": "C", "text": "Em processos inflacionários, tende a diminuir a razão entre o volume de moeda em poder do público e o volume de moeda bancária."},
            {"letter": "D", "text": "O resgate de um empréstimo bancário representa destruição de moeda."},
            {"letter": "E", "text": "As emissões de papel moeda pelo Tesouro Nacional são instrumento de política monetária à disposição do Ministério da Fazenda."}
        ],
        "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 62
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 62, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "O objetivo da contabilidade nacional é analisar a evolução dos indicadores da economia de um país como um todo. A esse respeito, assinale a opção correta.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "O conceito de formação bruta de capital fixo inclui não apenas os investimentos em máquinas e equipamentos, mas também os investimentos em imóveis e a variação dos estoques tanto de produtos acabados quanto intermediários."},
            {"letter": "B", "text": "A acumulação de capital é sempre positiva, pois a depreciação de um ativo fixo não pode ser maior que o valor do próprio ativo fixo."},
            {"letter": "C", "text": "O índice da carga tributária corresponde ao total da arrecadação fiscal do Ministério da Fazenda em relação à renda nacional bruta."},
            {"letter": "D", "text": "O produto nacional bruto é obtido pelo somatório do produto interno bruto com a renda recebida do exterior, descontadas as importações."},
            {"letter": "E", "text": "No cálculo da poupança externa, não se incluem aumentos ou diminuições das reservas cambiais do país."}
        ],
        "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 63
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 63, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "Acerca das teorias de comércio internacional e do sistema multilateral de comércio, julgue (C ou E) os itens a seguir.",
        "item_text": "As teorias clássicas do comércio internacional baseiam-se na produtividade relativa da mão de obra, e a teoria neoclássica do comércio internacional, na diferença relativa de dotação dos fatores de produção.",
        "alternatives": null, "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 63, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "Acerca das teorias de comércio internacional e do sistema multilateral de comércio, julgue (C ou E) os itens a seguir.",
        "item_text": "A salvaguarda, e não uma medida antidumping, é aplicada contra as importações originárias de todos os países envolvidos na transação.",
        "alternatives": null, "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 63, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "Acerca das teorias de comércio internacional e do sistema multilateral de comércio, julgue (C ou E) os itens a seguir.",
        "item_text": "Não existem regras multilaterais aplicáveis a investimentos.",
        "alternatives": null, "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 63, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "Acerca das teorias de comércio internacional e do sistema multilateral de comércio, julgue (C ou E) os itens a seguir.",
        "item_text": "Acordos comerciais regionais são incompatíveis com as normas multilaterais, a menos que a liberalização neles prevista abranja a totalidade do universo tarifário.",
        "alternatives": null, "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 64
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 64, "item_number": null,
        "question_type": "multipla_escolha",
        "question_text": "Assinale a opção correta no que diz respeito à análise da economia brasileira na década posterior ao fim da Segunda Guerra Mundial.",
        "item_text": null,
        "alternatives": [
            {"letter": "A", "text": "A crise cambial de 1952 resultou, entre outros fatores, da defasagem entre a concessão de licenças e a efetivação das importações, da queda das exportações de algodão decorrente da crise da indústria têxtil mundial e da quebra da safra de trigo nos EUA, que obrigou o governo brasileiro a importar da Argentina esse cereal, em condições menos favoráveis."},
            {"letter": "B", "text": "Conforme apontado por Carlos Lessa na obra clássica Quinze anos de Política Econômica, a industrialização \"não intencional\", que corresponde à política fiscal expansionista adotada no final dos anos 40, mesmo na ausência de medidas de planejamento, teria fortalecido setores da indústria brasileira."},
            {"letter": "C", "text": "A Instrução 70, adotada, em 1953, pela Superintendência da Moeda e do Crédito, órgão antecessor do Banco Central do Brasil, estabeleceu taxas múltiplas de câmbio, atribuindo taxas mais depreciadas à importação de máquinas, equipamentos e matérias-primas essenciais."},
            {"letter": "D", "text": "O período em que a taxa de câmbio oficial manteve-se fixa (CR$ 18,50 por dólar) representou, na prática, vigorosa apreciação da taxa de câmbio nominal."},
            {"letter": "E", "text": "A adoção da Instrução 113 da Superintendência da Moeda e do Crédito, que permitia a importação de bens de capital sem necessidade de cobertura cambial, não representou ruptura do tratamento vigente do capital estrangeiro. O governo Vargas, apesar da retórica nacionalista, já vinha adotando políticas que estimulavam a mobilização de recursos de origem externa e orientando inversões em setores prioritários."}
        ],
        "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    # QUESTÃO 65
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 65, "item_number": 1,
        "question_type": "certo_errado",
        "question_text": "Supondo que o governo adote um novo imposto específico sobre a venda de um bem em um mercado de concorrência perfeita e considerando a distribuição da incidência tributária entre vendedores e consumidores, julgue (C ou E) os itens a seguir.",
        "item_text": "Se a elasticidade-preço da demanda for infinita, os vendedores abandonarão o mercado.",
        "alternatives": null, "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 65, "item_number": 2,
        "question_type": "certo_errado",
        "question_text": "Supondo que o governo adote um novo imposto específico sobre a venda de um bem em um mercado de concorrência perfeita e considerando a distribuição da incidência tributária entre vendedores e consumidores, julgue (C ou E) os itens a seguir.",
        "item_text": "Vendedores e consumidores arcarão com o peso do imposto, conforme a sensibilidade das curvas de oferta e demanda às variações de preço.",
        "alternatives": null, "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 65, "item_number": 3,
        "question_type": "certo_errado",
        "question_text": "Supondo que o governo adote um novo imposto específico sobre a venda de um bem em um mercado de concorrência perfeita e considerando a distribuição da incidência tributária entre vendedores e consumidores, julgue (C ou E) os itens a seguir.",
        "item_text": "Vendedores irão transferir aos compradores o valor relativo a toda incidência do novo imposto, o que aumentará o preço do bem.",
        "alternatives": null, "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    },
    {
        "contest_id": contest_id, "year": year, "phase": phase, "stage": stage,
        "discipline": "Economia", "question_number": 65, "item_number": 4,
        "question_type": "certo_errado",
        "question_text": "Supondo que o governo adote um novo imposto específico sobre a venda de um bem em um mercado de concorrência perfeita e considerando a distribuição da incidência tributária entre vendedores e consumidores, julgue (C ou E) os itens a seguir.",
        "item_text": "Quanto menor for a elasticidade-preço da demanda, maior será a incidência do tributo para os consumidores.",
        "alternatives": null, "answer": null, "page": 10, "caderno": caderno, "source_file": source_file, "source_url": null, "confidence": 1.0, "notes": null
    }
]

# Escrevendo no arquivo JSON Lines
output_file = "questoes_cacd_2013_etapa2.jsonl"
with open(output_file, "w", encoding="utf-8") as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")