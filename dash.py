# pip install streamlit
# pip install plotly
# pip install streamlit_option_menu

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao

# ******Primeira consulta / Atualizações de dados ****** 
query = "select * from tb_carro"

#armazenando o resultado da consulta
df = conexao(query)

#botão para atualizar dados 
if st.button("Atualizar Dados"):
    df = conexao(query)


# ******Estrutura lateral de filtros******

modelo = st.sidebar.multiselect("Modelo Selecionado",options=df['modelo'].unique(),default=df['modelo'].unique())

st.sidebar.header("Selecione o Filtro")
marca = st.sidebar.multiselect("Marca Selecionada", #Nome do seletor 
                               options=df['marca'].unique(), #fazendo linda por valores unicos da coluna marca
                               default=df['marca'].unique()
                               )

valor = st.sidebar.multiselect("Valor Selecionado",options=df['valor'].unique(),default=df['valor'].unique())

cor = st.sidebar.multiselect("Cor Selecionada",options=df['cor'].unique(),default=df['cor'].unique())

numero_vendas = st.sidebar.multiselect("Vendas Selecionado",options=df['numero_vendas'].unique(),default=df['numero_vendas'].unique())

ano = st.sidebar.multiselect("Ano Selecionado",options=df['ano'].unique(),default=df['ano'].unique())

df_selecionado = df[
    (df['marca'].isin(marca)) &
    (df['modelo'].isin(modelo)) &
    (df['valor'].isin(valor)) &
    (df['cor'].isin(cor)) &
    (df['numero_vendas'].isin(numero_vendas)) &
    (df['ano'].isin(ano)) 
]



# ****** Exibir valores medios = estatistica *****
def home():
    with st.expander("Valores"): #Criando uma caixa espancivel com titulo
        mostrarDados = st.multiselect('Filter',df_selecionado,default=[])

        #verificando se colunas foram selelcionadas para serem exibidas
        if mostrarDados: 
            #exibindo os dados pelo filtros selecionados
            st.write(df_selecionado[mostrarDados])

        if not df_selecionado.empty:
            numero_vendas = df_selecionado['numero_vendas'].sum()
            venda_media = df_selecionado['numero_vendas'].mean()
            valor_mediana = df_selecionado['numero_vendas'].median()
    
            total1, total2, total3 = st.columns(3, gap='large')

            with total1:
                st.info('Soma Total de Vendas', icon='📌')
                st.metric(label='Total', value=f'{numero_vendas:,.0f}')

            with total2:
                st.info('Media de Vendas Carros',icon='📌')
                st.metric(label='Total', value=f'{venda_media:,.0f}')

            with total3:
                st.info('Mediana de Vendas',icon='📌')
                st.metric(label='Total', value=f'{valor_mediana:,.0f}')
        else:
            st.warning("Nenhum dado sisponivel com os filtros selecionados")#mensagem informando sem dados 

        st.markdown("""------""")#linha divisoria para dividir as seções 

#******Graficos***********
def graficos(df_selecionado):
    
    if df_selecionado.empty:
        st.warning("Nenhum dado sisponivel com os filtros selecionados")#mensagem informando sem dados
        return

    graf1, graf2, graf3, graf4 , graf5 = st.tabs(['Grafico de Barras', "Grafico de Linhas", "Grafico de Pizza", "Grafico de Dispersão", "Distrribuição 3D"])
    
    with graf1:
        st.write('Grafico de Barras') # Titulo

    investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)
            #agrupando pela marca e conta o nuemro de ocorrencias da coluna valor, depois ordena o resultado decrescente 

    fig_valores = px.bar(investimento, #contem os dados sobre os valores por marca
                        x=investimento.index,
                        y='valor',
                        orientation='h',
                        title='<b>Valores de Carrros</b>',
                        color_discrete_sequence=['#0083b3']
    )

    st.plotly_chart(fig_valores, use_container_width=True) #exu=ibe o grafico/ use ajusta o tamanho na tela 

    with graf2:
        st.write('Grafico de Linhas')
        dados = df_selecionado.groupby('marca').count()[['valor']]

        fig_valores2 = px.line(dados, 
                            x=dados.index,
                            y='valor', 
                            title="<b>Valores por Marca</b>", 
                            color_discrete_sequence=['#0083b3']
                            )

        st.plotly_chart(fig_valores2, use_container_width=True)

    with graf3:
        st.write('Grafico de Pizza')
        dados2 = df_selecionado.groupby('marca').sum()[['valor']]

        fig_valores3 = px.pie(dados2, values='valor', names=dados2.index, title='Distribuiçaõ de Valores por Marca')

        st.plotly_chart(fig_valores3, use_container_width=True)


    with graf4:
        st.write('Grafico de Dispersão')
        dados3 = df_selecionado.melt(id_vars=['marca'], value_vars=['valor'])

        fig_valores4 = px.scatter(dados3,x='marca',y='value',color='variable',title='<b>Dispersão de Valores por Marca</b>')

        
        st.plotly_chart(fig_valores4, use_container_width=True)

    with graf5:
        st.write('Distrribuição 3D')

        # Agrupando os dados por 'marca' e contando os valores
        dados4 = df_selecionado.groupby('marca').count()[['valor']].reset_index()  # Resetando o índice para usar 'marca' como coluna

        # Verifique se os dados foram agrupados corretamente
        st.write(dados4)

        # Criando o gráfico 3D com Plotly
        fig_valores5 = px.line_3d(dados4, 
                                    x='marca',            # Eixo X com a coluna 'marca'
                                    y='valor',            # Eixo Y com a contagem de 'valor'
                                    z=dados4.index,      # Eixo Z com o índice, você pode alterar se necessário
                                    title="<b>Distrribuição 3D Marca/Valor</b>", 
                                    color_discrete_sequence=['#0083b3'])

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig_valores5, use_container_width=True)

def barraprogresso():
    valorAtual = df_selecionado['numero_vendas'].sum()
    obetivo = 10200000
    percentual = round((valorAtual/obetivo*100))
    

    if percentual > 100:
        st.subheader("Valores Atingidos!")
    else:
        st.write(f'Voce tem {percentual}% de {obetivo}')
        mybar = st.progress(0)
        for percentualCompleto in range(percentual):
            mybar.progress(percentualCompleto + 1, text = "Alvo %")


#****Menu Lateral ****************
def menulateral():
    with st.sidebar:
        selecionado = option_menu(menu_title="Menu", options=["Home", "Progresso"], icons=['house','eye'],menu_icon=['cast'],default_index=0)

    if selecionado == "Home":
        st.subheader(f'Pagina: {selecionado}')
        home()
        graficos(df_selecionado)
    
    if selecionado == 'Progresso':
        st.subheader(f'Pagina: {selecionado}')
        barraprogresso()
        graficos(df_selecionado)


#************Ajustar CSS*************

menulateral()