BEGIN TRANSACTION;
CREATE TABLE "accounts_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "role" varchar(30) NOT NULL, "phone" varchar(30) NOT NULL, "photo" varchar(100) NOT NULL, "email_verified" bool NOT NULL, "is_public" bool NOT NULL, "bio" text NOT NULL);
INSERT INTO "accounts_user" VALUES(1,'pbkdf2_sha256$1500000$BWikDkOUzZvZBXNefHnrrB$dzxLa1efkvzxTJOeAWnwZPWcfPnvLJlc5e8u99fkHxI=','2026-08-14 00:22:00.491849',1,'admin','','','admin@citedelamisericorde.local',1,1,'2026-08-13 09:38:10.348265','superadmin','','',0,0,'');
INSERT INTO "accounts_user" VALUES(2,'pbkdf2_sha256$1500000$SiBPrplQx0gKn9mtVxu3B9$1tfuDS+PmCpdu3pJZA+NuaPMqcNvvsp8Wweyclqyl1Q=','2026-08-14 00:35:15.575066',1,'YAGIRWA GEDEON','','','',1,1,'2026-08-13 11:03:49.575363','author','','',0,0,'');
CREATE TABLE "accounts_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "accounts_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "analytics_dailystats" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "date" date NOT NULL UNIQUE, "visits" integer unsigned NOT NULL CHECK ("visits" >= 0), "unique_visitors" integer unsigned NOT NULL CHECK ("unique_visitors" >= 0), "top_pages" text NOT NULL CHECK ((JSON_VALID("top_pages") OR "top_pages" IS NULL)));
CREATE TABLE "analytics_pageview" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "path" varchar(500) NOT NULL, "country" varchar(100) NOT NULL, "referrer" varchar(500) NOT NULL, "is_bot" bool NOT NULL);
CREATE TABLE "articles_article" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "slug" varchar(255) NOT NULL UNIQUE, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "title" varchar(300) NOT NULL, "excerpt" text NOT NULL, "content" text NOT NULL, "status" varchar(20) NOT NULL, "published_at" datetime NOT NULL, "is_featured" bool NOT NULL, "allow_comments" bool NOT NULL, "publication_authorized" bool NOT NULL, "meta_title" varchar(160) NOT NULL, "meta_description" varchar(300) NOT NULL, "canonical_url" varchar(200) NOT NULL, "views" bigint unsigned NOT NULL CHECK ("views" >= 0), "reading_time_minutes" smallint unsigned NOT NULL CHECK ("reading_time_minutes" >= 0), "author_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "cover_image_id" bigint NULL REFERENCES "media_mediaitem" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "articles_article" VALUES(1,'projet-de-lutte-contre-la-malnutrition-aux-enfants-de-moin-de-10ans-dans-le-territoire-de-nyiragongonyiragongo-lorganisation-cite-de-la-misericorde-lance-un-programme-de-lutte-contre-la-mal','2026-08-13 10:15:34.762788','2026-08-13 10:15:34.762852','Lutte contre la malnutrition des enfants de moins de 10 ans — Nyiragongo','','
<figure><img width="1024" height="576" src="/media/media/2026/08/wp/2026/08/img-20260506-wa02381970975820798064068.jpg" alt=""/></figure>



<figure><img width="576" height="1024" src="/media/media/2026/08/wp/2026/08/img-20260506-wa03412751445177144991600.jpg" alt=""/></figure>



<figure><img width="576" height="1024" src="/media/media/2026/08/wp/2026/08/img-20260506-wa03436060045968838187555.jpg" alt=""/></figure>



<figure><img width="576" height="1024" src="/media/media/2026/08/wp/2026/08/img-20260506-wa03445546494334624814394.jpg" alt=""/><figcaption>Uwimana,1.5 ans: orpheline: malnutrition aiguë modérée </figcaption></figure>



<figure><img width="576" height="1024" src="/media/media/2026/08/wp/2026/08/img-20260506-wa03403213233309520412375.jpg" alt=""/><figcaption>Uwase,3ans: malnutrition aiguë modérée avec affection cutanée </figcaption></figure>



<figure><img width="576" height="1024" src="/media/media/2026/08/wp/2026/08/img-20260506-wa03412751445177144991600.jpg" alt=""/><figcaption>Pascale,2 ans: malnutrition aiguë modérée </figcaption></figure>



<figure><img width="1024" height="576" src="/media/media/2026/08/wp/2026/08/img-20260506-wa02368322511235557893179.jpg" alt=""/></figure>



<figure><img width="1024" height="768" src="/media/media/2026/08/wp/2026/08/img-20260506-wa02016162214566291000200.jpg" alt=""/></figure>



<figure><img width="1024" height="768" src="/media/media/2026/08/wp/2026/08/img-20260506-wa0219633882165674383537.jpg" alt=""/></figure>



<figure><img width="1024" height="768" src="/media/media/2026/08/wp/2026/08/img-20260506-wa01951393631366409934374.jpg" alt=""/><figcaption>Photo de famille </figcaption></figure>



<figure><img width="1024" height="768" src="/media/media/2026/08/wp/2026/08/img-20260506-wa02028497312733879524573.jpg" alt=""/><figcaption>Enseignement sur l’allaitement maternel par Marie-Manassé ZIRHUMANA KAMOLE </figcaption></figure>



<p></p>



<figure></figure>



<p></p>



<figure><img width="1024" height="576" src="/media/media/2026/08/wp/2026/08/img-20260506-wa02155240100164919600901.jpg" alt=""/><figcaption>Des femmes cheffes de ménages qui accompagnaient leurs enfants au centre </figcaption></figure>



<figure><img width="576" height="1024" src="/media/media/2026/08/wp/2026/08/img-20260506-wa03465002223706886785688.jpg" alt=""/><figcaption>Rebecca : (orpheline,2ans) malnutrition aiguë sévère </figcaption></figure>



<p></p>
','published','2026-08-13 10:48:15.229333',1,0,0,'','','https://citedelamisericorde.wordpress.com/2026/05/07/projet-de-lutte-contre-la-malnutrition-aux-enfants-de-moin-de-10ans-dans-le-territoire-de-nyiragongonyiragongo-lorganisation-cite-de-la-misericorde-lance-un-programme-de-lutte-contre-la-mal/',2,1,1,NULL);
INSERT INTO "articles_article" VALUES(2,'projet-de-contribution-a-la-stabilisation-et-autonomisation-socioecinomique-des-survivants-des-violences-basees-sur-les-genres-en-republique-democratique-du-congo','2026-08-13 10:15:42.407342','2026-08-13 10:15:42.407402','PROJET DE CONTRIBUTION A LA STABILISATION ET AUTONOMISATION SOCIOECONOMIQUE DES SURVIVANTS DES VIOLENCES BASEES SUR LES GENRES EN REPUBLIQUE DEMOCRATIQUE DU CONGO',' Le projet socio-économique et autonomisation des survivants des VSBG et restauration de la paix, est né suite à l&#8217;évolution des dynamiques socioculturelles et sécuritaires vécues dans la zone. Les groupements MUMOSHO,KAMISIMBI et MUDUSA ciblés par le projet sont périphériques de la ville de Bukavu et tous victimes des diverses atrocités. Les populations qui y vivent [&hellip;] 
','
<figure><img width="1024" height="1004" src="/media/media/2026/08/wp/2026/08/screenshot_20250918-042110_allpdfreader8920617283398532784.jpg" alt=""/></figure>



<ol>
<li><strong>Intitulé du projet : </strong>Projet de contribution à la stabilisation et autonomisation socioéconomique des survivants des violences basées sur le genre dans le groupement de Kamisimbi, Mumosho et Mudusa en République Democratique du Congo</li>



<li><strong>Contexte et justification du projet </strong>:</li>
</ol>



<p>Le projet socio-économique et autonomisation des survivants des VSBG et restauration de la paix, est né suite à l’évolution des dynamiques socioculturelles et sécuritaires vécues dans la zone.</p>



<p>Les groupements MUMOSHO,KAMISIMBI et MUDUSA ciblés par le projet sont périphériques de la ville de Bukavu et tous victimes des diverses atrocités. Les populations qui y vivent sont pour la plupart des personnes vulnérables qui mènent une vie de pauvreté car pour la plupart, ce sont des ménages gardant les parcelles des propriétaires qui habitent en centre-ville. Avant la résurgence de la guerre du M23, ils parvenaient à trouver de quoi survivre et ce parce que les dessertes agricoles reliant la ville aux territoires approvisionnaient la ville en nourriture. Suite à la dégradation du contexte sécuritaire dans ces groupements(en raison des conflits armés récurrents entre les troupes loyalistes des FARDC, alliées au groupe armé Wazalendu, et les rebelles du M23), de nombreuses femmes ont été violées, d’autres n’ont pas survécu aux lésions suite au manque d’encadrement et des soins appropriés.</p>



<p>En effet, la présence réelle des survivants des VBG dans ces groupements cibles, dans l’aire de santé AS Mudusa, AS  Kamisimbi, As Mumosho</p>



<p>Ainsi, dans ce contexte, le projet vise à renforcer la stabilisation et l’autonomie des survivants des VBG et à promouvoir la paix au sein des communautés vivant dans ces zones de santé</p>



<p>Ainsi, les activités comprennent une prise en charge psycho sociale,un appui aux moyens de subsistance pour promouvoir l’indépendance socio-économique des survivants, des séances de dialogue communautaire organisées dans les lieux de culte ainsi que des formations  des leaders religieux et communautaires sur les différentes approches du projet dont le CCT, le CCTD, TM et à cela nous ajoutons également des formations aux métiers (Coupe-couture et Art Culinaire).</p>



<p>Au total, 500 personnes bénéficieront directement du projet durant les deux phases de l’année dont :</p>



<ul>
<li>100 femmes violées bénéficiaires des fonds de démarrage pour les activités génératrices des revenues et activités socio-économiques dont celles des métiers en deux phases</li>



<li>180 hommes, femmes dont jeunes étudiantes, parmi lesquels : 60 pour les Dialogues Communautaires selon les approches du projet (TM, CCTD), les activités de prévention VSBG</li>



<li>60 bénéficiaires des activités du processus CCT dans l’Église et la communauté,</li>



<li>120 couples recevront une formation sur les thématiques du projet telles que la MT, le Genre et l’inclusion et la Masculinité Positive, …</li>



<li>40 leaders religieux et communautaires pour des sessions de formation sur le CCT, la MT, le VSBG, le Genre et l’inclusion</li>
</ul>



<p>Environ 10 778 personnes bénéficieront indirectement du projet, y compris celles qui écouteront des programmes de sensibilisation à la radio et qui seront sensibilisées ou informées à travers les bénéficiaires directs des activités du projet.</p>



<h2><strong>Objectif global</strong></h2>



<ul>
<li>Apporter une prise en charge psycho sociale globale et de qualité des SVBG des Aires de santé MUDUSA,KAMISIMBI et MUMOSHO dont 55% des filles de 14 à 25 ans,20% des personnes vivants avec handicap,20% des personnes de 2e et 3e âge</li>
</ul>



<p> </p>



<h2><strong>Objectifs spécifiques</strong></h2>



<ul>
<li>Sensibiliser l’ensemble des Aires de santé à la question des violences basées sur les genres</li>



<li>Former 500 bénéficiaires sur la prise en charge des violences basées sur les genres et le dépistage</li>



<li>Ecouter et orienter particulièrement des volontaires victimes des VBG</li>



<li>Apporter une prise en charge médicale aux SVBG</li>



<li>Collaborer avec les 3 aires de santé</li>
</ul>



<p><strong>Résultats attendus</strong></p>



<ul>
<li>La prise en charge de coïnfections et des violences basées sur les genres (repérage, accueil, accompagnement médical et psychosocial, orientation, suivi des victimes)</li>



<li>Les situations de violences qui pourraient avoir lieu auprès de nos bénéficiaires sont identifiées et réglées autant que possible</li>



<li>Les patients reçus de nos 500 bénéficiaires trouvent une écoute active, un appui psychologique et médical des qualités et des propositions concrètes pour les aider à sortir de la situation des violences</li>
</ul>



<p><strong>Localisation du projet :</strong> le présent <strong>Projet de contribution à la stabilisation et autonomisation socioéconomique des survivants des violences basées sur le genre dans le groupement de Kamisimbi, Mumosho et Mudusa</strong> dans la  province du Sud-Kivu en République Démocratique du Congo pendant une durée de 12 mois à dater du jour de financement.</p>



<ol>
<li><strong>Nature et cadre juridique du projet :</strong> cette initiative est une action de développement à caractère socio-économique visant la redynamisation et la promotion de la femme défavorisée</li>



<li><strong>Pertinence du projet</strong></li>
</ol>



<p>Le présent projet contribue à la réponse en matière de prévention et de prise en charge des SVBG à travers une approche participative et multidimensionnelle centrée sur les survivantes.</p>



<p>Ce projet ciblera les femmes et les filles avec et sans handicap dans 3 aires de santé où la prévalence des VBG est particulièrement importante.</p>



<p>Les VBG sont très souvent cachées  et les victimes peines à demander de l’aide ;de ce fait les personnels de santé et en particulier ceux travaillant sur la santé sexuelle et reproductive(SSR) representent une porte d’entrée stratégique pour toucher ces femmes.</p>



<p>Il est donc primordial qque le personnel de santé soit formé à reconnaitre les differents types de violence,à prendre en charge les femmes et filles handicapés survivantes des violences et à pouvoir y apporter une réponse adéquate</p>



<p>Pour y parvenir, le projet appuiera durablement les acteurs de première ligne par un renforcement de capacité(formation, coaching, sensibilisation) et l’amélioration de la qualité et de la capacité de réponse des services de santé(dotation des intrants, appui au système de référencement</p>



<p>Ce projet s’attachera également à renforcer la résilience  des groupes vulnérables à travers des groupes de sensibilisation aux VBG,SSR(santé sexuelle et reproductive)</p>



<p>Strategies</p>



<p>Stratégies développées (Theory of change):<br/><br/> Le projet s’articule autour d’un ensemble d’activités complémentaires qui produiront des effets à court, moyen et long terme. Le renforcement des capacités des intervenants et l’amélioration de la capacité d’accueil des centres permettront une prise en charge accrue et de qualité des bénéficiaires. L’amélioration de l’articulation des différentes interventions (création de cadres de concertation inclusifs, référencement, etc.) conduira à une meilleure synergie d’action entre les acteurs intervenant sur le terrain. L’appui aux besoins de base, les sensibilisations et suivi des femmes et filles renforceront leur résilience et favoriseront une meilleure participation sociale de ces femmes à la vie communautaire. <br/><br/>Enfin, la participation des femmes et des filles à l’ensemble du processus de lutte contre les VBG permettra d’améliorer la pertinence, la qualité et l’efficacité de la réponse apportée dans la lutte contre les VBG<br/><br/> – Activités prévues: <br/><br/>R1 : Les acteurs de première ligne et les services sont appuyés et leurs capacités renforcées<br/><br/> · R1.1: Diagnostic participatif de la problématique des VBG et des structures de SSR dans les zones d’intervention du projet <br/><br/>Effectué en début de projet, ce diagnostic sera mené de façon participative par un consultant indépendant recruté à cet effet. Il permettra de dresser un état des lieux précis de la situation des VBG dans les zones d’intervention du projet (types de VBG, prévalence, nombre et types de bénéficiaires, etc.), de faire la cartographie des différents intervenants et structures de santé existantes dans les zones d’action, et d’analyser l’offre et les capacités de ces structures en matière de VBG et SSR, y compris en termes d’accès pour les personnes en situation de handicap. Les résultats de cette étude permettront d’affiner les actions à mettre en œuvre, de proposer un plan d’amélioration pour chaque centre de santé et ainsi de renforcer la pertinence et la qualité de la réponse à apporter dans les 20 aires de santé du projet.<br/><br/> · R1.2: Constructions et/ou réhabilitations de salles d’écoute<br/><br/> Dans chacune des 20 aires de santé, le projet contribuera à améliorer les capacités de prise en charge des structures sanitaires existantes par la réhabilitation ou la construction de salles d’écoute pour l’accueil des femmes et des filles dans une espace aménagé et sécurisé (“safe space”), accessible aux personnes handicapées. <br/><br/>Identifier avec les responsables des centres et les Associations de Santé Communautaire (ASACO), ces espaces pourront être utilisés à la fois pour la prise en charge psychosociale et le suivi des survivantes de VBG mais aussi pour des séances de sensibilisation sur les VBG et la SSR. <br/><br/>· A1.3: Renforcement des capacités des prestataires socio-sanitaires et communautaires sur les VBG et la SSR<br/><br/> Le projet renforcera les capacités des acteurs de première ligne grâce à des formations théoriques et pratiques organisées dans le respect des mesures barrières.<br/><br/> Les formateurs seront issus des services socio-sanitaires et de la promotion de la femme et de la famille du district ou du niveau national. <br/><br/>La formation VBG et SSR s’adressera à 12 agents des services du développement social et de la promotion de la femme (2 par structure), 40 prestataires de soins (2 par centre), et 30 élus locaux et 120 volontaires communautaires (6 par centre), soit un total de 202 personnes. Dans le cadre du suivi et de l’accompagnement qu’ils dispensent aux survivantes des VBG, ces acteurs seront également formés au soutien émotionnel de base, à l’écoute active et bienveillante, à la reconnaissance des signes de détresse psychosociale.<br/><br/> Une attention particulière sera également portée à l’accès des femmes et des adolescentes avec et sans handicap à la contraception et aux méthodes contraceptives de longue durée. <br/><br/>De plus, les capacités de 220 membres des ASACO seront renforcées en matière de leadership, gestion, mobilisation et management des ressources afin qu’ils puissent pleinement jouer leur rôle dans la gouvernance locale de la santé communautaire.<br/><br/> Au niveau communautaire, un réseau de points focaux sera mis en place pour conseiller et accompagner les enfants, adolescentes, femmes victimes de violences.<br/><br/> · R1.5: Supervisions formatives des prestataires de santé et des volontaires communautaires sur la prise en charge holistique des violences basées sur le genre <br/><br/>En complément des formations, des supervisions formatives seront organisées chaque trimestre pour permettre un accompagnement continu des acteurs de première ligne. <br/><br/>Des recommandations seront formulées après chaque mission et évaluées au cours des missions suivantes. <br/><br/>Ces missions seront planifiées en commun accord avec les différentes parties prenantes et les leçons apprises seront capitalisées en vue de garantir une meilleure intervention et la pérennisation des acquis au-delà du projet.<br/><br/> <br/><br/>R2 : La résilience socioéconomique des femmes et des filles à risque de VBG est renforcée à long terme. <br/><br/>A2.2: Appui aux femmes à risques ou survivantes regroupées en coopératives ou groupements d’intérêt économique <br/><br/>Le projet appuiera des coopératives de femmes et des groupements d’intérêt économique de femmes pour qu’ils produisent et assemblent des « kits de dignité ».<br/><br/> Essentiels au bien-être physique et psychologique des femmes et des filles, ces kits améliorent la mobilité des femmes et ils contribuent aussi à la protection des bénéficiaires.<br/><br/> En effet, la distribution de ces kits permet de faire passer des messages de prévention, d’aborder des sujets de SSR et VBG, et d’informer les femmes et filles à risque sur les services de protection existants. Le contenu des kits (serviettes hygiéniques, pagnes, etc.) sera défini avec les bénéficiaires et les distributions seront réalisées lors des séances de sensibilisation au sein des espaces sûrs (Centre cité de la Miséricorde) réhabilités par le projet. <br/><br/> <br/><br/> <br/><br/> <br/><br/> <br/><br/> <br/><br/> · A2.3: Organisation des séances de sensibilisation et de suivi à l’attention des femmes et des adolescentes                                                                                                                                                                                          Afin de renforcer la résilience des femmes et des filles à risque de VBG, des séances de sensibilisation seront organisées sur des thématiques telles que les VBG, la SSR, la gestion des conflits au sein des ménages, la protection des enfants ou encore l’autonomisation économique des femmes.                                   Pour faciliter la participation et les échanges dans un cadre sécurisé, les bénéficiaires seront regroupées en petits groupes (établis selon certains critères tels que l’âge, le statut matrimonial, le handicap).                                                                                                                                                                                                         Ces séances seront animées par les conseillers psychosociaux et les relais communautaires, préalablement formés et appuyés par les acteurs de santé et du développement social.                                                                                              Un manuel d’activités sera élaboré en début de projet et sera utilisé pour ces séances.                                                                                     R3 : La participation inclusive des femmes et des filles au niveau de la prise de décision, de la programmation et de la mise en œuvre des interventions est assurée et elles vivent dans un environnement protecteur où leurs besoins et leur voix sont pris en compte                                                                            · A3.1: Sensibilisation des intervenants de santé à l’inclusion                                                                             Pour favoriser la pertinence et l’efficience des réponses apportées aux VBG, il est crucial de sensibiliser les intervenants spécialisés à l’importance d’inclure les femmes et les filles dans tous les stades de gestion de la problématique, depuis l’identification des besoins à la mise en œuvre et au suivi des activités. Des séances de sensibilisation seront donc organisées à l’endroit des agents des services du développement social et de la promotion de la femme, des prestataires de soins, des élus locaux et des volontaires communautaires afin qu’ils puissent inclure et promouvoir la participation des femmes et filles, et des personnes en situation de handicap<br/><br/>Impact et durabilité : Ancré au sein des communautés qu’il appuie, ce projet vise un impact à long terme par le biais du renforcement durable des capacités des acteurs locaux (volontaires, prestataires de soin…), l’amélioration de la capacité d’accueil des structures de santé communautaire et de la qualité de la prise en charge des survivantes de VBG, et le renforcement de la résilience socioéconomique des bénéficiaires.                                                                                                       Le projet dispose également d’un ancrage institutionnel à travers le renforcement de capacités des élus locaux et la mise sur pied de cadres de concertations inclusifs qui regroupent les autorités déconcentrés, les acteurs de santé et les associations de femmes.                                                     Présidés par les autorités régionales, ces espaces d’échanges favoriseront la création de synergies, le développement d’actions complémentaires qui intègrent les besoins spécifiques des femmes et des filles survivantes de VBG, et l’inclusion de ces femmes à tous les niveaux de la gestion de la problématique des VBG. Cela permettra de garantir la pertinence, l’efficacité et la durabilité des actions au-delà du projet.    <br/> <br/>  8. Visibilité du</p>



<p>donateur                                                                                      – Proposition à formuler par l’organisation financier                                                                                          La visibilité du donateur sera assurée par l’affichage du logo sur l’ensemble des produits de communication (manuels, posters, panneaux…) et sur tous les documents du projet (rapports, rapport du diagnostic, etc.). De plus, la contribution du Bailleur sera mise en avant dans les produits vidéos et audios des sensibilisations, lors de la présentation du projet aux acteurs institutionnels et communautaires, et lors des réunions (cluster VBG…).<br/><br/>Méthodes de suivi (Capacité de gestion)                                                           Au niveau local, un suivi de proximité sera assuré par les équipes terrain déployées dans chaque région, supervisés par le Chef de projet. Les conseillers psychosociaux veilleront également à impliquer activement les acteurs et les bénéficiaires dans le suivi de l’action.                                                                                      De plus, un Comité de pilotage composé par les membres du projet, les acteurs institutionnels et communautaires se réunira une fois par an pour analyser la progression vers les résultats escomptés                                                                                                                                                                                                             Des revues de projet interservices seront également organisées sur une base trimestrielle pour garantir une meilleure visibilité de l’évolution du projet entre tous les départements.                                                                            Le suivi budgétaire sera assuré par le Chef de projet, appuyé par le département financier</p>



<figure><img width="1024" height="586" src="/media/media/2026/08/wp/2026/08/screenshot_20250918-042159_allpdfreader2292687892584294550.jpg" alt=""/></figure>



<figure><img width="837" height="1023" src="/media/media/2026/08/wp/2026/08/screenshot_20250918-042226_allpdfreader16602280780433668.jpg" alt=""/></figure>



<figure><img width="734" height="1024" src="/media/media/2026/08/wp/2026/08/screenshot_20250918-042328_allpdfreader6477029220414693507.jpg" alt=""/></figure>



<p>CALENDRIER DU PROJET</p>



<p>Etant à la recherche du partenaire financier,nous estimons que le calendrier soit proposé par lui dès que le financement sera disponible </p>
','published','2026-08-13 10:48:15.229333',0,0,0,'','','https://citedelamisericorde.wordpress.com/2025/09/13/projet-de-contribution-a-la-stabilisation-et-autonomisation-socioecinomique-des-survivants-des-violences-basees-sur-les-genres-en-republique-democratique-du-congo/',1,13,1,NULL);
INSERT INTO "articles_article" VALUES(3,'appel-au-don-sos-orphelinat','2026-08-13 10:16:13.784233','2026-08-13 10:16:13.784297','SAUVER L’ORPHELINAT PAR UN DON',' SENTEZ-VOUS SOUCIEUX DE RENDRE HEUREUX UN ORPHELIN??? Notre orphelinat Cité de la Miséricorde vit grâce aux dons des personnes de bonne volonté vivant au Canada,France,Belgique, Liban,île de la Reunion et Australie. Avec un souci d&#8217;obtenir un partenariat avec tant d&#8217;autres organisations internationales. Nous justifions les dons par des exhibitions des factures, bordereau de retrait ,Procès [&hellip;] 
','
<figure><img width="1024" height="460" src="/media/media/2026/08/wp/2026/08/img-20250916-wa01981898577822918181262.jpg" alt=""/></figure>



<figure><img width="461" height="1024" src="/media/media/2026/08/wp/2026/08/img-20250805-wa01627097002993674100660.jpg" alt=""/></figure>



<figure></figure>



<p>SENTEZ-VOUS SOUCIEUX DE RENDRE HEUREUX UN ORPHELIN???</p>



<p><br/>Notre orphelinat Cité de la Miséricorde vit grâce aux dons des personnes de bonne volonté vivant au Canada,France,Belgique, Liban,île de la Reunion et Australie.</p>



<figure><img width="1024" height="460" src="/media/media/2026/08/wp/2026/08/img-20250916-wa01995318309058408762202.jpg" alt=""/></figure>



<figure><img width="1024" height="576" src="/media/media/2026/08/wp/2026/08/20250607_1446455337410690804642272.jpg" alt=""/></figure>



<p>Avec un souci d’obtenir un partenariat avec tant d’autres organisations internationales. </p>



<figure><img width="509" height="675" src="/media/media/2026/08/wp/2026/08/screenshot_20250612-103913_allpdfreader5778086046821372944.jpg" alt=""/></figure>



<figure><img width="960" height="720" src="/media/media/2026/08/wp/2026/08/messenger_creation_88806711286366136601049797752379667.jpeg" alt=""/></figure>



<figure><img width="715" height="322" src="/media/media/2026/08/wp/2026/08/messenger_creation_a3a3c1b7-381c-495c-b89b-f7026dafa2777146830_0M0lMGW.jpeg" alt=""/></figure>



<p>Nous justifions les dons par des exhibitions des factures, bordereau de retrait ,Procès verbal des réunions, images et vidéos des activités réalisées</p>



<p><strong>CONSOMMATION MENSUELLE</strong>.</p>



<ul>
<li>NOURRITURE: 400$</li>



<li>HYGIENE: 50$</li>



<li>CENTRE MEDICAL: 150$</li>



<li>LOISIRS: 150$</li>
</ul>



<figure><img width="1024" height="460" src="/media/media/2026/08/wp/2026/08/img-20250916-wa01963484513572074990243.jpg" alt=""/></figure>



<figure><img width="1024" height="460" src="/media/media/2026/08/wp/2026/08/img-20250916-wa01956780040587762343153.jpg" alt=""/></figure>



<p> <br/>L’orphelinat dispose tant des besoins répartis selon des départements suivants :</p>



<ul>
<li>Centre Medical</li>



<li>Alimentation</li>



<li>Hygiène</li>



<li>Loisirs </li>



<li>Construction </li>



<li>Payement des agents <br/>Nous recevons toute pièce, tout don car c’est ne pas la main qui donne mais c’est le cœur.<br/>Chaque fin du mois nous achetons un stock de nourriture consommable durant un mois.<br/>Nous recevons des dons via western union, Ria, Moneygram et portefeuille mobile airtel.</li>



<li><strong>Coordonnées :</strong> Prenom : MARIE MANASSE<em>/ </em>Nom: ZIRHUMANA KAMOLE/ Pays: République Démocratique du Congo/ Téléphone : +243985854422</li>



<li>Merci à tous les donateurs qui grâce à eux ces enfants respirent encore et retrouvent du jour au jour la joie de vivre</li>



<li>
<ul>
<li><strong>TÉMOIGNAGE</strong>S </li>
</ul>
</li>
</ul>



<p><strong>Distribution des souliers et habits aux 65 enfants démunis venant des familles déplacées des guerres dans le camp de Lushagala </strong></p>



<p><strong>A cette même occasion la Cité de la Miséricorde a remis 10 tank d’eau aux 10 ménages en vue de lutter contre les pathologies hydriques. </strong></p>



<p>Signalons que cette œuvre s’est déroulé en Janvier 2024 à 15 kilomètres de la ville de Goma par l’aide de Daniella,nationalité belge.</p>



<figure></figure>



<figure><figcaption>Mot du chef de camp</figcaption></figure>



<figure><figcaption>Remerciements </figcaption></figure>



<p>A cette même occasion les 50 enfants hébergés à l’orphélinat de la Cité de la Miséricorde n’ont pas été oublié pour les souliers </p>



<figure></figure>



<p><strong>2. RÉCEPTION DES TENUES DE SPORT ET FOOTBALL </strong></p>



<p>L’orphélinat Cité de la Miséricorde a recu en Novembre 2024 un don de 2 nouvelles vareuses de sport et 5 ballons en vue de promouvoir le Loisir au milieu de ces enfants. </p>



<figure></figure>



<p>Signalons que ce don a été remis par Madame Claudia de la nationalité Australienne.</p>



<figure><img width="960" height="540" src="/media/media/2026/08/wp/2026/08/17459985047933610022980594444200.jpg" alt=""/></figure>



<figure><img width="1024" height="461" src="/media/media/2026/08/wp/2026/08/1745998514337340925539926636663.jpg" alt=""/></figure>



<figure><img width="768" height="1024" src="/media/media/2026/08/wp/2026/08/1742845457350571329581381628336.jpg" alt=""/></figure>



<figure><img width="1024" height="576" src="/media/media/2026/08/wp/2026/08/17428454848146172090732852265988.jpg" alt=""/><figcaption>Des moments de joie après réception de la tenue de sport</figcaption></figure>



<p>ACTIVITÉS DE DISTRIBUTION DES FOURNITURES SCOLAIRES AUX ORPHELINS </p>



<p>Ce samedi 30 Août 2025 est prévu une grande journée de distribution des objets classiques :</p>



<ul>
<li>Latte</li>



<li>Gomme</li>



<li>Stylos </li>



<li>Cahiers</li>



<li>Cartables</li>



<li>Crayons</li>
</ul>



<p>Le coût global de cette activité s’élève à 300 Dollars américains </p>



<p>Mise à part, la tenue uniforme va nous coûter 200$ US.</p>



<figure><img width="620" height="877" src="/media/media/2026/08/wp/2026/08/17558486773284954862579276484696.jpg" alt=""/><figcaption>Coût global des fournitures scolaires moins la tenue uniforme </figcaption></figure>



<p>Le total général s’élève à 500$ US.</p>



<p>Merci pour tous les donateurs qui continuent de nous soutenir.</p>



<p></p>



<p><strong>JOURNEE DE DISTRIBUTION DES FOURNITURES SCOLAIRES AUX ORPHELINS</strong></p>



<figure><img width="960" height="540" src="/media/media/2026/08/wp/2026/08/img-20250830-wa00422053147038746002351.jpg" alt=""/></figure>



<figure><img width="1024" height="768" src="/media/media/2026/08/wp/2026/08/img_20250104_1305463341567229702749640.jpg" alt=""/></figure>



<figure><img width="1024" height="460" src="/media/media/2026/08/wp/2026/08/img-20250830-wa00531461900489581247822.jpg" alt=""/></figure>



<figure><img width="1024" height="460" src="/media/media/2026/08/wp/2026/08/img-20250910-wa03073254836903788807763.jpg" alt=""/></figure>



<figure><img width="1024" height="768" src="/media/media/2026/08/wp/2026/08/img-20250910-wa03081213545354360873965.jpg" alt=""/></figure>



<figure><img width="1024" height="460" src="/media/media/2026/08/wp/2026/08/img-20250830-wa00563139045169594564033.jpg" alt=""/></figure>



<p></p>



<p>NOS SINCERES REMERCIEMENTS A TOUS LES DONATEURS</p>



<figure></figure>



<figure></figure>



<figure></figure>



<p></p>



<p><strong>VOTRE DON CONTRIBUE A LA DURABILITÉ DE NOTRE ORPHELINAT CAR CELUI-CI EN DEPEND</strong></p>
','published','2026-08-13 10:48:15.229333',0,0,0,'','','https://citedelamisericorde.wordpress.com/2025/07/03/appel-au-don-sos-orphelinat/',1,3,1,NULL);
INSERT INTO "articles_article" VALUES(4,'amenagement-cuisine-orphelinat','2026-08-13 10:16:29.279963','2026-08-13 10:16:29.280001','AMENAGEMENT CUISINE ORPHELINAT',' Il y a quelques années, l&#8217;orphelinat Cité de la Miséricorde utilise le dehors comme cuisine près du dortoire des garçons. Faute de fonds suffisants, cette cuisine n’a jusqu’à présent jamais été reconstruite à l&#8217;endroit favorable. Après un temps, le conseil d&#8217;administration a remarqué certains defis liés à l&#8217;emplacement de cette cuisine: 1. Destabilisation pendant la [&hellip;] 
','
<p>Il y a quelques années, l’orphelinat Cité de la Miséricorde utilise le dehors comme cuisine près du dortoire des garçons. </p>



<figure><img width="540" height="960" src="/media/media/2026/08/wp/2026/08/img-20250523-wa0141222926321828171613.jpg" alt=""/></figure>



<p>Faute de fonds suffisants, cette cuisine n’a jusqu’à présent jamais été reconstruite à l’endroit favorable.</p>



<p><br/>Après un temps, le conseil d’administration a remarqué certains defis liés à l’emplacement de cette cuisine:</p>



<figure><img width="960" height="540" src="/media/media/2026/08/wp/2026/08/17486510645782090586428310662383.jpg" alt=""/></figure>



<figure><img width="715" height="536" src="/media/media/2026/08/wp/2026/08/17486510048671244758245769843434.jpg" alt=""/></figure>



<p>1. Destabilisation pendant la période pluvieuse qui nous oblige d’utiliser une partie du dortoir garçon. </p>



<p>2. Présence des affections pulmonaires chez les enfants liées à la Présence de la fumée</p>



<p>3. Haut risque de brulure chez les enfants mal intentionnés</p>



<p>4. Dégradation du mur de ce dortoir et celle de la peinture<br/></p>



<p>Pour ce faire,l’orphelinat souhaite construire une cuisinière moderne en materiaux durables.</p>



<figure><img width="739" height="415" src="/media/media/2026/08/wp/2026/08/images-144084199170270482493.jpg" alt=""/><figcaption>Modèle cuisine</figcaption></figure>



<p>Le budget total de ce travail est de 475$ et grâce aux généreux donateurs l’orphélinat dispose déjà de 229 dollars americains.</p>



<figure><img width="1024" height="461" src="/media/media/2026/08/wp/2026/08/17486509867461484831157422268935.jpg" alt=""/></figure>



<p>Mode de transfert:</p>



<ul>
<li>Virement sur le RIB de Orphélinat</li>



<li>Moneygram </li>



<li>Western union</li>



<li>Ria</li>
</ul>



<figure><img width="720" height="1010" src="/media/media/2026/08/wp/2026/08/17486509447393762670018825719022.jpg" alt=""/></figure>



<p>Autres contacts:</p>



<p>Whatsapp: +243970884579</p>



<p>Email: citedelamisericorde@gmail.com</p>



<figure><img width="1024" height="576" src="/media/media/2026/08/wp/2026/08/20250607_1507176236056726197115682.jpg" alt=""/></figure>



<figure><img width="1024" height="576" src="/media/media/2026/08/wp/2026/08/20250607_1511337610400258125782750.jpg" alt=""/></figure>



<figure><img width="1024" height="576" src="/media/media/2026/08/wp/2026/08/20250607_151836796568189709966243.jpg" alt=""/></figure>
','published','2026-08-13 10:48:15.229333',0,0,0,'','','https://citedelamisericorde.wordpress.com/2025/05/31/amenagement-cuisine-orphelinat/',1,1,1,NULL);
INSERT INTO "articles_article" VALUES(5,'projet-dimplantation-dune-ferme-agro-ecologique-projet-execute-par-lassociation-collectif-des-jeunes-pour-la-paix-et-le-developpement-cjpd-congo-asbl','2026-08-13 10:16:49.459382','2026-08-14 14:58:22.506372','PROJET D’IMPLANTATION D’UNE FERME AGRO-ÉCOLOGIQUE- Projet Exécuté par L’Association Cité de la Miséricorde',' Initié en 2024 par: Manassé Kamole,coordonateur du CJPD et fondateur de la Cité de la Miséricorde Durée: Décembre 2024-Novembre 2025 L’agroécologie couvre de nombreux aspects de l’agriculture et intègre les dimensions à la fois écologiques, économiques et sociales.Ces 3 grands piliers en font une discipline complète, jouant sur l’interaction entre l’écosystème et l’homme, cherchant à [&hellip;] 
','
<p>Initié en 2024 par: <em>Manassé Kamole,coordonateur de la Cité de la Miséricorde et fondateur de la Cité de </em>la Miséricorde</p>



<p>Durée: Décembre 2024-Novembre 2025</p>



<figure><img width="735" height="1023" src="/media/media/2026/08/wp/2026/08/screenshot_20250528-024125_allpdfreader3833799926878037949.jpg" alt=""/></figure>



<p>L’agroécologie couvre de nombreux aspects de l’agriculture et intègre les dimensions à la fois écologiques, économiques et sociales.Ces 3 grands piliers en font une discipline complète, jouant sur l’interaction entre l’écosystème et l’homme, cherchant à préserver l’environnement et la biodiversité tout en assurant la productivité agricole et en maximisant les fonctionnalités offertes par les écosystèmes.</p>



<figure><img width="730" height="1023" src="/media/media/2026/08/wp/2026/08/screenshot_20250528-024150_allpdfreader4829083458068890546.jpg" alt=""/></figure>



<p><br/>Le projet d’implantationd’unefermeagro-écologique à vocation pédagogique , situé à Kamisimbi-Sud Kivu, en RD Congo a pour but de développer les filières agricoles de Mukama,Bukera,Bushigi,Bukalwa localités situées dans le groupement de Kamisimbi à 24 kilomètres de la ville de Bukavu, pour assurer la sécurité alimentaire.</p>



<figure><img width="727" height="1023" src="/media/media/2026/08/wp/2026/08/screenshot_20250528-024222_allpdfreader7600737550913901488.jpg" alt=""/></figure>



<p>Ce projet s’inscrit dans une démarche agroécologique afin d’augmenter la productivité des exploitations de manière durable, en maximisant les interactions écologiques et en limitant l’investissement nécessaire.<br/><br/>Trois des techniques agroécologiques testées par le projet sont présentées dans cet article pour illustrer les trois fondements (respect de l’environnement, rentabilité économique, développement social) de la discipline.</p>



<p><br/><br/>Le respect de l’environnement – lutte contre les adventices sans herbicide<br/>L’agroécologie prône une moindre utilisation des intrants chimiques, ainsi, l’apprentissage des différentes techniques agroécologiques dans la culture des produits maraichers,les protéger de l’érosion grâce au drainage et lutter contre les adventices sans avoir besoin d’utiliser des herbicides. Certaines plantes sont également des ennemis de ravageurs et peuvent servir pour lutter écologiquement contre les insectes.</p>



<p><br/><br/>Dans ce cadre, le projet d’implantationd’unefermeagro-écologique a construit à Kamisimbi un hangar de 12m/6m en vue de:</p>



<figure><img width="960" height="540" src="/media/media/2026/08/wp/2026/08/img-20250512-wa01118383869258837182857.jpg" alt=""/></figure>



<figure><img width="960" height="540" src="/media/media/2026/08/wp/2026/08/img-20250512-wa01136174425786015489728.jpg" alt=""/></figure>



<figure><img width="1024" height="767" src="/media/media/2026/08/wp/2026/08/img-20250526-wa00172200971259058324818.jpg" alt=""/></figure>



<figure><img width="960" height="540" src="/media/media/2026/08/wp/2026/08/img-20250526-wa00105837685643869570860.jpg" alt=""/></figure>



<figure><img width="540" height="960" src="/media/media/2026/08/wp/2026/08/17474142968685918074515064676847.jpg" alt=""/></figure>



<ul>
<li>Faciliter les enseignements</li>



<li>Aider au deroulement des differentes activités du projet</li>



<li>Stocker les outils aratoires</li>



<li>Mutuelle de solidarité</li>



<li>Coopérative agricole</li>
</ul>



<p>Un champ école de 1 hectare qui a reçu 200 bénéficiaires dont 100 femmes de ménage,60 hommes et 40 jeunes tous bénéficiaires venant des localités ciblés par le projet</p>



<p></p>



<p><br/><br/>Au Sud-Kivu, la plantation des produits maraichers a permis de lutter efficacement contre la pauvreté et la malnutrition.Imperata cylindrica et autres herbacées adventices.</p>



<figure><img width="731" height="1024" src="/media/media/2026/08/wp/2026/08/screenshot_20250528-015417_allpdfreader6755130329156372865.jpg" alt=""/></figure>



<p><strong>Une économie performante </strong><br/>L’agroécologie n’a d’intérêt pour les agriculteurs que s’ils s’y retrouvent financièrement. Pour cela, il faut que les rendements parfois moindres et les besoins en main d’œuvre quelques fois plus importants qu’en agriculture conventionnelle soient compensés.<br/><br/>Les produits chimiques de synthèse comme les herbicides, pesticides, antifongiques et engrais coûtent chers. Ils sont ainsi inaccessibles pour bon nombre de paysans.</p>



<figure></figure>



<p>L’alternative proposée par l’agroécologie avec des plantes susceptibles de remplacer ces intrants permettra aux bénéficiaires de réduire les besoins en investissements financiers.</p>



<figure></figure>



<p>Mais l’agroécologie permet aussi de mieux s’insérer sur le marché en produisant de manière régulière à l’abri des aléas climatiques et à des périodes où les prix des produits agricoles sont favorables,ce qui fait l’utilité du hangar. C’est le cas des pépinières sur table, ou pépinière sur pilotis, que met en place notre projet.</p>



<figure></figure>



<p>Après la formation théorique,les bénéficiaires du projet de création d’une ferme agro-écologique ont fait pendant 2 mois une formation pratique au champ d’éxperience avec les éléments suivants:</p>



<ul>
<li>Amenagement des plates bandes </li>



<li>Entretien du drainage </li>



<li>Labour</li>



<li>Repiquage</li>



<li>Identification des maladies des plantes </li>



<li>Soins phytoterapeutique</li>
</ul>



<figure><img width="1024" height="767" src="/media/media/2026/08/wp/2026/08/img-20250602-wa00721404359030771124198.jpg" alt=""/></figure>



<figure><img width="960" height="540" src="/media/media/2026/08/wp/2026/08/img-20250602-wa00746434878816712837539.jpg" alt=""/></figure>



<figure><img width="960" height="540" src="/media/media/2026/08/wp/2026/08/img-20250602-wa00762706476337958274775.jpg" alt=""/></figure>



<p><strong>PARTIE PRATIQUE DU PROJET</strong></p>



<p>A l’issue des activités des activités d’enseignement sur les pratiques agroécologiques, 200 bénéficiaires ont assimilé cette phase et ceci s’est découvert au champ d’expérience où différentes activités ont eu lieu entre autre:</p>



<ul>
<li>Drainage </li>



<li>Culture des différentes semences : choux,oignons, amarante,obergines,carottes, poireaux </li>



<li>Sarclage</li>



<li>Repiquage </li>



<li>Triage</li>
</ul>



<p>A la fin du mois de Juin débuteront les activités de descente sur terrain dans les champs particuliers des bénéficiaires </p>
','published','2026-08-13 10:48:15.229333',0,0,0,'','','https://citedelamisericorde.wordpress.com/2025/05/28/projet-dimplantation-dune-ferme-agro-ecologique-projet-execute-par-lassociation-collectif-des-jeunes-pour-la-paix-et-le-developpement-cjpd-congo-asbl/',1,4,1,NULL);
INSERT INTO "articles_article" VALUES(6,'une-bonne-journee-sannonce','2026-08-13 10:17:05.421378','2026-08-13 10:17:05.421420','UNE BONNE JOURNÉE S’ANNONCE.',' Par la grâce du Seigneur nous avons vu aujourd&#8217;hui 09 Mai 2026 un nouveau jour. Un jour de paix plein de douceur. Après nous avoir lavé et rincer les dents,nous avons reçu de notre chère cuisine un très bon plat de bouillie composé de farine de maïs,soja et sorgho. Une bouillie très qualifié en matière [&hellip;] 
','
<p>Par la grâce du Seigneur nous avons vu aujourd’hui 09 Mai 2026 un nouveau jour.</p>



<p>Un jour de paix plein de douceur.</p>



<p>Après nous avoir lavé et rincer les dents,nous avons reçu de notre chère cuisine un très bon plat de bouillie composé de farine de maïs,soja et sorgho. Une bouillie très qualifié en matière nutritionnelle.</p>



<figure><img width="1024" height="767" src="/media/media/2026/08/wp/2026/08/img-20250523-wa01454190386095213270707.jpg" alt=""/></figure>



<figure><img width="1024" height="767" src="/media/media/2026/08/wp/2026/08/img-20250523-wa01503776728102908662145.jpg" alt=""/></figure>



<figure><img width="1024" height="767" src="/media/media/2026/08/wp/2026/08/img-20250523-wa01554808910707710625529.jpg" alt=""/></figure>



<p><strong>Nos remerciements :</strong></p>



<p>A tous les donateurs et donatrices:</p>



<ul>
<li>Au canada</li>



<li>En France</li>



<li>En Belgique</li>



<li>Au Liban</li>



<li>En Australie</li>
</ul>



<p>Trouvez ici nos sentiments de gratitude</p>



<figure></figure>



<figure></figure>



<figure></figure>



<p>Soyez richement bénis chers bienfaiteurs. </p>



<p>Vos soutiens nous apportent la joie et le gout de vivre.</p>



<figure><img width="1024" height="460" src="/media/media/2026/08/wp/2026/08/messenger_creation_9cfbf2af-2a94-485a-8684-74605e63c62d1104606_2kGtRvc.jpeg" alt=""/></figure>



<figure><img width="461" height="1024" src="/media/media/2026/08/wp/2026/08/messenger_creation_7e982e81-cc97-4caa-9ba9-1033af4e961d8576736_JK2baU8.jpeg" alt=""/></figure>



<figure><img width="960" height="540" src="/media/media/2026/08/wp/2026/08/img-20250805-wa01579084261201756904707.jpg" alt=""/></figure>



<figure><img width="1024" height="460" src="/media/media/2026/08/wp/2026/08/img-20250805-wa01515668812181185078001.jpg" alt=""/></figure>



<figure><img width="1024" height="460" src="/media/media/2026/08/wp/2026/08/img-20250805-wa01543281009616049951436.jpg" alt=""/></figure>



<p>Les enfants sont toujours heureux d’avoir connu certaines personnes comme:</p>



<ol>
<li>Piercel : canada</li>



<li>Sylvio: canada</li>



<li>Marie-Pierre : canada</li>



<li>Rodrigue: canada</li>



<li>Mado: canada</li>



<li>Gary : canada</li>



<li>Sylvie: canada</li>



<li>Gps disraeli: canada</li>



<li>Jacquastri: Canada</li>



<li>Berangere : canada</li>



<li>Suzy: Canada</li>



<li>Cathy: Canada</li>



<li>Guilene: Canada</li>



<li>Sophie: Liban</li>



<li>Brigitte: Liban</li>



<li>Stephanie: Liban</li>



<li>Jean-François: France</li>



<li>Antonio: France</li>



<li>Marie-Paule: France</li>



<li>Daniella: Belgique</li>



<li>Tantine: Australie</li>
</ol>



<p><strong>BESOIN DES FOURNITURES SCOLAIRES</strong></p>



<p><strong>A l’occasion de la rentrée scolaire de ce 2 Septembre 2025,l’orphélinat Cité de la Miséricorde lance un appel à toutes les personnes de bonne volonté qui peuvent nous aider à garantir des objects classiques aux 50 orphelins encadrés et hebergés par le centre.</strong></p>



<p>Les objects à distribuer sont:</p>



<ol>
<li>Cahiers</li>



<li>Lattes</li>



<li>Stylos</li>



<li>Ardoises</li>



<li>Cartables</li>



<li>Gomme</li>



<li>Crayons</li>
</ol>



<figure><img width="733" height="1024" src="/media/media/2026/08/wp/2026/08/screenshot_20250806-180054_gallery2997741796954331103.jpg" alt=""/></figure>



<p>Que Dieu benisses toutes ces personnes qui ne cessent de penser à nous.</p>
','published','2026-08-13 10:48:15.229333',0,0,0,'','','https://citedelamisericorde.wordpress.com/2025/05/24/une-bonne-journee-sannonce/',1,2,1,NULL);
INSERT INTO "articles_article" VALUES(7,'projet-de-creation-dun-aire-des-jeux','2026-08-13 10:17:09.055166','2026-08-13 10:17:09.055202','PROJET DE CRÉATION D’UN AIRE DES JEUX',' L’aire des jeux joue un rôle essentiel dans le développement des enfants, offrant un espace unique où ils peuvent s’épanouir physiquement, socialement et émotionnellement. Cet environnement extérieur, sera équipé des structures variées, en stimulant non seulement leur motricité, mais favorisera également l’interaction sociale et la créativité.En engageant les enfants dans des activités ludiques, les aires de jeux sont autant de terrains d’apprentissage [&hellip;] 
','
<p>L’aire des jeux joue un rôle essentiel dans le développement des enfants, offrant un espace unique où ils peuvent s’épanouir physiquement, socialement et émotionnellement.</p>



<p><brCet environnement extérieur, sera équipé des structures variées, en stimulant non seulement leur motricité, mais favorisera également l’interaction sociale et la créativité.<brEn engageant les enfants dans des activités ludiques, les aires de jeux sont autant de terrains d’apprentissage précieux qui contribuent à leur bien-être global et à leur épanouissement.<brLe terrain de jeux constitue un espace essentiel pour le développement physique, social et émotionnel des enfants.<brÀ travers divers jeux et activités en plein air, ce terrain permettra aux jeunes de s’épanouir et d’apprendre, tout en s’amusant.</p>



<figure><img width="1024" height="768" src="/media/media/2026/08/wp/2026/08/img-20250516-wa0082492460727698598290.jpg" alt=""/></figure>



<p>Cet espace dédié aux jeux est le pivot de l’aire de jeux pour les enfants encadrés au sein de la Cité de la Miséricorde.<brLes équipements de jeux seront de plus en plus stimulants pour encourager les enfants à ne pas rester enfermer à la maison à ne rien faire.<brces équipements de jeux seront classés de la façon suivante : <brjeux multifonctions : combinaisons modulaires de différentes plateformes et d’éléments ludiques tels que passerelles, filets, murs d’escalade<brjeux classiques : balançoires, petites maisons<brjeux dynamiques : ils permettent des mouvements d’oscillation, de translation ou de gestion de l’équilibre, du vide ou de la vitesse<brjeux thématiques : ce sont des jeux reproduisant des décors fabuleux, conçus pour les enfants de 2 à 8 ans, qui transforment chaque terrain de jeu en théâtre à ciel ouvert.</p>



<p><brjeux éducatifs : ils augmentent les capacités cognitives et sensorielles des enfants et incluent une variété d’éléments interactifs, des bacs à sable ou jouer par terre<brjeux d’équilibre et d’escalade : ils comprennent divers éléments qui testent l’agilité, l’équilibre et la capacité de concentration et de coordination des mouvements.<brVos contributions nous permettront à y arriver :<brPour tout soutien financier,Merci de nous contacter pour recevoir nos coordonnées de transfert</p>



<figure><img width="1024" height="768" src="/media/media/2026/08/wp/2026/08/img-20250516-wa0081261469961774322770.jpg" alt=""/></figure>
','published','2026-08-13 10:48:15.229333',0,0,0,'','','https://citedelamisericorde.wordpress.com/2025/05/19/projet-de-creation-dun-aire-des-jeux/',1,2,1,NULL);
INSERT INTO "articles_article" VALUES(8,'projet-de-la-creation-dun-centre-de-formation-professionnel-en-faveur-des-orphelins-de-lorphelinat-cite-de-la-misericorde-en-republique-democratique-du-congo','2026-08-13 10:17:16.394947','2026-08-13 10:17:16.394970','PROJET DE LA CRÉATION D’UN CENTRE DE FORMATION PROFESSIONNEL EN FAVEUR DES ORPHELINS DE L’ORPHELINAT CITÉ DE LA MISÉRICORDE EN RÉPUBLIQUE DÉMOCRATIQUE DU CONGO',' Contexte et justification du projet&nbsp;: Le faible taux de fréquentation aux études des orphelins due aux guerres à répétition à l’Est de la République Démocratique du Congo et plus spécialement au manque des moyens financiers par les membres de leurs familles connus ou inconnus ont poussé certains enfants dont l’âge scolaire est déjà avancé à [&hellip;] 
','
<figure><img width="715" height="429" src="/media/media/2026/08/wp/2026/08/img-20241215-wa00592900465635429704277.jpg" alt=""/></figure>



<p>Contexte et justification du projet : Le faible taux de fréquentation aux études des orphelins due aux guerres à répétition à l’Est de la République Démocratique du Congo et plus spécialement au manque des moyens financiers par les membres de leurs familles connus ou inconnus ont poussé certains enfants dont l’âge scolaire est déjà avancé à ne plus avoir la chance de gagner leur vie.</p>



<figure><img width="715" height="429" src="/media/media/2026/08/wp/2026/08/img-20241215-wa00615161243459594582671.jpg" alt=""/></figure>



<p>Ceux-ci  deviennent après l’orphelinat des éléments constituant un danger pour la société soit retrouvés dans la rue, soit des voleurs ou victimes d’autres antivaleurs comme alcoolisme, tabagisme… Ainsi nous estimons que la création d’un centre de formation des orphelins en métier peut résoudre ce fléau<br/></p>



<p>Objectif du projet : notre projet a pour objectif principal de mettre en place un centre spécial pour l’apprentissage professionnel des orphelins de l’Orphelinat Cité de la Miséricorde ayant l’âge avancé et d’autres personnes qui désirent apprendre chez-nous en payant leur formation<br/></p>



<figure><img width="1024" height="768" src="/media/media/2026/08/wp/2026/08/img-20241215-wa00704925568464169999774.jpg" alt=""/></figure>



<p>Localisation du projet : le présent projet de construction sera localisé dans le quartier Panzi, ville de Bukavu, province du Sud-Kivu pendant une durée de 11 mois allant du 05 janvier 2025 au 05 Décembre 2025.<br/>Nature et cadre juridique du projet : cette initiative est une action de développement à caractère socio-éducatif visant la redynamisation et la promotion du secteur de l’enseignement. <br/></p>



<p>Stratégies du projet : notre stratégie est celle de la relance du secteur </p>



<p></p>



<figure><img width="1024" height="585" src="/media/media/2026/08/wp/2026/08/17459985616232594201096817036247.jpg" alt=""/></figure>



<p></p>



<p>Contacts:</p>



<p>Email: </p>



<p>citedelamisericorde@gmail.com  </p>



<p></p>
','published','2026-08-13 10:48:15.229333',0,0,0,'','','https://citedelamisericorde.wordpress.com/2024/12/15/projet-de-la-creation-dun-centre-de-formation-professionnel-en-faveur-des-orphelins-de-lorphelinat-cite-de-la-misericorde-en-republique-democratique-du-congo/',1,1,1,NULL);
INSERT INTO "articles_article" VALUES(9,'bienvenue-sur-la-page-de-la-cite-de-la-misericorde','2026-08-13 10:17:18.625043','2026-08-13 10:17:18.625062','BIENVENUE SUR LA PAGE DE LA CITÉ DE LA MISÉRICORDE',' La Cité de la Miséricorde est créé à BUKAVU en 2018,une organisation sans but lucratif, apolitique et non confessionnelle soumise aux dispositions du décret-loi n°004/2001 du 20 juillet portant dispositions générales applicables aux associations sans but lucratif et aux établissements d’utilité publique en RDC en vue d&#8217;apporter un soutien holistique aux enfants nécessiteux victimes des [&hellip;] 
','
<figure><img width="715" height="474" src="/media/media/2026/08/wp/2026/08/1000566683.jpg" alt=""/></figure>



<p>La Cité de la Miséricorde est créé à BUKAVU en 2018,une organisation sans but lucratif, apolitique et non confessionnelle soumise aux dispositions du décret-loi n°004/2001 du 20 juillet portant dispositions générales applicables aux associations sans but lucratif et aux établissements d’utilité publique en RDC en vue d’apporter un soutien holistique aux enfants nécessiteux victimes des conflits des guerres et violences sous toute forme.</p>



<p></p>
','published','2026-08-13 10:48:15.229333',0,0,0,'','','https://citedelamisericorde.wordpress.com/2024/12/15/bienvenue-sur-la-page-de-la-cite-de-la-misericorde/',1,1,1,NULL);
INSERT INTO "articles_article" VALUES(10,'autonomisation-des-femmes-autochtones-a-nyiragongo','2026-08-13 16:17:50.205856','2026-08-13 16:17:50.205875','Autonomisation des femmes autochtones à Nyiragongo','Découverte du projet d''autonomisation des femmes autochtones à Nyiragongo par la Cité de la Miséricorde. Un appui financier direct pour 150 ménages.','
<h2>Autonomisation socio-économique des femmes autochtones à Nyiragongo</h2>
<p>Dans le territoire de Nyiragongo, la Cité de la Miséricorde a concrétisé un projet ciblé de distribution de cash. Cette initiative s''adresse aux femmes autochtones pygmées cheffes de ménage afin de réduire la pauvreté et renforcer leur autonomie financière.</p>
<h3>Un soutien financier direct pour booster l''entrepreneuriat</h3>
<p>Avec un budget global de 7 500 dollars, le projet a permis d''octroyer une aide directe de 50 dollars par personne à un groupe de 150 femmes vulnérables. Ce panel comprend 70 veuves, 55 femmes abandonnées et 25 femmes au foyer. Cette somme sert de capital de départ pour lancer ou consolider de petites activités génératrices de revenus.</p>
<figure><img src="/media/media/2026/08/activite-femmes-nyiragongo/1786633035372.jpg" alt="Activité de la Cité de la Miséricorde à Nyiragongo"><figcaption>Remise de cash aux femmes autochtones cheffes de ménage — Nyiragongo</figcaption></figure><figure><img src="/media/media/2026/08/activite-femmes-nyiragongo/1786633357838.jpg" alt="Activité de la Cité de la Miséricorde à Nyiragongo"><figcaption>Remise de cash aux femmes autochtones cheffes de ménage — Nyiragongo</figcaption></figure><figure><img src="/media/media/2026/08/activite-femmes-nyiragongo/IMG-20260813-WA0027.jpg" alt="Activité de la Cité de la Miséricorde à Nyiragongo"><figcaption>Remise de cash aux femmes autochtones cheffes de ménage — Nyiragongo</figcaption></figure>
<h3>Sensibilisation et accompagnement communautaire</h3>
<p>En plus de la remise des fonds, l''organisation a sensibilisé les bénéficiaires sur la gestion efficace de ce capital. Pour garantir une inclusion sociale et économique durable, la Cité de la Miséricorde a également mobilisé les autorités locales, les leaders communautaires et les acteurs religieux autour de l''accompagnement de ces femmes.</p>
<figure><img src="/media/media/2026/08/activite-femmes-nyiragongo/IMG-20260813-WA0028.jpg" alt="Activité de la Cité de la Miséricorde à Nyiragongo"><figcaption>Bénéficiaires et équipe de la Cité de la Miséricorde — Nyiragongo</figcaption></figure><figure><img src="/media/media/2026/08/activite-femmes-nyiragongo/IMG-20260813-WA0033.jpg" alt="Activité de la Cité de la Miséricorde à Nyiragongo"><figcaption>Bénéficiaires et équipe de la Cité de la Miséricorde — Nyiragongo</figcaption></figure><figure><img src="/media/media/2026/08/activite-femmes-nyiragongo/IMG-20260813-WA0036.jpg" alt="Activité de la Cité de la Miséricorde à Nyiragongo"><figcaption>Bénéficiaires et équipe de la Cité de la Miséricorde — Nyiragongo</figcaption></figure>
<h3>Une démarche axée sur la dignité et l''autonomie</h3>
<p>L''organisation rappelle que lutter contre la vulnérabilité implique de redonner aux personnes la capacité de subvenir elles-mêmes aux besoins fondamentaux de leurs enfants. Ce transfert d''argent constitue une première étape essentielle vers une résilience à long terme.</p>
<h3>Remerciements et appel aux partenaires</h3>
<p>La Cité de la Miséricorde exprime sa reconnaissance envers ses donateurs. Elle invite les institutions, les organisations humanitaires et les personnes de bonne volonté à poursuivre leur soutien aux femmes autochtones cheffes de famille, car investir dans une femme revient à protéger toute une communauté.</p>
<figure><img src="/media/media/2026/08/activite-femmes-nyiragongo/IMG-20260813-WA0039.jpg" alt="Activité de la Cité de la Miséricorde à Nyiragongo"><figcaption>Rencontre avec les autorités et leaders communautaires — Nyiragongo</figcaption></figure>
','published','2026-08-13 16:17:50.204145',1,0,1,'Autonomisation des femmes autochtones à Nyiragongo — Cité de la Miséricorde','Découverte du projet d''autonomisation des femmes autochtones à Nyiragongo par la Cité de la Miséricorde. Un appui financier direct pour 150 ménages.','',6,2,2,78);
INSERT INTO "articles_article" VALUES(11,'lutte-contre-la-malnutrition-a-nyiragongo-bilan-du-projet','2026-08-13 16:26:15.459499','2026-08-13 16:26:15.459523','Lutte contre la malnutrition à Nyiragongo — Bilan du projet','Bilan du projet nutritionnel mené à Mudja au Nord-Kivu par la Cité de la Miséricorde : 250 enfants pris en charge et 62 % de guérisons.','
<h2>Lutte contre la malnutrition infantile à Mudja — Bilan et impact du projet</h2>
<p>Dans le territoire de Nyiragongo au Nord-Kivu, la santé des enfants reste une priorité. Du 8 janvier au 8 juillet 2026, l''organisation Cité de la Miséricorde, sous la coordination de Marie-Manassé ZIRHUMANA KAMOLE, a exécuté un projet de prévention, de dépistage et de prise en charge de la malnutrition dans le groupement de Mudja.</p>
<h3>Une équipe mobilisée pour la communauté</h3>
<p>Pour mener à bien ce projet financé à hauteur de 5 500 dollars, l''organisation a réuni trois nutritionnistes, quatre relais communautaires, deux cuisinières et un superviseur. Ensemble, ils ont assuré le dépistage, le suivi nutritionnel trois fois par semaine et la distribution de repas adaptés.</p>
<figure><img src="/media/media/2026/08/bilan-malnutrition-nyiragongo/1786632805802.jpg" alt="Prise en charge nutritionnelle des enfants à Mudja (Nyiragongo)"><figcaption>Équipe mobilisée pour la prise en charge nutritionnelle — Mudja</figcaption></figure><figure><img src="/media/media/2026/08/bilan-malnutrition-nyiragongo/1786632905245.jpg" alt="Prise en charge nutritionnelle des enfants à Mudja (Nyiragongo)"><figcaption>Équipe mobilisée pour la prise en charge nutritionnelle — Mudja</figcaption></figure>
<h3>Des résultats encourageants</h3>
<p>L''initiative a permis de prendre en charge 250 enfants de moins de 59 mois. Parmi eux, 157 enfants ont été déclarés totalement guéris, ce qui représente un taux de réussite de 62,8 %. C''est une avancée importante pour les familles de la région.</p>
<figure><img src="/media/media/2026/08/bilan-malnutrition-nyiragongo/1786632934252.jpg" alt="Prise en charge nutritionnelle des enfants à Mudja (Nyiragongo)"><figcaption>Suivi nutritionnel des enfants de moins de 59 mois — Mudja</figcaption></figure><figure><img src="/media/media/2026/08/activite-femmes-nyiragongo/1786633357838.jpg" alt="Activité de la Cité de la Miséricorde à Nyiragongo"><figcaption>Suivi nutritionnel des enfants de moins de 59 mois — Mudja</figcaption></figure>
<h3>Défis et perspectives d''avenir</h3>
<p>Malgré ces bons résultats, la précarité et l''insécurité alimentaire exposent certains enfants guéris à des risques de rechute. De plus, le manque de financements n''a pas permis de prolonger le suivi de ceux qui nécessitent encore des soins.</p>
<h3>Un grand merci à nos donateurs</h3>
<p>La Cité de la Miséricorde remercie chaleureusement les donateurs de France et du Canada pour leur générosité. Leur soutien a permis d''offrir une prise en charge vitale à ces enfants.</p>
<h3>Appel à l''action</h3>
<p>La lutte contre la malnutrition doit se poursuivre. Nous invitons les partenaires et les personnes de bonne volonté à nous rejoindre pour pérenniser ces actions et protéger durablement la santé des enfants vulnérables.</p>
<figure><img src="/media/media/2026/08/bilan-malnutrition-nyiragongo/IMG-20260804-WA0007.jpg" alt="Prise en charge nutritionnelle des enfants à Mudja (Nyiragongo)"><figcaption>Activité du projet nutritionnel — Nyiragongo</figcaption></figure>
','published','2026-08-13 16:26:15.457638',1,0,1,'Lutte contre la malnutrition à Nyiragongo — Bilan du projet | Cité de la Miséricorde','Bilan du projet nutritionnel mené à Mudja au Nord-Kivu par la Cité de la Miséricorde : 250 enfants pris en charge et 62 % de guérisons.','',2,2,2,87);
CREATE TABLE "articles_article_categories" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "article_id" bigint NOT NULL REFERENCES "articles_article" ("id") DEFERRABLE INITIALLY DEFERRED, "articlecategory_id" bigint NOT NULL REFERENCES "articles_articlecategory" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "articles_article_categories" VALUES(1,1,2);
INSERT INTO "articles_article_categories" VALUES(2,2,2);
INSERT INTO "articles_article_categories" VALUES(3,3,2);
INSERT INTO "articles_article_categories" VALUES(4,4,2);
INSERT INTO "articles_article_categories" VALUES(5,5,1);
INSERT INTO "articles_article_categories" VALUES(6,6,2);
INSERT INTO "articles_article_categories" VALUES(7,7,2);
INSERT INTO "articles_article_categories" VALUES(8,8,1);
INSERT INTO "articles_article_categories" VALUES(9,9,2);
INSERT INTO "articles_article_categories" VALUES(10,10,3);
INSERT INTO "articles_article_categories" VALUES(11,11,4);
INSERT INTO "articles_article_categories" VALUES(12,1,5);
INSERT INTO "articles_article_categories" VALUES(13,11,5);
CREATE TABLE "articles_article_related_images" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "article_id" bigint NOT NULL REFERENCES "articles_article" ("id") DEFERRABLE INITIALLY DEFERRED, "mediaitem_id" bigint NOT NULL REFERENCES "media_mediaitem" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "articles_article_related_images" VALUES(1,10,78);
INSERT INTO "articles_article_related_images" VALUES(2,10,79);
INSERT INTO "articles_article_related_images" VALUES(3,10,80);
INSERT INTO "articles_article_related_images" VALUES(4,10,81);
INSERT INTO "articles_article_related_images" VALUES(5,10,82);
INSERT INTO "articles_article_related_images" VALUES(6,10,83);
INSERT INTO "articles_article_related_images" VALUES(7,10,84);
INSERT INTO "articles_article_related_images" VALUES(8,11,79);
INSERT INTO "articles_article_related_images" VALUES(9,11,85);
INSERT INTO "articles_article_related_images" VALUES(10,11,86);
INSERT INTO "articles_article_related_images" VALUES(11,11,87);
INSERT INTO "articles_article_related_images" VALUES(12,11,88);
CREATE TABLE "articles_article_tags" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "article_id" bigint NOT NULL REFERENCES "articles_article" ("id") DEFERRABLE INITIALLY DEFERRED, "articletag_id" bigint NOT NULL REFERENCES "articles_articletag" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "articles_article_tags" VALUES(1,3,1);
INSERT INTO "articles_article_tags" VALUES(2,3,2);
INSERT INTO "articles_article_tags" VALUES(3,5,3);
INSERT INTO "articles_article_tags" VALUES(4,10,4);
INSERT INTO "articles_article_tags" VALUES(5,10,5);
INSERT INTO "articles_article_tags" VALUES(6,11,4);
INSERT INTO "articles_article_tags" VALUES(7,11,6);
INSERT INTO "articles_article_tags" VALUES(8,11,7);
CREATE TABLE "articles_articlecategory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "slug" varchar(255) NOT NULL UNIQUE, "name" varchar(120) NOT NULL);
INSERT INTO "articles_articlecategory" VALUES(1,'projet','PROJET');
INSERT INTO "articles_articlecategory" VALUES(2,'uncategorized','Uncategorized');
INSERT INTO "articles_articlecategory" VALUES(3,'autonomisation-des-femmes','Autonomisation des femmes');
INSERT INTO "articles_articlecategory" VALUES(4,'lutte-contre-la-malnutrition','Lutte contre la malnutrition');
INSERT INTO "articles_articlecategory" VALUES(5,'nutrition','Nutrition');
CREATE TABLE "articles_articletag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "slug" varchar(255) NOT NULL UNIQUE, "name" varchar(80) NOT NULL);
INSERT INTO "articles_articletag" VALUES(1,'appel','APPEL');
INSERT INTO "articles_articletag" VALUES(2,'don','DON');
INSERT INTO "articles_articletag" VALUES(3,'lutte-contre-la-pauvrete-et-la-malnutrition-a-lest-de-la-republique-democratique-du-congo','lutte contre la pauvreté et la malnutrition à l''Est de la République Démocratique du Congo');
INSERT INTO "articles_articletag" VALUES(4,'nyiragongo','Nyiragongo');
INSERT INTO "articles_articletag" VALUES(5,'femmes','Femmes');
INSERT INTO "articles_articletag" VALUES(6,'mudja','Mudja');
INSERT INTO "articles_articletag" VALUES(7,'nutrition','Nutrition');
CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
INSERT INTO "auth_group" VALUES(1,'Super Admin');
INSERT INTO "auth_group" VALUES(2,'Administrateur');
INSERT INTO "auth_group" VALUES(3,'Éditeur');
INSERT INTO "auth_group" VALUES(4,'Gestionnaire de projets');
INSERT INTO "auth_group" VALUES(5,'Gestionnaire financier');
INSERT INTO "auth_group" VALUES(6,'Auteur');
CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
INSERT INTO "auth_permission" VALUES(1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES(2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES(3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES(4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES(5,3,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES(6,3,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES(7,3,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES(8,3,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES(9,2,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES(10,2,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES(11,2,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES(12,2,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES(13,4,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES(14,4,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES(15,4,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES(16,4,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES(17,5,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES(18,5,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES(19,5,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES(20,5,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES(21,6,'add_user','Can add utilisateur');
INSERT INTO "auth_permission" VALUES(22,6,'change_user','Can change utilisateur');
INSERT INTO "auth_permission" VALUES(23,6,'delete_user','Can delete utilisateur');
INSERT INTO "auth_permission" VALUES(24,6,'view_user','Can view utilisateur');
INSERT INTO "auth_permission" VALUES(25,7,'add_sitesettings','Can add paramètres du site');
INSERT INTO "auth_permission" VALUES(26,7,'change_sitesettings','Can change paramètres du site');
INSERT INTO "auth_permission" VALUES(27,7,'delete_sitesettings','Can delete paramètres du site');
INSERT INTO "auth_permission" VALUES(28,7,'view_sitesettings','Can view paramètres du site');
INSERT INTO "auth_permission" VALUES(29,8,'add_page','Can add page');
INSERT INTO "auth_permission" VALUES(30,8,'change_page','Can change page');
INSERT INTO "auth_permission" VALUES(31,8,'delete_page','Can delete page');
INSERT INTO "auth_permission" VALUES(32,8,'view_page','Can view page');
INSERT INTO "auth_permission" VALUES(33,9,'add_report','Can add rapport / document');
INSERT INTO "auth_permission" VALUES(34,9,'change_report','Can change rapport / document');
INSERT INTO "auth_permission" VALUES(35,9,'delete_report','Can delete rapport / document');
INSERT INTO "auth_permission" VALUES(36,9,'view_report','Can view rapport / document');
INSERT INTO "auth_permission" VALUES(37,11,'add_articlecategory','Can add catégorie d''article');
INSERT INTO "auth_permission" VALUES(38,11,'change_articlecategory','Can change catégorie d''article');
INSERT INTO "auth_permission" VALUES(39,11,'delete_articlecategory','Can delete catégorie d''article');
INSERT INTO "auth_permission" VALUES(40,11,'view_articlecategory','Can view catégorie d''article');
INSERT INTO "auth_permission" VALUES(41,12,'add_articletag','Can add étiquette');
INSERT INTO "auth_permission" VALUES(42,12,'change_articletag','Can change étiquette');
INSERT INTO "auth_permission" VALUES(43,12,'delete_articletag','Can delete étiquette');
INSERT INTO "auth_permission" VALUES(44,12,'view_articletag','Can view étiquette');
INSERT INTO "auth_permission" VALUES(45,10,'add_article','Can add article');
INSERT INTO "auth_permission" VALUES(46,10,'change_article','Can change article');
INSERT INTO "auth_permission" VALUES(47,10,'delete_article','Can delete article');
INSERT INTO "auth_permission" VALUES(48,10,'view_article','Can view article');
INSERT INTO "auth_permission" VALUES(49,13,'add_program','Can add programme');
INSERT INTO "auth_permission" VALUES(50,13,'change_program','Can change programme');
INSERT INTO "auth_permission" VALUES(51,13,'delete_program','Can delete programme');
INSERT INTO "auth_permission" VALUES(52,13,'view_program','Can view programme');
INSERT INTO "auth_permission" VALUES(53,15,'add_projectstatus','Can add statut de projet');
INSERT INTO "auth_permission" VALUES(54,15,'change_projectstatus','Can change statut de projet');
INSERT INTO "auth_permission" VALUES(55,15,'delete_projectstatus','Can delete statut de projet');
INSERT INTO "auth_permission" VALUES(56,15,'view_projectstatus','Can view statut de projet');
INSERT INTO "auth_permission" VALUES(57,14,'add_project','Can add projet');
INSERT INTO "auth_permission" VALUES(58,14,'change_project','Can change projet');
INSERT INTO "auth_permission" VALUES(59,14,'delete_project','Can delete projet');
INSERT INTO "auth_permission" VALUES(60,14,'view_project','Can view projet');
INSERT INTO "auth_permission" VALUES(61,17,'add_donor','Can add donateur');
INSERT INTO "auth_permission" VALUES(62,17,'change_donor','Can change donateur');
INSERT INTO "auth_permission" VALUES(63,17,'delete_donor','Can delete donateur');
INSERT INTO "auth_permission" VALUES(64,17,'view_donor','Can view donateur');
INSERT INTO "auth_permission" VALUES(65,16,'add_donation','Can add don');
INSERT INTO "auth_permission" VALUES(66,16,'change_donation','Can change don');
INSERT INTO "auth_permission" VALUES(67,16,'delete_donation','Can delete don');
INSERT INTO "auth_permission" VALUES(68,16,'view_donation','Can view don');
INSERT INTO "auth_permission" VALUES(69,18,'add_paymentprovider','Can add passerelle de paiement');
INSERT INTO "auth_permission" VALUES(70,18,'change_paymentprovider','Can change passerelle de paiement');
INSERT INTO "auth_permission" VALUES(71,18,'delete_paymentprovider','Can delete passerelle de paiement');
INSERT INTO "auth_permission" VALUES(72,18,'view_paymentprovider','Can view passerelle de paiement');
INSERT INTO "auth_permission" VALUES(73,19,'add_paymenttransaction','Can add transaction de paiement');
INSERT INTO "auth_permission" VALUES(74,19,'change_paymenttransaction','Can change transaction de paiement');
INSERT INTO "auth_permission" VALUES(75,19,'delete_paymenttransaction','Can delete transaction de paiement');
INSERT INTO "auth_permission" VALUES(76,19,'view_paymenttransaction','Can view transaction de paiement');
INSERT INTO "auth_permission" VALUES(77,20,'add_webhookevent','Can add événement webhook');
INSERT INTO "auth_permission" VALUES(78,20,'change_webhookevent','Can change événement webhook');
INSERT INTO "auth_permission" VALUES(79,20,'delete_webhookevent','Can delete événement webhook');
INSERT INTO "auth_permission" VALUES(80,20,'view_webhookevent','Can view événement webhook');
INSERT INTO "auth_permission" VALUES(81,21,'add_mediacategory','Can add catégorie de média');
INSERT INTO "auth_permission" VALUES(82,21,'change_mediacategory','Can change catégorie de média');
INSERT INTO "auth_permission" VALUES(83,21,'delete_mediacategory','Can delete catégorie de média');
INSERT INTO "auth_permission" VALUES(84,21,'view_mediacategory','Can view catégorie de média');
INSERT INTO "auth_permission" VALUES(85,22,'add_mediaitem','Can add média');
INSERT INTO "auth_permission" VALUES(86,22,'change_mediaitem','Can change média');
INSERT INTO "auth_permission" VALUES(87,22,'delete_mediaitem','Can delete média');
INSERT INTO "auth_permission" VALUES(88,22,'view_mediaitem','Can view média');
INSERT INTO "auth_permission" VALUES(89,23,'add_gallery','Can add galerie');
INSERT INTO "auth_permission" VALUES(90,23,'change_gallery','Can change galerie');
INSERT INTO "auth_permission" VALUES(91,23,'delete_gallery','Can delete galerie');
INSERT INTO "auth_permission" VALUES(92,23,'view_gallery','Can view galerie');
INSERT INTO "auth_permission" VALUES(93,24,'add_galleryitem','Can add image de galerie');
INSERT INTO "auth_permission" VALUES(94,24,'change_galleryitem','Can change image de galerie');
INSERT INTO "auth_permission" VALUES(95,24,'delete_galleryitem','Can delete image de galerie');
INSERT INTO "auth_permission" VALUES(96,24,'view_galleryitem','Can view image de galerie');
INSERT INTO "auth_permission" VALUES(97,25,'add_testimonial','Can add témoignage');
INSERT INTO "auth_permission" VALUES(98,25,'change_testimonial','Can change témoignage');
INSERT INTO "auth_permission" VALUES(99,25,'delete_testimonial','Can delete témoignage');
INSERT INTO "auth_permission" VALUES(100,25,'view_testimonial','Can view témoignage');
INSERT INTO "auth_permission" VALUES(101,26,'add_partner','Can add partenaire');
INSERT INTO "auth_permission" VALUES(102,26,'change_partner','Can change partenaire');
INSERT INTO "auth_permission" VALUES(103,26,'delete_partner','Can delete partenaire');
INSERT INTO "auth_permission" VALUES(104,26,'view_partner','Can view partenaire');
INSERT INTO "auth_permission" VALUES(105,27,'add_statistic','Can add indicateur d''impact');
INSERT INTO "auth_permission" VALUES(106,27,'change_statistic','Can change indicateur d''impact');
INSERT INTO "auth_permission" VALUES(107,27,'delete_statistic','Can delete indicateur d''impact');
INSERT INTO "auth_permission" VALUES(108,27,'view_statistic','Can view indicateur d''impact');
INSERT INTO "auth_permission" VALUES(109,28,'add_subscriber','Can add abonné');
INSERT INTO "auth_permission" VALUES(110,28,'change_subscriber','Can change abonné');
INSERT INTO "auth_permission" VALUES(111,28,'delete_subscriber','Can delete abonné');
INSERT INTO "auth_permission" VALUES(112,28,'view_subscriber','Can view abonné');
INSERT INTO "auth_permission" VALUES(113,29,'add_contactmessage','Can add message de contact');
INSERT INTO "auth_permission" VALUES(114,29,'change_contactmessage','Can change message de contact');
INSERT INTO "auth_permission" VALUES(115,29,'delete_contactmessage','Can delete message de contact');
INSERT INTO "auth_permission" VALUES(116,29,'view_contactmessage','Can view message de contact');
INSERT INTO "auth_permission" VALUES(117,30,'add_dailystats','Can add statistique quotidienne');
INSERT INTO "auth_permission" VALUES(118,30,'change_dailystats','Can change statistique quotidienne');
INSERT INTO "auth_permission" VALUES(119,30,'delete_dailystats','Can delete statistique quotidienne');
INSERT INTO "auth_permission" VALUES(120,30,'view_dailystats','Can view statistique quotidienne');
INSERT INTO "auth_permission" VALUES(121,31,'add_pageview','Can add vue de page');
INSERT INTO "auth_permission" VALUES(122,31,'change_pageview','Can change vue de page');
INSERT INTO "auth_permission" VALUES(123,31,'delete_pageview','Can delete vue de page');
INSERT INTO "auth_permission" VALUES(124,31,'view_pageview','Can view vue de page');
INSERT INTO "auth_permission" VALUES(125,33,'add_migrationrun','Can add exécution de migration');
INSERT INTO "auth_permission" VALUES(126,33,'change_migrationrun','Can change exécution de migration');
INSERT INTO "auth_permission" VALUES(127,33,'delete_migrationrun','Can delete exécution de migration');
INSERT INTO "auth_permission" VALUES(128,33,'view_migrationrun','Can view exécution de migration');
INSERT INTO "auth_permission" VALUES(129,34,'add_urlmapping','Can add correspondance d''URL');
INSERT INTO "auth_permission" VALUES(130,34,'change_urlmapping','Can change correspondance d''URL');
INSERT INTO "auth_permission" VALUES(131,34,'delete_urlmapping','Can delete correspondance d''URL');
INSERT INTO "auth_permission" VALUES(132,34,'view_urlmapping','Can view correspondance d''URL');
INSERT INTO "auth_permission" VALUES(133,32,'add_importedrecord','Can add élément importé');
INSERT INTO "auth_permission" VALUES(134,32,'change_importedrecord','Can change élément importé');
INSERT INTO "auth_permission" VALUES(135,32,'delete_importedrecord','Can delete élément importé');
INSERT INTO "auth_permission" VALUES(136,32,'view_importedrecord','Can view élément importé');
INSERT INTO "auth_permission" VALUES(137,35,'add_teammember','Can add Membre de l''équipe');
INSERT INTO "auth_permission" VALUES(138,35,'change_teammember','Can change Membre de l''équipe');
INSERT INTO "auth_permission" VALUES(139,35,'delete_teammember','Can delete Membre de l''équipe');
INSERT INTO "auth_permission" VALUES(140,35,'view_teammember','Can view Membre de l''équipe');
CREATE TABLE "contact_contactmessage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "name" varchar(200) NOT NULL, "email" varchar(254) NOT NULL, "phone" varchar(50) NOT NULL, "subject" varchar(30) NOT NULL, "message" text NOT NULL, "is_read" bool NOT NULL, "read_at" datetime NULL, "is_spam" bool NOT NULL, "ip_address" char(39) NULL, "user_agent" varchar(300) NOT NULL);
INSERT INTO "contact_contactmessage" VALUES(1,'2026-08-13 10:37:27.813521','2026-08-13 10:37:27.813588','Test Contact','test-contact@example.org','+243 990 000 000','donation','Message de test du formulaire securise.',0,NULL,0,'127.0.0.1','Mozilla/5.0 (Windows NT; Windows NT 10.0; fr-FR) WindowsPowerShell/5.1.19041.6456');
CREATE TABLE "core_sitesettings" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "organization_name" varchar(200) NOT NULL, "legal_name" varchar(200) NOT NULL, "tagline" varchar(200) NOT NULL, "email" varchar(254) NOT NULL, "phone" varchar(50) NOT NULL, "address_bukavu" varchar(300) NOT NULL, "address_goma" varchar(300) NOT NULL, "facebook" varchar(200) NOT NULL, "instagram" varchar(200) NOT NULL, "pinterest" varchar(200) NOT NULL, "twitter" varchar(200) NOT NULL, "youtube" varchar(200) NOT NULL, "whatsapp" varchar(50) NOT NULL, "map_embed_url" varchar(200) NOT NULL, "donation_currency" varchar(3) NOT NULL, "pwa_theme_color" varchar(7) NOT NULL, "google_analytics_id" varchar(50) NOT NULL, "matomo_url" varchar(200) NOT NULL, "matomo_site_id" varchar(20) NOT NULL, "recaptcha_site_key" varchar(100) NOT NULL, "maintenance_mode" bool NOT NULL);
INSERT INTO "core_sitesettings" VALUES(1,'Cité de la Miséricorde','Cité de la Miséricorde','Heureux ceux qui procurent la paix','citedelamisericorde@gmail.com','','','','','','','','','','','USD','#0f766e','','','','',0);
CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
INSERT INTO "django_content_type" VALUES(1,'admin','logentry');
INSERT INTO "django_content_type" VALUES(2,'auth','group');
INSERT INTO "django_content_type" VALUES(3,'auth','permission');
INSERT INTO "django_content_type" VALUES(4,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES(5,'sessions','session');
INSERT INTO "django_content_type" VALUES(6,'accounts','user');
INSERT INTO "django_content_type" VALUES(7,'core','sitesettings');
INSERT INTO "django_content_type" VALUES(8,'pages','page');
INSERT INTO "django_content_type" VALUES(9,'pages','report');
INSERT INTO "django_content_type" VALUES(10,'articles','article');
INSERT INTO "django_content_type" VALUES(11,'articles','articlecategory');
INSERT INTO "django_content_type" VALUES(12,'articles','articletag');
INSERT INTO "django_content_type" VALUES(13,'programs','program');
INSERT INTO "django_content_type" VALUES(14,'projects','project');
INSERT INTO "django_content_type" VALUES(15,'projects','projectstatus');
INSERT INTO "django_content_type" VALUES(16,'donations','donation');
INSERT INTO "django_content_type" VALUES(17,'donations','donor');
INSERT INTO "django_content_type" VALUES(18,'payments','paymentprovider');
INSERT INTO "django_content_type" VALUES(19,'payments','paymenttransaction');
INSERT INTO "django_content_type" VALUES(20,'payments','webhookevent');
INSERT INTO "django_content_type" VALUES(21,'media','mediacategory');
INSERT INTO "django_content_type" VALUES(22,'media','mediaitem');
INSERT INTO "django_content_type" VALUES(23,'gallery','gallery');
INSERT INTO "django_content_type" VALUES(24,'gallery','galleryitem');
INSERT INTO "django_content_type" VALUES(25,'testimonials','testimonial');
INSERT INTO "django_content_type" VALUES(26,'partners','partner');
INSERT INTO "django_content_type" VALUES(27,'statistics','statistic');
INSERT INTO "django_content_type" VALUES(28,'newsletter','subscriber');
INSERT INTO "django_content_type" VALUES(29,'contact','contactmessage');
INSERT INTO "django_content_type" VALUES(30,'analytics','dailystats');
INSERT INTO "django_content_type" VALUES(31,'analytics','pageview');
INSERT INTO "django_content_type" VALUES(32,'migration','importedrecord');
INSERT INTO "django_content_type" VALUES(33,'migration','migrationrun');
INSERT INTO "django_content_type" VALUES(34,'migration','urlmapping');
INSERT INTO "django_content_type" VALUES(35,'team','teammember');
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
INSERT INTO "django_migrations" VALUES(1,'contenttypes','0001_initial','2026-08-13 09:33:30.061112');
INSERT INTO "django_migrations" VALUES(2,'contenttypes','0002_remove_content_type_name','2026-08-13 09:33:30.157226');
INSERT INTO "django_migrations" VALUES(3,'auth','0001_initial','2026-08-13 09:33:30.342170');
INSERT INTO "django_migrations" VALUES(4,'auth','0002_alter_permission_name_max_length','2026-08-13 09:33:30.455752');
INSERT INTO "django_migrations" VALUES(5,'auth','0003_alter_user_email_max_length','2026-08-13 09:33:30.553448');
INSERT INTO "django_migrations" VALUES(6,'auth','0004_alter_user_username_opts','2026-08-13 09:33:30.651145');
INSERT INTO "django_migrations" VALUES(7,'auth','0005_alter_user_last_login_null','2026-08-13 09:33:30.744075');
INSERT INTO "django_migrations" VALUES(8,'auth','0006_require_contenttypes_0002','2026-08-13 09:33:30.830203');
INSERT INTO "django_migrations" VALUES(9,'auth','0007_alter_validators_add_error_messages','2026-08-13 09:33:30.909293');
INSERT INTO "django_migrations" VALUES(10,'auth','0008_alter_user_username_max_length','2026-08-13 09:33:30.995536');
INSERT INTO "django_migrations" VALUES(11,'auth','0009_alter_user_last_name_max_length','2026-08-13 09:33:31.106323');
INSERT INTO "django_migrations" VALUES(12,'auth','0010_alter_group_name_max_length','2026-08-13 09:33:31.216996');
INSERT INTO "django_migrations" VALUES(13,'auth','0011_update_proxy_permissions','2026-08-13 09:33:31.322370');
INSERT INTO "django_migrations" VALUES(14,'auth','0012_alter_user_first_name_max_length','2026-08-13 09:33:31.429565');
INSERT INTO "django_migrations" VALUES(15,'accounts','0001_initial','2026-08-13 09:33:31.631636');
INSERT INTO "django_migrations" VALUES(16,'admin','0001_initial','2026-08-13 09:33:31.897057');
INSERT INTO "django_migrations" VALUES(17,'admin','0002_logentry_remove_auto_add','2026-08-13 09:33:31.995210');
INSERT INTO "django_migrations" VALUES(18,'admin','0003_logentry_add_action_flag_choices','2026-08-13 09:33:32.102478');
INSERT INTO "django_migrations" VALUES(19,'analytics','0001_initial','2026-08-13 09:33:32.263828');
INSERT INTO "django_migrations" VALUES(20,'media','0001_initial','2026-08-13 09:33:32.440229');
INSERT INTO "django_migrations" VALUES(21,'articles','0001_initial','2026-08-13 09:33:32.661867');
INSERT INTO "django_migrations" VALUES(22,'contact','0001_initial','2026-08-13 09:33:32.950840');
INSERT INTO "django_migrations" VALUES(23,'core','0001_initial','2026-08-13 09:33:33.069198');
INSERT INTO "django_migrations" VALUES(24,'programs','0001_initial','2026-08-13 09:33:33.317166');
INSERT INTO "django_migrations" VALUES(25,'projects','0001_initial','2026-08-13 09:33:33.559949');
INSERT INTO "django_migrations" VALUES(26,'donations','0001_initial','2026-08-13 09:33:33.771238');
INSERT INTO "django_migrations" VALUES(27,'payments','0001_initial','2026-08-13 09:33:34.004040');
INSERT INTO "django_migrations" VALUES(28,'donations','0002_initial','2026-08-13 09:33:34.174628');
INSERT INTO "django_migrations" VALUES(29,'gallery','0001_initial','2026-08-13 09:33:34.403190');
INSERT INTO "django_migrations" VALUES(30,'migration','0001_initial','2026-08-13 09:33:34.591205');
INSERT INTO "django_migrations" VALUES(31,'newsletter','0001_initial','2026-08-13 09:33:34.769172');
INSERT INTO "django_migrations" VALUES(32,'pages','0001_initial','2026-08-13 09:33:35.002591');
INSERT INTO "django_migrations" VALUES(33,'partners','0001_initial','2026-08-13 09:33:35.214293');
INSERT INTO "django_migrations" VALUES(34,'sessions','0001_initial','2026-08-13 09:33:35.391106');
INSERT INTO "django_migrations" VALUES(35,'testimonials','0001_initial','2026-08-13 09:33:35.634709');
INSERT INTO "django_migrations" VALUES(36,'statistics','0001_initial','2026-08-13 09:37:45.866190');
INSERT INTO "django_migrations" VALUES(37,'team','0001_initial','2026-08-13 23:37:55.930517');
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
INSERT INTO "django_session" VALUES('shiegwdg3idcbbfawl2wt1pcz4cvs71p','.eJxVjDkOwjAQAP-yNbJ8sF6ckp43WF4fOIBsKU4qxN9RpBTQzozmDT5sa_XbyIufE0yg4PTLOMRnbrtIj9DuXcTe1mVmsSfisEPcesqv69H-DWoYFSYgx8VyKo6YEA0zoXWWg9WStXHuQueUURZijFwUp1Jk0KiNtMopMvD5AusmN7E:1wuSCS:AuvVMv0elVS9QzoehesTj_AMgl5iA12tG_q-DJtojaU','2026-08-27 09:58:12.165408');
INSERT INTO "django_session" VALUES('j7whvqeqjc0bhyvqbeks9zf9u9quw71y','.eJxVjDkOwjAQAP-yNbJ8sF6ckp43WF4fOIBsKU4qxN9RpBTQzozmDT5sa_XbyIufE0yg4PTLOMRnbrtIj9DuXcTe1mVmsSfisEPcesqv69H-DWoYFSYgx8VyKo6YEA0zoXWWg9WStXHuQueUURZijFwUp1Jk0KiNtMopMvD5AusmN7E:1wuSD6:uOno2h4EMF6JPM9KP-5tLeLFlCyLLfqsC7Nx2WumDZ8','2026-08-27 09:58:52.783603');
INSERT INTO "django_session" VALUES('5tipax8lgmk508xwqockfpis07afavbu','.eJxVjDkOwjAQAP-yNbJ8sF6ckp43WF4fOIBsKU4qxN9RpBTQzozmDT5sa_XbyIufE0yg4PTLOMRnbrtIj9DuXcTe1mVmsSfisEPcesqv69H-DWoYFSYgx8VyKo6YEA0zoXWWg9WStXHuQueUURZijFwUp1Jk0KiNtMopMvD5AusmN7E:1wuSFn:BUIHVvGm3u65LIPt2cSWKy1SWGhxi6ek7nQhrLEQnfM','2026-08-27 10:01:39.411978');
INSERT INTO "django_session" VALUES('5c6rdx3ftlubaygq2n0ao1gsbnl9hjuy','.eJxVjDkOwjAQAP-yNbJ8sF6ckp43WF4fOIBsKU4qxN9RpBTQzozmDT5sa_XbyIufE0yg4PTLOMRnbrtIj9DuXcTe1mVmsSfisEPcesqv69H-DWoYFSYgx8VyKo6YEA0zoXWWg9WStXHuQueUURZijFwUp1Jk0KiNtMopMvD5AusmN7E:1wuSG2:WVNfqM91VtOqtkAnFDgYH5JrqpBRqnWfPtVYZHkAzn0','2026-08-27 10:01:54.466565');
INSERT INTO "django_session" VALUES('5xig44tv53mufz3em0fxei9ausa97mpv','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuTEN:_ZtI0VrruwSVzlgEm2huqLmMI8WTcUiPbb-MU98t3AQ','2026-08-27 11:04:15.298014');
INSERT INTO "django_session" VALUES('j8047mvob90u0y0aekh72yl2fysonr2w','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuTVD:9Wc-IE3QUZfZdAl5oD3tdt7OFwm1OIb2xsUBppuCwuU','2026-08-27 11:21:39.279021');
INSERT INTO "django_session" VALUES('103m81lbtwmrnk71yeh2i09ma89ffncv','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuV2d:paW_UNOGD33gvP-Znm_tvoKszdyp5XDJQE8YWRd-Z5M','2026-08-27 13:00:15.454297');
INSERT INTO "django_session" VALUES('uszmzhsv8mpsny1cuteoy5ne8s4clxp8','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuesr:VN2soizBmfgYoNwK5rqw7YLz1k0182mUZbG3MlVkg2g','2026-08-27 23:30:49.561963');
INSERT INTO "django_session" VALUES('thwktvhsob8iyov5tf0afhteukvettia','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuetN:nOM3YzhIHY8cp16QChcNRnyFm8vWtvgf3beiXQBPvW4','2026-08-27 23:31:21.661750');
INSERT INTO "django_session" VALUES('by8cllzv84swnwdgl3zrdidgcflqvuld','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuetW:DMw28rmje4NQ5y7r-8CzaRODfKtkMfH8oVNTZVvJH7U','2026-08-27 23:31:30.571247');
INSERT INTO "django_session" VALUES('s0ym1taqutjhbx6tcl5t2g4aukunnv01','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuetc:1dBJ2of7LARVzsUZSRvV7nlNb4HkwnKpTexmTFGUvJg','2026-08-27 23:31:36.461823');
INSERT INTO "django_session" VALUES('q7wvsb023ecl5ouwfbspf4h4gtil8puf','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuev4:SNhYP98YT9SAIOStyEwse1J6BIsYtcUcmsgou5JVqWs','2026-08-27 23:33:06.549365');
INSERT INTO "django_session" VALUES('gpnm9vbhmtw8scbwko80sbaoeyl8fh6s','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuevC:TBfg7n9T8aqlkBAb_j2ReZbCVV9pSAEnHV3PDGlNKTE','2026-08-27 23:33:14.149725');
INSERT INTO "django_session" VALUES('yjess2604zxfqigkk2klxwka5i4qa9xk','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuevG:N4nf_AXKO7YAaLsw8_nXIn3rLB4xRoB4Lo0ztPJ4z0U','2026-08-27 23:33:18.876405');
INSERT INTO "django_session" VALUES('6qn7bk7m3jxtvakvuy1k5w6uer6cjuvu','.eJxVjEEOwiAQAP_C2RBgi109eu8byMJupWogKe3J-HdD0oNeZybzVoH2LYe9yRoWVlfl1OmXRUpPKV3wg8q96lTLti5R90QftumpsrxuR_s3yNRy34owAY-SBD17tnzGAaJN0UaazXhhGsAwekaYCdFCx-AtG-cQQH2-Ens4Tw:1wuevd:wH_S_UBPFPsoZtErouR3xvwkYtneXne1d9GzRKB2uwY','2026-08-27 23:33:41.963131');
INSERT INTO "django_session" VALUES('huoca54id13ei4mma8juyt3qf4ji48id','.eJxVjMsKwjAQAP9lzxLyKNmkR-9-Q9jsJqYqLTTtSfx3KfSg15lh3pBo31rae1nTJDCCgcsvy8TPMh9CHjTfF8XLvK1TVkeiTtvVbZHyup7t36BRbzBCdp41VrSDcdFHpjrEiNaSY67BVI2cbfBWSgyIIiaLiPOaHJJEE-DzBdk7N-M:1wuf3q:zxIVeMyEBH9HI2mjdpFiLVCUwfxTfNwUHmkKDf2sbFo','2026-08-27 23:42:10.985836');
INSERT INTO "django_session" VALUES('3l7nek4qr375l0ipztqosy46dbw19kqr','.eJxVjMsKwjAQAP9lzxLyKNmkR-9-Q9jsJqYqLTTtSfx3KfSg15lh3pBo31rae1nTJDCCgcsvy8TPMh9CHjTfF8XLvK1TVkeiTtvVbZHyup7t36BRbzBCdp41VrSDcdFHpjrEiNaSY67BVI2cbfBWSgyIIiaLiPOaHJJEE-DzBdk7N-M:1wuf40:lEazSANXKXTi8gj_uGfjn-giIwOLmr_zfpsrjmW4xeA','2026-08-27 23:42:20.836911');
INSERT INTO "django_session" VALUES('50x4o8zmrtnk5vucqb8ucepk39408tfs','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJkZGEyNHctZmUyNmFlNDY3NWRlYjU1MmFhNTQ4MmFkOTExNTU4NDYifQ:1wuf5N:BfqML5rsElsdETwRJl925fPEEVcnESh5d1d6qAzK5uA','2026-08-27 23:43:45.070773');
INSERT INTO "django_session" VALUES('52r9sks362ams07zz2jo3kca8lb2swvm','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJkZGEyNTktZTg4YzRmNjU5ZjAyMzEzODdlM2UxNzEwZjhiZWVhYWEifQ:1wuf5a:KWNh4hhAsFDvyc8oHkNNuHX1uJPJAJjufiN4XfQIz50','2026-08-27 23:43:58.370637');
INSERT INTO "django_session" VALUES('blwky6d6jlk7z54ge14rtohcwv8jy3xi','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJkZGEyNjgtOGUwOGY4Nzg0NjUyNTBjYWUxYzQxNjQ4N2FiMjk3ZDYifQ:1wuf68:PYZtUxmcfUl1qZwB7O8bwnlN4EUDYy61a6sgZ5-Wv_M','2026-08-27 23:44:32.917077');
INSERT INTO "django_session" VALUES('4jqirtq2glw2yvy2gm2sy5yvz3wrwdr4','eyJfcGFzc3dvcmRfcmVzZXRfdG9rZW4iOiJkZGEyNmgtZTczNzk4OTUyYzA0M2E2OTRjODQ0YTU0MDQ3YTE1N2EifQ:1wuf6I:8LT-AT-laWv4K_CcjkpQe2vobhOj7MkTRuOrLvoP0VY','2026-08-27 23:44:42.266509');
INSERT INTO "django_session" VALUES('snbyb77axna0e5kt86v5mky27op7nhfd','.eJxVjMsKwjAQAP9lzxLI5rFpj979hrBJtqYqKTTtSfx3KfSg15lh3hB532rcu6xxLjCChssvS5yf0g5RHtzui8pL29Y5qSNRp-3qthR5Xc_2b1C5VxgBHU0iZMVno00KlBMZdJ6FODgfyoCoOcvgyRBbO3kKOWhNFhkTJvh8AdfqN1M:1wuf6n:8GJ-NHif8rt5Hp0o3RpSCZo8ZjqGR5jSRiYr0YehpEo','2026-08-27 23:45:13.400237');
INSERT INTO "django_session" VALUES('fvdhi9js5zvkw5136ll5mzj245ra52u9','.eJxVjLsOwjAMAP_FM4ryMLTpyM43RHackAJKpKadEP-OKnWA9e50bwi0rSVsPS1hFpjAwOmXMcVnqruQB9V7U7HVdZlZ7Yk6bFe3Jul1Pdq_QaFeYALn0Iw-oTaE-UISh2itE-MtIboUz2hY0GvC7BgHY1HHkZGzZCZyCJ8vzWM33g:1wuf7B:fcpLDEZRZO3QGVr4pE7cTkLNFoo09djUi9reqT-_ty8','2026-08-27 23:45:37.068489');
INSERT INTO "django_session" VALUES('cw218jnvppnzfwcilz63zhc0gnv17ai1','.eJxVjLsOwjAMAP_FM4ryMLTpyM43RHackAJKpKadEP-OKnWA9e50bwi0rSVsPS1hFpjAwOmXMcVnqruQB9V7U7HVdZlZ7Yk6bFe3Jul1Pdq_QaFeYALn0Iw-oTaE-UISh2itE-MtIboUz2hY0GvC7BgHY1HHkZGzZCZyCJ8vzWM33g:1wufgO:FKoikEF4Tvbp8ko2zHW_2KZ2ROgpcYz53kEsK8d73qg','2026-08-28 00:22:00.582742');
INSERT INTO "django_session" VALUES('4xazcmqry6hejq7qb4b93r9jxwjo8s3f','.eJxVjDEOwjAMAP_iGUUldanTkZ03VI5j0wJKpKadEH9HlTrAene6N4y8rdO4VV3GOcEAHk6_LLI8Ne8iPTjfi5OS12WObk_cYau7laSv69H-DSauEwyA2lvTJQniKVFvgkbejEm6Hs2bURtCFERtjaRJjZ4FVWMwZeRLgM8XDiY5Sw:1wuftD:I8hQaSHHroULfh77BhuYrLsRPaw2lNyIpGJ230K5JDU','2026-08-28 00:35:15.658630');
CREATE TABLE "donations_donation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "reference" varchar(30) NOT NULL UNIQUE, "amount" decimal NOT NULL, "currency" varchar(3) NOT NULL, "frequency" varchar(10) NOT NULL, "status" varchar(12) NOT NULL, "provider_reference" varchar(255) NOT NULL, "idempotency_key" varchar(100) NOT NULL UNIQUE, "is_anonymous" bool NOT NULL, "donor_message" text NOT NULL, "receipt_pdf" varchar(100) NOT NULL, "receipt_sent_at" datetime NULL, "paid_at" datetime NULL, "project_id" bigint NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED, "provider_id" bigint NULL REFERENCES "payments_paymentprovider" ("id") DEFERRABLE INITIALLY DEFERRED, "donor_id" bigint NOT NULL REFERENCES "donations_donor" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "donations_donation" VALUES(1,'2026-08-13 10:27:35.287595','2026-08-13 10:34:04.636659','CMD-DON-2026-000001',25,'USD','once','SUCCEEDED','','k1',0,'','receipts/2026/08/recu-CMD-DON-2026-000001_P8gvXyN.pdf','2026-08-13 10:34:04.635451',NULL,NULL,NULL,1);
INSERT INTO "donations_donation" VALUES(2,'2026-08-13 10:29:06.154297','2026-08-13 10:29:06.154361','CMD-DON-2026-000002',25,'USD','once','SUCCEEDED','','k2',0,'','',NULL,NULL,NULL,NULL,2);
INSERT INTO "donations_donation" VALUES(3,'2026-08-13 10:30:57.931532','2026-08-13 10:30:57.931699','CMD-DON-2026-000003',25,'USD','once','PENDING','','anon-1786617057.899882',0,'','',NULL,NULL,NULL,NULL,3);
INSERT INTO "donations_donation" VALUES(4,'2026-08-13 10:31:35.570491','2026-08-13 10:31:37.179609','CMD-DON-2026-000004',25,'USD','once','SUCCEEDED','sandbox-0731216a322c402bab5d1d65272daa18','anon-1786617095.563991',0,'','receipts/2026/08/recu-CMD-DON-2026-000004.pdf','2026-08-13 10:31:37.179132','2026-08-13 10:31:36.113200',NULL,4,3);
INSERT INTO "donations_donation" VALUES(5,'2026-08-14 00:39:08.942708','2026-08-14 00:39:08.942728','CMD-DON-2026-000005',25,'USD','once','PENDING','','anon-1786667948.941412',0,'','',NULL,NULL,NULL,NULL,4);
INSERT INTO "donations_donation" VALUES(6,'2026-08-14 00:39:22.837108','2026-08-14 00:39:37.456239','CMD-DON-2026-000006',25,'USD','once','SUCCEEDED','sandbox-c38110326e5c4a8f8c279cb94aca5380','anon-1786667962.835564',0,'','receipts/2026/08/recu-CMD-DON-2026-000006.pdf','2026-08-14 00:39:37.455993','2026-08-14 00:39:23.243795',NULL,4,4);
CREATE TABLE "donations_donor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "name" varchar(200) NOT NULL, "email" varchar(254) NOT NULL, "phone" varchar(50) NOT NULL, "country" varchar(100) NOT NULL, "is_anonymous" bool NOT NULL, "is_recurring" bool NOT NULL, "notes" text NOT NULL);
INSERT INTO "donations_donor" VALUES(1,'2026-08-13 10:27:35.156134','2026-08-13 10:27:35.156283','Test','test@example.org','','',0,0,'');
INSERT INTO "donations_donor" VALUES(2,'2026-08-13 10:29:06.040053','2026-08-13 10:29:06.040097','T2','t2@example.org','','',0,0,'');
INSERT INTO "donations_donor" VALUES(3,'2026-08-13 10:30:57.721196','2026-08-13 10:30:57.721316','Donateur Live','test-live@example.org','','RD Congo',0,0,'');
INSERT INTO "donations_donor" VALUES(4,'2026-08-14 00:39:08.838900','2026-08-14 00:39:08.838947','Test Donateur','test.donateur@example.org','','France',0,0,'');
CREATE TABLE "gallery_gallery" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "slug" varchar(255) NOT NULL UNIQUE, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "title" varchar(200) NOT NULL, "description" text NOT NULL, "is_published" bool NOT NULL, "order" smallint unsigned NOT NULL CHECK ("order" >= 0), "cover_id" bigint NULL REFERENCES "media_mediaitem" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "gallery_gallery" VALUES(1,'autonomisation-des-femmes-autochtones-a-nyiragongo','2026-08-13 16:18:19.940009','2026-08-13 16:18:19.940148','Autonomisation des femmes autochtones à Nyiragongo','Distribution de cash et accompagnement de 150 femmes autochtones cheffes de ménage dans le territoire de Nyiragongo — projet de la Cité de la Miséricorde.',1,1,78);
INSERT INTO "gallery_gallery" VALUES(2,'lutte-contre-la-malnutrition-a-mudja-bilan','2026-08-13 16:26:15.934021','2026-08-13 16:26:15.934044','Lutte contre la malnutrition à Mudja — Bilan du projet','Prise en charge de 250 enfants de moins de 59 mois dans le groupement de Mudja (Nyiragongo) : dépistage, suivi nutritionnel et distribution de repas adaptés.',1,2,87);
CREATE TABLE "gallery_galleryitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "caption" varchar(300) NOT NULL, "position" smallint unsigned NOT NULL CHECK ("position" >= 0), "gallery_id" bigint NOT NULL REFERENCES "gallery_gallery" ("id") DEFERRABLE INITIALLY DEFERRED, "media_id" bigint NOT NULL REFERENCES "media_mediaitem" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "gallery_galleryitem" VALUES(1,'2026-08-13 16:18:20.086741','2026-08-13 16:18:20.086783','Photo 1 — Activité de distribution de cash, Nyiragongo',1,1,78);
INSERT INTO "gallery_galleryitem" VALUES(2,'2026-08-13 16:18:20.201625','2026-08-13 16:18:20.201681','Photo 2 — Activité de distribution de cash, Nyiragongo',2,1,79);
INSERT INTO "gallery_galleryitem" VALUES(3,'2026-08-13 16:18:20.303691','2026-08-13 16:18:20.303740','Photo 3 — Activité de distribution de cash, Nyiragongo',3,1,80);
INSERT INTO "gallery_galleryitem" VALUES(4,'2026-08-13 16:18:20.400698','2026-08-13 16:18:20.400750','Photo 4 — Activité de distribution de cash, Nyiragongo',4,1,81);
INSERT INTO "gallery_galleryitem" VALUES(5,'2026-08-13 16:18:20.502716','2026-08-13 16:18:20.502760','Photo 5 — Activité de distribution de cash, Nyiragongo',5,1,82);
INSERT INTO "gallery_galleryitem" VALUES(6,'2026-08-13 16:18:20.589394','2026-08-13 16:18:20.589442','Photo 6 — Activité de distribution de cash, Nyiragongo',6,1,83);
INSERT INTO "gallery_galleryitem" VALUES(7,'2026-08-13 16:18:20.702814','2026-08-13 16:18:20.702855','Photo 7 — Activité de distribution de cash, Nyiragongo',7,1,84);
INSERT INTO "gallery_galleryitem" VALUES(8,'2026-08-13 16:26:16.065399','2026-08-13 16:26:16.065431','Photo 1 — Activité du projet nutritionnel, Mudja',1,2,85);
INSERT INTO "gallery_galleryitem" VALUES(9,'2026-08-13 16:26:16.163662','2026-08-13 16:26:16.163712','Photo 2 — Activité du projet nutritionnel, Mudja',2,2,86);
INSERT INTO "gallery_galleryitem" VALUES(10,'2026-08-13 16:26:16.320835','2026-08-13 16:26:16.320889','Photo 3 — Activité du projet nutritionnel, Mudja',3,2,87);
INSERT INTO "gallery_galleryitem" VALUES(11,'2026-08-13 16:26:16.407226','2026-08-13 16:26:16.407253','Photo 4 — Activité du projet nutritionnel, Mudja',4,2,79);
INSERT INTO "gallery_galleryitem" VALUES(12,'2026-08-13 16:26:16.509175','2026-08-13 16:26:16.509214','Photo 5 — Activité du projet nutritionnel, Mudja',5,2,88);
CREATE TABLE "media_mediacategory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "slug" varchar(120) NOT NULL UNIQUE);
INSERT INTO "media_mediacategory" VALUES(1,'Import WordPress','import-wordpress');
CREATE TABLE "media_mediaitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "file" varchar(100) NOT NULL, "kind" varchar(20) NOT NULL, "title" varchar(200) NOT NULL, "description" text NOT NULL, "alt_text" varchar(300) NOT NULL, "checksum" varchar(64) NOT NULL UNIQUE, "width" integer unsigned NULL CHECK ("width" >= 0), "height" integer unsigned NULL CHECK ("height" >= 0), "source_url" varchar(200) NOT NULL, "taken_at" datetime NULL, "category_id" bigint NULL REFERENCES "media_mediacategory" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "media_mediaitem" VALUES(1,'2026-08-13 10:15:04.220035','2026-08-13 10:15:04.220171','media/2026/08/wp/2026/08/img-20241215-wa00683347026291772110706.jpg','image','img-20241215-wa00683347026291772110706','','','88cd27414cbef038219747dbeb138772d754eb7800d6572f53c303644af0dba4',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2024/12/img-20241215-wa00683347026291772110706.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(2,'2026-08-13 10:15:06.166365','2026-08-13 10:15:06.166486','media/2026/08/wp/2026/08/1000566679.jpg','image','1000566679','','','e191dbcbecfc86865802264918815578ba627cdbf227546d17e7b142667b8d1c',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2024/12/1000566679.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(3,'2026-08-13 10:15:07.463950','2026-08-13 10:15:07.464036','media/2026/08/wp/2026/08/1000566685.jpg','image','1000566685','','','89733bfb00055e1e9e7ce003361f39471b358e46df00ce7b8bd78459db477370',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2024/12/1000566685.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(4,'2026-08-13 10:15:08.941460','2026-08-13 10:15:08.941561','media/2026/08/wp/2026/08/phhistorique.jpg','image','phhistorique','','','178386eba1312fe46bf9274439196ee38bf2a30590f88cb0333708d9c053297f',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2024/12/phhistorique.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(5,'2026-08-13 10:15:13.514580','2026-08-13 10:15:13.514640','media/2026/08/wp/2026/08/img-20260506-wa01951393631366409934374.jpg','image','img-20260506-wa01951393631366409934374','','','d71b027614818b6c83aab14fd122624993761cd064f59dd9d92e156c373ffa18',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa01951393631366409934374.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(6,'2026-08-13 10:15:15.397227','2026-08-13 10:15:15.397304','media/2026/08/wp/2026/08/img-20260506-wa02016162214566291000200.jpg','image','img-20260506-wa02016162214566291000200','','','9b10e546a7df3363167998013eb71a48b1afe3c8a811b8e578c51e30c8fd40fd',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa02016162214566291000200.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(7,'2026-08-13 10:15:17.315248','2026-08-13 10:15:17.315312','media/2026/08/wp/2026/08/img-20260506-wa02028497312733879524573.jpg','image','img-20260506-wa02028497312733879524573','','','a31482985a7814b7a9636f85645acf16dcb05e1142cb0132f323a9d91582ca3f',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa02028497312733879524573.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(8,'2026-08-13 10:15:19.461573','2026-08-13 10:15:19.461673','media/2026/08/wp/2026/08/img-20260506-wa02155240100164919600901.jpg','image','img-20260506-wa02155240100164919600901','','','aa70a7bd14dceb32e4d6732707f8d1e33684c5b291a509b00701c74d9060987b',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa02155240100164919600901.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(9,'2026-08-13 10:15:21.099368','2026-08-13 10:15:21.099432','media/2026/08/wp/2026/08/img-20260506-wa0219633882165674383537.jpg','image','img-20260506-wa0219633882165674383537','','','15c873fed15fed136f7c172717f05b935b1365f1311468e6de6604d347ab2df3',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa0219633882165674383537.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(10,'2026-08-13 10:15:22.510339','2026-08-13 10:15:22.510401','media/2026/08/wp/2026/08/img-20260506-wa02368322511235557893179.jpg','image','img-20260506-wa02368322511235557893179','','','92f5d0cb066cf5c6579bd02c4c1f25906adc6b414330cb1529bb0ff9ee4a1c08',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa02368322511235557893179.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(11,'2026-08-13 10:15:24.170746','2026-08-13 10:15:24.170853','media/2026/08/wp/2026/08/img-20260506-wa02381970975820798064068.jpg','image','img-20260506-wa02381970975820798064068','','','25a8b21068c4ac99f9084377bb9477cc55c109d3a2284493f04764e0d27562bd',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa02381970975820798064068.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(12,'2026-08-13 10:15:26.136119','2026-08-13 10:15:26.136213','media/2026/08/wp/2026/08/img-20260506-wa03403213233309520412375.jpg','image','img-20260506-wa03403213233309520412375','','','aa99928091bd66397c0a0b800822dd0fa7619287a7069295c45a4ee12e867414',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa03403213233309520412375.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(13,'2026-08-13 10:15:27.891509','2026-08-13 10:15:27.891584','media/2026/08/wp/2026/08/img-20260506-wa03412751445177144991600.jpg','image','img-20260506-wa03412751445177144991600','','','0ddb4af141f2b7a6694719b082a7e565a8ee83d86a61393d5b8f3c9327391cec',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa03412751445177144991600.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(14,'2026-08-13 10:15:31.035423','2026-08-13 10:15:31.035508','media/2026/08/wp/2026/08/img-20260506-wa03436060045968838187555.jpg','image','img-20260506-wa03436060045968838187555','','','47f1d524f15db50901a754a0fc864ec1f35e2233fed04ca78bd34c2ce18fcd29',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa03436060045968838187555.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(15,'2026-08-13 10:15:32.834444','2026-08-13 10:15:32.834512','media/2026/08/wp/2026/08/img-20260506-wa03445546494334624814394.jpg','image','img-20260506-wa03445546494334624814394','','','eddc240a90ade7a3c2f630a3e533f2b57fe3c06bd79d68f659e466cd2692dd4d',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa03445546494334624814394.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(16,'2026-08-13 10:15:34.562585','2026-08-13 10:15:34.562715','media/2026/08/wp/2026/08/img-20260506-wa03465002223706886785688.jpg','image','img-20260506-wa03465002223706886785688','','','86da98a58891d0869f8a844dc3e9f88eac82dad3ec6ee6727a3538c78f489c15',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2026/05/img-20260506-wa03465002223706886785688.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(17,'2026-08-13 10:15:36.758978','2026-08-13 10:15:36.759020','media/2026/08/wp/2026/08/screenshot_20250918-042110_allpdfreader8920617283398532784.jpg','image','screenshot_20250918-042110_allpdfreader8920617283398532784','','','2ea6d1c59c02392a10fb3936df26708b233c9f95ad8d0403b2bd816985b84e03',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/09/screenshot_20250918-042110_allpdfreader8920617283398532784.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(18,'2026-08-13 10:15:38.379603','2026-08-13 10:15:38.379690','media/2026/08/wp/2026/08/screenshot_20250918-042159_allpdfreader2292687892584294550.jpg','image','screenshot_20250918-042159_allpdfreader2292687892584294550','','','04947792f6d1874ced8a02a7c2ce4ce1c0ed612f7facf417aa85d71e64000642',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/09/screenshot_20250918-042159_allpdfreader2292687892584294550.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(19,'2026-08-13 10:15:40.204598','2026-08-13 10:15:40.204685','media/2026/08/wp/2026/08/screenshot_20250918-042226_allpdfreader16602280780433668.jpg','image','screenshot_20250918-042226_allpdfreader16602280780433668','','','cb7e69694d27ad65a69755803ab1f9d7c680e74a8c9420bc4390418a12a6bed3',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/09/screenshot_20250918-042226_allpdfreader16602280780433668.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(20,'2026-08-13 10:15:42.281742','2026-08-13 10:15:42.281810','media/2026/08/wp/2026/08/screenshot_20250918-042328_allpdfreader6477029220414693507.jpg','image','screenshot_20250918-042328_allpdfreader6477029220414693507','','','e423a6a637690f56c94d8202ca44deda20bdb39f16d2097214457b5004accc6f',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/09/screenshot_20250918-042328_allpdfreader6477029220414693507.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(21,'2026-08-13 10:15:44.340832','2026-08-13 10:15:44.340964','media/2026/08/wp/2026/08/1742845457350571329581381628336.jpg','image','1742845457350571329581381628336','','','7793ea7ff7d56f9efe92dd1d6f24f7267f6a472c9390c88114a344d659da2a4d',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/1742845457350571329581381628336.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(22,'2026-08-13 10:15:45.862009','2026-08-13 10:15:45.862043','media/2026/08/wp/2026/08/17428454848146172090732852265988.jpg','image','17428454848146172090732852265988','','','40d5b9446c205011fb2d8adb75582a0ff32fd55c39bfe4ad2372a87b4468ed4e',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/17428454848146172090732852265988.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(23,'2026-08-13 10:15:47.330778','2026-08-13 10:15:47.330852','media/2026/08/wp/2026/08/17459985047933610022980594444200.jpg','image','17459985047933610022980594444200','','','e051c7ac50c6b9486d8bf68e59e4606b17afd41655c3a6a5855d1028315f1845',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/17459985047933610022980594444200.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(24,'2026-08-13 10:15:48.880546','2026-08-13 10:15:48.880830','media/2026/08/wp/2026/08/1745998514337340925539926636663.jpg','image','1745998514337340925539926636663','','','6136efec7fe299c3ccc0b1dcb5631d71a6384e7e9082bd970a0c562511428c8f',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/1745998514337340925539926636663.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(25,'2026-08-13 10:15:50.427538','2026-08-13 10:15:50.427566','media/2026/08/wp/2026/08/17558486773284954862579276484696.jpg','image','17558486773284954862579276484696','','','431e346c25d2c578cb59bb31470056e873a3559175d13403773215344da6c766',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/17558486773284954862579276484696.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(26,'2026-08-13 10:15:52.018371','2026-08-13 10:15:52.018414','media/2026/08/wp/2026/08/20250607_1446455337410690804642272.jpg','image','20250607_1446455337410690804642272','','','80120e5722bc0a908fb2c0d11b6c2d15ee5e1ca19c97f76b2b019032fb2a8e98',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/20250607_1446455337410690804642272.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(27,'2026-08-13 10:15:53.458312','2026-08-13 10:15:53.458352','media/2026/08/wp/2026/08/img-20250805-wa01627097002993674100660.jpg','image','img-20250805-wa01627097002993674100660','','','b791c03ff5af85d7ca897ddfa2e2799fad4c584694d49698990f2ffee78b521b',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img-20250805-wa01627097002993674100660.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(28,'2026-08-13 10:15:54.941143','2026-08-13 10:15:54.941177','media/2026/08/wp/2026/08/img-20250830-wa00422053147038746002351.jpg','image','img-20250830-wa00422053147038746002351','','','28dc3f1fcead90dc773b764f716d27a41a9632c86e1a3de2413dee569cff224f',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img-20250830-wa00422053147038746002351.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(29,'2026-08-13 10:15:56.468146','2026-08-13 10:15:56.468210','media/2026/08/wp/2026/08/img-20250830-wa00531461900489581247822.jpg','image','img-20250830-wa00531461900489581247822','','','21279635eb937db1b80daf8ff9d3c2e4752d25b71210adb563a78820f5002285',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img-20250830-wa00531461900489581247822.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(30,'2026-08-13 10:15:58.088083','2026-08-13 10:15:58.088141','media/2026/08/wp/2026/08/img-20250830-wa00563139045169594564033.jpg','image','img-20250830-wa00563139045169594564033','','','4cdfa35858bf762ef789dd4e762625feb2ef351428f348bddb90181a35b5ed26',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img-20250830-wa00563139045169594564033.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(31,'2026-08-13 10:15:59.835167','2026-08-13 10:15:59.835223','media/2026/08/wp/2026/08/img-20250910-wa03073254836903788807763.jpg','image','img-20250910-wa03073254836903788807763','','','e7a592719d496be3d06727c6ec6dcb782fbe8bfb66c6c74c435a701548b64f8e',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img-20250910-wa03073254836903788807763.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(32,'2026-08-13 10:16:01.392098','2026-08-13 10:16:01.392166','media/2026/08/wp/2026/08/img-20250910-wa03081213545354360873965.jpg','image','img-20250910-wa03081213545354360873965','','','e728b873d4d52fe553518e97f28e3c130d2241c325a8bfbd075dedb5829225b3',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img-20250910-wa03081213545354360873965.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(33,'2026-08-13 10:16:03.005692','2026-08-13 10:16:03.005759','media/2026/08/wp/2026/08/img-20250916-wa01956780040587762343153.jpg','image','img-20250916-wa01956780040587762343153','','','f37e6be13ee75c320a04d5e4374c5b580201eaf8f392ee3cda88e05f1a7d8a4e',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img-20250916-wa01956780040587762343153.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(34,'2026-08-13 10:16:04.223991','2026-08-13 10:16:04.224036','media/2026/08/wp/2026/08/img-20250916-wa01963484513572074990243.jpg','image','img-20250916-wa01963484513572074990243','','','eefc649b44661e0c3062be23cf9a8270f7b548d8f2a353cbf050c1d84cc60bc1',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img-20250916-wa01963484513572074990243.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(35,'2026-08-13 10:16:05.701549','2026-08-13 10:16:05.701610','media/2026/08/wp/2026/08/img-20250916-wa01981898577822918181262.jpg','image','img-20250916-wa01981898577822918181262','','','76e71390d619f9658d5f92d1127bcb1d8e3f32dbd5fc21862ada74efdbb64ea4',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img-20250916-wa01981898577822918181262.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(36,'2026-08-13 10:16:07.237115','2026-08-13 10:16:07.237195','media/2026/08/wp/2026/08/img-20250916-wa01995318309058408762202.jpg','image','img-20250916-wa01995318309058408762202','','','bd9982e51a315f5779da82fa27fac939718598ee3310fd6955769ad845147cfb',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img-20250916-wa01995318309058408762202.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(37,'2026-08-13 10:16:09.302051','2026-08-13 10:16:09.302086','media/2026/08/wp/2026/08/img_20250104_1305463341567229702749640.jpg','image','img_20250104_1305463341567229702749640','','','ac7f0e8cb563a9054625ab76c46e604b912997abdb11c4b41f87d1560ed4016f',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/img_20250104_1305463341567229702749640.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(38,'2026-08-13 10:16:10.823475','2026-08-13 10:16:10.823517','media/2026/08/wp/2026/08/messenger_creation_88806711286366136601049797752379667.jpeg','image','messenger_creation_88806711286366136601049797752379667','','','9326548a5b62ef65c8665ef1077b3215f4c5ca1843c8d552699fda59c47d5763',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/messenger_creation_88806711286366136601049797752379667.jpeg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(39,'2026-08-13 10:16:12.121189','2026-08-13 10:16:12.121248','media/2026/08/wp/2026/08/messenger_creation_a3a3c1b7-381c-495c-b89b-f7026dafa2777146830_0M0lMGW.jpeg','image','messenger_creation_a3a3c1b7-381c-495c-b89b-f7026dafa2777146830329812191226','','','8a6f113198c42454d3ca50d08b5dbdb8d87ac23238cc3ff5f539ceecbe46848e',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/messenger_creation_a3a3c1b7-381c-495c-b89b-f7026dafa2777146830329812191226.jpeg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(40,'2026-08-13 10:16:13.549494','2026-08-13 10:16:13.549554','media/2026/08/wp/2026/08/screenshot_20250612-103913_allpdfreader5778086046821372944.jpg','image','screenshot_20250612-103913_allpdfreader5778086046821372944','','','7d155cda9a027858c4adf3c4ff6d473343a8a1f28f03076ef73a5ac0d771dbd1',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/07/screenshot_20250612-103913_allpdfreader5778086046821372944.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(41,'2026-08-13 10:16:16.250336','2026-08-13 10:16:16.250404','media/2026/08/wp/2026/08/17486509447393762670018825719022.jpg','image','17486509447393762670018825719022','','','05da7620e73d669efb44138db09d3c0d4eca6932fb49ff54af907ef35a2187a1',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/17486509447393762670018825719022.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(42,'2026-08-13 10:16:17.880094','2026-08-13 10:16:17.880169','media/2026/08/wp/2026/08/17486509867461484831157422268935.jpg','image','17486509867461484831157422268935','','','82ec53c13965ebd63a5f2d76394a8f62fadd16796c4177a8176f7c561f665ddd',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/17486509867461484831157422268935.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(43,'2026-08-13 10:16:19.493831','2026-08-13 10:16:19.493895','media/2026/08/wp/2026/08/17486510048671244758245769843434.jpg','image','17486510048671244758245769843434','','','3fafc34611503ac1f5e1814f26d300bf3e800e018f26455dc8c9f72d511b8b98',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/17486510048671244758245769843434.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(44,'2026-08-13 10:16:20.805887','2026-08-13 10:16:20.805983','media/2026/08/wp/2026/08/17486510645782090586428310662383.jpg','image','17486510645782090586428310662383','','','6cd07b8b4e84a583508a807cc265655bb2c139e3a6017e8dc881f0c9de962d31',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/17486510645782090586428310662383.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(45,'2026-08-13 10:16:22.640120','2026-08-13 10:16:22.640204','media/2026/08/wp/2026/08/20250607_1507176236056726197115682.jpg','image','20250607_1507176236056726197115682','','','ac3d24fae54e896fcaa30eb78a8e4f94b1bcd5ed4696f0be51a6c0d128aa91cd',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/20250607_1507176236056726197115682.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(46,'2026-08-13 10:16:24.374325','2026-08-13 10:16:24.374392','media/2026/08/wp/2026/08/20250607_1511337610400258125782750.jpg','image','20250607_1511337610400258125782750','','','b6bd89fadb12ccea6a7cc71d48b2a6188dd5312f6ea5943b4284234dc299afbe',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/20250607_1511337610400258125782750.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(47,'2026-08-13 10:16:26.382570','2026-08-13 10:16:26.382620','media/2026/08/wp/2026/08/20250607_151836796568189709966243.jpg','image','20250607_151836796568189709966243','','','3a370207acb96d26e7952d640c30cb27410957ae4078b29a96d424dd2c06849b',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/20250607_151836796568189709966243.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(48,'2026-08-13 10:16:27.732261','2026-08-13 10:16:27.732334','media/2026/08/wp/2026/08/images-144084199170270482493.jpg','image','images-144084199170270482493','','','0ffcd90fc7351a7a9c641a60d1cfe53e1731fa4bfcacf08e49b6f48715c32478',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/images-144084199170270482493.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(49,'2026-08-13 10:16:29.109336','2026-08-13 10:16:29.109681','media/2026/08/wp/2026/08/img-20250523-wa0141222926321828171613.jpg','image','img-20250523-wa0141222926321828171613','','','d8edbda1d49d9818fe1e7ce04cad47257095c4bbbcf07c93c38a616a141e9f14',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250523-wa0141222926321828171613.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(50,'2026-08-13 10:16:31.345222','2026-08-13 10:16:31.345387','media/2026/08/wp/2026/08/17474142968685918074515064676847.jpg','image','17474142968685918074515064676847','','','b8f3fcbe0b5eebced372f58c851f00b0aa424321abfa2d6ea19971dea2bbb4c9',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/17474142968685918074515064676847.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(51,'2026-08-13 10:16:32.906956','2026-08-13 10:16:32.907053','media/2026/08/wp/2026/08/img-20250512-wa01118383869258837182857.jpg','image','img-20250512-wa01118383869258837182857','','','1241b791f77af90f339859142e236b285955acdc6256716f25624a48d1902729',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250512-wa01118383869258837182857.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(52,'2026-08-13 10:16:34.504771','2026-08-13 10:16:34.504873','media/2026/08/wp/2026/08/img-20250512-wa01136174425786015489728.jpg','image','img-20250512-wa01136174425786015489728','','','58bb72490895a7a0aeed9816a1e8c01c63214ba9660bc83fd6fb241e153e96d3',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250512-wa01136174425786015489728.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(53,'2026-08-13 10:16:36.145597','2026-08-13 10:16:36.145714','media/2026/08/wp/2026/08/img-20250526-wa00105837685643869570860.jpg','image','img-20250526-wa00105837685643869570860','','','0b46106d028342a37a2111a6b95979ab2f993d9952defc7ae3788e51e513867d',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250526-wa00105837685643869570860.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(54,'2026-08-13 10:16:37.798467','2026-08-13 10:16:37.798538','media/2026/08/wp/2026/08/img-20250526-wa00172200971259058324818.jpg','image','img-20250526-wa00172200971259058324818','','','12e804ae6ffb35188d6e76d148dbbd961cd4edc642b2db23a63257e8877ca516',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250526-wa00172200971259058324818.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(55,'2026-08-13 10:16:39.440478','2026-08-13 10:16:39.440536','media/2026/08/wp/2026/08/img-20250602-wa00721404359030771124198.jpg','image','img-20250602-wa00721404359030771124198','','','25501c604f71133c44c1841aa240c8fb23e4cd62cdbb5275da4788d1a383c0b1',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250602-wa00721404359030771124198.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(56,'2026-08-13 10:16:41.122134','2026-08-13 10:16:41.122274','media/2026/08/wp/2026/08/img-20250602-wa00746434878816712837539.jpg','image','img-20250602-wa00746434878816712837539','','','7c22de4aba44b16a32bdb615984b20c53ebad0bc617b2ddb800dcf345e76737b',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250602-wa00746434878816712837539.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(57,'2026-08-13 10:16:42.735096','2026-08-13 10:16:42.735158','media/2026/08/wp/2026/08/img-20250602-wa00762706476337958274775.jpg','image','img-20250602-wa00762706476337958274775','','','d2c2c5d798bf8a6df87c865febb7d5ef0e7004cd093bc5da14ca82ada20536d9',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250602-wa00762706476337958274775.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(58,'2026-08-13 10:16:44.189645','2026-08-13 10:16:44.189813','media/2026/08/wp/2026/08/screenshot_20250528-015417_allpdfreader6755130329156372865.jpg','image','screenshot_20250528-015417_allpdfreader6755130329156372865','','','fa3c70217ac7e60532e44f26c4c67f8cea63324be6eaddcc3f98e116aac40e17',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/screenshot_20250528-015417_allpdfreader6755130329156372865.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(59,'2026-08-13 10:16:45.808381','2026-08-13 10:16:45.808435','media/2026/08/wp/2026/08/screenshot_20250528-024125_allpdfreader3833799926878037949.jpg','image','screenshot_20250528-024125_allpdfreader3833799926878037949','','','bf7745953bfcb0170428ec1cc58a9a6f054300bec835c9138aac054292dba02a',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/screenshot_20250528-024125_allpdfreader3833799926878037949.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(60,'2026-08-13 10:16:47.582964','2026-08-13 10:16:47.583016','media/2026/08/wp/2026/08/screenshot_20250528-024150_allpdfreader4829083458068890546.jpg','image','screenshot_20250528-024150_allpdfreader4829083458068890546','','','fb2ff00d911f2f58ad412f3bca2553dc9a437359e0882a565482580bce0f63ac',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/screenshot_20250528-024150_allpdfreader4829083458068890546.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(61,'2026-08-13 10:16:49.266968','2026-08-13 10:16:49.267053','media/2026/08/wp/2026/08/screenshot_20250528-024222_allpdfreader7600737550913901488.jpg','image','screenshot_20250528-024222_allpdfreader7600737550913901488','','','530351885ed437c44031ec386ef9b83b314a651c4cf385350eda29f78300434d',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/screenshot_20250528-024222_allpdfreader7600737550913901488.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(62,'2026-08-13 10:16:51.458876','2026-08-13 10:16:51.458931','media/2026/08/wp/2026/08/img-20250523-wa01454190386095213270707.jpg','image','img-20250523-wa01454190386095213270707','','','67efc6df7f43bc23917586b3aa520d155504ae5eaf24a5040989a3ce19c796f5',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250523-wa01454190386095213270707.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(63,'2026-08-13 10:16:53.435684','2026-08-13 10:16:53.435719','media/2026/08/wp/2026/08/img-20250523-wa01503776728102908662145.jpg','image','img-20250523-wa01503776728102908662145','','','b44d903c1b66b5cc297405e567b7ff76bc3f9b599dcd740d1b6b57169f468bfa',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250523-wa01503776728102908662145.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(64,'2026-08-13 10:16:55.242275','2026-08-13 10:16:55.242331','media/2026/08/wp/2026/08/img-20250523-wa01554808910707710625529.jpg','image','img-20250523-wa01554808910707710625529','','','f84795d09f5b8e9df876a7229e1cff957220c490b9d87db3734f17682ba0b3b1',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250523-wa01554808910707710625529.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(65,'2026-08-13 10:16:57.684815','2026-08-13 10:16:57.684878','media/2026/08/wp/2026/08/img-20250805-wa01515668812181185078001.jpg','image','img-20250805-wa01515668812181185078001','','','2faa5716b000d88d0a8014a69870a49c2984b86b83742d7c531245abadf5d98e',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250805-wa01515668812181185078001.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(66,'2026-08-13 10:16:59.106607','2026-08-13 10:16:59.106700','media/2026/08/wp/2026/08/img-20250805-wa01543281009616049951436.jpg','image','img-20250805-wa01543281009616049951436','','','10f30143d4b3800c6df5564d2032f4305880143dbd4fb57b9e5fa049cd34eb3f',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250805-wa01543281009616049951436.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(67,'2026-08-13 10:17:00.585195','2026-08-13 10:17:00.585235','media/2026/08/wp/2026/08/img-20250805-wa01579084261201756904707.jpg','image','img-20250805-wa01579084261201756904707','','','8531abbd00e7845546a2a068ac2873a9f9c99c5d531dc78c51cc8be2bf9ac8b8',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250805-wa01579084261201756904707.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(68,'2026-08-13 10:17:01.853525','2026-08-13 10:17:01.853582','media/2026/08/wp/2026/08/messenger_creation_7e982e81-cc97-4caa-9ba9-1033af4e961d8576736_JK2baU8.jpeg','image','messenger_creation_7e982e81-cc97-4caa-9ba9-1033af4e961d8576736750867150698','','','fcbed96eecfc5d81308890ac2d2b39863dbaec72b3b6e499da0b35d950979d07',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/messenger_creation_7e982e81-cc97-4caa-9ba9-1033af4e961d8576736750867150698.jpeg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(69,'2026-08-13 10:17:03.448079','2026-08-13 10:17:03.448156','media/2026/08/wp/2026/08/messenger_creation_9cfbf2af-2a94-485a-8684-74605e63c62d1104606_2kGtRvc.jpeg','image','messenger_creation_9cfbf2af-2a94-485a-8684-74605e63c62d1104606749245048736','','','75219de6c25051a06e1100a82fbb6fa39aa0088775f6dbca7853ce8e02e2c9aa',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/messenger_creation_9cfbf2af-2a94-485a-8684-74605e63c62d1104606749245048736.jpeg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(70,'2026-08-13 10:17:05.258234','2026-08-13 10:17:05.258281','media/2026/08/wp/2026/08/screenshot_20250806-180054_gallery2997741796954331103.jpg','image','screenshot_20250806-180054_gallery2997741796954331103','','','2925dca5b04431d0089b797fae4efa915f062408feb0f9392e617b2740c4e598',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/screenshot_20250806-180054_gallery2997741796954331103.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(71,'2026-08-13 10:17:07.279588','2026-08-13 10:17:07.279616','media/2026/08/wp/2026/08/img-20250516-wa0081261469961774322770.jpg','image','img-20250516-wa0081261469961774322770','','','22fe2b90128dd4c169456b610bdb500f05483207dbec3e491a855ab7a5e64586',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250516-wa0081261469961774322770.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(72,'2026-08-13 10:17:08.751636','2026-08-13 10:17:08.751684','media/2026/08/wp/2026/08/img-20250516-wa0082492460727698598290.jpg','image','img-20250516-wa0082492460727698598290','','','95dbe89c5885fe9f0b515cf98942baca8569606e66413c56cbd95c355c478318',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2025/05/img-20250516-wa0082492460727698598290.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(73,'2026-08-13 10:17:11.111541','2026-08-13 10:17:11.111569','media/2026/08/wp/2026/08/17459985616232594201096817036247.jpg','image','17459985616232594201096817036247','','','5377da03ec8017f95970b08e1fd36dfcd1f72cb157815251281dbe2937664e4e',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2024/12/17459985616232594201096817036247.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(74,'2026-08-13 10:17:12.772600','2026-08-13 10:17:12.772648','media/2026/08/wp/2026/08/img-20241215-wa00592900465635429704277.jpg','image','img-20241215-wa00592900465635429704277','','','4787bf83e6f169183997b40404236701a74e8e979b8ba88ffc4cfb8c90901e92',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2024/12/img-20241215-wa00592900465635429704277.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(75,'2026-08-13 10:17:14.019043','2026-08-13 10:17:14.019117','media/2026/08/wp/2026/08/img-20241215-wa00615161243459594582671.jpg','image','img-20241215-wa00615161243459594582671','','','3446accb0e1073d5d57577c1f24653fc8e487adeb8da4cc6da6212243d658155',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2024/12/img-20241215-wa00615161243459594582671.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(76,'2026-08-13 10:17:16.217257','2026-08-13 10:17:16.217324','media/2026/08/wp/2026/08/img-20241215-wa00704925568464169999774.jpg','image','img-20241215-wa00704925568464169999774','','','6386344c31a34140725dea70e9df44d2dec6d854dde9431883c1e205c99dfffe',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2024/12/img-20241215-wa00704925568464169999774.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(77,'2026-08-13 10:17:18.442329','2026-08-13 10:17:18.442373','media/2026/08/wp/2026/08/1000566683.jpg','image','1000566683','','','d1600e27f5aa1c11975b83408c4c131337f47f9c66b5d580616612a4a6da2647',NULL,NULL,'https://citedelamisericorde.wordpress.com/wp-content/uploads/2024/12/1000566683.jpg',NULL,1);
INSERT INTO "media_mediaitem" VALUES(78,'2026-08-13 16:17:48.818329','2026-08-13 16:17:48.818472','media/2026/08/activite-femmes-nyiragongo/1786633035372.jpg','image','Autonomisation des femmes autochtones à Nyiragongo — photo 1','','Activité de la Cité de la Miséricorde à Nyiragongo','2c1f6bcac59e3362d848ca69f0b735de199cfc85414064ec95eee34fa6d23d88',1280,960,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(79,'2026-08-13 16:17:48.996372','2026-08-13 16:17:48.996405','media/2026/08/activite-femmes-nyiragongo/1786633357838.jpg','image','Autonomisation des femmes autochtones à Nyiragongo — photo 2','','Activité de la Cité de la Miséricorde à Nyiragongo','cdb43d699d97428a0ca8c2b87afa9638d044f7f6a5accce810f7bfeb745d1d22',1280,960,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(80,'2026-08-13 16:17:49.118849','2026-08-13 16:17:49.118892','media/2026/08/activite-femmes-nyiragongo/IMG-20260813-WA0027.jpg','image','Autonomisation des femmes autochtones à Nyiragongo — photo 3','','Activité de la Cité de la Miséricorde à Nyiragongo','2a909498559ba4fdcb17ede06ded834c6d69987c62ea2fd0a17cc2ba88472c8e',960,540,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(81,'2026-08-13 16:17:49.318062','2026-08-13 16:17:49.318140','media/2026/08/activite-femmes-nyiragongo/IMG-20260813-WA0028.jpg','image','Autonomisation des femmes autochtones à Nyiragongo — photo 4','','Activité de la Cité de la Miséricorde à Nyiragongo','895361b8eeb99bd5376c41ebc46aaa504ca5e5c2566ba71a461ea8adaf895f52',960,540,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(82,'2026-08-13 16:17:49.496237','2026-08-13 16:17:49.496260','media/2026/08/activite-femmes-nyiragongo/IMG-20260813-WA0033.jpg','image','Autonomisation des femmes autochtones à Nyiragongo — photo 5','','Activité de la Cité de la Miséricorde à Nyiragongo','474165de7cc6bda24d4b239a90d9ff1a28dcdff65ae29ae34b1ba365e080b197',960,540,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(83,'2026-08-13 16:17:49.635959','2026-08-13 16:17:49.635979','media/2026/08/activite-femmes-nyiragongo/IMG-20260813-WA0036.jpg','image','Autonomisation des femmes autochtones à Nyiragongo — photo 6','','Activité de la Cité de la Miséricorde à Nyiragongo','9d9b1edbfaaf3243512c6e548816fd0163fa6a3f4728aa956c41437bde877fbc',960,540,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(84,'2026-08-13 16:17:49.780877','2026-08-13 16:17:49.780908','media/2026/08/activite-femmes-nyiragongo/IMG-20260813-WA0039.jpg','image','Autonomisation des femmes autochtones à Nyiragongo — photo 7','','Activité de la Cité de la Miséricorde à Nyiragongo','d030048020d15a88e65dafd82d913d1c0fce5f509bbe3912e2d0f220fed1f3d0',960,540,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(85,'2026-08-13 16:26:14.459501','2026-08-13 16:26:14.459534','media/2026/08/bilan-malnutrition-nyiragongo/1786632805802.jpg','image','Lutte contre la malnutrition à Mudja — photo 1','','Prise en charge nutritionnelle des enfants à Mudja (Nyiragongo)','f331cba14ab77d0dddd71494ff46cad3b45a70ed26dc5d1d0576a21b998c14f8',1280,960,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(86,'2026-08-13 16:26:14.649121','2026-08-13 16:26:14.649160','media/2026/08/bilan-malnutrition-nyiragongo/1786632905245.jpg','image','Lutte contre la malnutrition à Mudja — photo 2','','Prise en charge nutritionnelle des enfants à Mudja (Nyiragongo)','f6f06f0d946c17009ac4fe9ef457912e01b96d653ad1f933c5ee73c4a5de709b',1280,960,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(87,'2026-08-13 16:26:14.821611','2026-08-13 16:26:14.821640','media/2026/08/bilan-malnutrition-nyiragongo/1786632934252.jpg','image','Lutte contre la malnutrition à Mudja — photo 3','','Prise en charge nutritionnelle des enfants à Mudja (Nyiragongo)','95f5de038e93a3ff23dfa6964eb588d09e0ae69a94b3680ac7006c19036a555a',1430,1907,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(88,'2026-08-13 16:26:15.008459','2026-08-13 16:26:15.008506','media/2026/08/bilan-malnutrition-nyiragongo/IMG-20260804-WA0007.jpg','image','Lutte contre la malnutrition à Mudja — photo 5','','Prise en charge nutritionnelle des enfants à Mudja (Nyiragongo)','4c66cc9a07214417e1489b68c18763f4b7ec681ae20e3c104461aaa95337cfd4',756,1008,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(89,'2026-08-14 06:36:21.247471','2026-08-14 06:36:21.247527','media/2026/08/logo-adrns_MsUNfMl.png','image','Logo ADRNS','Logo de l''Association Développement Relations Nord-Sud, partenaire de la ferme-école agroécologique.','Logo ADRNS','13a1a0f52f914c49d71cd0452bc4f8030112a65baace4bc4c2220e40f219eeb1',NULL,NULL,'',NULL,NULL);
INSERT INTO "media_mediaitem" VALUES(90,'2026-08-14 14:58:22.869177','2026-08-14 14:58:22.869205','media/2026/08/statuts-cite-de-la-misericorde_errWqWS.pdf','document','Statuts de la Cité de la Miséricorde','Projet de statut de l''association (adopté à Bukavu le 12 février 2018).','','c0abe48281ae3687466caa2025792f8fb03951f4ea47e76b2cdac37e0c353ca0',NULL,NULL,'',NULL,NULL);
CREATE TABLE "migration_importedrecord" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "source_type" varchar(20) NOT NULL, "source_id" varchar(40) NOT NULL, "source_title" varchar(300) NOT NULL, "source_url" varchar(500) NOT NULL, "destination_model" varchar(100) NOT NULL, "destination_id" bigint unsigned NULL CHECK ("destination_id" >= 0), "status" varchar(20) NOT NULL, "notes" text NOT NULL, "run_id" bigint NOT NULL REFERENCES "migration_migrationrun" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "migration_importedrecord" VALUES(1,'2026-08-13 10:15:01.674471','2026-08-13 10:15:01.674580','page','177','MANASSE WEDDING','https://citedelamisericorde.wordpress.com/manasse-wedding/','',NULL,'SKIPPED','Contenu personnel (MANASSE WEDDING) — hors périmètre',7);
INSERT INTO "migration_importedrecord" VALUES(2,'2026-08-13 10:15:02.200533','2026-08-13 10:15:02.200622','page','91','CRÉATION D’UN CENTRE DE FORMATION PROFESSIONNEL EN FAVEUR DES ORPHELINS DE LA CITÉ DE LA MISÉRICORDE RDC','https://citedelamisericorde.wordpress.com/projets/','pages.Page',7,'IMPORTED','',7);
INSERT INTO "migration_importedrecord" VALUES(3,'2026-08-13 10:15:04.584690','2026-08-13 10:15:04.584833','page','1','CITE DE LA MISERICORDE','https://citedelamisericorde.wordpress.com/','pages.Page',8,'IMPORTED','',7);
INSERT INTO "migration_importedrecord" VALUES(4,'2026-08-13 10:15:09.297450','2026-08-13 10:15:09.297615','page','29','CTE DE LA MISERICORDE QUI SOMMES-NOUS?','https://citedelamisericorde.wordpress.com/historique/','pages.Page',9,'IMPORTED','',7);
INSERT INTO "migration_importedrecord" VALUES(5,'2026-08-13 10:15:35.171495','2026-08-13 10:15:35.171558','post','256','Lutte contre la malnutrition des enfants de moins de 10 ans — Nyiragongo','https://citedelamisericorde.wordpress.com/2026/05/07/projet-de-lutte-contre-la-malnutrition-aux-enfants-de-moin-de-10ans-dans-le-territoire-de-nyiragongonyiragongo-lorganisation-cite-de-la-misericorde-lance-un-programme-de-lutte-contre-la-mal/','articles.Article',1,'IMPORTED','Titre restructuré depuis le contenu (anomalie WP post 256) — à valider',7);
INSERT INTO "migration_importedrecord" VALUES(6,'2026-08-13 10:15:42.736785','2026-08-13 10:15:42.736843','post','209','PROJET DE CONTRIBUTION A LA STABILISATION ET AUTONOMISATION SOCIOECONOMIQUE DES SURVIVANTS DES VIOLENCES BASEES SUR LES GENRES EN REPUBLIQUE DEMOCRATIQUE DU CONGO','https://citedelamisericorde.wordpress.com/2025/09/13/projet-de-contribution-a-la-stabilisation-et-autonomisation-socioecinomique-des-survivants-des-violences-basees-sur-les-genres-en-republique-democratique-du-congo/','articles.Article',2,'IMPORTED','',7);
INSERT INTO "migration_importedrecord" VALUES(7,'2026-08-13 10:16:14.444187','2026-08-13 10:16:14.444267','post','170','SAUVER L’ORPHELINAT PAR UN DON','https://citedelamisericorde.wordpress.com/2025/07/03/appel-au-don-sos-orphelinat/','articles.Article',3,'IMPORTED','',7);
INSERT INTO "migration_importedrecord" VALUES(8,'2026-08-13 10:16:29.612777','2026-08-13 10:16:29.612815','post','149','AMENAGEMENT CUISINE ORPHELINAT','https://citedelamisericorde.wordpress.com/2025/05/31/amenagement-cuisine-orphelinat/','articles.Article',4,'IMPORTED','',7);
INSERT INTO "migration_importedrecord" VALUES(9,'2026-08-13 10:16:49.895252','2026-08-13 10:16:49.895272','post','128','PROJET D’IMPLANTATION D’UNE FERME AGRO-ÉCOLOGIQUE- Projet Exécuté par L’Association Collectif des Jeunes pour la Paix et le Développement/CJPD CONGO Asbl','https://citedelamisericorde.wordpress.com/2025/05/28/projet-dimplantation-dune-ferme-agro-ecologique-projet-execute-par-lassociation-collectif-des-jeunes-pour-la-paix-et-le-developpement-cjpd-congo-asbl/','articles.Article',5,'IMPORTED','',7);
INSERT INTO "migration_importedrecord" VALUES(10,'2026-08-13 10:17:05.725565','2026-08-13 10:17:05.725623','post','126','UNE BONNE JOURNÉE S’ANNONCE.','https://citedelamisericorde.wordpress.com/2025/05/24/une-bonne-journee-sannonce/','articles.Article',6,'IMPORTED','',7);
INSERT INTO "migration_importedrecord" VALUES(11,'2026-08-13 10:17:09.521067','2026-08-13 10:17:09.521137','post','105','PROJET DE CRÉATION D’UN AIRE DES JEUX','https://citedelamisericorde.wordpress.com/2025/05/19/projet-de-creation-dun-aire-des-jeux/','articles.Article',7,'IMPORTED','',7);
INSERT INTO "migration_importedrecord" VALUES(12,'2026-08-13 10:17:16.691173','2026-08-13 10:17:16.691244','post','44','PROJET DE LA CRÉATION D’UN CENTRE DE FORMATION PROFESSIONNEL EN FAVEUR DES ORPHELINS DE L’ORPHELINAT CITÉ DE LA MISÉRICORDE EN RÉPUBLIQUE DÉMOCRATIQUE DU CONGO','https://citedelamisericorde.wordpress.com/2024/12/15/projet-de-la-creation-dun-centre-de-formation-professionnel-en-faveur-des-orphelins-de-lorphelinat-cite-de-la-misericorde-en-republique-democratique-du-congo/','articles.Article',8,'IMPORTED','',7);
INSERT INTO "migration_importedrecord" VALUES(13,'2026-08-13 10:17:18.963127','2026-08-13 10:17:18.963173','post','20','BIENVENUE SUR LA PAGE DE LA CITÉ DE LA MISÉRICORDE','https://citedelamisericorde.wordpress.com/2024/12/15/bienvenue-sur-la-page-de-la-cite-de-la-misericorde/','articles.Article',9,'IMPORTED','',7);
CREATE TABLE "migration_migrationrun" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "kind" varchar(20) NOT NULL, "started_at" datetime NOT NULL, "finished_at" datetime NULL, "status" varchar(20) NOT NULL, "log" text NOT NULL);
INSERT INTO "migration_migrationrun" VALUES(1,'2026-08-13 10:10:02.006348','2026-08-13 10:10:06.980018','audit','2026-08-13 10:10:02.006535','2026-08-13 10:10:06.979512','FAILED','HTTP 404 sur https://public-api.wordpress.com/rest/v1.1/sites/citedelamisericorde.wordpress.com/pages?number=50&page=1');
INSERT INTO "migration_migrationrun" VALUES(2,'2026-08-13 10:12:19.102021','2026-08-13 10:12:26.590105','audit','2026-08-13 10:12:19.102169','2026-08-13 10:12:26.589738','SUCCESS','{
  "site": "CITE DE LA MISERICORDE CONGO",
  "found": {
    "posts": 9,
    "pages": 4,
    "categories": 2,
    "tags": 6
  },
  "images": 78,
  "founder_hits": [
    "https://citedelamisericorde.wordpress.com/2026/05/07/projet-de-lutte-contre-la-malnutrition-aux-enfants-de-moin-de-10ans-dans-le-territoire-de-nyiragongonyiragongo-lorganisation-cite-de-la-misericorde-lance-un-programme-de-lutte-contre-la-mal/",
    "https://citedelamisericorde.wordpress.com/2025/07/03/appel-au-don-sos-orphelinat/",
    "https://citedelamisericorde.wordpress.com/2025/05/28/projet-dimplantation-dune-ferme-agro-ecologique-projet-execute-par-lassociation-collectif-des-jeunes-pour-la-paix-et-le-developpement-cjpd-congo-asbl/",
    "https://citedelamisericorde.wordpress.com/manasse-wedding/",
    "https://citedelamisericorde.wordpress.com/historique/"
  ]
}');
INSERT INTO "migration_migrationrun" VALUES(3,'2026-08-13 10:12:49.383127','2026-08-13 10:12:58.894163','audit','2026-08-13 10:12:49.383277','2026-08-13 10:12:58.892746','SUCCESS','{
  "site": "CITE DE LA MISERICORDE CONGO",
  "found": {
    "posts": 9,
    "pages": 4,
    "categories": 2,
    "tags": 6
  },
  "images": 78,
  "founder_hits": [
    "https://citedelamisericorde.wordpress.com/2026/05/07/projet-de-lutte-contre-la-malnutrition-aux-enfants-de-moin-de-10ans-dans-le-territoire-de-nyiragongonyiragongo-lorganisation-cite-de-la-misericorde-lance-un-programme-de-lutte-contre-la-mal/",
    "https://citedelamisericorde.wordpress.com/2025/07/03/appel-au-don-sos-orphelinat/",
    "https://citedelamisericorde.wordpress.com/2025/05/28/projet-dimplantation-dune-ferme-agro-ecologique-projet-execute-par-lassociation-collectif-des-jeunes-pour-la-paix-et-le-developpement-cjpd-congo-asbl/",
    "https://citedelamisericorde.wordpress.com/manasse-wedding/",
    "https://citedelamisericorde.wordpress.com/historique/"
  ]
}');
INSERT INTO "migration_migrationrun" VALUES(4,'2026-08-13 10:13:24.321472','2026-08-13 10:13:32.912148','audit','2026-08-13 10:13:24.321717','2026-08-13 10:13:32.911893','SUCCESS','{
  "site": "CITE DE LA MISERICORDE CONGO",
  "found": {
    "posts": 9,
    "pages": 4,
    "categories": 2,
    "tags": 6
  },
  "images": 78,
  "founder_hits": [
    "https://citedelamisericorde.wordpress.com/2026/05/07/projet-de-lutte-contre-la-malnutrition-aux-enfants-de-moin-de-10ans-dans-le-territoire-de-nyiragongonyiragongo-lorganisation-cite-de-la-misericorde-lance-un-programme-de-lutte-contre-la-mal/",
    "https://citedelamisericorde.wordpress.com/2025/07/03/appel-au-don-sos-orphelinat/",
    "https://citedelamisericorde.wordpress.com/2025/05/28/projet-dimplantation-dune-ferme-agro-ecologique-projet-execute-par-lassociation-collectif-des-jeunes-pour-la-paix-et-le-developpement-cjpd-congo-asbl/",
    "https://citedelamisericorde.wordpress.com/manasse-wedding/",
    "https://citedelamisericorde.wordpress.com/historique/"
  ]
}');
INSERT INTO "migration_migrationrun" VALUES(5,'2026-08-13 10:13:46.575858','2026-08-13 10:13:51.522526','import','2026-08-13 10:13:46.575972','2026-08-13 10:13:51.521971','SUCCESS','[page 177] MANASSE WEDDING -> pages:page_detail (slug: manasse-wedding)
[page 91] CRÉATION D’UN CENTRE DE FORMATION PROFESSIONNEL EN FAVEUR DES ORPHELINS DE LA CITÉ DE LA MISÉRICORDE RDC -> pages:page_detail (slug: projets)
[page 1] CITE DE LA MISERICORDE -> pages:page_detail (slug: about)
[page 29] CTE DE LA MISERICORDE QUI SOMMES-NOUS? -> pages:page_detail (slug: historique)
[post 256] PROJET DE LUTTE CONTRE LA MALNUTRITION AUX ENFANTS DE MOIN DE 10ANS DANS LE TERRITOIRE DE NYIRAGONGO l’organisation Cité de la Miséricorde lance un programme de lutte contre la malnutrition des enfantsL’organisation Collectif des jeunes pour la paix et le développement (CJPD Asbl) Cité de la Miséricorde a officiellement lancé, ce lundi 04 mai 2026, son programme de lutte contre la malnutrition et d’encadrement des enfants nécessiteux dans le groupement Mudja, en territoire de Nyiragongo, au Nord-Kivu.                   Cette initiative a pour objectif d’apporter une réponse concrète à la situation préoccupante de nombreux enfants victimes de malnutrition dans cette partie de la province.La cérémonie de lancement a réuni plusieurs autorités locales, cadres de base ainsi que des représentants du corps de santé venus s’informer des différentes activités prévues dans le cadre de ce projet humanitaire qui s’étendra sur une période d’une année avec possibilité de renouvellement.                     À travers cette action, l’organisation vise un accompagnement nutritionnel complet de 200 enfants âgés de moins de 10 ans.Pour cette occasion, l’organisation Cité de la Miséricorde a également présenté le site qui servira d’espace d’accueil et de prise en charge des enfants ciblés.                                      Cet espace devra garantir un cadre sécurisé et adapté aux besoins des bénéficiaires durant toute la période d’accompagnement.           Les responsables du projet indiquent que plusieurs activités d’encadrement nutritionnel et de suivi seront organisées afin de réduire les risques liés à la malnutrition infantile.Selon Manassée Kamole, coordonnateur national de l’organisation Cité de la Miséricorde, ce projet est le résultat d’un constat communautaire appuyé par des études réalisées par des experts sur la situation nutritionnelle des enfants dans le territoire de Nyiragongo.Manassée Kamole, coordonnateur national de l’organisation Cité de la MiséricordeIl explique que cette initiative répond à une urgence humanitaire qui nécessite l’implication de plusieurs acteurs.« C’est un projet que nous avons tant attendu et nous sommes heureux de le lancer aujourd’hui. C’est un projet qui nous permettra d’atténuer le taux de mortalité des enfants de moins de 10 ans. Nous avons vu que l’essentiel c’est de sauver ces enfants. Nous avons été heureux de rencontrer aujourd’hui les autorités locales et leur avons parlé de l’impact de notre projet, des résultats attendus et nous leur avons tendu la main puisque sans eux nous ne pouvons pas avancer.» a dit le coordonnateur de cette organisation.Profitant de cette occasion, Manassée Kamole a également lancé un appel aux partenaires et personnes de bonne volonté à soutenir cette initiative afin de renforcer les capacités de prise en charge des enfants vulnérables.                      Selon lui, les besoins restent énormes face au nombre croissant de cas de malnutrition enregistrés dans plusieurs villages du territoire de Nyiragongo.Du côté des autorités locales et des cadres de base, le lancement de ce programme a été accueilli avec satisfaction.     Plusieurs intervenants ont salué une initiative qui vient répondre à une préoccupation majeure des familles confrontées aux difficultés socio-économiques et à l’insécurité alimentaire persistante dans la région.C’est notamment le cas de monsieur Tegeya Byenda Adolphe, secrétaire exécutif du village Kiziba 1, qui représentait le chef de ce même village où seront accueillis les enfants bénéficiaires du projet.Tegeya Byenda Adolphe, secrétaire exécutif du village Kiziba 1Ce dernier a encouragé les parents à s’approprier cette initiative afin de permettre aux enfants concernés de bénéficier pleinement de cette prise en charge.« C’est à bras ouverts que nous avons accueilli ce projet car il vient en aide à nos enfants qui souffrent la malnutrition. Nous sommes contents et remercions Cité de la Miséricorde. Ici, nous avons plusieurs enfants malnutris; une initiative comme celle-ci et la bienvenue.                           Aux parents nous lançons un appel.                           Qu’ils disponibilisent leurs enfants pour qu’ils bénéficient de cette prise en charge. » a-t-il dit.Dans cette partie de la province du Nord-Kivu, la question de la malnutrition infantile demeure une préoccupation majeure pour les acteurs sanitaires et humanitaires.              Selon les données du Programme national de nutrition PRONANUT, la zone de santé de Nyiragongo figure parmi les zones qui notifient le plus de cas de malnutrition au Nord-Kivu.Face à cette réalité, l’initiative portée par l’organisation Cité de la Miséricorde apparaît comme un appui important aux efforts de protection des enfants vulnérables et de soutien aux familles en difficulté.                               Les responsables du projet espèrent, grâce à celui-ci, contribuer à l’amélioration des conditions de vie des enfants tout en sensibilisant la communauté sur l’importance de la nutrition et de la protection de l’enfance.Stoïcien Sky Lwembo -> articles:detail (slug: projet-de-lutte-contre-la-malnutrition-aux-enfants-de-moin-de-10ans-dans-le-territoire-de-nyiragongonyiragongo-lorganisation-cite-de-la-misericorde-lance-un-programme-de-lutte-contre-la-mal)
[post 209] PROJET DE CONTRIBUTION A LA STABILISATION ET AUTONOMISATION SOCIOECONOMIQUE DES SURVIVANTS DES VIOLENCES BASEES SUR LES GENRES EN REPUBLIQUE DEMOCRATIQUE DU CONGO -> articles:detail (slug: projet-de-contribution-a-la-stabilisation-et-autonomisation-socioecinomique-des-survivants-des-violences-basees-sur-les-genres-en-republique-democratique-du-congo)
[post 170] SAUVER L&#8217;ORPHELINAT PAR UN DON -> articles:detail (slug: appel-au-don-sos-orphelinat)
[post 149] AMENAGEMENT CUISINE ORPHELINAT -> articles:detail (slug: amenagement-cuisine-orphelinat)
[post 128] PROJET D&#8217;IMPLANTATION D&#8217;UNE FERME AGRO-ÉCOLOGIQUE- Projet Exécuté par L&#8217;Association Collectif des Jeunes pour la Paix et le Développement/CJPD CONGO Asbl -> articles:detail (slug: projet-dimplantation-dune-ferme-agro-ecologique-projet-execute-par-lassociation-collectif-des-jeunes-pour-la-paix-et-le-developpement-cjpd-congo-asbl)
[post 126] UNE BONNE JOURNÉE S&#8217;ANNONCE. -> articles:detail (slug: une-bonne-journee-sannonce)
[post 105] PROJET DE CRÉATION D’UN AIRE DES JEUX -> articles:detail (slug: projet-de-creation-dun-aire-des-jeux)
[post 44] PROJET DE LA CRÉATION D&#8217;UN CENTRE DE FORMATION PROFESSIONNEL EN FAVEUR DES ORPHELINS DE L&#8217;ORPHELINAT CITÉ DE LA MISÉRICORDE EN RÉPUBLIQUE DÉMOCRATIQUE DU CONGO -> articles:detail (slug: projet-de-la-creation-dun-centre-de-formation-professionnel-en-faveur-des-orphelins-de-lorphelinat-cite-de-la-misericorde-en-republique-democratique-du-congo)
[post 20] BIENVENUE SUR LA PAGE DE LA CITÉ DE LA MISÉRICORDE -> articles:detail (slug: bienvenue-sur-la-page-de-la-cite-de-la-misericorde)
dry-run — aucun objet créé');
INSERT INTO "migration_migrationrun" VALUES(6,'2026-08-13 10:14:22.723490','2026-08-13 10:14:27.951006','import','2026-08-13 10:14:22.723691','2026-08-13 10:14:27.950792','FAILED','Interrompu (erreur avant correction)');
INSERT INTO "migration_migrationrun" VALUES(7,'2026-08-13 10:14:57.207551','2026-08-13 10:17:19.053206','import','2026-08-13 10:14:57.207782','2026-08-13 10:17:19.052601','SUCCESS','Importé : 12 | Ignoré : 1 | Erreur : 0');
INSERT INTO "migration_migrationrun" VALUES(8,'2026-08-13 10:17:36.416983','2026-08-13 10:17:36.624640','report','2026-08-13 10:17:36.417036','2026-08-13 10:17:36.624523','SUCCESS','{
  "runs": [
    {
      "kind": "report",
      "status": "RUNNING",
      "started_at": "2026-08-13 10:17:36.417036+00:00"
    },
    {
      "kind": "import",
      "status": "SUCCESS",
      "started_at": "2026-08-13 10:14:57.207782+00:00"
    },
    {
      "kind": "import",
      "status": "RUNNING",
      "started_at": "2026-08-13 10:14:22.723691+00:00"
    },
    {
      "kind": "import",
      "status": "SUCCESS",
      "started_at": "2026-08-13 10:13:46.575972+00:00"
    },
    {
      "kind": "audit",
      "status": "SUCCESS",
      "started_at": "2026-08-13 10:13:24.321717+00:00"
    },
    {
      "kind": "audit",
      "status": "SUCCESS",
      "started_at": "2026-08-13 10:12:49.383277+00:00"
    },
    {
      "kind": "audit",
      "status": "SUCCESS",
      "started_at": "2026-08-13 10:12:19.102169+00:00"
    },
    {
      "kind": "audit",
      "status": "FAILED",
      "started_at": "2026-08-13 10:10:02.006535+00:00"
    }
  ],
  "articles": {
    "total": 9,
    "draft": 9
  },
  "pages": {
    "total": 9,
    "draft": 9
  },
  "media": {
    "total": 77,
    "imported": 77
  },
  "url_mappings": {
    "total": 12,
    "pending": 0
  },
  "errors": 0
}');
CREATE TABLE "migration_urlmapping" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "old_url" varchar(500) NOT NULL UNIQUE, "new_url" varchar(500) NOT NULL, "mapped_at" datetime NOT NULL);
INSERT INTO "migration_urlmapping" VALUES(1,'https://citedelamisericorde.wordpress.com/projets/','/page/projets/','2026-08-13 10:15:02.079850');
INSERT INTO "migration_urlmapping" VALUES(2,'https://citedelamisericorde.wordpress.com/','/page/about/','2026-08-13 10:15:04.447184');
INSERT INTO "migration_urlmapping" VALUES(3,'https://citedelamisericorde.wordpress.com/historique/','/page/historique/','2026-08-13 10:15:09.211772');
INSERT INTO "migration_urlmapping" VALUES(4,'https://citedelamisericorde.wordpress.com/2026/05/07/projet-de-lutte-contre-la-malnutrition-aux-enfants-de-moin-de-10ans-dans-le-territoire-de-nyiragongonyiragongo-lorganisation-cite-de-la-misericorde-lance-un-programme-de-lutte-contre-la-mal/','/actualites/projet-de-lutte-contre-la-malnutrition-aux-enfants-de-moin-de-10ans-dans-le-territoire-de-nyiragongonyiragongo-lorganisation-cite-de-la-misericorde-lance-un-programme-de-lutte-contre-la-mal/','2026-08-13 10:15:35.053950');
INSERT INTO "migration_urlmapping" VALUES(5,'https://citedelamisericorde.wordpress.com/2025/09/13/projet-de-contribution-a-la-stabilisation-et-autonomisation-socioecinomique-des-survivants-des-violences-basees-sur-les-genres-en-republique-democratique-du-congo/','/actualites/projet-de-contribution-a-la-stabilisation-et-autonomisation-socioecinomique-des-survivants-des-violences-basees-sur-les-genres-en-republique-democratique-du-congo/','2026-08-13 10:15:42.639289');
INSERT INTO "migration_urlmapping" VALUES(6,'https://citedelamisericorde.wordpress.com/2025/07/03/appel-au-don-sos-orphelinat/','/actualites/appel-au-don-sos-orphelinat/','2026-08-13 10:16:14.350127');
INSERT INTO "migration_urlmapping" VALUES(7,'https://citedelamisericorde.wordpress.com/2025/05/31/amenagement-cuisine-orphelinat/','/actualites/amenagement-cuisine-orphelinat/','2026-08-13 10:16:29.500564');
INSERT INTO "migration_urlmapping" VALUES(8,'https://citedelamisericorde.wordpress.com/2025/05/28/projet-dimplantation-dune-ferme-agro-ecologique-projet-execute-par-lassociation-collectif-des-jeunes-pour-la-paix-et-le-developpement-cjpd-congo-asbl/','/actualites/projet-dimplantation-dune-ferme-agro-ecologique-projet-execute-par-lassociation-collectif-des-jeunes-pour-la-paix-et-le-developpement-cjpd-congo-asbl/','2026-08-13 10:16:49.815547');
INSERT INTO "migration_urlmapping" VALUES(9,'https://citedelamisericorde.wordpress.com/2025/05/24/une-bonne-journee-sannonce/','/actualites/une-bonne-journee-sannonce/','2026-08-13 10:17:05.638015');
INSERT INTO "migration_urlmapping" VALUES(10,'https://citedelamisericorde.wordpress.com/2025/05/19/projet-de-creation-dun-aire-des-jeux/','/actualites/projet-de-creation-dun-aire-des-jeux/','2026-08-13 10:17:09.387282');
INSERT INTO "migration_urlmapping" VALUES(11,'https://citedelamisericorde.wordpress.com/2024/12/15/projet-de-la-creation-dun-centre-de-formation-professionnel-en-faveur-des-orphelins-de-lorphelinat-cite-de-la-misericorde-en-republique-democratique-du-congo/','/actualites/projet-de-la-creation-dun-centre-de-formation-professionnel-en-faveur-des-orphelins-de-lorphelinat-cite-de-la-misericorde-en-republique-democratique-du-congo/','2026-08-13 10:17:16.600511');
INSERT INTO "migration_urlmapping" VALUES(12,'https://citedelamisericorde.wordpress.com/2024/12/15/bienvenue-sur-la-page-de-la-cite-de-la-misericorde/','/actualites/bienvenue-sur-la-page-de-la-cite-de-la-misericorde/','2026-08-13 10:17:18.862729');
CREATE TABLE "newsletter_subscriber" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "email" varchar(254) NOT NULL UNIQUE, "name" varchar(200) NOT NULL, "token" varchar(64) NOT NULL UNIQUE, "is_confirmed" bool NOT NULL, "confirmed_at" datetime NULL, "is_active" bool NOT NULL, "unsubscribed_at" datetime NULL, "source" varchar(100) NOT NULL);
CREATE TABLE "pages_page" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "slug" varchar(255) NOT NULL UNIQUE, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "title" varchar(200) NOT NULL, "content" text NOT NULL, "template" varchar(80) NOT NULL, "status" varchar(20) NOT NULL, "order" smallint unsigned NOT NULL CHECK ("order" >= 0), "in_menu" bool NOT NULL, "meta_title" varchar(160) NOT NULL, "meta_description" varchar(300) NOT NULL, "cover_image_id" bigint NULL REFERENCES "media_mediaitem" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "pages_page" VALUES(1,'a-propos','2026-08-13 09:53:32.553649','2026-08-14 14:58:22.995190','À propos','<p>La <strong>Cité de la Miséricorde</strong> est une association sans but lucratif, apolitique et non confessionnelle, fondée en <strong>2018</strong> à Bukavu par des membres fondateurs engagés pour la paix et le développement. Elle est régie par le décret-loi n°004/2001 du 20 juillet 2001 portant dispositions générales applicables aux associations sans but lucratif et aux établissements d’utilité publique, et enregistrée sous le n° <strong>JUST 112/DP-SKV/CA/-5754/2020 du 18 juillet 2020</strong>.</p><p>Le siège social est établi à <strong>Bukavu, commune d’Ibanda, quartier Panzi</strong>, province du Sud-Kivu, en République Démocratique du Congo. Le rayon d’action s’étend sur toute la province du Sud-Kivu, avec la perspective de s’étendre dans d’autres provinces du pays.</p><p>L’association accueille et encadre aujourd’hui un <strong>orphelinat</strong> qui prend en charge des enfants orphelins et vulnérables, et mène des actions de <strong>développement communautaire</strong> : autonomisation des femmes, ferme-école agroécologique, appui aux ménages vulnérables et aux déplacés des guerres de la région des Grands Lacs.</p><p>La Cité de la Miséricorde collabore avec des ONG locales et internationales afin d’apporter sa part à la reconstruction d’un Congo nouveau.</p>','','published',0,1,'','',NULL);
INSERT INTO "pages_page" VALUES(2,'notre-histoire','2026-08-13 09:53:32.652227','2026-08-14 14:58:22.144708','Notre histoire','
<p>Il est créé à BUKAVU par les membres fondateurs l’orphelinat CITE DE LA MISERICORDE, une association sans but lucratif dénommée Cité de la Miséricorde. Elle est apolitique et non confessionnelle soumise aux dispositions du décret-loi n°004/2001 du 20 juillet portant dispositions générales applicables aux associations sans but lucratif et aux établissements d’utilité publique.   </p>



<p>Le siège social de la Cité de la Miséricorde est établi à BUKAVU, en Commune d’IBANDA, quartier PANZI, dans la province du SUD-KIVU, en République Démocratique du Congo.</p>



<figure><img width="1024" height="575" src="/media/media/2026/08/wp/2026/08/1000566679.jpg" alt=""/></figure>



<p>Le rayon d’action de la Cité de la Miséricorde s’étend sur toute l’étendue de la province du Sud-Kivu et avec comme perspective de l’étendre dans d’autres provinces de la République Démocratique du Congo</p>



<p><strong>Administration</strong></p>



<p>L’organisation est dirigée par Monsieur ZIRHUMANA KAMOLE Marie-Manassé, Coordinateur de la Cité de la Miséricorde et directeur de  l’orphelinat avec un diplôme de baccalauréat en Psychologie sociale et en Théologie à l’Université Bilingue Anglicane de Goma. </p>



<p>Un conseil administratif composé de 5 membres, un conseil de gestion composé de 4 membres et 5 agents de terrain</p>



<p><strong>Objectifs principaux</strong></p>



<ul>
<li>Encadrement holistique et orientation des orphelins et enfants nécessiteux en vue de leurs donner la possibilité d’accéder à l’instruction et d’acquérir une formation leur permettant de devenir responsables de leur propre développement</li>



<li>Promouvoir les activités de développement communautaire de base tout en prenant en compte les aspects de genre dans le domaine agropastoral.</li>
</ul>



<p><strong>Motivation de création de l’organisation</strong> Les guerres que notre pays la République Démocratique du Congo a connues nous ont amené beaucoup de conséquences sur le plan environnemental et sur le plan social : exode massif des populations et détérioration du tissu économique.</p>



<figure><img width="715" height="402" src="/media/media/2026/08/wp/2026/08/1000566685.jpg" alt=""/></figure>



<p>Plusieurs ménages ont été dépouillés de leurs ressources, les enfants ont perdu leurs droits d’accès à l’école, les parents ont perdu leurs emplois et sont incapables d’assumer leurs responsabilités.</p>



<p>Ces enfants sont en majorité absents à l’école, présents dans les rues, dans les places publiques, dans les marchés et même sur les dépotoirs. Ils sont confrontés quotidiennement à d’énormes problèmes de viol, vol, logement, alimentation, éducation et d’accès aux soins de santé primaire. </p>



<p>Pour ces raisons ces enfants livrés à eux-mêmes sont au cœur des problèmes tels que l’exploitation sous toutes les formes, la délinquance, la toxicomanie…ils sont obligés de se lancer sur le marché du travail où ils se font exploités dans des gros travaux de porte faits, comme creuseurs dans les mines illégales … </p>



<p>D’autres se livrent à l’alcool, aux tabacs et à la prostitution s’exposant ainsi aux dangers comme les IST,VIH/SIDA et à des grossesses non désirées dont la paternité est souvent difficile à déterminer. Ce projet est de sensibilisation sur la promotion et la protection des droits de l’enfant sur une durée indéfinie, il améliorera les conditions de vie de ces derniers, pour les créer un cadre de vie favorable et pour répondre aux règlements de la charte des nations unies sur les droits des enfants. Ainsi l’association Cité de la Miséricorde a pris l’initiative de prendre en charge 50 orphelins  </p>



<p>Depuis un certain temps, nous observons que les femmes victimes de ces guerres, et donc défavorisées, assurent la responsabilité de supporter la charge sociale de leurs enfants : les frais scolaires, les soins médicaux, l’alimentation familiale, … au moment où elles n’ont pas d’emplois et les petits revenus qu’elles gagnent dans leur façon de se débrouiller ne parviennent pas à supporter la charge sociale de leurs ménages.  </p>



<p>La population jeune qui devait soutenir le développement de leurs milieux respectifs a totalement abandonné le secteur agricole et élevage à la merci de la population vieille. </p>



<figure><img width="605" height="325" src="/media/media/2026/08/wp/2026/08/phhistorique.jpg" alt=""/></figure>



<p>Ces jeunes ont trouvé utile de se lancer dans les carrières minières où ils ne gagnent presque rien. La Cité de la Miséricorde dans son plan encourage la participation de la femme dans la gestion de l’environnement, car c’est elle qui est devenue le centre de la production familiale, les rôles étant inversés dans les familles suite à la guerre qu’a connu notre sous-région : « LES GRANDS LACS ».  </p>



<p>Pour ce faire, nous initions la création de la Cité de la Miséricorde, afin de renforcer la synergie entre tous les intervenants à tous les niveaux (Etats, Communautés religieuses, Bailleurs des fonds)6</p>
','','published',0,1,'','',NULL);
INSERT INTO "pages_page" VALUES(3,'notre-mission','2026-08-13 09:53:32.750096','2026-08-14 14:58:23.118701','Notre mission','<p>Notre mission est de <strong>contribuer à la reconstruction d’un Congo nouveau</strong> en renforçant la synergie entre les États, les communautés religieuses et les bailleurs de fonds. Concrètement, nous nous engageons à :</p><ul><li>Encadrer les <strong>enfants orphelins et vulnérables</strong> pour leur donner accès à l’instruction et à une formation leur permettant de devenir responsables de leur propre développement ;</li><li>Promouvoir des associations féminines de base et la <strong>participation des femmes</strong> à la gestion du milieu environnemental ;</li><li>Développer des activités <strong>agropastorales</strong> en prenant en compte les aspects de genre, notamment à travers notre ferme-école agroécologique ;</li><li>Renforcer la <strong>conservation de la nature</strong> et la protection quotidienne de l’environnement (flore, faune) ;</li><li>Créer des <strong>emplois</strong> afin de contribuer à la lutte contre la pauvreté ;</li><li>Encadrer la communauté de base dans l’<strong>éducation morale et technico-professionnelle</strong> ;</li><li>Créer des <strong>centres nutritionnels et psycho-socio-économiques</strong> pour les enfants défavorisés, les femmes vulnérables et les déplacés des guerres ;</li><li>Réhabiliter les <strong>infrastructures sanitaires, scolaires, routières et énergétiques</strong> et créer des structures sanitaires, vétérinaires et agricoles.</li></ul>','','published',0,1,'','',NULL);
INSERT INTO "pages_page" VALUES(4,'notre-vision','2026-08-13 09:53:32.840465','2026-08-14 14:58:23.219914','Notre vision','<p>Après des années de guerre dans la région des Grands Lacs, nos familles ont été dépouillées de leurs ressources, nos enfants ont perdu l’accès à l’école et nos femmes portent seules la charge sociale de leurs ménages. Notre vision est celle d’une <strong>région des Grands Lacs pacifique et prospère</strong> où :</p><ul><li>chaque <strong>enfant orphelin</strong> est protégé, scolarisé et en bonne santé ;</li><li>chaque <strong>femme</strong>, au cœur de la production familiale, est autonome et reconnue ;</li><li>chaque <strong>jeune</strong> retrouve sa place dans l’agriculture et l’élevage, moteurs du développement de ses communautés ;</li><li>chaque communauté vit dans la <strong>paix, la dignité</strong> et gère durablement son environnement.</li></ul>','','published',0,1,'','',NULL);
INSERT INTO "pages_page" VALUES(5,'nos-valeurs','2026-08-13 09:53:32.936954','2026-08-14 14:58:23.315626','Nos valeurs','<p>Les valeurs qui guident notre action au quotidien :</p><ul><li><strong>Miséricorde</strong> : la compassion et l’amour du prochain au cœur de chaque action ;</li><li><strong>Paix et réconciliation</strong> : panser les blessures des guerres et reconstruire le tissu social ;</li><li><strong>Égalité de genre</strong> : reconnaître et soutenir le rôle central des femmes dans la production familiale ;</li><li><strong>Solidarité</strong> : venir en aide aux plus vulnérables, sans discrimination ;</li><li><strong>Développement durable</strong> : protéger la nature et gérer responsablement l’environnement ;</li><li><strong>Transparence</strong> : une gestion rigoureuse et vérifiable des ressources, fondée sur des rapports réguliers ;</li><li><strong>Engagement communautaire</strong> : la synergie entre les États, les communautés religieuses et les bailleurs de fonds.</li></ul>','','published',0,1,'','',NULL);
INSERT INTO "pages_page" VALUES(6,'notre-equipe','2026-08-13 09:53:33.018458','2026-08-13 11:03:49.460513','Notre équipe','<p>La présentation de l''équipe dirigeante (Conseil d''administration, coordinateur, équipe terrain) sera publiée ici prochainement.</p>','default','published',98,1,'','',NULL);
INSERT INTO "pages_page" VALUES(7,'projets','2026-08-13 10:15:01.831305','2026-08-13 10:15:01.831407','CRÉATION D’UN CENTRE DE FORMATION PROFESSIONNEL EN FAVEUR DES ORPHELINS DE LA CITÉ DE LA MISÉRICORDE RDC','','','published',0,0,'','',NULL);
INSERT INTO "pages_page" VALUES(8,'about','2026-08-13 10:15:04.337474','2026-08-14 14:58:22.420631','CITE DE LA MISERICORDE','
<p>Il est créé à BUKAVU par les membres fondateurs l’orphelinat CITE DE LA MISERICORDE, une association sans but lucratif dénommée Cité de la Miséricorde. Elle est apolitique et non confessionnelle soumise aux dispositions du décret-loi n°004/2001 du 20 juillet portant dispositions générales applicables aux associations sans but lucratif et aux établissements d’utilité publique.   </p>



<figure><img width="1024" height="768" src="/media/media/2026/08/wp/2026/08/img-20241215-wa00683347026291772110706.jpg" alt=""/></figure>



<p>Le siège social de la Cité de la Miséricorde est établi à BUKAVU, en Commune d’IBANDA, quartier PANZI, dans la province du SUD-KIVU, en République Démocratique du Congo. <a href="https://citedelamisericorde.wordpress.com/historique/">cliquez ici pour plus d’information</a></p>
','','published',0,0,'','',NULL);
INSERT INTO "pages_page" VALUES(9,'historique','2026-08-13 10:15:09.095457','2026-08-14 14:58:22.329303','Cité de la Miséricorde — Qui sommes-nous ?','
<p>Il est créé à BUKAVU par les membres fondateurs l’orphelinat CITE DE LA MISERICORDE, une association sans but lucratif dénommée Cité de la Miséricorde. Elle est apolitique et non confessionnelle soumise aux dispositions du décret-loi n°004/2001 du 20 juillet portant dispositions générales applicables aux associations sans but lucratif et aux établissements d’utilité publique.   </p>



<p>Le siège social de la Cité de la Miséricorde est établi à BUKAVU, en Commune d’IBANDA, quartier PANZI, dans la province du SUD-KIVU, en République Démocratique du Congo.</p>



<figure><img width="1024" height="575" src="/media/media/2026/08/wp/2026/08/1000566679.jpg" alt=""/></figure>



<p>Le rayon d’action de la Cité de la Miséricorde s’étend sur toute l’étendue de la province du Sud-Kivu et avec comme perspective de l’étendre dans d’autres provinces de la République Démocratique du Congo</p>



<p><strong>Administration</strong></p>



<p>L’organisation est dirigée par Monsieur ZIRHUMANA KAMOLE Marie-Manassé, Coordinateur de la Cité de la Miséricorde et directeur de  l’orphelinat avec un diplôme de baccalauréat en Psychologie sociale et en Théologie à l’Université Bilingue Anglicane de Goma. </p>



<p>Un conseil administratif composé de 5 membres, un conseil de gestion composé de 4 membres et 5 agents de terrain</p>



<p><strong>Objectifs principaux</strong></p>



<ul>
<li>Encadrement holistique et orientation des orphelins et enfants nécessiteux en vue de leurs donner la possibilité d’accéder à l’instruction et d’acquérir une formation leur permettant de devenir responsables de leur propre développement</li>



<li>Promouvoir les activités de développement communautaire de base tout en prenant en compte les aspects de genre dans le domaine agropastoral.</li>
</ul>



<p><strong>Motivation de création de l’organisation</strong> Les guerres que notre pays la République Démocratique du Congo a connues nous ont amené beaucoup de conséquences sur le plan environnemental et sur le plan social : exode massif des populations et détérioration du tissu économique.</p>



<figure><img width="715" height="402" src="/media/media/2026/08/wp/2026/08/1000566685.jpg" alt=""/></figure>



<p>Plusieurs ménages ont été dépouillés de leurs ressources, les enfants ont perdu leurs droits d’accès à l’école, les parents ont perdu leurs emplois et sont incapables d’assumer leurs responsabilités.</p>



<p>Ces enfants sont en majorité absents à l’école, présents dans les rues, dans les places publiques, dans les marchés et même sur les dépotoirs. Ils sont confrontés quotidiennement à d’énormes problèmes de viol, vol, logement, alimentation, éducation et d’accès aux soins de santé primaire. </p>



<p>Pour ces raisons ces enfants livrés à eux-mêmes sont au cœur des problèmes tels que l’exploitation sous toutes les formes, la délinquance, la toxicomanie…ils sont obligés de se lancer sur le marché du travail où ils se font exploités dans des gros travaux de porte faits, comme creuseurs dans les mines illégales … </p>



<p>D’autres se livrent à l’alcool, aux tabacs et à la prostitution s’exposant ainsi aux dangers comme les IST,VIH/SIDA et à des grossesses non désirées dont la paternité est souvent difficile à déterminer. Ce projet est de sensibilisation sur la promotion et la protection des droits de l’enfant sur une durée indéfinie, il améliorera les conditions de vie de ces derniers, pour les créer un cadre de vie favorable et pour répondre aux règlements de la charte des nations unies sur les droits des enfants. Ainsi l’association Cité de la Miséricorde a pris l’initiative de prendre en charge 50 orphelins  </p>



<p>Depuis un certain temps, nous observons que les femmes victimes de ces guerres, et donc défavorisées, assurent la responsabilité de supporter la charge sociale de leurs enfants : les frais scolaires, les soins médicaux, l’alimentation familiale, … au moment où elles n’ont pas d’emplois et les petits revenus qu’elles gagnent dans leur façon de se débrouiller ne parviennent pas à supporter la charge sociale de leurs ménages.  </p>



<p>La population jeune qui devait soutenir le développement de leurs milieux respectifs a totalement abandonné le secteur agricole et élevage à la merci de la population vieille. </p>



<figure><img width="605" height="325" src="/media/media/2026/08/wp/2026/08/phhistorique.jpg" alt=""/></figure>



<p>Ces jeunes ont trouvé utile de se lancer dans les carrières minières où ils ne gagnent presque rien. La Cité de la Miséricorde dans son plan encourage la participation de la femme dans la gestion de l’environnement, car c’est elle qui est devenue le centre de la production familiale, les rôles étant inversés dans les familles suite à la guerre qu’a connu notre sous-région : « LES GRANDS LACS ».  </p>



<p>Pour ce faire, nous initions la création de la Cité de la Miséricorde, afin de renforcer la synergie entre tous les intervenants à tous les niveaux (Etats, Communautés religieuses, Bailleurs des fonds)6</p>
','','published',0,0,'','',NULL);
INSERT INTO "pages_page" VALUES(10,'statuts','2026-08-13 11:03:49.357974','2026-08-14 14:58:23.407834','Statuts de l''ASBL','<p>L’association est régie par ses statuts, adoptés à Bukavu le <strong>12 février 2018</strong> par les membres fondateurs, conformément au décret-loi n°004/2001 du 20 juillet 2001 portant dispositions générales applicables aux associations sans but lucratif et aux établissements d’utilité publique.</p><h2>Dénomination et siège</h2><p>Association sans but lucratif, apolitique et non confessionnelle, enregistrée sous le n° JUST 112/DP-SKV/CA/-5754/2020 du 18 juillet 2020. Siège social : Bukavu, commune d’Ibanda, quartier Panzi, province du Sud-Kivu, République Démocratique du Congo. Durée : indéterminée.</p><h2>Organes</h2><ul><li>L’<strong>Assemblée Générale</strong> : organe suprême, composée de tous les membres effectifs ;</li><li>Le <strong>Conseil d’Administration</strong> : sept membres élus pour trois ans renouvelables (président, vice-président, secrétaire, trésorier et trois conseillers) ;</li><li>Le <strong>Bureau de Coordination</strong> : un coordinateur (trice), secondé (e) par un chargé de programme.</li></ul><h2>Ressources</h2><ul><li>Cotisations des membres fondateurs, effectifs et d’honneur ;</li><li>Financements des partenaires ;</li><li>Activités d’autofinancement ;</li><li>Dons, legs et subventions de l’État.</li></ul><p>Les fonds de l’association sont placés dans une institution bancaire agréée. La gestion des comptes s’effectue au moyen de trois signatures : celle du président et du trésorier au niveau du Conseil d’Administration, et celle du coordinateur au niveau du Bureau de Coordination.</p><p><a href="/media/media/2026/08/statuts-cite-de-la-misericorde_errWqWS.pdf" class="btn btn-accent" download>Télécharger les statuts (PDF)</a></p>','default','published',99,1,'','',NULL);
CREATE TABLE "pages_report" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "title" varchar(250) NOT NULL, "kind" varchar(20) NOT NULL, "year" smallint unsigned NULL CHECK ("year" >= 0), "document" varchar(100) NOT NULL, "summary" text NOT NULL, "is_published" bool NOT NULL, "validated_at" datetime NULL, "published_at" datetime NULL, "validated_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "partners_partner" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "name" varchar(200) NOT NULL, "kind" varchar(20) NOT NULL, "website" varchar(200) NOT NULL, "description" text NOT NULL, "is_published" bool NOT NULL, "sort_order" smallint unsigned NOT NULL CHECK ("sort_order" >= 0), "logo_id" bigint NULL REFERENCES "media_mediaitem" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "partners_partner" VALUES(1,'2026-08-14 06:36:21.430221','2026-08-14 06:36:21.430286','ADRNS — Association Développement Relations Nord-Sud','partner','https://www.adrns.org','ADRNS (Association Développement Relations Nord-Sud), association loi 1901 basée à Saint-Germain-en-Laye (France), est notre partenaire bailleur. Grâce à son soutien, nous développons une ferme-école agroécologique de formation au Sud-Kivu : un projet de 12 mois visant à former et à autonomiser les agriculteurs locaux en situation de vulnérabilité. ADRNS assure le financement par tranches, l''acquisition des équipements et un suivi technique sur le terrain ; de notre côté, nous garantissons une transparence totale des dépenses grâce à des rapports d''activités réguliers.',1,1,89);
CREATE TABLE "payments_paymentprovider" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "name" varchar(100) NOT NULL, "code" varchar(30) NOT NULL UNIQUE, "is_active" bool NOT NULL, "supported_currencies" varchar(100) NOT NULL, "supported_countries" varchar(200) NOT NULL, "display_order" smallint unsigned NOT NULL CHECK ("display_order" >= 0), "logo" varchar(100) NOT NULL, "description" varchar(300) NOT NULL);
INSERT INTO "payments_paymentprovider" VALUES(1,'2026-08-13 10:25:57.525390','2026-08-13 10:25:57.525458','Stripe','stripe',0,'USD','US,BE,FR,GB,KE,NG',10,'','Cartes bancaires internationales (USD, EUR)');
INSERT INTO "payments_paymentprovider" VALUES(2,'2026-08-13 10:25:57.670822','2026-08-13 10:25:57.670870','PayPal','paypal',0,'USD','US,BE,FR,GB,KE,NG',20,'','Compte PayPal (international)');
INSERT INTO "payments_paymentprovider" VALUES(3,'2026-08-13 10:25:57.760647','2026-08-13 10:25:57.760700','Mobile Money (Flutterwave)','mobile_money',0,'USD','CD,KE,UG,TZ,RW',30,'','Airtel Money, M-Pesa, Orange Money (RDC)');
INSERT INTO "payments_paymentprovider" VALUES(4,'2026-08-13 10:25:57.868571','2026-08-13 10:25:57.868601','Mode démo (sans paiement réel)','sandbox',1,'USD','',99,'','Simulation de paiement — développement uniquement');
CREATE TABLE "payments_paymenttransaction" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "amount" decimal NOT NULL, "currency" varchar(3) NOT NULL, "status" varchar(12) NOT NULL, "provider_transaction_id" varchar(255) NOT NULL, "raw_response" text NOT NULL CHECK ((JSON_VALID("raw_response") OR "raw_response" IS NULL)), "error_message" text NOT NULL, "attempted_at" datetime NULL, "succeeded_at" datetime NULL, "donation_id" bigint NOT NULL REFERENCES "donations_donation" ("id") DEFERRABLE INITIALLY DEFERRED, "provider_id" bigint NOT NULL REFERENCES "payments_paymentprovider" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "payments_paymenttransaction" VALUES(1,'2026-08-13 10:31:35.880786','2026-08-13 10:31:36.121713',25,'USD','SUCCEEDED','sandbox-0731216a322c402bab5d1d65272daa18','{}','',NULL,'2026-08-13 10:31:36.113156',4,4);
INSERT INTO "payments_paymenttransaction" VALUES(2,'2026-08-14 00:39:23.023227','2026-08-14 00:39:23.245708',25,'USD','SUCCEEDED','sandbox-c38110326e5c4a8f8c279cb94aca5380','{}','',NULL,'2026-08-14 00:39:23.243791',6,4);
CREATE TABLE "payments_webhookevent" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "event_id" varchar(255) NOT NULL, "event_type" varchar(100) NOT NULL, "payload" text NOT NULL CHECK ((JSON_VALID("payload") OR "payload" IS NULL)), "signature_valid" bool NOT NULL, "is_processed" bool NOT NULL, "processed_at" datetime NULL, "error_message" text NOT NULL, "provider_id" bigint NOT NULL REFERENCES "payments_paymentprovider" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "programs_program" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "slug" varchar(255) NOT NULL UNIQUE, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "domain" varchar(30) NOT NULL UNIQUE, "title" varchar(200) NOT NULL, "short_description" varchar(300) NOT NULL, "description" text NOT NULL, "icon" varchar(80) NOT NULL, "is_active" bool NOT NULL, "order" smallint unsigned NOT NULL CHECK ("order" >= 0), "image_id" bigint NULL REFERENCES "media_mediaitem" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "programs_program" VALUES(1,'enfants-vulnerables','2026-08-13 09:53:31.696044','2026-08-13 09:53:31.696083','children','Enfants vulnérables','Assistance, protection et accompagnement des enfants orphelins et vulnérables.','','',1,0,NULL);
INSERT INTO "programs_program" VALUES(2,'autonomisation-des-femmes','2026-08-13 09:53:31.808974','2026-08-13 09:53:31.809025','women','Autonomisation des femmes','Formation, soutien socio-économique et autonomisation des femmes.','','',1,0,NULL);
INSERT INTO "programs_program" VALUES(3,'assistance-humanitaire','2026-08-13 09:53:31.909240','2026-08-13 09:53:31.909291','humanitarian','Assistance humanitaire','Réponse aux crises : nutrition, aide d''urgence, accompagnement des personnes affectées.','','',1,0,NULL);
INSERT INTO "programs_program" VALUES(4,'developpement-communautaire','2026-08-13 09:53:32.020658','2026-08-13 09:53:32.020706','community','Développement communautaire','Développement communautaire, mobilisation des partenaires et de la société civile.','','',1,0,NULL);
CREATE TABLE "projects_project" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "slug" varchar(255) NOT NULL UNIQUE, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "title" varchar(300) NOT NULL, "location" varchar(200) NOT NULL, "context" text NOT NULL, "problem" text NOT NULL, "objectives" text NOT NULL, "beneficiaries" text NOT NULL, "activities" text NOT NULL, "results" text NOT NULL, "progress_percent" smallint unsigned NOT NULL CHECK ("progress_percent" >= 0), "start_date" date NULL, "end_date" date NULL, "budget" decimal NULL, "currency" varchar(3) NOT NULL, "is_featured" bool NOT NULL, "publication_authorized" bool NOT NULL, "needs_donation" bool NOT NULL, "seo_description" varchar(300) NOT NULL, "cover_image_id" bigint NULL REFERENCES "media_mediaitem" ("id") DEFERRABLE INITIALLY DEFERRED, "program_id" bigint NULL REFERENCES "programs_program" ("id") DEFERRABLE INITIALLY DEFERRED, "status_id" bigint NULL REFERENCES "projects_projectstatus" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "projects_project" VALUES(1,'lutte-contre-la-malnutrition-des-enfants-de-moins-de-10-ans-nyiragongo','2026-08-13 11:03:48.521093','2026-08-13 11:03:48.521119','Lutte contre la malnutrition des enfants de moins de 10 ans — Nyiragongo','Nyiragongo (Nord-Kivu)','Uwimana,1.5 ans: orpheline: malnutrition aiguë modérée Uwase,3ans: malnutrition aiguë modérée avec affection cutanée Pascale,2 ans: malnutrition aiguë modérée Photo de famille Enseignement sur l’allaitement maternel par Marie-Manassé ZIRHUMANA KAMOLE Des femmes cheffes de ménages qui accompagnaient leurs enfants au centre Rebecca : (orpheline,2ans) malnutrition aiguë sévère','','','','','',0,NULL,NULL,NULL,'USD',1,1,1,'',11,1,1);
INSERT INTO "projects_project" VALUES(2,'contribution-la-stabilisation-et-l-autonomisation-socio-conomique-des-survivante','2026-08-13 11:03:48.637125','2026-08-13 11:03:48.637144','Contribution à la stabilisation et à l''autonomisation socioéconomique des survivantes des VBG','République Démocratique du Congo','Intitulé du projet : Projet de contribution à la stabilisation et autonomisation socioéconomique des survivants des violences basées sur le genre dans le groupement de Kamisimbi, Mumosho et Mudusa en République Democratique du Congo Contexte et justification du projet : Le projet socio-économique et autonomisation des survivants des VSBG et restauration de la paix, est né suite à l’évolution des dynamiques socioculturelles et sécuritaires vécues dans la zone. Les groupements MUMOSHO,KAMISIMBI et MUDUSA ciblés par le projet sont périphériques de la ville de Bukavu et tous victimes des diverses atrocités. Les populations qui y vivent sont pour la plupart des personnes vulnérables qui mènent une vie de pauvreté car pour la plupart, ce sont des ménages gardant les parcelles des propriétaires qui habitent en centre-ville. Avant la résurgence de la guerre du M23, ils parvenaient à trouver de quoi survivre et ce parce que les dessertes agricoles reliant la ville aux territoires approvisionnaient la ville en nourriture. Suite à la dégradation du contexte sécuritaire dans ces groupements(en raison des conflits armés récurrents entre les troupes loyalistes des FARDC, alliées au groupe armé Wazalendu, et les rebelles du M23), de nombreuses femmes ont été violées, d’autres n’ont pas survécu aux lésions suite au manque d’encadrement et des soins appropriés. En effet, la présence réelle des survivants des VBG dans ces groupements cibles, dans l’aire de santé AS Mudusa, AS Kamisimbi, As Mumosho Ainsi, dans ce contexte, le projet vise à renforcer la stabilisation et l’autonomie des surviva','','','','','',0,NULL,NULL,NULL,'USD',1,1,1,'',17,2,1);
INSERT INTO "projects_project" VALUES(3,'am-nagement-de-la-cuisine-de-l-orphelinat','2026-08-13 11:03:48.758378','2026-08-13 11:03:48.758396','Aménagement de la cuisine de l''orphelinat','Bukavu (Sud-Kivu)','Il y a quelques années, l’orphelinat Cité de la Miséricorde utilise le dehors comme cuisine près du dortoire des garçons. Faute de fonds suffisants, cette cuisine n’a jusqu’à présent jamais été reconstruite à l’endroit favorable. Après un temps, le conseil d’administration a remarqué certains defis liés à l’emplacement de cette cuisine: 1. Destabilisation pendant la période pluvieuse qui nous oblige d’utiliser une partie du dortoir garçon. 2. Présence des affections pulmonaires chez les enfants liées à la Présence de la fumée 3. Haut risque de brulure chez les enfants mal intentionnés 4. Dégradation du mur de ce dortoir et celle de la peinture Pour ce faire,l’orphelinat souhaite construire une cuisinière moderne en materiaux durables. Modèle cuisine Le budget total de ce travail est de 475$ et grâce aux généreux donateurs l’orphélinat dispose déjà de 229 dollars americains. Mode de transfert: Virement sur le RIB de Orphélinat Moneygram Western union Ria Autres contacts: Whatsapp: +243970884579 Email: citedelamisericorde@gmail.com','','','','','',0,NULL,NULL,NULL,'USD',1,1,1,'',49,1,1);
INSERT INTO "projects_project" VALUES(4,'implantation-d-une-ferme-agro-cologique','2026-08-13 11:03:48.858320','2026-08-13 11:03:48.858336','Implantation d''une ferme agro-écologique','République Démocratique du Congo','Initié en 2024 par: Manassé Kamole,coordonateur du CJPD et fondateur de la Cité de la Miséricorde Durée: Décembre 2024-Novembre 2025 L’agroécologie couvre de nombreux aspects de l’agriculture et intègre les dimensions à la fois écologiques, économiques et sociales.Ces 3 grands piliers en font une discipline complète, jouant sur l’interaction entre l’écosystème et l’homme, cherchant à préserver l’environnement et la biodiversité tout en assurant la productivité agricole et en maximisant les fonctionnalités offertes par les écosystèmes. Le projet d’implantationd’unefermeagro-écologique à vocation pédagogique , situé à Kamisimbi-Sud Kivu, en RD Congo a pour but de développer les filières agricoles de Mukama,Bukera,Bushigi,Bukalwa localités situées dans le groupement de Kamisimbi à 24 kilomètres de la ville de Bukavu, pour assurer la sécurité alimentaire. Ce projet s’inscrit dans une démarche agroécologique afin d’augmenter la productivité des exploitations de manière durable, en maximisant les interactions écologiques et en limitant l’investissement nécessaire. Trois des techniques agroécologiques testées par le projet sont présentées dans cet article pour illustrer les trois fondements (respect de l’environnement, rentabilité économique, développement social) de la discipline. Le respect de l’environnement – lutte contre les adventices sans herbicide L’agroécologie prône une moindre utilisation des intrants chimiques, ainsi, l’apprentissage des différentes techniques agroécologiques dans la culture des produits maraichers,les protéger de l’érosion grâce au drainage et lutter ','','','','','',0,NULL,NULL,NULL,'USD',0,1,1,'',59,4,1);
INSERT INTO "projects_project" VALUES(5,'cr-ation-d-une-aire-de-jeux-pour-les-enfants-de-l-orphelinat','2026-08-13 11:03:49.041025','2026-08-13 11:03:49.041043','Création d''une aire de jeux pour les enfants de l''orphelinat','Bukavu (Sud-Kivu)','L’aire des jeux joue un rôle essentiel dans le développement des enfants, offrant un espace unique où ils peuvent s’épanouir physiquement, socialement et émotionnellement. Cet espace dédié aux jeux est le pivot de l’aire de jeux pour les enfants encadrés au sein de la Cité de la Miséricorde.','','','','','',0,NULL,NULL,NULL,'USD',0,1,1,'',72,1,1);
INSERT INTO "projects_project" VALUES(6,'cr-ation-d-un-centre-de-formation-professionnelle-pour-les-orphelins','2026-08-13 11:03:49.157662','2026-08-13 11:03:49.157678','Création d''un centre de formation professionnelle pour les orphelins','Bukavu (Sud-Kivu)','Contexte et justification du projet : Le faible taux de fréquentation aux études des orphelins due aux guerres à répétition à l’Est de la République Démocratique du Congo et plus spécialement au manque des moyens financiers par les membres de leurs familles connus ou inconnus ont poussé certains enfants dont l’âge scolaire est déjà avancé à ne plus avoir la chance de gagner leur vie. Ceux-ci deviennent après l’orphelinat des éléments constituant un danger pour la société soit retrouvés dans la rue, soit des voleurs ou victimes d’autres antivaleurs comme alcoolisme, tabagisme… Ainsi nous estimons que la création d’un centre de formation des orphelins en métier peut résoudre ce fléau Objectif du projet : notre projet a pour objectif principal de mettre en place un centre spécial pour l’apprentissage professionnel des orphelins de l’Orphelinat Cité de la Miséricorde ayant l’âge avancé et d’autres personnes qui désirent apprendre chez-nous en payant leur formation Localisation du projet : le présent projet de construction sera localisé dans le quartier Panzi, ville de Bukavu, province du Sud-Kivu pendant une durée de 11 mois allant du 05 janvier 2025 au 05 Décembre 2025. Nature et cadre juridique du projet : cette initiative est une action de développement à caractère socio-éducatif visant la redynamisation et la promotion du secteur de l’enseignement. Stratégies du projet : notre stratégie est celle de la relance du secteur Contacts: Email: citedelamisericorde@gmail.com','','','','','',0,NULL,NULL,NULL,'USD',0,1,1,'',74,1,1);
CREATE TABLE "projects_project_gallery" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "project_id" bigint NOT NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED, "mediaitem_id" bigint NOT NULL REFERENCES "media_mediaitem" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "projects_projectstatus" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "code" varchar(40) NOT NULL UNIQUE, "color" varchar(7) NOT NULL);
INSERT INTO "projects_projectstatus" VALUES(1,'En cours','ongoing','#16a34a');
INSERT INTO "projects_projectstatus" VALUES(2,'Réalisé','completed','#64748b');
INSERT INTO "projects_projectstatus" VALUES(3,'Urgent','urgent','#dc2626');
INSERT INTO "projects_projectstatus" VALUES(4,'Planifié','planned','#f59e0b');
CREATE TABLE "statistics_statistic" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "label" varchar(200) NOT NULL, "value" bigint unsigned NOT NULL CHECK ("value" >= 0), "prefix" varchar(10) NOT NULL, "suffix" varchar(10) NOT NULL, "icon" varchar(80) NOT NULL, "sort_order" smallint unsigned NOT NULL CHECK ("sort_order" >= 0), "is_published" bool NOT NULL, "source" varchar(300) NOT NULL, "updated_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "statistics_statistic" VALUES(1,'2026-08-13 11:03:49.257056','2026-08-13 11:03:49.257077','Enfants orphelins assistés',637,'','','',1,1,'Validation humaine — 13/08/2026',NULL);
CREATE TABLE "team_teammember" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(120) NOT NULL, "role" varchar(160) NOT NULL, "formation" varchar(220) NOT NULL, "bio" text NOT NULL, "photo" varchar(100) NOT NULL, "order" integer unsigned NOT NULL CHECK ("order" >= 0), "is_published" bool NOT NULL);
INSERT INTO "team_teammember" VALUES(1,'ZIRHUMANA KAMOLE Marie-Manassé','Fondateur et Coordonnateur','Bachelier en Développement et Action Humanitaire — Institut Supérieur de Pêche de Goma','Fondateur de l''organisation depuis 2018, il assure la coordination générale, veille à l''orientation stratégique, à la coordination des programmes et à la représentation de la structure auprès des partenaires et des parties prenantes.','team/1786632893229_ayLMwTc.jpg',1,1);
INSERT INTO "team_teammember" VALUES(2,'KABAGALE LEONARD','Président du Conseil d''Administration','Graduat en Sciences Infirmières','Président du Conseil d''Administration depuis 2019, il contribue à la gouvernance, à l''orientation institutionnelle et au suivi du fonctionnement général de l''organisation.','team/1786632974426_OogyTeY.jpg',2,1);
INSERT INTO "team_teammember" VALUES(3,'ELIONOR MUGEMA','Chef des Projets','Licence en Santé et Développement Communautaire','Responsable de la conception, de la planification, de la coordination et du suivi de la mise en œuvre des projets ; il contribue à la préparation des rapports et au développement des relations avec les partenaires.','team/1786633064769_oKipJ1B.jpg',3,1);
INSERT INTO "team_teammember" VALUES(4,'SAFARI MAKALA','Superviseur','Licence en Économie Rurale — Université Évangélique en Afrique (UEA)','Il assure la supervision des activités sur le terrain, le contrôle de la qualité des interventions, le respect des plans de travail et la remontée des informations issues des activités réalisées.','team/1786633081305_s8dSE3M.jpg',4,1);
INSERT INTO "team_teammember" VALUES(5,'BALUME BIZUKANZA BONHEUR','Chargé de Suivi et Évaluation','Licence en Santé et Développement Communautaire — Université Bilingue Anglicane de Goma','Chargé du suivi et de l''évaluation des activités et des projets : collecte, analyse et documentation des données pour mesurer les progrès, les résultats et l''impact des interventions.','',5,1);
INSERT INTO "team_teammember" VALUES(6,'BORAUZIMA CHARLINE','Chargée de Finance','Licenciée en Économie','Chargée de la gestion financière de l''organisation : suivi des ressources financières, tenue des documents comptables et préparation des éléments nécessaires à la bonne gestion des projets.','',6,1);
INSERT INTO "team_teammember" VALUES(7,'CLARISSE NABINTU','Chargée de Logistique','Licenciée en Logistique','Chargée de la logistique : organisation matérielle des activités, suivi des besoins logistiques et disponibilité des ressources nécessaires à la mise en œuvre des projets.','',7,1);
CREATE TABLE "testimonials_testimonial" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "author_name" varchar(200) NOT NULL, "kind" varchar(20) NOT NULL, "role_or_relation" varchar(200) NOT NULL, "content" text NOT NULL, "is_published" bool NOT NULL, "publication_authorized" bool NOT NULL, "sort_order" smallint unsigned NOT NULL CHECK ("sort_order" >= 0), "validated_at" datetime NULL, "photo_id" bigint NULL REFERENCES "media_mediaitem" ("id") DEFERRABLE INITIALLY DEFERRED, "related_project_id" bigint NULL REFERENCES "projects_project" ("id") DEFERRABLE INITIALLY DEFERRED, "validated_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE UNIQUE INDEX "accounts_user_groups_user_id_group_id_59c0b32f_uniq" ON "accounts_user_groups" ("user_id", "group_id");
CREATE INDEX "accounts_user_groups_user_id_52b62117" ON "accounts_user_groups" ("user_id");
CREATE INDEX "accounts_user_groups_group_id_bd11a704" ON "accounts_user_groups" ("group_id");
CREATE UNIQUE INDEX "accounts_user_user_permissions_user_id_permission_id_2ab516c2_uniq" ON "accounts_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "accounts_user_user_permissions_user_id_e4f0a161" ON "accounts_user_user_permissions" ("user_id");
CREATE INDEX "accounts_user_user_permissions_permission_id_113bb443" ON "accounts_user_user_permissions" ("permission_id");
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE INDEX "analytics_pageview_path_a3bf8434" ON "analytics_pageview" ("path");
CREATE INDEX "analytics_p_created_4c2b45_idx" ON "analytics_pageview" ("created_at");
CREATE INDEX "analytics_p_path_53ae0e_idx" ON "analytics_pageview" ("path", "created_at");
CREATE INDEX "media_mediaitem_category_id_de87f89c" ON "media_mediaitem" ("category_id");
CREATE INDEX "articles_article_status_f68a8acd" ON "articles_article" ("status");
CREATE INDEX "articles_article_published_at_b692f2ff" ON "articles_article" ("published_at");
CREATE INDEX "articles_article_author_id_059aea7d" ON "articles_article" ("author_id");
CREATE INDEX "articles_article_cover_image_id_c45eb2b3" ON "articles_article" ("cover_image_id");
CREATE INDEX "articles_ar_status_7759bd_idx" ON "articles_article" ("status", "published_at");
CREATE INDEX "articles_ar_slug_452037_idx" ON "articles_article" ("slug");
CREATE UNIQUE INDEX "articles_article_related_images_article_id_mediaitem_id_f82e013f_uniq" ON "articles_article_related_images" ("article_id", "mediaitem_id");
CREATE INDEX "articles_article_related_images_article_id_76374ff1" ON "articles_article_related_images" ("article_id");
CREATE INDEX "articles_article_related_images_mediaitem_id_cbc3ee5b" ON "articles_article_related_images" ("mediaitem_id");
CREATE UNIQUE INDEX "articles_article_categories_article_id_articlecategory_id_c546ef32_uniq" ON "articles_article_categories" ("article_id", "articlecategory_id");
CREATE INDEX "articles_article_categories_article_id_5d5f3e6c" ON "articles_article_categories" ("article_id");
CREATE INDEX "articles_article_categories_articlecategory_id_828bbb7e" ON "articles_article_categories" ("articlecategory_id");
CREATE UNIQUE INDEX "articles_article_tags_article_id_articletag_id_948a7866_uniq" ON "articles_article_tags" ("article_id", "articletag_id");
CREATE INDEX "articles_article_tags_article_id_524565b8" ON "articles_article_tags" ("article_id");
CREATE INDEX "articles_article_tags_articletag_id_0fbbc1da" ON "articles_article_tags" ("articletag_id");
CREATE INDEX "contact_contactmessage_is_spam_b04772fa" ON "contact_contactmessage" ("is_spam");
CREATE INDEX "contact_con_is_read_9a011e_idx" ON "contact_contactmessage" ("is_read");
CREATE INDEX "contact_con_is_spam_8ef3b9_idx" ON "contact_contactmessage" ("is_spam");
CREATE INDEX "programs_program_image_id_9a68c93b" ON "programs_program" ("image_id");
CREATE INDEX "projects_project_cover_image_id_578fb7d5" ON "projects_project" ("cover_image_id");
CREATE INDEX "projects_project_program_id_3eb7e51b" ON "projects_project" ("program_id");
CREATE INDEX "projects_project_status_id_9f58ac46" ON "projects_project" ("status_id");
CREATE INDEX "projects_pr_status__c35bcb_idx" ON "projects_project" ("status_id", "start_date");
CREATE UNIQUE INDEX "projects_project_gallery_project_id_mediaitem_id_e7e71320_uniq" ON "projects_project_gallery" ("project_id", "mediaitem_id");
CREATE INDEX "projects_project_gallery_project_id_eef19f7d" ON "projects_project_gallery" ("project_id");
CREATE INDEX "projects_project_gallery_mediaitem_id_627a9a4f" ON "projects_project_gallery" ("mediaitem_id");
CREATE INDEX "payments_paymenttransaction_status_54d89342" ON "payments_paymenttransaction" ("status");
CREATE INDEX "payments_paymenttransaction_provider_transaction_id_0e19c63a" ON "payments_paymenttransaction" ("provider_transaction_id");
CREATE INDEX "payments_paymenttransaction_donation_id_28dd7f0d" ON "payments_paymenttransaction" ("donation_id");
CREATE INDEX "payments_paymenttransaction_provider_id_f05f6028" ON "payments_paymenttransaction" ("provider_id");
CREATE INDEX "payments_pa_status_b6726a_idx" ON "payments_paymenttransaction" ("status");
CREATE INDEX "payments_pa_provide_1199a9_idx" ON "payments_paymenttransaction" ("provider_id", "status");
CREATE UNIQUE INDEX "payments_webhookevent_provider_id_event_id_0d6e39b7_uniq" ON "payments_webhookevent" ("provider_id", "event_id");
CREATE INDEX "payments_webhookevent_event_id_802a2532" ON "payments_webhookevent" ("event_id");
CREATE INDEX "payments_webhookevent_provider_id_6e3d6398" ON "payments_webhookevent" ("provider_id");
CREATE INDEX "donations_d_email_16156b_idx" ON "donations_donor" ("email");
CREATE INDEX "donations_donation_status_6c73bb41" ON "donations_donation" ("status");
CREATE INDEX "donations_donation_provider_reference_bed535a5" ON "donations_donation" ("provider_reference");
CREATE INDEX "donations_donation_project_id_5afb2670" ON "donations_donation" ("project_id");
CREATE INDEX "donations_donation_provider_id_1aa8ad2d" ON "donations_donation" ("provider_id");
CREATE INDEX "donations_donation_donor_id_25b1f2bc" ON "donations_donation" ("donor_id");
CREATE INDEX "donations_d_status_73ca83_idx" ON "donations_donation" ("status");
CREATE INDEX "donations_d_created_26bd74_idx" ON "donations_donation" ("created_at");
CREATE INDEX "donations_d_currenc_a53a25_idx" ON "donations_donation" ("currency", "amount");
CREATE INDEX "gallery_gallery_cover_id_63ebf279" ON "gallery_gallery" ("cover_id");
CREATE UNIQUE INDEX "gallery_galleryitem_gallery_id_media_id_7491e414_uniq" ON "gallery_galleryitem" ("gallery_id", "media_id");
CREATE INDEX "gallery_galleryitem_gallery_id_f9f02e39" ON "gallery_galleryitem" ("gallery_id");
CREATE INDEX "gallery_galleryitem_media_id_d40f9481" ON "gallery_galleryitem" ("media_id");
CREATE UNIQUE INDEX "migration_importedrecord_run_id_source_type_source_id_83eab9e9_uniq" ON "migration_importedrecord" ("run_id", "source_type", "source_id");
CREATE INDEX "migration_importedrecord_run_id_11276b51" ON "migration_importedrecord" ("run_id");
CREATE INDEX "newsletter__is_acti_b7fe03_idx" ON "newsletter_subscriber" ("is_active");
CREATE INDEX "pages_page_cover_image_id_06b868d3" ON "pages_page" ("cover_image_id");
CREATE INDEX "pages_report_validated_by_id_46ef569c" ON "pages_report" ("validated_by_id");
CREATE INDEX "partners_partner_logo_id_0b63c998" ON "partners_partner" ("logo_id");
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE INDEX "testimonials_testimonial_photo_id_f8f7fc9f" ON "testimonials_testimonial" ("photo_id");
CREATE INDEX "testimonials_testimonial_related_project_id_9148f409" ON "testimonials_testimonial" ("related_project_id");
CREATE INDEX "testimonials_testimonial_validated_by_id_73efc2d9" ON "testimonials_testimonial" ("validated_by_id");
CREATE INDEX "statistics_statistic_updated_by_id_bfd315c5" ON "statistics_statistic" ("updated_by_id");
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('django_migrations',37);
INSERT INTO "sqlite_sequence" VALUES('django_content_type',35);
INSERT INTO "sqlite_sequence" VALUES('auth_permission',140);
INSERT INTO "sqlite_sequence" VALUES('auth_group',6);
INSERT INTO "sqlite_sequence" VALUES('django_admin_log',0);
INSERT INTO "sqlite_sequence" VALUES('donations_donation',6);
INSERT INTO "sqlite_sequence" VALUES('core_sitesettings',1);
INSERT INTO "sqlite_sequence" VALUES('accounts_user',2);
INSERT INTO "sqlite_sequence" VALUES('programs_program',4);
INSERT INTO "sqlite_sequence" VALUES('projects_projectstatus',4);
INSERT INTO "sqlite_sequence" VALUES('pages_page',10);
INSERT INTO "sqlite_sequence" VALUES('migration_migrationrun',8);
INSERT INTO "sqlite_sequence" VALUES('articles_articlecategory',5);
INSERT INTO "sqlite_sequence" VALUES('articles_articletag',7);
INSERT INTO "sqlite_sequence" VALUES('migration_importedrecord',13);
INSERT INTO "sqlite_sequence" VALUES('migration_urlmapping',12);
INSERT INTO "sqlite_sequence" VALUES('media_mediacategory',1);
INSERT INTO "sqlite_sequence" VALUES('media_mediaitem',90);
INSERT INTO "sqlite_sequence" VALUES('articles_article',11);
INSERT INTO "sqlite_sequence" VALUES('articles_article_categories',13);
INSERT INTO "sqlite_sequence" VALUES('articles_article_tags',8);
INSERT INTO "sqlite_sequence" VALUES('payments_paymentprovider',4);
INSERT INTO "sqlite_sequence" VALUES('donations_donor',4);
INSERT INTO "sqlite_sequence" VALUES('payments_paymenttransaction',2);
INSERT INTO "sqlite_sequence" VALUES('contact_contactmessage',1);
INSERT INTO "sqlite_sequence" VALUES('projects_project',6);
INSERT INTO "sqlite_sequence" VALUES('statistics_statistic',1);
INSERT INTO "sqlite_sequence" VALUES('articles_article_related_images',12);
INSERT INTO "sqlite_sequence" VALUES('gallery_gallery',2);
INSERT INTO "sqlite_sequence" VALUES('gallery_galleryitem',12);
INSERT INTO "sqlite_sequence" VALUES('team_teammember',7);
INSERT INTO "sqlite_sequence" VALUES('partners_partner',1);
COMMIT;
