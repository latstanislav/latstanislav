Hi, I'm Stanislav ML Engineer
# Привет! Это мой профиль-визитка

В данном репозитории собраны ключевые проекты, реализованные мной в коммерчесских целях, а также в рамках обучения на курсе ML Engineer в Яндекс Практикуме.   
Каждый проект представляет собой решение конкретной бизнес-задачи (RecSys, NLP, LLM, MLOps).
Особенности:  
Все проекты доведены до стадии работающих прототипов или пайплайнов.
Тетради (Jupyter Notebooks) содержат подробный анализ данных (EDA), построение моделей и выводы.

## Commercial Experience (Коммерческий опыт)
| Project name | Role | Description | Stack |
| :--- | :--- | :--- | :--- |
| [**Marketplace Backend**](./ML-Engineer-Portfolio/Marketplace_Backend) | Lead Backend Developer | Проектирование и реализация микросервисной архитектуры маркетплейса с автоматизированным CI/CD и деплоем в GCP. | FastAPI, Docker, GitHub Actions, Google Cloud, PostgreSQL |

---

## ML Projects (Yandex Practicum)
Здесь представлены ключевые кейсы, реализованные в рамках обучения на программе ML Engineer.

### 🤖 Generative AI & NLP (LLM, RAG, Search)
| Project name | Description | Stack |
| :--- | :--- | :--- |
| [**Agentic Multi-modal Search (CLIP)**](./ML-Engineer-Portfolio/Agentic_Multi-modal_Search_(CLIP)) | Разработка системы поиска товаров на основе дообученной модели CLIP. Реализация агентской логики для обработки запросов и анализа качества данных через Visual Question Answering (VQA).| CLIP, smolagents, autogen, MCP, VQA, PyTorch, Hugging Face|
| [**Semantic Retrieval System**](./ML-Engineer-Portfolio/Semantic_Retrieval_System) | Разработка поисковой системы по статьям arXiv.org. Использование LLM для выделения сущностей (NER) и оценка качества выдачи по метрике **MRR@5**. | Hugging Face, Transformers, Datasets, LLM-based NER |
| [**LLM SFT & Adaptation**](./ML-Engineer-Portfolio/LLM_SFT_&_Adaptation) | Обучение базовой модели (Llama) и SFT (Qwen) на диалоговых корпусах с применением LoRA. Подготовка пайплайна для RAG-систем. | Python, PyTorch, Transformers, LoRA, ClearML |
| [**Multi-task NLP Model**](./ML-Engineer-Portfolio/Multi-task_NLP_Model) | Система семантического анализа новостей: совместное решение задач NER и CLS на базе RuBERT с кастомной архитектурой. | RuBERT, BIO-tagging, Custom Loss, PyTorch |

### 🚀 MLOps & Production
| Project name | Description | Stack |
| :--- | :--- | :--- |
| [**End-to-End Real Estate Pipeline**](./ML-Engineer-Portfolio/End-to-End_Real_Estate_Pipeline) | Сквозной проект: от ETL-процессов и версионирования данных до деплоя модели оценки недвижимости с мониторингом (Grafana). | Airflow, DVC, FastAPI, Docker, Prometheus, Grafana, MLflow, PostgreSQL |
| [**Uplift Modeling (Yandex Food)**](./ML-Engineer-Portfolio/Uplift_Modeling_(Yandex_Food)) | Оценка эффективности маркетинговых акций: построение Uplift-моделей (X/S/T/R-learners) и расчет стат. значимости (Z-test, Chi-square). | MLflow, Optuna, LightGBM, XGBoost, UpliftML, Statistics |

### 🎵 Recommendation Systems
| Project name | Description | Stack |
| :--- | :--- | :--- |
| [**Two-stage RecSys**](./ML-Engineer-Portfolio/Two-stage-RecSys) | Рекомендательная система для музыки: матричная факторизация (ALS) + ранжирование кандидатов (CatBoost). | ALS, CatBoost, Cosine Similarity, Pandas |
