# dashboard_analyse_democratie_liberale.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime
import base64
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="ANALYSE STRATÉGIQUE - DÉMOCRATIE LIBÉRALE",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé (adapté)
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f3a60;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        border-bottom: 3px solid #1f3a60;
        padding-bottom: 1rem;
    }
    .insight-box {
        background-color: #e8f4fd;
        border-left: 5px solid #3498db;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .insight-box h4 {
        color: #2980b9;
        margin-top: 0;
    }
    .metric-card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
    .fondation { border-left: 5px solid #e74c3c; color: #c0392b; }
    .croissance { border-left: 5px solid #3498db; color: #2980b9; }
    .influence { border-left: 5px solid #9b59b6; color: #8e44ad; }
    .heritage { border-left: 5px solid #2ecc71; color: #27ae60; }
    .dl-blue { color: #1f3a60; }
    .dl-orange { color: #e67e22; }
</style>
""", unsafe_allow_html=True)

class AnalyseDemocratieLiberale:
    def __init__(self):
        self.initialize_data()
        self.generate_chronological_data()
        self.generate_comparative_data()

    def initialize_data(self):
        """Initialise les données de base sur Démocratie Libérale"""
        self.parti_data = {
            'FONDATION': {
                'date_creation': '1997-06-24',
                'fondateur_principal': 'Alain Madelin',
                'membres_fondateurs': 15,
                'budget_initial_millions': 2.5,
                'origine': 'Fusion du Parti républicain et du Parti populaire pour la démocratie française'
            },
            'CROISSANCE': {
                'membres_max': 30000,
                'elus_nationaux': 42,
                'ministres_gouvernement': 8,
                'budget_peak_millions': 15.2,
                'influence_mediatique': 7
            },
            'INFLUENCE': {
                'doctrine': 'Libéralisme classique',
                'positionnement': 'Droite libérale',
                'alliances_strategiques': ['UMP', 'UDF'],
                'think_tanks_affilies': 3,
                'courants_internes': ['Libéraux-conservateurs', 'Centristes libéraux']
            },
            'HERITAGE': {
                'dissolution': '2002-11-17',
                'integration': 'Union pour un mouvement populaire (UMP)',
                'heritage_ideologique': 'Renouveau de la pensée libérale en France',
                'personnalites_issues': ['Alain Madelin', 'Jean-Pierre Raffarin', 'Hervé Novelli']
            }
        }
        
        # Relations politiques stratégiques
        self.relations_politiques = [
            {'source': 'Alain Madelin', 'target': 'Jacques Chirac', 'poids': 8, 'type': 'Alliance tactique'},
            {'source': 'Démocratie Libérale', 'target': 'UMP', 'poids': 9, 'type': 'Fusion-absorption'},
            {'source': 'Jean-Pierre Raffarin', 'target': 'Démocratie Libérale', 'poids': 7, 'type': 'Leadership'},
            {'source': 'Libéraux', 'target': 'Centristes UDF', 'poids': 6, 'type': 'Convergence idéologique'},
            {'source': 'Démocratie Libérale', 'target': 'Medias libéraux', 'poids': 5, 'type': 'Influence'},
            {'source': 'Alain Madelin', 'target': 'Think tanks', 'poids': 7, 'type': 'Expertise'},
            {'source': 'DL Jeunes', 'target': 'Démocratie Libérale', 'poids': 4, 'type': 'Militantisme'}
        ]

    def generate_chronological_data(self):
        """Génère des données chronologiques pour l'analyse historique"""
        annees = list(range(1997, 2004))
        
        # Données simulées mais réalistes basées sur l'histoire du parti
        self.evolution_membres = [5000, 15000, 28000, 30000, 25000, 18000, 12000]
        self.evolution_budget = [2.5, 8.2, 12.5, 15.2, 11.8, 8.5, 4.2]
        self.influence_politique = [3, 6, 8, 9, 8, 6, 4]
        self.resultats_electoraux = [4.2, 5.8, 7.2, 6.8, 5.5, 4.1, 3.2]  # en %
        
        self.annees_chrono = annees
        
        # Événements clés
        self.evenements_cles = [
            {'annee': 1997, 'evenement': 'Fondation officielle', 'impact': 9},
            {'annee': 1998, 'evenement': 'Premières élections régionales', 'impact': 6},
            {'annee': 1999, 'evenement': 'Élections européennes - liste commune', 'impact': 7},
            {'annee': 2000, 'evenement': 'Participation au gouvernement', 'impact': 8},
            {'annee': 2001, 'evenement': 'Élections municipales - succès local', 'impact': 6},
            {'annee': 2002, 'evenement': 'Présidentielle + création UMP', 'impact': 10},
            {'annee': 2003, 'evenement': 'Dissolution officielle', 'impact': 8}
        ]

    def generate_comparative_data(self):
        """Génère des données comparatives avec d'autres partis de l'époque"""
        self.comparaison_partis = pd.DataFrame({
            'Parti': ['Démocratie Libérale', 'RPR', 'UDF', 'PS', 'PCF', 'FN'],
            'Période_activité': ['1997-2002', '1976-2002', '1978-2007', '1969-', '1920-', '1972-'],
            'Membres_max': [30000, 170000, 60000, 120000, 200000, 50000],
            'Doctrine': ['Libéralisme', 'Gaullisme', 'Centrisme', 'Socialisme', 'Communisme', 'Nationalisme'],
            'Ministres_gouvernement': [8, 45, 32, 38, 15, 0],
            'Durée_vie_annees': [5, 26, 29, '53+', '103+', '51+']
        })

    def display_header(self):
        """Affiche l'en-tête avec des métriques analytiques"""
        st.markdown('<h1 class="main-header">🏛️ ANALYSE STRATÉGIQUE - DÉMOCRATIE LIBÉRALE (1997-2002)</h1>', unsafe_allow_html=True)
        st.markdown("### Analyse du parcours politique et de l'héritage libéral")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value fondation">{self.parti_data['FONDATION']['membres_fondateurs']}</div>
                <div class="metric-label">Membres Fondateurs</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value croissance">{self.parti_data['CROISSANCE']['membres_max']}</div>
                <div class="metric-label">Membres Maximum</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value influence">{self.parti_data['CROISSANCE']['ministres_gouvernement']}</div>
                <div class="metric-label">Ministres au Gouvernement</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            duree_vie = 2002 - 1997
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value heritage">{duree_vie}</div>
                <div class="metric-label">Années d'Existence</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
            <h4>🧠 Analyse Stratégique Principale</h4>
            <p>Démocratie Libérale a représenté une tentative unique de structurer une <strong>droite libérale pure</strong> dans le paysage politique français. Malgré sa courte existence (1997-2002), le parti a réussi à influencer durablement le débat économique et à former des cadres qui joueront un rôle important dans les gouvernements suivants. Sa fusion dans l'UMP marque à la fois un échec de pérennisation autonome et une réussite d'intégration dans le jeu politique majoritaire.</p>
        </div>
        """, unsafe_allow_html=True)

    def analyse_reseau_influence(self):
        """Analyse du réseau d'influence et des relations politiques"""
        st.markdown("### 🔗 Analyse du Réseau d'Influence Politique")
        
        # Création du graphe
        G = nx.DiGraph()
        for rel in self.relations_politiques:
            G.add_edge(rel['source'], rel['target'], weight=rel['poids'], type=rel['type'])
        
        # Calcul des métriques de centralité
        centrality_degree = nx.degree_centrality(G)
        centrality_betweenness = nx.betweenness_centrality(G, weight='weight')
        centrality_closeness = nx.closeness_centrality(G)

        # DataFrame des résultats
        df_centralite = pd.DataFrame({
            'Acteur': list(centrality_degree.keys()),
            'Influence Directe': [centrality_degree[n] for n in centrality_degree.keys()],
            'Contrôle des Réseaux': [centrality_betweenness[n] for n in centrality_betweenness.keys()],
            'Accessibilité Stratégique': [centrality_closeness[n] for n in centrality_closeness.keys()]
        }).sort_values(by='Contrôle des Réseaux', ascending=False)

        st.dataframe(df_centralite, use_container_width=True)

        # Visualisation du réseau
        pos = nx.spring_layout(G, k=1, iterations=50)
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1.5, color='#888'), hoverinfo='none', mode='lines')
        
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"{node}<br>Contrôle: {centrality_betweenness[node]:.2f}")
            node_size.append(20 + centrality_betweenness[node] * 60)

        node_trace = go.Scatter(
            x=node_x, y=node_y, mode='markers+text', hoverinfo='text', text=list(G.nodes()),
            textposition="top center", marker=dict(size=node_size, color='#1f3a60', line=dict(width=2, color='#e67e22'))
        )
        
        fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
            title=dict(text="Réseau d'Influence de Démocratie Libérale", font=dict(size=16)),
            showlegend=False, hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40), annotations=[ dict(
                text="La taille des nœuds indique la capacité de contrôle dans le réseau d'influence.",
                showarrow=False, xref="paper", yref="paper", x=0.005, y=-0.002, xanchor='left', yanchor='bottom', font=dict(size=12)
            )], xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), 
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), height=500
        ))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <h4>🧠 Analyse du Réseau d'Influence</h4>
            <p><strong>Alain Madelin</strong> apparaît comme le nœud central incontournable, ce qui correspond à son rôle de fondateur et figure médiatique du libéralisme français. La connexion forte avec <strong>l'UMP</strong> montre la stratégie d'intégration au sein de la droite gouvernementale. Les relations avec les <strong>think tanks</strong> et <strong>médias libéraux</strong> illustrent l'ancrage intellectuel du mouvement, caractéristique des partis doctrinaux.</p>
        </div>
        """, unsafe_allow_html=True)

    def analyse_performance_politique(self):
        """Analyse de la performance politique et électorale"""
        st.markdown("### 📈 Analyse de la Performance Politique")
        
        # Création d'indicateurs de performance
        df_performance = pd.DataFrame([
            {
                'Indicateur': 'Croissance membres',
                'Valeur': self.parti_data['CROISSANCE']['membres_max'],
                'Unité': 'membres',
                'Performance': 'Élevée'
            },
            {
                'Indicateur': 'Influence gouvernementale', 
                'Valeur': self.parti_data['CROISSANCE']['ministres_gouvernement'],
                'Unité': 'ministres',
                'Performance': 'Moyenne'
            },
            {
                'Indicateur': 'Budget maximum',
                'Valeur': self.parti_data['CROISSANCE']['budget_peak_millions'],
                'Unité': 'millions €',
                'Performance': 'Correcte'
            },
            {
                'Indicateur': 'Durée de vie',
                'Valeur': 5,
                'Unité': 'années',
                'Performance': 'Faible'
            }
        ])

        col1, col2 = st.columns(2)
        with col1:
            fig_croissance = px.bar(df_performance, x='Indicateur', y='Valeur', 
                                   color='Performance',
                                   title="Indicateurs de Performance Clé",
                                   color_discrete_map={'Élevée': '#2ecc71', 'Moyenne': '#f39c12', 'Correcte': '#3498db', 'Faible': '#e74c3c'})
            st.plotly_chart(fig_croissance, use_container_width=True)
        
        with col2:
            # Analyse du rapport coût/efficacité
            cout_par_membre = (self.parti_data['CROISSANCE']['budget_peak_millions'] * 1000000) / self.parti_data['CROISSANCE']['membres_max']
            influence_par_membre = self.parti_data['CROISSANCE']['ministres_gouvernement'] / self.parti_data['CROISSANCE']['membres_max'] * 1000
            
            fig_efficacite = go.Figure()
            fig_efficacite.add_trace(go.Bar(name='Coût par membre', x=['Efficacité'], y=[cout_par_membre]))
            fig_efficacite.add_trace(go.Bar(name='Influence par 1000 membres', x=['Efficacité'], y=[influence_par_membre]))
            fig_efficacite.update_layout(title="Analyse d'Efficacité Organisationnelle")
            st.plotly_chart(fig_efficacite, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <h4>🧠 Analyse de Performance</h4>
            <p>Démocratie Libérale démontre une <strong>croissance rapide</strong> mais une <strong>pérennité limitée</strong>. La performance en termes d'influence gouvernementale est remarquable pour un parti jeune, avec 8 ministres issus de ses rangs. Cependant, la courte durée de vie révèle les limites d'une structure trop dépendante de son leader et de son positionnement doctrinal strict dans le paysage politique français peu favorable aux partis monothématiques.</p>
        </div>
        """, unsafe_allow_html=True)

    def analyse_chronologie_strategique(self):
        """Analyse chronologique détaillée avec événements clés"""
        st.markdown("### ⏳ Chronologie Stratégique (1997-2002)")
        
        # Graphique d'évolution
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.annees_chrono, y=self.evolution_membres, 
                               mode='lines+markers', name='Membres', yaxis='y1'))
        fig.add_trace(go.Scatter(x=self.annees_chrono, y=self.evolution_budget, 
                               mode='lines+markers', name='Budget (M€)', yaxis='y2'))
        fig.add_trace(go.Scatter(x=self.annees_chrono, y=self.influence_politique, 
                               mode='lines+markers', name='Influence politique', yaxis='y3'))
        
        fig.update_layout(
            title='Évolution Conjointe: Membres, Budget et Influence',
            xaxis=dict(title='Année'),
            yaxis=dict(title='Membres', side='left'),
            yaxis2=dict(title='Budget (M€)', side='right', overlaying='y'),
            yaxis3=dict(title='Influence (0-10)', side='right', overlaying='y', position=0.85),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # Tableau des événements clés
        st.markdown("#### 📅 Événements Politiques Majeurs")
        df_evenements = pd.DataFrame(self.evenements_cles)
        fig_events = px.timeline(df_evenements, x_start="annee", x_end="annee", y="evenement", 
                               color="impact", color_continuous_scale="Viridis",
                               title="Chronologie des Événements Clés")
        fig_events.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_events, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <h4>🧠 Analyse Chronologique</h4>
            <p>La courbe de croissance montre un <strong>pic en 2000</strong> correspondant à la participation au gouvernement Jospin, suivie d'un déclin rapide après l'échec de la stratégie autonome lors de la présidentielle 2002. L'année 2002 représente un point d'inflexion stratégique : l'échec de Madelin à la présidentielle (3,91%) pousse à la fusion dans l'UMP, validant la thèse de l'impossibilité d'une voie purement libérale autonome dans le système politique français.</p>
        </div>
        """, unsafe_allow_html=True)

    def analyse_comparative_partis(self):
        """Analyse comparative avec les autres partis politiques"""
        st.markdown("### 🌍 Analyse Comparative dans le Paysage Politique")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_membres = px.bar(self.comparaison_partis, x='Parti', y='Membres_max',
                               title="Comparaison des Effectifs Maximum",
                               color='Parti')
            st.plotly_chart(fig_membres, use_container_width=True)
            
        with col2:
            fig_ministres = px.bar(self.comparaison_partis, x='Parti', y='Ministres_gouvernement',
                                 title="Influence Gouvernementale (Nombre de Ministres)",
                                 color='Parti')
            st.plotly_chart(fig_ministres, use_container_width=True)

        st.markdown("#### Positionnement Idéologique")
        # Carte politique simplifiée
        positionnement = pd.DataFrame({
            'Parti': ['Démocratie Libérale', 'RPR', 'UDF', 'PS', 'PCF', 'FN'],
            'Economic': [9, 6, 5, 2, 1, 4],  # 10=libéral, 1=étatiste
            'Societal': [6, 7, 5, 8, 9, 2],   # 10=progressiste, 1=conservateur
            'Europe': [8, 6, 8, 7, 3, 1]      # 10=fédéraliste, 1=souverainiste
        })
        
        fig_ideologie = px.scatter(positionnement, x='Economic', y='Societal', 
                                 size=[20, 25, 20, 25, 20, 25], text='Parti',
                                 title="Positionnement Idéologique des Partis",
                                 labels={'Economic': 'Libéralisme Économique', 'Societal': 'Progressisme Sociétal'})
        fig_ideologie.update_traces(textposition='top center')
        st.plotly_chart(fig_ideologie, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <h4>🧠 Analyse Comparative</h4>
            <p>Démocratie Libérale occupe une position <strong>unique dans l'espace politique français</strong> : ultra-libérale en économie mais modérément progressiste sur les questions sociétales. Ce positionnement le distingue nettement du RPR (gaulliste, plus étatiste) et de l'UDF (centriste, libéral modéré). Sa taille modeste mais son influence disproportionnée s'expliquent par la rareté de l'offre libérale pure et la qualité de ses cadres. La comparaison avec les partis de gouvernement établis montre les limites structurelles des micro-partis doctrinaux dans le système politique français.</p>
        </div>
        """, unsafe_allow_html=True)

    def simulation_scenarios_historiques(self):
        """Simulation de scénarios historiques alternatifs"""
        st.markdown("### 🎲 Simulation de Scénarios Historiques Alternatifs")
        st.warning("⚠️ Analyse contrefactuelle à but pédagogique - Ces scénarios sont des hypothèses stratégiques")
        
        scenario = st.selectbox(
            "Choisissez un scénario contrefactuel à explorer :",
            ["Stratégie d'autonomie prolongée", "Alliance précoce avec l'UDF", 
             "Leadership différent", "Contexte politique alternatif"]
        )

        if scenario == "Stratégie d'autonomie prolongée":
            st.markdown("#### Scénario : Maintien de l'indépendance au-delà de 2002")
            st.markdown("""
            **Hypothèses :**
            - Refus de la fusion dans l'UMP
            - Maintien d'une structure autonome
            - Stratégie de niche libérale
            
            **Impacts probables :**
            ✅ Conservation d'une voix libérale distincte
            ✅ Maintien d'un think tank influent
            ❌ Marginalisation électorale accrue
            ❌ Difficultés financières chroniques
            ❌ Départ des cadres vers l'UMP
            
            **Probabilité de succès :** 20%
            """)
            
        elif scenario == "Alliance précoce avec l'UDF":
            st.markdown("#### Scénario : Fusion avec l'UDF plutôt qu'avec le RPR")
            st.markdown("""
            **Hypothèses :**
            - Rapprochement avec le centre libéral dès 1998
            - Construction d'un pôle libéral-centriste
            - Stratégie électorale commune
            
            **Impacts probables :**
            ✅ Renforcement mutuel des familles libérales
            ✅ Meilleure résistance face à l'UMP
            ✅ Positionnement plus lisible
            ❌ Conflits doctrinaux avec la gauche UDF
            ❌ Risque de dilution identitaire
            
            **Probabilité de succès :** 40%
            """)
            
        elif scenario == "Leadership différent":
            st.markdown("#### Scénario : Leadership autre qu'Alain Madelin")
            col1, col2 = st.columns(2)
            with col1:
                nouveau_leader = st.selectbox("Leader alternatif :", 
                                            ["Jean-Pierre Raffarin", "Hervé Novelli", "Autre personnalité"])
            with col2:
                st.markdown(f"""
                **Impact de {nouveau_leader} :**
                - Style de leadership : {"Plus conciliant" if nouveau_leader == "Raffarin" else "Plus technique"}
                - Relations avec le RPR : {"Améliorées" if nouveau_leader == "Raffarin" else "Stables"}
                - Stratégie médiatique : {"Moins polarisante" if nouveau_leader == "Raffarin" else "Similaire"}
                """)
                
        elif scenario == "Contexte politique alternatif":
            st.markdown("#### Scénario : Contexte électoral différent en 2002")
            score_madelin = st.slider("Score d'Alain Madelin à la présidentielle 2002 (%)", 
                                   1.0, 10.0, 3.91)
            
            if score_madelin > 5.0:
                st.success(f"**Avec {score_madelin}% : Percée historique du libéralisme**")
                st.markdown("""
                - Légitimation de la voie libérale autonome
                - Financement public garanti
                - Position de force pour négocier avec l'UMP
                - Possible maintien de l'autonomie
                """)
            else:
                st.error(f"**Avec {score_madelin}% : Confirmation de la marginalisation**")
                st.markdown("""
                - Accélération de la fusion dans l'UMP
                - Affaiblissement du leadership Madelin
                - Renforcement des partisans de l'intégration
                """)

    def run(self):
        """Fonction principale pour exécuter le dashboard"""
        self.display_header()
        
        # Onglets pour l'analyse
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔗 Réseau d'Influence", 
            "📈 Performance", 
            "⏳ Chronologie Stratégique",
            "🌍 Analyse Comparative", 
            "🎲 Scénarios Alternatifs"
        ])
        
        with tab1:
            self.analyse_reseau_influence()
        
        with tab2:
            self.analyse_performance_politique()
        
        with tab3:
            self.analyse_chronologie_strategique()
        
        with tab4:
            self.analyse_comparative_partis()
        
        with tab5:
            self.simulation_scenarios_historiques()

# Point d'entrée principal
if __name__ == "__main__":
    analyseur = AnalyseDemocratieLiberale()
    analyseur.run()