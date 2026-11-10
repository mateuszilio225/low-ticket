# Auditoria das referências — antes dos criativos 3, 4 e 5

Auditoria executada em 10 de novembro de 2026, por leitura dos arquivos locais, FFprobe, decodificação integral com FFmpeg, leitura dos scripts de origem e inspeção visual efetiva de quadros. Não há dados de campanha ou de vendas disponíveis nesta auditoria.

## Arquivos efetivamente disponíveis

| Referência pedida | Arquivo encontrado e analisado | Situação |
| --- | --- | --- |
| Momentos_Anuncio_Optimizado_15s_9x16.mp4 | `marketing/video-otimizado/finais/Momentos_Anuncio_Optimizado_15s_9x16.mp4` | Nome exato encontrado |
| Momentos_Anuncio_15s_9x16(2).mp4 | `marketing/video-15s/finais/Momentos_Anuncio_15s_9x16.mp4` | Cópia com sufixo literal `(2)` não encontrada; analisado o original canônico da entrega anterior |
| Momentos_para_Compartir_COMPLETO(1).pdf | `revision/finais/Momentos_para_Compartir_COMPLETO.pdf` | Cópia com sufixo literal `(1)` não encontrada; analisado o PDF canônico revisado da entrega anterior |

A busca cobriu o projeto e `/workspace/attachments`. Não se afirma que uma cópia de download com nome diferente foi analisada. Os arquivos canônicos correspondem às entregas que originaram essas referências; se os arquivos com sufixo tiverem sido editados fora do projeto, essas alterações externas não estão incluídas nesta análise.

Hashes SHA-256 dos arquivos analisados:

- Original: `9c7b8df5da1e03991219d4f8e4003ed2c824bb877fc3f365e76a1d2a0d6ea02e` — 2.572.285 bytes.
- Otimizado: `17ae9fcd150749231b8d6ad61f8dc5dfafd54a1ee2173d6da2959660da167e78` — 2.479.123 bytes.
- PDF revisado: `c561be54badb020f09257502d99462d2de76db2e81717c70301116a051a47426` — 5.637.183 bytes.

## Validação técnica comum

Ambos os vídeos têm 15,000 segundos, 450 quadros, 1080 × 1920, 30 FPS, H.264 e AAC estéreo a 48 kHz. As faixas de vídeo e áudio foram decodificadas integralmente, sem erro do FFmpeg. Isso demonstra integridade técnica, não eficácia publicitária.

Medição atual do áudio, feita com o filtro loudnorm em modo de análise:

| Arquivo | Loudness integrado de entrada | Pico verdadeiro de entrada |
| --- | ---: | ---: |
| Original | −16,26 LUFS | −1,36 dBTP |
| Otimizado | −16,75 LUFS | −1,48 dBTP |

A trilha é discreta e a locução sintética espanhola domina a mixagem, conforme fontes e amplitude. Não houve nesta auditoria teste de audição em altifalante de telemóvel, estudo com ouvintes nem validação de sotaque por um locutor humano. Os textos falados e seus tempos foram conferidos nos manifests e SRT produzidos com os arquivos.

## Criativo original — estrutura real

| Intervalo | O que aparece | Avaliação |
| --- | --- | --- |
| 0–3 s | Fotografia de avó e filha; pergunta «¿Buscas ejercicios prácticos para estimular la memoria de tus mayores?» | Situação acolhedora, mas o arquivo vendido ainda não é mostrado em detalhe. O movimento é zoom discreto da fotografia; a pergunta permanece fixa. |
| 3–5 s | C1-01, lista de memória, recorte da página | Prova real e identificada; tamanho total da folha limita o tamanho do enunciado no telemóvel. |
| 5–7 s | C3-31, ordenar uma frase, moldura de tablet | Mostra alternativa digital; muda de tarefa antes de demonstrar uso. |
| 7–9 s | C7-28, procurar posição numa grade | Estímulo concreto, mas não há resolução nesta versão. |
| 9–11 s | C8-27, preparação de desenho | Acrescenta variedade, mas é a quarta folha em oito segundos. |
| 11–15 s | Fotografia, capa pequena, «¡Descarga inmediata en PDF!», «Un solo pago», CTA Comprar ahora e condição de pagamento | É o primeiro momento em que capa, formato PDF e condição comercial ficam reunidos explicitamente. Não apresenta preço. |

### Texto, legibilidade e transições

O título da abertura usa aproximadamente 61 px no vídeo de 1080 px de largura. Outros slogans ficam em torno de 43–70 px; o rótulo de marca em 28 px e as notas em aproximadamente 27–30 px. Nas fichas, texto de PDF de 17 pt é reduzido ao tamanho de um cartão de 812 px; corresponde a cerca de 27 px no vídeo, ou apenas 9 px quando exibido com 360 px de largura. Portanto, o slogan é legível com maior facilidade que as instruções da página. Esses valores são estimados pelo pipeline original; não são uma certificação de acessibilidade.

As cenas seguem cortes diretos nos tempos acima, acompanhados de zoom de cerca de 2,5%. Não há passagem progressiva entre as quatro páginas. A maior parte da ação visual continua parecida com uma sequência de cartões, mesmo existindo movimento discreto. O espaço inferior conserva margem para a interface do Reels, mas a área útil das fichas poderia ser maior mediante recorte seletivo, evitando exibir tantas linhas vazias.

### Diagnóstico revisado

Confirma-se a apresentação informativa e o ritmo de quatro folhas rápidas. A demonstração não permite ver alguém escolher ou responder à tarefa. A hipótese de atrair curiosidade informacional em vez de intenção de compra é plausível, porém não foi demonstrada por métricas. O formato PDF só se torna explícito na CTA, embora a impressão e o uso digital sejam mencionados antes. Não é adequado afirmar que o anúncio gera cliques ruins sem dados de checkout ou compra.

## Criativo otimizado — estrutura real

| Intervalo | O que aparece | Avaliação |
| --- | --- | --- |
| 0–3 s | C7-28 com mão e caneta animadas; «¿Te preocupa que pase el día a solas?» | A ficha real aparece desde o início. O gancho emocional aborda isolamento, antes de explicar o formato vendido. |
| 3–6,4 s | A caneta circula CAFÉ e escreve «Fila 3, columna 3.» | A resposta corresponde ao estímulo. Há demonstração concreta mais longa que no original. |
| 6,4–8 s | Calendário de 90 dias | Identificação do bônus é clara; o conteúdo diário fica pequeno e tem somente 1,6 s de exposição. |
| 8–9,6 s | Diploma personalizado com María e ampliação do nome | Personalização reconhecível; o corpo do certificado é pequeno. O exemplo é identificado como demonstração. |
| 9,6–11,5 s | Avó e filha sorrindo, mensagem de convivência | Retoma emoção, mas reutiliza a fotografia do primeiro anúncio. |
| 11,5–15 s | Capa, pacote completo, pagamento único, CTA e condição de acesso | Formato PDF aparece explicitamente aqui; oferta continua sem preço. |

### Texto, movimento e legibilidade

Abertura em aproximadamente 65 px, títulos de bônus em 71–73 px e notas de 27–35 px. Esses títulos são legíveis em redução mobile; o calendário usa página de 515 unidades reduzida para 760 px, trazendo texto de 15 pt para cerca de 22 px no vídeo, aproximadamente 7 px numa visualização de 360 px. A parte de conteúdo do diploma é ainda menor; a ampliação do nome resolve o reconhecimento do campo personalizado, não a leitura de todo o certificado.

A mão muda de posição realmente entre quadros; não é apenas um zoom. A resolução CAFÉ/fila 3/coluna 3 é correta. A mão é um recorte de imagem gerada por IA, não filmagem de uma pessoa, e desaparece por fade depois do preenchimento. Não é recomendável repetir esse efeito de desaparecimento nos novos vídeos: marcações gráficas simples ou um movimento de saída motivado preservam clareza sem sugerir uma ação física impossível.

A capa e a noção de arquivo PDF/kit digital continuam surgindo tarde. A expressão «320 actividades» aparece aos 3 s; «Paquete completo» e «PDF» ficam explícitos aos 11,5 s. Para cliques mais qualificados, os novos podem deixar a natureza de material digital clara antes do final, sem sobrecarregar as legendas.

### Diagnóstico revisado

Confirma-se a melhora de tangibilidade por mostrar uma resposta correta. Também se confirma o risco de o gancho ser lido apenas como mensagem de convivência/solidão, porque não apresenta imediatamente a oferta digital. A demonstração está mais clara que no original, mas bônus pequenos e rápidos ainda limitam leitura. O uso repetido de CAFÉ e da mesma fotografia aproxima visualmente os dois anúncios. O anúncio não contém depoimentos ou compradores fictícios; tampouco há evidência de desempenho superior real.

## CTA e clareza comercial — ambos

Os dois vídeos desenham a CTA como um botão, embora o elemento dentro do MP4 não seja clicável. Para os novos, respeitar a solicitação de CTA tipográfica ou faixa editorial sem simular controle funcional. A frase sobre acesso após confirmação de pagamento é adequada, mas não substitui a verificação da oferta atual. Nenhum dos vídeos anteriores contém o preço vigente ou prova de correspondência com o checkout atual da Espanha; não usar esse material como confirmação de 9,90 € ou 10,30 €.

## PDF e novas páginas adequadas

O PDF foi aberto e o texto de todas as 404 páginas foi extraído. Foram identificadas 320 folhas de atividade por código e nível, com 320 códigos únicos. Foram renderizadas e inspecionadas a capa e quatro folhas novas. Não se refez nesta missão a revisão clínica ou editorial integral de todos os 320 enunciados; há um relatório anterior de revisão no projeto.

| Código | Página do PDF completo | Proposta real e solução/critério | Possível uso |
| --- | ---: | --- | --- |
| C2-01 | 49 | «Busque la letra A»: A M A S O A L A P R; quatro As nas posições 1, 3, 6 e 8 | Demonstração de atenção, sem reutilizar CAFÉ |
| C1-31 | 38 | «Una comida querida»: nomear uma comida e com quem gostaria de partilhá-la; resposta pessoal, sem correção de lembranças | Conversa em família |
| C3-01 | 90 | «Palabras de frutas»: três exemplos; manzana, pera e uva são válidos | Variedade e uso oral/escrito |
| C5-02 | 173 | «La serie avanza 2»: 2, 5, 8, __, __; respostas 11 e 14, somando 3 | Prova de lógica e clareza da oferta |

Essas quatro atividades diferem de C1-01, C3-31, C7-28 e C8-27 já exibidas. Pode-se ampliar a área do estímulo sem inventar páginas novas: recortar o cabeçalho/consigna real e usar os campos de resposta existentes ou marcações demonstrativas identificadas.

## Recomendações para os três novos testes

- **C3 demonstração:** começar no estímulo real ampliado e manter uma resolução visual correta; reduzir a alternância de páginas sem uso. Apresentar o kit e o formato antes da CTA. Uma marcação gráfica de A em quatro posições é mais simples de compreender que uma mão flutuante.
- **C4 família:** usar uma conversa concreta de C1-31, preservando a resposta voluntária, em vez de repetir apenas rostos sorrindo. Evitar gancho de culpa ou vulnerabilidade. Conectar a escolha de uma folha à experiência de convivência.
- **C5 oferta:** organizar 8 cadernos e 320 atividades em uma visualização de produto; declarar PDF digital e materiais efetivamente incluídos. Validar o preço-base e o texto de impostos com a oferta vigente, sem herdar valores antigos da landing de demonstração.

Não há base nesta auditoria para prometer vendas ou qualificação superior dos cliques. As três abordagens são hipóteses. Observar compra/checkout e custo por compra, usando retenção e CTR apenas como diagnósticos secundários.

## Evidências e limites

Foram abertos os arquivos `qa_referencias/original-contato.jpg`, `otimizado-contato.jpg` e `pdf-amostras.jpg`, além dos manifestos e fontes originais. As folhas de contato contêm quadros reais em 0,2; 1,5; 2,8; 3,5; 5,8; 7,2; 8,8; 10,4; 12,6 e 14,5 segundos de cada vídeo. Os resultados de FFprobe, hashes e busca dos nomes estão em `inventario.json`; as medições de áudio em `medicoes_audio.json`.

Esta auditoria não testa compra, compatibilidade em um telefone físico nem reprodução audível no dispositivo do público. Não substitui a prévia do anúncio no Gerenciador de Anúncios ou o teste de campanha. A adequação de layouts novos precisa ser validada após sua própria renderização.
