# Analyseur de Sentiments des Tweets

## Objectifs du projet
Ce projet vise à développer une application web permettant d’analyser les sentiments des tweets en temps réel. Les principales fonctionnalités incluent :

- Utilisation de l’API Twitter pour récupérer des tweets en fonction de mots-clés ou de hashtags.
- Intégration d’un modèle d’analyse de sentiment open-source via Hugging Face.
- Affichage des tweets et de leur classification (positif, négatif, neutre) dans une interface utilisateur.
- Déploiement de l’application pour une utilisation en ligne.

## Fonctionnalités clés

- **Récupération des tweets** – Obtenir des tweets récents en fonction de mots-clés définis.
- **Analyse des sentiments** – Utiliser un modèle NLP de Hugging Face pour classifier les tweets.
- **Affichage interactif** – Présenter les tweets et leurs sentiments avec une interface utilisateur en React.
- **Filtrage et recherche** – Permettre aux utilisateurs de rechercher un ou plusieurs tweets sur un sujet spécifique.
  - *(En fonction du problème : si l’on ne peut récupérer qu’un tweet toutes les 15 minutes, uniquement un lien vers un tweet ; sinon, permettre la recherche de plusieurs tweets.)*
- **Déploiement en ligne** – Héberger l’application pour qu’elle soit accessible publiquement.

## Utilisation de Python
Plusieurs bibliothèques sont disponibles :  
[https://docs.x.com/x-api/tools-and-libraries/overview](https://docs.x.com/x-api/tools-and-libraries/overview)

## Problèmes potentiels
L’API gratuite impose certaines limitations :
- **1 requête toutes les 15 minutes par utilisateur**
- **Jusqu’à 100 posts récupérés et 500 écritures par mois**

[https://developer.x.com/en/portal/products](https://developer.x.com/en/portal/products)

