# Inspeção visual efetiva dos três criativos

## Escopo executado

Foram abertos com `view_image` os três contatos atuais em `output/qa`, cada um com 15 quadros selecionados em 0,5, 1,5, …, 14,5 segundos. Isso corresponde a 45 amostras visuais atuais, não à inspeção visual manual de todos os 1.350 quadros. O runner automatizado decodificou integralmente os vídeos e verificou os metadados, quadro preto, limites de texto e áudio.

Também foram extraídos diretamente dos MP4 e abertos em resolução integral:

- `C3_3.5_detalhe.jpg`: demonstração das palavras LAGO/LADO.
- `C4_7.5_detalhe.jpg`: etapa «2. Conversad».
- `C4_13.5_detalhe.jpg`: capa e CTA.
- `C5_11.5_detalhe.jpg`: preço, impostos e indicação de consultar o total.

## Achados

### C3 — Demonstração

O vídeo começa pelo conteúdo real. As duas palavras são grandes e legíveis no contato em tamanho aproximado de visualização mobile; a identificação «Kit digital en PDF» aparece desde a abertura. LAGO/LADO, o resultado LAGO → LADO e o código C2-22 correspondem à atividade real de comparação. A marcação progressiva é visível entre as amostras de 2,5, 3,5 e 4,5 segundos. Não foi vista mão artificial a desaparecer ou um movimento físico impossível.

Os dois recortes seguintes e as capas documentam variedade e quantidade sem substituir a demonstração inicial. Os textos essenciais estão legíveis e em bom contraste. Os textos completos das folhas, quando aparecem pequenos, funcionam como prova do material; a compreensão da oferta é sustentada por títulos publicitários grandes.

**Correção executada e reinspecionada:** na primeira inspeção, «LAGO → LADO» cruzava a borda inferior da carta. O responsável moveu o resultado para baixo da carta. Reabri o quadro atual de 3,5 segundos e o contato atualizado: a palavra LADO e o resultado estão inteiros, separados da borda e da legenda de código. A aproximação discreta na abertura preserva a legibilidade.

### C4 — Família

A abertura é acolhedora e distinta dos rostos usados nos anúncios anteriores. A folha real aparece sobre a mesa, e «Kit digital en PDF» torna o produto explícito cedo. O trecho «Una comida querida» e a pergunta ampliada estão íntegros; a sequência de escolha, conversa e exemplo de resposta tem etapas visuais identificáveis. O calendário liga a escolha ao dia 08 e ao código C1-31; o destaque do código é visível no contato. O CTA final é texto com seta, sem botão funcional simulado.

**Correção executada e reinspecionada:** na primeira inspeção, a faixa «2. Conversad» deixava uma tira de fotografia aparecendo abaixo. A foto foi encurtada e centralizada. Reabri o quadro atual de 7,5 segundos e o contato atualizado: a imagem agora termina antes da legenda, sem a tira desconexa e sem cobrir rostos.

### C5 — Oferta

A capa, as oito aberturas reais e os exemplos de conteúdo diferenciam este vídeo de C3 e C4. O preço aparece grande e completo com a composição «Desde 9,90 €» e «+ impuestos aplicables». A linha «Consulta el total en el checkout» também é legível. Não foi observado «IVA incluido» nem a apresentação de 9,90 € como valor final garantido.

A clareza visual do preço foi verificada; a vigência comercial não foi confirmada por esta inspeção. O relatório `input/verificacao_oferta.md` registra o bloqueio do proxy às URLs comerciais, e `config/projeto.json` identifica o preço como informado pelo usuário, não como checkout verificado. É necessário manter essa distinção no relatório de entrega.

## Comparação entre os três

- C3 começa por um problema visual e sua demonstração concreta, com produto digital explícito desde o primeiro quadro.
- C4 começa pela convivência e usa uma atividade pessoal para organizar escolha, conversa e prática.
- C5 começa pela composição do pacote e avança para conteúdo, complementos e preço com impostos.

Não são cópias com títulos trocados: as aberturas, sequências centrais e a presença de preço são diferentes. Não se afirma que alguma variante converterá melhor antes de uma campanha controlada.

## Limites e estado desta inspeção

Não observei texto essencial cortado, glifos quebrados, preço sem ressalva de impostos ou regiões pretas indevidas nas amostras. O runner atual passou em duração, resolução, FPS, codec, contagem de quadros, decodificação integral, áudio e caixas de texto. Isso não é escuta humana, teste em um telemóvel físico, confirmação de oferta no checkout, certificação da Meta ou teste de conversão.

Os dois refinamentos foram aplicados e os MP4 C3/C4 foram renderizados novamente. Seus contatos atuais de 15 quadros e os dois detalhes ampliados foram reabertos para esta revisão final. O arquivo C5 permaneceu byte a byte igual ao inspecionado inicialmente, inclusive a tela ampliada de preço. O relatório automatizado atual aprovou novamente os três vídeos. Não foram observados outros problemas bloqueantes nas amostras finais.

### Hashes finais inspecionados

- MOMENTOS_C3_DEMONSTRACAO_15S.mp4: `03cb3c98179d72bb840d29e9f398bf21b2ebb0aab1be4b7b78e67997d04430b4`.
- MOMENTOS_C4_FAMILIA_15S.mp4: `c8890ed3c4710d9105eb1f06fabf44393d9de1ae3ad83170eada1311d610dfac`.
- MOMENTOS_C5_OFERTA_15S.mp4: `7ea1b75a5701936125e2bb1a5477cf59d674ea6e63f3329103a1c85652cb45c8`.
