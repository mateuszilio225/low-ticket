# Verificação da oferta — Espanha

## Resultado executivo

**Não foi possível confirmar a oferta publicada.** As duas URLs informadas foram bloqueadas pelo proxy do ambiente com `CONNECT 403 Forbidden`. Isso é evidência de bloqueio de acesso neste ambiente; não demonstra que a página ou o checkout estejam fora do ar.

O preço-base **EUR 9,90** é um preço informado para esta tarefa, **não um preço observado no checkout por esta verificação**. O total com IVA, a moeda exibida para compradores na Espanha e os conteúdos da oferta vigente permanecem não confirmados.

## URLs verificadas

- Landing: `https://momentos-para-compartir.wrydingo.chatgpt.site/`
- Checkout: `https://pay.hotmart.com/B108342710S?off=v64n7urs`

Nenhuma compra foi iniciada, nenhum formulário foi preenchido e nenhum pagamento foi realizado.

## Procedimento executado e evidência

1. Foram lidas as skills atuais `cloud-environment-runtime` e a referência `references/networking.md`.
2. Foi inspecionado `/etc/codex/network-policy.json`: rede HTTP restrita, VPN não configurada; os dois hosts da oferta não estão na expansão de domínios permitidos do arquivo.
3. O serviço `cloud_environment.environment_status` informou observações atuais (`observations_current: true`), fase `running` e política `restricted` / `enforced`. A lista efetiva não inclui `pay.hotmart.com` nem `momentos-para-compartir.wrydingo.chatgpt.site`.
4. Um GET somente de leitura para cada URL, com os proxies e certificados herdados e verificação TLS preservada, falhou no sandbox com `curl (7): Failed to connect to proxy port 8080`.
5. A mesma consulta foi tentada uma vez pela via suportada `require_escalated`. Para ambas as URLs, o resultado foi `curl (56): CONNECT tunnel failed, response 403`.
6. Os cabeçalhos do túnel para ambas as URLs foram:

```text
HTTP/1.1 403 Forbidden
content-length: 16
content-type: text/plain
date: Tue, 10 Nov 2026 14:47:01 GMT
server: envoy
connection: close
```

O bloqueio ocorreu antes do recebimento do HTML remoto. Nenhum texto de produto, preço, impostos ou condições foi observado. Não se tentou outro proxy, conexão direta, domínio alternativo ou navegador para contornar a restrição. Não foram alterados allowlist, configuração do ambiente ou rascunho.

## O que está e o que não está confirmado

| Item | Estado | Evidência |
| --- | --- | --- |
| Identidade das URLs consultadas | Confirmada | Foram usados os dois links acima, inclusive o parâmetro `off=v64n7urs` |
| Acesso HTTP à landing neste ambiente | Bloqueado | CONNECT 403 do proxy |
| Acesso HTTP ao checkout neste ambiente | Bloqueado | CONNECT 403 do proxy |
| Preço-base EUR 9,90 no checkout | Não confirmado | Checkout não carregou |
| Preço final com IVA para Espanha | Não confirmado | País fiscal, impostos e total não foram observados |
| Total de atividades anunciado na landing atual | Não confirmado remotamente | Landing não carregou |
| Bônus e arquivos entregues pela oferta vigente | Não confirmados remotamente | Não houve leitura da oferta nem compra |
| Consistência landing × checkout | Não avaliada | Ambas as páginas bloqueadas |
| Disponibilidade de entrega após pagamento | Não testada | Nenhuma compra realizada |

Os PDFs locais do projeto e sua auditoria editorial podem demonstrar o conteúdo do produto preparado. Eles **não demonstram quais arquivos foram associados a esta oferta Hotmart** nem que o checkout cobra o preço pretendido.

## Implicação para os criativos

Até obter evidência da oferta vigente, a recomendação é **não tratar EUR 9,90 como total final ao consumidor** e não usar afirmações como «IVA incluido» ou «precio final» sem confirmação. O caminho menos dependente dessa pendência é anunciar o conteúdo verificável do produto e direcionar a «Ver contenido y precio» / «Consultar el precio» na página. Se a decisão comercial for manter o preço-base nos anúncios, registrar explicitamente que ele foi fornecido pelo responsável e que o total aplicável deve ser confirmado no checkout; isso não equivale a uma validação da oferta.

Uma confirmação efetiva pode vir de leitura autorizada dessas URLs após ajuste da política pelo responsável, ou de capturas atuais da landing e do checkout com país Espanha, moeda, preço, discriminação do IVA/total e lista de conteúdo visíveis. Não é necessário compartilhar dados de cartão nem concluir uma compra para documentar a tela pré-pagamento.
