#!/bin/bash
# Script simplificado para geração automática de snapshot
# Apenas gera o snapshot estático - upload manual para IPFS

set -e

# Configurações
LIMIT_PER_SOURCE=5
EXTRACT_ARTICLES=true
TIMESTAMP=$(date +"%Y-%m-%d-%H%M%S")
SNAPSHOT_DIR="static_snapshots/$TIMESTAMP"

echo "🚀 Gerando snapshot estático do Politicagem..."
echo "📅 Timestamp: $TIMESTAMP"
echo "📰 Limite por fonte: $LIMIT_PER_SOURCE"
echo "📄 Extrair artigos: $EXTRACT_ARTICLES"

# Criar diretório se não existir
mkdir -p static_snapshots

# Gerar snapshot
source venv/bin/activate
if [ "$EXTRACT_ARTICLES" = true ]; then
    python3 snapshot_generator.py --output "$SNAPSHOT_DIR" --limit "$LIMIT_PER_SOURCE"
else
    python3 snapshot_generator.py --output "$SNAPSHOT_DIR" --limit "$LIMIT_PER_SOURCE" --no-extract
fi

# Limpar snapshots antigos (manter últimos 5)
echo "🧹 Limpando snapshots antigos (mantendo últimos 5)..."
cd static_snapshots
ls -t | tail -n +6 | xargs -r rm -rf
cd ..

echo "✅ Snapshot gerado com sucesso!"
echo "📁 Diretório: $SNAPSHOT_DIR"
echo "📄 Arquivo principal: $SNAPSHOT_DIR/index.html"
echo ""
echo "📋 Próximos passos manuais:"
echo "   1. Revise o conteúdo em: $SNAPSHOT_DIR"
echo "   2. Upload manual para IPFS: ipfs add -r $SNAPSHOT_DIR"
echo "   3. Copie o CID gerado"
echo "   4. Atualize seu domínio .eth/.tezos manualmente"