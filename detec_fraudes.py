import streamlit as st
import pandas as pd
import datetime
import time

# 1. configuração e identidade visual --------------------------------------------------

st.set_page_config(page_title="Stema Secure | Checkout", page_icon="🔒", layout="wide")

st.markdown("""
<style>
    /* Tema Base Stema */
    .stApp { background-color: #060B13; color: #F4F4F6; }
    h1, h2, h3, h4, h5, h6, label, p { color: #F4F4F6 !important; }
    
    /* Cores Específicas */
    .text-cyan { color: #00C4B5 !important; }
    
    /* Botão de Compra E-commerce */
    .btn-comprar {
        background-color: #00C4B5; color: #060B13 !important; font-weight: bold;
        width: 100%; border: none; padding: 12px; border-radius: 8px; font-size: 1.2rem;
    }
    .btn-comprar:hover { background-color: #00E0CF; color: #060B13 !important; }

    /* Estilo das Simulações de Email */
    .email-box {
        background-color: #ffffff; color: #333333; padding: 20px; 
        border-radius: 8px; margin-top: 10px; border-left: 5px solid #00C4B5;
        font-family: Arial, sans-serif;
    }
    .email-header { border-bottom: 1px solid #eeeeee; padding-bottom: 10px; margin-bottom: 15px; }
    .email-header p { color: #555555 !important; margin: 0; font-size: 0.9rem; }
    .email-body h3 { color: #111111 !important; margin-top: 0; }
    .email-body p { color: #333333 !important; }
    
    /* Botão 2FA no Email */
    .btn-2fa {
        display: inline-block; background-color: #ffc107; color: #000 !important;
        padding: 12px 24px; text-decoration: none; font-weight: bold;
        border-radius: 5px; margin-top: 15px; text-align: center;
    }
    
    /* Badges de Risco */
    .badge-red { background-color: #ff4b4b; color: white; padding: 5px 10px; border-radius: 4px; }
    .badge-yellow { background-color: #ffc107; color: black; padding: 5px 10px; border-radius: 4px; }
    .badge-green { background-color: #00C4B5; color: black; padding: 5px 10px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# 2. banco de dados e memória ----------------------------------------------------

@st.cache_data
def carregar_banco():
    return pd.DataFrame({
        'cpf': ['00001', '00001', '00002'],
        'nome': ['João Silva', 'João Silva', 'Lucas Pereira'],
        'email': ['joao.silva@email.com', 'joao.silva@email.com', 'lucas.p@email.com'],
        'cartao': ['1111', '1112', '2222'],
        'banco': ['Nubank', 'Itaú', 'Inter'],
        'valor_medio': [100.0, 5000.0, 250.0],
        'horario_comum': ['12.0-22.0', '10.0-16.0', '08.0-18.0'],
        'localizacao': ['São Paulo, BR', 'São Paulo, BR', 'Joinville, SC'],
        'sistema': ['Windows 11', 'Windows 11', 'Mac OS']
    })

df_base = carregar_banco()

#inicializa o estado da sessão para controlar o fluxo da tela
if 'status_compra' not in st.session_state:
    st.session_state.status_compra = 'pendente'
    st.session_state.dados_analise = {}

# 3. interface do e-commerce ----------------------------------------------------------

st.image("logo_stema.jpg", width=250) #logo Stema Secure

st.markdown("<h2 class='text-cyan'>🛒 Loja Fictícia - Finalizar Compra</h2>", unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Dados de Pagamento")
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            input_nome = st.text_input("Nome Completo", "João Silva")
            input_cpf = st.text_input("CPF", "00001")
            input_cartao = st.text_input("Final do Cartão", "1111")
        with col_form2:
            input_email = st.text_input("E-mail", "joao.silva@email.com")
            input_local = st.text_input("Localização Atual (IP)", "São Paulo, BR")
            input_sistema = st.text_input("Dispositivo", "Windows 11")

    with c2:
        st.subheader("Resumo do Pedido")
        st.write("📦 1x Smartphone Ultra X")
        input_valor = st.number_input("Total a Pagar (R$)", value=150.0, step=50.0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("FINALIZAR COMPRA ➔", use_container_width=True):
            st.session_state.status_compra = 'processando'
            st.session_state.dados_analise = {
                'cpf': input_cpf, 'cartao': input_cartao, 'valor': input_valor,
                'local': input_local, 'sistema': input_sistema, 'email': input_email, 'nome': input_nome
            }
            st.rerun()

st.markdown("---")

# 4. motor antifraude e simulação de emails ---------------------------------------------

if st.session_state.status_compra == 'processando':
    dados = st.session_state.dados_analise
    
    #efeito visual de carregamento para a apresentação
    with st.spinner("Analisando transação via Stema Secure..."):
        time.sleep(2)
    
    cliente_cpf = df_base[df_base['cpf'] == dados['cpf']]
    
    if cliente_cpf.empty or dados['cartao'] not in cliente_cpf['cartao'].values:
        st.error("❌ Transação Negada: Dados bancários inválidos.")
        st.button("Tentar Novamente", on_click=lambda: st.session_state.update(status_compra='pendente'))
    else:
        cliente_cartao = cliente_cpf[cliente_cpf['cartao'] == dados['cartao']]
        valor_medio = cliente_cartao['valor_medio'].values[0]
        local_base = cliente_cartao['localizacao'].values[0]
        sistema_base = cliente_cartao['sistema'].values[0]
        
        pontuacao = 0
        motivos = []

        if dados['valor'] > (valor_medio * 1.5):
            pontuacao += 40
            motivos.append("Valor atípico")
        if dados['local'] not in local_base:
            pontuacao += 20
            motivos.append("Localização suspeita")
        if dados['sistema'] not in sistema_base:
            pontuacao += 20
            motivos.append("Dispositivo desconhecido")

        st.markdown("<h2 class='text-cyan'>⚙️ Painel de Controle (Visão do Sistema)</h2>", unsafe_allow_html=True)
        
        #lógica de emails simulados
        st.subheader("📬 Caixa de Entrada Simulada")
        
        if pontuacao >= 70:
            st.error(f"🔴 SCORE {pontuacao}: ALTO RISCO - Bloqueio Automático Efetuado.")
            
            #email para a empresa
            st.markdown(f"""
            <div class='email-box' style='border-left-color: #ff4b4b;'>
                <div class='email-header'>
                    <p><b>De:</b> Stema Secure &lt;alertas@stema.com&gt;</p>
                    <p><b>Para:</b> Administrador da Loja</p>
                    <p><b>Assunto:</b> [URGENTE] Transação Bloqueada - Fraude Detectada</p>
                </div>
                <div class='email-body'>
                    <h3><span class='badge-red'>BLOQUEADO</span> Tentativa de fraude evitada</h3>
                    <p>Bloqueamos a compra do cliente <b>{dados['nome']}</b> no valor de <b>R$ {dados['valor']:.2f}</b>.</p>
                    <p><b>Motivos do bloqueio preventivo (Score {pontuacao}):</b><br> {', '.join(motivos)}.</p>
                    <p>Nenhuma ação é necessária da sua parte. O dinheiro não foi processado.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif pontuacao >= 40:
            st.warning(f"🟡 SCORE {pontuacao}: RISCO MODERADO - Disparando 2FA.")
            
            #email para a empresa
            st.markdown(f"""
            <div class='email-box' style='border-left-color: #ffc107;'>
                <div class='email-header'>
                    <p><b>De:</b> Stema Secure &lt;alertas@stema.com&gt;</p>
                    <p><b>Para:</b> Administrador da Loja</p>
                    <p><b>Assunto:</b> [ALERTA] Transação Pendente - Aguardando 2FA</p>
                </div>
                <div class='email-body'>
                    <h3><span class='badge-yellow'>PENDENTE</span> Verificação de Identidade Acionada</h3>
                    <p>A compra de <b>R$ {dados['valor']:.2f}</b> de <b>{dados['nome']}</b> gerou um alerta por: {', '.join(motivos)}.</p>
                    <p>Enviamos um e-mail de desafio para o cliente para garantir que a compra é legítima.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            #email para o cliente (2FA)
            st.markdown(f"""
            <div class='email-box'>
                <div class='email-header'>
                    <p><b>De:</b> Segurança Bancária &lt;seguranca@banco.com&gt;</p>
                    <p><b>Para:</b> {dados['email']}</p>
                    <p><b>Assunto:</b> Confirme sua tentativa de compra</p>
                </div>
                <div class='email-body'>
                    <h3>Olá, {dados['nome'].split()[0]}!</h3>
                    <p>Detectamos uma tentativa de compra no valor de <b>R$ {dados['valor']:.2f}</b> usando o seu cartão com final <b>{dados['cartao']}</b>.</p>
                    <p>Como essa transação foge um pouco do seu padrão habitual, precisamos ter certeza de que é você mesmo.</p>
                    <a href='#' class='btn-2fa'>✅ SIM, FUI EU (Autorizar Compra)</a>
                    <p style='margin-top: 20px; font-size: 0.8rem; color: #777;'>Se você não reconhece essa compra, ignore este e-mail e seu cartão permanecerá protegido pela Stema Secure.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.success(f"🟢 SCORE {pontuacao}: RISCO BAIXO - Compra Aprovada.")
            
            #email para empresa
            st.markdown(f"""
            <div class='email-box'>
                <div class='email-header'>
                    <p><b>De:</b> Stema Secure &lt;notificacoes@stema.com&gt;</p>
                    <p><b>Para:</b> Administrador da Loja</p>
                    <p><b>Assunto:</b> Nova Venda Aprovada e Segura!</p>
                </div>
                <div class='email-body'>
                    <h3><span class='badge-green'>APROVADO</span> Transação Liberada</h3>
                    <p>A compra do cliente <b>{dados['nome']}</b> no valor de <b>R$ {dados['valor']:.2f}</b> foi analisada e classificada como segura.</p>
                    <p>Você já pode seguir com a separação e envio do produto.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Voltar para Nova Compra"):
            st.session_state.status_compra = 'pendente'
            st.rerun()

#para enviar email reais---------------------------------------------------------

# import smtplib
# from email.mime.text import MIMEText
#
# def enviar_email_real(destinatario, assunto, corpo_html):
#     msg = MIMEText(corpo_html, 'html')
#     msg['Subject'] = assunto
#     msg['From'] = 'seu_email@gmail.com'
#     msg['To'] = destinatario
#     
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     server.login('seu_email@gmail.com', 'sua_senha_de_app')
#     server.send_message(msg)
#     server.quit()
# ---------------------------------------------------------