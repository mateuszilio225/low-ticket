# Momentos para Compartir — C3, C4 e C5

Três anúncios independentes de **15 segundos**, em **1080 × 1920**, **30 FPS**, **H.264**, **yuv420p** e **AAC estéreo**. O projeto produz os três MP4 numa única execução e executa as verificações técnicas no final.

## Downloads e arquivos

Os mesmos arquivos MP4 são disponibilizados individualmente na raiz da branch `entrega-video` do repositório `mateuszilio225/low-ticket` e nesta pasta `output/`:

- `MOMENTOS_C3_DEMONSTRACAO_15S.mp4`: demonstração de comparação de palavras, variedade e apresentação do kit.
- `MOMENTOS_C4_FAMILIA_15S.mp4`: conversa em família com uma proposta real do caderno e escolha no calendário.
- `MOMENTOS_C5_OFERTA_15S.mp4`: conteúdo recebido, formato digital, complementos e preço-base com impostos aplicáveis.

O comparativo de hipóteses, públicos, métricas e limitações está em `comparativo_criativos.md`. Não foram publicadas campanhas nem medidos resultados de vendas. Os anúncios são hipóteses para testar.

## Estrutura

```text
criativos_meta_3/
  gerar_3_criativos.py
  comparativo_criativos.md
  requirements.txt
  config/projeto.json
  assets/
    capa.png
    familia.png
    familia_com_pagina.png
    fonts/              fontes e licença
    voz/                WAV prontos + janelas de fala
    pages/              recortes reais gerados do PDF
  input/
    Momentos_para_Compartir_COMPLETO.pdf
    referencia_original.mp4
    referencia_otimizada.mp4
    auditoria_referencias.md
    verificacao_oferta.md
  scripts/
    comum.py
    criativo_c3.py
    criativo_c4.py
    criativo_c5.py
    audio.py
    gerar_voz_local.py   opcional
    validar.py
  output/
    MOMENTOS_C3_DEMONSTRACAO_15S.mp4
    MOMENTOS_C4_FAMILIA_15S.mp4
    MOMENTOS_C5_OFERTA_15S.mp4
    C3_legendas.srt
    C4_legendas.srt
    C5_legendas.srt
    qa/
```

Os nomes de referência com sufixos literais `(2)` e `(1)` não estavam no disco. Foram analisadas as versões canônicas dos dois vídeos anteriores e do PDF revisado, com hashes e limites documentados na auditoria. As cópias em `input/` tornam o projeto independente dos caminhos da máquina de produção.

## Windows e PowerShell

Requisitos: Windows com Python 3.11 ou posterior, FFmpeg/FFprobe e acesso de leitura ao repositório. Python 3.12 é a versão recomendada. Não é necessário executar como administrador nem alterar a política de execução do PowerShell para usar o ambiente virtual.

Se os programas ainda não estiverem instalados, estes são pacotes gratuitos distribuídos por fontes oficiais via WinGet:

```powershell
winget install --exact --id Python.Python.3.12
winget install --exact --id Gyan.FFmpeg
winget install --exact --id Git.Git
```

Após instalar, feche e abra novamente o terminal para atualizar o `PATH`. Em seguida, numa pasta em que queira guardar o projeto:

```powershell
git clone --branch entrega-video https://github.com/mateuszilio225/low-ticket.git momentos-criativos
Set-Location .\momentos-criativos\criativos_meta_3

py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

ffmpeg -version
ffprobe -version

& .\.venv\Scripts\python.exe .\gerar_3_criativos.py
Invoke-Item .\output
```

Se já tiver Python 3.11 ou posterior com outro lançador, substitua apenas `py -3.12` pelo seu comando Python. Os comandos usam caminhos relativos à pasta do projeto e preservam pastas existentes; escolha outro nome para o clone se `momentos-criativos` já existir.

Para abrir no VS Code, use **Arquivo → Abrir Pasta** e selecione `criativos_meta_3`; se o comando estiver disponível no terminal, também pode usar `code .`.

Se o FFmpeg estiver instalado fora do `PATH`, informe os caminhos dos executáveis em `config/projeto.json`, por exemplo `ffmpeg` e `ffprobe` com barras `/` ou barras invertidas duplicadas. Não altere os scripts.

## Uma única configuração editável

Edite `config/projeto.json` no VS Code:

| Campo | Uso |
| --- | --- |
| `produto.nome`, `produto.formato` | Identidade e indicação de PDF desde o início |
| `produto.preco` | Preço-base, atualmente `9,90 €` |
| `produto.preco_prefixo` | Atualmente `Desde` |
| `produto.impostos` | Atualmente `+ impuestos aplicables` |
| `produto.mostrar_preco` | `false` troca o preço por consulta à oferta no checkout |
| `produto.landing_url`, `produto.checkout_url` | Referências comerciais; não são chamadas para criar compras |
| `visual` | Fontes locais incluídas, cores, CRF e número de renderizações simultâneas |
| `audio` | Volumes, voz habilitada, loudness e pico-alvo |
| `criativos.C3/C4/C5` | Textos, nomes de arquivo e durações dos blocos |
| `paginas` | Códigos e dados de seleção dos exercícios |
| `idioma` | Identificação editorial da locução e dos textos em espanhol da Espanha |

As durações de cada criativo devem continuar somando **15 segundos**. As janelas da narração acompanham os blocos; alterações que deixem uma fala longa demais geram um erro, em vez de cortar palavras. A locução não anuncia um número de preço: o valor pode mudar no JSON sem precisar refazer a voz.

As vozes em `assets/voz/` já estão prontas em espanhol, com construções como *elegid*, *conversad* e *a vuestro ritmo*. Alterar apenas o campo `idioma` não traduz nem substitui gravações: para outro idioma, forneça textos e áudios correspondentes. As fontes incluídas tornam os acentos, símbolos e setas independentes das fontes instaladas no Windows.

Alterar a página da demonstração exige conferir a resposta e o enquadramento do recorte. O padrão C2-22 foi verificado no PDF e no solucionário: **LAGO → LADO, terceira palavra**. O recorte é uma ampliação real, não uma página inventada. O calendário do dia 8 contém C1-31 e o exemplo de conversa corresponde a essa atividade.

## Preço, impostos e oferta

O C5 apresenta **“Desde 9,90 € + impuestos aplicables”**, conforme o preço-base atual informado pelo responsável nesta tarefa. Não apresenta €9,90 como total final, não promete `IVA incluido` e orienta consultar o total no checkout.

Não foi possível conferir independentemente a oferta publicada: a landing e o checkout retornaram bloqueio **CONNECT 403 do proxy do ambiente**, antes de entregar seu conteúdo. Isso não demonstra indisponibilidade dos sites. A evidência está em `input/verificacao_oferta.md`. Antes de ativar a campanha, confira a oferta vigente para Espanha, o total com impostos e a entrega efetivamente configurada. Se não quiser exibir preço antes dessa conferência, defina `produto.mostrar_preco` como `false` e gere novamente.

Os PDFs locais confirmam o material preparado, mas não provam que todos esses arquivos estejam associados à oferta Hotmart. Os complementos exibidos devem estar incluídos na oferta anunciada. Não foram feitos pagamentos ou testes de compra.

## Áudio sem API comercial

O gerador principal usa os WAV locais que acompanham o projeto. Ele não precisa de uma API, chave, assinatura, download de modelos nem acesso à internet durante a renderização. As trilhas e os efeitos de página foram compostos por síntese no código, sem músicas de terceiros. Os anúncios têm textos comerciais sincronizados e também entregam legendas SRT; a compreensão do produto não depende da voz.

Há uma alternativa sem locução:

```powershell
& .\.venv\Scripts\python.exe .\gerar_3_criativos.py --sem-voz
```

Para regenerar a voz opcionalmente, o script `scripts/gerar_voz_local.py` usa Kokoro local. Isso requer dependências adicionais gratuitas (`kokoro-onnx`, `soundfile`, `espeakng-loader`) e os modelos do repositório oficial [Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx), publicação `model-files-v1.1`: `kokoro-v1.0.onnx` e `voices-v1.0.bin`. Informe a pasta dos modelos, sem caminhos fixos:

```powershell
& .\.venv\Scripts\python.exe -m pip install kokoro-onnx soundfile espeakng-loader
& .\.venv\Scripts\python.exe .\scripts\gerar_voz_local.py --model-dir 'C:\sua-pasta\modelos-kokoro'
```

O wrapper é MIT e o modelo Kokoro é Apache 2.0 segundo sua documentação. A voz sintética é `ef_dora`, em espanhol; não houve clonagem. Não se afirma que tenha sido gravada por um locutor humano espanhol. A cena familiar foi gerada por IA para este projeto e recebeu uma sobreposição em perspectiva da página verdadeira; ela é ilustrativa, não um depoimento ou uma filmagem documental.

## Verificações

O comando principal chama `scripts/validar.py`. Para repetir apenas os testes:

```powershell
& .\.venv\Scripts\python.exe .\scripts\validar.py
```

As verificações executadas ficam em `output/qa/verificacao.json`: duração, tamanho, FPS, codec, 450 quadros, decodificação integral, ausência de quadros pretos indevidos, áudio sem clipping e término suave, caixas de textos na área segura e hashes distintos. As três folhas de contato têm um quadro de cada segundo. A inspeção visual efetiva e seus limites ficam em `output/qa/inspecao_visual.md`.

Os textos essenciais têm pelo menos 42 px e ficam longe das bordas. As miniaturas de capas e recortes são provas visuais e não exigem que todas as suas letras pequenas sejam lidas no anúncio. Confira também a prévia dos posicionamentos escolhidos no Gerenciador de Anúncios: a interface pode cobrir margens.

O controle de qualidade técnico não mede CTR, CPA ou conversões, não valida uma oferta vigente e não substitui um teste com público real. Configure o CTA real da campanha para a landing/checkout correto; os vídeos usam texto e seta, sem fingir um botão funcional.
