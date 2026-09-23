import streamlit as st
import os
import pandas as pd
import altair as alt

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Dashboard de Indicadores - Ifes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CONFIGURAÇÃO GLOBAL DE LOCALE (PT-BR)
# ==========================================
locale_pt_br = {
    "decimal": ",",
    "thousands": ".",
    "grouping": [3],
    "currency": ["R$ ", ""]
}
alt.renderers.set_embed_options(formatLocale=locale_pt_br)

# ==========================================
# ESTILIZAÇÃO PERSONALIZADA (CORES DO IFES)
# ==========================================
st.markdown(
    """
    <style>
        /* Ajustando fontes e cores gerais */
        html, body, [class*="css"] {
            font-family: 'Liberation Sans', sans-serif;
        }
        
        /* Cor de fundo da aplicação */
        .stApp {
            background-color: #F4F6F8;
        }

        /* Customização do Cabeçalho Institucional de Ponta a Ponta */
        .ifes-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 30px;
            background-color: #FFFFFF;
            border-bottom: 4px solid #006633;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 25px;
        }
        .ifes-title-box h1 {
            color: #006633;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0;
            padding: 0;
        }
       .ifes-title-box p {
            color: #718096;
            font-size: 0.95rem;
            margin: 4px 0 0 0;
            padding: 0;
        }
        /* Crédito de Desenvolvimento Alinhado à Direita */
        .dev-credit {
            text-align: right;
            font-family: 'Liberation Sans', sans-serif;
        }
        .dev-credit-title {
            font-size: 0.8rem;
            color: #718096;
            font-weight: bold;
            display: block;
        }
        .dev-credit-name {
            font-size: 0.75rem;
            color: #718096;
            display: block;
            margin-top: 2px;
            font-weight: normal;
        }

        /* Banner de "Em Construção" Estilizado */
        .under-construction-card {
            background-color: #FFFFFF;
            border-left: 5px solid #CC0000;
            padding: 25px;
            border-radius: 4px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-top: 20px;
            text-align: center;
        }
        .under-construction-title {
            color: #CC0000;
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .under-construction-text {
            color: #4A5568;
            font-size: 1.1rem;
        }

        /* Estilização da Barra Lateral */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0;
        }
        
        /* Forçar centralização do logotipo na barra lateral */
        [data-testid="stSidebar"] [data-testid="stImage"] {
            display: flex !important;
            justify-content: center !important;
        }
        [data-testid="stSidebar"] [data-testid="stImage"] img {
            display: block !important;
            margin-left: auto !important;
            margin-right: auto !important;
            margin-bottom: 15px !important;
        }

        /* Ajustes de espaçamento interno */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# CABEÇALHO DA PÁGINA
# ==========================================
st.markdown(
    """
    <div class="ifes-header">
        <div class="ifes-title-box">
            <h1>Painel de Indicadores Educacionais</h1>
            <h1>Campus Cachoeiro de Itapemirim</h1>
            <p>Instituto Federal do Espírito Santo</p>
            <p>Dados extraídos para este painel em 01/09/2026</p>
        </div>
        <div class="dev-credit">
            <span class="dev-credit-title">Desenvolvido por @wtcifes</span>
            <span class="dev-credit-name">Wagner Teixeira da Costa</span>
            <span class="dev-credit-name">NESC - Núcleo de Estudos em Sistemas Ciberfísicos</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# BARRA LATERAL (SIDEBAR) - LOGO E MENUS
# ==========================================

if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=180)
else:
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 20px; background-color: #006633; color: #FFFFFF; border-radius: 4px; margin-bottom: 15px; font-weight: bold; font-family: 'Liberation Sans', sans-serif;">
            <div style="font-size: 1.5rem; letter-spacing: -1px; margin-bottom: 5px;">Ifes</div>
            <div style="font-size: 0.75rem; font-weight: normal; opacity: 0.85;">[logo.png]</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <h3 style="color: #006633; margin: 0; font-weight: 700; font-size: 1.15rem;">Menu Principal</h3>
        <hr style="margin: 10px 0 20px 0; border: 0; border-top: 1px solid #E2E8F0;">
    </div>
    """,
    unsafe_allow_html=True
)

menu_opcao = st.sidebar.radio(
    "Selecione uma categoria:",
    [
        "🏠 Início",
        "🎯 Candidato x Vaga",
        "🎓 Acadêmico",
        "📊 Plataforma PNP",
        "📝 Enem",
        "🧪 Enade",
        "🏛️ Conif",
        "ℹ️ Informações Adicionais"
    ]
)

# ==========================================
# FUNÇÃO AUXILIAR PARA FORMATAR VALORES PT-BR
# ==========================================
def fmt_br(val, casas=2):
    if pd.isna(val) or val is None:
        return ""
    try:
        val_f = float(val)
        fmt = f"{{:,.{casas}f}}"
        return fmt.format(val_f).replace(',', 'X').replace('.', ',').replace('X', '.')
    except ValueError:
        return str(val)

def render_em_construcao(nome_pagina):
    st.markdown(
        f"""
        <div class="under-construction-card">
            <div class="under-construction-title">⚠️ Área em Desenvolvimento</div>
            <div class="under-construction-text">
                A tela <strong>"{nome_pagina}"</strong> está sendo integrada aos bancos de dados do Ifes. 
                <br>Em breve os indicadores e gráficos interativos estarão disponíveis aqui.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------
# 1. INÍCIO
# ------------------------------------------
if menu_opcao == "🏠 Início":
    st.markdown("### 🏠 Início")
    
    st.markdown(
        """
        Bem-vindo ao **Painel de Indicadores Educacionais do Ifes Campus Cachoeiro de Itapemirim**.
        
        Este dashboard foi projetado para promover o acesso público, a transparência e a tomada de decisões acadêmicas com base em dados consolidados do sistema acadêmico, da [Plataforma Nilo Peçanha](https://www.gov.br/mec/pt-br/pnp), da plataforma de [Dados Abertos do Ministério da Educação](https://dadosabertos.mec.gov.br/) e dos [microdados do Inep](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados).

        ---

        #### 🎯 A Importância da Gestão Baseada em Dados

        A implementação deste painel transforma dados institucionais em conhecimento estratégico. Em um cenário educacional dinâmico, acompanhar indicadores em tempo real permite:
        * **Diagnóstico Preciso:** Identificar gargalos de ingresso, retenção e evasão discente.
        * **Alocação Eficiente de Recursos:** Direcionar investimentos pedagógicos, infraestrutura e ações de assistência estudantil com base em evidências estatísticas.
        * **Tomada de Decisão Assertiva:** Subsidiar gestores, docentes e comissões acadêmicas com diagnósticos precisos para o planejamento de ações preventivas e de melhoria contínua da gestão.

        ---

        #### 📌 Navegação do Painel

        Utilize o menu lateral à esquerda para navegar pelas diferentes dimensões de dados do Instituto:

        * **🏠 Início:** Apresentação da plataforma, objetivos institucionais, fontes de dados e guia de navegação.
        * **🎯 Candidato x Vaga:** Análise da demanda e concorrência nos processos seletivos do campus por curso, modalidade e turno.
        * **🎓 Acadêmico:** Mapeamento do fluxo discente (situação de matrícula, retenção por reprovações, desempenho em disciplinas e taxa de integralização temporal).
        * **📊 Plataforma PNP:** Indicadores oficiais da Rede Federal alinhados à Plataforma Nilo Peçanha (eficiência acadêmica, gastos por aluno e taxa de retenção).
        * **📝 Enem:** Dados do Exame Nacional do Ensino Médio para acompanhamento do perfil de entrada e desempenho dos ingressantes.
        * **🧪 Enade:** Resultados e indicadores do Exame Nacional de Desempenho dos Estudantes para avaliação da qualidade dos cursos de graduação.
        * **🏛️ Conif:** Dados institucionais e comparativos alinhados às diretrizes do Conselho Nacional das Instituições da Rede Federal.
        * **ℹ️ Informações Adicionais:** Documentações técnicas, notas metodológicas e orientações adicionais sobre o tratamento dos dados do painel.
        """
    )

# ------------------------------------------
# 2. CANDIDATO X VAGA
# ------------------------------------------
elif menu_opcao == "🎯 Candidato x Vaga":
    st.markdown("### 📝 Processos Seletivos")
    
    tab1, tab2 = st.tabs([
        "📊 Candidato x Vaga", 
        "📄 Editais"
    ])
    
    with tab1:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, 'Cand_Vaga.csv')
            
            try:
                df_cv = pd.read_csv(csv_path, sep=";", encoding="utf-8")
            except UnicodeDecodeError:
                df_cv = pd.read_csv(csv_path, sep=";", encoding="latin1")
                
            df_cv['Curso'] = df_cv['Curso'].replace({
                'Informatica para Internet': 'Informática para Internet', 
                'Eletromecanica': 'Eletromecânica'
            })
            
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA</p>", unsafe_allow_html=True)
            filtros_col1, filtros_col2, filtros_col3, filtros_col4 = st.columns(4)
            
            if 'f_semestres' not in st.session_state: st.session_state.f_semestres = []
            if 'f_cursos' not in st.session_state: st.session_state.f_cursos = []
            if 'f_modalidades' not in st.session_state: st.session_state.f_modalidades = []
            if 'f_turnos' not in st.session_state: st.session_state.f_turnos = []
            
            def get_opts(col):
                df_temp = df_cv.copy()
                if col != 'Semestre' and st.session_state.f_semestres: df_temp = df_temp[df_temp['Semestre'].isin(st.session_state.f_semestres)]
                if col != 'Curso' and st.session_state.f_cursos: df_temp = df_temp[df_temp['Curso'].isin(st.session_state.f_cursos)]
                if col != 'Modalidade' and st.session_state.f_modalidades: df_temp = df_temp[df_temp['Modalidade'].isin(st.session_state.f_modalidades)]
                if col != 'Turno' and st.session_state.f_turnos: df_temp = df_temp[df_temp['Turno'].isin(st.session_state.f_turnos)]
                
                opts = sorted(list(df_temp[col].dropna().unique()))
                if col == 'Semestre': opts = sorted(list(set(opts + st.session_state.f_semestres)), reverse=True)
                if col == 'Curso': opts = sorted(list(set(opts + st.session_state.f_cursos)))
                if col == 'Modalidade': opts = sorted(list(set(opts + st.session_state.f_modalidades)))
                if col == 'Turno': opts = sorted(list(set(opts + st.session_state.f_turnos)))
                return opts

            with filtros_col1:
                st.session_state.f_semestres = st.multiselect("Semestre", get_opts('Semestre'), default=st.session_state.f_semestres, placeholder="Todos")
            with filtros_col2:
                st.session_state.f_cursos = st.multiselect("Curso", get_opts('Curso'), default=st.session_state.f_cursos, placeholder="Todos")
            with filtros_col3:
                st.session_state.f_modalidades = st.multiselect("Modalidade", get_opts('Modalidade'), default=st.session_state.f_modalidades, placeholder="Todas")
            with filtros_col4:
                st.session_state.f_turnos = st.multiselect("Turno", get_opts('Turno'), default=st.session_state.f_turnos, placeholder="Todos")
                
            st.markdown("---")
            
            df_filtrado = df_cv.copy()
            if st.session_state.f_semestres: df_filtrado = df_filtrado[df_filtrado['Semestre'].isin(st.session_state.f_semestres)]
            if st.session_state.f_cursos: df_filtrado = df_filtrado[df_filtrado['Curso'].isin(st.session_state.f_cursos)]
            if st.session_state.f_modalidades: df_filtrado = df_filtrado[df_filtrado['Modalidade'].isin(st.session_state.f_modalidades)]
            if st.session_state.f_turnos: df_filtrado = df_filtrado[df_filtrado['Turno'].isin(st.session_state.f_turnos)]
                
            total_vagas = df_filtrado['Vagas'].sum()
            total_inscritos = df_filtrado['Inscritos'].sum()
            cand_vaga = total_inscritos / total_vagas if total_vagas > 0 else 0
            
            box_style = """
            <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 20px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;'>
                <p style='color: #666; font-size: 1.1rem; margin-bottom: 5px; font-weight: bold;'>{title}</p>
                <h2 style='color: #006633; margin-top: 0px; font-size: 2.2rem;'>{value}</h2>
            </div>
            """
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(box_style.format(title="Total de Vagas", value=fmt_br(total_vagas, 0)), unsafe_allow_html=True)
            with col2:
                st.markdown(box_style.format(title="Total de Inscritos", value=fmt_br(total_inscritos, 0)), unsafe_allow_html=True)
            with col3:
                st.markdown(box_style.format(title="Candidato x Vaga Geral", value=fmt_br(cand_vaga, 2)), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

            if not df_filtrado.empty:
                df_curso_cand = df_filtrado.groupby(['Curso', 'Modalidade'])[['Vagas', 'Inscritos']].sum().reset_index()
                df_curso_cand['Cand_Vaga'] = df_curso_cand['Inscritos'] / df_curso_cand['Vagas']
                df_curso_cand['Cand_Vaga'] = df_curso_cand['Cand_Vaga'].fillna(0)

                df_curso_cand['Curso_Modalidade'] = df_curso_cand['Curso'] + " - " + df_curso_cand['Modalidade']

                top_menores = df_curso_cand.sort_values(by='Cand_Vaga', ascending=True).head(5)
                top_maiores = df_curso_cand.sort_values(by='Cand_Vaga', ascending=False).head(5)

                card_list_style = """
                <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px 20px; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 100%;'>
                    <p style='color: {color}; font-size: 1.05rem; margin-bottom: 10px; font-weight: bold; text-align: center;'>{title}</p>
                    <ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>
                        {items}
                    </ul>
                </div>
                """

                items_menores = "".join([
                    f"<li style='display: flex; justify-content: space-between; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.9rem; color: #333;'>"
                    f"<span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 78%;' title='{row['Curso_Modalidade']}'>• {row['Curso_Modalidade']}</span>"
                    f"<strong style='color: #006633;'>{fmt_br(row['Cand_Vaga'], 2)}</strong></li>"
                    for _, row in top_menores.iterrows()
                ])

                items_maiores = "".join([
                    f"<li style='display: flex; justify-content: space-between; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.9rem; color: #333;'>"
                    f"<span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 78%;' title='{row['Curso_Modalidade']}'>• {row['Curso_Modalidade']}</span>"
                    f"<strong style='color: #006633;'>{fmt_br(row['Cand_Vaga'], 2)}</strong></li>"
                    for _, row in top_maiores.iterrows()
                ])

                col_menores, col_maiores = st.columns(2)
                with col_menores:
                    st.markdown(card_list_style.format(title="📉 Cursos com Menor Candidato x Vaga", color="#2E7D32", items=items_menores), unsafe_allow_html=True)
                with col_maiores:
                    st.markdown(card_list_style.format(title="📈 Cursos com Maior Candidato x Vaga", color="#006633", items=items_maiores), unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📈 VISÃO GRÁFICA</p>", unsafe_allow_html=True)
            
            df_group = df_filtrado.groupby('Semestre')[['Vagas', 'Inscritos']].sum().reset_index()
            df_group['Cand x Vaga'] = df_group['Inscritos'] / df_group['Vagas']
            df_group['Cand x Vaga'] = df_group['Cand x Vaga'].fillna(0)
            
            df_group['Vagas_Txt'] = df_group['Vagas'].apply(lambda x: fmt_br(x, 0))
            df_group['Inscritos_Txt'] = df_group['Inscritos'].apply(lambda x: fmt_br(x, 0))
            df_group['Cand_Vaga_Txt'] = df_group['Cand x Vaga'].apply(lambda x: fmt_br(x, 2))

            def criar_grafico_altair(df_dados, coluna_y, col_txt, cor_barra_padrao):
                max_val = df_dados[coluna_y].max()
                cor_destaque = alt.condition(
                    alt.datum[coluna_y] == max_val,
                    alt.value('#006633'), 
                    alt.value(cor_barra_padrao)
                )
                y_axis = alt.Axis(title=None, format=',d', labelExpr="replace(datum.label, ',', '.')")
                base = alt.Chart(df_dados).encode(x=alt.X('Semestre:N', axis=alt.Axis(labelAngle=-90, grid=True, gridColor='#EAEAEA')))
                barras = base.mark_bar().encode(y=alt.Y(f'{coluna_y}:Q', axis=y_axis), color=cor_destaque)
                textos = base.mark_text(align='center', baseline='bottom', dy=-5, color='black', fontWeight='bold').encode(
                    y=alt.Y(f'{coluna_y}:Q'), text=alt.Text(f'{col_txt}:N')
                )
                return (barras + textos).properties(height=300)
            
            st.markdown("**1. Total de Vagas por Semestre**")
            st.altair_chart(criar_grafico_altair(df_group, 'Vagas', 'Vagas_Txt', '#66BB6A'), width="stretch")
            
            st.markdown("**2. Total de Inscritos por Semestre**")
            st.altair_chart(criar_grafico_altair(df_group, 'Inscritos', 'Inscritos_Txt', '#4CAF50'), width="stretch")
                
            st.markdown("**3. Relação Candidato x Vaga por Semestre**")
            st.altair_chart(criar_grafico_altair(df_group, 'Cand x Vaga', 'Cand_Vaga_Txt', '#66BB6A'), width="stretch")
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📊 Consultar Tabela Geral - Candidato x Vaga", expanded=True):
                df_exibicao = df_filtrado.drop(columns=['Campus'], errors='ignore').copy()
                for num_col in ['Vagas', 'Inscritos']:
                    if num_col in df_exibicao.columns:
                        df_exibicao[num_col] = df_exibicao[num_col].apply(lambda x: fmt_br(x, 0))
                st.dataframe(df_exibicao, width="stretch", hide_index=True)

        except FileNotFoundError:
            st.error("Arquivo 'Cand_Vaga.csv' não encontrado.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao carregar os dados: {e}")

    with tab2:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_editais_path = os.path.join(script_dir, 'Cand_Vaga_Editais.csv')
            
            try:
                df_editais = pd.read_csv(csv_editais_path, sep=";", encoding="utf-8")
            except UnicodeDecodeError:
                df_editais = pd.read_csv(csv_editais_path, sep=";", encoding="latin1")
            
            if 'df_filtrado' in locals() and not df_filtrado.empty:
                semestres_ativos = df_filtrado['Semestre'].unique()
                df_editais = df_editais[df_editais['Semestre'].isin(semestres_ativos)]
            
            st.dataframe(
                df_editais, 
                width="stretch", 
                hide_index=True,
                column_config={
                    "Semestre": st.column_config.TextColumn(width="small"),
                    "Edital": st.column_config.TextColumn(width="medium")
                }
            )
        except FileNotFoundError:
            st.warning("Arquivo 'Cand_Vaga_Editais.csv' não encontrado.")
        except Exception as e:
            st.error(f"Erro ao carregar os editais: {e}")

# ------------------------------------------
# 3. ACADÊMICO
# ------------------------------------------
elif menu_opcao == "🎓 Acadêmico":
    st.markdown("### 🎓 Dados do Sistema Acadêmico")

    # ==========================================
    # 📌 MAPEADOR DE RÓTULOS (EIXO X DOS HEATMAPS)
    # ==========================================
    MAPA_LEGENDAS = {
        # Tempo
        '0-2 anos': 'Tempo: 0 a 2 anos',
        '2-4 anos': 'Tempo: 2 a 4 anos',
        '4-6 anos': 'Tempo: 4 a 6 anos',
        '>6 anos': 'Tempo: >6 anos',
        # Estágio
        'Sim': 'Estágio: Sim',
        'Não': 'Estágio: Não',
        'SIM': 'Estágio: Sim',
        'NÃO': 'Estágio: Não',
        # Sexo
        'M': 'Masc',
        'F': 'Femin',
        'MASCULINO': 'Masc',
        'FEMININO': 'Femin',
        # Formas de Ingresso
        'AMPLA CONCORRÊNCIA': 'Ampla Concorrência',
        'AMPLA CONCORRENCIA': 'Ampla Concorrência',
        'AÇÃO AFIRMATIVA': 'Ação Afirmativa',
        'ACAO AFIRMATIVA': 'Ação Afirmativa',
        'COTAS': 'Ação Afirmativa',
        'OUTROS': 'Outros'
    }

    def limpar_rotulo(val):
        val_str = str(val).strip()
        return MAPA_LEGENDAS.get(val_str, MAPA_LEGENDAS.get(val_str.upper(), val_str))

    # ==========================================
    # TABS PRINCIPAIS
    # ==========================================
    tab_sit, tab2, tab3, tab4 = st.tabs([
        "📁 Situação de Matrícula", 
        "❌ Quantidade de Reprovações", 
        "📚 Situação das Disciplinas", 
        "⏳ Formam no Tempo ?"
    ])
    
    # ==========================================
    # TAB 1: SITUAÇÃO DE MATRÍCULA
    # ==========================================
    with tab_sit:
        subtab_ciclo, subtab_semestre = st.tabs([
            "🔄 Ciclo", 
            "📅 Semestre"
        ])
        
        @st.cache_data
        def load_acad_data():
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, 'CI_Acad.csv')
            try:
                df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(csv_path, sep=';', encoding='latin1')
            
            if 'CR' in df.columns:
                df['CR'] = df['CR'].astype(str).str.replace(',', '.', regex=False).apply(pd.to_numeric, errors='coerce')
            if 'Tempo' in df.columns:
                df['Tempo'] = df['Tempo'].astype(str).str.replace(',', '.', regex=False).apply(pd.to_numeric, errors='coerce')
            if 'Idade' in df.columns:
                df['Idade'] = df['Idade'].astype(str).str.replace(',', '.', regex=False).apply(pd.to_numeric, errors='coerce')
            if 'Descricao_Curso' in df.columns and 'Modalidade' in df.columns:
                df['Curso_Modalidade'] = df['Descricao_Curso'].fillna('') + ' - ' + df['Modalidade'].fillna('')
            return df

        df_acad_full = load_acad_data()

        # Helper para Matriz de Associação (Situação de Matrícula)
        def render_heatmap_sit(df_source, title):
            st.markdown(f"**🔥 Matriz de Associação: {title}**")
            
            df_temp = df_source.copy()
            estagio_col = 'Fez_Estágio' if 'Fez_Estágio' in df_temp.columns else ('Fez_Estagio' if 'Fez_Estagio' in df_temp.columns else None)
            
            if 'Tempo' in df_temp.columns:
                df_temp['Faixa_Tempo'] = pd.cut(
                    df_temp['Tempo'], 
                    bins=[-1, 2, 4, 6, 99], 
                    labels=['0-2 anos', '2-4 anos', '4-6 anos', '>6 anos']
                )
            
            blocos = []
            if 'Faixa_Tempo' in df_temp.columns: blocos.append('Faixa_Tempo')
            if estagio_col: blocos.append(estagio_col)
            if 'Forma_Ingresso' in df_temp.columns: blocos.append('Forma_Ingresso')
            if 'Sexo' in df_temp.columns: blocos.append('Sexo')

            melted_data = []
            order_labels = []

            for cv in blocos:
                if cv in df_temp.columns and 'Situacao_Matricula' in df_temp.columns:
                    ct = pd.crosstab(df_temp['Situacao_Matricula'], df_temp[cv], normalize='index') * 100
                    for col_val in ct.columns:
                        rotulo_limpo = limpar_rotulo(col_val)
                        if rotulo_limpo not in order_labels:
                            order_labels.append(rotulo_limpo)
                        for row_val in ct.index:
                            melted_data.append({
                                'Situação Matrícula': str(row_val),
                                'Atributo': rotulo_limpo,
                                'Proporção (%)': ct.loc[row_val, col_val]
                            })

            if melted_data:
                df_hm = pd.DataFrame(melted_data)
                df_hm['Txt'] = df_hm['Proporção (%)'].apply(lambda x: fmt_br(x, 1) + "%")
                
                chart = alt.Chart(df_hm).mark_rect().encode(
                    x=alt.X('Atributo:O', title=None, sort=order_labels, axis=alt.Axis(labelAngle=-90, labelFontSize=11)),
                    y=alt.Y('Situação Matrícula:O', title='Situação de Matrícula'),
                    color=alt.Color('Proporção (%):Q', scale=alt.Scale(scheme='greens'), legend=alt.Legend(title="Proporção %")),
                    tooltip=['Situação Matrícula:N', 'Atributo:N', 'Txt:N']
                )
                text = chart.mark_text(baseline='middle', fontSize=10, fontWeight='bold').encode(
                    text='Txt:N',
                    color=alt.condition(alt.datum['Proporção (%)'] > 50, alt.value('white'), alt.value('black'))
                )
                st.altair_chart((chart + text).properties(height=320).interactive(), width="stretch")

        # SUB-ABA 1: CICLO
        with subtab_ciclo:
            if df_acad_full.empty:
                st.warning("Dados não encontrados.")
            else:
                st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA (CICLO)</p>", unsafe_allow_html=True)
                
                for f_key in ['f_semestre_acad', 'f_mod_acad', 'f_curso_acad', 'f_sit_acad', 'f_forma_acad']:
                    if f_key not in st.session_state:
                        st.session_state[f_key] = []
                        
                def get_opts_acad(col):
                    df_temp = df_acad_full.copy()
                    if col != 'Semestre_Letivo_Inicial' and st.session_state.f_semestre_acad: df_temp = df_temp[df_temp['Semestre_Letivo_Inicial'].isin(st.session_state.f_semestre_acad)]
                    if col != 'Modalidade' and st.session_state.f_mod_acad: df_temp = df_temp[df_temp['Modalidade'].isin(st.session_state.f_mod_acad)]
                    if col != 'Descricao_Curso' and st.session_state.f_curso_acad: df_temp = df_temp[df_temp['Descricao_Curso'].isin(st.session_state.f_curso_acad)]
                    if col != 'Situacao_Matricula' and st.session_state.f_sit_acad: df_temp = df_temp[df_temp['Situacao_Matricula'].isin(st.session_state.f_sit_acad)]
                    if col != 'Forma_Ingresso' and st.session_state.f_forma_acad: df_temp = df_temp[df_temp['Forma_Ingresso'].isin(st.session_state.f_forma_acad)]
                    
                    opts = sorted(list(df_temp[col].dropna().unique()))
                    if col == 'Semestre_Letivo_Inicial':
                        opts = sorted(list(set(opts + st.session_state.f_semestre_acad)), reverse=True)
                    return opts
                    
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.session_state.f_semestre_acad = st.multiselect("Ciclo", get_opts_acad('Semestre_Letivo_Inicial'), default=st.session_state.f_semestre_acad, placeholder="Todos")
                with col2:
                    st.session_state.f_mod_acad = st.multiselect("Modalidade", get_opts_acad('Modalidade'), default=st.session_state.f_mod_acad, placeholder="Todas")
                with col3:
                    st.session_state.f_curso_acad = st.multiselect("Curso", get_opts_acad('Descricao_Curso'), default=st.session_state.f_curso_acad, placeholder="Todos")
                with col4:
                    st.session_state.f_sit_acad = st.multiselect("Situação", get_opts_acad('Situacao_Matricula'), default=st.session_state.f_sit_acad, placeholder="Todas")
                with col5:
                    st.session_state.f_forma_acad = st.multiselect("Forma Ingresso", get_opts_acad('Forma_Ingresso'), default=st.session_state.f_forma_acad, placeholder="Todas")

                df_acad = df_acad_full.copy()
                if st.session_state.f_semestre_acad: df_acad = df_acad[df_acad['Semestre_Letivo_Inicial'].isin(st.session_state.f_semestre_acad)]
                if st.session_state.f_mod_acad: df_acad = df_acad[df_acad['Modalidade'].isin(st.session_state.f_mod_acad)]
                if st.session_state.f_curso_acad: df_acad = df_acad[df_acad['Descricao_Curso'].isin(st.session_state.f_curso_acad)]
                if st.session_state.f_sit_acad: df_acad = df_acad[df_acad['Situacao_Matricula'].isin(st.session_state.f_sit_acad)]
                if st.session_state.f_forma_acad: df_acad = df_acad[df_acad['Forma_Ingresso'].isin(st.session_state.f_forma_acad)]

                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                
                modo_vis_acad = st.radio(
                    "Modo de Exibição dos Indicadores:",
                    ["Valor Absoluto", "Valor em %"],
                    horizontal=True,
                    key="radio_modo_vis_acad"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                def format_val(val, total, is_money=False):
                    if pd.isna(val): return "-"
                    if modo_vis_acad == "Valor em %" and not is_money:
                        pct = (val / total * 100) if total > 0 else 0
                        return fmt_br(pct, 1) + "%"
                    else:
                        if isinstance(val, float):
                            return fmt_br(val, 1)
                        return fmt_br(val, 0)
                
                tot_alunos = len(df_acad)
                
                estagio_col = 'Fez_Estágio' if 'Fez_Estágio' in df_acad.columns else ('Fez_Estagio' if 'Fez_Estagio' in df_acad.columns else None)
                
                df_est_total = df_acad[df_acad[estagio_col].astype(str).str.upper() == 'SIM'] if estagio_col else pd.DataFrame()
                tot_estagio = len(df_est_total)
                evad_estagio = len(df_est_total[df_est_total['Situacao_Matricula'].str.upper() == 'EVADIDO'])
                concl_estagio = len(df_est_total[df_est_total['Situacao_Matricula'].str.upper() == 'CONCLUÍDO'])
                
                cr_medio = df_acad['CR'].mean()
                idade_media = df_acad['Idade'].mean() if 'Idade' in df_acad.columns else None
                t_evad = df_acad[df_acad['Situacao_Matricula'].str.upper() == 'EVADIDO']['Tempo'].mean()
                t_concl = df_acad[df_acad['Situacao_Matricula'].str.upper() == 'CONCLUÍDO']['Tempo'].mean()

                card_style = "<div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 12px 5px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; height: 100%;'><p style='color: #666; font-size: 0.85rem; margin-bottom: 6px; font-weight: bold;'>{title}</p>{main_val}{subtitle}</div>"

                c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
                c1.markdown(card_style.format(title="Total de Alunos", main_val=f"<h2 style='color: #006633; margin: 5px 0; font-size: 1.4rem;'>{fmt_br(tot_alunos, 0)}</h2>", subtitle=""), unsafe_allow_html=True)
                
                sit_counts = df_acad['Situacao_Matricula'].value_counts().head(3)
                sit_txt = "".join([f"<p style='margin: 2px 0; font-size: 0.78rem; color: #444;'><strong>{k}:</strong> {format_val(v, tot_alunos)}</p>" for k, v in sit_counts.items()])
                c2.markdown(card_style.format(title="Situação Matrícula", main_val="", subtitle=sit_txt), unsafe_allow_html=True)
                
                form_counts = df_acad['Forma_Ingresso'].value_counts().head(3)
                form_txt = "".join([f"<p style='margin: 2px 0; font-size: 0.78rem; color: #444;'><strong>{k}:</strong> {format_val(v, tot_alunos)}</p>" for k, v in form_counts.items()])
                c3.markdown(card_style.format(title="Formas de Ingresso", main_val="", subtitle=form_txt), unsafe_allow_html=True)

                sex_counts = df_acad['Sexo'].value_counts()
                sex_txt = "".join([f"<p style='margin: 2px 0; font-size: 0.78rem; color: #444;'><strong>{k}:</strong> {format_val(v, tot_alunos)}</p>" for k, v in sex_counts.items()])
                c4.markdown(card_style.format(title="Distribuição Sexo", main_val="", subtitle=sex_txt), unsafe_allow_html=True)

                c5.markdown(card_style.format(title="Fizeram Estágio", main_val=f"<h2 style='color: #006633; margin: 2px 0; font-size: 1.2rem;'>{format_val(tot_estagio, tot_alunos)}</h2>", subtitle=f"<p style='margin: 2px 0; font-size: 0.72rem; color: #444;'>Evadidos: {format_val(evad_estagio, tot_estagio)}<br>Concluídos: {format_val(concl_estagio, tot_estagio)}</p>"), unsafe_allow_html=True)
                c6.markdown(card_style.format(title="CR Médio", main_val=f"<h2 style='color: #006633; margin: 5px 0; font-size: 1.4rem;'>{format_val(cr_medio, tot_alunos, is_money=True)}</h2>", subtitle=f"<p style='margin: 2px 0; font-size: 0.72rem; color: #444;'>Cursos com CR</p>"), unsafe_allow_html=True)
                c7.markdown(card_style.format(title="Idade Média", main_val=f"<h2 style='color: #006633; margin: 5px 0; font-size: 1.4rem;'>{fmt_br(idade_media, 1) + ' anos' if pd.notnull(idade_media) else '-'}</h2>", subtitle=f"<p style='margin: 2px 0; font-size: 0.72rem; color: #444;'>Idade dos Alunos</p>"), unsafe_allow_html=True)
                c8.markdown(card_style.format(title="Tempo Médio", main_val="", subtitle=f"<p style='margin: 4px 0; font-size: 0.78rem; color: #444;'><strong>Evadidos:</strong> {format_val(t_evad, 0, is_money=True)} anos<br><strong>Concluídos:</strong> {format_val(t_concl, 0, is_money=True)} anos</p>"), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                
                def create_card_list(title, color, data_dict, is_pct=False):
                    items_html = ""
                    for nome, valor in data_dict.items():
                        nome_clean = str(nome).replace('<', '&lt;').replace('>', '&gt;')
                        val_str = f"{fmt_br(valor * 100, 1)}%" if is_pct else f"{fmt_br(valor, 1)} anos"
                        items_html += f"<li style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.88rem; color: #333;'><span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 78%;' title='{nome_clean}'>• {nome_clean}</span><strong style='color: {color};'>{val_str}</strong></li>"
                    return f"<div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px 20px; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 100%;'><p style='color: {color}; font-size: 1.05rem; margin-bottom: 10px; font-weight: bold; text-align: center;'>{title}</p><ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>{items_html}</ul></div>"

                t1, t2 = st.columns(2)
                with t1:
                    evasao_df = df_acad.groupby('Curso_Modalidade')['Situacao_Matricula'].agg(
                        Total='count',
                        Evadidos=lambda x: (x.str.upper() == 'EVADIDO').sum()
                    ).reset_index()
                    evasao_df['Taxa_Evasao'] = (evasao_df['Evadidos'] / evasao_df['Total']).fillna(0)
                    
                    df_maior_ev = evasao_df[evasao_df['Taxa_Evasao'] > 0].sort_values('Taxa_Evasao', ascending=False).head(3)
                    maior_ev = dict(zip(df_maior_ev['Curso_Modalidade'], df_maior_ev['Taxa_Evasao']))
                    
                    df_menor_ev = evasao_df[evasao_df['Taxa_Evasao'] > 0].sort_values('Taxa_Evasao', ascending=True).head(3)
                    menor_ev = dict(zip(df_menor_ev['Curso_Modalidade'], df_menor_ev['Taxa_Evasao']))
                    
                    st.markdown(create_card_list("📈 Cursos com Maior Evasão", "#E53935", maior_ev, is_pct=True), unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(create_card_list("📉 Cursos com Menor Evasão", "#006633", menor_ev, is_pct=True), unsafe_allow_html=True)
                
                with t2:
                    t_curso = df_acad.groupby(['Curso_Modalidade', 'Situacao_Matricula'])['Tempo'].mean().reset_index()
                    ev = t_curso[t_curso['Situacao_Matricula'].str.upper() == 'EVADIDO'].sort_values('Tempo', ascending=False).head(3)
                    co = t_curso[t_curso['Situacao_Matricula'].str.upper() == 'CONCLUÍDO'].sort_values('Tempo', ascending=False).head(3)
                    
                    maior_t_ev = dict(zip(ev['Curso_Modalidade'], ev['Tempo']))
                    maior_t_co = dict(zip(co['Curso_Modalidade'], co['Tempo']))
                    
                    st.markdown(create_card_list("⏳ Maiores Médias de Tempo (Evadidos)", "#E53935", maior_t_ev, is_pct=False), unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(create_card_list("🎓 Maiores Médias de Tempo (Concluídos)", "#006633", maior_t_co, is_pct=False), unsafe_allow_html=True)

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📈 VISÃO GRÁFICA</p>", unsafe_allow_html=True)

                is_pct_mode = modo_vis_acad == 'Valor em %'
                
                def render_bar_chart(df, x_col, y_col, color_col, title, y_title, is_pct=False, height=380, casas_dec=1):
                    st.markdown(f"**{title}**")
                    
                    df_plot = df.copy()
                    dec_casas = casas_dec if (is_pct or casas_dec > 0) else 0
                    df_plot['Valor_Txt'] = df_plot[y_col].apply(lambda x: fmt_br(x, dec_casas) + ("%" if is_pct else ""))
                    
                    max_val = df_plot[y_col].max() if not df_plot.empty else 1
                    escala_max = max(1.0, float(max_val) * 1.35) if pd.notnull(max_val) and max_val > 0 else 1.0

                    x_axis = alt.Axis(labelAngle=-90, grid=True, gridColor='#EAEAEA', title='Ciclo')
                    
                    if is_pct:
                        y_axis = alt.Axis(title=y_title, format=',.1f', labelExpr="replace(datum.label, ',', '.')")
                    else:
                        y_axis = alt.Axis(title=y_title, format=',d', labelExpr="replace(datum.label, ',', '.')")
                    
                    x_kwargs = {'title': 'Ciclo', 'axis': x_axis}
                    y_kwargs = {'title': y_title, 'axis': y_axis, 'scale': alt.Scale(domain=[0, escala_max])}

                    if color_col:
                        chart = alt.Chart(df_plot).mark_bar().encode(
                            x=alt.X(f'{x_col}:O', **x_kwargs),
                            y=alt.Y(f'{y_col}:Q', **y_kwargs),
                            color=alt.Color(f'{color_col}:N', legend=alt.Legend(orient='bottom', title=None)),
                            xOffset=f'{color_col}:N',
                            tooltip=[f'{x_col}:O', f'{color_col}:N', 'Valor_Txt:N']
                        )
                        text = alt.Chart(df_plot).mark_text(
                            align='left', baseline='middle', dx=5, angle=270, fontSize=10, fontWeight='bold'
                        ).encode(
                            x=alt.X(f'{x_col}:O', **x_kwargs),
                            y=alt.Y(f'{y_col}:Q', **y_kwargs),
                            xOffset=f'{color_col}:N',
                            text='Valor_Txt:N'
                        )
                        final_chart = chart + text
                    else:
                        chart = alt.Chart(df_plot).mark_bar(color='#006633').encode(
                            x=alt.X(f'{x_col}:O', **x_kwargs),
                            y=alt.Y(f'{y_col}:Q', **y_kwargs),
                            tooltip=[f'{x_col}:O', 'Valor_Txt:N']
                        )
                        text = alt.Chart(df_plot).mark_text(
                            align='left', baseline='middle', dx=5, angle=270, fontSize=10, fontWeight='bold'
                        ).encode(
                            x=alt.X(f'{x_col}:O', **x_kwargs),
                            y=alt.Y(f'{y_col}:Q', **y_kwargs),
                            text='Valor_Txt:N'
                        )
                        final_chart = chart + text
                    
                    st.altair_chart(final_chart.properties(height=height).interactive(), width="stretch")

                df_acum = df_acad.groupby('Semestre_Letivo_Inicial').size().reset_index(name='Total')
                df_acum['Acumulado'] = df_acum['Total'].cumsum()
                render_bar_chart(df_acum, 'Semestre_Letivo_Inicial', 'Acumulado', None, 
                                 "1. Evolução de Matrículas Acumuladas", "Total Acumulado", is_pct=False, casas_dec=0)

                df_sit_chart = df_acad.groupby(['Semestre_Letivo_Inicial', 'Situacao_Matricula']).size().reset_index(name='Qtd')
                if is_pct_mode:
                    df_sit_totals = df_acad.groupby('Semestre_Letivo_Inicial').size().reset_index(name='Tot')
                    df_sit_chart = df_sit_chart.merge(df_sit_totals, on='Semestre_Letivo_Inicial')
                    df_sit_chart['Valor'] = (df_sit_chart['Qtd'] / df_sit_chart['Tot']) * 100
                else:
                    df_sit_chart['Valor'] = df_sit_chart['Qtd']

                render_bar_chart(df_sit_chart, 'Semestre_Letivo_Inicial', 'Valor', 'Situacao_Matricula', 
                                 "2. Situação de Matrícula por Ciclo", "Proporção (%)" if is_pct_mode else "Quantidade", is_pct=is_pct_mode, casas_dec=1 if is_pct_mode else 0)

                df_form_chart = df_acad.groupby(['Semestre_Letivo_Inicial', 'Forma_Ingresso']).size().reset_index(name='Qtd')
                if is_pct_mode:
                    df_form_totals = df_acad.groupby('Semestre_Letivo_Inicial').size().reset_index(name='Tot')
                    df_form_chart = df_form_chart.merge(df_form_totals, on='Semestre_Letivo_Inicial')
                    df_form_chart['Valor'] = (df_form_chart['Qtd'] / df_form_chart['Tot']) * 100
                else:
                    df_form_chart['Valor'] = df_form_chart['Qtd']

                render_bar_chart(df_form_chart, 'Semestre_Letivo_Inicial', 'Valor', 'Forma_Ingresso', 
                                 "3. Forma de Ingresso por Ciclo", "Proporção (%)" if is_pct_mode else "Quantidade", is_pct=is_pct_mode, casas_dec=1 if is_pct_mode else 0)

                df_sex_chart = df_acad.groupby(['Semestre_Letivo_Inicial', 'Sexo']).size().reset_index(name='Qtd')
                if is_pct_mode:
                    df_sex_totals = df_acad.groupby('Semestre_Letivo_Inicial').size().reset_index(name='Tot')
                    df_sex_chart = df_sex_chart.merge(df_sex_totals, on='Semestre_Letivo_Inicial')
                    df_sex_chart['Valor'] = (df_sex_chart['Qtd'] / df_sex_chart['Tot']) * 100
                else:
                    df_sex_chart['Valor'] = df_sex_chart['Qtd']

                render_bar_chart(df_sex_chart, 'Semestre_Letivo_Inicial', 'Valor', 'Sexo', 
                                 "4. Distribuição por Sexo por Ciclo", "Proporção (%)" if is_pct_mode else "Quantidade", is_pct=is_pct_mode, casas_dec=1 if is_pct_mode else 0)
                
                if estagio_col:
                    df_est_chart = df_acad[
                        (df_acad[estagio_col].astype(str).str.upper() == 'SIM') & 
                        (df_acad['Situacao_Matricula'].str.upper().isin(['EVADIDO', 'CONCLUÍDO']))
                    ].groupby(['Semestre_Letivo_Inicial', 'Situacao_Matricula']).size().reset_index(name='Qtd')
                    
                    if not df_est_chart.empty:
                        if is_pct_mode:
                            df_est_tot = df_acad[df_acad[estagio_col].astype(str).str.upper() == 'SIM'].groupby('Semestre_Letivo_Inicial').size().reset_index(name='Tot')
                            df_est_chart = df_est_chart.merge(df_est_tot, on='Semestre_Letivo_Inicial')
                            df_est_chart['Valor'] = (df_est_chart['Qtd'] / df_est_chart['Tot']) * 100
                        else:
                            df_est_chart['Valor'] = df_est_chart['Qtd']
                            
                        render_bar_chart(df_est_chart, 'Semestre_Letivo_Inicial', 'Valor', 'Situacao_Matricula', 
                                          "5. Fizeram Estágio (Evadidos vs Concluídos)", "Proporção (%)" if is_pct_mode else "Quantidade", is_pct=is_pct_mode, casas_dec=1 if is_pct_mode else 0)
                
                df_tmp_chart = df_acad[df_acad['Situacao_Matricula'].str.upper().isin(['EVADIDO', 'CONCLUÍDO'])]
                if not df_tmp_chart.empty:
                    df_tmp_agg = df_tmp_chart.groupby(['Semestre_Letivo_Inicial', 'Situacao_Matricula'])['Tempo'].mean().reset_index(name='Tempo_Medio')
                    render_bar_chart(df_tmp_agg, 'Semestre_Letivo_Inicial', 'Tempo_Medio', 'Situacao_Matricula', 
                                     "6. Tempo Médio (Evadidos vs Concluídos)", "Tempo (Anos)", is_pct=False, casas_dec=1)

                st.markdown("<hr style='margin: 30px 0 10px 0;'>", unsafe_allow_html=True)
                
                # MATRIZ DE ASSOCIAÇÃO (ANTES DA TABELA)
                render_heatmap_sit(df_acad, "Situação de Matrícula x Perfis Discentes e Tempo (Ciclo)")
                
                st.markdown("<br>", unsafe_allow_html=True)

                with st.expander("📊 Consultar Tabela Geral - Situação da Matrícula Acadêmica (Ciclo)", expanded=True):
                    try:
                        pivot = df_acad.pivot_table(
                            index=['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'],
                            columns='Situacao_Matricula',
                            values='Cod_Matricula',
                            aggfunc='count',
                            fill_value=0
                        ).reset_index()
                        
                        p_forma = df_acad.pivot_table(
                            index=['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'],
                            columns='Forma_Ingresso',
                            values='Cod_Matricula',
                            aggfunc='count',
                            fill_value=0
                        ).reset_index()
                        
                        p_sexo = df_acad.pivot_table(
                            index=['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'],
                            columns='Sexo',
                            values='Cod_Matricula',
                            aggfunc='count',
                            fill_value=0
                        ).reset_index()
                        
                        p_idade = df_acad.groupby(['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'])['Idade'].mean().reset_index(name='Idade_Média')
                        
                        p_tempo = df_acad[df_acad['Situacao_Matricula'].str.upper().isin(['EVADIDO', 'CONCLUÍDO'])].pivot_table(
                            index=['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'],
                            columns='Situacao_Matricula',
                            values='Tempo',
                            aggfunc='mean'
                        ).reset_index()
                        p_tempo.columns = [c + '_Tempo' if c in ['Evadido', 'Concluído'] else c for c in p_tempo.columns]
                        
                        p_cr = df_acad.groupby(['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'])['CR'].mean().reset_index(name='Média_CR')
                        
                        final_table = pivot.merge(p_forma, on=['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'], how='left')
                        final_table = final_table.merge(p_sexo, on=['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'], how='left')
                        final_table = final_table.merge(p_idade, on=['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'], how='left')
                        final_table = final_table.merge(p_tempo, on=['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'], how='left')
                        final_table = final_table.merge(p_cr, on=['Semestre_Letivo_Inicial', 'Descricao_Curso', 'Modalidade'], how='left')
                        
                        final_table = final_table.sort_values('Semestre_Letivo_Inicial', ascending=False)
                        
                        cols_float = [c for c in final_table.columns if 'Tempo' in c or 'Média' in c or 'Idade' in c]
                        for col in cols_float:
                            final_table[col] = final_table[col].apply(lambda x: fmt_br(x, 2) if pd.notnull(x) else "-")
                        
                        st.dataframe(final_table, width="stretch", hide_index=True)
                    except Exception as e:
                        st.error(f"Erro ao gerar a tabela consolidada: {e}")

        # SUB-ABA 2: SEMESTRE
        with subtab_semestre:
            if df_acad_full.empty:
                st.warning("Dados não encontrados.")
            else:
                st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA (SEMESTRE)</p>", unsafe_allow_html=True)
                
                for f_key in ['f_semestre_sem', 'f_mod_sem', 'f_curso_sem', 'f_sit_sem', 'f_forma_sem']:
                    if f_key not in st.session_state:
                        st.session_state[f_key] = []
                        
                def get_opts_acad_sem(col):
                    df_temp = df_acad_full.copy()
                    if col != 'Ultimo_Periodo_Letivo' and st.session_state.f_semestre_sem: df_temp = df_temp[df_temp['Ultimo_Periodo_Letivo'].isin(st.session_state.f_semestre_sem)]
                    if col != 'Modalidade' and st.session_state.f_mod_sem: df_temp = df_temp[df_temp['Modalidade'].isin(st.session_state.f_mod_sem)]
                    if col != 'Descricao_Curso' and st.session_state.f_curso_sem: df_temp = df_temp[df_temp['Descricao_Curso'].isin(st.session_state.f_curso_sem)]
                    if col != 'Situacao_Matricula' and st.session_state.f_sit_sem: df_temp = df_temp[df_temp['Situacao_Matricula'].isin(st.session_state.f_sit_sem)]
                    if col != 'Forma_Ingresso' and st.session_state.f_forma_sem: df_temp = df_temp[df_temp['Forma_Ingresso'].isin(st.session_state.f_forma_sem)]
                    
                    opts = sorted(list(df_temp[col].dropna().unique()))
                    if col == 'Ultimo_Periodo_Letivo':
                        opts = sorted(list(set(opts + st.session_state.f_semestre_sem)), reverse=True)
                    return opts
                    
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.session_state.f_semestre_sem = st.multiselect("Semestre", get_opts_acad_sem('Ultimo_Periodo_Letivo'), default=st.session_state.f_semestre_sem, placeholder="Todos", key="ms_sem_periodo")
                with col2:
                    st.session_state.f_mod_sem = st.multiselect("Modalidade", get_opts_acad_sem('Modalidade'), default=st.session_state.f_mod_sem, placeholder="Todas", key="ms_sem_mod")
                with col3:
                    st.session_state.f_curso_sem = st.multiselect("Curso", get_opts_acad_sem('Descricao_Curso'), default=st.session_state.f_curso_sem, placeholder="Todos", key="ms_sem_curso")
                with col4:
                    st.session_state.f_sit_sem = st.multiselect("Situação", get_opts_acad_sem('Situacao_Matricula'), default=st.session_state.f_sit_sem, placeholder="Todas", key="ms_sem_sit")
                with col5:
                    st.session_state.f_forma_sem = st.multiselect("Forma Ingresso", get_opts_acad_sem('Forma_Ingresso'), default=st.session_state.f_forma_sem, placeholder="Todas", key="ms_sem_forma")

                df_base_sem_full = df_acad_full.copy()
                if st.session_state.f_mod_sem: df_base_sem_full = df_base_sem_full[df_base_sem_full['Modalidade'].isin(st.session_state.f_mod_sem)]
                if st.session_state.f_curso_sem: df_base_sem_full = df_base_sem_full[df_base_sem_full['Descricao_Curso'].isin(st.session_state.f_curso_sem)]
                if st.session_state.f_sit_sem: df_base_sem_full = df_base_sem_full[df_base_sem_full['Situacao_Matricula'].isin(st.session_state.f_sit_sem)]
                if st.session_state.f_forma_sem: df_base_sem_full = df_base_sem_full[df_base_sem_full['Forma_Ingresso'].isin(st.session_state.f_forma_sem)]

                semestres_disponiveis = get_opts_acad_sem('Ultimo_Periodo_Letivo')
                semestres_foco = st.session_state.f_semestre_sem if st.session_state.f_semestre_sem else semestres_disponiveis

                df_base_sem = df_base_sem_full[
                    (df_base_sem_full['Ultimo_Periodo_Letivo'].isin(semestres_foco)) & 
                    (df_base_sem_full['Situacao_Matricula'].str.upper().isin(['EVADIDO', 'CONCLUÍDO']))
                ].copy()

                min_sem_foco = min(semestres_foco) if semestres_foco else ""
                df_populacao_acumulada = df_base_sem_full[df_base_sem_full['Ultimo_Periodo_Letivo'] >= min_sem_foco] if min_sem_foco else df_base_sem_full

                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                
                modo_vis_sem = st.radio(
                    "Modo de Exibição dos Indicadores:",
                    ["Valor Absoluto", "Valor em %"],
                    horizontal=True,
                    key="radio_modo_vis_sem"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                def format_val_sem(val, total, is_money=False):
                    if pd.isna(val): return "-"
                    if modo_vis_sem == "Valor em %" and not is_money:
                        pct = (val / total * 100) if total > 0 else 0
                        return fmt_br(pct, 1) + "%"
                    else:
                        if isinstance(val, float):
                            return fmt_br(val, 1)
                        return fmt_br(val, 0)

                tot_populacao_base = len(df_populacao_acumulada)
                tot_ingressantes = len(df_base_sem_full[df_base_sem_full['Semestre_Letivo_Inicial'].isin(semestres_foco)])

                estagio_col = 'Fez_Estágio' if 'Fez_Estágio' in df_base_sem.columns else ('Fez_Estagio' if 'Fez_Estagio' in df_base_sem.columns else None)
                df_est_total_sem = df_base_sem[df_base_sem[estagio_col].astype(str).str.upper() == 'SIM'] if estagio_col else pd.DataFrame()
                tot_estagio_sem = len(df_est_total_sem)
                evad_estagio_sem = len(df_est_total_sem[df_est_total_sem['Situacao_Matricula'].str.upper() == 'EVADIDO'])
                concl_estagio_sem = len(df_est_total_sem[df_est_total_sem['Situacao_Matricula'].str.upper() == 'CONCLUÍDO'])

                card_style = "<div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 12px 5px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; height: 100%;'><p style='color: #666; font-size: 0.85rem; margin-bottom: 6px; font-weight: bold;'>{title}</p>{main_val}{subtitle}</div>"

                cs1, cs2, cs3 = st.columns(3)
                cs1.markdown(card_style.format(title="Ingressantes", main_val=f"<h2 style='color: #006633; margin: 5px 0; font-size: 1.4rem;'>{fmt_br(tot_ingressantes, 0)}</h2>", subtitle=""), unsafe_allow_html=True)

                if not df_base_sem.empty:
                    sit_counts_sem = df_base_sem['Situacao_Matricula'].value_counts()
                    sit_txt_sem = "".join([f"<p style='margin: 2px 0; font-size: 0.78rem; color: #444;'><strong>{k}:</strong> {format_val_sem(v, tot_populacao_base)}</p>" for k, v in sit_counts_sem.items()])
                else:
                    sit_txt_sem = "-"
                cs2.markdown(card_style.format(title="Situação Matrícula", main_val="", subtitle=sit_txt_sem), unsafe_allow_html=True)

                cs3.markdown(card_style.format(title="Fizeram Estágio", main_val=f"<h2 style='color: #006633; margin: 2px 0; font-size: 1.2rem;'>{format_val_sem(tot_estagio_sem, tot_populacao_base)}</h2>", subtitle=f"<p style='margin: 2px 0; font-size: 0.72rem; color: #444;'>Evadidos: {format_val_sem(evad_estagio_sem, tot_estagio_sem)}<br>Concluídos: {format_val_sem(concl_estagio_sem, tot_estagio_sem)}</p>"), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                if not df_base_sem.empty and not df_populacao_acumulada.empty:
                    tot_curso_pop = df_populacao_acumulada.groupby('Curso_Modalidade').size().reset_index(name='Total_Alunos')
                    evad_curso_sem = df_base_sem[df_base_sem['Situacao_Matricula'].str.upper() == 'EVADIDO'].groupby('Curso_Modalidade').size().reset_index(name='Evadidos')
                    
                    evasao_df_sem = tot_curso_pop.merge(evad_curso_sem, on='Curso_Modalidade', how='left').fillna(0)
                    evasao_df_sem['Taxa_Evasao'] = (evasao_df_sem['Evadidos'] / evasao_df_sem['Total_Alunos']).fillna(0)
                    
                    df_maior_ev_sem = evasao_df_sem[evasao_df_sem['Taxa_Evasao'] > 0].sort_values('Taxa_Evasao', ascending=False).head(3)
                    maior_ev_sem = dict(zip(df_maior_ev_sem['Curso_Modalidade'], df_maior_ev_sem['Taxa_Evasao']))
                    
                    df_menor_ev_sem = evasao_df_sem[evasao_df_sem['Taxa_Evasao'] > 0].sort_values('Taxa_Evasao', ascending=True).head(3)
                    menor_ev_sem = dict(zip(df_menor_ev_sem['Curso_Modalidade'], df_menor_ev_sem['Taxa_Evasao']))
                else:
                    maior_ev_sem, menor_ev_sem = {}, {}

                ts1, ts2 = st.columns(2)
                with ts1:
                    st.markdown(create_card_list("📈 Cursos com Maior Evasão", "#E53935", maior_ev_sem, is_pct=True), unsafe_allow_html=True)
                with ts2:
                    st.markdown(create_card_list("📉 Cursos com Menor Evasão", "#006633", menor_ev_sem, is_pct=True), unsafe_allow_html=True)

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📈 VISÃO GRÁFICA (SEMESTRE)</p>", unsafe_allow_html=True)

                is_pct_mode_sem = modo_vis_sem == 'Valor em %'

                def render_bar_chart_sem(df, x_col, y_col, color_col, title, y_title, x_title='Semestre', is_pct=False, height=380, casas_dec=1):
                    st.markdown(f"**{title}**")
                    
                    df_plot = df.copy()
                    dec_casas = casas_dec if (is_pct or casas_dec > 0) else 0
                    df_plot['Valor_Txt'] = df_plot[y_col].apply(lambda x: fmt_br(x, dec_casas) + ("%" if is_pct else ""))
                    
                    max_val = df_plot[y_col].max() if not df_plot.empty else 1
                    escala_max = max(1.0, float(max_val) * 1.35) if pd.notnull(max_val) and max_val > 0 else 1.0

                    x_axis = alt.Axis(labelAngle=-90, grid=True, gridColor='#EAEAEA', title=x_title)
                    
                    if is_pct:
                        y_axis = alt.Axis(title=y_title, format=',.1f', labelExpr="replace(datum.label, ',', '.')")
                    else:
                        y_axis = alt.Axis(title=y_title, format=',d', labelExpr="replace(datum.label, ',', '.')")
                    
                    x_kwargs = {'title': x_title, 'axis': x_axis}
                    y_kwargs = {'title': y_title, 'axis': y_axis, 'scale': alt.Scale(domain=[0, escala_max])}

                    if color_col:
                        chart = alt.Chart(df_plot).mark_bar().encode(
                            x=alt.X(f'{x_col}:O', **x_kwargs),
                            y=alt.Y(f'{y_col}:Q', **y_kwargs),
                            color=alt.Color(f'{color_col}:N', legend=alt.Legend(orient='bottom', title=None)),
                            xOffset=f'{color_col}:N',
                            tooltip=[f'{x_col}:O', f'{color_col}:N', 'Valor_Txt:N']
                        )
                        text = alt.Chart(df_plot).mark_text(
                            align='left', baseline='middle', dx=5, angle=270, fontSize=10, fontWeight='bold'
                        ).encode(
                            x=alt.X(f'{x_col}:O', **x_kwargs),
                            y=alt.Y(f'{y_col}:Q', **y_kwargs),
                            xOffset=f'{color_col}:N',
                            text='Valor_Txt:N'
                        )
                        final_chart = chart + text
                    else:
                        chart = alt.Chart(df_plot).mark_bar(color='#006633').encode(
                            x=alt.X(f'{x_col}:O', **x_kwargs),
                            y=alt.Y(f'{y_col}:Q', **y_kwargs),
                            tooltip=[f'{x_col}:O', 'Valor_Txt:N']
                        )
                        text = alt.Chart(df_plot).mark_text(
                            align='left', baseline='middle', dx=5, angle=270, fontSize=10, fontWeight='bold'
                        ).encode(
                            x=alt.X(f'{x_col}:O', **x_kwargs),
                            y=alt.Y(f'{y_col}:Q', **y_kwargs),
                            text='Valor_Txt:N'
                        )
                        final_chart = chart + text
                    
                    st.altair_chart(final_chart.properties(height=height).interactive(), width="stretch")

                if not df_base_sem.empty:
                    df_sit_chart_sem = df_base_sem.groupby(['Ultimo_Periodo_Letivo', 'Situacao_Matricula']).size().reset_index(name='Qtd')
                    df_sit_chart_sem.rename(columns={'Ultimo_Periodo_Letivo': 'Semestre'}, inplace=True)
                    
                    if is_pct_mode_sem:
                        tot_sem_acum = df_base_sem_full.groupby('Ultimo_Periodo_Letivo').size().reset_index(name='Tot_Sem')
                        tot_sem_acum['Tot_Acum'] = tot_sem_acum.sort_values('Ultimo_Periodo_Letivo', ascending=False)['Tot_Sem'].cumsum()
                        tot_sem_acum.rename(columns={'Ultimo_Periodo_Letivo': 'Semestre'}, inplace=True)
                        
                        df_sit_chart_sem = df_sit_chart_sem.merge(tot_sem_acum[['Semestre', 'Tot_Acum']], on='Semestre', how='left')
                        df_sit_chart_sem['Valor'] = (df_sit_chart_sem['Qtd'] / df_sit_chart_sem['Tot_Acum']) * 100
                    else:
                        df_sit_chart_sem['Valor'] = df_sit_chart_sem['Qtd']

                    render_bar_chart_sem(df_sit_chart_sem, 'Semestre', 'Valor', 'Situacao_Matricula', 
                                         "1. Situação de Matrícula por Semestre", "Proporção (%)" if is_pct_mode_sem else "Quantidade", x_title='Semestre', is_pct=is_pct_mode_sem, casas_dec=1 if is_pct_mode_sem else 0)

                if estagio_col and not df_base_sem.empty:
                    df_est_sem = df_base_sem[df_base_sem[estagio_col].astype(str).str.upper() == 'SIM'].groupby(['Ultimo_Periodo_Letivo', 'Situacao_Matricula']).size().reset_index(name='Qtd')
                    
                    if not df_est_sem.empty:
                        df_est_sem.rename(columns={'Ultimo_Periodo_Letivo': 'Semestre'}, inplace=True)
                        if is_pct_mode_sem:
                            tot_est_sem = df_base_sem[df_base_sem[estagio_col].astype(str).str.upper() == 'SIM'].groupby('Ultimo_Periodo_Letivo').size().reset_index(name='Tot_Est')
                            tot_est_sem.rename(columns={'Ultimo_Periodo_Letivo': 'Semestre'}, inplace=True)
                            df_est_sem = df_est_sem.merge(tot_est_sem, on='Semestre', how='left')
                            df_est_sem['Valor'] = (df_est_sem['Qtd'] / df_est_sem['Tot_Est']) * 100
                        else:
                            df_est_sem['Valor'] = df_est_sem['Qtd']

                        render_bar_chart_sem(df_est_sem, 'Semestre', 'Valor', 'Situacao_Matricula', 
                                             "2. Fizeram Estágio (Evadidos vs Concluídos)", "Proporção (%)" if is_pct_mode_sem else "Quantidade", x_title='Semestre', is_pct=is_pct_mode_sem, casas_dec=1 if is_pct_mode_sem else 0)

                st.markdown("<hr style='margin: 30px 0 10px 0;'>", unsafe_allow_html=True)

                # MATRIZ DE ASSOCIAÇÃO (SEMESTRE)
                render_heatmap_sit(df_base_sem_full, "Situação de Matrícula x Perfis Discentes e Tempo (Semestre)")
                
                st.markdown("<br>", unsafe_allow_html=True)

                with st.expander("📊 Consultar Tabela Geral - Situação da Matrícula Acadêmica (Semestre)", expanded=True):
                    try:
                        if not df_base_sem.empty:
                            pivot_sem = df_base_sem.pivot_table(
                                index=['Ultimo_Periodo_Letivo', 'Descricao_Curso', 'Modalidade'],
                                columns='Situacao_Matricula',
                                values='Cod_Matricula',
                                aggfunc='count',
                                fill_value=0
                            ).reset_index()

                            final_table_sem = pivot_sem.rename(columns={'Ultimo_Periodo_Letivo': 'Semestre'}).sort_values('Semestre', ascending=False)
                            st.dataframe(final_table_sem, width="stretch", hide_index=True)
                        else:
                            st.info("Nenhum dado encontrado para a consulta da tabela.")
                    except Exception as e:
                        st.error(f"Erro ao gerar a tabela consolidada do semestre: {e}")

    # ==========================================
    # TAB 2: QUANTIDADE DE REPROVAÇÕES
    # ==========================================
    with tab2:
        st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA (QUANTIDADE DE REPROVAÇÕES)</p>", unsafe_allow_html=True)
        
        import unicodedata

        def strip_accents_rep(text):
            if not isinstance(text, str):
                return text
            return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

        @st.cache_data
        def load_rep_data():
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, 'CI_Rep.csv')
            try:
                df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(csv_path, sep=';', encoding='latin1')
            
            if 'Quantidade_Reprovacoes' in df.columns:
                df['Quantidade_Reprovacoes'] = pd.to_numeric(df['Quantidade_Reprovacoes'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce').fillna(0).astype(int)
            
            if 'Desc_Disciplina' in df.columns and 'Desc_Curso' in df.columns and 'Modalidade' in df.columns:
                df['Disc_Curso_Mod'] = df['Desc_Disciplina'].fillna('') + ' - ' + df['Desc_Curso'].fillna('') + ' - ' + df['Modalidade'].fillna('')
            
            def categorizar_rep(qtd):
                if qtd == 1: return "1 Reprovação"
                elif qtd == 2: return "2 Reprovações"
                elif qtd == 3: return "3 Reprovações"
                elif qtd >= 4: return ">= 4 Reprovações"
                return "0 Reprovações"

            df['Faixa_Reprovacao'] = df['Quantidade_Reprovacoes'].apply(categorizar_rep)
            return df

        df_rep_full = load_rep_data()

        if df_rep_full.empty:
            st.warning("Dados de reprovações não encontrados no arquivo CI_Rep.csv.")
        else:
            for f_key in ['f_mod_rep', 'f_curso_rep', 'f_disc_rep', 'f_sit_rep', 'f_forma_rep']:
                if f_key not in st.session_state:
                    st.session_state[f_key] = []

            def get_opts_rep(col):
                df_temp = df_rep_full.copy()
                if col != 'Modalidade' and st.session_state.f_mod_rep:
                    df_temp = df_temp[df_temp['Modalidade'].isin(st.session_state.f_mod_rep)]
                if col != 'Desc_Curso' and st.session_state.f_curso_rep:
                    df_temp = df_temp[df_temp['Desc_Curso'].isin(st.session_state.f_curso_rep)]
                if col != 'Desc_Disciplina' and st.session_state.f_disc_rep:
                    df_temp = df_temp[df_temp['Desc_Disciplina'].isin(st.session_state.f_disc_rep)]
                if col != 'Situacao_Matricula' and st.session_state.f_sit_rep:
                    df_temp = df_temp[df_temp['Situacao_Matricula'].isin(st.session_state.f_sit_rep)]
                if col != 'Forma_Ingresso' and st.session_state.f_forma_rep:
                    df_temp = df_temp[df_temp['Forma_Ingresso'].isin(st.session_state.f_forma_rep)]
                
                opts = list(df_temp[col].dropna().unique())
                opts = sorted(opts, key=lambda x: strip_accents_rep(str(x)).lower())
                return opts

            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.session_state.f_mod_rep = st.multiselect("Modalidade", get_opts_rep('Modalidade'), default=st.session_state.f_mod_rep, placeholder="Todas", key="ms_rep_mod")
            with c2:
                st.session_state.f_curso_rep = st.multiselect("Curso", get_opts_rep('Desc_Curso'), default=st.session_state.f_curso_rep, placeholder="Todos", key="ms_rep_curso")
            with c3:
                st.session_state.f_disc_rep = st.multiselect("Disciplina", get_opts_rep('Desc_Disciplina'), default=st.session_state.f_disc_rep, placeholder="Todas", key="ms_rep_disc")
            with c4:
                st.session_state.f_sit_rep = st.multiselect("Situação Matrícula", get_opts_rep('Situacao_Matricula'), default=st.session_state.f_sit_rep, placeholder="Todas", key="ms_rep_sit")
            with c5:
                st.session_state.f_forma_rep = st.multiselect("Forma Ingresso", get_opts_rep('Forma_Ingresso'), default=st.session_state.f_forma_rep, placeholder="Todas", key="ms_rep_forma")

            df_rep = df_rep_full.copy()
            if st.session_state.f_mod_rep: df_rep = df_rep[df_rep['Modalidade'].isin(st.session_state.f_mod_rep)]
            if st.session_state.f_curso_rep: df_rep = df_rep[df_rep['Desc_Curso'].isin(st.session_state.f_curso_rep)]
            if st.session_state.f_disc_rep: df_rep = df_rep[df_rep['Desc_Disciplina'].isin(st.session_state.f_disc_rep)]
            if st.session_state.f_sit_rep: df_rep = df_rep[df_rep['Situacao_Matricula'].isin(st.session_state.f_sit_rep)]
            if st.session_state.f_forma_rep: df_rep = df_rep[df_rep['Forma_Ingresso'].isin(st.session_state.f_forma_rep)]

            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

            modo_vis_rep = st.radio(
                "Modo de Exibição dos Indicadores:",
                ["Valor Absoluto", "Valor em %"],
                horizontal=True,
                key="radio_modo_vis_rep"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            tot_registros_rep = len(df_rep)

            def fmt_rep_val(val, total):
                if pd.isna(val): return "-"
                if modo_vis_rep == "Valor em %":
                    pct = (val / total * 100) if total > 0 else 0
                    return fmt_br(pct, 1) + "%"
                else:
                    return fmt_br(val, 0)

            faixas = ["1 Reprovação", "2 Reprovações", "3 Reprovações", ">= 4 Reprovações"]
            card_style_rep = "<div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 12px 8px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 100%;'><p style='color: #666; font-size: 0.85rem; margin-bottom: 4px; font-weight: bold;'>{title}</p><h2 style='color: #006633; margin: 2px 0; font-size: 1.3rem;'>{main_val}</h2>{details}</div>"

            cols_cards = st.columns(5)
            for idx, fx in enumerate(faixas):
                df_fx = df_rep[df_rep['Faixa_Reprovacao'] == fx]
                qtd_fx = len(df_fx)
                
                fi_counts = df_fx['Forma_Ingresso'].value_counts().head(2)
                sit_counts = df_fx['Situacao_Matricula'].value_counts().head(2)
                
                det_html = "<div style='text-align: left; font-size: 0.72rem; color: #444; margin-top: 6px; border-top: 1px solid #eee; padding-top: 4px;'>"
                det_html += "<strong>Ingresso:</strong><br>" + "".join([f"• {k}: {fmt_rep_val(v, qtd_fx)}<br>" for k, v in fi_counts.items()])
                det_html += "<strong>Situação:</strong><br>" + "".join([f"• {k}: {fmt_rep_val(v, qtd_fx)}<br>" for k, v in sit_counts.items()])
                det_html += "</div>"
                
                cols_cards[idx].markdown(card_style_rep.format(title=fx, main_val=fmt_rep_val(qtd_fx, tot_registros_rep), details=det_html), unsafe_allow_html=True)

            max_rep_val = df_rep['Quantidade_Reprovacoes'].max() if not df_rep.empty else 0
            df_max_rep = df_rep[df_rep['Quantidade_Reprovacoes'] == max_rep_val] if max_rep_val > 0 else pd.DataFrame()
            qtd_max_rep = len(df_max_rep)

            if not df_max_rep.empty:
                fi_max_counts = df_max_rep['Forma_Ingresso'].value_counts().head(2)
                sit_max_counts = df_max_rep['Situacao_Matricula'].value_counts().head(2)
                det_max_html = "<div style='text-align: left; font-size: 0.72rem; color: #444; margin-top: 6px; border-top: 1px solid #eee; padding-top: 4px;'>"
                det_max_html += "<strong>Ingresso:</strong><br>" + "".join([f"• {k}: {fmt_rep_val(v, qtd_max_rep)}<br>" for k, v in fi_max_counts.items()])
                det_max_html += "<strong>Situação:</strong><br>" + "".join([f"• {k}: {fmt_rep_val(v, qtd_max_rep)}<br>" for k, v in sit_max_counts.items()])
                det_max_html += "</div>"
            else:
                det_max_html = "<p style='font-size: 0.75rem; color: #666; margin-top: 10px;'>Sem dados.</p>"

            cols_cards[4].markdown(card_style_rep.format(
                title="Maior Reprovação", 
                main_val=f"{max_rep_val}x", 
                details=det_max_html
            ), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            def create_card_list_rep(title, color, items_data):
                items_html = ""
                for item in items_data:
                    nome_clean = str(item['nome']).replace('<', '&lt;').replace('>', '&gt;')
                    sub_txt = f" <span style='font-size: 0.75rem; color: #666;'>({item['sub_val']})</span>" if 'sub_val' in item and item['sub_val'] else ""
                    items_html += f"<li style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.85rem; color: #333;'><span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 75%;' title='{nome_clean}'>• {nome_clean}</span><strong style='color: {color};'>{item['val_str']}{sub_txt}</strong></li>"
                return f"<div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 12px 15px; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 100%; margin-bottom: 15px;'><p style='color: {color}; font-size: 0.95rem; margin-bottom: 8px; font-weight: bold; text-align: center;'>{title}</p><ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>{items_html}</ul></div>"

            # ==========================================
            # MONTAGEM DOS CARDS TOP POR FAIXA DE REPROVAÇÃO
            # ==========================================
            r1_c1, r1_c2 = st.columns(2)
            r2_c1, r2_c2 = st.columns(2)
            grid_cols = [r1_c1, r1_c2, r2_c1, r2_c2]

            for idx, fx in enumerate(faixas):
                df_fx_list = df_rep[df_rep['Faixa_Reprovacao'] == fx]
                
                # Agrupa por disciplina e conta a quantidade de alunos únicos (Cod_Matricula)
                top_disc_fx = (
                    df_fx_list.groupby('Disc_Curso_Mod')['Cod_Matricula']
                    .nunique()
                    .reset_index(name='Qtd_Alunos')
                    .sort_values('Qtd_Alunos', ascending=False)
                    .head(3)
                )
                
                # Formata a string para exibir o total de alunos
                items_fx = [
                    {
                        'nome': r['Disc_Curso_Mod'], 
                        'val_str': f"{fmt_br(r['Qtd_Alunos'], 0)} alunos"
                    } 
                    for _, r in top_disc_fx.iterrows()
                ]
                
                grid_cols[idx].markdown(
                    create_card_list_rep(f"Top {fx}", "#E53935", items_fx), 
                    unsafe_allow_html=True
                )

            if not df_rep.empty:
                df_max_disc_group = df_rep.groupby('Disc_Curso_Mod').agg(
                    Max_Rep=('Quantidade_Reprovacoes', 'max')
                ).reset_index().sort_values('Max_Rep', ascending=False).head(3)

                items_max = []
                for _, r in df_max_disc_group.iterrows():
                    d_nome = r['Disc_Curso_Mod']
                    m_val = r['Max_Rep']
                    qtd_al_unicos = df_rep[(df_rep['Disc_Curso_Mod'] == d_nome) & (df_rep['Quantidade_Reprovacoes'] == m_val)]['Cod_Matricula'].nunique()
                    items_max.append({
                        'nome': d_nome, 
                        'val_str': f"{m_val}x", 
                        'sub_val': f"{fmt_br(qtd_al_unicos, 0)} alunos"
                    })
            else:
                items_max = []

            st.markdown(create_card_list_rep("🏆 Disciplinas com Maior Quantidade de Reprovações (Pontual por Aluno)", "#006633", items_max), unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📈 VISÃO GRÁFICA (REPROVAÇÕES)</p>", unsafe_allow_html=True)

            is_pct_rep = modo_vis_rep == "Valor em %"

            st.markdown("**1. Faixas de Reprovação por Forma de Ingresso**")
            if not df_rep.empty:
                df_g1 = df_rep.groupby(['Forma_Ingresso', 'Faixa_Reprovacao']).size().reset_index(name='Qtd')
                if is_pct_rep:
                    tot_fi = df_rep.groupby('Forma_Ingresso').size().reset_index(name='Tot')
                    df_g1 = df_g1.merge(tot_fi, on='Forma_Ingresso')
                    df_g1['Valor'] = (df_g1['Qtd'] / df_g1['Tot'] * 100).fillna(0)
                else:
                    df_g1['Valor'] = df_g1['Qtd']

                df_g1['Valor_Txt'] = df_g1['Valor'].apply(lambda x: fmt_br(x, 1 if is_pct_rep else 0) + ("%" if is_pct_rep else ""))
                max_g1 = df_g1['Valor'].max() if not df_rep.empty else 1
                escala_g1 = max(1.0, float(max_g1) * 1.35)

                y_axis_g1 = alt.Axis(
                    title="Proporção (%)" if is_pct_rep else "Qtd Alunos",
                    labelExpr="replace(datum.label, ',', '.')"
                )

                c_g1 = alt.Chart(df_g1).mark_bar().encode(
                    x=alt.X('Forma_Ingresso:O', title='Forma de Ingresso', axis=alt.Axis(labelAngle=-90, grid=True)),
                    y=alt.Y('Valor:Q', title="Proporção (%)" if is_pct_rep else "Qtd Alunos", scale=alt.Scale(domain=[0, escala_g1]), axis=y_axis_g1),
                    color=alt.Color('Faixa_Reprovacao:N', legend=alt.Legend(orient='bottom', title=None)),
                    xOffset='Faixa_Reprovacao:N',
                    tooltip=['Forma_Ingresso:O', 'Faixa_Reprovacao:N', 'Valor_Txt:N']
                )
                t_g1 = alt.Chart(df_g1).mark_text(align='left', baseline='middle', dx=5, angle=270, fontSize=9, fontWeight='bold').encode(
                    x=alt.X('Forma_Ingresso:O'), y=alt.Y('Valor:Q'), xOffset='Faixa_Reprovacao:N', text='Valor_Txt:N'
                )
                st.altair_chart((c_g1 + t_g1).properties(height=360).interactive(), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**2. Faixas de Reprovação por Situação de Matrícula**")
            if not df_rep.empty:
                df_g2 = df_rep.groupby(['Situacao_Matricula', 'Faixa_Reprovacao']).size().reset_index(name='Qtd')
                if is_pct_rep:
                    tot_sit = df_rep.groupby('Situacao_Matricula').size().reset_index(name='Tot')
                    df_g2 = df_g2.merge(tot_sit, on='Situacao_Matricula')
                    df_g2['Valor'] = (df_g2['Qtd'] / df_g2['Tot'] * 100).fillna(0)
                else:
                    df_g2['Valor'] = df_g2['Qtd']

                df_g2['Valor_Txt'] = df_g2['Valor'].apply(lambda x: fmt_br(x, 1 if is_pct_rep else 0) + ("%" if is_pct_rep else ""))
                max_g2 = df_g2['Valor'].max() if not df_rep.empty else 1
                escala_g2 = max(1.0, float(max_g2) * 1.35)

                y_axis_g2 = alt.Axis(
                    title="Proporção (%)" if is_pct_rep else "Qtd Alunos",
                    labelExpr="replace(datum.label, ',', '.')"
                )

                c_g2 = alt.Chart(df_g2).mark_bar().encode(
                    x=alt.X('Situacao_Matricula:O', title='Situação da Matrícula', axis=alt.Axis(labelAngle=-90, grid=True)),
                    y=alt.Y('Valor:Q', title="Proporção (%)" if is_pct_rep else "Qtd Alunos", scale=alt.Scale(domain=[0, escala_g2]), axis=y_axis_g2),
                    color=alt.Color('Faixa_Reprovacao:N', legend=alt.Legend(orient='bottom', title=None)),
                    xOffset='Faixa_Reprovacao:N',
                    tooltip=['Situacao_Matricula:O', 'Faixa_Reprovacao:N', 'Valor_Txt:N']
                )
                t_g2 = alt.Chart(df_g2).mark_text(align='left', baseline='middle', dx=5, angle=270, fontSize=9, fontWeight='bold').encode(
                    x=alt.X('Situacao_Matricula:O'), y=alt.Y('Valor:Q'), xOffset='Faixa_Reprovacao:N', text='Valor_Txt:N'
                )
                st.altair_chart((c_g2 + t_g2).properties(height=360).interactive(), width="stretch")

            st.markdown("<hr style='margin: 30px 0 10px 0;'>", unsafe_allow_html=True)

            # MATRIZ DE ASSOCIAÇÃO (REPROVAÇÕES)
            st.markdown("**🔥 Matriz de Associação: Faixas de Reprovação x Ingressos e Situação**")
            if not df_rep.empty:
                df_temp_rep = df_rep.copy()
                blocos_rep = ['Forma_Ingresso', 'Situacao_Matricula']
                melted_rep = []
                order_labels_rep = []

                for cv in blocos_rep:
                    if cv in df_temp_rep.columns:
                        ct = pd.crosstab(df_temp_rep['Faixa_Reprovacao'], df_temp_rep[cv], normalize='index') * 100
                        for col_val in ct.columns:
                            rotulo_limpo = limpar_rotulo(col_val)
                            if rotulo_limpo not in order_labels_rep:
                                order_labels_rep.append(rotulo_limpo)
                            for row_val in ct.index:
                                melted_rep.append({
                                    'Faixa Reprovação': str(row_val),
                                    'Atributo': rotulo_limpo,
                                    'Proporção (%)': ct.loc[row_val, col_val]
                                })

                df_hm_rep = pd.DataFrame(melted_rep)
                df_hm_rep['Txt'] = df_hm_rep['Proporção (%)'].apply(lambda x: fmt_br(x, 1) + "%")
                
                chart_rep_hm = alt.Chart(df_hm_rep).mark_rect().encode(
                    x=alt.X('Atributo:O', title=None, sort=order_labels_rep, axis=alt.Axis(labelAngle=-90, labelFontSize=11)),
                    y=alt.Y('Faixa Reprovação:O', title='Faixa de Reprovação', sort=faixas),
                    color=alt.Color('Proporção (%):Q', scale=alt.Scale(scheme='reds'), legend=alt.Legend(title="Proporção %")),
                    tooltip=['Faixa Reprovação:N', 'Atributo:N', 'Txt:N']
                )
                text_rep_hm = chart_rep_hm.mark_text(baseline='middle', fontSize=10, fontWeight='bold').encode(
                    text='Txt:N',
                    color=alt.condition(alt.datum['Proporção (%)'] > 50, alt.value('white'), alt.value('black'))
                )
                st.altair_chart((chart_rep_hm + text_rep_hm).properties(height=300).interactive(), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            with st.expander("📊 Tabela Geral - Quantidade de Reprovações por Disciplina e Aluno", expanded=True):
                try:
                    if not df_rep.empty:
                        pivot_totais = df_rep.pivot_table(
                            index=['Modalidade', 'Desc_Curso', 'Desc_Disciplina'],
                            columns='Faixa_Reprovacao',
                            values='Cod_Matricula',
                            aggfunc='count',
                            fill_value=0
                        ).reset_index()

                        for fx in ["1 Reprovação", "2 Reprovações", "3 Reprovações", ">= 4 Reprovações"]:
                            if fx not in pivot_totais.columns:
                                pivot_totais[fx] = 0

                        pivot_totais.rename(columns={
                            '1 Reprovação': 'Total de 1 Reprovação',
                            '2 Reprovações': 'Total de 2 Reprovações',
                            '3 Reprovações': 'Total de 3 Reprovações',
                            '>= 4 Reprovações': 'Total de >= 4 Reprovações'
                        }, inplace=True)

                        cols_totais = ['Total de 1 Reprovação', 'Total de 2 Reprovações', 'Total de 3 Reprovações', 'Total de >= 4 Reprovações']

                        pivot_rep = df_rep.pivot_table(
                            index=['Modalidade', 'Desc_Curso', 'Desc_Disciplina'],
                            columns=['Faixa_Reprovacao', 'Situacao_Matricula', 'Forma_Ingresso'],
                            values='Cod_Matricula',
                            aggfunc='count',
                            fill_value=0
                        )

                        pivot_rep.columns = [f"{fx}\n({sit} - {forma})" for fx, sit, forma in pivot_rep.columns]
                        pivot_rep = pivot_rep.reset_index()

                        pivot_final = pivot_totais.merge(pivot_rep, on=['Modalidade', 'Desc_Curso', 'Desc_Disciplina'], how='left')

                        pivot_final['Disc_Sort'] = pivot_final['Desc_Disciplina'].apply(lambda x: strip_accents_rep(str(x)).lower())
                        
                        pivot_final = pivot_final.sort_values(
                            by=['Total de 1 Reprovação', 'Disc_Sort'],
                            ascending=[False, True]
                        ).drop(columns=['Disc_Sort'])

                        cols_base = ['Modalidade', 'Desc_Curso', 'Desc_Disciplina']
                        cols_detalhadase = [c for c in pivot_final.columns if c not in cols_base + cols_totais]
                        cols_ordem = cols_base + cols_totais + cols_detalhadase
                        pivot_final = pivot_final[cols_ordem]

                        if modo_vis_rep == "Valor em %":
                            tot_linha = pivot_final[cols_detalhadase].sum(axis=1)
                            for col in cols_totais:
                                pivot_final[col] = pivot_final.apply(lambda r: f"{fmt_br((r[col] / tot_linha[r.name] * 100), 1)}%" if tot_linha[r.name] > 0 else "0,0%", axis=1)

                            for col in cols_detalhadase:
                                pivot_final[col] = pivot_final.apply(lambda r: f"{fmt_br((r[col] / tot_linha[r.name] * 100), 1)}%" if tot_linha[r.name] > 0 else "0,0%", axis=1)
                        else:
                            for col in cols_totais + cols_detalhadase:
                                pivot_final[col] = pivot_final[col].apply(lambda x: fmt_br(x, 0))

                        st.dataframe(pivot_final, width="stretch", hide_index=True)
                    else:
                        st.info("Nenhum dado encontrado para gerar a tabela de reprovações.")
                except Exception as e:
                    st.error(f"Erro ao gerar a tabela consolidada de reprovações: {e}")

    # ==========================================
    # TAB 3: SITUAÇÃO DAS DISCIPLINAS
    # ==========================================
    with tab3:
        st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA (SITUAÇÃO DAS DISCIPLINAS)</p>", unsafe_allow_html=True)
        
        import unicodedata

        def strip_accents(text):
            if not isinstance(text, str):
                return text
            return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

        @st.cache_data
        def load_disp_data():
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, 'CI_Disp.csv')
            try:
                df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(csv_path, sep=';', encoding='latin1')
            
            if 'qtd_alunos' in df.columns:
                df['qtd_alunos'] = pd.to_numeric(df['qtd_alunos'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce').fillna(0)
            if 'Desc_Disciplina' in df.columns and 'Descricao_Curso' in df.columns and 'Modalidade' in df.columns:
                df['Disc_Curso_Mod'] = df['Desc_Disciplina'].fillna('') + ' - ' + df['Descricao_Curso'].fillna('') + ' - ' + df['Modalidade'].fillna('')
            return df

        df_disp_full = load_disp_data()

        if df_disp_full.empty:
            st.warning("Dados de disciplinas não encontrados no arquivo CI_Disp.csv.")
        else:
            for f_key in ['f_semestre_disp', 'f_mod_disp', 'f_curso_disp', 'f_disc_disp']:
                if f_key not in st.session_state:
                    st.session_state[f_key] = []

            def get_opts_disp(col):
                df_temp = df_disp_full.copy()
                if col != 'Semestre_Letivo' and st.session_state.f_semestre_disp:
                    df_temp = df_temp[df_temp['Semestre_Letivo'].isin(st.session_state.f_semestre_disp)]
                if col != 'Modalidade' and st.session_state.f_mod_disp:
                    df_temp = df_temp[df_temp['Modalidade'].isin(st.session_state.f_mod_disp)]
                if col != 'Descricao_Curso' and st.session_state.f_curso_disp:
                    df_temp = df_temp[df_temp['Descricao_Curso'].isin(st.session_state.f_curso_disp)]
                if col != 'Desc_Disciplina' and st.session_state.f_disc_disp:
                    df_temp = df_temp[df_temp['Desc_Disciplina'].isin(st.session_state.f_disc_disp)]
                
                opts = list(df_temp[col].dropna().unique())
                if col == 'Semestre_Letivo':
                    opts = sorted(list(set(opts + st.session_state.f_semestre_disp)), reverse=True)
                else:
                    opts = sorted(opts, key=lambda x: strip_accents(str(x)).lower())
                return opts

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.session_state.f_semestre_disp = st.multiselect("Semestre Letivo", get_opts_disp('Semestre_Letivo'), default=st.session_state.f_semestre_disp, placeholder="Todos", key="ms_disp_sem")
            with c2:
                st.session_state.f_mod_disp = st.multiselect("Modalidade", get_opts_disp('Modalidade'), default=st.session_state.f_mod_disp, placeholder="Todas", key="ms_disp_mod")
            with c3:
                st.session_state.f_curso_disp = st.multiselect("Curso", get_opts_disp('Descricao_Curso'), default=st.session_state.f_curso_disp, placeholder="Todos", key="ms_disp_curso")
            with c4:
                st.session_state.f_disc_disp = st.multiselect("Disciplina", get_opts_disp('Desc_Disciplina'), default=st.session_state.f_disc_disp, placeholder="Todas", key="ms_disp_disc")

            df_disp = df_disp_full.copy()
            if st.session_state.f_semestre_disp:
                df_disp = df_disp[df_disp['Semestre_Letivo'].isin(st.session_state.f_semestre_disp)]
            if st.session_state.f_mod_disp:
                df_disp = df_disp[df_disp['Modalidade'].isin(st.session_state.f_mod_disp)]
            if st.session_state.f_curso_disp:
                df_disp = df_disp[df_disp['Descricao_Curso'].isin(st.session_state.f_curso_disp)]
            if st.session_state.f_disc_disp:
                df_disp = df_disp[df_disp['Desc_Disciplina'].isin(st.session_state.f_disc_disp)]

            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

            modo_vis_disp = st.radio(
                "Modo de Exibição dos Indicadores:",
                ["Valor Absoluto", "Valor em %"],
                horizontal=True,
                key="radio_modo_vis_disp"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            tot_alunos_disp = df_disp['qtd_alunos'].sum()

            def fmt_disp_val(val, total):
                if pd.isna(val): return "-"
                if modo_vis_disp == "Valor em %":
                    pct = (val / total * 100) if total > 0 else 0
                    return fmt_br(pct, 1) + "%"
                else:
                    return fmt_br(val, 0)

            sit_map = df_disp.groupby('Sit_Disciplina_Aluno')['qtd_alunos'].sum().to_dict()
            
            v_aprovado = sit_map.get('Aprovado', 0)
            v_aprov_mod = sit_map.get('Aprovado /Rep. no Módulo', 0)
            v_aproveit = sit_map.get('Aproveit. Disciplina', 0)
            v_rep_falta = sit_map.get('Rep. Falta', 0)
            v_reprovado = sit_map.get('Reprovado', 0)

            card_style_disp = "<div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 12px 5px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 100%;'><p style='color: #666; font-size: 0.85rem; margin-bottom: 6px; font-weight: bold;'>{title}</p><h2 style='color: #006633; margin: 5px 0; font-size: 1.3rem;'>{main_val}</h2></div>"

            cs1, cs2, cs3, cs4, cs5 = st.columns(5)
            cs1.markdown(card_style_disp.format(title="Aprovado", main_val=fmt_disp_val(v_aprovado, tot_alunos_disp)), unsafe_allow_html=True)
            cs2.markdown(card_style_disp.format(title="Aprovado /Rep. Módulo", main_val=fmt_disp_val(v_aprov_mod, tot_alunos_disp)), unsafe_allow_html=True)
            cs3.markdown(card_style_disp.format(title="Aproveit. Disciplina", main_val=fmt_disp_val(v_aproveit, tot_alunos_disp)), unsafe_allow_html=True)
            cs4.markdown(card_style_disp.format(title="Rep. Falta", main_val=fmt_disp_val(v_rep_falta, tot_alunos_disp)), unsafe_allow_html=True)
            cs5.markdown(card_style_disp.format(title="Reprovado", main_val=fmt_disp_val(v_reprovado, tot_alunos_disp)), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            df_reprov_disc = df_disp[df_disp['Sit_Disciplina_Aluno'].isin(['Rep. Falta', 'Reprovado'])].groupby('Disc_Curso_Mod')['qtd_alunos'].sum().reset_index()
            df_tot_disc = df_disp.groupby('Disc_Curso_Mod')['qtd_alunos'].sum().reset_index(name='Total_Disc')
            
            df_reprov_disc = df_reprov_disc.merge(df_tot_disc, on='Disc_Curso_Mod', how='right').fillna(0)
            df_reprov_disc['Taxa_Reprovacao'] = (df_reprov_disc['qtd_alunos'] / df_reprov_disc['Total_Disc']).fillna(0)
            
            if modo_vis_disp == "Valor em %":
                top_reprov = df_reprov_disc.sort_values('Taxa_Reprovacao', ascending=False).head(3)
                top_reprov_dict = dict(zip(top_reprov['Disc_Curso_Mod'], top_reprov['Taxa_Reprovacao']))
                is_pct_card = True
            else:
                top_reprov = df_reprov_disc.sort_values('qtd_alunos', ascending=False).head(3)
                top_reprov_dict = dict(zip(top_reprov['Disc_Curso_Mod'], top_reprov['qtd_alunos']))
                is_pct_card = False

            def create_card_list_disp(title, color, data_dict, is_pct=False):
                items_html = ""
                for nome, valor in data_dict.items():
                    nome_clean = str(nome).replace('<', '&lt;').replace('>', '&gt;')
                    val_str = f"{fmt_br(valor * 100, 1)}%" if is_pct else f"{fmt_br(valor, 0)} alunos"
                    items_html += f"<li style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.88rem; color: #333;'><span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 78%;' title='{nome_clean}'>• {nome_clean}</span><strong style='color: {color};'>{val_str}</strong></li>"
                return f"<div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px 20px; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);'><p style='color: {color}; font-size: 1.05rem; margin-bottom: 10px; font-weight: bold; text-align: center;'>{title}</p><ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>{items_html}</ul></div>"

            st.markdown(create_card_list_disp("⚠️ Disciplinas com Maior Reprovação (Rep. Falta + Reprovado)", "#E53935", top_reprov_dict, is_pct=is_pct_card), unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📈 VISÃO GRÁFICA (SITUAÇÃO DAS DISCIPLINAS)</p>", unsafe_allow_html=True)

            if not df_disp.empty:
                df_grp_sem = df_disp.groupby(['Semestre_Letivo', 'Sit_Disciplina_Aluno'])['qtd_alunos'].sum().unstack(fill_value=0).reset_index()

                for col_esp in ['Aprovado', 'Aprovado /Rep. no Módulo', 'Aproveit. Disciplina', 'Rep. Falta', 'Reprovado']:
                    if col_esp not in df_grp_sem.columns:
                        df_grp_sem[col_esp] = 0

                df_grp_sem['Aprovados'] = df_grp_sem['Aprovado'] + df_grp_sem['Aprovado /Rep. no Módulo'] + df_grp_sem['Aproveit. Disciplina']
                df_grp_sem['Reprovados'] = df_grp_sem['Rep. Falta'] + df_grp_sem['Reprovado']

                df_chart_disp = pd.melt(
                    df_grp_sem, 
                    id_vars=['Semestre_Letivo'], 
                    value_vars=['Aprovados', 'Reprovados'],
                    var_name='Resultado', 
                    value_name='Qtd'
                )

                is_pct_disp = modo_vis_disp == "Valor em %"

                if is_pct_disp:
                    tot_sem_disp = df_chart_disp.groupby('Semestre_Letivo')['Qtd'].sum().reset_index(name='Total_Sem')
                    df_chart_disp = df_chart_disp.merge(tot_sem_disp, on='Semestre_Letivo')
                    df_chart_disp['Valor'] = (df_chart_disp['Qtd'] / df_chart_disp['Total_Sem'] * 100).fillna(0)
                else:
                    df_chart_disp['Valor'] = df_chart_disp['Qtd']

                st.markdown("**Evolução de Aprovados vs Reprovados por Semestre**")

                dec_c = 1 if is_pct_disp else 0
                df_chart_disp['Valor_Txt'] = df_chart_disp['Valor'].apply(lambda x: fmt_br(x, dec_c) + ("%" if is_pct_disp else ""))

                max_val_disp = df_chart_disp['Valor'].max() if not df_chart_disp.empty else 1
                escala_max_disp = max(1.0, float(max_val_disp) * 1.35) if pd.notnull(max_val_disp) and max_val_disp > 0 else 1.0

                x_axis_disp = alt.Axis(labelAngle=-90, grid=True, gridColor='#EAEAEA', title='Semestre Letivo')
                y_title_disp = "Proporção (%)" if is_pct_disp else "Quantidade de Alunos"
                y_axis_disp = alt.Axis(title=y_title_disp, format=',.1f' if is_pct_disp else ',d', labelExpr="replace(datum.label, ',', '.')")

                chart_disp = alt.Chart(df_chart_disp).mark_bar().encode(
                    x=alt.X('Semestre_Letivo:O', title='Semestre Letivo', axis=x_axis_disp),
                    y=alt.Y('Valor:Q', title=y_title_disp, axis=y_axis_disp, scale=alt.Scale(domain=[0, escala_max_disp])),
                    color=alt.Color('Resultado:N', scale=alt.Scale(domain=['Aprovados', 'Reprovados'], range=['#006633', '#E53935']), legend=alt.Legend(orient='bottom', title=None)),
                    xOffset='Resultado:N',
                    tooltip=['Semestre_Letivo:O', 'Resultado:N', 'Valor_Txt:N']
                )

                text_disp = alt.Chart(df_chart_disp).mark_text(
                    align='left', baseline='middle', dx=5, angle=270, fontSize=10, fontWeight='bold'
                ).encode(
                    x=alt.X('Semestre_Letivo:O', title='Semestre Letivo', axis=x_axis_disp),
                    y=alt.Y('Valor:Q', title=y_title_disp, axis=y_axis_disp),
                    xOffset='Resultado:N',
                    text='Valor_Txt:N'
                )

                st.altair_chart((chart_disp + text_disp).properties(height=380).interactive(), width="stretch")

            st.markdown("<hr style='margin: 30px 0 10px 0;'>", unsafe_allow_html=True)

            with st.expander("📊 Tabela Geral - Situação das Disciplinas por Semestre", expanded=True):
                try:
                    if not df_disp.empty:
                        pivot_disp = df_disp.pivot_table(
                            index=['Semestre_Letivo', 'Modalidade', 'Descricao_Curso', 'Desc_Disciplina'],
                            columns='Sit_Disciplina_Aluno',
                            values='qtd_alunos',
                            aggfunc='sum',
                            fill_value=0
                        ).reset_index()

                        colunas_esperadas = ['Aprovado', 'Aprovado /Rep. no Módulo', 'Aproveit. Disciplina', 'Rep. Falta', 'Reprovado']
                        for col in colunas_esperadas:
                            if col not in pivot_disp.columns:
                                pivot_disp[col] = 0

                        pivot_disp['Total de alunos'] = pivot_disp[colunas_esperadas].sum(axis=1)
                        pivot_disp['Soma_Reprovacoes'] = pivot_disp['Rep. Falta'] + pivot_disp['Reprovado']

                        pivot_disp['Disc_Sort'] = pivot_disp['Desc_Disciplina'].apply(lambda x: strip_accents(str(x)).lower())

                        pivot_disp = pivot_disp.sort_values(
                            by=['Semestre_Letivo', 'Soma_Reprovacoes', 'Disc_Sort'], 
                            ascending=[False, False, True]
                        ).drop(columns=['Disc_Sort'])

                        cols_final = ['Semestre_Letivo', 'Modalidade', 'Descricao_Curso', 'Desc_Disciplina', 'Total de alunos'] + colunas_esperadas
                        df_exibir = pivot_disp[cols_final].copy()
                        df_exibir.rename(columns={'Semestre_Letivo': 'Semestre'}, inplace=True)

                        if modo_vis_disp == "Valor em %":
                            for col in colunas_esperadas:
                                df_exibir[col] = df_exibir.apply(
                                    lambda r: f"{fmt_br((r[col] / r['Total de alunos'] * 100), 1)}%" if r['Total de alunos'] > 0 else "0,0%", axis=1
                                )
                            df_exibir['Total de alunos'] = df_exibir['Total de alunos'].apply(lambda x: fmt_br(x, 0))
                        else:
                            for col in ['Total de alunos'] + colunas_esperadas:
                                df_exibir[col] = df_exibir[col].apply(lambda x: fmt_br(x, 0))

                        st.dataframe(df_exibir, width="stretch", hide_index=True)
                    else:
                        st.info("Nenhum dado encontrado para a consulta da tabela.")
                except Exception as e:
                    st.error(f"Erro ao gerar a tabela de disciplinas: {e}")

    # ==========================================
    # TAB 4: FORMAM NO TEMPO ?
    # ==========================================
    with tab4:
        st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA (FORMAM NO TEMPO ?)</p>", unsafe_allow_html=True)
        
        import unicodedata

        def strip_accents_falta(text):
            if not isinstance(text, str):
                return text
            return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

        @st.cache_data
        def load_falta_data():
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, 'CI_Falta.csv')
            try:
                df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(csv_path, sep=';', encoding='latin1')
            
            for col_num in ['OK_Tempo', 'Tempo_Curso', 'Disc_Faltam', 'Periodo_Falta']:
                if col_num in df.columns:
                    df[col_num] = pd.to_numeric(df[col_num].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce').fillna(0)

            if 'Descricao_Curso' in df.columns and 'Desc_Curso' not in df.columns:
                df.rename(columns={'Descricao_Curso': 'Desc_Curso'}, inplace=True)

            if 'Situacao_Matricula' not in df.columns:
                df['Situacao_Matricula'] = 'Matriculado'

            if 'Desc_Curso' in df.columns and 'Modalidade' in df.columns:
                df['Curso_Mod'] = df['Desc_Curso'].fillna('') + ' - ' + df['Modalidade'].fillna('')

            def categorizar_tempo(row):
                ok_t = row['OK_Tempo']
                t_curso = row['Tempo_Curso']
                
                if 0 <= ok_t <= 1:
                    return "No Tempo (0 a 1 ano)"
                elif 1 < ok_t < 3:
                    return "Atraso de 1 a 2 anos"
                elif 3 <= ok_t < (2 * t_curso):
                    return "Atraso >= 3 anos"
                elif ok_t >= (2 * t_curso):
                    return "Passar do Tempo de Integralização"
                return "Outros"

            df['Faixa_Tempo'] = df.apply(categorizar_tempo, axis=1)
            return df[df['Faixa_Tempo'] != "Outros"]

        df_falta_full = load_falta_data()

        if df_falta_full.empty:
            st.warning("Dados não encontrados no arquivo CI_Falta.csv.")
        else:
            for f_key in ['f_mod_falta', 'f_curso_falta', 'f_sit_falta', 'f_forma_falta']:
                if f_key not in st.session_state:
                    st.session_state[f_key] = []

            def get_opts_falta(col):
                df_temp = df_falta_full.copy()
                if col != 'Modalidade' and st.session_state.f_mod_falta:
                    df_temp = df_temp[df_temp['Modalidade'].isin(st.session_state.f_mod_falta)]
                if col != 'Desc_Curso' and st.session_state.f_curso_falta:
                    df_temp = df_temp[df_temp['Desc_Curso'].isin(st.session_state.f_curso_falta)]
                if col != 'Situacao_Matricula' and st.session_state.f_sit_falta:
                    df_temp = df_temp[df_temp['Situacao_Matricula'].isin(st.session_state.f_sit_falta)]
                if col != 'Forma_Ingresso' and st.session_state.f_forma_falta:
                    df_temp = df_temp[df_temp['Forma_Ingresso'].isin(st.session_state.f_forma_falta)]
                
                opts = list(df_temp[col].dropna().unique())
                opts = sorted(opts, key=lambda x: strip_accents_falta(str(x)).lower())
                return opts

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.session_state.f_mod_falta = st.multiselect("Modalidade", get_opts_falta('Modalidade'), default=st.session_state.f_mod_falta, placeholder="Todas", key="ms_falta_mod")
            with c2:
                st.session_state.f_curso_falta = st.multiselect("Curso", get_opts_falta('Desc_Curso'), default=st.session_state.f_curso_falta, placeholder="Todos", key="ms_falta_curso")
            with c3:
                st.session_state.f_sit_falta = st.multiselect("Situação Matrícula", get_opts_falta('Situacao_Matricula'), default=st.session_state.f_sit_falta, placeholder="Todas", key="ms_falta_sit")
            with c4:
                st.session_state.f_forma_falta = st.multiselect("Forma Ingresso", get_opts_falta('Forma_Ingresso'), default=st.session_state.f_forma_falta, placeholder="Todas", key="ms_falta_forma")

            df_falta = df_falta_full.copy()
            if st.session_state.f_mod_falta: df_falta = df_falta[df_falta['Modalidade'].isin(st.session_state.f_mod_falta)]
            if st.session_state.f_curso_falta: df_falta = df_falta[df_falta['Desc_Curso'].isin(st.session_state.f_curso_falta)]
            if st.session_state.f_sit_falta: df_falta = df_falta[df_falta['Situacao_Matricula'].isin(st.session_state.f_sit_falta)]
            if st.session_state.f_forma_falta: df_falta = df_falta[df_falta['Forma_Ingresso'].isin(st.session_state.f_forma_falta)]

            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

            modo_vis_falta = st.radio(
                "Modo de Exibição dos Indicadores:",
                ["Valor Absoluto", "Valor em %"],
                horizontal=True,
                key="radio_modo_vis_falta"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            tot_alunos_falta = len(df_falta)
            media_disc_falta_geral = df_falta['Disc_Faltam'].mean() if not df_falta.empty else 0

            def fmt_falta_val(val, total):
                if pd.isna(val): return "-"
                if modo_vis_falta == "Valor em %":
                    pct = (val / total * 100) if total > 0 else 0
                    return fmt_br(pct, 1) + "%"
                else:
                    return fmt_br(val, 0)

            ordem_faixas = [
                "No Tempo (0 a 1 ano)",
                "Atraso de 1 a 2 anos",
                "Atraso >= 3 anos",
                "Passar do Tempo de Integralização"
            ]

            card_style_falta = "<div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 12px 8px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 100%;'><p style='color: #666; font-size: 0.82rem; margin-bottom: 4px; font-weight: bold;'>{title}</p><h2 style='color: #006633; margin: 2px 0; font-size: 1.3rem;'>{main_val}</h2>{details}</div>"

            cols_cards_f = st.columns(6)
            
            cols_cards_f[0].markdown(card_style_falta.format(
                title="Total de Alunos", 
                main_val=fmt_br(tot_alunos_falta, 0), 
                details="<p style='font-size: 0.72rem; color: #666; margin-top: 6px;'>Alunos Analisados</p>"
            ), unsafe_allow_html=True)

            for idx, fx_name in enumerate(ordem_faixas):
                df_fx = df_falta[df_falta['Faixa_Tempo'] == fx_name]
                qtd_fx = len(df_fx)
                
                fi_counts = df_fx['Forma_Ingresso'].value_counts().head(2)
                
                det_html = "<div style='text-align: left; font-size: 0.72rem; color: #444; margin-top: 6px; border-top: 1px solid #eee; padding-top: 4px;'>"
                det_html += "<strong>Ingresso:</strong><br>" + "".join([f"• {k}: {fmt_falta_val(v, qtd_fx)}<br>" for k, v in fi_counts.items()])
                det_html += "</div>"
                
                cols_cards_f[idx+1].markdown(card_style_falta.format(title=fx_name, main_val=fmt_falta_val(qtd_fx, tot_alunos_falta), details=det_html), unsafe_allow_html=True)

            cols_cards_f[5].markdown(card_style_falta.format(
                title="Média Disc. Faltantes", 
                main_val=fmt_br(media_disc_falta_geral, 1), 
                details="<p style='font-size: 0.72rem; color: #666; margin-top: 6px;'>Disciplinas / Aluno</p>"
            ), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            def build_list_card_html(title, color, items_df, tot_base):
                items_html = ""
                for _, r in items_df.iterrows():
                    nome_clean = str(r['Curso_Mod']).replace('<', '&lt;').replace('>', '&gt;')
                    val_str = fmt_falta_val(r['Qtd'], tot_base)
                    items_html += f"<li style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.88rem; color: #333;'><span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80%;' title='{nome_clean}'>• {nome_clean}</span><strong style='color: {color};'>{val_str}</strong></li>"
                return f"<div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px 20px; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 100%;'><p style='color: {color}; font-size: 1rem; margin-bottom: 10px; font-weight: bold; text-align: center;'>{title}</p><ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>{items_html}</ul></div>"

            l_col1, l_col2 = st.columns(2)

            df_atraso_3 = df_falta[df_falta['Faixa_Tempo'] == "Atraso >= 3 anos"]
            top_atraso_3 = df_atraso_3.groupby('Curso_Mod').size().reset_index(name='Qtd').sort_values('Qtd', ascending=False).head(3)
            l_col1.markdown(build_list_card_html("⚠️ Cursos com Maior Quantidade de Alunos Deve Atrasar >= 3 Anos", "#E53935", top_atraso_3, len(df_atraso_3)), unsafe_allow_html=True)

            df_excedeu = df_falta[df_falta['Faixa_Tempo'] == "Passar do Tempo de Integralização"]
            top_excedeu = df_excedeu.groupby('Curso_Mod').size().reset_index(name='Qtd').sort_values('Qtd', ascending=False).head(3)
            l_col2.markdown(build_list_card_html("🚨 Cursos com Maior Quantidade de Alunos Deve Passar da Integralização", "#C62828", top_excedeu, len(df_excedeu)), unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📈 VISÃO GRÁFICA (FORMAM NO TEMPO ?)</p>", unsafe_allow_html=True)

            is_pct_falta = modo_vis_falta == "Valor em %"

            st.markdown("**1. Previsão de Formatura por Situação de Matrícula**")
            if not df_falta.empty:
                df_g1_f = df_falta.groupby(['Situacao_Matricula', 'Faixa_Tempo']).size().reset_index(name='Qtd')
                if is_pct_falta:
                    tot_sit = df_falta.groupby('Situacao_Matricula').size().reset_index(name='Tot')
                    df_g1_f = df_g1_f.merge(tot_sit, on='Situacao_Matricula')
                    df_g1_f['Valor'] = (df_g1_f['Qtd'] / df_g1_f['Tot'] * 100).fillna(0)
                else:
                    df_g1_f['Valor'] = df_g1_f['Qtd']

                df_g1_f['Valor_Txt'] = df_g1_f['Valor'].apply(lambda x: fmt_br(x, 1 if is_pct_falta else 0) + ("%" if is_pct_falta else ""))
                max_g1_f = df_g1_f['Valor'].max() if not df_falta.empty else 1
                escala_g1_f = max(1.0, float(max_g1_f) * 1.35)

                y_axis_g1_f = alt.Axis(
                    title="Proporção (%)" if is_pct_falta else "Qtd Alunos",
                    labelExpr="replace(datum.label, ',', '.')"
                )

                c_g1_f = alt.Chart(df_g1_f).mark_bar().encode(
                    x=alt.X('Situacao_Matricula:O', title='Situação da Matrícula', axis=alt.Axis(labelAngle=-90, grid=True)),
                    y=alt.Y('Valor:Q', title="Proporção (%)" if is_pct_falta else "Qtd Alunos", scale=alt.Scale(domain=[0, escala_g1_f]), axis=y_axis_g1_f),
                    color=alt.Color('Faixa_Tempo:N', scale=alt.Scale(domain=ordem_faixas), legend=alt.Legend(orient='bottom', title=None)),
                    xOffset=alt.XOffset('Faixa_Tempo:N', sort=ordem_faixas),
                    tooltip=['Situacao_Matricula:O', 'Faixa_Tempo:N', 'Valor_Txt:N']
                )
                t_g1_f = alt.Chart(df_g1_f).mark_text(align='left', baseline='middle', dx=5, angle=270, fontSize=9, fontWeight='bold').encode(
                    x=alt.X('Situacao_Matricula:O'), y=alt.Y('Valor:Q'), xOffset=alt.XOffset('Faixa_Tempo:N', sort=ordem_faixas), text='Valor_Txt:N'
                )
                st.altair_chart((c_g1_f + t_g1_f).properties(height=360).interactive(), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**2. Previsão de Formatura por Forma de Ingresso**")
            if not df_falta.empty:
                df_g2_f = df_falta.groupby(['Forma_Ingresso', 'Faixa_Tempo']).size().reset_index(name='Qtd')
                if is_pct_falta:
                    tot_fi = df_falta.groupby('Forma_Ingresso').size().reset_index(name='Tot')
                    df_g2_f = df_g2_f.merge(tot_fi, on='Forma_Ingresso')
                    df_g2_f['Valor'] = (df_g2_f['Qtd'] / df_g2_f['Tot'] * 100).fillna(0)
                else:
                    df_g2_f['Valor'] = df_g2_f['Qtd']

                df_g2_f['Valor_Txt'] = df_g2_f['Valor'].apply(lambda x: fmt_br(x, 1 if is_pct_falta else 0) + ("%" if is_pct_falta else ""))
                max_g2_f = df_g2_f['Valor'].max() if not df_falta.empty else 1
                escala_g2_f = max(1.0, float(max_g2_f) * 1.35)

                y_axis_g2_f = alt.Axis(
                    title="Proporção (%)" if is_pct_falta else "Qtd Alunos",
                    labelExpr="replace(datum.label, ',', '.')"
                )

                c_g2_f = alt.Chart(df_g2_f).mark_bar().encode(
                    x=alt.X('Forma_Ingresso:O', title='Forma de Ingresso', axis=alt.Axis(labelAngle=-90, grid=True)),
                    y=alt.Y('Valor:Q', title="Proporção (%)" if is_pct_falta else "Qtd Alunos", scale=alt.Scale(domain=[0, escala_g2_f]), axis=y_axis_g2_f),
                    color=alt.Color('Faixa_Tempo:N', scale=alt.Scale(domain=ordem_faixas), legend=alt.Legend(orient='bottom', title=None)),
                    xOffset=alt.XOffset('Faixa_Tempo:N', sort=ordem_faixas),
                    tooltip=['Forma_Ingresso:O', 'Faixa_Tempo:N', 'Valor_Txt:N']
                )
                t_g2_f = alt.Chart(df_g2_f).mark_text(align='left', baseline='middle', dx=5, angle=270, fontSize=9, fontWeight='bold').encode(
                    x=alt.X('Forma_Ingresso:O'), y=alt.Y('Valor:Q'), xOffset=alt.XOffset('Faixa_Tempo:N', sort=ordem_faixas), text='Valor_Txt:N'
                )
                st.altair_chart((c_g2_f + t_g2_f).properties(height=360).interactive(), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**3. Média de Disciplinas que Faltam por Forma de Ingresso**")
            if not df_falta.empty:
                df_g3_f = df_falta.groupby('Forma_Ingresso')['Disc_Faltam'].mean().reset_index(name='Media_Falta')
                df_g3_f['Valor_Txt'] = df_g3_f['Media_Falta'].apply(lambda x: fmt_br(x, 1))
                max_g3_f = df_g3_f['Media_Falta'].max() if not df_falta.empty else 1
                escala_g3_f = max(1.0, float(max_g3_f) * 1.35)

                y_axis_g3_f = alt.Axis(title="Média de Disciplinas Faltantes", labelExpr="replace(datum.label, ',', '.')")

                c_g3_f = alt.Chart(df_g3_f).mark_bar(color='#006633').encode(
                    x=alt.X('Forma_Ingresso:O', title='Forma de Ingresso', axis=alt.Axis(labelAngle=-90, grid=True)),
                    y=alt.Y('Media_Falta:Q', title="Média de Disciplinas Faltantes", scale=alt.Scale(domain=[0, escala_g3_f]), axis=y_axis_g3_f),
                    tooltip=['Forma_Ingresso:O', 'Valor_Txt:N']
                )
                t_g3_f = alt.Chart(df_g3_f).mark_text(align='left', baseline='middle', dx=5, angle=270, fontSize=9, fontWeight='bold').encode(
                    x=alt.X('Forma_Ingresso:O'), y=alt.Y('Media_Falta:Q'), text='Valor_Txt:N'
                )
                st.altair_chart((c_g3_f + t_g3_f).properties(height=360).interactive(), width="stretch")

            st.markdown("<hr style='margin: 30px 0 10px 0;'>", unsafe_allow_html=True)

            # MATRIZ DE ASSOCIAÇÃO (FORMAM NO TEMPO)
            st.markdown("**🔥 Matriz de Associação: Previsão de Tempo x Forma de Ingresso**")
            if not df_falta.empty:
                df_temp_falta = df_falta.copy()
                melted_falta = []
                order_labels_falta = []

                if 'Forma_Ingresso' in df_temp_falta.columns:
                    ct = pd.crosstab(df_temp_falta['Faixa_Tempo'], df_temp_falta['Forma_Ingresso'], normalize='index') * 100
                    for col_val in ct.columns:
                        rotulo_limpo = limpar_rotulo(col_val)
                        if rotulo_limpo not in order_labels_falta:
                            order_labels_falta.append(rotulo_limpo)
                        for row_val in ct.index:
                            melted_falta.append({
                                'Previsão Tempo': str(row_val),
                                'Atributo': rotulo_limpo,
                                'Proporção (%)': ct.loc[row_val, col_val]
                            })

                df_hm_falta = pd.DataFrame(melted_falta)
                df_hm_falta['Txt'] = df_hm_falta['Proporção (%)'].apply(lambda x: fmt_br(x, 1) + "%")
                
                chart_falta_hm = alt.Chart(df_hm_falta).mark_rect().encode(
                    x=alt.X('Atributo:O', title=None, sort=order_labels_falta, axis=alt.Axis(labelAngle=-90, labelFontSize=11)),
                    y=alt.Y('Previsão Tempo:O', title='Previsão de Formatura', sort=ordem_faixas),
                    color=alt.Color('Proporção (%):Q', scale=alt.Scale(scheme='greens'), legend=alt.Legend(title="Proporção %")),
                    tooltip=['Previsão Tempo:N', 'Atributo:N', 'Txt:N']
                )
                text_falta_hm = chart_falta_hm.mark_text(baseline='middle', fontSize=10, fontWeight='bold').encode(
                    text='Txt:N',
                    color=alt.condition(alt.datum['Proporção (%)'] > 50, alt.value('white'), alt.value('black'))
                )
                st.altair_chart((chart_falta_hm + text_falta_hm).properties(height=280).interactive(), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            with st.expander("📊 Tabela Geral - Previsão de Formatura por Curso", expanded=True):
                try:
                    if not df_falta.empty:
                        pivot_falta = df_falta.pivot_table(
                            index=['Modalidade', 'Desc_Curso'],
                            columns='Faixa_Tempo',
                            values='Cod_Matricula',
                            aggfunc='count',
                            fill_value=0
                        ).reset_index()

                        for col in ordem_faixas:
                            if col not in pivot_falta.columns:
                                pivot_falta[col] = 0

                        df_media_curso = df_falta.groupby(['Modalidade', 'Desc_Curso'])['Disc_Faltam'].mean().reset_index(name='Média de Disciplinas que Faltam')

                        pivot_falta = pivot_falta.merge(df_media_curso, on=['Modalidade', 'Desc_Curso'], how='left')

                        pivot_falta['Curso_Sort'] = pivot_falta['Desc_Curso'].apply(lambda x: strip_accents_falta(str(x)).lower())
                        
                        pivot_falta = pivot_falta.sort_values(
                            by=['No Tempo (0 a 1 ano)', 'Curso_Sort'],
                            ascending=[False, True]
                        ).drop(columns=['Curso_Sort'])

                        cols_tabela = ['Modalidade', 'Desc_Curso'] + ordem_faixas + ['Média de Disciplinas que Faltam']
                        df_exibir_f = pivot_falta[cols_tabela].copy()

                        if modo_vis_falta == "Valor em %":
                            tot_linha_f = df_exibir_f[ordem_faixas].sum(axis=1)
                            for col in ordem_faixas:
                                df_exibir_f[col] = df_exibir_f.apply(
                                    lambda r: f"{fmt_br((r[col] / tot_linha_f[r.name] * 100), 1)}%" if tot_linha_f[r.name] > 0 else "0,0%", axis=1
                                )
                        else:
                            for col in ordem_faixas:
                                df_exibir_f[col] = df_exibir_f[col].apply(lambda x: fmt_br(x, 0))

                        df_exibir_f['Média de Disciplinas que Faltam'] = df_exibir_f['Média de Disciplinas que Faltam'].apply(lambda x: fmt_br(x, 1))

                        st.dataframe(df_exibir_f, width="stretch", hide_index=True)
                    else:
                        st.info("Nenhum dado encontrado para gerar a tabela de disciplinas que faltam.")
                except Exception as e:
                    st.error(f"Erro ao gerar a tabela consolidada: {e}")

# ------------------------------------------
# 4. PNP
# ------------------------------------------
elif menu_opcao == "📊 Plataforma PNP":
    st.markdown("### 📊 Plataforma Nilo Peçanha (PNP)")
    
    tab1, tab2, tab3 = st.tabs([
        "📈 Situação da Matrícula (PNP)", 
        "⚖️ Percentuais Legais e Rap", 
        "⚡ Eficiência Acadêmica"
    ])
    
    with tab1:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_geral_path = os.path.join(script_dir, 'CI_PNP_Geral.csv')
            csv_sit_path = os.path.join(script_dir, 'CI_PNP_Sit.csv')
            
            try:
                df_geral = pd.read_csv(csv_geral_path, sep=";", encoding="utf-8")
            except UnicodeDecodeError:
                df_geral = pd.read_csv(csv_geral_path, sep=";", encoding="latin1")
            df_geral.columns = df_geral.columns.str.strip()

            try:
                df_sit = pd.read_csv(csv_sit_path, sep=";", encoding="utf-8")
            except UnicodeDecodeError:
                df_sit = pd.read_csv(csv_sit_path, sep=";", encoding="latin1")
            df_sit.columns = df_sit.columns.str.strip()

            for col_str in ['Situação', 'Fluxo Escolar', 'FluxoRetido', 'Modalidade de Ensino', 'Tipo de Curso', 'Tipo de Oferta', 'Nome do Curso', 'Turno do Curso']:
                if col_str in df_sit.columns:
                    df_sit[col_str] = df_sit[col_str].astype(str).str.strip()

            if 'Situação' in df_sit.columns:
                df_sit['Situação'] = df_sit['Situação'].str.title()
                df_sit['Situação'] = df_sit['Situação'].replace({'Em Curso': 'Em Curso', 'Concluintes': 'Concluintes', 'Evadidos': 'Evadidos'})

            def limpar_numero(val):
                if pd.isna(val) or val is None:
                    return 0.0
                val_str = str(val).strip()
                if not val_str or val_str.lower() == 'nan':
                    return 0.0
                if ',' in val_str and '.' in val_str:
                    val_str = val_str.replace('.', '').replace(',', '.')
                elif ',' in val_str:
                    val_str = val_str.replace(',', '.')
                elif '.' in val_str:
                    partes = val_str.split('.')
                    if len(partes[-1]) == 3 and len(partes) > 1:
                        val_str = val_str.replace('.', '')
                try:
                    return float(val_str)
                except ValueError:
                    return 0.0

            cols_geral_num = ['Matrículas', 'Matrículas Equivalentes', 'Vagas', 'Inscritos', 'Ingressantes', 'Concluintes']
            for col in cols_geral_num:
                if col in df_geral.columns:
                    df_geral[col] = df_geral[col].apply(limpar_numero)

            if 'Matrículas' in df_sit.columns:
                df_sit['Matrículas'] = df_sit['Matrículas'].apply(limpar_numero)

            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA</p>", unsafe_allow_html=True)

            for f_key in ['f_anos_sit', 'f_mod_sit', 'f_tipo_curso_sit', 'f_tipo_oferta_sit', 'f_nome_curso_sit', 'f_turno_sit']:
                if f_key not in st.session_state:
                    st.session_state[f_key] = []

            def get_opts_sit(col):
                df_temp = df_sit.copy()
                if col != 'Ano' and st.session_state.f_anos_sit: df_temp = df_temp[df_temp['Ano'].isin(st.session_state.f_anos_sit)]
                if col != 'Modalidade de Ensino' and st.session_state.f_mod_sit: df_temp = df_temp[df_temp['Modalidade de Ensino'].isin(st.session_state.f_mod_sit)]
                if col != 'Tipo de Curso' and st.session_state.f_tipo_curso_sit: df_temp = df_temp[df_temp['Tipo de Curso'].isin(st.session_state.f_tipo_curso_sit)]
                if col != 'Tipo de Oferta' and st.session_state.f_tipo_oferta_sit: df_temp = df_temp[df_temp['Tipo de Oferta'].isin(st.session_state.f_tipo_oferta_sit)]
                if col != 'Nome do Curso' and st.session_state.f_nome_curso_sit: df_temp = df_temp[df_temp['Nome do Curso'].isin(st.session_state.f_nome_curso_sit)]
                if col != 'Turno do Curso' and st.session_state.f_turno_sit: df_temp = df_temp[df_temp['Turno do Curso'].isin(st.session_state.f_turno_sit)]
                
                opts = sorted(list(df_temp[col].dropna().unique()))
                if col == 'Ano':
                    opts = sorted(list(set(opts + st.session_state.f_anos_sit)), reverse=True)
                return opts

            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                st.session_state.f_anos_sit = st.multiselect("Ano", get_opts_sit('Ano'), default=st.session_state.f_anos_sit, placeholder="Todos os anos", key="ms_sit_ano")
                st.session_state.f_mod_sit = st.multiselect("Modalidade de Ensino", get_opts_sit('Modalidade de Ensino'), default=st.session_state.f_mod_sit, placeholder="Todas", key="ms_sit_mod")
            with f_col2:
                st.session_state.f_tipo_curso_sit = st.multiselect("Tipo de Curso", get_opts_sit('Tipo de Curso'), default=st.session_state.f_tipo_curso_sit, placeholder="Todos", key="ms_sit_tipo_curso")
                st.session_state.f_tipo_oferta_sit = st.multiselect("Tipo de Oferta", get_opts_sit('Tipo de Oferta'), default=st.session_state.f_tipo_oferta_sit, placeholder="Todas", key="ms_sit_tipo_oferta")
            with f_col3:
                st.session_state.f_nome_curso_sit = st.multiselect("Nome do Curso", get_opts_sit('Nome do Curso'), default=st.session_state.f_nome_curso_sit, placeholder="Todos", key="ms_sit_nome_curso")
                st.session_state.f_turno_sit = st.multiselect("Turno do Curso", get_opts_sit('Turno do Curso'), default=st.session_state.f_turno_sit, placeholder="Todos", key="ms_sit_turno")

            df_geral_filt = df_geral.copy()
            df_sit_filt = df_sit.copy()

            if st.session_state.f_anos_sit:
                df_geral_filt = df_geral_filt[df_geral_filt['Ano'].isin(st.session_state.f_anos_sit)]
                df_sit_filt = df_sit_filt[df_sit_filt['Ano'].isin(st.session_state.f_anos_sit)]
            if st.session_state.f_mod_sit:
                df_geral_filt = df_geral_filt[df_geral_filt['Modalidade de Ensino'].isin(st.session_state.f_mod_sit)]
                df_sit_filt = df_sit_filt[df_sit_filt['Modalidade de Ensino'].isin(st.session_state.f_mod_sit)]
            if st.session_state.f_tipo_curso_sit:
                df_geral_filt = df_geral_filt[df_geral_filt['Tipo de Curso'].isin(st.session_state.f_tipo_curso_sit)]
                df_sit_filt = df_sit_filt[df_sit_filt['Tipo de Curso'].isin(st.session_state.f_tipo_curso_sit)]
            if st.session_state.f_tipo_oferta_sit:
                df_geral_filt = df_geral_filt[df_geral_filt['Tipo de Oferta'].isin(st.session_state.f_tipo_oferta_sit)]
                df_sit_filt = df_sit_filt[df_sit_filt['Tipo de Oferta'].isin(st.session_state.f_tipo_oferta_sit)]
            if st.session_state.f_nome_curso_sit:
                df_geral_filt = df_geral_filt[df_geral_filt['Nome do Curso'].isin(st.session_state.f_nome_curso_sit)]
                df_sit_filt = df_sit_filt[df_sit_filt['Nome do Curso'].isin(st.session_state.f_nome_curso_sit)]
            if st.session_state.f_turno_sit:
                df_geral_filt = df_geral_filt[df_geral_filt['Turno do Curso'].isin(st.session_state.f_turno_sit)]
                df_sit_filt = df_sit_filt[df_sit_filt['Turno do Curso'].isin(st.session_state.f_turno_sit)]

            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

            modo_vis_sit = st.radio(
                "Modo de Exibição dos Indicadores de Situação:",
                ["Valor Absoluto", "Valor em %"],
                horizontal=True,
                key="radio_modo_vis_sit"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            tot_mat = df_geral_filt['Matrículas'].sum() if not df_geral_filt.empty else 0
            tot_mat_eq = df_geral_filt['Matrículas Equivalentes'].sum() if not df_geral_filt.empty else 0
            tot_fec = tot_mat_eq / tot_mat if tot_mat > 0 else 0
            tot_vagas = df_geral_filt['Vagas'].sum() if not df_geral_filt.empty else 0
            tot_insc = df_geral_filt['Inscritos'].sum() if not df_geral_filt.empty else 0
            cand_vaga_sit = tot_insc / tot_vagas if tot_vagas > 0 else 0

            card_l1_style = """
            <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;'>
                <p style='color: #666; font-size: 0.95rem; margin-bottom: 5px; font-weight: bold;'>{title}</p>
                <h2 style='color: #006633; margin-top: 0px; font-size: 1.8rem;'>{value}</h2>
            </div>
            """

            lc1, lc2, lc3, lc4, lc5, lc6 = st.columns(6)
            lc1.markdown(card_l1_style.format(title="Matrículas", value=fmt_br(tot_mat, 0)), unsafe_allow_html=True)
            lc2.markdown(card_l1_style.format(title="Matrículas Equivalentes", value=fmt_br(tot_mat_eq, 0)), unsafe_allow_html=True)
            lc3.markdown(card_l1_style.format(title="FEC", value=fmt_br(tot_fec, 2)), unsafe_allow_html=True)
            lc4.markdown(card_l1_style.format(title="Vagas Ofertadas", value=fmt_br(tot_vagas, 0)), unsafe_allow_html=True)
            lc5.markdown(card_l1_style.format(title="Inscritos", value=fmt_br(tot_insc, 0)), unsafe_allow_html=True)
            lc6.markdown(card_l1_style.format(title="Candidato x Vaga", value=fmt_br(cand_vaga_sit, 2)), unsafe_allow_html=True)

            mask_conc = df_sit_filt['Situação'].str.lower().str.startswith('conclu') if not df_sit_filt.empty else pd.Series(False, index=df_sit_filt.index)
            mask_curs = df_sit_filt['Situação'].str.lower().str.contains('em curso') if not df_sit_filt.empty else pd.Series(False, index=df_sit_filt.index)
            mask_evad = df_sit_filt['Situação'].str.lower().str.startswith('evad') if not df_sit_filt.empty else pd.Series(False, index=df_sit_filt.index)

            m_conc = df_sit_filt[mask_conc]['Matrículas'].sum()
            m_conc_c = df_sit_filt[mask_conc & df_sit_filt['Fluxo Escolar'].str.lower().str.startswith('conclu')]['Matrículas'].sum()
            m_conc_i = df_sit_filt[mask_conc & df_sit_filt['Fluxo Escolar'].str.lower().str.startswith('integral')]['Matrículas'].sum()

            m_curs = df_sit_filt[mask_curs]['Matrículas'].sum()
            mask_is_retido = df_sit_filt['FluxoRetido'].str.lower().str.startswith('retid')
            m_curs_r = df_sit_filt[mask_curs & mask_is_retido]['Matrículas'].sum()
            m_curs_c = df_sit_filt[mask_curs & (~mask_is_retido)]['Matrículas'].sum()

            m_evad = df_sit_filt[mask_evad]['Matrículas'].sum()
            m_total_sit = m_conc + m_curs + m_evad

            if modo_vis_sit == "Valor em %" and m_total_sit > 0:
                txt_conc = f"{fmt_br((m_conc / m_total_sit) * 100, 1)}%"
                txt_conc_sub = f"Concluída: {fmt_br((m_conc_c / m_total_sit) * 100, 1)}% | Integralizada: {fmt_br((m_conc_i / m_total_sit) * 100, 1)}%"
                
                txt_curs = f"{fmt_br((m_curs / m_total_sit) * 100, 1)}%"
                txt_curs_sub = f"Em curso: {fmt_br((m_curs_c / m_total_sit) * 100, 1)}% | Retido: {fmt_br((m_curs_r / m_total_sit) * 100, 1)}%"
                
                txt_evad = f"{fmt_br((m_evad / m_total_sit) * 100, 1)}%"
            else:
                txt_conc = fmt_br(m_conc, 0)
                txt_conc_sub = f"Concluída: {fmt_br(m_conc_c, 0)} | Integralizada: {fmt_br(m_conc_i, 0)}"
                
                txt_curs = fmt_br(m_curs, 0)
                txt_curs_sub = f"Em curso: {fmt_br(m_curs_c, 0)} | Retido: {fmt_br(m_curs_r, 0)}"
                
                txt_evad = fmt_br(m_evad, 0)

            card_l2_style = """
            <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;'>
                <p style='color: #666; font-size: 0.95rem; margin-bottom: 5px; font-weight: bold;'>{title}</p>
                <h2 style='color: #006633; margin-top: 0px; font-size: 1.8rem; margin-bottom: 5px;'>{value}</h2>
                <p style='color: #718096; font-size: 0.8rem; margin: 0;'>{subtext}</p>
            </div>
            """

            sc1, sc2, sc3 = st.columns(3)
            sc1.markdown(card_l2_style.format(title="Concluintes", value=txt_conc, subtext=txt_conc_sub), unsafe_allow_html=True)
            sc2.markdown(card_l2_style.format(title="Em Curso", value=txt_curs, subtext=txt_curs_sub), unsafe_allow_html=True)
            sc3.markdown(card_l2_style.format(title="Evadidos", value=txt_evad, subtext="Desligamentos do ciclo"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if not df_sit_filt.empty:
                cols_grp = ['Nome do Curso', 'Tipo de Curso', 'Tipo de Oferta', 'Turno do Curso']
                df_sit_work = df_sit_filt.copy()

                df_sit_work['Is_Evadido'] = df_sit_work['Situação'].str.lower().str.startswith('evad')
                df_sit_work['Is_Retido'] = (df_sit_work['Situação'].str.lower().str.contains('em curso')) & (df_sit_work['FluxoRetido'].str.lower().str.startswith('retid'))

                def calc_metricas_grupo(g):
                    return pd.Series({
                        'Tot_Mat': g['Matrículas'].sum(),
                        'Tot_Evadidos': g[g['Is_Evadido']]['Matrículas'].sum(),
                        'Tot_Retidos': g[g['Is_Retido']]['Matrículas'].sum()
                    })

                df_calc = df_sit_work.groupby(cols_grp)[['Matrículas', 'Is_Evadido', 'Is_Retido']].apply(calc_metricas_grupo).reset_index()

                df_calc['Pct_Evasao'] = (df_calc['Tot_Evadidos'] / df_calc['Tot_Mat'] * 100).fillna(0)
                df_calc['Pct_Retencao'] = (df_calc['Tot_Retidos'] / df_calc['Tot_Mat'] * 100).fillna(0)
                df_calc['Curso_Identificador'] = df_calc['Nome do Curso'] + " - " + df_calc['Tipo de Curso'] + " - " + df_calc['Tipo de Oferta'] + " - " + df_calc['Turno do Curso']

                top_menor_evas = df_calc.sort_values(by='Pct_Evasao', ascending=True).head(5)
                top_maior_evas = df_calc.sort_values(by='Pct_Evasao', ascending=False).head(5)

                top_menor_ret = df_calc.sort_values(by='Pct_Retencao', ascending=True).head(5)
                top_maior_ret = df_calc.sort_values(by='Pct_Retencao', ascending=False).head(5)

                card_list_style = """
                <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px 20px; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 100%;'>
                    <p style='color: {color}; font-size: 1.05rem; margin-bottom: 10px; font-weight: bold; text-align: center;'>{title}</p>
                    <ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>
                        {items}
                    </ul>
                </div>
                """

                items_m_evas = "".join([f"<li style='display: flex; justify-content: space-between; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.88rem; color: #333;'><span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80%;' title='{r['Curso_Identificador']}'>• {r['Curso_Identificador']}</span><strong style='color: #006633;'>{fmt_br(r['Pct_Evasao'], 1)}%</strong></li>" for _, r in top_menor_evas.iterrows()])
                items_M_evas = "".join([f"<li style='display: flex; justify-content: space-between; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.88rem; color: #333;'><span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80%;' title='{r['Curso_Identificador']}'>• {r['Curso_Identificador']}</span><strong style='color: #E53935;'>{fmt_br(r['Pct_Evasao'], 1)}%</strong></li>" for _, r in top_maior_evas.iterrows()])

                items_m_ret = "".join([f"<li style='display: flex; justify-content: space-between; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.88rem; color: #333;'><span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80%;' title='{r['Curso_Identificador']}'>• {r['Curso_Identificador']}</span><strong style='color: #006633;'>{fmt_br(r['Pct_Retencao'], 1)}%</strong></li>" for _, r in top_menor_ret.iterrows()])
                items_M_ret = "".join([f"<li style='display: flex; justify-content: space-between; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.88rem; color: #333;'><span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80%;' title='{r['Curso_Identificador']}'>• {r['Curso_Identificador']}</span><strong style='color: #E53935;'>{fmt_br(r['Pct_Retencao'], 1)}%</strong></li>" for _, r in top_maior_ret.iterrows()])

                col_ev1, col_ev2 = st.columns(2)
                with col_ev1: st.markdown(card_list_style.format(title="📉 Cursos com Menor Evasão", color="#006633", items=items_m_evas), unsafe_allow_html=True)
                with col_ev2: st.markdown(card_list_style.format(title="📈 Cursos com Maior Evasão", color="#E53935", items=items_M_evas), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                col_ret1, col_ret2 = st.columns(2)
                with col_ret1: st.markdown(card_list_style.format(title="📉 Cursos com Menor Retenção", color="#006633", items=items_m_ret), unsafe_allow_html=True)
                with col_ret2: st.markdown(card_list_style.format(title="📈 Cursos com Maior Retenção", color="#E53935", items=items_M_ret), unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📈 EVOLUÇÃO POR ANO</p>", unsafe_allow_html=True)

            st.markdown("**1. Evolução de Matrículas x Matrículas Equivalentes**")
            df_g_mat = df_geral_filt.groupby('Ano')[['Matrículas', 'Matrículas Equivalentes']].sum().reset_index()
            df_g_mat_melt = df_g_mat.melt(id_vars='Ano', value_vars=['Matrículas', 'Matrículas Equivalentes'], var_name='Tipo', value_name='Valor')
            df_g_mat_melt['Valor_Txt'] = df_g_mat_melt['Valor'].apply(lambda x: fmt_br(x, 0))

            x_axis_pnp = alt.Axis(title='Ano', grid=True, gridColor='#EAEAEA')
            y_axis_pnp = alt.Axis(title='Quantidade', format=',d', labelExpr="replace(datum.label, ',', '.')")

            base_g1 = alt.Chart(df_g_mat_melt).encode(x=alt.X('Ano:O', axis=x_axis_pnp), xOffset='Tipo:N')
            max_g1 = df_g_mat_melt['Valor'].max() if not df_g_mat_melt.empty else 1
            bar_g1 = base_g1.mark_bar().encode(
                y=alt.Y('Valor:Q', axis=y_axis_pnp, scale=alt.Scale(domain=[0, max_g1 * 1.15])),
                color=alt.Color('Tipo:N', scale=alt.Scale(range=['#006633', '#81C784']), legend=alt.Legend(orient='bottom', title=None))
            )
            txt_g1 = base_g1.mark_text(align='center', baseline='bottom', dy=-4, fontWeight='bold').encode(y=alt.Y('Valor:Q'), text=alt.Text('Valor_Txt:N'))
            st.altair_chart((bar_g1 + txt_g1).properties(height=300).interactive(), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**2. Evolução de Processo Seletivo (Inscritos x Vagas)**")
            df_g_proc = df_geral_filt.groupby('Ano')[['Inscritos', 'Vagas']].sum().reset_index()
            df_g_proc_melt = df_g_proc.melt(id_vars='Ano', value_vars=['Inscritos', 'Vagas'], var_name='Tipo', value_name='Valor')
            df_g_proc_melt['Valor_Txt'] = df_g_proc_melt['Valor'].apply(lambda x: fmt_br(x, 0))

            base_g2 = alt.Chart(df_g_proc_melt).encode(x=alt.X('Ano:O', axis=x_axis_pnp), xOffset='Tipo:N')
            max_g2 = df_g_proc_melt['Valor'].max() if not df_g_proc_melt.empty else 1
            bar_g2 = base_g2.mark_bar().encode(
                y=alt.Y('Valor:Q', axis=y_axis_pnp, scale=alt.Scale(domain=[0, max_g2 * 1.15])),
                color=alt.Color('Tipo:N', scale=alt.Scale(domain=['Inscritos', 'Vagas'], range=['#006633', '#81C784']), legend=alt.Legend(orient='bottom', title=None))
            )
            txt_g2 = base_g2.mark_text(align='center', baseline='bottom', dy=-4, fontWeight='bold').encode(y=alt.Y('Valor:Q'), text=alt.Text('Valor_Txt:N'))
            st.altair_chart((bar_g2 + txt_g2).properties(height=300).interactive(), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**3. Evolução do Candidato x Vaga**")
            df_g_cand = df_geral_filt.groupby('Ano')[['Inscritos', 'Vagas']].sum().reset_index()
            df_g_cand['Cand_Vaga'] = (df_g_cand['Inscritos'] / df_g_cand['Vagas']).fillna(0)
            df_g_cand['Cand_Vaga_Txt'] = df_g_cand['Cand_Vaga'].apply(lambda x: fmt_br(x, 2))

            base_g3 = alt.Chart(df_g_cand).encode(x=alt.X('Ano:O', axis=x_axis_pnp))
            max_g3 = df_g_cand['Cand_Vaga'].max() if not df_g_cand.empty else 1
            bar_g3 = base_g3.mark_bar(color='#006633').encode(
                y=alt.Y('Cand_Vaga:Q', axis=alt.Axis(title='Cand x Vaga', format=',.2f', labelExpr="replace(datum.label, ',', '.')"), scale=alt.Scale(domain=[0, max_g3 * 1.15]))
            )
            txt_g3 = base_g3.mark_text(align='center', baseline='bottom', dy=-4, fontWeight='bold').encode(y=alt.Y('Cand_Vaga:Q'), text=alt.Text('Cand_Vaga_Txt:N'))
            st.altair_chart((bar_g3 + txt_g3).properties(height=300).interactive(), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"**4. Distribuição da Situação de Matrícula ({modo_vis_sit})**")
            df_g_sit = df_sit_filt.groupby(['Ano', 'Situação'])['Matrículas'].sum().reset_index()

            if modo_vis_sit == "Valor em %":
                tot_ano_sit = df_g_sit.groupby('Ano')['Matrículas'].transform('sum')
                df_g_sit['Valor_Chart'] = (df_g_sit['Matrículas'] / tot_ano_sit * 100).fillna(0)
                df_g_sit['Valor_Txt'] = df_g_sit['Valor_Chart'].apply(lambda x: f"{fmt_br(x, 1)}%")
                tit_y4 = "Percentual (%)"
                axis_g4 = alt.Axis(title=tit_y4, format=',.1f', labelExpr="replace(datum.label, ',', '.')")
            else:
                df_g_sit['Valor_Chart'] = df_g_sit['Matrículas']
                df_g_sit['Valor_Txt'] = df_g_sit['Valor_Chart'].apply(lambda x: fmt_br(x, 0))
                tit_y4 = "Matrículas"
                axis_g4 = alt.Axis(title=tit_y4, format=',d', labelExpr="replace(datum.label, ',', '.')")

            base_g4 = alt.Chart(df_g_sit).encode(
                x=alt.X('Ano:O', axis=x_axis_pnp), 
                xOffset=alt.X('Situação:N', sort=['Concluintes', 'Em Curso', 'Evadidos'])
            )
            max_g4 = df_g_sit['Valor_Chart'].max() if not df_g_sit.empty else 1
            bar_g4 = base_g4.mark_bar().encode(
                y=alt.Y('Valor_Chart:Q', axis=axis_g4, scale=alt.Scale(domain=[0, max_g4 * 1.15])),
                color=alt.Color(
                    'Situação:N', 
                    scale=alt.Scale(domain=['Concluintes', 'Em Curso', 'Evadidos'], range=['#4CAF50', '#FF9800', '#E53935']), 
                    legend=alt.Legend(orient='bottom', title=None)
                )
            )
            txt_g4 = base_g4.mark_text(align='center', baseline='bottom', dy=-4, fontWeight='bold').encode(y=alt.Y('Valor_Chart:Q'), text=alt.Text('Valor_Txt:N'))
            st.altair_chart((bar_g4 + txt_g4).properties(height=320).interactive(), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"**5. Detalhamento do Fluxo Escolar por Situação ({modo_vis_sit})**")
            
            df_sit_filt_copy = df_sit_filt.copy()
            df_sit_filt_copy['Fluxo_Grupo'] = df_sit_filt_copy['Fluxo Escolar']
            
            mask_ret = (df_sit_filt_copy['Situação'].str.lower().str.contains('em curso')) & (df_sit_filt_copy['FluxoRetido'].str.lower().str.startswith('retid'))
            df_sit_filt_copy.loc[mask_ret, 'Fluxo_Grupo'] = 'Retido'
            mask_cur = (df_sit_filt_copy['Situação'].str.lower().str.contains('em curso')) & (~mask_ret)
            df_sit_filt_copy.loc[mask_cur, 'Fluxo_Grupo'] = 'Em curso'

            def criar_grafico_subfluxo_largo(sit_filtro, titulo_sub, paleta_cores):
                df_sub = df_sit_filt_copy[df_sit_filt_copy['Situação'].str.lower().str.startswith(sit_filtro.lower())]
                df_g = df_sub.groupby(['Ano', 'Fluxo_Grupo'])['Matrículas'].sum().reset_index()

                if df_g.empty:
                    return None

                if modo_vis_sit == "Valor em %":
                    tot_ano = df_g.groupby('Ano')['Matrículas'].transform('sum')
                    df_g['Valor_Chart'] = (df_g['Matrículas'] / tot_ano * 100).fillna(0)
                    df_g['Valor_Txt'] = df_g['Valor_Chart'].apply(lambda x: f"{fmt_br(x, 1)}%")
                    t_y = "%"
                    sub_axis = alt.Axis(title=t_y, format=',.1f', labelExpr="replace(datum.label, ',', '.')")
                else:
                    df_g['Valor_Chart'] = df_g['Matrículas']
                    df_g['Valor_Txt'] = df_g['Valor_Chart'].apply(lambda x: fmt_br(x, 0))
                    t_y = "Quantidade"
                    sub_axis = alt.Axis(title=t_y, format=',d', labelExpr="replace(datum.label, ',', '.')")

                max_val = df_g['Valor_Chart'].max() if not df_g.empty else 1
                base = alt.Chart(df_g).encode(x=alt.X('Ano:O', axis=x_axis_pnp), xOffset='Fluxo_Grupo:N')
                barras = base.mark_bar().encode(
                    y=alt.Y('Valor_Chart:Q', axis=sub_axis, scale=alt.Scale(domain=[0, max_val * 1.18])),
                    color=alt.Color('Fluxo_Grupo:N', scale=alt.Scale(range=paleta_cores), legend=alt.Legend(orient='bottom', title=None))
                )
                textos = base.mark_text(align='center', baseline='bottom', dy=-4, fontWeight='bold').encode(
                    y=alt.Y('Valor_Chart:Q'), text=alt.Text('Valor_Txt:N')
                )
                return (barras + textos).properties(height=260)

            st.markdown("**5.1. Concluintes (Concluída vs Integralizada)**")
            chart_conc = criar_grafico_subfluxo_largo('conclu', 'Concluintes', ['#006633', '#66BB6A'])
            if chart_conc: 
                st.altair_chart(chart_conc, width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**5.2. Em Curso (Em curso vs Retido)**")
            chart_curs = criar_grafico_subfluxo_largo('em curso', 'Em Curso', ['#E65100', '#FBC02D'])
            if chart_curs: 
                st.altair_chart(chart_curs, width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**5.3. Evadidos (Tipos de Desligamento)**")
            chart_evad = criar_grafico_subfluxo_largo('evad', 'Evadidos', ['#B71C1C', '#FF7043', '#880E4F', '#D32F2F', '#FF8A65'])
            if chart_evad: 
                st.altair_chart(chart_evad, width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            with st.expander("📊 Consultar Tabela Geral - Situação da Matrícula", expanded=True):
                cols_chave = ['Ano', 'Modalidade de Ensino', 'Tipo de Curso', 'Tipo de Oferta', 'Nome do Curso', 'Turno do Curso']
                
                df_g_tab = df_geral_filt.groupby(cols_chave)[['Matrículas', 'Matrículas Equivalentes', 'Vagas', 'Inscritos']].sum().reset_index()
                df_s_tab = df_sit_filt.groupby(cols_chave + ['Situação'])['Matrículas'].sum().unstack(fill_value=0).reset_index()

                df_s_tab.columns = [c if isinstance(c, str) else str(c) for c in df_s_tab.columns]
                cols_s_tab = list(df_s_tab.columns)
                
                col_c = [c for c in cols_s_tab if str(c).lower().startswith('conclu')]
                col_e = [c for c in cols_s_tab if str(c).lower().startswith('evad')]
                col_cur = [c for c in cols_s_tab if 'em curso' in str(c).lower()]

                df_s_tab['Concluintes'] = df_s_tab[col_c].sum(axis=1) if col_c else 0
                df_s_tab['Evadidos'] = df_s_tab[col_e].sum(axis=1) if col_e else 0
                df_s_tab['Em Curso'] = df_s_tab[col_cur].sum(axis=1) if col_cur else 0

                df_unificada = pd.merge(df_g_tab, df_s_tab[cols_chave + ['Concluintes', 'Em Curso', 'Evadidos']], on=cols_chave, how='outer').fillna(0)

                df_unificada['FEC (Fator de Esforço do Curso)'] = (df_unificada['Matrículas Equivalentes'] / df_unificada['Matrículas']).fillna(0)
                df_unificada['Candidato x Vaga'] = (df_unificada['Inscritos'] / df_unificada['Vagas']).fillna(0)

                cols_finais = [
                    'Ano', 'Modalidade de Ensino', 'Tipo de Curso', 'Tipo de Oferta', 'Nome do Curso', 'Turno do Curso',
                    'Matrículas', 'Matrículas Equivalentes', 'FEC (Fator de Esforço do Curso)', 'Vagas', 'Inscritos', 
                    'Candidato x Vaga', 'Concluintes', 'Em Curso', 'Evadidos'
                ]
                
                df_exibicao_unica = df_unificada[cols_finais].copy()

                if modo_vis_sit == "Valor em %":
                    soma_linha_sit = df_exibicao_unica['Concluintes'] + df_exibicao_unica['Em Curso'] + df_exibicao_unica['Evadidos']
                    df_exibicao_unica['Concluintes'] = (df_exibicao_unica['Concluintes'] / soma_linha_sit * 100).fillna(0).apply(lambda x: f"{fmt_br(x, 1)}%")
                    df_exibicao_unica['Em Curso'] = (df_exibicao_unica['Em Curso'] / soma_linha_sit * 100).fillna(0).apply(lambda x: f"{fmt_br(x, 1)}%")
                    df_exibicao_unica['Evadidos'] = (df_exibicao_unica['Evadidos'] / soma_linha_sit * 100).fillna(0).apply(lambda x: f"{fmt_br(x, 1)}%")
                else:
                    df_exibicao_unica['Concluintes'] = df_exibicao_unica['Concluintes'].apply(lambda x: fmt_br(x, 0))
                    df_exibicao_unica['Em Curso'] = df_exibicao_unica['Em Curso'].apply(lambda x: fmt_br(x, 0))
                    df_exibicao_unica['Evadidos'] = df_exibicao_unica['Evadidos'].apply(lambda x: fmt_br(x, 0))

                df_exibicao_unica['Matrículas'] = df_exibicao_unica['Matrículas'].apply(lambda x: fmt_br(x, 0))
                df_exibicao_unica['Matrículas Equivalentes'] = df_exibicao_unica['Matrículas Equivalentes'].apply(lambda x: fmt_br(x, 0))
                df_exibicao_unica['Vagas'] = df_exibicao_unica['Vagas'].apply(lambda x: fmt_br(x, 0))
                df_exibicao_unica['Inscritos'] = df_exibicao_unica['Inscritos'].apply(lambda x: fmt_br(x, 0))
                
                df_exibicao_unica['FEC (Fator de Esforço do Curso)'] = df_exibicao_unica['FEC (Fator de Esforço do Curso)'].apply(lambda x: fmt_br(x, 2))
                df_exibicao_unica['Candidato x Vaga'] = df_exibicao_unica['Candidato x Vaga'].apply(lambda x: fmt_br(x, 2))

                st.dataframe(
                    df_exibicao_unica.sort_values(by=['Ano', 'Nome do Curso'], ascending=[False, True]), 
                    width="stretch", 
                    hide_index=True
                )

        except FileNotFoundError as fnf_err:
            st.error(f"Arquivo de dados não encontrado: {fnf_err}")
        except Exception as e:
            st.error(f"Erro ao carregar dados da PNP - Situação da Matrícula: {e}")

    with tab2:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_rap_path = os.path.join(script_dir, 'CI_PNP_Rap.csv')
            
            try:
                df_rap = pd.read_csv(csv_rap_path, sep=";", encoding="utf-8")
            except UnicodeDecodeError:
                df_rap = pd.read_csv(csv_rap_path, sep=";", encoding="latin1")
                
            df_rap.columns = df_rap.columns.str.strip()
            
            cols_percent = ['Técnico', 'Formação de Professores', 'Proeja']
            for col in cols_percent:
                if col in df_rap.columns and str(df_rap[col].dtype) in ['object', 'string']:
                    df_rap[col] = df_rap[col].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False).astype(float)
                    
            cols_float = ['RAP Presencial', 'Matrículas Equivalentes RAP Presencial', 'RAP', 'Matrículas Equivalentes RAP']
            for col in cols_float:
                if col in df_rap.columns and str(df_rap[col].dtype) in ['object', 'string']:
                    df_rap[col] = df_rap[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
                    
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTRO</p>", unsafe_allow_html=True)
            
            anos_opts = sorted(list(df_rap['Ano'].dropna().unique()), reverse=True)
            if 'f_anos_pnp_rap' not in st.session_state:
                st.session_state.f_anos_pnp_rap = []
                
            anos_opts = sorted(list(set(anos_opts + st.session_state.f_anos_pnp_rap)), reverse=True)
            st.session_state.f_anos_pnp_rap = st.multiselect("Ano", anos_opts, default=st.session_state.f_anos_pnp_rap, placeholder="Todos os anos")
            
            st.markdown("---")
            df_rap_filtrado = df_rap.copy()
            if st.session_state.f_anos_pnp_rap:
                df_rap_filtrado = df_rap_filtrado[df_rap_filtrado['Ano'].isin(st.session_state.f_anos_pnp_rap)]
                
            val_rap = df_rap_filtrado['RAP'].mean() if not df_rap_filtrado.empty else 0
            val_rap_pres = df_rap_filtrado['RAP Presencial'].mean() if not df_rap_filtrado.empty else 0
            val_prof_eq = df_rap_filtrado['Professor Equivalente'].sum() if not df_rap_filtrado.empty else 0
            val_mat_eq = df_rap_filtrado['Matrículas Equivalentes RAP'].sum() if not df_rap_filtrado.empty else 0
            val_mat_eq_pres = df_rap_filtrado['Matrículas Equivalentes RAP Presencial'].sum() if not df_rap_filtrado.empty else 0
            
            val_tec = df_rap_filtrado['Técnico'].mean() if not df_rap_filtrado.empty else 0
            val_form = df_rap_filtrado['Formação de Professores'].mean() if not df_rap_filtrado.empty else 0
            val_pro = df_rap_filtrado['Proeja'].mean() if not df_rap_filtrado.empty else 0
            
            box_style = """
            <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;'>
                <p style='color: #666; font-size: 0.95rem; margin-bottom: 5px; font-weight: bold;'>{title}</p>
                <h2 style='color: #006633; margin-top: 0px; font-size: 1.8rem;'>{value}</h2>
            </div>
            """
            
            val_ano = ", ".join(map(str, sorted(df_rap_filtrado['Ano'].unique(), reverse=True))) if not df_rap_filtrado.empty else "-"
            if len(df_rap_filtrado['Ano'].unique()) > 3:
                val_ano = "Vários"
                
            c1, c2, c3 = st.columns(3)
            c1.markdown(box_style.format(title="Ano(s)", value=val_ano), unsafe_allow_html=True)
            c2.markdown(box_style.format(title="RAP", value=fmt_br(val_rap, 2)), unsafe_allow_html=True)
            c3.markdown(box_style.format(title="RAP Presencial", value=fmt_br(val_rap_pres, 2)), unsafe_allow_html=True)
            
            c4, c5, c6 = st.columns(3)
            c4.markdown(box_style.format(title="Mat. Eq. RAP", value=fmt_br(val_mat_eq, 0)), unsafe_allow_html=True)
            c5.markdown(box_style.format(title="Mat. Eq. Presencial", value=fmt_br(val_mat_eq_pres, 0)), unsafe_allow_html=True)
            c6.markdown(box_style.format(title="Prof. Equivalente", value=fmt_br(val_prof_eq, 0)), unsafe_allow_html=True)
            
            c7, c8, c9 = st.columns(3)
            c7.markdown(box_style.format(title="Técnico", value=f"{fmt_br(val_tec, 1)}%"), unsafe_allow_html=True)
            c8.markdown(box_style.format(title="Formação de Professores", value=f"{fmt_br(val_form, 1)}%"), unsafe_allow_html=True)
            c9.markdown(box_style.format(title="Proeja", value=f"{fmt_br(val_pro, 1)}%"), unsafe_allow_html=True)
            
            st.markdown("<br><p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📈 EVOLUÇÃO</p>", unsafe_allow_html=True)
            
            st.markdown("**Evolução do RAP (Meta RAP Presencial >= 20)**")
            df_g_rap = df_rap_filtrado.groupby('Ano')[['RAP', 'RAP Presencial']].mean().reset_index()
            df_g_rap.rename(columns={'RAP': 'RAP Total'}, inplace=True)
            df_g_rap_melt = df_g_rap.melt(id_vars='Ano', value_vars=['RAP Total', 'RAP Presencial'], var_name='Indicador', value_name='Valor')
            df_g_rap_melt['Valor_Txt'] = df_g_rap_melt['Valor'].apply(lambda x: fmt_br(x, 1))

            x_axis_rap = alt.Axis(title='Ano', grid=True, gridColor='#EAEAEA')
            y_axis_rap = alt.Axis(title='RAP', format=',.1f', labelExpr="replace(datum.label, ',', '.')")

            base_rap = alt.Chart(df_g_rap_melt).encode(x=alt.X('Ano:O', axis=x_axis_rap), xOffset='Indicador:N')
            max_rap = df_g_rap_melt['Valor'].max() if not df_g_rap_melt.empty else 1
            bar_rap = base_rap.mark_bar().encode(
                y=alt.Y('Valor:Q', axis=y_axis_rap, scale=alt.Scale(domain=[0, max_rap * 1.15])),
                color=alt.condition(
                    alt.datum.Valor < 20,
                    alt.value('#E53935'), 
                    alt.Color('Indicador:N', scale=alt.Scale(range=['#4CAF50', '#81C784']), legend=alt.Legend(orient='bottom', title=None))
                ),
                tooltip=['Ano', 'Indicador', alt.Tooltip('Valor:Q', title='Valor', format='.2f')]
            )
            text_rap = base_rap.mark_text(align='center', baseline='bottom', dy=-2, fontWeight='bold').encode(
                y=alt.Y('Valor:Q'),
                text=alt.Text('Valor_Txt:N'),
                color=alt.condition(alt.datum.Valor < 20, alt.value('#E53935'), alt.value('black'))
            )
            chart_rap = (bar_rap + text_rap).properties(height=300).interactive()
            st.altair_chart(chart_rap, width="stretch")
                
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**Evolução do Professor Equivalente**")
            df_g_prof = df_rap_filtrado.groupby('Ano')[['Professor Equivalente']].sum().reset_index()
            df_g_prof['Prof_Txt'] = df_g_prof['Professor Equivalente'].apply(lambda x: fmt_br(x, 0))
            max_prof = df_g_prof['Professor Equivalente'].max() if not df_g_prof.empty else 1
            
            base_prof = alt.Chart(df_g_prof).encode(x=alt.X('Ano:O', axis=x_axis_rap))
            bar_prof = base_prof.mark_bar(color='#006633').encode(
                y=alt.Y('Professor Equivalente:Q', axis=alt.Axis(title='Quant. Prof. Equiv.', format=',d', labelExpr="replace(datum.label, ',', '.')"), scale=alt.Scale(domain=[0, max_prof * 1.15])),
                tooltip=['Ano', 'Professor Equivalente']
            )
            text_prof = base_prof.mark_text(align='center', baseline='bottom', dy=-2, fontWeight='bold').encode(
                y=alt.Y('Professor Equivalente:Q'),
                text=alt.Text('Prof_Txt:N')
            )
            chart_prof = (bar_prof + text_prof).properties(height=300).interactive()
            st.altair_chart(chart_prof, width="stretch")
            
            st.markdown("**Matrículas Equivalentes: RAP vs Presencial**")
            df_g_mat = df_rap_filtrado.groupby('Ano')[['Matrículas Equivalentes RAP', 'Matrículas Equivalentes RAP Presencial']].sum().reset_index()
            df_g_mat.rename(columns={
                'Matrículas Equivalentes RAP': 'RAP Total',
                'Matrículas Equivalentes RAP Presencial': 'RAP Presencial'
            }, inplace=True)
            
            df_g_mat_melt = df_g_mat.melt(id_vars='Ano', value_vars=['RAP Total', 'RAP Presencial'], var_name='Tipo', value_name='Total')
            df_g_mat_melt['Total_Txt'] = df_g_mat_melt['Total'].apply(lambda x: fmt_br(x, 0))

            base_mat = alt.Chart(df_g_mat_melt).encode(x=alt.X('Ano:O', axis=x_axis_rap), xOffset='Tipo:N')
            max_mat = df_g_mat_melt['Total'].max() if not df_g_mat_melt.empty else 1
            bar_mat = base_mat.mark_bar().encode(
                y=alt.Y('Total:Q', axis=alt.Axis(title='Mat. Equiv. RAP', format=',d', labelExpr="replace(datum.label, ',', '.')"), scale=alt.Scale(domain=[0, max_mat * 1.15])),
                color=alt.Color('Tipo:N', legend=alt.Legend(orient='bottom', title=None), scale=alt.Scale(range=['#4CAF50', '#81C784'])),
                tooltip=['Ano', 'Tipo', alt.Tooltip('Total:Q', format=',.0f')]
            )
            text_mat = base_mat.mark_text(align='center', baseline='bottom', dy=-2, fontWeight='bold').encode(
                y=alt.Y('Total:Q'),
                text=alt.Text('Total_Txt:N')
            )
            chart_mat = (bar_mat + text_mat).properties(height=300).interactive()
            st.altair_chart(chart_mat, width="stretch")
            
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 5px;'>📊 INDICADORES DE PERCENTUAIS LEGAIS</p>", unsafe_allow_html=True)
            st.markdown("<p style='color: #666; font-size: 0.95rem; margin-bottom: 20px;'>Técnico (Meta &gt;= 50%); Formação de Professores (Meta &gt;= 20%); Proeja (Meta &gt;= 10%)</p>", unsafe_allow_html=True)
            
            df_g_leg = df_rap_filtrado.groupby('Ano')[['Técnico', 'Formação de Professores', 'Proeja']].mean().reset_index()
            df_g_leg_melt = df_g_leg.melt(id_vars='Ano', value_vars=['Técnico', 'Formação de Professores', 'Proeja'], var_name='Indicador Legal', value_name='Percentual')
            df_g_leg_melt['Percentual_Txt'] = df_g_leg_melt['Percentual'].apply(lambda x: fmt_br(x, 1))

            df_g_leg_melt['AbaixoMeta'] = False
            mask_tec = (df_g_leg_melt['Indicador Legal'] == 'Técnico') & (df_g_leg_melt['Percentual'] < 50)
            mask_form = (df_g_leg_melt['Indicador Legal'] == 'Formação de Professores') & (df_g_leg_melt['Percentual'] < 20)
            mask_pro = (df_g_leg_melt['Indicador Legal'] == 'Proeja') & (df_g_leg_melt['Percentual'] < 10)
            df_g_leg_melt.loc[mask_tec | mask_form | mask_pro, 'AbaixoMeta'] = True
            
            base_leg = alt.Chart(df_g_leg_melt).encode(x=alt.X('Ano:O', axis=x_axis_rap))
            max_leg = df_g_leg_melt['Percentual'].max() if not df_g_leg_melt.empty else 1
            line_leg = base_leg.mark_line(point=False).encode(
                y=alt.Y('Percentual:Q', axis=alt.Axis(title='Percentual (%)', format=',.1f', labelExpr="replace(datum.label, ',', '.')"), scale=alt.Scale(domain=[0, max_leg * 1.15])),
                color=alt.Color('Indicador Legal:N', legend=alt.Legend(orient='bottom', title=None))
            )
            point_leg = base_leg.mark_circle(size=60).encode(
                y=alt.Y('Percentual:Q'),
                color=alt.condition(alt.datum.AbaixoMeta, alt.value('#E53935'), alt.Color('Indicador Legal:N')),
                tooltip=['Ano', 'Indicador Legal', alt.Tooltip('Percentual:Q', format='.1f')]
            )
            text_leg = base_leg.mark_text(align='center', baseline='bottom', dy=-8, fontWeight='bold').encode(
                y=alt.Y('Percentual:Q'),
                text=alt.Text('Percentual_Txt:N'),
                color=alt.condition(alt.datum.AbaixoMeta, alt.value('#E53935'), alt.value('black'))
            )
            
            chart_legais = (line_leg + point_leg + text_leg).properties(height=350).interactive()
            st.altair_chart(chart_legais, width="stretch")
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📊 Consultar Tabela Geral - Indicadores Legais e RAP", expanded=True):
                cols_necessarias = ['Ano', 'Técnico', 'Formação de Professores', 'Proeja', 'RAP Presencial', 'Matrículas Equivalentes RAP Presencial', 'RAP', 'Matrículas Equivalentes RAP', 'Professor Equivalente']
                cols_presentes = [c for c in cols_necessarias if c in df_rap_filtrado.columns]
                
                df_exibicao = df_rap_filtrado[cols_presentes].copy()
                
                for col in ['Técnico', 'Formação de Professores', 'Proeja']:
                    if col in df_exibicao.columns:
                        df_exibicao[col] = df_exibicao[col].apply(lambda x: f"{fmt_br(x, 1)}%" if pd.notnull(x) else x)

                cols_rap_mat = ['RAP Presencial', 'Matrículas Equivalentes RAP Presencial', 'RAP', 'Matrículas Equivalentes RAP', 'Professor Equivalente']
                for col in cols_rap_mat:
                    if col in df_exibicao.columns:
                        df_exibicao[col] = df_exibicao[col].apply(lambda x: fmt_br(x, 2) if pd.notnull(x) else x)
                        
                df_exibicao.rename(columns={'RAP': 'RAP Total', 'Matrículas Equivalentes RAP': 'Matrículas Equivalentes RAP Total'}, inplace=True, errors='ignore')
                
                def style_meta(row):
                    styles = [''] * len(row)
                    if 'RAP Total' in row.index and pd.notnull(row['RAP Total']):
                        try:
                            val_rap = float(str(row['RAP Total']).replace('.', '').replace(',', '.'))
                            if val_rap < 20:
                                styles[row.index.get_loc('RAP Total')] = 'color: #E53935; font-weight: bold;'
                        except ValueError:
                            pass

                    if 'RAP Presencial' in row.index and pd.notnull(row['RAP Presencial']):
                        try:
                            val_rap_p = float(str(row['RAP Presencial']).replace('.', '').replace(',', '.'))
                            if val_rap_p < 20:
                                styles[row.index.get_loc('RAP Presencial')] = 'color: #E53935; font-weight: bold;'
                        except ValueError:
                            pass
                        
                    for col, meta in [('Técnico', 50), ('Formação de Professores', 20), ('Proeja', 10)]:
                        if col in row.index and pd.notnull(row[col]):
                            try:
                                val = float(str(row[col]).replace('%', '').replace('.', '').replace(',', '.'))
                                if val < meta:
                                    styles[row.index.get_loc(col)] = 'color: #E53935; font-weight: bold;'
                            except ValueError:
                                pass
                    return styles
                
                df_styler = df_exibicao.sort_values(by='Ano', ascending=False).style.apply(style_meta, axis=1)
                st.dataframe(df_styler, width="stretch", hide_index=True)
                
        except FileNotFoundError:
            st.error("Arquivo 'CI_PNP_Rap.csv' não encontrado.")
        except Exception as e:
            st.error(f"Erro ao carregar dados da PNP - % Legais e RAP: {e}")

    with tab3:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_efic_path = os.path.join(script_dir, 'CI_PNP_Efic.csv')
            
            try:
                df_efic = pd.read_csv(csv_efic_path, sep=";", encoding="utf-8")
            except UnicodeDecodeError:
                df_efic = pd.read_csv(csv_efic_path, sep=";", encoding="latin1")
                
            df_efic.columns = df_efic.columns.str.strip()

            if 'Eficiência Acadêmica' in df_efic.columns:
                df_efic['Eficiência Acadêmica'] = df_efic['Eficiência Acadêmica'].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
                df_efic['Eficiência Acadêmica'] = pd.to_numeric(df_efic['Eficiência Acadêmica'], errors='coerce').fillna(0)

            for col_ciclo in ['Conclusão Ciclo', 'Evasão Ciclo', 'Retenção Ciclo']:
                if col_ciclo in df_efic.columns:
                    df_efic[col_ciclo] = df_efic[col_ciclo].astype(str).str.strip()
                    df_efic[col_ciclo] = pd.to_numeric(df_efic[col_ciclo], errors='coerce').fillna(0)

            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA</p>", unsafe_allow_html=True)
            
            for f_key in ['f_anos_pnp_efic', 'f_mod_pnp_efic', 'f_tipo_curso_pnp_efic', 'f_tipo_oferta_pnp_efic', 'f_nome_curso_pnp_efic', 'f_turno_pnp_efic']:
                if f_key not in st.session_state:
                    st.session_state[f_key] = []

            def get_opts_efic(col):
                df_temp = df_efic.copy()
                if col != 'Ano' and st.session_state.f_anos_pnp_efic: df_temp = df_temp[df_temp['Ano'].isin(st.session_state.f_anos_pnp_efic)]
                if col != 'Modalidade de Ensino' and st.session_state.f_mod_pnp_efic: df_temp = df_temp[df_temp['Modalidade de Ensino'].isin(st.session_state.f_mod_pnp_efic)]
                if col != 'Tipo de Curso' and st.session_state.f_tipo_curso_pnp_efic: df_temp = df_temp[df_temp['Tipo de Curso'].isin(st.session_state.f_tipo_curso_pnp_efic)]
                if col != 'Tipo de Oferta' and st.session_state.f_tipo_oferta_pnp_efic: df_temp = df_temp[df_temp['Tipo de Oferta'].isin(st.session_state.f_tipo_oferta_pnp_efic)]
                if col != 'Nome do Curso' and st.session_state.f_nome_curso_pnp_efic: df_temp = df_temp[df_temp['Nome do Curso'].isin(st.session_state.f_nome_curso_pnp_efic)]
                if col != 'Turno do Curso' and st.session_state.f_turno_pnp_efic: df_temp = df_temp[df_temp['Turno do Curso'].isin(st.session_state.f_turno_pnp_efic)]
                
                opts = sorted(list(df_temp[col].dropna().unique()))
                if col == 'Ano':
                    opts = sorted(list(set(opts + st.session_state.f_anos_pnp_efic)), reverse=True)
                return opts

            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                st.session_state.f_anos_pnp_efic = st.multiselect(
                    "Ano", get_opts_efic('Ano'), default=st.session_state.f_anos_pnp_efic, placeholder="Todos os anos", key="ms_efic_ano"
                )
                st.session_state.f_mod_pnp_efic = st.multiselect(
                    "Modalidade de Ensino", get_opts_efic('Modalidade de Ensino'), default=st.session_state.f_mod_pnp_efic, placeholder="Todas", key="ms_efic_mod"
                )
            with f_col2:
                st.session_state.f_tipo_curso_pnp_efic = st.multiselect(
                    "Tipo de Curso", get_opts_efic('Tipo de Curso'), default=st.session_state.f_tipo_curso_pnp_efic, placeholder="Todos", key="ms_efic_tipo_curso"
                )
                st.session_state.f_tipo_oferta_pnp_efic = st.multiselect(
                    "Tipo de Oferta", get_opts_efic('Tipo de Oferta'), default=st.session_state.f_tipo_oferta_pnp_efic, placeholder="Todas", key="ms_efic_tipo_oferta"
                )
            with f_col3:
                st.session_state.f_nome_curso_pnp_efic = st.multiselect(
                    "Nome do Curso", get_opts_efic('Nome do Curso'), default=st.session_state.f_nome_curso_pnp_efic, placeholder="Todos", key="ms_efic_nome_curso"
                )
                st.session_state.f_turno_pnp_efic = st.multiselect(
                    "Turno do Curso", get_opts_efic('Turno do Curso'), default=st.session_state.f_turno_pnp_efic, placeholder="Todos", key="ms_efic_turno"
                )

            df_efic_filtrado = df_efic.copy()
            if st.session_state.f_anos_pnp_efic: df_efic_filtrado = df_efic_filtrado[df_efic_filtrado['Ano'].isin(st.session_state.f_anos_pnp_efic)]
            if st.session_state.f_mod_pnp_efic: df_efic_filtrado = df_efic_filtrado[df_efic_filtrado['Modalidade de Ensino'].isin(st.session_state.f_mod_pnp_efic)]
            if st.session_state.f_tipo_curso_pnp_efic: df_efic_filtrado = df_efic_filtrado[df_efic_filtrado['Tipo de Curso'].isin(st.session_state.f_tipo_curso_pnp_efic)]
            if st.session_state.f_tipo_oferta_pnp_efic: df_efic_filtrado = df_efic_filtrado[df_efic_filtrado['Tipo de Oferta'].isin(st.session_state.f_tipo_oferta_pnp_efic)]
            if st.session_state.f_nome_curso_pnp_efic: df_efic_filtrado = df_efic_filtrado[df_efic_filtrado['Nome do Curso'].isin(st.session_state.f_nome_curso_pnp_efic)]
            if st.session_state.f_turno_pnp_efic: df_efic_filtrado = df_efic_filtrado[df_efic_filtrado['Turno do Curso'].isin(st.session_state.f_turno_pnp_efic)]

            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

            modo_visualizacao = st.radio(
                "Modo de Exibição dos Indicadores de Ciclo:",
                ["Valor Absoluto", "Valor em %"],
                horizontal=True,
                key="radio_modo_visualizacao_efic"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            val_ano = ", ".join(map(str, sorted(df_efic_filtrado['Ano'].unique(), reverse=True))) if not df_efic_filtrado.empty else "-"
            if len(df_efic_filtrado['Ano'].unique()) > 3:
                val_ano = "Vários"

            total_conc = df_efic_filtrado['Conclusão Ciclo'].sum() if not df_efic_filtrado.empty else 0
            total_evas = df_efic_filtrado['Evasão Ciclo'].sum() if not df_efic_filtrado.empty else 0
            total_rete = df_efic_filtrado['Retenção Ciclo'].sum() if not df_efic_filtrado.empty else 0
            soma_ciclo = total_conc + total_evas + total_rete

            soma_conc_evas = total_conc + total_evas
            val_efic = (total_conc / soma_conc_evas * 100) if soma_conc_evas > 0 else 0

            if modo_visualizacao == "Valor em %" and soma_ciclo > 0:
                str_conc = f"{fmt_br((total_conc / soma_ciclo) * 100, 1)}%"
                str_evas = f"{fmt_br((total_evas / soma_ciclo) * 100, 1)}%"
                str_rete = f"{fmt_br((total_rete / soma_ciclo) * 100, 1)}%"
            else:
                str_conc = fmt_br(total_conc, 0)
                str_evas = fmt_br(total_evas, 0)
                str_rete = fmt_br(total_rete, 0)

            box_style = """
            <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;'>
                <p style='color: #666; font-size: 0.95rem; margin-bottom: 5px; font-weight: bold;'>{title}</p>
                <h2 style='color: #006633; margin-top: 0px; font-size: 1.8rem;'>{value}</h2>
            </div>
            """

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.markdown(box_style.format(title="Ano(s)", value=val_ano), unsafe_allow_html=True)
            c2.markdown(box_style.format(title="Eficiência Acadêmica", value=f"{fmt_br(val_efic, 2)}%"), unsafe_allow_html=True)
            c3.markdown(box_style.format(title="Conclusão Ciclo", value=str_conc), unsafe_allow_html=True)
            c4.markdown(box_style.format(title="Evasão Ciclo", value=str_evas), unsafe_allow_html=True)
            c5.markdown(box_style.format(title="Retenção Ciclo", value=str_rete), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if not df_efic_filtrado.empty:
                df_curso_efic = df_efic_filtrado.groupby(['Nome do Curso', 'Tipo de Curso', 'Tipo de Oferta'])[['Conclusão Ciclo', 'Evasão Ciclo']].sum().reset_index()
                
                soma_c_e_curso = df_curso_efic['Conclusão Ciclo'] + df_curso_efic['Evasão Ciclo']
                df_curso_efic['Eficiência Acadêmica'] = (df_curso_efic['Conclusão Ciclo'] / soma_c_e_curso * 100).fillna(0)
                
                df_curso_efic['Curso_Identificador'] = df_curso_efic['Nome do Curso'] + " - " + df_curso_efic['Tipo de Curso'] + " - " + df_curso_efic['Tipo de Oferta']

                top_piores = df_curso_efic.sort_values(by='Eficiência Acadêmica', ascending=True).head(5)
                top_melhores = df_curso_efic.sort_values(by='Eficiência Acadêmica', ascending=False).head(5)

                card_list_style = """
                <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px 20px; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 100%;'>
                    <p style='color: {color}; font-size: 1.05rem; margin-bottom: 10px; font-weight: bold; text-align: center;'>{title}</p>
                    <ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>
                        {items}
                    </ul>
                </div>
                """

                items_piores = "".join([
                    f"<li style='display: flex; justify-content: space-between; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.88rem; color: #333;'>"
                    f"<span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80%;' title='{row['Curso_Identificador']}'>• {row['Curso_Identificador']}</span>"
                    f"<strong style='color: #E53935;'>{fmt_br(row['Eficiência Acadêmica'], 2)}%</strong></li>"
                    for _, row in top_piores.iterrows()
                ])

                items_melhores = "".join([
                    f"<li style='display: flex; justify-content: space-between; border-bottom: 1px solid #f0f0f0; padding: 6px 0; font-size: 0.88rem; color: #333;'>"
                    f"<span style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80%;' title='{row['Curso_Identificador']}'>• {row['Curso_Identificador']}</span>"
                    f"<strong style='color: #006633;'>{fmt_br(row['Eficiência Acadêmica'], 2)}%</strong></li>"
                    for _, row in top_melhores.iterrows()
                ])

                col_piores, col_melhores = st.columns(2)
                with col_piores:
                    st.markdown(card_list_style.format(title="📉 Cursos com Piores Eficiências Acadêmicas", color="#E53935", items=items_piores), unsafe_allow_html=True)
                with col_melhores:
                    st.markdown(card_list_style.format(title="📈 Cursos com Melhores Eficiências Acadêmicas", color="#006633", items=items_melhores), unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📈 EVOLUÇÃO POR ANO</p>", unsafe_allow_html=True)

            df_g_ano = df_efic_filtrado.groupby('Ano')[['Conclusão Ciclo', 'Evasão Ciclo', 'Retenção Ciclo']].sum().reset_index()

            soma_c_e_ano = df_g_ano['Conclusão Ciclo'] + df_g_ano['Evasão Ciclo']
            df_g_ano['Eficiência Acadêmica'] = (df_g_ano['Conclusão Ciclo'] / soma_c_e_ano * 100).fillna(0)
            df_g_ano['Eficiencia_Txt'] = df_g_ano['Eficiência Acadêmica'].apply(lambda x: fmt_br(x, 1))

            df_g_ano['Soma_Ciclos'] = df_g_ano['Conclusão Ciclo'] + df_g_ano['Evasão Ciclo'] + df_g_ano['Retenção Ciclo']

            if modo_visualizacao == "Valor em %":
                df_g_ano['Conclusão Ciclo Chart'] = (df_g_ano['Conclusão Ciclo'] / df_g_ano['Soma_Ciclos']) * 100
                df_g_ano['Evasão Ciclo Chart'] = (df_g_ano['Evasão Ciclo'] / df_g_ano['Soma_Ciclos']) * 100
                df_g_ano['Retenção Ciclo Chart'] = (df_g_ano['Retenção Ciclo'] / df_g_ano['Soma_Ciclos']) * 100
                
                df_g_ano['Conc_Txt'] = df_g_ano['Conclusão Ciclo Chart'].apply(lambda x: fmt_br(x, 1))
                df_g_ano['Evas_Txt'] = df_g_ano['Evasão Ciclo Chart'].apply(lambda x: fmt_br(x, 1))
                df_g_ano['Rete_Txt'] = df_g_ano['Retenção Ciclo Chart'].apply(lambda x: fmt_br(x, 1))
                sufixo_fmt = "%"
            else:
                df_g_ano['Conclusão Ciclo Chart'] = df_g_ano['Conclusão Ciclo']
                df_g_ano['Evasão Ciclo Chart'] = df_g_ano['Evasão Ciclo']
                df_g_ano['Retenção Ciclo Chart'] = df_g_ano['Retenção Ciclo']
                
                df_g_ano['Conc_Txt'] = df_g_ano['Conclusão Ciclo Chart'].apply(lambda x: fmt_br(x, 0))
                df_g_ano['Evas_Txt'] = df_g_ano['Evasão Ciclo Chart'].apply(lambda x: fmt_br(x, 0))
                df_g_ano['Rete_Txt'] = df_g_ano['Retenção Ciclo Chart'].apply(lambda x: fmt_br(x, 0))
                sufixo_fmt = ""

            def criar_grafico_barra_efic(df_dados, col_y, col_txt, titulo_y, cor_barra, is_pct_chart=False):
                if df_dados.empty:
                    return alt.Chart(pd.DataFrame()).mark_bar()
                
                max_val = df_dados[col_y].max()
                escala_max = max(1.0, float(max_val) * 1.18) if pd.notnull(max_val) and max_val > 0 else 1.0

                if is_pct_chart:
                    axis_y_ef = alt.Axis(title=titulo_y, format=',.1f', labelExpr="replace(datum.label, ',', '.')")
                else:
                    axis_y_ef = alt.Axis(title=titulo_y, format=',d', labelExpr="replace(datum.label, ',', '.')")

                base = alt.Chart(df_dados).encode(x=alt.X('Ano:O', axis=alt.Axis(title='Ano', grid=True, gridColor='#EAEAEA')))
                barras = base.mark_bar(color=cor_barra).encode(
                    y=alt.Y(f'{col_y}:Q', axis=axis_y_ef, scale=alt.Scale(domain=[0, escala_max])),
                    tooltip=['Ano:O', alt.Tooltip(f'{col_y}:Q', title=titulo_y, format='.2f')]
                )
                textos = base.mark_text(align='center', baseline='bottom', dy=-4, fontWeight='bold').encode(
                    y=alt.Y(f'{col_y}:Q'),
                    text=alt.Text(f'{col_txt}:N')
                )
                return (barras + textos).properties(height=280).interactive()

            g_col1, g_col2 = st.columns(2)
            with g_col1:
                st.markdown("**Eficiência Acadêmica (%)**")
                st.altair_chart(criar_grafico_barra_efic(df_g_ano, 'Eficiência Acadêmica', 'Eficiencia_Txt', 'Eficiência (%)', '#006633', is_pct_chart=True), width="stretch")

                st.markdown(f"**Evasão Ciclo ({modo_visualizacao})**")
                st.altair_chart(criar_grafico_barra_efic(df_g_ano, 'Evasão Ciclo Chart', 'Evas_Txt', f'Evasão ({sufixo_fmt})', '#E53935', is_pct_chart=(modo_visualizacao == "Valor em %")), width="stretch")

            with g_col2:
                st.markdown(f"**Conclusão Ciclo ({modo_visualizacao})**")
                st.altair_chart(criar_grafico_barra_efic(df_g_ano, 'Conclusão Ciclo Chart', 'Conc_Txt', f'Conclusão ({sufixo_fmt})', '#4CAF50', is_pct_chart=(modo_visualizacao == "Valor em %")), width="stretch")

                st.markdown(f"**Retenção Ciclo ({modo_visualizacao})**")
                st.altair_chart(criar_grafico_barra_efic(df_g_ano, 'Retenção Ciclo Chart', 'Rete_Txt', f'Retenção ({sufixo_fmt})', '#FF9800', is_pct_chart=(modo_visualizacao == "Valor em %")), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)

            with st.expander("📊 Consultar Tabela Geral - Eficiência Acadêmica", expanded=True):
                cols_tabela = ['Ano', 'Modalidade de Ensino', 'Tipo de Curso', 'Tipo de Oferta', 'Nome do Curso', 'Turno do Curso', 'Eficiência Acadêmica', 'Conclusão Ciclo', 'Evasão Ciclo', 'Retenção Ciclo']
                cols_existentes = [c for c in cols_tabela if c in df_efic_filtrado.columns]
                
                df_exibicao_efic = df_efic_filtrado[cols_existentes].copy()

                if modo_visualizacao == "Valor em %":
                    soma_linhas = df_exibicao_efic['Conclusão Ciclo'] + df_exibicao_efic['Evasão Ciclo'] + df_exibicao_efic['Retenção Ciclo']
                    df_exibicao_efic['Conclusão Ciclo'] = (df_exibicao_efic['Conclusão Ciclo'] / soma_linhas * 100).fillna(0).apply(lambda x: f"{fmt_br(x, 1)}%")
                    df_exibicao_efic['Evasão Ciclo'] = (df_exibicao_efic['Evasão Ciclo'] / soma_linhas * 100).fillna(0).apply(lambda x: f"{fmt_br(x, 1)}%")
                    df_exibicao_efic['Retenção Ciclo'] = (df_exibicao_efic['Retenção Ciclo'] / soma_linhas * 100).fillna(0).apply(lambda x: f"{fmt_br(x, 1)}%")
                else:
                    df_exibicao_efic['Conclusão Ciclo'] = df_exibicao_efic['Conclusão Ciclo'].apply(lambda x: fmt_br(x, 0))
                    df_exibicao_efic['Evasão Ciclo'] = df_exibicao_efic['Evasão Ciclo'].apply(lambda x: fmt_br(x, 0))
                    df_exibicao_efic['Retenção Ciclo'] = df_exibicao_efic['Retenção Ciclo'].apply(lambda x: fmt_br(x, 0))

                soma_c_e_tab = df_efic_filtrado['Conclusão Ciclo'] + df_efic_filtrado['Evasão Ciclo']
                df_exibicao_efic['Eficiência Acadêmica'] = (df_efic_filtrado['Conclusão Ciclo'] / soma_c_e_tab * 100).fillna(0).apply(lambda x: f"{fmt_br(x, 2)}%")

                st.dataframe(
                    df_exibicao_efic.sort_values(by=['Ano', 'Nome do Curso'], ascending=[False, True]),
                    width="stretch",
                    hide_index=True
                )

        except FileNotFoundError:
            st.error("Arquivo 'CI_PNP_Efic.csv' não encontrado.")
        except Exception as e:
            st.error(f"Erro ao carregar dados da PNP - Eficiência Acadêmica: {e}")

# ------------------------------------------
# 5. ENEM
# ------------------------------------------
elif menu_opcao == "📝 Enem":
    st.markdown("### 📝 Dados do Enem")
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_enem_path = os.path.join(script_dir, 'CI_Enem.csv')
        
        try:
            df_enem = pd.read_csv(csv_enem_path, sep=";", decimal=",", encoding="utf-8")
        except UnicodeDecodeError:
            df_enem = pd.read_csv(csv_enem_path, sep=";", decimal=",", encoding="latin1")
            
        cols_medias = ['Média LC', 'Média CH', 'Média CN', 'Média MT', 'Média Redação', 'Média Objetivas', 'Média Geral']
        for col in cols_medias:
            if col in df_enem.columns and str(df_enem[col].dtype) in ['object', 'string']:
                df_enem[col] = df_enem[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
                    
        def criar_grafico_linhas_valores(df, cols, altura=350, cor_linha=None):
            df_melt = df.melt(id_vars=['Ano'], value_vars=cols, var_name='Indicador', value_name='Média')
            df_melt['Media_Txt'] = df_melt['Média'].apply(lambda x: fmt_br(x, 1))

            val_min = df_melt['Média'].min()
            val_max = df_melt['Média'].max()
            
            folga = (val_max - val_min) * 0.15 if (val_max - val_min) > 0 else 10
            y_min = max(0, float(val_min) - folga)
            y_max = float(val_max) + folga

            if cor_linha:
                cor_encode = alt.Color('Indicador:N', scale=alt.Scale(range=[cor_linha]), legend=None)
            else:
                cor_encode = alt.Color('Indicador:N', legend=alt.Legend(title="Médias", orient="bottom"))
                
            base = alt.Chart(df_melt).encode(
                x=alt.X('Ano:O', axis=alt.Axis(labelAngle=-90, title='Ano', grid=True, gridColor='#EAEAEA')),
                color=cor_encode,
                tooltip=[
                    alt.Tooltip('Ano:O', title='Ano'), 
                    alt.Tooltip('Indicador:N', title='Indicador'), 
                    alt.Tooltip('Média:Q', title='Nota', format='.2f')
                ]
            )
            
            linhas = base.mark_line(point=True, clip=False).encode(
                y=alt.Y('Média:Q', axis=alt.Axis(title='Média', format=',.1f', labelExpr="replace(datum.label, ',', '.')"), scale=alt.Scale(domain=[y_min, y_max]))
            )
            
            textos = base.mark_text(
                align='center', 
                baseline='bottom', 
                dy=-8, 
                fontSize=11, 
                fontWeight='bold',
                clip=False
            ).encode(
                y=alt.Y('Média:Q'), 
                text=alt.Text('Media_Txt:N')
            )
            
            return (linhas + textos).properties(height=altura).interactive()
            
        st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📈 MÉDIAS AO LONGO DOS ANOS</p>", unsafe_allow_html=True)
        cols_grupo1 = ['Média LC', 'Média CH', 'Média CN', 'Média MT']
        st.markdown("**Áreas de Conhecimento (LC, CH, CN, MT)**")
        st.altair_chart(criar_grafico_linhas_valores(df_enem, cols_grupo1), width="stretch")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        col_redacao, col_objetiva = st.columns(2)
        with col_redacao:
            st.markdown("**Média Redação**")
            st.altair_chart(criar_grafico_linhas_valores(df_enem, ['Média Redação'], altura=300, cor_linha='#E53935'), width="stretch")
            
        with col_objetiva:
            st.markdown("**Média Objetivas**")
            st.altair_chart(criar_grafico_linhas_valores(df_enem, ['Média Objetivas'], altura=300, cor_linha='#006633'), width="stretch")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Média Geral**")
        st.altair_chart(criar_grafico_linhas_valores(df_enem, ['Média Geral'], altura=300), width="stretch")
        
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📊 PARTICIPAÇÃO E RESULTADOS</p>", unsafe_allow_html=True)
        
        def criar_grafico_altair_enem(df_dados, coluna_y, cor_barra_padrao, formato=".0f", melhor='max'):
            destaque_val = df_dados[coluna_y].max() if melhor == 'max' else df_dados[coluna_y].min()
            cor_destaque = alt.condition(alt.datum[coluna_y] == destaque_val, alt.value('#006633'), alt.value(cor_barra_padrao))
            
            df_dados_plot = df_dados.copy()
            df_dados_plot['Valor_Txt'] = df_dados_plot[coluna_y].apply(lambda x: fmt_br(x, 0))

            val_max = df_dados_plot[coluna_y].max()
            escala_max = max(1.0, float(val_max) * 1.18) if pd.notnull(val_max) and val_max > 0 else 1.0

            base = alt.Chart(df_dados_plot).encode(
                x=alt.X('Ano:O', axis=alt.Axis(labelAngle=-90, title='Ano', grid=True, gridColor='#EAEAEA'))
            )
            
            barras = base.mark_bar().encode(
                y=alt.Y(f'{coluna_y}:Q', axis=alt.Axis(title=None, format=',d', labelExpr="replace(datum.label, ',', '.')"), scale=alt.Scale(domain=[0, escala_max])), 
                color=cor_destaque
            )
            
            textos = base.mark_text(align='center', baseline='bottom', dy=-4, color='black', fontWeight='bold').encode(
                y=alt.Y(f'{coluna_y}:Q'), 
                text=alt.Text('Valor_Txt:N')
            )
            
            return (barras + textos).properties(height=320)
            
        graf_col1, graf_col2 = st.columns(2)
        with graf_col1:
            st.markdown("**Alunos Participantes**")
            st.altair_chart(criar_grafico_altair_enem(df_enem, 'Alunos', '#66BB6A', melhor='max'), width="stretch")
            st.markdown("**Posição no Estado**")
            st.altair_chart(criar_grafico_altair_enem(df_enem, 'Posição Estado', '#4CAF50', melhor='min'), width="stretch")
            
        with graf_col2:
            st.markdown("**Posição no País**")
            st.altair_chart(criar_grafico_altair_enem(df_enem, 'Posição País', '#66BB6A', melhor='min'), width="stretch")
            st.markdown("**Posição na Cidade**")
            st.altair_chart(criar_grafico_altair_enem(df_enem, 'Posição Cidade', '#81C784', melhor='min'), width="stretch")
            
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📊 Consultar Tabela Geral - Enem", expanded=True):
            df_enem_exibicao = df_enem.copy()
            for col in df_enem_exibicao.columns:
                if col not in ['Ano', 'Campus']:
                    df_enem_exibicao[col] = df_enem_exibicao[col].apply(lambda x: fmt_br(x, 1 if 'Média' in col else 0))
            st.dataframe(df_enem_exibicao, width="stretch", hide_index=True)
            
    except FileNotFoundError:
        st.error("Arquivo 'CI_Enem.csv' não encontrado.")
    except Exception as e:
        st.error(f"Erro ao carregar dados do Enem: {e}")

# ------------------------------------------
# 6. ENADE
# ------------------------------------------
elif menu_opcao == "🧪 Enade":
    st.markdown("### 🧪 Dados do Enade")
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_enade_path = os.path.join(script_dir, 'CI_Enade.csv')
        
        try:
            df_enade = pd.read_csv(csv_enade_path, sep=";", encoding="utf-8")
        except UnicodeDecodeError:
            df_enade = pd.read_csv(csv_enade_path, sep=";", encoding="latin1")
            
        cols_numericas = ['Alunos Inscritos', 'Alunos Participantes', 'ENADE', 'CPC', 'IDD']
        for col in cols_numericas:
            if str(df_enade[col].dtype) in ['object', 'string']:
                df_enade[col] = df_enade[col].astype(str).str.replace(',', '.', regex=False).astype(float)
                
        st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA</p>", unsafe_allow_html=True)
        
        if 'f_cursos_enade' not in st.session_state: st.session_state.f_cursos_enade = []
        if 'f_anos_enade' not in st.session_state: st.session_state.f_anos_enade = []
        
        def get_opts_enade(col):
            df_temp = df_enade.copy()
            if col != 'Curso' and st.session_state.f_cursos_enade: df_temp = df_temp[df_temp['Curso'].isin(st.session_state.f_cursos_enade)]
            if col != 'Ano' and st.session_state.f_anos_enade: df_temp = df_temp[df_temp['Ano'].isin(st.session_state.f_anos_enade)]
            
            opts = sorted(list(df_temp[col].dropna().unique()))
            if col == 'Curso': opts = sorted(list(set(opts + st.session_state.f_cursos_enade)))
            if col == 'Ano': opts = sorted(list(set(opts + st.session_state.f_anos_enade)), reverse=True)
            return opts
        
        col_filtro, col_box1, col_box2 = st.columns([2, 1, 1])
        with col_filtro:
            st.session_state.f_cursos_enade = st.multiselect("Curso", options=get_opts_enade('Curso'), default=st.session_state.f_cursos_enade, placeholder="Selecione o(s) Curso(s)")
            st.session_state.f_anos_enade = st.multiselect("Ano", options=get_opts_enade('Ano'), default=st.session_state.f_anos_enade, placeholder="Selecione o(s) Ano(s)")
            
        df_filtrado_enade = df_enade.copy()
        if st.session_state.f_cursos_enade: df_filtrado_enade = df_filtrado_enade[df_filtrado_enade['Curso'].isin(st.session_state.f_cursos_enade)]
        if st.session_state.f_anos_enade: df_filtrado_enade = df_filtrado_enade[df_filtrado_enade['Ano'].isin(st.session_state.f_anos_enade)]
            
        box_style = """
        <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 20px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;'>
            <p style='color: #666; font-size: 1.1rem; margin-bottom: 5px; font-weight: bold;'>{title}</p>
            <h2 style='color: #006633; margin-top: 0px; font-size: 2.2rem;'>{value}</h2>
        </div>
        """
        
        total_inscritos_enade = df_filtrado_enade['Alunos Inscritos'].sum()
        total_participantes_enade = df_filtrado_enade['Alunos Participantes'].sum()
        
        with col_box1:
            st.markdown(box_style.format(title="Total Inscritos", value=fmt_br(total_inscritos_enade, 0)), unsafe_allow_html=True)
        with col_box2:
            st.markdown(box_style.format(title="Total Participantes", value=fmt_br(total_participantes_enade, 0)), unsafe_allow_html=True)
            
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;'>📊 RESULTADOS ENADE</p>", unsafe_allow_html=True)
        
        def criar_grafico_altair_enade(df_dados, coluna_y, cor_barra_padrao, e_nota=False):
            df_plot = df_dados.dropna(subset=[coluna_y]).copy()
            if df_plot.empty:
                return alt.Chart(pd.DataFrame({'Ano': [], coluna_y: []})).mark_bar().encode(x='Ano:O', y=f'{coluna_y}:Q').properties(height=300)
                
            if coluna_y in ['Alunos Inscritos', 'Alunos Participantes']:
                df_agrupado = df_plot.groupby('Ano', as_index=False)[coluna_y].sum()
            else:
                df_agrupado = df_plot.groupby('Ano', as_index=False)[coluna_y].mean()
                
            df_agrupado['Valor_Txt'] = df_agrupado[coluna_y].apply(lambda x: fmt_br(x, 1 if e_nota else 0))

            destaque_val = df_agrupado[coluna_y].max()
            cor_destaque = alt.condition(alt.datum[coluna_y] == destaque_val, alt.value('#006633'), alt.value(cor_barra_padrao))
            escala_max = max(1, df_agrupado[coluna_y].max() * 1.2)
            
            if e_nota:
                y_axis_en = alt.Axis(title=None, format=',.1f', labelExpr="replace(datum.label, ',', '.')")
            else:
                y_axis_en = alt.Axis(title=None, format=',d', labelExpr="replace(datum.label, ',', '.')")

            base = alt.Chart(df_agrupado).encode(x=alt.X('Ano:O', axis=alt.Axis(labelAngle=-90, title='Ano', grid=True, gridColor='#EAEAEA')))
            barras = base.mark_bar().encode(
                y=alt.Y(f'{coluna_y}:Q', axis=y_axis_en, scale=alt.Scale(domain=[0, escala_max])), 
                color=cor_destaque,
                tooltip=[alt.Tooltip('Ano:O', title='Ano'), alt.Tooltip(f'{coluna_y}:Q', title=coluna_y, format='.2f')]
            )
            textos = base.mark_text(align='center', baseline='bottom', dy=-5, color='black', fontWeight='bold').encode(
                y=alt.Y(f'{coluna_y}:Q'), text=alt.Text('Valor_Txt:N')
            )
            return (barras + textos).properties(height=300).interactive()
            
        col_graf1, col_graf2 = st.columns(2)
        with col_graf1:
            st.markdown("**Alunos Inscritos**")
            st.altair_chart(criar_grafico_altair_enade(df_filtrado_enade, 'Alunos Inscritos', '#66BB6A'), width="stretch")
        with col_graf2:
            st.markdown("**Alunos Participantes**")
            st.altair_chart(criar_grafico_altair_enade(df_filtrado_enade, 'Alunos Participantes', '#4CAF50'), width="stretch")
            
        st.markdown("<br>", unsafe_allow_html=True)
        col_graf3, col_graf4, col_graf5 = st.columns(3)
        with col_graf3:
            st.markdown("**Nota ENADE**")
            st.altair_chart(criar_grafico_altair_enade(df_filtrado_enade, 'ENADE', '#66BB6A', e_nota=True), width="stretch")
        with col_graf4:
            st.markdown("**Nota CPC**")
            st.altair_chart(criar_grafico_altair_enade(df_filtrado_enade, 'CPC', '#81C784', e_nota=True), width="stretch")
        with col_graf5:
            st.markdown("**Nota IDD**")
            st.altair_chart(criar_grafico_altair_enade(df_filtrado_enade, 'IDD', '#4CAF50', e_nota=True), width="stretch")
            
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📊 Consultar Tabela Geral - Enade", expanded=True):
            df_exibicao_enade = df_filtrado_enade.drop(columns=['Instituição', 'Estrutura com Matrícula'], errors='ignore').copy()
            for col in cols_numericas:
                if col in df_exibicao_enade.columns:
                    df_exibicao_enade[col] = df_exibicao_enade[col].apply(lambda x: fmt_br(x, 1 if col in ['ENADE', 'CPC', 'IDD'] else 0))
            st.dataframe(df_exibicao_enade.sort_values(by='Ano', ascending=False), width="stretch", hide_index=True)
            
    except FileNotFoundError:
        st.error("Arquivo 'CI_Enade.csv' não encontrado.")
    except Exception as e:
        st.error(f"Erro ao carregar dados do Enade: {e}")

# ==========================================
# 7. CONIF
# ==========================================
elif menu_opcao == "🏛️ Conif":
    st.markdown("### 🏛️ Indicadores CONIF")
    st.info("ℹ️ **Dados da PNP 2023 para estimar o orçamento de 2025.** O orçamento utiliza a PNP de dois anos antes e é calculado a partir da Portaria 243/2026.")

    tab1, tab2 = st.tabs([
        "💰 Matriz Orçamentária", 
        "🤝 Assistência Estudantil"
    ])
    
    with tab1:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_conif_path = os.path.join(script_dir, 'CI_Orcamento.csv')
            
            try:
                df_conif = pd.read_csv(csv_conif_path, sep=";", encoding="utf-8")
            except UnicodeDecodeError:
                df_conif = pd.read_csv(csv_conif_path, sep=";", encoding="latin1")
            
            df_conif.columns = df_conif.columns.str.strip()

            cols_num = ['DACP1', 'DACP2', 'DACP3', 'DACP4', 'DACP5', 'MECHDA', 'PC', 'MT_FINAL']
            for col in cols_num:
                if col in df_conif.columns:
                    if str(df_conif[col].dtype) in ['object', 'string']:
                        df_conif[col] = df_conif[col].astype(str).str.replace(',', '.', regex=False).astype(float)
                    
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA</p>", unsafe_allow_html=True)
            
            for f_key in ['f_conif_tipo_curso', 'f_conif_tipo_oferta', 'f_conif_nome_curso', 'f_conif_turno']:
                if f_key not in st.session_state:
                    st.session_state[f_key] = []

            def get_opts_conif(col):
                df_temp = df_conif.copy()
                if col != 'Tipo de Curso' and st.session_state.f_conif_tipo_curso: df_temp = df_temp[df_temp['Tipo de Curso'].isin(st.session_state.f_conif_tipo_curso)]
                if col != 'Tipo de Oferta' and st.session_state.f_conif_tipo_oferta: df_temp = df_temp[df_temp['Tipo de Oferta'].isin(st.session_state.f_conif_tipo_oferta)]
                if col != 'Nome de Curso' and st.session_state.f_conif_nome_curso: df_temp = df_temp[df_temp['Nome de Curso'].isin(st.session_state.f_conif_nome_curso)]
                if col != 'Turno' and st.session_state.f_conif_turno: df_temp = df_temp[df_temp['Turno'].isin(st.session_state.f_conif_turno)]
                
                opts = sorted(list(df_temp[col].dropna().unique()))
                if col == 'Tipo de Curso': opts = sorted(list(set(opts + st.session_state.f_conif_tipo_curso)))
                if col == 'Tipo de Oferta': opts = sorted(list(set(opts + st.session_state.f_conif_tipo_oferta)))
                if col == 'Nome de Curso': opts = sorted(list(set(opts + st.session_state.f_conif_nome_curso)))
                if col == 'Turno': opts = sorted(list(set(opts + st.session_state.f_conif_turno)))
                return opts

            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            with col_f1:
                st.session_state.f_conif_tipo_curso = st.multiselect("Tipo de Curso", options=get_opts_conif('Tipo de Curso'), default=st.session_state.f_conif_tipo_curso, placeholder="Selecione o Tipo")
            with col_f2:
                st.session_state.f_conif_tipo_oferta = st.multiselect("Tipo de Oferta", options=get_opts_conif('Tipo de Oferta'), default=st.session_state.f_conif_tipo_oferta, placeholder="Selecione a Oferta")
            with col_f3:
                st.session_state.f_conif_nome_curso = st.multiselect("Nome do Curso", options=get_opts_conif('Nome de Curso'), default=st.session_state.f_conif_nome_curso, placeholder="Selecione o Curso")
            with col_f4:
                st.session_state.f_conif_turno = st.multiselect("Turno", options=get_opts_conif('Turno'), default=st.session_state.f_conif_turno, placeholder="Selecione o Turno")

            df_conif_f = df_conif.copy()
            if st.session_state.f_conif_tipo_curso: df_conif_f = df_conif_f[df_conif_f['Tipo de Curso'].isin(st.session_state.f_conif_tipo_curso)]
            if st.session_state.f_conif_tipo_oferta: df_conif_f = df_conif_f[df_conif_f['Tipo de Oferta'].isin(st.session_state.f_conif_tipo_oferta)]
            if st.session_state.f_conif_nome_curso: df_conif_f = df_conif_f[df_conif_f['Nome de Curso'].isin(st.session_state.f_conif_nome_curso)]
            if st.session_state.f_conif_turno: df_conif_f = df_conif_f[df_conif_f['Turno'].isin(st.session_state.f_conif_turno)]

            soma_dacp1 = (df_conif_f['DACP1'] != 0).sum() if 'DACP1' in df_conif_f else 0
            soma_dacp2 = (df_conif_f['DACP2'] != 0).sum() if 'DACP2' in df_conif_f else 0
            soma_dacp3 = (df_conif_f['DACP3'] != 0).sum() if 'DACP3' in df_conif_f else 0
            soma_dacp4 = (df_conif_f['DACP4'] != 0).sum() if 'DACP4' in df_conif_f else 0
            soma_dacp5 = (df_conif_f['DACP5'] != 0).sum() if 'DACP5' in df_conif_f else 0
            soma_mechda_0 = len(df_conif_f[df_conif_f['MECHDA'] == 0]) if 'MECHDA' in df_conif_f else 0
            media_pc = df_conif_f['PC'].mean() if 'PC' in df_conif_f else 0
            soma_mt_final = df_conif_f['MT_FINAL'].sum() if 'MT_FINAL' in df_conif_f else 0
            
            box_style = """
            <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; height: 100%;'>
                <p style='color: #666; font-size: 0.85rem; margin-bottom: 5px; font-weight: bold;'>{title}</p>
                <h3 style='color: #006633; margin-top: 0px;'>{value}</h3>
            </div>
            """
            
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.markdown(box_style.format(title="DACP1<br>(Ativo Todo o Ano)", value=fmt_br(soma_dacp1, 0)), unsafe_allow_html=True)
            with c2: st.markdown(box_style.format(title="DACP2<br>(Início no Ano / Fim Após)", value=fmt_br(soma_dacp2, 0)), unsafe_allow_html=True)
            with c3: st.markdown(box_style.format(title="DACP3<br>(Início Antes / Fim no Ano)", value=fmt_br(soma_dacp3, 0)), unsafe_allow_html=True)
            with c4: st.markdown(box_style.format(title="DACP4<br>(Início e Fim no Ano)", value=fmt_br(soma_dacp4, 0)), unsafe_allow_html=True)
            
            c5, c6, c7, c8 = st.columns(4)
            with c5: st.markdown(box_style.format(title="DACP5<br>(Retidos / Pós-Término)", value=fmt_br(soma_dacp5, 0)), unsafe_allow_html=True)
            with c6: st.markdown(box_style.format(title="MECHDA = 0<br>(Expirados >3 Anos)", value=fmt_br(soma_mechda_0, 0)), unsafe_allow_html=True)
            with c7: st.markdown(box_style.format(title="Peso do Curso (Média)", value=fmt_br(media_pc)), unsafe_allow_html=True)
            with c8: st.markdown(box_style.format(title="MT_FINAL (Soma)", value=fmt_br(soma_mt_final)), unsafe_allow_html=True)
            
            st.markdown("<br><hr>", unsafe_allow_html=True)
            
            col_pie1, col_pie2 = st.columns(2)
            
            with col_pie1:
                st.markdown("**Distribuição dos DACP**")
                df_pie = pd.DataFrame({
                    'Categoria': ['DACP1', 'DACP2', 'DACP3', 'DACP4', 'DACP5'],
                    'Valor': [soma_dacp1, soma_dacp2, soma_dacp3, soma_dacp4, soma_dacp5]
                })
                df_pie = df_pie[df_pie['Valor'] > 0]
                
                if not df_pie.empty and df_pie['Valor'].sum() > 0:
                    df_pie['Porcentagem'] = (df_pie['Valor'] / df_pie['Valor'].sum()) * 100
                    df_pie['Porcentagem_Txt'] = df_pie['Porcentagem'].apply(lambda x: f"{fmt_br(x, 1)}%")
                    
                    base_pie = alt.Chart(df_pie).encode(
                        theta=alt.Theta(field="Valor", type="quantitative", stack=True),
                        color=alt.Color(
                            field="Categoria", 
                            type="nominal", 
                            legend=alt.Legend(orient="bottom", title=None, columns=3, labelLimit=200),
                            scale=alt.Scale(range=['#4CAF50', '#2196F3', '#FF9800', '#F44336', '#9C27B0'])
                        )
                    )
                    
                    graf_pie = base_pie.mark_arc(innerRadius=50, outerRadius=100).encode(
                        tooltip=['Categoria', alt.Tooltip('Valor:Q', format='.0f'), alt.Tooltip('Porcentagem_Txt:N', title='Porcentagem')]
                    )
                    
                    text_pie = base_pie.mark_text(radius=125, size=12, fontWeight='bold', color='#333333').encode(
                        text=alt.Text('Porcentagem_Txt:N')
                    )
                    
                    st.altair_chart((graf_pie + text_pie).properties(height=380), width="stretch")
                else:
                    st.info("Não há dados de DACP para os filtros selecionados.")
                    
            with col_pie2:
                st.markdown("**MT_Final por Tipo de Curso**")
                
                df_mt = df_conif_f.copy()
                if 'MT_FINAL' in df_mt.columns and not df_mt.empty:
                    df_mt['Tipo_Pie'] = df_mt['Tipo de Curso']
                    
                    mask_tec = df_mt['Tipo de Curso'].astype(str).str.contains('Técnico', case=False, na=False)
                    mask_int = mask_tec & df_mt['Tipo de Oferta'].astype(str).str.contains('Integrado', case=False, na=False)
                    mask_conc = mask_tec & df_mt['Tipo de Oferta'].astype(str).str.contains('Concomitante|Subsequente', case=False, na=False)
                    
                    df_mt.loc[mask_int, 'Tipo_Pie'] = 'Técnico Integrado'
                    df_mt.loc[mask_conc, 'Tipo_Pie'] = 'Técnico Concomit/Subseq'
                    
                    df_mt_pie = df_mt.groupby('Tipo_Pie', as_index=False)['MT_FINAL'].sum()
                    df_mt_pie = df_mt_pie[df_mt_pie['MT_FINAL'] > 0]
                    
                    if not df_mt_pie.empty and df_mt_pie['MT_FINAL'].sum() > 0:
                        df_mt_pie['Porcentagem'] = (df_mt_pie['MT_FINAL'] / df_mt_pie['MT_FINAL'].sum()) * 100
                        df_mt_pie['Porcentagem_Txt'] = df_mt_pie['Porcentagem'].apply(lambda x: f"{fmt_br(x, 1)}%")
                        
                        base_mt_pie = alt.Chart(df_mt_pie).encode(
                            theta=alt.Theta(field="MT_FINAL", type="quantitative", stack=True),
                            color=alt.Color(
                                field="Tipo_Pie", 
                                type="nominal", 
                                legend=alt.Legend(orient="bottom", title=None, columns=2, labelLimit=250)
                            )
                        )
                        
                        graf_mt_pie = base_mt_pie.mark_arc(innerRadius=50, outerRadius=100).encode(
                            tooltip=['Tipo_Pie', alt.Tooltip('MT_FINAL:Q', format='.2f'), alt.Tooltip('Porcentagem_Txt:N', title='Porcentagem')]
                        )
                        
                        text_mt_pie = base_mt_pie.mark_text(radius=125, size=12, fontWeight='bold', color='#333333').encode(
                            text=alt.Text('Porcentagem_Txt:N')
                        )
                        
                        st.altair_chart((graf_mt_pie + text_mt_pie).properties(height=380), width="stretch")
                    else:
                        st.info("Não há dados de MT_FINAL para os filtros selecionados.")
                else:
                    st.info("Não há dados de MT_FINAL.")
                
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Tabela Consolidada**")
            
            groupby_cols = ['Tipo de Curso', 'Tipo de Oferta', 'Nome de Curso']
            if 'Turno' in df_conif_f.columns:
                groupby_cols.append('Turno')
                
            df_tab = df_conif_f.groupby(groupby_cols, as_index=False).agg(
                DACP1=('DACP1', lambda x: (x != 0).sum()),
                DACP2=('DACP2', lambda x: (x != 0).sum()),
                DACP3=('DACP3', lambda x: (x != 0).sum()),
                DACP4=('DACP4', lambda x: (x != 0).sum()),
                DACP5=('DACP5', lambda x: (x != 0).sum()),
                MECHDA_0=('MECHDA', lambda x: (x == 0).sum()),
                Peso_Curso=('PC', 'mean'),
                Soma_MT_Final=('MT_FINAL', 'sum')
            )
            
            df_tab = df_tab.sort_values(by='Soma_MT_Final', ascending=False)
            
            total_mt_final = df_tab['Soma_MT_Final'].sum()
            if total_mt_final > 0:
                df_tab['% MT_Final'] = (df_tab['Soma_MT_Final'] / total_mt_final) * 100
            else:
                df_tab['% MT_Final'] = 0.0
                
            df_tab_show = df_tab.copy()
            for col in ['DACP1', 'DACP2', 'DACP3', 'DACP4', 'DACP5', 'MECHDA_0', 'Peso_Curso', 'Soma_MT_Final']:
                if col in ['DACP1', 'DACP2', 'DACP3', 'DACP4', 'DACP5', 'MECHDA_0']:
                    df_tab_show[col] = df_tab_show[col].apply(lambda x: fmt_br(x, 0))
                else:
                    df_tab_show[col] = df_tab_show[col].apply(lambda x: fmt_br(x, 2))
            df_tab_show['% MT_Final'] = df_tab_show['% MT_Final'].apply(lambda x: fmt_br(x, 2) + "%")
            
            df_tab_show = df_tab_show.rename(columns={'Peso_Curso': 'Peso do Curso', 'MECHDA_0': 'Qtd. MECHDA=0'})
            
            cols_order = ['Tipo de Curso', 'Tipo de Oferta', 'Nome de Curso']
            if 'Turno' in df_tab_show.columns:
                cols_order.append('Turno')
            cols_order.extend(['DACP1', 'DACP2', 'DACP3', 'DACP4', 'DACP5', 'Qtd. MECHDA=0', 'Peso do Curso', 'Soma_MT_Final', '% MT_Final'])
            df_tab_show = df_tab_show[cols_order]
            
            st.dataframe(df_tab_show, width="stretch", hide_index=True)
                
        except FileNotFoundError:
            st.error("Arquivo 'CI_Orcamento.csv' não encontrado.")
        except Exception as e:
            st.error(f"Erro ao carregar dados do Conif: {e}")

    with tab2:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_conif_path = os.path.join(script_dir, 'CI_Orcamento.csv')
            
            try:
                df_ae = pd.read_csv(csv_conif_path, sep=";", encoding="utf-8")
            except UnicodeDecodeError:
                df_ae = pd.read_csv(csv_conif_path, sep=";", encoding="latin1")
            
            df_ae.columns = df_ae.columns.str.strip()

            if 'MAE' in df_ae.columns:
                if str(df_ae['MAE'].dtype) in ['object', 'string']:
                    df_ae['MAE'] = df_ae['MAE'].astype(str).str.replace(',', '.', regex=False).astype(float)
                df_ae['MAE'] = df_ae['MAE'].fillna(0)

            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA</p>", unsafe_allow_html=True)

            for f_key in ['f_ae_tipo_curso', 'f_ae_tipo_oferta', 'f_ae_nome_curso', 'f_ae_turno']:
                if f_key not in st.session_state:
                    st.session_state[f_key] = []

            def get_opts_ae(col):
                df_temp = df_ae.copy()
                if col != 'Tipo de Curso' and st.session_state.f_ae_tipo_curso:
                    df_temp = df_temp[df_temp['Tipo de Curso'].isin(st.session_state.f_ae_tipo_curso)]
                if col != 'Tipo de Oferta' and st.session_state.f_ae_tipo_oferta:
                    df_temp = df_temp[df_temp['Tipo de Oferta'].isin(st.session_state.f_ae_tipo_oferta)]
                if col != 'Nome de Curso' and st.session_state.f_ae_nome_curso:
                    df_temp = df_temp[df_temp['Nome de Curso'].isin(st.session_state.f_ae_nome_curso)]
                if col != 'Turno' and st.session_state.f_ae_turno:
                    df_temp = df_temp[df_temp['Turno'].isin(st.session_state.f_ae_turno)]
                
                opts = sorted(list(df_temp[col].dropna().unique()))
                if col == 'Tipo de Curso': opts = sorted(list(set(opts + st.session_state.f_ae_tipo_curso)))
                if col == 'Tipo de Oferta': opts = sorted(list(set(opts + st.session_state.f_ae_tipo_oferta)))
                if col == 'Nome de Curso': opts = sorted(list(set(opts + st.session_state.f_ae_nome_curso)))
                if col == 'Turno': opts = sorted(list(set(opts + st.session_state.f_ae_turno)))
                return opts

            f_ae_col1, f_ae_col2, f_ae_col3, f_ae_col4 = st.columns(4)
            with f_ae_col1:
                st.session_state.f_ae_tipo_curso = st.multiselect(
                    "Tipo de Curso", get_opts_ae('Tipo de Curso'), default=st.session_state.f_ae_tipo_curso, placeholder="Todos", key="ms_ae_tipo_curso"
                )
            with f_ae_col2:
                st.session_state.f_ae_tipo_oferta = st.multiselect(
                    "Tipo de Oferta", get_opts_ae('Tipo de Oferta'), default=st.session_state.f_ae_tipo_oferta, placeholder="Todas", key="ms_ae_tipo_oferta"
                )
            with f_ae_col3:
                st.session_state.f_ae_nome_curso = st.multiselect(
                    "Nome do Curso", get_opts_ae('Nome de Curso'), default=st.session_state.f_ae_nome_curso, placeholder="Todos", key="ms_ae_nome_curso"
                )
            with f_ae_col4:
                st.session_state.f_ae_turno = st.multiselect(
                    "Turno", get_opts_ae('Turno'), default=st.session_state.f_ae_turno, placeholder="Todos", key="ms_ae_turno"
                )

            df_ae_f = df_ae.copy()
            if st.session_state.f_ae_tipo_curso: df_ae_f = df_ae_f[df_ae_f['Tipo de Curso'].isin(st.session_state.f_ae_tipo_curso)]
            if st.session_state.f_ae_tipo_oferta: df_ae_f = df_ae_f[df_ae_f['Tipo de Oferta'].isin(st.session_state.f_ae_tipo_oferta)]
            if st.session_state.f_ae_nome_curso: df_ae_f = df_ae_f[df_ae_f['Nome de Curso'].isin(st.session_state.f_ae_nome_curso)]
            if st.session_state.f_ae_turno: df_ae_f = df_ae_f[df_ae_f['Turno'].isin(st.session_state.f_ae_turno)]

            st.markdown("<br>", unsafe_allow_html=True)

            # Ordem Oficial conforme Tabela 6 da Portaria MEC 243/2026
            rendas_ordem_pesos = [
                ("0<RFP<=0,5", "Peso 2,5"),
                ("0,5<RFP<=1", "Peso 2,0"),
                ("1<RFP<=1,5", "Peso 1,5"),
                ("1,5<RFP<=2,5", "Peso 1,0"),
                ("2,5<RFP<=3,5", "Peso 0,5"),
                ("RFP>3,5", "Peso 0"),
                ("Não declarada", "Peso 0")
            ]

            card_ae_style = """
            <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 12px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; height: 100%;'>
                <p style='color: #666; font-size: 0.85rem; margin-bottom: 3px; font-weight: bold;'>{title}<br><span style='color: #718096; font-size: 0.78rem; font-weight: normal;'>({peso})</span></p>
                <h3 style='color: #006633; margin-top: 4px; margin-bottom: 0px;'>{value}</h3>
            </div>
            """

            c_r1, c_r2, c_r3, c_r4 = st.columns(4)
            for col_obj, (renda, peso_txt) in zip([c_r1, c_r2, c_r3, c_r4], rendas_ordem_pesos[:4]):
                qtd = len(df_ae_f[df_ae_f['Renda Familiar'] == renda]) if not df_ae_f.empty else 0
                title_html = renda.replace('<', '&lt;').replace('>', '&gt;')
                col_obj.markdown(card_ae_style.format(title=title_html, peso=peso_txt, value=fmt_br(qtd, 0)), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            c_r5, c_r6, c_r7, c_r8 = st.columns(4)
            for col_obj, (renda, peso_txt) in zip([c_r5, c_r6, c_r7], rendas_ordem_pesos[4:]):
                qtd = len(df_ae_f[df_ae_f['Renda Familiar'] == renda]) if not df_ae_f.empty else 0
                title_html = renda.replace('<', '&lt;').replace('>', '&gt;')
                col_obj.markdown(card_ae_style.format(title=title_html, peso=peso_txt, value=fmt_br(qtd, 0)), unsafe_allow_html=True)

            soma_mae_val = df_ae_f['MAE'].sum() if 'MAE' in df_ae_f.columns and not df_ae_f.empty else 0
            box_mae_style = """
            <div style='border: 2px solid #006633; border-radius: 10px; padding: 12px; text-align: center; background-color: #E8F5E9; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; height: 100%;'>
                <p style='color: #006633; font-size: 0.85rem; margin-bottom: 3px; font-weight: bold;'>Soma MAE<br><span style='color: #2E7D32; font-size: 0.78rem; font-weight: normal;'>(Matrícula Equivalente AE)</span></p>
                <h3 style='color: #006633; margin-top: 4px; margin-bottom: 0px;'>{value}</h3>
            </div>
            """
            c_r8.markdown(box_mae_style.format(value=fmt_br(soma_mae_val, 2)), unsafe_allow_html=True)

            st.markdown("<br><hr>", unsafe_allow_html=True)

            if not df_ae_f.empty:
                df_rf_summary = df_ae_f.groupby('Renda Familiar', as_index=False).size().rename(columns={'size': 'Qtd_Alunos'})
                
                all_rendas = pd.DataFrame([r[0] for r in rendas_ordem_pesos], columns=['Renda Familiar'])
                df_rf_summary = pd.merge(all_rendas, df_rf_summary, on='Renda Familiar', how='left').fillna(0)

                top_menores_renda = df_rf_summary.sort_values(by='Qtd_Alunos', ascending=True).head(3)
                top_maiores_renda = df_rf_summary.sort_values(by='Qtd_Alunos', ascending=False).head(3)

                card_list_style = """
                <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px 20px; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 100%;'>
                    <p style='color: {color}; font-size: 1.05rem; margin-bottom: 10px; font-weight: bold; text-align: center;'>{title}</p>
                    <ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>
                        {items}
                    </ul>
                </div>
                """

                items_menores_rf = "".join([
                    f"<li style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 8px 0; font-size: 0.9rem; color: #333;'>"
                    f"<span>• {str(row['Renda Familiar']).replace('<', '&lt;').replace('>', '&gt;')}</span>"
                    f"<strong style='color: #006633;'>{fmt_br(row['Qtd_Alunos'], 0)} alunos</strong></li>"
                    for _, row in top_menores_renda.iterrows()
                ])

                items_maiores_rf = "".join([
                    f"<li style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 8px 0; font-size: 0.9rem; color: #333;'>"
                    f"<span>• {str(row['Renda Familiar']).replace('<', '&lt;').replace('>', '&gt;')}</span>"
                    f"<strong style='color: #006633;'>{fmt_br(row['Qtd_Alunos'], 0)} alunos</strong></li>"
                    for _, row in top_maiores_renda.iterrows()
                ])

                col_menor_rf, col_maior_rf = st.columns(2)
                with col_menor_rf:
                    st.markdown(card_list_style.format(title="📉 Rendas Familiares com Menos Alunos", color="#2E7D32", items=items_menores_rf), unsafe_allow_html=True)
                with col_maior_rf:
                    st.markdown(card_list_style.format(title="📈 Rendas Familiares com Mais Alunos", color="#006633", items=items_maiores_rf), unsafe_allow_html=True)

            st.markdown("<br><hr>", unsafe_allow_html=True)

            col_pie_ae1, col_pie_ae2 = st.columns(2)
            
            with col_pie_ae1:
                st.markdown("**Distribuição de Alunos por Renda Familiar (%)**")
                if not df_ae_f.empty:
                    df_pie_rf = df_ae_f.groupby('Renda Familiar', as_index=False).size().rename(columns={'size': 'Qtd_Alunos'})
                    df_pie_rf = df_pie_rf[df_pie_rf['Qtd_Alunos'] > 0]
                    
                    tot_alunos_pie = df_pie_rf['Qtd_Alunos'].sum()
                    if tot_alunos_pie > 0:
                        df_pie_rf['Porcentagem'] = (df_pie_rf['Qtd_Alunos'] / tot_alunos_pie) * 100
                        df_pie_rf['Porcentagem_Txt'] = df_pie_rf['Porcentagem'].apply(lambda x: f"{fmt_br(x, 1)}%")
                        
                        base_pie_rf = alt.Chart(df_pie_rf).encode(
                            theta=alt.Theta(field="Qtd_Alunos", type="quantitative", stack=True),
                            color=alt.Color(
                                field="Renda Familiar", 
                                type="nominal", 
                                legend=alt.Legend(orient="bottom", title=None, columns=2, labelLimit=250),
                                scale=alt.Scale(range=['#4CAF50', '#2196F3', '#FF9800', '#E53935', '#9C27B0', '#009688', '#795548'])
                            )
                        )
                        
                        graf_pie_rf = base_pie_rf.mark_arc(innerRadius=50, outerRadius=100).encode(
                            tooltip=[
                                'Renda Familiar', 
                                alt.Tooltip('Qtd_Alunos:Q', title='Qtd Alunos', format=',.0f'), 
                                alt.Tooltip('Porcentagem_Txt:N', title='Porcentagem')
                            ]
                        )
                        
                        text_pie_rf = base_pie_rf.mark_text(radius=125, size=12, fontWeight='bold', color='#333333').encode(
                            text=alt.Text('Porcentagem_Txt:N')
                        )
                        
                        st.altair_chart((graf_pie_rf + text_pie_rf).properties(height=380), width="stretch")
                    else:
                        st.info("Não há dados de Renda Familiar para os filtros selecionados.")
                else:
                    st.info("Não há dados para exibir no gráfico.")

            with col_pie_ae2:
                st.markdown("**Distribuição de MAE por Tipo de Curso (%)**")
                if not df_ae_f.empty and 'MAE' in df_ae_f.columns:
                    df_mae_pie = df_ae_f.copy()
                    df_mae_pie['Tipo_Pie'] = df_mae_pie['Tipo de Curso']
                    
                    mask_tec = df_mae_pie['Tipo de Curso'].astype(str).str.contains('Técnico', case=False, na=False)
                    mask_int = mask_tec & df_mae_pie['Tipo de Oferta'].astype(str).str.contains('Integrado', case=False, na=False)
                    mask_conc = mask_tec & df_mae_pie['Tipo de Oferta'].astype(str).str.contains('Concomitante|Subsequente', case=False, na=False)
                    
                    df_mae_pie.loc[mask_int, 'Tipo_Pie'] = 'Técnico Integrado'
                    df_mae_pie.loc[mask_conc, 'Tipo_Pie'] = 'Técnico Concomit/Subseq'
                    
                    df_mae_grp = df_mae_pie.groupby('Tipo_Pie', as_index=False)['MAE'].sum()
                    df_mae_grp = df_mae_grp[df_mae_grp['MAE'] > 0]
                    
                    tot_mae_pie = df_mae_grp['MAE'].sum()
                    if tot_mae_pie > 0:
                        df_mae_grp['Porcentagem'] = (df_mae_grp['MAE'] / tot_mae_pie) * 100
                        df_mae_grp['Porcentagem_Txt'] = df_mae_grp['Porcentagem'].apply(lambda x: f"{fmt_br(x, 1)}%")
                        
                        base_pie_mae = alt.Chart(df_mae_grp).encode(
                            theta=alt.Theta(field="MAE", type="quantitative", stack=True),
                            color=alt.Color(
                                field="Tipo_Pie", 
                                type="nominal", 
                                legend=alt.Legend(orient="bottom", title=None, columns=2, labelLimit=250)
                            )
                        )
                        
                        graf_pie_mae = base_pie_mae.mark_arc(innerRadius=50, outerRadius=100).encode(
                            tooltip=[
                                alt.Tooltip('Tipo_Pie:N', title='Tipo de Curso'), 
                                alt.Tooltip('MAE:Q', title='Soma MAE', format=',.2f'), 
                                alt.Tooltip('Porcentagem_Txt:N', title='Porcentagem')
                            ]
                        )
                        
                        text_pie_mae = base_pie_mae.mark_text(radius=125, size=12, fontWeight='bold', color='#333333').encode(
                            text=alt.Text('Porcentagem_Txt:N')
                        )
                        
                        st.altair_chart((graf_pie_mae + text_pie_mae).properties(height=380), width="stretch")
                    else:
                        st.info("Não há dados de MAE para os filtros selecionados.")
                else:
                    st.info("Não há dados para exibir o gráfico de MAE.")

            st.markdown("<br><hr>", unsafe_allow_html=True)

            st.markdown("**Tabela Consolidada - Assistência Estudantil**")
            
            groupby_cols_ae = ['Tipo de Curso', 'Tipo de Oferta', 'Nome de Curso']
            if 'Turno' in df_ae_f.columns:
                groupby_cols_ae.append('Turno')

            if not df_ae_f.empty:
                df_pivot_rf = pd.crosstab(
                    index=[df_ae_f[col] for col in groupby_cols_ae], 
                    columns=df_ae_f['Renda Familiar']
                ).reset_index()

                lista_rendas_todas = [r[0] for r in rendas_ordem_pesos]
                for r_col in lista_rendas_todas:
                    if r_col not in df_pivot_rf.columns:
                        df_pivot_rf[r_col] = 0

                df_soma_mae = df_ae_f.groupby(groupby_cols_ae, as_index=False)['MAE'].sum().rename(columns={'MAE': 'Soma MAE'})

                df_tab_ae = pd.merge(df_pivot_rf, df_soma_mae, on=groupby_cols_ae, how='left').fillna(0)

                total_mae_geral = df_tab_ae['Soma MAE'].sum()
                if total_mae_geral > 0:
                    df_tab_ae['% MAE Num'] = (df_tab_ae['Soma MAE'] / total_mae_geral) * 100
                else:
                    df_tab_ae['% MAE Num'] = 0.0

                df_tab_ae = df_tab_ae.sort_values(by='% MAE Num', ascending=False)

                df_tab_ae_show = df_tab_ae.copy()
                for col_r in lista_rendas_todas:
                    df_tab_ae_show[col_r] = df_tab_ae_show[col_r].apply(lambda x: fmt_br(x, 0))
                
                df_tab_ae_show['Soma MAE'] = df_tab_ae_show['Soma MAE'].apply(lambda x: fmt_br(x, 2))
                df_tab_ae_show['% MAE'] = df_tab_ae_show['% MAE Num'].apply(lambda x: f"{fmt_br(x, 2)}%")

                cols_ordem_tabela_ae = groupby_cols_ae + lista_rendas_todas + ['Soma MAE', '% MAE']
                df_tab_ae_show = df_tab_ae_show[cols_ordem_tabela_ae]

                st.dataframe(df_tab_ae_show, width="stretch", hide_index=True)
            else:
                st.info("Não há registros para os filtros selecionados.")

        except FileNotFoundError:
            st.error("Arquivo 'CI_Orcamento.csv' não encontrado.")
        except Exception as e:
            st.error(f"Erro ao carregar dados de Assistência Estudantil: {e}")

# ------------------------------------------
# 8. INFORMAÇÕES ADICIONAIS
# ------------------------------------------
elif menu_opcao == "ℹ️ Informações Adicionais":
    st.markdown("### ℹ️ Informações Adicionais")
    
    tab_glossario, tab_leis, tab_fec, tab_pnp, tab_conif = st.tabs([
        "📖 Glossário", 
        "⚖️ Leis", 
        "📊 FEC", 
        "📈 PNP",
        "🏛️ Conif"
    ])
    
    with tab_glossario:
        st.markdown("""
        #### Glossário de Termos e Expressões
        
        * **Concluintes:** É o somatório dos alunos Formados com os Integralizados em Fase Escolar no ano de referência.
        * **Cursos:** Conjunto de atividades educativas formais que constroem um perfil de formação, composto por componentes curriculares, agrupados em períodos letivos. Considera-se a diferenciação entre cursos de uma mesma Unidade de Ensino, com mesma denominação, e Tipo de Curso, Tipo de oferta, Modalidade de Ensino e Turno distintos.
        * **Carga horária do curso - chc:** Carga horária do curso estabelecida no projeto pedagógico do curso ou na carga horária fixada para o curso.
        * **Carga horária mínima regulamentada do curso - chmr:** Carga horária mínima dos cursos, estabelecidas no Catálogo Nacional de Cursos Superiores de Tecnologia - CNCST, no Catálogo Nacional de Cursos Técnicos - CNCT, no Guia Pronatec de Cursos de Formação Inicial e Continuada - Guia-Pronatec de cursos FIC, nas Diretrizes Curriculares Nacionais dos Cursos de Graduação e demais regramentos do MEC para definição de cargas horárias mínimas de cursos.
        * **Eixo tecnológico:** É o agrupamento de ações e das aplicações científicas às atividades humanas de mesma natureza, possuindo um núcleo de saberes comuns, embasados nas mesmas ciências e metodologias. São aplicados na classificação dos cursos da educação profissional, constante dos Catálogos Nacionais. Para efeitos da Plataforma Nilo Peçanha, os cursos de Educação Básica, não profissionais, foram agregados ao Eixo Propedêutico.
        * **Evadidos:** Corresponde aos alunos que perderam o vínculo com a instituição antes da conclusão de um curso.
        * **Fator de equiparação de carga horária - fech:** Permite a equiparação de cursos de qualificação profissional com durações distintas, sendo calculado pela razão entre a carga horária mínima regulamentada do curso (chmr) e carga horária padrão de 800 horas anuais. Para os demais cursos, o fator de equiparação de carga horária será igual a 1 (um).
        * **Fator de correção da graduação - fcg:** O fator de correção da graduação (fcg) ajusta a contagem das matrículas para os cursos de graduação, em atendimento à estratégia 12.3 da Lei nº 13.005, de 2014.
        * **Fator de esforço de curso - fec:** Ajusta a contagem de matrículas-equivalentes (Mateq) para cursos que demandem, para o desenvolvimento de suas atividades, uma menor relação aluno por professor (rap).
        * **Fonte de financiamento:** Indica a Fonte de Financiamento das matrículas apresentadas na Plataforma Nilo Peçanha.
        * **Formados:** Corresponde aos alunos que concluíram com êxito todos os componentes curriculares de um curso no ano de referência, fazendo jus ao diploma ou certificado.
        * **Gastos:** As definições de gastos deste glossário são específicas para os cálculos dos indicadores de gestão da Rede Federal. Tratam-se dos gastos liquidados no ano de exercício. São extraídos do SIAFI, por meio do sistema do Tesouro Gerencial.
        * **Gasto corrente:** Todos os gastos, exceto investimento, capital, precatórios, inativos e pensionistas. Sua apuração é feita a partir da subtração das despesas realizadas nos GND 4 e 5 e das despesas realizadas nas ações orçamentárias específicas para pagamentos de precatórios, inativos e pensionistas dos Gastos Totais.
        * **Gastos com investimento:** Extraídos pelos Grupos de Natureza de Despesas 4 e 5 (GND 4 - INVESTIMENTOS e GND 5 - INVERSÕES FINANCEIRAS), permite-se apurar o total de despesas realizadas com investimentos e inversões financeiras.
        * **Gastos com outros custeios:** É entendido como os gastos totais liquidados no exercício, deduzindo gastos com pessoal, benefícios, Pis/Pasep, investimentos e inversões financeiras.
        * **Gastos com pessoal:** São aqueles definidos como Gastos com servidores ativos, inativos, pensionistas, sentenças judiciais e precatórios. A apuração destas despesas nos relatórios extraídos é obtida a partir do Grupo de Natureza de Despesas 1 (GND 1 - PESSOAL E ENCARGOS SOCIAIS).
        * **Gastos totais:** São definidos a partir de todas as despesas realizadas no exercício pelas unidades orçamentárias da Rede Federal, acrescidos das despesas realizadas com créditos descentralizados.
        * **Ingressantes:** Corresponde aos alunos que ingressaram em um curso no ano de referência e tem seu registro no Sistema Nacional de Informações da Educação Profissional e Tecnológica - SISTEC.
        * **Inscritos:** Corresponde aos candidatos que concorreram às vagas disponibilizadas para a fase inicial de um curso, em suas diversas formas de ingresso.
        * **Instituição:** Instituição de Ensino integrante da Rede Federal de EPCT.
        * **Integralizados em fase escolar:** Corresponde aos alunos que concluíram a carga horária das unidades curriculares de um curso no ano de referência, mas não concluíram todos os componentes curriculares (Estágio, TCC, Extensão e o ENADE).
        * **Jornada de Trabalho:** Jornada semanal de trabalho cumpridas pelos servidores da Rede Federal de EPCT, incluindo o regime de Dedicação Exclusiva (DE).
        * **Matrícula-equivalente - Mateq:** Corresponde à matrícula ponderada pelo Fator de Equiparação de Carga Horária de Curso e pelo Fator de Esforço de Curso.
        * **Matrícula - Mat:** Corresponde ao aluno que esteve com sua matrícula ativa em pelo menos um dia no ano de referência, independentemente do tipo ou modalidade do curso. Um aluno pode ter mais de uma matrícula nesse período, caso tenha se matriculado em mais de um curso.
        * **Modalidade de ensino:** Modo de desenvolvimento do curso quanto ao acompanhamento das atividades acadêmicas, podendo ser presencial ou a distância.
        * **Nível da carreira:** Reúne os níveis funcionais do corpo técnico-administrativo.
        * **Nível de curso:** Categorização utilizada na Plataforma Nilo Peçanha para reunir cursos de mesmo nível educacional.
        * **Organização acadêmica:** Refere-se à tipologia das Instituições pertencentes à Rede Federal de EPCT, podendo ser: Institutos Federais; Universidade Tecnológica Federal do Paraná - UTFPR; Centros Federais de Educação Tecnológica Celso Suckow da Fonseca - CEFET-RJ e de Minas Gerais - CEFET-MG; Escolas Técnicas Vinculadas às Universidades Federais; e Colégio Pedro II.
        * **Professor-equivalente - Profeq:** O cálculo do total de professores-equivalentes (Profeq) considera todos os professores efetivos da instituição, ponderando com peso igual a 1,0 (um) aqueles em regime de 40 (quarenta) horas semanais ou dedicação exclusiva e com peso igual a 0,5 (meio) aqueles em regime de 20 (vinte) horas semanais.
        * **Professores - Prof:** Refere-se ao número de professores da Rede Federal de EPCT, reunindo servidores efetivos e substitutos/temporários.
        * **Relação Matrícula por Professor (RMP):** Definida como a razão entre o total das Matrículas-equivalentes (Mateq), ponderada pelo fator de correção da graduação (fcg), e o total dos professores-equivalentes (Profeq).
        * **Retidos:** Corresponde aos alunos que permaneceram matriculados por período superior ao tempo previsto para integralização de um curso.
        * **RSC:** Reconhecimento de Saberes e Competências, atribuído aos professores da Carreira de Educação Básica, Técnica e Tecnológica (EBTT), visando a equivalência de titulação para fins de percepção de Retribuição de Titulação (RT).
        * **Subeixo tecnológico:** Categorização própria da Plataforma Nilo Peçanha, criada para distinguir cursos de um mesmo Eixo Tecnológico em suas diferentes áreas de concentração.
        * **Tipo de curso:** Categorização transversal utilizada para diferenciar os cursos da EPCT em seus diversos níveis e graus.
        * **Tipo de Oferta:** Categorização transversal utilizada para diferenciar as formas de ofertas dos Cursos Técnicos e de Qualificação Profissional (FIC).
        * **Titulação:** Maior Título Acadêmico apresentado pelos servidores da Rede Federal, podendo ser: Ensino Fundamental, Ensino Médio, Técnico, Graduação, Aperfeiçoamento, Especialização, Mestrado e Doutorado.
        * **Turno:** Período do dia ou da noite em que o aluno cursa a maior parte das aulas, podendo ser matutino, vespertino, noturno ou integral. Não se aplica aos cursos com Modalidade de Ensino a Distância.
        * **Unidades de ensino:** Todas as unidades organizacionais que possuam matrículas vinculadas no ano de referência.
        * **Vagas:** Corresponde às vagas disponibilizadas para a fase inicial de um curso, por meio de processo seletivo, vestibular, sorteio, SISU ou outras formas de ingresso, no ano de referência.
        * **Vínculo com a administração pública:** Apresenta o vínculo funcional dos professores com a Administração Pública, podendo ser Efetivo ou Substituto/Temporário.

        ---
        **Fontes:**
        - [Referência Metodológica da Plataforma Nilo Peçanha](https://www.gov.br/mec/pt-br/pnp/referencia-metodologica)
        - Portaria SETEC/MEC nº 146, de 25 de março de 2021
        """)

    with tab_leis:
        st.markdown("""
        #### Base Normativa e Metas
        
        | Indicador | Base Normativa | Valor da Meta |
        | :--- | :--- | :--- |
        | **Matrícula Equivalente** | Não há meta prevista em instrumento normativo. | - |
        | **Matrículas Equivalentes em cursos técnicos** | Portaria 357/2026 | Campi com autorização de funcionamento a partir de 01/01/2023: meta 80%; até 31/12/2022: meta 50% |
        | **Matrículas Equivalentes em cursos de formação de professores** | Meta estabelecida pelo art. 8º da Lei 11.892/2008. | Mínimo de 20% |
        | **Matrículas Equivalentes em Educação de Jovens e Adultos (EJA)** | Meta definida a partir do estabelecido pelo Art. 2º do Decreto 5.840/2006. | Mínimo de 10% |
        | **Oferta de vagas noturnas para graduação** | Meta definida a partir do estabelecido pela estratégia 12.3 da Lei 13.005/2014. | Mínimo de 33,3% |
        | **Relação de Inscritos por Vagas** | Não há meta prevista em instrumento normativo. | - |
        | **Taxa de Evasão Anual** | Não há meta prevista em instrumento normativo. | - |
        | **Conclusão por Ciclo** | As metas estabelecidas pelas estratégias 11.11 e 12.3, previstas na Lei 13.005/2014, serão melhores acompanhadas pelo Índice de Eficiência Acadêmica. | - |
        | **Evasão por Ciclo** | Não há meta prevista em instrumento normativo. | - |
        | **Retenção por Ciclo** | Não há meta prevista em instrumento normativo. | - |
        | **Índice de Eficiência Acadêmica** | Meta estabelecida considerando as estratégias 11.11 e 12.3, previstas na Lei 13.005/2014. | - |
        | **Índice de Titulação do Corpo Docente** | Meta definida a partir do estabelecido pela Meta 13 da Lei 13.005/2014. | 3,6 |
        | **Relação de Matrículas por Professor** | Meta estabelecida considerando as estratégias 11.11 e 12.3, previstas na Lei 13.005/2014. | 20 |
        | **Relação de Matrículas Presenciais por Professor** | Meta estabelecida considerando as estratégias 11.11 e 12.3, previstas na Lei 13.005/2014. | 20 |
        | **Gasto Corrente por Matrícula** | Não há meta prevista em instrumento normativo. | - |
        | **Índice de Verticalização** | Não há meta prevista em instrumento normativo. | - |
        | **Taxa de Ocupação** | Não há meta prevista em instrumento normativo. | - |
        | **Índice Geral de Cursos (IGC) Indicador INEP** | Não há meta prevista em instrumento normativo. | - |
        | **Conceito Preliminar de Curso (CPC) Indicador INEP** | Não há meta prevista em instrumento normativo. | - |

        *Baseado na Tabela 3.1.3 do Guia de Referência Metodológica (PNP 2020) e Portaria 357/2026.*
        """)

    with tab_fec:
        st.markdown("#### Fator de Esforço de Curso (FEC)")
        st.markdown("O Fator de Esforço de Curso (FEC) ajusta a carga horária do curso em função da quantidade de aulas práticas que, tecnicamente, demandem menor Relação Matrícula por Professor.")
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_fec_path = os.path.join(script_dir, 'FEC.csv')
            
            try:
                df_fec = pd.read_csv(csv_fec_path, sep=';', encoding='utf-8')
            except UnicodeDecodeError:
                df_fec = pd.read_csv(csv_fec_path, sep=';', encoding='latin1')
            
            df_fec.columns = df_fec.columns.str.strip()
            
            # Tratamento da coluna FEC para valor numérico float
            if 'FEC' in df_fec.columns:
                if str(df_fec['FEC'].dtype) in ['object', 'string']:
                    df_fec['FEC_num'] = df_fec['FEC'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
                else:
                    df_fec['FEC_num'] = df_fec['FEC'].astype(float)
            else:
                df_fec['FEC_num'] = 0.0

            # Filtros padronizados
            st.markdown("<p style='color: #006633; font-weight: bold; font-size: 1.1rem; margin-bottom: 0px;'>⚙️ FILTROS DE PESQUISA</p>", unsafe_allow_html=True)
            
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                tipos = sorted(df_fec['TIPO DE CURSO'].dropna().unique().tolist())
                f_tipo = st.multiselect("Tipo de Curso", tipos, placeholder="Todos os tipos")
            
            with col_f2:
                if f_tipo:
                    eixos = sorted(df_fec[df_fec['TIPO DE CURSO'].isin(f_tipo)]['EIXO TECNOLÓGICO'].dropna().unique().tolist())
                else:
                    eixos = sorted(df_fec['EIXO TECNOLÓGICO'].dropna().unique().tolist())
                f_eixo = st.multiselect("Eixo Tecnológico", eixos, placeholder="Todos os eixos")
                
            with col_f3:
                df_temp = df_fec.copy()
                if f_tipo:
                    df_temp = df_temp[df_temp['TIPO DE CURSO'].isin(f_tipo)]
                if f_eixo:
                    df_temp = df_temp[df_temp['EIXO TECNOLÓGICO'].isin(f_eixo)]
                
                cursos = sorted(df_temp['CURSO'].dropna().unique().tolist())
                f_curso = st.multiselect("Curso", cursos, placeholder="Todos os cursos")
                
            # Aplicação dos filtros aos dados
            df_fec_f = df_fec.copy()
            if f_tipo:
                df_fec_f = df_fec_f[df_fec_f['TIPO DE CURSO'].isin(f_tipo)]
            if f_eixo:
                df_fec_f = df_fec_f[df_fec_f['EIXO TECNOLÓGICO'].isin(f_eixo)]
            if f_curso:
                df_fec_f = df_fec_f[df_fec_f['CURSO'].isin(f_curso)]
                
            media_fec = df_fec_f['FEC_num'].mean() if not df_fec_f.empty else 0.0
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Card Estilizado no Padrão do Dashboard
            box_style = """
            <div style='border: 2px solid #a3d9a5; border-radius: 10px; padding: 15px; text-align: center; background-color: #FFFFFF; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;'>
                <p style='color: #666; font-size: 0.95rem; margin-bottom: 5px; font-weight: bold;'>{title}</p>
                <h2 style='color: #006633; margin-top: 0px; font-size: 1.8rem;'>{value}</h2>
            </div>
            """
            
            col_card, _ = st.columns([1, 2])
            with col_card:
                val_card_str = fmt_br(media_fec, 3) if pd.notna(media_fec) else "-"
                st.markdown(box_style.format(title="Média do FEC", value=val_card_str), unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Expander + Tabela formatada no padrão PNP
            with st.expander("📊 Consultar Tabela Geral - Fator de Esforço de Curso (FEC)", expanded=True):
                df_fec_exibicao = df_fec_f[['TIPO DE CURSO', 'EIXO TECNOLÓGICO', 'CURSO', 'FEC_num']].copy()
                df_fec_exibicao.rename(columns={'FEC_num': 'FEC'}, inplace=True)
                
                # Formatando os valores da coluna FEC no padrão PT-BR com 3 casas decimais
                df_fec_exibicao['FEC'] = df_fec_exibicao['FEC'].apply(lambda x: fmt_br(x, 3))
                
                st.dataframe(
                    df_fec_exibicao.sort_values(by=['TIPO DE CURSO', 'CURSO'], ascending=[True, True]), 
                    width="stretch", 
                    hide_index=True
                )
            
        except FileNotFoundError:
            st.error("Arquivo 'FEC.csv' não encontrado.")
        except Exception as e:
            st.error(f"Erro ao processar FEC.csv: {e}")

    with tab_pnp:
        st.markdown("#### Plataforma Nilo Peçanha (PNP)")
        st.markdown(
            """
            A Plataforma Nilo Peçanha (PNP) é um ambiente virtual de coleta, validação e disseminação das estatísticas oficiais da Rede Federal de Educação Profissional, Científica e Tecnológica (Rede Federal). Tem como objetivo reunir dados relativos ao corpo docente, discente, técnico-administrativo e de gastos financeiros das unidades da Rede Federal, para fins de cálculo dos indicadores de gestão monitorados pela Secretaria de Educação Profissional e Tecnológica do Ministério da Educação (SETEC/MEC).
            """
        )
        st.markdown("---")

        with st.expander("🏁 Conclusão Ciclo – CCiclo [%]", expanded=False):
            st.markdown(
                r"""
                Este indicador mede o percentual de concluintes em um Ciclo de Matrícula, sendo que para este cálculo é empregado o conceito de matrícula e não de matrícula equivalente.

                * **Meta:** Não há meta prevista em nenhum instrumento normativo.
                * **Polaridade:** Quanto maior melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Curso.

                **Modelo Matemático:**
                $$CCiclo[\%] = \frac{CCiclo}{MCiclo} \times 100$$

                ---
                ### Componentes e Definições

                * **CCiclo - Concluintes no Ciclo**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Resultado da soma entre a Quantidade de alunos "Formados" e a Quantidade de alunos "integralizados em fase escolar", considerando apenas as matrículas vinculadas a ciclos com término previsto para o ano anterior ao Ano de Referência.

                * **MCiclo - Matrículas no Ciclo**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas efetuadas no início do ciclo de matrícula.
                """
            )

        with st.expander("⚠️ Evasão Ciclo – EvCiclo [%]", expanded=False):
            st.markdown(
                r"""
                Este indicador mede o percentual de evadidos em um Ciclo de Matrícula, sendo que, para este cálculo, é empregado o conceito de matrícula e não de matrícula equivalente.

                * **Meta:** Não há meta prevista em nenhum instrumento normativo.
                * **Polaridade:** Quanto menor melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Curso.

                **Modelo Matemático:**
                $$EvCiclo[\%] = \frac{EvCiclo}{MCiclo} \times 100$$

                ---
                ### Componentes e Definições

                * **EvCiclo - Evadidos no Ciclo**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Alunos que perderam vínculo com a instituição antes da conclusão do curso, considerando apenas as matrículas vinculadas a ciclos de matrícula com término previsto para o ano anterior ao ano de referência.

                * **MCiclo - Matrículas no Ciclo**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas efetuadas no início do ciclo de matrícula.
                """
            )

        with st.expander("💰 Gasto Corrente por Matrícula - GCM", expanded=False):
            st.markdown(
                r"""
                Este indicador apresenta o valor investido em média para cada matrícula equivalente na Rede Federal. (Excetua os dados das ETV-UF).

                * **Meta:** Não há meta prevista em nenhum instrumento normativo.
                * **Polaridade:** Quanto menor melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Instituição.

                **Modelo Matemático:**
                $$GCM = \frac{GC}{Meq}$$

                ---
                ### Componentes e Definições

                * **GC - Gasto Corrente**
                  * **Fonte:** SIAFI
                  * **Definição:** Gasto Total com as Instituições no ano de Referência, excetuando inativos/pensionistas, investimentos, inversões financeiras e precatórios.

                * **Meq - Matrículas Equivalentes**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas equivalentes, exceto as das ETV-UF.
                """
            )

        with st.expander("📊 Índice de Eficiência Acadêmica – IEA [%]", expanded=False):
            st.markdown(
                r"""
                Este indicador mede o percentual de alunos que concluíram o curso com êxito dentro do período previsto (+ 1 ano), acrescido de um percentual (projeção) dos alunos retidos no ano de referência que poderão concluir o curso.

                * **Meta:** Meta estabelecida considerando as estratégias 11.11 e 12.3, previstas na Lei 13.005/2014.
                * **Polaridade:** Quanto maior melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Curso.

                **Modelo Matemático:**
                $$IEA[\%] = 100 \times \frac{CCiclo}{CCiclo + EvCiclo}$$

                ---
                ### Componentes e Definições

                * **CCiclo - Conclusão Ciclo**
                  * **Fonte:** PNP
                  * **Definição:** Percentual de CONCLUINTES, em relação às matrículas vinculadas aos ciclos concluídos no ano anterior ao ano de referência.

                * **EvCiclo - Evasão Ciclo**
                  * **Fonte:** PNP
                  * **Definição:** Percentual de EVADIDOS, em relação às matrículas vinculadas aos ciclos concluídos no ano anterior ao ano de referência.
                """
            )

        with st.expander("🎖️ Índice de Titulação do Corpo Docente – ITCD", expanded=False):
            st.markdown(
                r"""
                Este indicador mede a titulação média dos professores efetivos da Rede Federal.

                * **Meta:** 3,6 - Meta 13 prevista na Lei 13.005/2014.
                * **Polaridade:** Quanto maior melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Unidade.

                **Modelo Matemático:**
                $$ITCD = \frac{(DG) + (DA \times 2) + (DE \times 3) + (DM \times 4) + (DD \times 5)}{TDE}$$

                ---
                ### Componentes e Definições

                * **Docentes Ponderados por Titulação**
                  * **Fonte:** PNP (SIAPE / Revalide)
                  * **Definição:** Quantidade de Docentes Graduados (DG) $\times 1$, Aperfeiçoados (DA) $\times 2$, Especialistas (DE) $\times 3$, Mestres (DM) $\times 4$ e Doutores (DD) $\times 5$.

                * **TDE - Total de Docentes Efetivos**
                  * **Fonte:** PNP (SIAPE / Revalide)
                  * **Definição:** Quantidade total de professores efetivos afastados ou não.
                """
            )

        with st.expander("🏢 Índice de Verticalização - IV", expanded=False):
            st.markdown(
                r"""
                Este indicador busca verificar a condição de verticalização dos cursos oferecidos por uma mesma unidade acadêmica em um mesmo eixo tecnológico, considerando vagas de ingresso em 04 categorias: QP, CT, CG e PG.

                * **Meta:** Não há meta prevista em nenhum instrumento normativo.
                * **Polaridade:** Quanto maior melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Subeixo Tecnológico.

                **Modelo Matemático:**
                $$IV = \left[\left(\frac{V_{QP}}{V_{CT}}\right) \times 0{,}397\right] + \left[\left(\frac{V_{CT}}{V_{CG}}\right) \times 0{,}365\right] + \left[\left(\frac{V_{CG}}{V_{PG}}\right) \times 0{,}095\right] + \left[\left(\frac{V_{CT}}{V_{PG}}\right) \times 0{,}089\right] + \left[\left(\frac{V_{QP}}{V_{CG}}\right) \times 0{,}028\right] + \left[\left(\frac{V_{QP}}{V_{PG}}\right) \times 0{,}026\right]$$

                ---
                ### Componentes e Definições

                * **Vagas por Nível de Ensino**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Total de Vagas de Ingresso ofertadas em Qualificação Profissional ($V_{QP}$), Cursos Técnicos ($V_{CT}$), Graduação ($V_{CG}$) e Pós-Graduação ($V_{PG}$).
                """
            )

        with st.expander("📌 Matrículas Equivalentes - Meq", expanded=False):
            st.markdown(
                r"""
                Este indicador converte a quantidade de Matrículas em Matrículas Equivalentes.

                * **Meta:** Não há meta prevista em nenhum instrumento normativo.
                * **Polaridade:** Quanto maior melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Unidade.

                **Modelo Matemático:**
                $$Meq = (M \times FECH \times FEC)$$

                ---
                ### Componentes e Definições

                * **M – Matrículas**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de alunos que estiveram com matrícula ativa em pelo menos um dia no ano de referência.

                * **FECH - Fator de Equiparação de Carga Horária**
                  * **Fonte:** Portaria 51/2018
                  * **Definição:** Para os cursos de qualificação profissional é calculated pela razão entre a carga horária mínima regulamentada do curso (CHMR) e carga horária padrão de 800 horas anuais. Para os demais cursos, o FECH é igual a 1.

                * **FEC - Fator de Esforço de Curso**
                  * **Fonte:** Anexo II da Portaria 51/2018
                  * **Definição:** Ajusta a contagem de matrículas-equivalentes para cursos que demandem, para o desenvolvimento de suas atividades, uma maior relação professor/aluno. O FEC é elaborado pelo Grupo de Especialistas da PNP a partir das informações apresentadas pelas instituições da Rede Federal EPCT.
                """
            )

        with st.expander("👨‍🏫 Matrículas por Professor - RAP", expanded=False):
            st.markdown(
                r"""
                Este indicador mede a relação entre a quantidade de matrículas equivalentes e a quantidade de docentes efetivos ponderados pelo tipo de Regime de Trabalho.

                * **Meta:** 20 - estratégias 11.11 e 12.3 previstas na Lei 13.005/2014.
                * **Polaridade:** Quanto maior melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Unidade.

                **Modelo Matemático:**
                $$RAP = \frac{(MeqCG \times FCG) + MeqDC}{DEq}$$

                ---
                ### Componentes e Definições

                * **MeqCG / MeqDC - Matrículas Equivalentes**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Matrículas equivalentes em Cursos de Graduação (MeqCG) e nos demais cursos (MeqDC).
                  * **FCG - Fator de Correção de Graduação:** $FCG = 20 / 18 = 1{,}111...$

                * **DEq - Docentes Equivalentes**
                  * **Fonte:** PNP (SIAPE / Revalide)
                  * **Definição:** Professores efetivos em RT 20h $\times 0{,}5$, somado aos professores em RT 40h e RDE.
                """
            )

        with st.expander("🏫 Matrículas Presenciais por Professor – RAP Presencial", expanded=False):
            st.markdown(
                r"""
                Este indicador mede a relação entre a quantidade de matrículas equivalentes em cursos na modalidade presencial e a quantidade de docentes efetivos ponderados pelo tipo de Regime de Trabalho.

                * **Meta:** 20 - estratégias 11.11 e 12.3 previstas na Lei 13.005/2014.
                * **Polaridade:** Ultrapassado o mínimo estabelecido, quanto mais próximo da meta melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Unidade.

                **Modelo Matemático:**
                $$RAP \text{ Presencial} = \frac{(MeqPCG \times FCG) + MeqPDC}{DEq}$$

                ---
                ### Componentes e Definições

                * **MeqPCG / MeqPDC - Matrículas Presenciais**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Matrículas equivalentes presenciais em Cursos de Graduação (MeqPCG) e nos demais cursos presenciais (MeqPDC).

                * **DEq - Docentes Equivalentes**
                  * **Fonte:** PNP (SIAPE / Revalide)
                  * **Definição:** Professores efetivos em RT 20h $\times 0{,}5$, somado aos professores em RT 40h e RDE.
                """
            )

        with st.expander("🎓 Percentual Matrículas Equivalentes em Cursos Técnicos - MeqCT [%]", expanded=False):
            st.markdown(
                r"""
                Este indicador mede o percentual de matrículas equivalentes vinculadas a Cursos Técnicos.

                * **Meta:** Portaria 357/2026 (Campi com autorização de funcionamento a partir de 1 de janeiro de 2023: meta 80%; até 31/12/2022: meta 50%).
                * **Polaridade:** Ultrapassado o mínimo estabelecido, quanto mais próximo do centro da meta melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Unidade.

                **Modelo Matemático:**
                $$MeqCT[\%] = \frac{MeqCT}{Meq} \times 100$$

                ---
                ### Componentes e Definições

                * **MeqCT - Matrículas Equivalentes em Cursos Técnicos**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas em Cursos Técnicos que estiveram ativas em pelo menos um dia no ano de referência, ponderada pelos fatores de equivalência previstos.

                * **Meq - Matrículas Equivalentes**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas que estiveram ativas em pelo menos um dia no ano de referência, ponderada pelos fatores de equivalência previstos.
                """
            )

        with st.expander("📚 Percentual de Matrículas Equivalentes em Educação de Jovens e Adultos - MeqEJA [%]", expanded=False):
            st.markdown(
                r"""
                Este indicador mede o percentual de matrículas equivalentes na modalidade EJA, tanto nos cursos de Formação Inicial e Continuada de Trabalhadores (FIC) quanto nos cursos de educação profissional técnica de nível médio contemplados no programa nacional de integração da educação profissional com a educação básica na modalidade EJA.

                * **Meta:** Mínimo de 10% - §1º do Art. 2º do Decreto 5.840/2006.
                * **Polaridade:** Ultrapassado o mínimo estabelecido, quanto mais próximo do centro da meta, melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Unidade.

                **Modelo Matemático:**
                $$MeqEJA[\%] = \frac{MeqEJA}{Meq} \times 100$$

                ---
                ### Componentes e Definições

                * **MeqEJA - Matrículas Equivalentes em Educação de Jovens e Adultos**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas em Curso FIC ou técnico integrado contemplado pelo programa EJA que estiveram ativas por pelo menos um dia no ano de referência, ponderada pelos fatores de equivalência previstos.

                * **Meq - Matrículas Equivalentes**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas que estiveram ativas em pelo menos um dia no ano de referência, ponderada pelos fatores de equivalência previstos.
                """
            )

        with st.expander("👨‍🏫 Percentual de Matrículas Equivalentes em Formação de Professores - MeqFP [%]", expanded=False):
            st.markdown(
                r"""
                Este indicador mede o percentual de matrículas equivalentes vinculadas à formação de professores.

                * **Meta:** Mínimo de 20% - Art. 8º da Lei 11.892/2008.
                * **Polaridade:** Ultrapassado o mínimo estabelecido, quanto mais próximo do centro da meta melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Unidade.

                **Modelo Matemático:**
                $$MeqFP[\%] = \frac{MeqFP}{Meq} \times 100$$

                ---
                ### Componentes e Definições

                * **MeqFP - Matrículas Equivalentes em Formação de Professores**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas em Cursos destinados à formação de professores que estiveram ativas em pelo menos um dia no ano de referência, ponderada pelos fatores de equivalência previstos.

                * **Meq - Matrículas Equivalentes**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas que estiveram ativas em pelo menos um dia no ano de referência, ponderada pelos fatores de equivalência previstos.
                """
            )

        with st.expander("📝 Relação de Inscritos por Vagas - RIV", expanded=False):
            st.markdown(
                r"""
                Este indicador mede a relação entre a quantidade de candidatos inscritos e a quantidade de vagas disponibilizadas.

                * **Meta:** Não há meta prevista em nenhum instrumento normativo.
                * **Polaridade:** Quanto maior melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Curso.

                **Modelo Matemático:**
                $$RIV = \frac{I}{V}$$

                ---
                ### Componentes e Definições

                * **I - Inscritos**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Candidatos que concorreram às vagas disponibilizadas para a fase inicial dos cursos, em suas diversas formas de ingresso, no ano de referência.

                * **V - Vagas Disponibilizadas**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade total de vagas disponibilizadas para a fase inicial dos cursos, em suas diversas formas de ingresso, no ano de referência.
                """
            )

        with st.expander("⏳ Retenção Ciclo – RCiclo [%]", expanded=False):
            st.markdown(
                r"""
                Este indicador mede o percentual de retidos em um Ciclo de Matrícula, sendo que para este cálculo é empregado o conceito de matrícula e não de matrícula equivalente.

                * **Meta:** Não há meta prevista em nenhum instrumento normativo.
                * **Polaridade:** Quanto menor melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Curso.

                **Modelo Matemático:**
                $$RCiclo[\%] = \frac{RCiclo}{MCiclo} \times 100$$

                ---
                ### Componentes e Definições

                * **RCiclo - Retidos no Ciclo**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Alunos que permaneceram matriculados por período superior ao tempo previsto para a integralização do curso, considerando apenas as matrículas vinculadas a ciclos com término previsto para o ano anterior ao ano de referência.

                * **MCiclo - Matrículas no Ciclo**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas efetuadas no início do ciclo de matrícula.
                """
            )

        with st.expander("📉 Taxa de Evasão Anual – Ev [%]", expanded=False):
            st.markdown(
                r"""
                Este indicador mede o percentual de matrículas que perderam o vínculo com a instituição no ano de referência sem a conclusão do curso em relação ao total de matrículas. Para este cálculo é empregado o conceito de matrícula e não de matrícula equivalente.

                * **Meta:** 10% - derivado da análise das estratégias 11.11 e 12.3 previstas na Lei 13.005/2014.
                * **Polaridade:** Quanto menor melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Curso.

                **Modelo Matemático:**
                $$Ev[\%] = \frac{Ev}{M} \times 100$$

                ---
                ### Componentes e Definições

                * **Ev - Evadidos**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Alunos que perderam vínculo com a instituição antes da conclusão do curso.

                * **M - Matrículas**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Soma de todos os alunos que estiveram com matrícula ativa em pelo menos um dia no ano de referência.
                """
            )

        with st.expander("📌 Taxa de Ocupação - TO", expanded=False):
            st.markdown(
                r"""
                Este indicador mede o percentual de vagas ocupadas no ano de referência em relação às vagas disponibilizadas em cada tipo de curso, excetuando-se os cursos de Qualificação Profissional.

                * **Meta:** Não há meta prevista em nenhum instrumento normativo.
                * **Polaridade:** Quanto maior melhor.
                * **Agregação Máxima:** Rede Federal | **Agregação Mínima:** Tipo de Curso.

                **Modelo Matemático:**
                $$TO[\%] = \frac{M}{V_{\text{ciclos DNE}}}$$

                ---
                ### Componentes e Definições

                * **M - Matrículas**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de matrículas.

                * **$V_{\text{ciclos DNE}}$ - Vagas em Ciclos Válidos**
                  * **Fonte:** PNP (SISTEC / Revalide)
                  * **Definição:** Quantidade de vagas de ingresso ofertadas nos ciclos de matrículas com data não expirada.
                """
            )

        st.markdown("---")

        with st.expander("💡 Exemplo Prático de Cálculo por Ciclo (Metodologia PNP)", expanded=False):
            st.markdown(
                r"""
                **Cenário Exemplo:**
                Um curso Técnico em Edificações Integrado ao Ensino Médio com duração prevista para **4 anos** teve **40 ingressantes em janeiro de 2013**, tendo, portanto, o *ciclo encerrado* em dezembro de 2016.

                O método de análise da PNP prevê neste caso que, em **31 de dezembro de 2017** (um ano após o término do ciclo iniciado em 2013), seja realizado o levantamento da situação de matrícula dos 40 alunos ingressantes em janeiro/2013.

                Considerando que esses 40 alunos matriculados em 2013, no momento do levantamento feito em 31 de dezembro de 2017, apresentaram a seguinte situação de matrícula:

                * **20 alunos (50%) Concluintes:**
                  * **16 alunos (40%):** Concluíram todos os componentes curriculares (*Formados*).
                  * **4 alunos (10%):** Concluíram todas as unidades curriculares, mas ainda não podem receber a certificação (*Integralizados em fase escolar*).
                * **8 alunos (20%) Evadidos:** Perderam o vínculo com a instituição.
                * **12 alunos (30%) Retidos:** Ainda estão matriculados em alguma das unidades curriculares.

                ---
                ### Resultados apresentados pela PNP no Ano de Referência (2018)

                * **Conclusão por Ciclo (CCiclo):** **50%** *(Formados + Integralizados em fase escolar)*
                * **Evasão por Ciclo (EvCiclo):** **20%**
                * **Retenção por Ciclo (RCiclo):** **30%**
                * **Eficiência:** **71,4% [20 / (20 + 8)] x 100**
                """
            )

        st.markdown("---")
        st.caption("**Referência:** [Plataforma PNP](https://www.gov.br/mec/pt-br/pnp)")

    with tab_conif:
        st.markdown("#### Conif")
        aba_matriz, aba_assistencia = st.tabs(["Matriz Orçamentária", "Assistência Estudantil"])
        
        with aba_matriz:
            st.markdown(
                r"""
                ### Metodologia de Cálculo da Matriz de Distribuição Orçamentária da RFEPCT
                *(Portaria MEC nº 243, de 10 de março de 2026)*

                O cálculo da Matriz de Distribuição Orçamentária da RFEPCT utiliza o conjunto de dados acadêmicos informados pelas instituições no Sistema Nacional de Informações da Educação Profissional e Tecnológica (Sistec) e consolidados na Plataforma Nilo Peçanha (PNP). A Matriz de um dado ano é elaborada com dados da PNP do ano anterior.
                """
            )

            st.markdown("---")
            st.markdown("### 📊 Divisão Geral do Orçamento (Art. 3º)")
            st.markdown(
                r"""
                A distribuição orçamentária inicia-se deduzindo do Orçamento Total ($OT$) o montante destinado à **Assistência Estudantil ($AE$)**. Do valor restante, os recursos são distribuídos nos seguintes blocos:
                * 🔲 **80%** para o **Bloco de Funcionamento ($F$)**
                * 🏛️ **10%** para o **Bloco de Reitoria / Direção-Geral ($R$)**
                * 🏆 **10%** para o **Bloco de Qualidade e Eficiência ($QE$)**

                **Fórmulas da Divisão:**
                $$F = 0{,}8 \times (OT - AE)$$
                $$R = 0{,}1 \times (OT - AE)$$
                $$QE = 0{,}1 \times (OT - AE)$$
                """
            )

            st.markdown("---")
            st.markdown("### 📝 Passos do Cálculo do Bloco de Funcionamento - Matrícula Total")

            with st.expander("🔹 1º Passo: Cálculo da Quantidade de Dias do Ciclo (QTDC)", expanded=False):
                st.markdown(
                    r"""
                    Calcula a duração total prevista do ciclo em dias:
                    $$QTDC = (DTC - DIC) + 1$$
                    * **$QTDC$**: Quantidade de Dias do Ciclo.
                    * **$DTC$**: Data Prevista do Término do Ciclo.
                    * **$DIC$**: Data do Início do Ciclo.
                    """
                )

            with st.expander("🔹 2º Passo: Cálculo da Carga Horária Média Diária (CHMD)", expanded=False):
                st.markdown(
                    r"""
                    Distribui a carga horária ajustada do curso pela quantidade de dias do ciclo:
                    $$CHMD = \frac{CHM}{QTDC}$$
                    * **$CHMD$**: Carga Horária Média Diária.
                    * **$CHM$**: Carga Horária por Matriz (ajustada conforme o Catálogo Nacional de Cursos Técnicos - CNCT).
                    * **$QTDC$**: Quantidade de Dias do Ciclo.
                    """
                )

            with st.expander("🔹 3º Passo: Cálculo da Carga Horária Anualizada (CHA)", expanded=False):
                st.markdown(
                    r"""
                    Converte a carga horária diária para uma base anual padrão de 365 dias:
                    * **Se $QTDC > 365$ dias:**
                      $$CHA = CHMD \times 365$$
                    * **Se $QTDC \le 365$ dias:**
                      $$CHA = CHM$$
                    """
                )

            with st.expander("🔹 4º Passo: Cálculo do Fator de Equalização de Carga Horária (FECH)", expanded=False):
                st.markdown(
                    r"""
                    Equipara a carga horária em relação à carga horária padrão de 800 horas anuais:
                    * **Se $QTDC > 365$ dias:**
                      $$FECH = \frac{CHA}{800}$$
                    * **Se $QTDC \le 365$ dias:**
                      $$FECH = \frac{CHC}{800}$$
                    * **$CHC$**: Carga Horária do Ciclo.
                    """
                )

            with st.expander("🔹 5º Passo: Cálculo dos Dias Ativos do Ciclo no Período Analisado (DACP₁ a DACP₅)", expanded=False):
                st.markdown(
                    r"""
                    Determina a quantidade de dias ativos do ciclo dentro do ano civil analisado:

                    * **$DACP_1$ (Ciclo com duração integral no período):**
                      $$DACP_1 = (DFP1P - DIP1P) + 1$$

                    * **$DACP_2$ (Ciclo iniciado dentro do período e que termina após):**
                      $$DACP_2 = (DFP1P - DIC) + 1$$

                    * **$DACP_3$ (Ciclo iniciado antes do período e finalizado dentro dele):**
                      $$DACP_3 = (DTC - DIP1P) + 1$$

                    * **$DACP_4$ (Ciclo que inicia e termina dentro do próprio período):**
                      $$DACP_4 = (DTC - DIC) + 1$$

                    * **$DACP_5$ (Ciclo finalizado antes do período, mas com alunos retidos ainda ativos):**
                      $$DACP_5 = \frac{(DFP1P - DIP1P) + 1}{2}$$

                    ---
                    * **$DIP1P$**: Data do Início do Período Analisado (01/jan).
                    * **$DFP1P$**: Data do Final do Período Analisado (31/dez).
                    """
                )

            with st.expander("🔹 6º Passo: Cálculo do Fator de Equalização de Dias Ativos (FEDA)", expanded=False):
                st.markdown(
                    r"""
                    Pondera a proporção de dias em que o ciclo esteve ativo no ano em relação ao total do período analisado:
                    $$FEDA = \frac{DACP_1 + DACP_2 + DACP_3 + DACP_4 + DACP_5}{(DFP1P - DIP1P) + 1}$$
                    """
                )

            with st.expander("🔹 7º Passo: Cálculo do Fator de Equalização de Carga Horária e Dias Ativos (FECHDA)", expanded=False):
                st.markdown(
                    r"""
                    Combina o fator de carga horária ($FECH$) com o fator de dias ativos ($FEDA$):
                    $$FECHDA = FECH \times FEDA$$
                    """
                )

            with st.expander("🔹 8º Passo: Cálculo das Matrículas Equalizadas por Carga Horária e Dias Ativos (MECHDA)", expanded=False):
                st.markdown(
                    r"""
                    Consolida o quantitativo de matrículas ativas ($QTM1P$):
                    * **Para matrículas em ciclo regular:**
                      $$MECHDA = FECHDA \times QTM1P$$
                    * **Para alunos em retenção (até 3 anos após o término previsto do ciclo):**
                      Aplica-se fator qualitativo de $50\%$:
                      $$MECHDA = FECHDA \times QTM1P \times 50\%$$
                    *(Nota: Alunos ativos há mais de 3 anos do término de seu ciclo não são considerados).*
                    """
                )

            with st.expander("🔹 9º Passo: Cálculo das Matrículas Ponderadas (MP)", expanded=False):
                st.markdown(
                    r"""
                    Aplica o peso de grupo do curso ($PC$) sobre as matrículas equalizadas:
                    $$MP = MECHDA \times PC$$
                    * **$PC$**: Peso do Curso (baseado no número de laboratórios e eixo tecnológico).
                    """
                )

            with st.expander("🔹 10º Passo: Cálculo do Bônus para Cursos de Agropecuária (BA)", expanded=False):
                st.markdown(
                    r"""
                    Aplica bonificação para manutenção de infraestrutura de fazenda-escola:
                    * **Se Curso de Agropecuária = "Sim":**
                      $$BA = MP \times 50\%$$
                    * **Se Curso de Agropecuária = "Não":**
                      $$BA = 0$$
                    """
                )

            with st.expander("🔹 11º Passo: Cálculo das Matrículas Totais (MT)", expanded=False):
                st.markdown(
                    r"""
                    Soma a Matrícula Ponderada ao Bônus de Agropecuária:
                    $$MT = MP + BA$$
                    """
                )

            with st.expander("🌐 Ponderação para Cursos na Modalidade a Distância (EaD)", expanded=False):
                st.markdown(
                    r"""
                    A valoração das matrículas de Educação a Distância equipara-se à presencial conforme o tipo de financiamento:
                    * **Financiamento Próprio:** Equipara-se a **80%** da Matrícula Presencial.
                    * **Financiamento Externo (UAB, Novos Caminhos):** Equipara-se a **25%** da Matrícula Presencial.
                    * **Cursos ON-LINE MOOC:** Equiparam-se a **8%** da Matrícula Presencial.

                    **Fórmula Generalizada:**
                    $$MEAD = CMTD25 + CMTD80 + CMTM08$$
                    """
                )

            with st.expander("🏆 Bloco Qualidade e Eficiência (Indicadores e Faixas)", expanded=False):
                st.markdown(
                    r"""
                    O Bloco de Qualidade e Eficiência ($QE$) avalia os indicadores institucionais no âmbito geral da instituição:

                    1. **IEA Equalizado (Índice de Eficiência Acadêmica):** Compara a eficiência da instituição com a média da Rede Federal ($IEA_{Rede}$), atribuindo pesos de $0{,}5$ a $2{,}5$.
                    2. **RAPP Equalizada (Relação Aluno-Professor Presencial):** Considera a meta de $20$ alunos/professor (Lei nº 13.005/2014), com pesos variando de $0$ ($<18$) a $2{,}5$ ($\ge 22$).
                    3. **IAML Equalizado (Índice de Atendimento ao Marco Legal):** Média ponderada do atendimento às metas do Art. 8º da Lei nº 11.892/2008:
                       * **Cursos Técnicos (CT - Meta 50%):** Peso 7 na composição.
                       * **Formação de Professores (FP - Meta 20%):** Peso 2 na composição.
                       * **Educação de Jovens e Adultos (EJA - Meta 10%):** Peso 1 na composição.

                    **Fórmula do IAML Equalizado:**
                    $$IAML^{Equal} = 0{,}7 \times CT^{Equal} + 0{,}2 \times FP^{Equal} + 0{,}1 \times EJA^{Equal}$$
                    """
                )

            st.markdown("---")
            st.caption("**Fonte Normativa:** [PORTARIA MEC Nº 243, DE 10 DE MARÇO DE 2026](https://www.in.gov.br/web/dou/-/portaria-mec-n-243-de-10-de-marco-de-2026-692098706)")
            
        with aba_assistencia:
            st.markdown(
                r"""
                ### Cálculos do Bloco Assistência Estudantil
                *(Portaria MEC nº 243, de 10 de março de 2026)*

                O Bloco de Assistência Estudantil ($AE$) atende aos estudantes dos cursos presenciais, a distância (EaD) e em Regime de Internato Pleno (RIP), com base na vulnerabilidade socioeconômica aferida pela Renda Familiar Per Capita (RFP).
                """
            )
            st.markdown("---")

            with st.expander("🔹 Componentes da Matriz de Assistência Estudantil", expanded=False):
                st.markdown(
                    r"""
                    **Fórmula Geral:**
                    $$MAE = MAEP + MAEEAD + MAERIP$$

                    * **$MAEP$**: Matriz Assistência Estudantil - Matrículas Presenciais.
                    * **$MAEEAD$**: Matriz Assistência Estudantil - Matrículas EaD.
                    * **$MAERIP$**: Matriz Assistência Estudantil - Alunos em Regime de Internato Pleno.

                    ---
                    #### Cálculo para Internato Pleno (RIP):
                    $$MAERIP = QRIP \times AERIP$$
                    * **$QRIP$**: Quantidade de Alunos em Regime de Internato Pleno.
                    * **$AERIP$**: Valor de referência do per capita para Assistência Estudantil RIP.
                    """
                )

            with st.expander("📊 Atribuição de Pesos na RFP para Assistência Estudantil (Tabela 6)", expanded=False):
                st.markdown(
                    r"""
                    A distribuição dos recursos fundamenta-se nas faixas de **Renda Familiar Per Capita (RFP)** dos estudantes matriculados:

                    | Declaração da Renda | Pesos Oficial Portaria 243/2026 |
                    | :--- | :---: |
                    | $0 < \text{RFP} \le 0{,}5\text{ SM}^*$ | **2,5** |
                    | $0{,}5 < \text{RFP} \le 1{,}0\text{ SM}^*$ | **2,0** |
                    | $1{,}0 < \text{RFP} \le 1{,}5\text{ SM}^*$ | **1,5** |
                    | $1{,}5 < \text{RFP} \le 2{,}5\text{ SM}^*$ | **1,0** |
                    | $2{,}5 < \text{RFP} \le 3{,}5\text{ SM}^*$ | **0,5** |
                    | $\text{RFP} \ge 3{,}5\text{ SM}^*$ | **0** |
                    | $\text{RFP - Não Informada}$ | **0** |

                    $$\text{* SM: Salário Mínimo}$$
                    """
                )

            with st.expander("🔹 Roteiro para Apuração das Matrículas Equalizadas pela Renda", expanded=False):
                st.markdown(
                    r"""
                    1. **Identificação das Matrículas Próprias:** Considera-se exclusivamente as matrículas mantidas por orçamento próprio.
                    2. **Segregação por Modalidade:** Separa-se a quantidade de matrículas entre Presencial e EaD.
                    3. **Distribuição Percentual de Declarantes:** Identifica-se a proporção de alunos declarantes em cada faixa de RFP.
                    4. **Cálculo da Matrícula Equalizada pela Renda:** Multiplica-se a quantidade total de matrículas da modalidade pelo percentual de declarantes na faixa e pelo peso de renda da **Tabela 6**.
                    """
                )

            st.markdown("---")
            st.caption("**Fonte Normativa:** [PORTARIA MEC Nº 243, DE 10 DE MARÇO DE 2026](https://www.in.gov.br/web/dou/-/portaria-mec-n-243-de-10-de-marco-de-2026-692098706)")