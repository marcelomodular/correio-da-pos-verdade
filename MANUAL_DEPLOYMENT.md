# Deployment Manual do Politicagem para IPFS

## Geração Automática de Snapshot

O snapshot estático é gerado automaticamente pelo script:

```bash
./generate_snapshot.sh
```

Ou manualmente:
```bash
python3 snapshot_generator.py --output static_snapshots/2026-09-02-120000 --limit 5
```

**Opções:**
- `--limit N`: Limite de notícias por fonte (default: 5)
- `--no-extract`: Não extrair conteúdo dos artigos (gera apenas index.html)

**O que é gerado:**
- `index.html`: Página principal com todas as notícias
- `visualizar/artigo-X.html`: Páginas estáticas individuais para cada artigo
- `snapshot_metadata.json`: Metadata do snapshot

## Upload Manual para IPFS

### 1. Iniciar daemon IPFS
```bash
ipfs daemon
```

### 2. Upload do snapshot
```bash
cd static_snapshots/2026-09-02-120000
ipfs add -r .
```

Você receberá um CID como: `QmXyZ...`

### 3. Fazer pin local (opcional mas recomendado)
```bash
ipfs pin add QmXyZ...
```

### 4. Verificar no gateway
Acesse: `https://ipfs.io/ipfs/QmXyZ...`

## Atualização Manual de Domínios Descentralizados

### Para domínio .eth (ENS)

#### Opção 1: Via ENS Manager (Web)
1. Acesse https://manager.ens.domains/
2. Conecte sua carteira Ethereum
3. Selecione seu domínio .eth
4. Vá em "Records" → "Content Hash"
5. Cole o CID no formato: `ipfs://QmXyZ...`
6. Confirme a transação (paga gas em ETH)

#### Opção 2: Via CLI (avançado)
```bash
# Exemplo conceitual - requer configuração web3.py
# Não implementado por segurança
```

### Para domínio .tezos

#### Via Tezos Domains (Web)
1. Acesse https://tezos.domains/
2. Conecte sua carteira Tezos
3. Selecione seu domínio .tezos
4. Edite o registro IPFS
5. Cole o CID no formato: `ipfs://QmXyZ...`
6. Confirme a operação (paga gas em XTZ)

## Agendamento Automático (Cron)

Para gerar snapshots automaticamente a cada 24h:

```bash
# Adicionar ao crontab
crontab -e

# Linha para executar à meia-noite todos os dias
0 0 * * * cd /home/mnlm/Público/politicagem && ./generate_snapshot.sh >> snapshots.log 2>&1
```

## Verificação

### 1. Verificar snapshot gerado
```bash
ls -la static_snapshots/
cat static_snapshots/último/snapshot_metadata.json
```

### 2. Verificar upload IPFS
```bash
ipfs ls QmXyZ...
ipfs cat QmXyZ.../index.html
```

### 3. Verificar domínio
```bash
# Para ENS
dig +short TXT _ens.seudominio.eth

# Acesse no navegador
https://seudominio.eth
```

## Segurança

- Nunca commit chaves privadas
- Use variáveis de ambiente para credenciais
- Revise o conteúdo antes do upload
- Teste em ambiente de desenvolvimento primeiro
- Mantenha backup dos snapshots importantes

## Troubleshooting

### Snapshot não gera
- Verifique dependências: `pip install -r requirements.txt`
- Verifique conexão com fontes RSS
- Verifique permissões de escrita

### Upload IPFS falha
- Verifique se daemon está rodando: `ipfs swarm peers`
- Verifique espaço em disco
- Verifique conectividade de rede

### Domínio não atualiza
- Verifique saldo de gas (ETH/XTZ)
- Verifique se você é o owner do domínio
- Verifique se a transação foi confirmada na blockchain