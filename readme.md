# **Améliorer les soins en réanimation grâce à une solution innovante de suivi à distance des patients**

> à partir de 24/5/22 jusqu'à 10/5/2022

> Réaliser par : RHIBA Zakaria et TAKILI Youssef

> Encadré par : Pr El Hanine

## Introduction : 

La surveillance médicale des patients en réanimation est une tâche importante et essentielle pour les professionnels de la santé. Cependant, avec un nombre limité de lits et de moniteurs, il peut être difficile de surveiller tous les patients en temps réel. C'est pourquoi, dans le cadre de ce projet, nous avons développé une plateforme IoT pour le suivi à distance des signes vitaux des patients en réanimation en utilisant une smartwatch connectée à un microcontrôleur ESP8266. Cette plateforme permettra aux professionnels de la santé de surveiller les signes vitaux des patients en temps réel via une interface utilisateur conviviale, sans avoir à être constamment présents à côté du patient. En utilisant des capteurs tels que l'ECG, le SpO2 et la pression sanguine, nous pourrons collecter des données précises sur l'état du patient et les stocker dans une base de données PostgreSQL. Grâce à la mise en place de cette plateforme IoT, nous espérons améliorer la qualité des soins prodigués aux patients en réanimation tout en optimisant la gestion des ressources médicales.


## Problématique : 

La réanimation est une étape cruciale dans les soins de santé qui nécessite une surveillance constante des patients pour prévenir les complications et améliorer les chances de survie. Toutefois, le nombre limité de lits médicaux et de moniteurs disponibles dans les salles de réanimation peut entraîner un manque de suivi adéquat des patients, ce qui peut avoir des conséquences graves pour leur santé. Dans le cadre de nos stage de fin d'étude à l'hôpital CHU Ibn Rochd de Casablanca,nous avons entrepris de résoudre cette problématique en créant une plateforme IoT basée sur une smartwatch. Notre solution permet aux professionnels de la santé de surveiller les signes vitaux des patients à distance, réduisant ainsi la charge de travail des équipes soignantes et augmentant les chances de survie des patients. Nous avons utilisé des technologies innovantes pour concevoir une plateforme sécurisée et facile à utiliser, qui permet aux professionnels de la santé de surveiller les patients en temps réel et de recevoir des alertes en cas de changements dans leur état de santé. Notre solution offre également une meilleure qualité de vie aux patients, car elle leur permet d'être surveillés en temps réel sans avoir besoin d'être continuellement connectés à des moniteurs médicaux encombrants. Notre plateforme IoT est une solution innovante et efficace pour répondre aux besoins croissants de suivi médical en réanimation et améliorer la qualité des soins de santé.

## Solution : 

Notre solution de suivi à distance des signes vitaux des patients en réanimation est une avancée significative dans le domaine de la santé. En permettant aux professionnels de la santé de surveiller les signes vitaux des patients en temps réel, même lorsqu'ils ne sont pas constamment présents à côté du patient, notre solution permettra de réduire les risques d'erreurs médicales et d'améliorer la qualité des soins prodigués aux patients en réanimation. De plus, notre plateforme IoT est facile à utiliser et peut être intégrée dans n'importe quelle installation médicale existante, ce qui la rend accessible à un large éventail d'utilisateurs. Nous sommes convaincus que notre solution aura un impact positif sur les soins de santé et contribuera à améliorer la qualité de vie des patients.

## Objectifs : 

- Développer une plateforme IoT innovante et efficace pour surveiller à distance les signes vitaux des patients en réanimation.

- Concevoir un système de collecte de données précis et fiable à partir de capteurs portables tels qu'une smartwatch.

- Utiliser des technologies modernes telles que le microcontrôleur ESP8264, le protocole MQTT et le back-end Python pour créer une solution intégrée et rentable.

- Développer une interface utilisateur facile à utiliser pour permettre aux professionnels de la santé de surveiller les patients en temps réel et de recevoir des alertes en cas de changements dans leur état de santé.

- Assurer la sécurité des données des patients en utilisant des protocoles de cryptage robustes et une base de données sécurisée.
- Améliorer la qualité des soins de santé en offrant une surveillance non invasive et plus confortable pour les patients en réanimation.

- Optimiser les ressources de l'hôpital en permettant aux professionnels de la santé de surveiller plusieurs patients en même temps grâce à la solution IoT.

- Offrir une solution rentable pour la surveillance médicale en réanimation qui peut être utilisée dans des hôpitaux de différentes tailles et niveaux de ressources.

- Fournir une solution évolutive qui peut être mise à jour avec des fonctionnalités supplémentaires à l'avenir pour améliorer la surveillance des patients et les soins de santé.

## Prérequis : 

- Connaissance en électronique et en programmation pour utiliser le microcontrôleur ESP8264 et les capteurs nécessaires à la collecte des données des patients.

- Compréhension des protocoles de communication IoT tels que MQTT pour transmettre les données collectées à une plateforme centralisée.

- Compétences en développement web et mobile pour créer une interface utilisateur conviviale pour les professionnels de la santé.

- Connaissance de la gestion de bases de données pour stocker les données collectées de manière efficace et sécurisée.

- Compréhension de la sécurité des données en matière de conformité aux réglementations sur la protection des données personnelles et de la confidentialité des patients.

- Capacité à collaborer efficacement avec d'autres membres de l'équipe pour le développement et la mise en œuvre du projet.

- Connaissance des principes de la surveillance médicale en réanimation et de la manière dont les signes vitaux des patients sont surveillés.

- Compréhension de l'environnement hospitalier et des réglementations régissant l'utilisation de dispositifs médicaux.

## Plan de Travail : 

- Jour 1-2 : Recherche et sélection des capteurs appropriés pour collecter les signes vitaux des patients tels que l'ECG, le SpO2 et la pression sanguine.

- Jour 3-4 : Assemblage du circuit électronique avec le microcontrôleur ESP8266 pour connecter les capteurs et collecter les données.

- Jour 5-6 : Programmation du microcontrôleur pour configurer la connexion Wi-Fi et la transmission des données via le protocole MQTT.

- Jour 7-8 : Création d'une base de données PostgreSQL pour stocker les données collectées des capteurs.

- Jour 9-10 : Développement d'une application Flask pour créer une interface utilisateur pour les professionnels de la santé pour accéder aux données collectées des capteurs.

- Jour 11-12 : Configuration du back-end Python pour recevoir les données du microcontrôleur ESP8266 et les stocker dans la base de données PostgreSQL.

- Jour 13-14 : Intégration de l'application Flask avec la base de données PostgreSQL pour afficher les données collectées en temps réel pour les professionnels de la santé.

- Jour 15 : Tests et débogage de l'ensemble du système pour s'assurer que les données collectées des capteurs sont correctement affichées dans l'interface utilisateur et stockées dans la base de données. Réalisation de toutes les documentations nécessaires pour le projet.


## Conclusion : 

En conclusion, nous avons développé avec succès une plateforme IoT pour le suivi à distance des signes vitaux des patients en réanimation. Grâce à cette plateforme, les professionnels de la santé pourront surveiller les signes vitaux des patients en temps réel, même s'ils ne sont pas constamment présents à côté du patient. Nous avons utilisé des capteurs tels que l'ECG, le SpO2 et la pression sanguine pour collecter des données précises sur l'état du patient et les avons stockées dans une base de données PostgreSQL. La plateforme IoT que nous avons développée permettra aux professionnels de la santé d'accéder facilement aux données collectées, ce qui facilitera la prise de décision en matière de traitement médical. Ce projet nous a également permis d'acquérir une expérience précieuse dans le développement de systèmes IoT pour la santé. Nous espérons que cette plateforme IoT contribuera à améliorer la qualité des soins prodigués aux patients en réanimation et à optimiser la gestion des ressources médicales.