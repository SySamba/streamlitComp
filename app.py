import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator




# Application du CSS pour placer l'image à l'extrémité gauche
st.markdown(
    f"""
    <style>
        .title {{
            font-size: 24px;
            font-weight: bold;
            margin-left: 80px; /* Espacement entre l'image et le texte */
            
        }}
        body {{
            margin: 0;
            padding: 0;
        }}
        .footer {{
            text-align: center;
            padding: 30px;
            font-size: 20px;
            color: #888;
            font-weignht:bold;
            margin-bottom: 50px;
        }}
    </style>
    <div class="logo-container">
        <p class="title">Analyse Fret et Mouvement</p>
    </div>
    <br>
    <br>
    """ ,
    
    unsafe_allow_html=True
)

# Charger les données
try:
    # Lecture des fichiers Excel
    fret_data = pd.read_excel("Fret.xlsx")
    mouvement_data = pd.read_excel("Pax.xlsx")
    
    # Nettoyer les noms de colonnes
    fret_data.columns = fret_data.columns.str.strip()
    mouvement_data.columns = mouvement_data.columns.str.strip()
    
    # Supprimer les valeurs inutiles (0, 1, 2)
    fret_data = fret_data[fret_data['Fret'] > 0]
    mouvement_data = mouvement_data[mouvement_data['PAX'] > 0]
    
    # Affichage des datasets dans un conteneur stylisé
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Fret")
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(fret_data.style.format({'Fret': '{:.0f}', 'ANNEE': '{:.0f}'}), height=1020)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("Mvt")
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(mouvement_data.style.format({'PAX': '{:.0f}', 'ANNEE': '{:.0f}'}), height=1020)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Personnalisation des sliders
    start_year = st.slider("Sélectionner l'année de début", min_value=int(fret_data['ANNEE'].min()), 
                           max_value=int(fret_data['ANNEE'].max()), value=int(fret_data['ANNEE'].min()), key="start")
    end_year = st.slider("Sélectionner l'année de fin", min_value=start_year, max_value=int(fret_data['ANNEE'].max()), 
                         value=int(fret_data['ANNEE'].max()), key="end")

    # Afficher la plage des années sélectionnées
    st.markdown(f"<p style='font-size: 16px; color: #FF5722;'>Plage des années sélectionnées : {start_year} à {end_year}</p>", unsafe_allow_html=True)

    # Filtrer les données en fonction des années sélectionnées
    filtered_fret_data = fret_data[(fret_data['ANNEE'] >= start_year) & (fret_data['ANNEE'] <= end_year)]
    filtered_mouvement_data = mouvement_data[(mouvement_data['ANNEE'] >= start_year) & (mouvement_data['ANNEE'] <= end_year)]

    # Tracer les courbes Fret
    fig_fret, ax_fret = plt.subplots(figsize=(12, 7))
    ax_fret.plot(filtered_fret_data['ANNEE'], filtered_fret_data['Fret'], linestyle='-', linewidth=3, color='#1f77b4', label="Fret (en tonnes)")

    # Personnalisation du graphique Fret
    ax_fret.set_xticks(range(start_year, end_year + 1))
    ax_fret.set_xticklabels(range(start_year, end_year + 1), rotation=45, fontsize=12)
    ax_fret.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax_fret.set_title("Évolution du Fret en Tonnes", fontsize=16, fontweight='bold')
    ax_fret.set_xlabel("Année", fontsize=14)
    ax_fret.set_ylabel("Fret (en Tonnes)", fontsize=14)
    ax_fret.grid(True, linestyle='--', linewidth=0.7, alpha=0.6)
    ax_fret.legend(fontsize=12)
    
    st.pyplot(fig_fret)

    # Tracer les courbes Mouvement
    fig_mouvement, ax_mouvement = plt.subplots(figsize=(12, 7))
    ax_mouvement.plot(filtered_mouvement_data['ANNEE'], filtered_mouvement_data['PAX'], linestyle='-', linewidth=3, color='#ff7f0e', label="Mouvement (PAX)")

    # Personnalisation du graphique Mouvement
    ax_mouvement.set_xticks(range(start_year, end_year + 1))
    ax_mouvement.set_xticklabels(range(start_year, end_year + 1), rotation=45, fontsize=12)
    ax_mouvement.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax_mouvement.set_title("Évolution du Mouvement en PAX", fontsize=16, fontweight='bold')
    ax_mouvement.set_xlabel("Année", fontsize=14)
    ax_mouvement.set_ylabel("Mouvement (PAX)", fontsize=14)
    ax_mouvement.grid(True, linestyle='--', linewidth=0.7, alpha=0.6)
    ax_mouvement.legend(fontsize=12)
    
    st.pyplot(fig_mouvement)
    

    

      # Charger les fichiers Excel
    fret_data = pd.read_excel("FretMois.xlsx")
    mouvement_data = pd.read_excel("PaxMois.xlsx")

    # Convertir les noms de colonnes en chaînes et les nettoyer
    fret_data.columns = fret_data.columns.astype(str).str.strip()
    mouvement_data.columns = mouvement_data.columns.astype(str).str.strip()

    # Colonnes attendues
    expected_columns = ['Mois', '2019', '2020', '2021', '2022', '2023', '2024']

    # Vérifier les colonnes
    missing_columns_fret = [col for col in expected_columns if col not in fret_data.columns]
    missing_columns_mouvement = [col for col in expected_columns if col not in mouvement_data.columns]

    if missing_columns_fret:
        st.error(f"Le fichier 'FretMois.xlsx' est incomplet. Colonnes manquantes : {', '.join(missing_columns_fret)}")
    elif missing_columns_mouvement:
        st.error(f"Le fichier 'PaxMois.xlsx' est incomplet. Colonnes manquantes : {', '.join(missing_columns_mouvement)}")
    else:
        # Nettoyer les valeurs : supprimer les points et les virgules
        for df in [fret_data, mouvement_data]:
            numeric_columns = df.columns[1:]  # Exclure la colonne 'Mois'
            df[numeric_columns] = df[numeric_columns].replace({r'[.,]': ''}, regex=True)
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')  # Convertir en numérique

        # Afficher les datasets nettoyés
        st.subheader(" Fret Mensuel")
        st.dataframe(fret_data)
        st.subheader("Mvt Mensuel")
        st.dataframe(mouvement_data)
        # Charger les fichiers Excel
    fret_data = pd.read_excel("FretMois.xlsx")
    mouvement_data = pd.read_excel("PaxMois.xlsx")

    # Nettoyer les colonnes
    fret_data.columns = fret_data.columns.astype(str).str.strip()
    mouvement_data.columns = mouvement_data.columns.astype(str).str.strip()

    # Colonnes attendues
    expected_columns = ['Mois', '2019', '2020', '2021', '2022', '2023', '2024']

    # Vérifier les colonnes
    missing_columns_fret = [col for col in expected_columns if col not in fret_data.columns]
    missing_columns_mouvement = [col for col in expected_columns if col not in mouvement_data.columns]

    if missing_columns_fret:
        st.error(f"Le fichier 'FretMois.xlsx' est incomplet. Colonnes manquantes : {', '.join(missing_columns_fret)}")
    elif missing_columns_mouvement:
        st.error(f"Le fichier 'PaxMois.xlsx' est incomplet. Colonnes manquantes : {', '.join(missing_columns_mouvement)}")
    else:
        # Nettoyer les valeurs
        for df in [fret_data, mouvement_data]:
            numeric_columns = df.columns[1:]  # Exclure la colonne 'Mois'
            df[numeric_columns] = df[numeric_columns].replace({r'[.,]': ''}, regex=True)
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')  # Convertir en numérique

        # Sélectionner les années à analyser
        available_years = list(fret_data.columns[1:])  # Exclure la colonne 'Mois'
        selected_years = st.multiselect("Sélectionnez une ou plusieurs années", available_years, default=available_years)

        # Filtrer les données
        fret_filtered = fret_data[['Mois'] + selected_years]
        mouvement_filtered = mouvement_data[['Mois'] + selected_years]

        # Tracer les courbes pour chaque dataset
        fig_monthly_fret, ax_fret = plt.subplots(figsize=(12, 7))
        for year in selected_years:
            ax_fret.plot(fret_filtered['Mois'], fret_filtered[year], marker='o', label=f"Fret {year}")

        ax_fret.set_title("Évolution mensuelle du Fret", fontsize=16, fontweight='bold')
        ax_fret.set_xlabel("Mois", fontsize=14)
        ax_fret.set_ylabel("Fret (en tonnes)", fontsize=14)
        ax_fret.legend(fontsize=12)
        ax_fret.grid(True, linestyle='--', linewidth=0.7, alpha=0.6)
        st.pyplot(fig_monthly_fret)

        fig_monthly_mouvement, ax_mouvement = plt.subplots(figsize=(12, 7))
        for year in selected_years:
            ax_mouvement.plot(mouvement_filtered['Mois'], mouvement_filtered[year], marker='o', label=f"Mouvement {year}")

        ax_mouvement.set_title("Évolution mensuelle du Mouvement (PAX)", fontsize=16, fontweight='bold')
        ax_mouvement.set_xlabel("Mois", fontsize=14)
        ax_mouvement.set_ylabel("Mouvement (PAX)", fontsize=14)
        ax_mouvement.legend(fontsize=12)
        ax_mouvement.grid(True, linestyle='--', linewidth=0.7, alpha=0.6)
        st.pyplot(fig_monthly_mouvement)

        # Footer
        st.markdown('<div class="footer">© 2024 Agence Nationale de l\'Aviation Civile et de la Météorologie.</div>', unsafe_allow_html=True)

except FileNotFoundError:
    st.error("Les fichiers 'FretMois.xlsx' et 'PaxMois.xlsx' doivent être placés dans le même répertoire que 'app.py'.")
except KeyError as e:
    st.error(f"Erreur : La colonne {e} est manquante dans l'un des fichiers.")
                                                  

