# Fermarc Robótica - Plataforma E-commerce Profissional

## Overview
Plataforma completa de e-commerce desenvolvida com Python Flask, SQLite3, HTML, CSS e JavaScript. Sistema profissional com todas as funcionalidades necessárias para uma loja virtual de robótica e eletrônica.

## Tecnologias Utilizadas
- **Backend**: Python 3.11 + Flask 3.0.0
- **Banco de Dados**: SQLite3 com SQLAlchemy ORM
- **Autenticação**: Flask-Login com hash de senhas
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Deploy**: Gunicorn (pronto para Render)

## Estrutura do Projeto
```
├── app/
│   ├── __init__.py          # Configuração do Flask
│   ├── models.py            # Modelos do banco de dados
│   ├── routes/              # Rotas organizadas por módulo
│   │   ├── main.py          # Rotas públicas (home, produtos, busca)
│   │   ├── auth.py          # Autenticação (login, registro)
│   │   ├── cart.py          # Carrinho e checkout
│   │   └── admin.py         # Painel administrativo
│   ├── templates/           # Templates HTML (Jinja2)
│   │   ├── base.html        # Layout base
│   │   ├── index.html       # Página inicial
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── orders.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── admin/           # Templates administrativos
│   └── static/
│       ├── css/style.css    # Estilos CSS
│       ├── js/              # JavaScript
│       └── images/          # Imagens
├── run.py                   # Arquivo principal para executar o app
├── requirements.txt         # Dependências Python
├── Procfile                 # Configuração para Render
└── replit.md               # Documentação
```

## Funcionalidades Implementadas

### Sistema de Usuários
- ✅ Registro de novos usuários
- ✅ Login/Logout com sessões
- ✅ Hash de senhas com Werkzeug
- ✅ Controle de acesso (usuário comum vs admin)

### Catálogo de Produtos
- ✅ Listagem de produtos com paginação
- ✅ Página de detalhes do produto
- ✅ Busca de produtos por nome/código/descrição
- ✅ Filtro por categorias
- ✅ Produtos em destaque
- ✅ Imagens de produtos
- ✅ Controle de estoque

### Carrinho de Compras
- ✅ Adicionar/remover produtos
- ✅ Atualizar quantidades
- ✅ Cálculo automático de totais
- ✅ Verificação de estoque
- ✅ Cálculo de parcelamento
- ✅ Desconto PIX (5%)
- ✅ **NOVO**: Sistema de cupons de desconto
- ✅ **NOVO**: Aplicar/remover cupons no carrinho
- ✅ **NOVO**: Validação de cupons (validade, usos, compra mínima)

### Sistema de Pedidos
- ✅ Finalização de compra
- ✅ Histórico de pedidos do usuário
- ✅ Gerenciamento de status
- ✅ Controle de estoque automático
- ✅ Detalhes completos do pedido

### Painel Administrativo
- ✅ Dashboard com estatísticas
- ✅ CRUD completo de produtos
- ✅ CRUD completo de categorias
- ✅ Gerenciamento de pedidos
- ✅ Atualização de status de pedidos
- ✅ Controle de estoque
- ✅ Produtos em destaque
- ✅ **NOVO**: CRUD completo de cupons de desconto
- ✅ **NOVO**: Gerenciamento de validade e usos de cupons

### Wishlist (Lista de Desejos) - NOVO
- ✅ Adicionar produtos à lista de desejos
- ✅ Remover produtos da lista
- ✅ Visualizar lista de desejos completa
- ✅ Indicador visual de produtos na wishlist

### Sistema de Avaliações (Reviews) - NOVO
- ✅ Avaliar produtos com estrelas (1-5)
- ✅ Adicionar comentários nas avaliações
- ✅ Verificação de compra confirmada
- ✅ Editar e deletar próprias avaliações
- ✅ Exibir avaliações na página do produto

## Dados Iniciais
O sistema é inicializado com:
- **Usuário Admin**: email: `admin@fermarc.com.br`
  - Senha padrão (desenvolvimento): `TrocarSenha123!`
  - Para produção: definir variável de ambiente `ADMIN_PASSWORD`
- **8 Categorias**: Arduino, Raspberry Pi, Sensores, Módulos, Componentes, Kits Didáticos, Ferramentas, Impressão 3D
- **6 Produtos de Exemplo**: Arduino Uno, Sensor HC-SR04, Kit Iniciante, ESP32, DHT22, Arduino Nano

## Como Usar

### Desenvolvimento (Replit)
O sistema está configurado para rodar automaticamente no Replit. Basta acessar a URL fornecida.

### Deploy no Render
1. Conecte o repositório ao Render
2. Configure como Web Service
3. O Render detectará automaticamente o Procfile
4. O sistema usará SQLite3 (para produção real, recomenda-se PostgreSQL)

### Acessos
- **Site**: Página inicial com produtos
- **Login**: Faça login ou registre-se
- **Admin**: Login com usuário admin para acessar /admin

## Credenciais de Acesso
- **Administrador**: 
  - Email: `admin@fermarc.com.br`
  - Senha (dev): `TrocarSenha123!` 
  - **IMPORTANTE**: Em produção, defina a variável de ambiente `ADMIN_PASSWORD` com uma senha segura

## Recursos Adicionais
- Cache-Control configurado para evitar problemas de cache
- Sistema de mensagens flash para feedback ao usuário
- Design responsivo (mobile e desktop)
- Validações de formulário
- Proteção de rotas administrativas
- Hash seguro de senhas
- Gerenciamento de sessões

## Replit Environment Setup
- **Python Version**: 3.11
- **Dependencies**: All packages from requirements.txt installed
- **Workflow**: Flask development server on port 5000
- **Host**: Configured for 0.0.0.0 to work with Replit proxy
- **Database**: SQLite (instance/ecommerce.db)

## Recent Changes
- **2025-10-31 (Replit Setup)**: Project configured for Replit environment
  - ✅ Python 3.11 installed
  - ✅ All dependencies installed from requirements.txt
  - ✅ .gitignore created for Python projects
  - ✅ Workflow configured for Flask development server
  - ✅ Ready to run in Replit environment

- **2025-10-31 (Integração Mercado Pago + Sistema de Entrega)**: Nova funcionalidade de checkout e pagamento
  - ✅ Sistema de escolha entre retirada no local ou entrega
  - ✅ Modelo Order expandido com campos: delivery_type, delivery_address, customer_name, customer_phone, shipping_cost, payment_status, payment_id
  - ✅ Modelo StoreSettings para configurações da loja (endereço de retirada, custos de frete, frete grátis)
  - ✅ Painel administrativo para configurar local de retirada e opções de entrega
  - ✅ Integração completa com Mercado Pago SDK v2.3.0
  - ✅ Rotas de pagamento: criar preferência, webhooks, callbacks de sucesso/falha/pendente
  - ✅ Templates de status de pagamento (aprovado, recusado, pendente)
  - ✅ Formulário de checkout com validação de dados do cliente
  - ✅ Cálculo automático de frete com frete grátis acima de valor configurável

- **2025-10-31**: Adicionadas imagens demonstrativas aos produtos
  - ✅ 6 imagens reais de produtos de eletrônica e robótica
  - ✅ Produtos atualizados: Arduino Uno R3, HC-SR04, ESP32, DHT22, Arduino Nano, Kit Iniciante
  - ✅ Todos os produtos marcados como destaque na página inicial
  - ✅ Imagens armazenadas em `/app/static/images/`
  - ✅ Visual profissional com fotos reais substituindo placeholders

- **2025-10-30 (Fase 2)**: Novas funcionalidades de engajamento implementadas
  - ✅ Sistema completo de cupons de desconto
  - ✅ Wishlist (lista de desejos) funcional
  - ✅ Sistema de avaliações com estrelas e comentários
  - ✅ Novos modelos de banco de dados: Coupon, Wishlist, Review, PasswordResetToken
  - ✅ Rotas administrativas para gerenciar cupons
  - ✅ Interface de cupons integrada ao carrinho
  - ✅ Templates HTML para todas as novas funcionalidades
  
- **2025-10-30 (Fase 1)**: Sistema base implementado
  - Criada estrutura Flask completa
  - Implementados modelos base de banco de dados
  - Criadas rotas (públicas, autenticação, carrinho, admin)
  - Desenvolvidos templates HTML base
  - Sistema de autenticação funcional
  - Painel administrativo completo
  - Sistema de carrinho e pedidos funcionais
  - Pronto para deploy no Render

## Desenvolvedor
**Sistema desenvolvido por: [João Layon - Desenvolvedor Fullstack](https://dujao22.github.io/Apresentacao_Solucoes_Digitais-/)**

Portfólio completo e serviços disponíveis no link acima.

## Configuração do Mercado Pago

Para habilitar os pagamentos via Mercado Pago:

1. Crie uma conta no [Mercado Pago](https://www.mercadopago.com.br)
2. Acesse o [painel de desenvolvedores](https://www.mercadopago.com.br/developers/panel)
3. Obtenha seu **Access Token** (Production ou Test)
4. Configure a variável de ambiente no Replit:
   - Nome: `MERCADOPAGO_ACCESS_TOKEN`
   - Valor: Seu access token do Mercado Pago

**IMPORTANTE**: Use o token de teste durante o desenvolvimento e o token de produção apenas quando for publicar o site.

### Testando Pagamentos

O Mercado Pago oferece cartões de teste para simular diferentes cenários:
- **Cartão aprovado**: `5031 4332 1540 6351` (MASTERCARD)
- **Cartão recusado**: `5031 7557 3453 0604` (MASTERCARD)
- **Nome**: Qualquer nome
- **CVV**: Qualquer 3 dígitos
- **Validade**: Qualquer data futura

### Webhooks

Os webhooks estão configurados em `/pagamento/webhook` e atualizam automaticamente o status dos pedidos quando há mudanças no pagamento.

## Próximos Passos Sugeridos
- Implementar upload de imagens de produtos
- Implementar notificações por email para confirmação de pedidos
- Adicionar rastreamento de pedidos
- Migrar para PostgreSQL em produção
- Adicionar painel de analytics
- Implementar sistema de avaliação de entregas
