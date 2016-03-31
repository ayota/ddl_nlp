#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

corpus = """
Respiratory  2 0 1 5   E l s e v i e r   I n c .   A l l   r i g h t s   r e s e r v e d .Influenza is an acute respiratory illness that occurs virtually every year
and results in substantial disease, death and expense. Detection of Influenza
in its earliest stage would facilitate timely action that could reduce the
spread of the illness. Existing systems such as CDC and EISS which try to
collect diagnosis data, are almost entirely manual, resulting in about two-week
delays for clinical data acquisition. Twitter, a popular microblogging service,
provides us with a perfect source for early-stage flu detection due to its
real- time nature. For example, when a flu breaks out, people that get the flu
may post related tweets which enables the detection of the flu breakout
promptly. In this paper, we investigate the real-time flu detection problem on
Twitter data by proposing Flu Markov Network (Flu-MN): a spatio-temporal
unsupervised Bayesian algorithm based on a 4 phase Markov Network, trying to
identify the flu breakout at the earliest stage. We test our model on real
Twitter datasets from the United States along with baselines in multiple
applications, such as real-time flu breakout detection, future epidemic phase
prediction, or Influenza-like illness (ILI) physician visits. Experimental
results show the robustness and effectiveness of our approach. We build up a
real time flu reporting system based on the proposed approach, and we are
hopeful that it would help government or health organizations in identifying
flu outbreaks and facilitating timely actions to decrease unnecessary
mortality. A very inexpensive simple procedure for protection of humans against avian
flu that could blunt a pandemic is described.<p><span class="qt0">Fluis a respiratory infection caused by a number of viruses. The viruses pass through the air and enter your body through your nose or mouth. Between 5% and 20% of people in the U.S. get the <span class="qt0">flueach year.   The <span class="qt0">flucan be serious or even deadly for elderly people, newborn babies, and people with certain chronic illnesses.</p><p>Symptoms of the <span class="qt0">flucome on suddenly and are worse than those of the common cold. They may include
</p><ul><li>Body or muscle aches</li><li>Chills </li><li>Cough </li><li>Fever </li><li>Headache </li><li>Sore throat </li></ul><p>Is it a cold or the <span class="qt0">flu</span>?  Colds rarely cause a fever or headaches.  <span class="qt0">Flualmost never causes an upset stomach.  And <span class="qt0">"stomach flu" isn't really <span class="qt0">fluat all, but gastroenteritis.</p><p>Most people with the <span class="qt0">flurecover on their own without medical care. People with mild cases of the <span class="qt0">flushould stay home and avoid contact with others, except to get medical care. If you get the <span class="qt0">flu</span>, your health care provider may prescribe medicine to help your body fight the infection and lessen symptoms. </p><p>The main way to keep from getting the <span class="qt0">fluis to get a yearly <span class="qt0">fluvaccine. Good hygiene, including hand washing, can also help.</p><p>NIH: National Institute of Allergy and Infectious Diseases<p>Swine <span class="qt0">fluis an infection caused by a virus. It's named for a virus that pigs can get. People do not normally get swine <span class="qt0">flu</span>, but human infections can and do happen.  In 2009 a strain of swine <span class="qt0">flucalled H1N1 infected many people around the world.</p><p>The virus is contagious and can spread from human to human.   Symptoms of swine <span class="qt0">fluin people are similar to the symptoms of regular human <span class="qt0">fluand include fever, cough, sore throat, body aches, headache, chills and fatigue.</p><p>There are antiviral medicines you can take to prevent or treat swine <span class="qt0">flu</span>. There is a vaccine available to protect against swine <span class="qt0">flu</span>. You can help prevent the spread of germs that cause respiratory illnesses like <span class="qt0">influenzaby</p><ul><li>Covering your nose and mouth with a tissue when you cough or sneeze. Throw the tissue in the trash after you use it.</li><li>Washing your hands often with soap and water, especially after you cough or sneeze. You can also use alcohol-based hand cleaners.</li><li>Avoiding touching your eyes, nose or mouth. Germs spread this way.</li><li>Trying to avoid close contact with sick people.</li><li>Staying home from work or school if you are sick.</li></ul><p>Centers for Disease Control and Prevention</p>
Respiratory  2 0 1 5   E l s e v i e r   I n c .   A l l   r i g h t s   r e s e r v e d .Influenza is an acute respiratory illness that occurs virtually every year
and results in substantial disease, death and expense. Detection of Influenza
in its earliest stage would facilitate timely action that could reduce the
spread of the illness. Existing systems such as CDC and EISS which try to
collect diagnosis data, are almost entirely manual, resulting in about two-week
delays for clinical data acquisition. Twitter, a popular microblogging service,
provides us with a perfect source for early-stage flu detection due to its
real- time nature. For example, when a flu breaks out, people that get the flu
may post related tweets which enables the detection of the flu breakout
promptly. In this paper, we investigate the real-time flu detection problem on
Twitter data by proposing Flu Markov Network (Flu-MN): a spatio-temporal
unsupervised Bayesian algorithm based on a 4 phase Markov Network, trying to
identify the flu breakout at the earliest stage. We test our model on real
Twitter datasets from the United States along with baselines in multiple
applications, such as real-time flu breakout detection, future epidemic phase
prediction, or Influenza-like illness (ILI) physician visits. Experimental
results show the robustness and effectiveness of our approach. We build up a
real time flu reporting system based on the proposed approach, and we are
hopeful that it would help government or health organizations in identifying
flu outbreaks and facilitating timely actions to decrease unnecessary
mortality. A very inexpensive simple procedure for protection of humans against avian
flu that could blunt a pandemic is described.<p><span class="qt0">Fluis a respiratory infection caused by a number of viruses. The viruses pass through the air and enter your body through your nose or mouth. Between 5% and 20% of people in the U.S. get the <span class="qt0">flueach year.   The <span class="qt0">flucan be serious or even deadly for elderly people, newborn babies, and people with certain chronic illnesses.</p><p>Symptoms of the <span class="qt0">flucome on suddenly and are worse than those of the common cold. They may include
</p><ul><li>Body or muscle aches</li><li>Chills </li><li>Cough </li><li>Fever </li><li>Headache </li><li>Sore throat </li></ul><p>Is it a cold or the <span class="qt0">flu</span>?  Colds rarely cause a fever or headaches.  <span class="qt0">Flualmost never causes an upset stomach.  And <span class="qt0">"stomach flu" isn't really <span class="qt0">fluat all, but gastroenteritis.</p><p>Most people with the <span class="qt0">flurecover on their own without medical care. People with mild cases of the <span class="qt0">flushould stay home and avoid contact with others, except to get medical care. If you get the <span class="qt0">flu</span>, your health care provider may prescribe medicine to help your body fight the infection and lessen symptoms. </p><p>The main way to keep from getting the <span class="qt0">fluis to get a yearly <span class="qt0">fluvaccine. Good hygiene, including hand washing, can also help.</p><p>NIH: National Institute of Allergy and Infectious Diseases<p>Swine <span class="qt0">fluis an infection caused by a virus. It's named for a virus that pigs can get. People do not normally get swine <span class="qt0">flu</span>, but human infections can and do happen.  In 2009 a strain of swine <span class="qt0">flucalled H1N1 infected many people around the world.</p><p>The virus is contagious and can spread from human to human.   Symptoms of swine <span class="qt0">fluin people are similar to the symptoms of regular human <span class="qt0">fluand include fever, cough, sore throat, body aches, headache, chills and fatigue.</p><p>There are antiviral medicines you can take to prevent or treat swine <span class="qt0">flu</span>. There is a vaccine available to protect against swine <span class="qt0">flu</span>. You can help prevent the spread of germs that cause respiratory illnesses like <span class="qt0">influenzaby</p><ul><li>Covering your nose and mouth with a tissue when you cough or sneeze. Throw the tissue in the trash after you use it.</li><li>Washing your hands often with soap and water, especially after you cough or sneeze. You can also use alcohol-based hand cleaners.</li><li>Avoiding touching your eyes, nose or mouth. Germs spread this way.</li><li>Trying to avoid close contact with sick people.</li><li>Staying home from work or school if you are sick.</li></ul><p>Centers for Disease Control and Prevention</p>
Cancer is a group of diseases involving abnormal cell growth with the potential to invade or spread to other parts of the body. Not all tumors are cancerous; benign tumors do not spread to other parts of the body. Possible signs and symptoms include: a new lump, abnormal bleeding, a prolonged cough, unexplained weight loss, and a change in bowel movements among others. While these symptoms may indicate cancer, they may also occur due to other issues. There are over 100 different known cancers that affect humans.
Tobacco use is the cause of about 22% of cancer deaths. Another 10% is due to obesity, a poor diet, lack of physical activity, and consumption of alcohol. Other factors include certain infections, exposure to ionizing radiation, and environmental pollutants. In the developing world nearly 20% of cancers are due to infections such as hepatitis B, hepatitis C, and human papillomavirus (HPV). These factors act, at least partly, by changing the genes of a cell. Typically many such genetic changes are required before cancer develops. Approximately 5–10% of cancers are due to genetic defects inherited from a person's parents. Cancer can be detected by certain signs and symptoms or screening tests. It is then typically further investigated by medical imaging and confirmed by biopsy.
Many cancers can be prevented by not smoking, maintaining a healthy weight, not drinking too much alcohol, eating plenty of vegetables, fruits and whole grains, being vaccinated against certain infectious diseases, not eating too much processed and red meat, and avoiding too much exposure to sunlight. Early detection through screening is useful for cervical and colorectal cancer. The benefits of screening in breast cancer are controversial. Cancer is often treated with some combination of radiation therapy, surgery, chemotherapy, and targeted therapy. Pain and symptom management are an important part of care. Palliative care is particularly important in those with advanced disease. The chance of survival depends on the type of cancer and extent of disease at the start of treatment. In children under 15 at diagnosis the five-year survival rate in the developed world is on average 80%. For cancer in the United States the average five-year survival rate is 66%.
In 2012 about 14.1 million new cases of cancer occurred globally (not including skin cancer other than melanoma). It caused about 8.2 million deaths or 14.6% of all human deaths. The most common types of cancer in males are lung cancer, prostate cancer, colorectal cancer, and stomach cancer, and in females, the most common types are breast cancer, colorectal cancer, lung cancer, and cervical cancer. If skin cancer other than melanoma were included in total new cancers each year it would account for around 40% of cases. In children, acute lymphoblastic leukaemia and brain tumors are most common except in Africa where non-Hodgkin lymphoma occurs more often. In 2012, about 165,000 children under 15 years of age were diagnosed with cancer. The risk of cancer increases significantly with age and many cancers occur more commonly in developed countries. Rates are increasing as more people live to an old age and as lifestyle changes occur in the developing world. The financial costs of cancer have been estimated at $1.16 trillion US dollars per year as of 2010.


== Definitions ==
Cancers are a large family of diseases that involve abnormal cell growth with the potential to invade or spread to other parts of the body. They form a subset of neoplasms. A neoplasm or tumor is a group of cells that have undergone unregulated growth, and will often form a mass or lump, but may be distributed diffusely.
All tumor cells show the six hallmarks of cancer. These are characteristics that the cancer cells need to produce a malignant tumor. They include:
Cell growth and division without the proper signals to do so
Continuous growth and division even when there are signals telling them to stop
Avoidance of programmed cell death
Limitless number of cell divisions
Promoting blood vessel construction
Invasion of tissue and formation of metastases
The progression from normal cells to cells that can form a detectable mass to outright cancer involves multiple steps known as malignant progression.


== Signs and symptoms ==

When cancer begins, it invariably produces no symptoms. Signs and symptoms only appear as the mass continues to grow or ulcerates. The findings that result depend on the type and location of the cancer. Few symptoms are specific, with many of them also frequently occurring in individuals who have other conditions. Cancer is the new "great imitator". Thus, it is not uncommon for people diagnosed with cancer to have been treated for other diseases, which were assumed to be causing their symptoms.


=== Local effects ===
Local symptoms may occur due to the mass of the tumor or its ulceration. For example, mass effects from lung cancer can cause blockage of the bronchus resulting in cough or pneumonia; esophageal cancer can cause narrowing of the esophagus, making it difficult or painful to swallow; and colorectal cancer may lead to narrowing or blockages in the bowel, resulting in changes in bowel habits. Masses in breasts or testicles may be easily felt. Ulceration can cause bleeding that, if it occurs in the lung, will lead to coughing up blood, in the bowels to anemia or rectal bleeding, in the bladder to blood in the urine, and in the uterus to vaginal bleeding. Although localized pain may occur in advanced cancer, the initial swelling is usually painless. Some cancers can cause a buildup of fluid within the chest or abdomen.


=== Systemic symptoms ===
General symptoms occur due to distant effects of the cancer that are not related to direct or metastatic spread. These may include: unintentional weight loss, fever, being excessively tired, and changes to the skin. Hodgkin disease, leukemias, and cancers of the liver or kidney can cause a persistent fever of unknown origin.
Some cancers may cause specific groups of systemic symptoms, termed paraneoplastic phenomena. Examples include the appearance of myasthenia gravis in thymoma and clubbing in lung cancer.


=== Metastasis ===

Cancer can spread from its original site by local spread, lymphatic spread to regional lymph nodes or by blood (haematogenous spread) to distant sites, known as metastasis. When cancer spreads by a haematogenous route, it usually spreads all over the body. However, cancer 'seeds' grow in certain selected site only ('soil') as hypothesized in the soil and seed hypothesis of cancer metastasis. The symptoms of metastatic cancers depend on the location of the tumor, and can include enlarged lymph nodes (which can be felt or sometimes seen under the skin and are typically hard), enlarged liver or enlarged spleen, which can be felt in the abdomen, pain or fracture of affected bones, and neurological symptoms.


== Causes ==

The great majority of cancers, some 90–95% of cases, are due to environmental factors. The remaining 5–10% are due to inherited genetics. Environmental, as used by cancer researchers, means any cause that is not inherited genetically, such as lifestyle, economic and behavioral factors, and not merely pollution. Common environmental factors that contribute to cancer death include tobacco (25–30%), diet and obesity (30–35%), infections (15–20%), radiation (both ionizing and non-ionizing, up to 10%), stress, lack of physical activity, and environmental pollutants.
It is nearly impossible to prove what caused a cancer in any individual, because most cancers have multiple possible causes. For example, if a person who uses tobacco heavily develops lung cancer, then it was probably caused by the tobacco use, but since everyone has a small chance of developing lung cancer as a result of air pollution or radiation, then there is a small chance that the cancer developed because of air pollution or radiation. Excepting the rare transmissions that occur with pregnancies and only a marginal few organ donors, cancer is generally not a transmissible disease.


=== Chemicals ===

Exposure to particular substances have been linked to specific types of cancer. These substances are called carcinogens. Tobacco smoking, for example, causes 90% of lung cancer. It also causes cancer in the larynx, head, neck, stomach, bladder, kidney, esophagus and pancreas. Tobacco smoke contains over fifty known carcinogens, including nitrosamines and polycyclic aromatic hydrocarbons. Tobacco is responsible for about one in three of all cancer deaths in the developed world, and about one in five worldwide. Lung cancer death rates in the United States have mirrored smoking patterns, with increases in smoking followed by dramatic increases in lung cancer death rates and, more recently, decreases in smoking rates since the 1950s followed by decreases in lung cancer death rates in men since 1990.
In Western Europe, 10% of cancers in males and 3% of all cancers in females are attributed to alcohol exposure, especially cancer of the liver and of the digestive tract. Cancer related to substance exposures at work is believed to represent between 2–20% of all cases. Every year, at least 200,000 people die worldwide from cancer related to their workplaces. Millions of workers run the risk of developing cancers such as lung cancer and mesothelioma from inhaling tobacco smoke or asbestos fibers on the job, or leukemia from exposure to benzene at their workplaces.


=== Diet and exercise ===

Diet, physical inactivity, and obesity are related to up to 30–35% of cancer deaths. In the United States excess body weight is associated with the development of many types of cancer and is a factor in 14–20% of all cancer deaths. Correspondingly, a UK study including data on over 5 million people showed higher body mass index to be related to at least 10 types of cancer, and responsible for around 12,000 cases each year in that country. Physical inactivity is believed to contribute to cancer risk, not only through its effect on body weight but also through negative effects on the immune system and endocrine system. More than half of the effect from diet is due to overnutrition (eating too much), rather than from eating too few vegetables or other healthful foods.
Some specific foods are linked to specific cancers. A high-salt diet is linked to gastric cancer. Aflatoxin B1, a frequent food contaminate, causes liver cancer. Betel nut chewing causes oral cancer. The differences in dietary practices may partly explain differences in cancer incidence in different countries. For example, gastric cancer is more common in Japan due to its high-salt diet and colon cancer is more common in the United States. Immigrants develop the risk of their new country, often within one generation, suggesting a substantial link between diet and cancer.


=== Infection ===

Worldwide approximately 18% of cancer deaths are related to infectious diseases. This proportion varies in different regions of the world from a high of 25% in Africa to less than 10% in the developed world. Viruses are the usual infectious agents that cause cancer but cancer bacteria and parasites may also have an effect.
A virus that can cause cancer is called an oncovirus. These include human papillomavirus (cervical cancer), Epstein–Barr virus (B-cell lymphoproliferative disease and nasopharyngeal carcinoma), Kaposi's sarcoma herpesvirus (Kaposi's sarcoma and primary effusion lymphomas), hepatitis B and hepatitis C viruses (hepatocellular carcinoma), and human T-cell leukemia virus-1 (T-cell leukemias). Bacterial infection may also increase the risk of cancer, as seen in Helicobacter pylori-induced gastric carcinoma. Parasitic infections strongly associated with cancer include Schistosoma haematobium (squamous cell carcinoma of the bladder) and the liver flukes, Opisthorchis viverrini and Clonorchis sinensis (cholangiocarcinoma).


=== Radiation ===

Up to 10% of invasive cancers are related to radiation exposure, including both ionizing radiation and non-ionizing ultraviolet radiation. Additionally, the vast majority of non-invasive cancers are non-melanoma skin cancers caused by non-ionizing ultraviolet radiation, mostly from sunlight. Sources of ionizing radiation include medical imaging and radon gas.
Ionizing radiation is not a particularly strong mutagen. Residential exposure to radon gas, for example, has similar cancer risks as passive smoking. Radiation is a more potent source of cancer when it is combined with other cancer-causing agents, such as radon gas exposure plus smoking tobacco. Radiation can cause cancer in most parts of the body, in all animals, and at any age. Children and adolescents are twice as likely to develop radiation-induced leukemia as adults; radiation exposure before birth has ten times the effect.
Medical use of ionizing radiation is a small but growing source of radiation-induced cancers. Ionizing radiation may be used to treat other cancers, but this may, in some cases, induce a second form of cancer. It is also used in some kinds of medical imaging.
Prolonged exposure to ultraviolet radiation from the sun can lead to melanoma and other skin malignancies. Clear evidence establishes ultraviolet radiation, especially the non-ionizing medium wave UVB, as the cause of most non-melanoma skin cancers, which are the most common forms of cancer in the world.
Non-ionizing radio frequency radiation from mobile phones, electric power transmission, and other similar sources have been described as a possible carcinogen by the World Health Organization's International Agency for Research on Cancer. However, studies have not found a consistent link between cell phone radiation and cancer risk.


=== Heredity ===

The vast majority of cancers are non-hereditary ("sporadic cancers"). Hereditary cancers are primarily caused by an inherited genetic defect. Less than 0.3% of the population are carriers of a genetic mutation that has a large effect on cancer risk and these cause less than 3–10% of all cancer. Some of these syndromes include: certain inherited mutations in the genes BRCA1 and BRCA2 with a more than 75% risk of breast cancer and ovarian cancer, and hereditary nonpolyposis colorectal cancer (HNPCC or Lynch syndrome), which is present in about 3% of people with colorectal cancer, among others.


=== Physical agents ===
Some substances cause cancer primarily through their physical, rather than chemical, effects on cells. A prominent example of this is prolonged exposure to asbestos, naturally occurring mineral fibers that are a major cause of mesothelioma, which is a cancer of the serous membrane, usually the serous membrane surrounding the lungs. Other substances in this category, including both naturally occurring and synthetic asbestos-like fibers, such as wollastonite, attapulgite, glass wool, and rock wool, are believed to have similar effects. Non-fibrous particulate materials that cause cancer include powdered metallic cobalt and nickel, and crystalline silica (quartz, cristobalite, and tridymite). Usually, physical carcinogens must get inside the body (such as through inhaling tiny pieces) and require years of exposure to develop cancer.
Physical trauma resulting in cancer is relatively rare. Claims that breaking bones resulted in bone cancer, for example, have never been proven. Similarly, physical trauma is not accepted as a cause for cervical cancer, breast cancer, or brain cancer. One accepted source is frequent, long-term application of hot objects to the body. It is possible that repeated burns on the same part of the body, such as those produced by kanger and kairo heaters (charcoal hand warmers), may produce skin cancer, especially if carcinogenic chemicals are also present. Frequently drinking scalding hot tea may produce esophageal cancer. Generally, it is believed that the cancer arises, or a pre-existing cancer is encouraged, during the process of repairing the trauma, rather than the cancer being caused directly by the trauma. However, repeated injuries to the same tissues might promote excessive cell proliferation, which could then increase the odds of a cancerous mutation.
It is controversial whether chronic inflammation can directly cause mutation. It is recognized, however, that inflammation can contribute to proliferation, survival, angiogenesis and migration of cancer cells by influencing the microenvironment around tumors. Furthermore, oncogenes are known to build up an inflammatory pro-tumorigenic microenvironment.


=== Hormones ===
Some hormones play a role in the development of cancer by promoting cell proliferation. Insulin-like growth factors and their binding proteins play a key role in cancer cell proliferation, differentiation and apoptosis, suggesting possible involvement in carcinogenesis.
Hormones are important agents in sex-related cancers, such as cancer of the breast, endometrium, prostate, ovary, and testis, and also of thyroid cancer and bone cancer. For example, the daughters of women who have breast cancer have significantly higher levels of estrogen and progesterone than the daughters of women without breast cancer. These higher hormone levels may explain why these women have higher risk of breast cancer, even in the absence of a breast-cancer gene. Similarly, men of African ancestry have significantly higher levels of testosterone than men of European ancestry, and have a correspondingly much higher level of prostate cancer. Men of Asian ancestry, with the lowest levels of testosterone-activating androstanediol glucuronide, have the lowest levels of prostate cancer.
Other factors are also relevant: obese people have higher levels of some hormones associated with cancer and a higher rate of those cancers. Women who take hormone replacement therapy have a higher risk of developing cancers associated with those hormones. On the other hand, people who exercise far more than average have lower levels of these hormones, and lower risk of cancer. Osteosarcoma may be promoted by growth hormones. Some treatments and prevention approaches leverage this cause by artificially reducing hormone levels, and thus discouraging hormone-sensitive cancers.


== Pathophysiology ==


=== Genetics ===
Cancer is fundamentally a disease of tissue growth regulation failure. In order for a normal cell to transform into a cancer cell, the genes that regulate cell growth and differentiation must be altered.
The affected genes are divided into two broad categories. Oncogenes are genes that promote cell growth and reproduction. Tumor suppressor genes are genes that inhibit cell division and survival. Malignant transformation can occur through the formation of novel oncogenes, the inappropriate over-expression of normal oncogenes, or by the under-expression or disabling of tumor suppressor genes. Typically, changes in many genes are required to transform a normal cell into a cancer cell.
Genetic changes can occur at different levels and by different mechanisms. The gain or loss of an entire chromosome can occur through errors in mitosis. More common are mutations, which are changes in the nucleotide sequence of genomic DNA.
Large-scale mutations involve the deletion or gain of a portion of a chromosome. Genomic amplification occurs when a cell gains many copies (often 20 or more) of a small chromosomal locus, usually containing one or more oncogenes and adjacent genetic material. Translocation occurs when two separate chromosomal regions become abnormally fused, often at a characteristic location. A well-known example of this is the Philadelphia chromosome, or translocation of chromosomes 9 and 22, which occurs in chronic myelogenous leukemia, and results in production of the BCR-abl fusion protein, an oncogenic tyrosine kinase.
Small-scale mutations include point mutations, deletions, and insertions, which may occur in the promoter region of a gene and affect its expression, or may occur in the gene's coding sequence and alter the function or stability of its protein product. Disruption of a single gene may also result from integration of genomic material from a DNA virus or retrovirus, leading to the expression of viral oncogenes in the affected cell and its descendants.
Replication of the enormous amount of data contained within the DNA of living cells will probabilistically result in some errors (mutations). Complex error correction and prevention is built into the process, and safeguards the cell against cancer. If significant error occurs, the damaged cell can "self-destruct" through programmed cell death, termed apoptosis. If the error control processes fail, then the mutations will survive and be passed along to daughter cells.
Some environments make errors more likely to arise and propagate. Such environments can include the presence of disruptive substances called carcinogens, repeated physical injury, heat, ionising radiation, or hypoxia.
The errors that cause cancer are self-amplifying and compounding, for example:
A mutation in the error-correcting machinery of a cell might cause that cell and its children to accumulate errors more rapidly.
A further mutation in an oncogene might cause the cell to reproduce more rapidly and more frequently than its normal counterparts.
A further mutation may cause loss of a tumor suppressor gene, disrupting the apoptosis signalling pathway and resulting in the cell becoming immortal.
A further mutation in signaling machinery of the cell might send error-causing signals to nearby cells.
The transformation of normal cell into cancer is akin to a chain reaction caused by initial errors, which compound into more severe errors, each progressively allowing the cell to escape the controls that limit normal tissue growth. This rebellion-like scenario becomes an undesirable survival of the fittest, where the driving forces of evolution work against the body's design and enforcement of order. Once cancer has begun to develop, this ongoing process, termed clonal evolution, drives progression towards more invasive stages. Clonal evolution leads to intra-tumour heterogeneity that complicates designing effective treatment strategies.
Characteristic abilities developed by cancers are divided into a number of categories. Six categories were originally proposed, in a 2000 article called "The Hallmarks of Cancer" by Douglas Hanahan and Robert Weinberg: evasion of apoptosis, self-sufficiency in growth signals, insensitivity to anti-growth signals, sustained angiogenesis, limitless replicative potential, and metastasis. Based on further work, the same authors added two more categories in 2011: reprogramming of energy metabolism and evasion of immune destruction.


=== Epigenetics ===

Classically, cancer has been viewed as a set of diseases that are driven by progressive genetic abnormalities that include mutations in tumor-suppressor genes and oncogenes, and chromosomal abnormalities. However, it has become apparent that cancer is also driven by epigenetic alterations.
Epigenetic alterations refer to functionally relevant modifications to the genome that do not involve a change in the nucleotide sequence. Examples of such modifications are changes in DNA methylation (hypermethylation and hypomethylation) and histone modification and changes in chromosomal architecture (caused by inappropriate expression of proteins such as HMGA2 or HMGA1). Each of these epigenetic alterations serves to regulate gene expression without altering the underlying DNA sequence. These changes may remain through cell divisions, last for multiple generations, and can be considered to be epimutations (equivalent to mutations).
Epigenetic alterations occur frequently in cancers. As an example, Schnekenburger and Diederich listed protein coding genes that were frequently altered in their methylation in association with colon cancer. These included 147 hypermethylated and 27 hypomethylated genes. Of the hypermethylated genes, 10 were hypermethylated in 100% of colon cancers, and many others were hypermethylated in more than 50% of colon cancers.
While large numbers of epigenetic alterations are found in cancers, the epigenetic alterations in DNA repair genes, causing reduced expression of DNA repair proteins, may be of particular importance. Such alterations are thought to occur early in progression to cancer and to be a likely cause of the genetic instability characteristic of cancers.
Reduced expression of DNA repair genes causes deficient DNA repair. This is shown in the figure at the 4th level from the top. (In the figure, red wording indicates the central role of DNA damage and defects in DNA repair in progression to cancer.) When DNA repair is deficient DNA damages remain in cells at a higher than usual level (5th level from the top in figure), and these excess damages cause increased frequencies of mutation and/or epimutation (6th level from top of figure). Mutation rates increase substantially in cells defective in DNA mismatch repair or in homologous recombinational repair (HRR). Chromosomal rearrangements and aneuploidy also increase in HRR defective cells.
Higher levels of DNA damage not only cause increased mutation (right side of figure), but also cause increased epimutation. During repair of DNA double strand breaks, or repair of other DNA damages, incompletely cleared sites of repair can cause epigenetic gene silencing.
Deficient expression of DNA repair proteins due to an inherited mutation can cause an increased risk of cancer. Individuals with an inherited impairment in any of 34 DNA repair genes (see article DNA repair-deficiency disorder) have an increased risk of cancer, with some defects causing up to a 100% lifetime chance of cancer (e.g. p53 mutations). Germ line DNA repair mutations are noted in a box on the left side of the figure, with an arrow indicating their contribution to DNA repair deficiency. However, such germline mutations (which cause highly penetrant cancer syndromes) are the cause of only about 1 percent of cancers.
In sporadic cancers, deficiencies in DNA repair are occasionally caused by a mutation in a DNA repair gene, but are much more frequently caused by epigenetic alterations that reduce or silence expression of DNA repair genes. This is indicated in the figure at the 3rd level from the top. Many studies of heavy metal-induced carcinogenesis show that such heavy metals cause reduction in expression of DNA repair enzymes, some through epigenetic mechanisms. In some cases, DNA repair inhibition is proposed to be a predominant mechanism in heavy metal-induced carcinogenicity. In addition, there are frequent epigenetic alterations of the DNA sequences coding for small RNAs called microRNAs (or miRNAs). MiRNAs do not code for proteins, but can "target" protein-coding genes and reduce their expression.
Cancers usually arise from an assemblage of mutations and epimutations that confer a selective advantage leading to clonal expansion (see Field defects in progression to cancer). Mutations, however, may not be as frequent in cancers as epigenetic alterations. An average cancer of the breast or colon can have about 60 to 70 protein-altering mutations, of which about three or four may be "driver" mutations, and the remaining ones may be "passenger" mutations.
As pointed out above under genetic alterations, cancer is caused by failure to regulate tissue growth, when the genes that regulate cell growth and differentiation are altered. It has become clear that these alterations are caused by both DNA sequence mutation in oncogenes and tumor suppressor genes as well as by epigenetic alterations. The epigenetic deficiencies in expression of DNA repair genes, in particular, likely cause an increased frequency of mutations, some of which then occur in oncogenes and tumor suppressor genes.


=== Metastasis ===

Metastasis is the spread of cancer to other locations in the body. The new tumors are called metastatic tumors, while the original is called the primary tumor. Almost all cancers can metastasize. Most cancer deaths are due to cancer that has spread from its primary site to other organs (metastasized).
Metastasis is very common in the late stages of cancer, and it can occur via the blood or the lymphatic system or both. The typical steps in metastasis are local invasion, intravasation into the blood or lymph, circulation through the body, extravasation into the new tissue, proliferation, and angiogenesis. Different types of cancers tend to metastasize to particular organs, but overall the most common places for metastases to occur are the lungs, liver, brain, and the bones.


== Diagnosis ==

Most cancers are initially recognized either because of the appearance of signs or symptoms or through screening. Neither of these lead to a definitive diagnosis, which requires the examination of a tissue sample by a pathologist. People with suspected cancer are investigated with medical tests. These commonly include blood tests, X-rays, CT scans and endoscopy.
Most people are distressed to learn that they have cancer. They may become extremely anxious and depressed. The risk of suicide in people with cancer is approximately double the normal risk.


=== Classification ===

Cancers are classified by the type of cell that the tumor cells resemble and is therefore presumed to be the origin of the tumor. These types include:
Carcinoma: Cancers derived from epithelial cells. This group includes many of the most common cancers, particularly in the aged, and include nearly all those developing in the breast, prostate, lung, pancreas, and colon.
Sarcoma: Cancers arising from connective tissue (i.e. bone, cartilage, fat, nerve), each of which develops from cells originating in mesenchymal cells outside the bone marrow.
Lymphoma and leukemia: These two classes of cancer arise from hematopoietic (blood-forming) cells that leave the marrow and tend to mature in the lymph nodes and blood, respectively. Leukemia is the most common type of cancer in children accounting for about 30%.
Germ cell tumor: Cancers derived from pluripotent cells, most often presenting in the testicle or the ovary (seminoma and dysgerminoma, respectively).
Blastoma: Cancers derived from immature "precursor" cells or embryonic tissue. Blastomas are more common in children than in older adults.
Cancers are usually named using -carcinoma, -sarcoma or -blastoma as a suffix, with the Latin or Greek word for the organ or tissue of origin as the root. For example, cancers of the liver parenchyma arising from malignant epithelial cells is called hepatocarcinoma, while a malignancy arising from primitive liver precursor cells is called a hepatoblastoma, and a cancer arising from fat cells is called a liposarcoma. For some common cancers, the English organ name is used. For example, the most common type of breast cancer is called ductal carcinoma of the breast. Here, the adjective ductal refers to the appearance of the cancer under the microscope, which suggests that it has originated in the milk ducts.
Benign tumors (which are not cancers) are named using -oma as a suffix with the organ name as the root. For example, a benign tumor of smooth muscle cells is called a leiomyoma (the common name of this frequently occurring benign tumor in the uterus is fibroid). Confusingly, some types of cancer use the -noma suffix, examples including melanoma and seminoma.
Some types of cancer are named for the size and shape of the cells under a microscope, such as giant cell carcinoma, spindle cell carcinoma, and small-cell carcinoma.


=== Pathology ===
The tissue diagnosis given by the pathologist indicates the type of cell that is proliferating, its histological grade, genetic abnormalities, and other features of the tumor. Together, this information is useful to evaluate the prognosis of the patient and to choose the best treatment. Cytogenetics and immunohistochemistry are other types of testing that the pathologist may perform on the tissue specimen. These tests may provide information about the molecular changes (such as mutations, fusion genes, and numerical chromosome changes) that have happened in the cancer cells, and may thus also indicate the future behavior of the cancer (prognosis) and best treatment.


== Prevention ==

Cancer prevention is defined as active measures to decrease the risk of cancer. The vast majority of cancer cases are due to environmental risk factors, and many, but not all, of these environmental factors are controllable lifestyle choices. Thus, cancer is considered a largely preventable disease. Between 70% and 90% of common cancers are due to environmental factors and therefore possibly preventable.
Greater than 30% of cancer deaths could be prevented by avoiding risk factors including: tobacco, overweight / obesity, an insufficient diet, physical inactivity, alcohol, sexually transmitted infections, and air pollution. Not all environmental causes are controllable, such as naturally occurring background radiation, and other cases of cancer are caused through hereditary genetic disorders, and thus it is not possible to prevent all cases of cancer.


=== Dietary ===

While many dietary recommendations have been proposed to reduce the risk of cancer, the evidence to support them is not definitive. The primary dietary factors that increase risk are obesity and alcohol consumption; with a diet low in fruits and vegetables and high in red meat being implicated but not confirmed. A 2014 meta-analysis did not find a relationship between fruits and vegetables and cancer. Consumption of coffee is associated with a reduced risk of liver cancer. Studies have linked excessive consumption of red or processed meat to an increased risk of breast cancer, colon cancer, and pancreatic cancer, a phenomenon that could be due to the presence of carcinogens in meats cooked at high temperatures. This was confirmed in 2015 by the IARC of the World Health Organization, which determined that eating processed meat (e.g., bacon, ham, hot dogs, sausages) and, to a lesser degree, red meat was linked to some cancers.
Dietary recommendations for cancer prevention typically include an emphasis on vegetables, fruit, whole grains, and fish, and an avoidance of processed and red meat (beef, pork, lamb), animal fats, and refined carbohydrates.


=== Medication ===
The concept that medications can be used to prevent cancer is attractive, and evidence supports their use in a few defined circumstances. In the general population, NSAIDs reduce the risk of colorectal cancer, however due to the cardiovascular and gastrointestinal side effects they cause overall harm when used for prevention. Aspirin has been found to reduce the risk of death from cancer by about 7%. COX-2 inhibitor may decrease the rate of polyp formation in people with familial adenomatous polyposis, however it is associated with the same adverse effects as NSAIDs. Daily use of tamoxifen or raloxifene has been demonstrated to reduce the risk of developing breast cancer in high-risk women. The benefit versus harm for 5-alpha-reductase inhibitor such as finasteride is not clear.
Vitamins have not been found to be effective at preventing cancer, although low blood levels of vitamin D are correlated with increased cancer risk. Whether this relationship is causal and vitamin D supplementation is protective is not determined. Beta-Carotene supplementation has been found to increase lung cancer rates in those who are high risk. Folic acid supplementation has not been found effective in preventing colon cancer and may increase colon polyps. It is unclear if selenium supplementation has an effect.


=== Vaccination ===
Vaccines have been developed that prevent infection by some carcinogenic viruses. Human papillomavirus vaccine (Gardasil and Cervarix) decreases the risk of developing cervical cancer. The hepatitis B vaccine prevents infection with hepatitis B virus and thus decreases the risk of liver cancer. The administration of human papillomavirus and hepatitis B vaccinations is recommended when resources allow.


== Screening ==

Unlike diagnosis efforts prompted by symptoms and medical signs, cancer screening involves efforts to detect cancer after it has formed, but before any noticeable symptoms appear. This may involve physical examination, blood or urine tests, or medical imaging.
Cancer screening is currently not possible for many types of cancers, and even when tests are available, they may not be recommended for everyone. Universal screening or mass screening involves screening everyone. Selective screening identifies people who are known to be at higher risk of developing cancer, such as people with a family history of cancer. Several factors are considered to determine whether the benefits of screening outweigh the risks and the costs of screening. These factors include:
Possible harms from the screening test: for example, X-ray images involve exposure to potentially harmful ionizing radiation.
The likelihood of the test correctly identifying cancer.
The likelihood of cancer being present: Screening is not normally useful for rare cancers.
Possible harms from follow-up procedures.
Whether suitable treatment is available.
Whether early detection improves treatment outcomes.
Whether the cancer will ever need treatment.
Whether the test is acceptable to the people: If a screening test is too burdensome (for example, being extremely painful), then people will refuse to participate.
Cost of the test.


=== Recommendations ===
The U.S. Preventive Services Task Force (USPSTF) strongly recommends cervical cancer screening in women who are sexually active and have a cervix at least until the age of 65. They recommend that Americans be screened for colorectal cancer via fecal occult blood testing, sigmoidoscopy, or colonoscopy starting at age 50 until age 75. There is insufficient evidence to recommend for or against screening for skin cancer, oral cancer, lung cancer, or prostate cancer in men under 75. Routine screening is not recommended for bladder cancer, testicular cancer, ovarian cancer, pancreatic cancer, or prostate cancer.
The USPSTF recommends mammography for breast cancer screening every two years for those 50–74 years old; however, they do not recommend either breast self-examination or clinical breast examination. A 2011 Cochrane review came to slightly different conclusions with respect to breast cancer screening stating that routine mammography may do more harm than good.
Japan screens for gastric cancer using photofluorography due to the high incidence there.


=== Genetic testing ===

Genetic testing for individuals at high-risk of certain cancers is recommended. Carriers of these mutations may then undergo enhanced surveillance, chemoprevention, or preventative surgery to reduce their subsequent risk.


== Management ==

Many treatment options for cancer exist, with the primary ones including surgery, chemotherapy, radiation therapy, hormonal therapy, targeted therapy and palliative care. Which treatments are used depends on the type, location, and grade of the cancer as well as the person's health and wishes. The treatment intent may be curative or not curative.


=== Chemotherapy ===
Chemotherapy is the treatment of cancer with one or more cytotoxic anti-neoplastic drugs (chemotherapeutic agents) as part of a standardized regimen. The term encompasses any of a large variety of different anticancer drugs, which are divided into broad categories such as alkylating agents and antimetabolites. Traditional chemotherapeutic agents act by killing cells that divide rapidly, one of the main properties of most cancer cells.
Targeted therapy is a form of chemotherapy that targets specific molecular differences between cancer and normal cells. The first targeted therapies to be developed blocked the estrogen receptor molecule, inhibiting the growth of breast cancer. Another common example is the class of Bcr-Abl inhibitors, which are used to treat chronic myelogenous leukemia (CML). Currently, there are targeted therapies for breast cancer, multiple myeloma, lymphoma, prostate cancer, melanoma and other cancers.
The efficacy of chemotherapy depends on the type of cancer and the stage. In combination with surgery, chemotherapy has proven useful in a number of different cancer types including: breast cancer, colorectal cancer, pancreatic cancer, osteogenic sarcoma, testicular cancer, ovarian cancer, and certain lung cancers. The overall effectiveness ranges from being curative for some cancers, such as some leukemias, to being ineffective, such as in some brain tumors, to being needless in others, like most non-melanoma skin cancers. The effectiveness of chemotherapy is often limited by toxicity to other tissues in the body. Even when it is impossible for chemotherapy to provide a permanent cure, chemotherapy may be useful to reduce symptoms like pain or to reduce the size of an inoperable tumor in the hope that surgery will be possible in the future.


=== Radiation ===
Radiation therapy involves the use of ionizing radiation in an attempt to either cure or improve the symptoms of cancer. It works by damaging the DNA of cancerous tissue leading to cellular death. To spare normal tissues (such as skin or organs, which radiation must pass through to treat the tumor), shaped radiation beams are aimed from several angles of exposure to intersect at the tumor, providing a much larger absorbed dose there than in the surrounding, healthy tissue. As with chemotherapy, different cancers respond differently to radiation therapy.
Radiation therapy is used in about half of all cases and the radiation can be from either internal sources in the form of brachytherapy or external radiation sources. The radiation is most commonly low energy x-rays for treating skin cancers while higher energy x-ray beams are used in the treatment of cancers within the body. Radiation is typically used in addition to surgery and or chemotherapy but for certain types of cancer, such as early head and neck cancer, may be used alone. For painful bone metastasis, it has been found to be effective in about 70% of people.


=== Surgery ===
Surgery is the primary method of treatment of most isolated solid cancers and may play a role in palliation and prolongation of survival. It is typically an important part of making the definitive diagnosis and staging the tumor as biopsies are usually required. In localized cancer surgery typically attempts to remove the entire mass along with, in certain cases, the lymph nodes in the area. For some types of cancer this is all that is needed to eliminate the cancer.


=== Palliative care ===
Palliative care refers to treatment that attempts to make the person feel better and may or may not be combined with an attempt to treat the cancer. Palliative care includes action to reduce the physical, emotional, spiritual, and psycho-social distress experienced by people with cancer. Unlike treatment that is aimed at directly killing cancer cells, the primary goal of palliative care is to improve the person's quality of life.
People at all stages of cancer treatment should have some kind of palliative care to provide comfort. In some cases, medical specialty professional organizations recommend that people and physicians respond to cancer only with palliative care and not with cure-directed therapy. This includes:
people with low performance status, corresponding with limited ability to care for themselves
people who received no benefit from prior evidence-based treatments
people who are not eligible to participate in any appropriate clinical trial
people for whom the physician sees no strong evidence that treatment would be effective
Palliative care is often confused with hospice and therefore only involved when people approach end of life. Like hospice care, palliative care attempts to help the person cope with the immediate needs and to increase the person's comfort. Unlike hospice care, palliative care does not require people to stop treatment aimed at prolonging their lives or curing the cancer.
Multiple national medical guidelines recommend early palliative care for people whose cancer has produced distressing symptoms (pain, shortness of breath, fatigue, nausea) or who need help coping with their illness. In people who have metastatic disease when first diagnosed, oncologists should consider a palliative care consult immediately. Additionally, an oncologist should consider a palliative care consult in any person they feel has less than 12 months of life even if continuing aggressive treatment.


=== Immunotherapy ===

A variety of therapies using immunotherapy, stimulating or helping the immune system to fight cancer, have come into use since 1997, and this continues to be an area of very active research.


=== Alternative medicine ===
Complementary and alternative cancer treatments are a diverse group of health care systems, practices, and products that are not part of conventional medicine. "Complementary medicine" refers to methods and substances used along with conventional medicine, while "alternative medicine" refers to compounds used instead of conventional medicine. Most complementary and alternative medicines for cancer have not been rigorously studied or tested. Some alternative treatments have been investigated and shown to be ineffective but still continue to be marketed and promoted. Cancer researcher Andrew J. Vickers has stated: "The label 'unproven' is inappropriate for such therapies; it is time to assert that many alternative cancer therapies have been 'disproven'."


== Prognosis ==

Cancer has a reputation as a deadly disease. Taken as a whole, about half of people receiving treatment for invasive cancer (excluding carcinoma in situ and non-melanoma skin cancers) die from cancer or its treatment. Survival is worse in the developing world, partly because the types of cancer that are most common there are at present harder to treat than those associated with the lifestyle of developed countries. However, the survival rates vary dramatically by type of cancer, and by the stage at which it is diagnosed, with the range running from the great majority of people surviving to almost no one surviving as long as five years after diagnosis. Once a cancer has metastasized or spread beyond its original site, the prognosis normally becomes much worse.
Those who survive cancer are at increased risk of developing a second primary cancer at about twice the rate of those never diagnosed with cancer. The increased risk is believed to be primarily due to the same risk factors that produced the first cancer, partly due to the treatment for the first cancer, and potentially related to better compliance with screening.
Predicting either short-term or long-term survival is difficult and depends on many factors. The most important factors are the particular kind of cancer and the patient's age and overall health. People who are frail with many other health problems have lower survival rates than otherwise healthy people. A centenarian is unlikely to survive for five years even if the treatment is successful. People who report a higher quality of life tend to survive longer. People with lower quality of life may be affected by major depressive disorder and other complications from cancer treatment and/or disease progression that both impairs their quality of life and reduces their quantity of life. Additionally, patients with worse prognoses may be depressed or report a lower quality of life directly because they correctly perceive that their condition is likely to be fatal.
People with cancer, even those who are walking on their own, have an increased risk of blood clots in veins. The use of heparin appears improve survival and decrease the risk of blood clots.


== Epidemiology ==

In 2008, approximately 12.7 million cancers were diagnosed (excluding non-melanoma skin cancers and other non-invasive cancers), and in 2010 nearly 7.98 million people died. Cancers as a group account for approximately 13% of all deaths each year with the most common being: lung cancer (1.4 million deaths), stomach cancer (740,000 deaths), liver cancer (700,000 deaths), colorectal cancer (610,000 deaths), and breast cancer (460,000 deaths). This makes invasive cancer the leading cause of death in the developed world and the second leading cause of death in the developing world. Over half of cases occur in the developing world.
Deaths from cancer were 5.8 million in 1990 and rates have been increasing primarily due to an aging population and lifestyle changes in the developing world. The most significant risk factor for developing cancer is old age. Although it is possible for cancer to strike at any age, most people who are diagnosed with invasive cancer are over the age of 65. According to cancer researcher Robert A. Weinberg, "If we lived long enough, sooner or later we all would get cancer." Some of the association between aging and cancer is attributed to immunosenescence, errors accumulated in DNA over a lifetime, and age-related changes in the endocrine system. The effect of aging on cancer is complicated with a number of factors such as DNA damage and inflammation promoting it and a number of factors such as vascular aging and endocrine changes inhibiting it.
Some slow-growing cancers are particularly common. Autopsy studies in Europe and Asia have shown that up to 36% of people have undiagnosed and apparently harmless thyroid cancer at the time of their deaths, and that 80% of men develop prostate cancer by age 80. As these cancers did not cause the person's death, identifying them would have represented overdiagnosis rather than useful medical care.
The three most common childhood cancers are leukemia (34%), brain tumors (23%), and lymphomas (12%). In the United States cancer affects about 1 in 285 children. Rates of childhood cancer have increased by 0.6% per year between 1975 to 2002 in the United States and by 1.1% per year between 1978 and 1997 in Europe. Death from childhood cancer have decreased by half since 1975 in the United States.


== History ==

Cancer has existed for all of human history. The earliest written record regarding cancer is from circa 1600 BC in the Egyptian Edwin Smith Papyrus and describes cancer of the breast. Hippocrates (ca. 460 BC – ca. 370 BC) described several kinds of cancer, referring to them with the Greek word καρκίνος karkinos (crab or crayfish). This name comes from the appearance of the cut surface of a solid malignant tumor, with "the veins stretched on all sides as the animal the crab has its feet, whence it derives its name". Galen stated that "cancer of the breast is so called because of the fancied resemblance to a crab given by the lateral prolongations of the tumor and the adjacent distended veins". Celsus (ca. 25 BC – 50 AD) translated karkinos into the Latin cancer, also meaning crab and recommended surgery as treatment. Galen (2nd century AD) disagreed with the use of surgery and recommended purgatives instead. These recommendations largely stood for 1000 years.
In the 15th, 16th and 17th centuries, it became acceptable for doctors to dissect bodies to discover the cause of death. The German professor Wilhelm Fabry believed that breast cancer was caused by a milk clot in a mammary duct. The Dutch professor Francois de la Boe Sylvius, a follower of Descartes, believed that all disease was the outcome of chemical processes, and that acidic lymph fluid was the cause of cancer. His contemporary Nicolaes Tulp believed that cancer was a poison that slowly spreads, and concluded that it was contagious.
The physician John Hill described tobacco snuff as the cause of nose cancer in 1761. This was followed by the report in 1775 by British surgeon Percivall Pott that chimney sweeps' carcinoma, a cancer of the scrotum, was a common disease among chimney sweeps. With the widespread use of the microscope in the 18th century, it was discovered that the 'cancer poison' spread from the primary tumor through the lymph nodes to other sites ("metastasis"). This view of the disease was first formulated by the English surgeon Campbell De Morgan between 1871 and 1874.


== Society and culture ==
Though many diseases (such as heart failure) may have a worse prognosis than most cases of cancer, cancer is the subject of widespread fear and taboos. The euphemism "after a long illness" is still commonly used (2012), reflecting an apparent stigma. This deep belief that cancer is necessarily a difficult and usually deadly disease is reflected in the systems chosen by society to compile cancer statistics: the most common form of cancer—non-melanoma skin cancers, accounting for about one-third of all cancer cases worldwide, but very few deaths—are excluded from cancer statistics specifically because they are easily treated and almost always cured, often in a single, short, outpatient procedure.
Cancer is regarded as a disease that must be "fought" to end the "civil insurrection"; a War on Cancer has been declared. Military metaphors are particularly common in descriptions of cancer's human effects, and they emphasize both the parlous state of the affected individual's health and the need for the individual to take immediate, decisive actions himself, rather than to delay, to ignore, or to rely entirely on others caring for him. The military metaphors also help rationalize radical, destructive treatments.
In the 1970s, a relatively popular alternative cancer treatment was a specialized form of talk therapy, based on the idea that cancer was caused by a bad attitude. People with a "cancer personality"—depressed, repressed, self-loathing, and afraid to express their emotions—were believed to have manifested cancer through subconscious desire. Some psychotherapists said that treatment to change the patient's outlook on life would cure the cancer. Among other effects, this belief allows society to blame the victim for having caused the cancer (by "wanting" it) or having prevented its cure (by not becoming a sufficiently happy, fearless, and loving person). It also increases patients' anxiety, as they incorrectly believe that natural emotions of sadness, anger or fear shorten their lives. The idea was excoriated by the notoriously outspoken Susan Sontag, who published Illness as Metaphor while recovering from treatment for breast cancer in 1978. Although the original idea is now generally regarded as nonsense, the idea partly persists in a reduced form with a widespread, but incorrect, belief that deliberately cultivating a habit of positive thinking will increase survival. This notion is particularly strong in breast cancer culture.
One idea about why people with cancer are blamed or stigmatized, called the just-world hypothesis, is that blaming cancer on the patient's actions or attitudes allows the blamers to regain a sense of control. This is based upon the blamers' belief that the world is fundamentally just, and so any dangerous illness, like cancer, must be a type of punishment for bad choices, because in a just world, bad things would not happen to good people.


=== Economic effect ===
In 2007, the overall costs of cancer in the U.S. — including treatment and indirect mortality expenses (such as lost productivity in the workplace) — was estimated to be $226.8 billion. In 2009, 32% of Hispanics and 10% of children 17 years old or younger lacked health insurance; "uninsured patients and those from ethnic minorities are substantially more likely to be diagnosed with cancer at a later stage, when treatment can be more extensive and more costly."


== Research ==

Because cancer is a class of diseases, it is unlikely that there will ever be a single "cure for cancer" any more than there will be a single treatment for all infectious diseases. Angiogenesis inhibitors were once thought to have potential as a "silver bullet" treatment applicable to many types of cancer, but this has not been the case in practice. It is more likely that angiogenesis inhibitors and other cancer therapeutics will be used in combination to reduce cancer morbidity and mortality.
Experimental cancer treatments are treatments that are being studied to see whether they work. Typically, these are studied in clinical trials to compare the proposed treatment to the best existing treatment. They may be entirely new treatments, or they may be treatments that have been used successfully in one type of cancer, and are now being tested to see whether they are effective in another type. More and more, such treatments are being developed alongside companion diagnostic tests to target the right drugs to the right patients, based on their individual biology.
Cancer research is the intense scientific effort to understand disease processes and discover possible therapies.
Research about cancer causes focuses on the following issues:
Agents (e.g. viruses) and events (e.g. mutations) that cause or facilitate genetic changes in cells destined to become cancer.
The precise nature of the genetic damage, and the genes that are affected by it.
The consequences of those genetic changes on the biology of the cell, both in generating the defining properties of a cancer cell, and in facilitating additional genetic events that lead to further progression of the cancer.
The improved understanding of molecular biology and cellular biology due to cancer research has led to a number of new treatments for cancer since U.S. President Nixon declared the "War on Cancer" in 1971. Since then, the U.S. has spent over $200 billion on cancer research, including resources from the public and private sectors and foundations. During that time, the country has seen a five percent decrease in the cancer death rate (adjusting for size and age of the population) between 1950 and 2005.
Hypercompetition for the financial resources that are required to conduct science appears to suppress the creativity, cooperation, risk-taking, and original thinking required to make fundamental discoveries, unduly favoring low-risk research into small incremental advancements over innovative research that might discover radically new and dramatically improved therapy. Other consequences of the highly pressured competition for research resources appear to be a substantial number of research publications whose results cannot be replicated, and perverse incentives in research funding that encourage grantee institutions to grow without making sufficient investments in their own faculty and facilities.


== Pregnancy ==
Because cancer is largely a disease of older adults, it is not common in pregnant women. Cancer affects approximately 1 in 1,000 pregnant women. The most common cancers found during pregnancy are the same as the most common cancers found in non-pregnant women during childbearing ages: breast cancer, cervical cancer, leukemia, lymphoma, melanoma, ovarian cancer, and colorectal cancer.
Diagnosing a new cancer in a pregnant woman is difficult, in part because any symptoms are commonly assumed to be a normal discomfort associated with pregnancy. As a result, cancer is typically discovered at a somewhat later stage than average in many pregnant or recently pregnant women. Some imaging procedures, such as MRIs (magnetic resonance imaging), CT scans, ultrasounds, and mammograms with fetal shielding are considered safe during pregnancy; some others, such as PET scans are not.
Treatment is generally the same as for non-pregnant women. However, radiation and radioactive drugs are normally avoided during pregnancy, especially if the fetal dose might exceed 100 cGy. In some cases, some or all treatments are postponed until after birth if the cancer is diagnosed late in the pregnancy. Early deliveries to speed the start of treatment are not uncommon. Surgery is generally safe, but pelvic surgeries during the first trimester may cause miscarriage. Some treatments, especially certain chemotherapy drugs given during the first trimester, increase the risk of birth defects and pregnancy loss (spontaneous abortions and stillbirths).
Elective abortions are not required and, for the most common forms and stages of cancer, do not improve the likelihood of the mother surviving or being cured. In a few instances, such as advanced uterine cancer, the pregnancy cannot be continued, and in others, such as an acute leukemia discovered early in pregnancy, the pregnant woman may choose to have an abortion so that she can begin aggressive chemotherapy without worrying about birth defects.
Some treatments may interfere with the mother's ability to give birth vaginally or to breastfeed her baby. Cervical cancer may require birth by Caesarean section. Radiation to the breast reduces the ability of that breast to produce milk and increases the risk of mastitis. Also, when chemotherapy is being given after birth, many of the drugs pass through breast milk to the baby, which could harm the baby.


== Other animals ==
Veterinary oncology, concentrating mainly on cats and dogs, is a growing specialty in wealthy countries, and the major forms of human treatment such as surgery and radiotherapy may be offered. The most common types of cancer differ, but the cancer burden seems at least as high in pets as in humans. Animals, typically rodents, are often used in cancer research, and studies of natural cancers in larger animals may benefit research into human cancer.
In non-humans, a few types of transmissible cancer have been described, wherein the cancer spreads between animals by transmission of the tumor cells themselves. This phenomenon is seen in dogs with Sticker's sarcoma, also known as canine transmissible venereal tumor, as well as devil facial tumor disease in Tasmanian devils.


== Notes ==

References
Holland, James F. (2009). Holland-Frei cancer medicine. (8th ed.). New York: McGraw-Hill Medical. ISBN 978-1-60795-014-1. 


== Further reading ==
Kleinsmith, Lewis J. (2006). Principles of cancer biology. Pearson Benjamin Cummings. ISBN 978-0-8053-4003-7. 
Mukherjee, Siddhartha (16 November 2010). The Emperor of All Maladies: A Biography of Cancer. Simon & Schuster. ISBN 978-1-4391-0795-9. Retrieved August 7, 2013. 
Pazdur, Richard; et al. (May 2009). Cancer Management: A Multidisciplinary Approach. Cmp United Business Media. ISBN 978-1-891483-62-2.  (online at cancernetwork.com)
Tannock, Ian (2005). The basic science of oncology. McGraw-Hill Professional. ISBN 978-0-07-138774-3. 
Manfred Schwab (2008). Encyclopedia of Cancer (4 Volume Set). Berlin: Springer. ISBN 3-540-36847-7. 


== External links ==
Cancer at DMOZSubsequent  2 0 1 5   A m e r i c a n   C a n c e r   S o c i e t y .We present a general computational theory of cancer and its developmental
dynamics. The theory is based on a theory of the architecture and function of
developmental control networks which guide the formation of multicellular
organisms. Cancer networks are special cases of developmental control networks.
Cancer results from transformations of normal developmental networks. Our
theory generates a natural classification of all possible cancers based on
their network architecture. Each cancer network has a unique topology and
semantics and developmental dynamics that result in distinct clinical tumor
phenotypes. We apply this new theory with a series of proof of concept cases
for all the basic cancer types. These cases have been computationally modeled,
their behavior simulated and mathematically described using a multicellular
systems biology approach. There are fascinating correspondences between the
dynamic developmental phenotype of computationally modeledcancers. The theory lays the foundation for a
new research paradigm for understanding and investigating cancer. The theory of
cancer networks implies that new diagnostic methods and new treatments to cure
cancer will become possible. In recent years, cancer genome sequencing and other high-throughput studies
of cancer genomes have generated many notable discoveries. In this review,
Novel genomic alteration mechanisms, such as chromothripsis (chromosomal
crisis) and kataegis (mutation storms), and their implications for cancer are
discussed. Genomic alterations spur cancer genome evolution. Thus, the
relationship between cancer clonal evolution and cancer stems cells is
commented. The key question in cancer biology concerns how these genomic
alterations support cancer development and metastasis in the context of
biological functioning. Thus far, efforts such as pathway analysis have
improved the understanding of the functional contributions of genetic mutations
and DNA copy number variations to cancer development, progression and
metastasis. However, the known pathways correspond to a small fraction,
plausibly 5-10%, of somatic mutations and genes with an altered copy number. To
develop a comprehensive understanding of the function of these genomic
alterations in cancer, an integrative network framework is proposed and
discussed. Finally, the challenges and the directions of studying cancer omic
data using an integrative network approach are commented.<p><span class="qt0"><span class="qt1">Cancer</span>begins in your cells, which are the building blocks of your body.   Normally, your body forms new cells as you need them, replacing old cells that die. Sometimes this process goes wrong. New cells grow even when you don't need them, and old cells don't die when they should. These extra cells can form a mass called a <span class="qt0"><span class="qt1">tumor. Tumors</span>can be benign or malignant. Benign <span class="qt0"><span class="qt1">tumors</span>aren't <span class="qt0"><span class="qt1">cancer</span>while malignant ones are. Cells from malignant <span class="qt0"><span class="qt1">tumors</span>can invade nearby tissues. They can also break away and spread to other parts of the body. </p><p><span class="qt0"><span class="qt1">Cancer</span>is not just one disease but many diseases. There are more than 100 different types of <span class="qt0"><span class="qt1">cancer</span></span>. Most <span class="qt0"><span class="qt1">cancers</span>are named for where they start. For example, lung <span class="qt0"><span class="qt1">cancer</span>starts in the lung, and breast <span class="qt0"><span class="qt1">cancer</span>starts in the breast. The spread of <span class="qt0"><span class="qt1">cancer</span>from one part of the body to another is called metastasis. Symptoms and treatment depend on the <span class="qt0"><span class="qt1">cancer</span>type and how advanced it is. Most treatment plans may include surgery, radiation and/or chemotherapy. Some may involve hormone therapy, biologic therapy, or stem cell transplantation. </p><p>NIH: National <span class="qt0"><span class="qt1">Cancer</span>Institute<p>Throat <span class="qt0"><span class="qt1">cancer</span>is a type of head and neck <span class="qt0"><span class="qt1">cancer</span></span>. Throat <span class="qt0"><span class="qt1">cancer</span>has different names, depending on what part of the throat is affected. The different parts of the throat are called the oropharynx, the hypopharynx, and the nasopharynx. Sometimes the larynx, or voice box, is also included.</p><p>The main risk factors for throat <span class="qt0"><span class="qt1">cancer</span>are smoking or using smokeless tobacco and use of alcohol.</p><p>Symptoms of throat <span class="qt0"><span class="qt1">cancer</span>may include</p><ul><li>Trouble breathing or speaking</li><li>Frequent headaches</li><li>Pain or ringing in the ears</li><li>Trouble swallowing</li><li>Ear pain</li></ul><p>Treatments include surgery, radiation therapy, and chemotherapy.</p><p>NIH: National <span class="qt0"><span class="qt1">Cancer</span>Institute</p>

Zika virus /ˈziːkə, ˈzɪkə/ (ZIKV) is a member of the virus family Flaviviridae and the genus Flavivirus. It is spread by daytime-active Aedes mosquitoes, such as A. aegypti and A. albopictus. Its name comes from the Zika Forest of Uganda, where the virus was first isolated in 1947. Zika virus is related to dengue, yellow fever, Japanese encephalitis, and West Nile viruses.
The infection, known as Zika fever, often causes no or only mild symptoms, similar to a mild form of dengue fever. It is treated by rest. Since the 1950s, it has been known to occur within a narrow equatorial belt from Africa to Asia. The virus spread eastward across the Pacific Ocean 2013–2014 Zika virus outbreaks in Oceania to French Polynesia, New Caledonia, the Cook Islands, and Easter Island, and in 2015 to Mexico, Central America, the Caribbean, and South America, where the Zika outbreak has reached pandemic levels. As of 2016, the illness cannot be prevented by medications or vaccines. Zika fever in pregnant women is associated with microcephaly but it is unclear whether the virus is the cause. An association with the neurologic condition Guillain–Barré syndrome has been found in adults.
In January 2016, the U.S. Centers for Disease Control and Prevention (CDC) issued travel guidance on affected countries, including the use of enhanced precautions, and guidelines for pregnant women including considering postponing travel. Other governments or health agencies also issued similar travel warnings, while Colombia, the Dominican Republic, Ecuador, El Salvador, and Jamaica advised women to postpone getting pregnant until more is known about the risks.


== Virology ==

The Zika virus belongs to Flaviviridae and the genus Flavivirus, and is thus related to the dengue, yellow fever, Japanese encephalitis, and West Nile viruses. Like other flaviviruses, Zika virus is enveloped and icosahedral and has a nonsegmented, single-stranded, positive-sense RNA genome. It is most closely related to the Spondweni virus and is one of the two viruses in the Spondweni virus clade.
A positive-sense RNA genome can be directly translated into viral proteins. In other flaviviruses, such as the similarly sized West Nile virus, the RNA genome genes encode seven nonstructural proteins and three structural proteins. The structural proteins encapsulate the virus. The replicated RNA strand is held within a nucleocapsid formed from 12-kDa protein blocks; the capsid is contained within a host-derived membrane modified with two viral glycoproteins. Replication of the viral genome would first require creation of an anti-sense nucleotide strand.
There are two lineages of the Zika virus: the African lineage, and the Asian lineage. Phylogenetic studies indicate that the virus spreading in the Americas is most closely related to the Asian strain, which circulated in French Polynesia during the 2013–2014 outbreak. The complete genome sequence of the Zika virus has been published. Western Hemisphere Zika virus is found to be 89% identical to African genotypes, but is most closely related to the strain found in French Polynesia during 2013–2014.


== Transmission ==
The vertebrate hosts of the virus were primarily monkeys in a so-called enzootic mosquito-monkey-mosquito cycle, with only occasional transmission to humans. Before the current pandemic began in 2007, Zika virus "rarely caused recognized 'spillover' infections in humans, even in highly enzootic areas". Infrequently, other arboviruses have become established as a human disease though, and spread in a mosquito–human–mosquito cycle, like the yellow fever virus and the dengue fever virus (both flaviruses), and the chikungunya virus (a togavirus).


=== Mosquito ===

The Zika virus is spread by daytime-active mosquitoes. It is primarily spread by the female Aedes aegypti in order to lay eggs, but has been isolated from a number of arboreal mosquito species in the Aedes genus, such as A. africanus, A. apicoargenteus, A. furcifer, A. hensilli, A. luteocephalus and A. vittatus with an extrinsic incubation period in mosquitoes of about 10 days.
The true extent of the vectors is still unknown. The Zika virus has been detected in many more species of Aedes, along with Anopheles coustani, Mansonia uniformis, and Culex perfuscus, although this alone does not incriminate them as a vector.
Transmission by A. albopictus, the tiger mosquito, was reported from a 2007 urban outbreak in Gabon where it had newly invaded the country and become the primary vector for the concomitant chikungunya and dengue virus outbreaks. There is concern for autochthonous infections in urban areas of European countries infested by A. albopictus because the first two cases of laboratory confirmed Zika virus infections imported into Italy were reported from viremic travelers returning from French Polynesia.
The potential societal risk of Zika virus can be delimited by the distribution of the mosquito species that transmit it. The global distribution of the most cited carrier of Zika virus, A. aegypti, is expanding due to global trade and travel. A. aegypti distribution is now the most extensive ever recorded – across all continents including North America and even the European periphery (Madeira, the Netherlands, and the northeastern Black Sea coast). A mosquito population capable of carrying the Zika virus has been found in a Capitol Hill neighborhood of Washington, D. C., and genetic evidence suggests they survived at least four consecutive winters in the region. The study authors conclude that mosquitos are adapting for persistence in a northern climate.
Since 2015, news reports have drawn attention to the spread of Zika in Latin America and the Caribbean. The countries and territories that have been identified by the Pan American Health Organisation as having experienced "local Zika virus transmission" are Barbados, Bolivia, Brazil, Colombia, the Dominican Republic, Ecuador, El Salvador, French Guiana, Guadeloupe, Guatemala, Guyana, Haiti, Honduras, Martinique, Mexico, Panama, Paraguay, Puerto Rico, Saint Martin, Suriname, and Venezuela.


=== Sexual ===
As of February 2016, there are three reported cases indicating that Zika virus could possibly be sexually transmitted. In 2014, Zika virus capable of growth in lab culture was found in the semen of a man at least two weeks (and possibly up to 10 weeks) after he fell ill with Zika fever. The second report is of a United States biologist who had been bitten many times while studying mosquitoes in Senegal. Six days after returning home in August 2008, he fell ill with symptoms of Zika fever but not before having unprotected intercourse with his wife, who had not been outside the US in 2008. She subsequently developed symptoms of Zika fever, and Zika antibodies in both the biologist's and his wife's blood confirmed the diagnosis. In the third case, in early February 2016 the Dallas County Health and Human Services department reported that a person contracted Zika fever after sexual contact with an ill person who had recently returned from a high risk country. This case is still under investigation. Fourteen additional cases of possible sexual transmission are under investigation. All cases involve transmitting the Zika virus from men to women and it is unknown whether women can transmit Zika virus to their sexual partners.
As of March 2016, the CDC updated its recommendations about length of precautions for couples and advised that couples with men who have confirmed Zika fever or symptoms of Zika should consider using condoms or not having sex (i.e., vaginal intercourse, anal intercourse, or fellatio) for at least 6 months after symptoms begin. This includes men who live in and men who traveled to areas with Zika. Couples with men who traveled to an area with Zika, but did not develop symptoms of Zika, should consider using condoms or not having sex for at least 8 weeks after their return in order to minimize risk. Couples with men who live in an area with Zika, but have not developed symptoms, might consider using condoms or not having sex while there is active Zika transmission in the area.
The "incidence and duration of shedding in the male genitourinary tract is limited to one case report" and "testing of men for the purpose of assessing risk for sexual transmission is not recommended."


=== During pregnancy ===
In 2015, Zika virus RNA was detected in the amniotic fluid of two pregnant women whose fetuses had microcephaly, indicating that the virus had crossed the placenta and could have caused a mother-to-child infection. Up until February 2016 the link was thought possible but unproven. Zika fever in pregnant women is associated with intrauterine growth restriction including abnormal brain development in their fetuses, which may result in miscarriage; Brain tissue from two newborns with microcephaly who died within 20 hours of birth and placenta and other tissue of two miscarriages (11 and 13 weeks) from Rio Grande do Norte in Brazil tested positive for Zika virus by RT-PCR at the CDC.
In a cohort study of pregnant women in Rio de Janeiro, Zika virus infection was associated with fetal death, placental insufficiency, fetal growth restriction, and central nervous system (CNS) injury (microcephaly and/or ventricular calcifications or other lesions) in 12 of 42 fetuses studied using ultrasound.
According to the World Health Organization (WHO) on 5 February 2016, a causal link between the Zika virus and microcephaly was "strongly suspected but not yet scientifically proven" and "Although the microcephaly cases in Brazil are spatio-temporally associated with the Zika outbreak, more robust investigations and research is needed to better understand this potential link."
On 5 February 2016, the United States CDC updated its health care provider guidelines for pregnant women and women of reproductive age. The new recommendations include offering serologic testing to pregnant women without Zika fever symptoms who have returned from areas with ongoing Zika virus transmission in the last 2–12 weeks; and for pregnant women without Zika symptoms living in such areas, they recommend testing at the beginning of prenatal care and follow-up testing in the fifth month of pregnancy.


=== Other, unproven ===
As of February 2016 there are no confirmed cases of Zika virus transmission through blood transfusions. A potential risk is supected based on a study conducted between November 2013 and February 2014 during the Zika outbreak in French Polynesia, in which 2.8% (42) of blood donors tested positive for the Zika virus RNA and were asymptomatic at the time of blood donation. Eleven of those positive donors reported symptoms of Zika fever after their donation, and only three of 34 samples grew in culture. Since January 2014 nucleic acid testing of blood donors was implemented in French Polynesia to prevent unintended transmission.


== Pathogenesis ==
Zika virus replicates in the mosquito's midgut epithelial cells and then its salivary gland cells. After 5–10 days, ZIKV can be found in the mosquito’s saliva which can then infect human. If the mosquito’s saliva is inoculated into human skin, the virus infect epidermal keratinocytes, skin fibroblasts in the skin and the Langerhans cells. The pathogenesis of the virus is hypothesized to continue with a spread to lymph nodes and the bloodstream., Flaviviruses generally replicate in the cytoplasm, but Zika virus antigens have been found in infected cell nuclei.


== Zika fever ==

Common symptoms of infection with the virus include mild headaches, maculopapular rash, fever, malaise, conjunctivitis, and joint pains. Three well-documented cases of Zika virus were described in brief in 1954, whereas a detailed description was published in 1964; it began with a mild headache, and progressed to a maculopapular rash, fever, and back pain. Within two days, the rash started fading, and within three days, the fever resolved and only the rash remained. Thus far, Zika fever has been a relatively mild disease of limited scope, with only one in five persons developing symptoms, with no fatalities, but its true potential as a viral agent of disease is unknown.
As of 2016, no vaccine or preventative drug is available. Symptoms can be treated with rest, fluids, and paracetamol (acetaminophen), while aspirin and other nonsteroidal anti-inflammatory drugs should be used only when dengue has been ruled out to reduce the risk of bleeding.
There is a link between Zika fever and neurologic conditions in infected adults, including cases of the Guillain–Barré syndrome.


== Vaccine development ==
Effective vaccines exist for several viruses of the flaviviridae family, namely Yellow fever vaccine, Japanese encephalitis vaccine, and Tick-borne encephalitis vaccine since the 1930s, and dengue fever vaccine since the mid-2010s. WHO experts have suggested that the priority should be to develop inactivated vaccines and other non-live vaccines, which are safe to use in pregnant women and those of childbearing age.
The NIH Vaccine Research Center began work towards developing a vaccine for the Zika virus per a January 2016 report. Bharat Biotech International, reported in early February 2016 that it was working on vaccines for the Zika virus using two approaches: "recombinant", involving genetic engineering, and "inactivated", where the virus is incapable of reproducing itself but can still trigger an immune response with animal trials of the inactivated version to commence in late February. As of March 2016, 18 companies and institutions internationally were developing vaccines against Zika virus, but none had yet reached clinical trials. Nikos Vasilakis of the Center for Biodefense and Emerging Infectious Diseases predicted that it may take two years to develop a vaccine, but 10 to 12 years may be needed before an effective Zika virus vaccine is approved by regulators for public use.


== History ==


=== Virus isolation in monkeys and mosquitoes, 1947 ===
The virus was first isolated in April 1947 from a rhesus macaque monkey that had been placed in a cage in the Zika Forest of Uganda, near Lake Victoria, by the scientists of the Yellow Fever Research Institute. A second isolation from the mosquito A. africanus followed at the same site in January 1948. When the monkey developed a fever, researchers isolated from its serum a "filterable transmissible agent" that was named Zika virus in 1948.


=== First evidence of human infection, 1952 ===
Zika virus had been known to infect humans from the results of serological surveys in Uganda and Nigeria, published in 1952: Among 84 people of all ages, 50 individuals had antibodies to Zika, and all above 40 years of age were immune. A 1952 research study conducted in India had shown a "significant number" of Indians tested for Zika had exhibited an immune response to the virus, suggesting it had long been widespread within human populations.
It was not until 1954 that the isolation of Zika virus from a human was published. This came as part of a 1952 outbreak investigation of jaundice suspected to be yellow fever. It was found in the blood of a 10-year-old Nigerian female with low-grade fever, headache, and evidence of malaria, but no jaundice, who recovered within three days. Blood was injected into the brain of laboratory mice, followed by up to 15 mice passages. The virus from mouse brains was then tested in neutralization tests using rhesus monkey sera specifically immune to Zika virus. In contrast, no virus was isolated from the blood of two infected adults with fever, jaundice, cough, diffuse joint pains in one and fever, headache, pain behind the eyes and in the joints. Infection was proven by a rise in Zika virus-specific serum antibodies.


=== Spread in equatorial Africa and to Asia, 1951–1983 ===

From 1951 through 1983, evidence of human infection with Zika virus was reported from other African countries, such as the Central African Republic, Egypt, Gabon, Sierra Leone, Tanzania, and Uganda, as well as in parts of Asia including India, Indonesia, Malaysia, the Philippines, Thailand, Vietnam and Pakistan. From its discovery until 2007, there were only 14 confirmed human cases of Zika virus infection from Africa and Southeast Asia.


=== Micronesia, 2007 ===

In April 2007, the first outbreak outside of Africa and Asia occurred on the island of Yap in the Federated States of Micronesia, characterized by rash, conjunctivitis, and arthralgia, which was initially thought to be dengue, chikungunya, or Ross River disease. Serum samples from patients in the acute phase of illness contained RNA of Zika virus. There were 49 confirmed cases, 59 unconfirmed cases, no hospitalizations, and no deaths.


=== 2013–2014 ===


==== Oceania ====

Between 2013 and 2014, further epidemics occurred in French Polynesia, Easter Island, the Cook Islands, and New Caledonia.


==== Other cases ====
On 22 March 2016 Reuters reported that Zika virus was isolated from a 2014 blood sample of an elderly man in Chittagong in Bangladesh as part of a retrospective study.


=== Americas, 2015–present ===

As of early 2016, a widespread outbreak of Zika virus is ongoing, primarily in the Americas. The outbreak began in April 2015 in Brazil, and has spread to other countries in South America, Central America, Mexico, and the Caribbean. In January 2016, the WHO said the virus was likely to spread throughout most of the Americas by the end of the year; and in February 2016, the WHO declared the cluster of microcephaly and Guillain–Barré syndrome cases reported in Brazil – strongly suspected to be associated with the Zika virus outbreak – a Public Health Emergency of International Concern. It is estimated that 1.5 million people have been infected by Zika virus in Brazil, with over 3,500 cases of microcephaly reported between October 2015 and January 2016.
A number of countries have issued travel warnings, and the outbreak is expected to significantly impact the tourism industry. Several countries have taken the unusual step of advising their citizens to delay pregnancy until more is known about the virus and its impact on fetal development.


== References ==

This article contains public domain text from the CDC as cited


== External links ==

Zika Virus – Centers for Disease Control and Prevention
World Health Organization Zika Virus Fact Sheet
Zika virus illustrations, 3D model, and animation
ViralZone: Zika virus (strain Mr 766)
Zika virus at NCBI Taxonomy Browser
Schmaljohn, Alan L.; McClain, David (1996). "54. Alphaviruses (Togaviridae) and Flaviviruses (Flaviviridae)". In Baron, Samuel. Medical Microbiology (4th ed.). ISBN 0-9631172-1-1. NBK7633.
"""

def clean_corpus(corpus=None):
	'''
    cleans out all non-ascii characters, newlines, carriage returns, wikipedia headers, other fun stuff
    :param corpus: a string from a text file representing the corpus
    :return:
    '''

	corpus = re.sub(r'<.*?>', ' ', corpus)
	corpus = re.sub(r'={2,}.*?={2,}', ' ', corpus)
	corpus = re.sub(r'\n|\r', ' ', corpus)
	corpus = re.sub(r'\\x[a-zA-Z0-9]{2,}', ' ', corpus)
	corpus = re.sub(r'\s{2,}.*?\s{2,}', ' ', corpus)
	corpus = corpus.strip()
	return corpus


def tokenize_sentences(corpus=None):
    '''
    split the corpus into sentences.
    :param corpus: a string from a text file representing the corpus
    :return:
    '''
    return re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',corpus)

test = clean_corpus(corpus)
test2 = tokenize_sentences(test)

for i,t in enumerate(test2):
	test2[i] = clean_corpus(t)
	try:
		words = len(test2[i].split(' '))
		if words < 10: test2.pop(i)
		if '.' not in test2[i][-1]: del test2[i]
		if test2[i][0].isupper() == False: del test2[i]
		if test2[i][0].isdigit() == True: del test2[i]
	except:
		pass


f = open('test.txt','w')
f.write('\n\n'.join(test2))
