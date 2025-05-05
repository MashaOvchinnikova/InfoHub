"""
Модели и схемы для работы с Elasticsearch в поисковом сервисе.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator


class ElasticsearchIndex(BaseModel):
    """
    Базовая схема для индекса в Elasticsearch.
    Определяет общую структуру индекса и настройки анализаторов.
    """
    index_name: str
    settings: Dict[str, Any]
    mappings: Dict[str, Any]

    class Config:
        extra = "allow"


class SourceDocument(BaseModel):
    """
    Модель документа источника для индексации в Elasticsearch.
    """
    id: str  # UUID в виде строки для ES
    source_id: str
    title: str
    description: Optional[str] = None
    url: str
    content_type: str

    publication_date: Optional[datetime] = None
    added_date: datetime
    avg_rating: float = 0.0
    is_verified: bool = False
    is_recommended: bool = False

    tags: List[str] = []
    tag_ids: List[str] = []  # UUID в виде строки для ES
    interests: List[str] = []
    interest_ids: List[str] = []  # UUID в виде строки для ES

    added_by_username: Optional[str] = None
    thumbnail_url: Optional[str] = None

    popularity_score: float = 0.0
    relevance_score: float = 0.0

    # Поле для полнотекстового поиска - объединение всех текстовых полей
    full_text: Optional[str] = None

    @validator('full_text', always=True)
    def set_full_text(cls, v, values):
        """Создает полнотекстовое поле из других полей."""
        if v is not None:
            return v

        text_parts = []
        if 'title' in values:
            text_parts.append(values['title'])
        if 'description' in values and values['description']:
            text_parts.append(values['description'])
        if 'tags' in values and values['tags']:
            text_parts.append(' '.join(values['tags']))
        if 'interests' in values and values['interests']:
            text_parts.append(' '.join(values['interests']))
        if 'added_by_username' in values and values['added_by_username']:
            text_parts.append(values['added_by_username'])

        return ' '.join(text_parts)


class SourceIndex(ElasticsearchIndex):
    """
    Схема для индекса источников в Elasticsearch.
    Включает определение полей, анализаторов и настроек.
    """
    index_name: str = "sources"

    settings: Dict[str, Any] = {
        "analysis": {
            "analyzer": {
                "custom_russian": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "russian_stop", "russian_stemmer"]
                },
                "custom_english": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "english_stop", "english_stemmer"]
                },
                "ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "ngram_filter"]
                }
            },
            "filter": {
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                },
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "ngram_filter": {
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 20
                }
            }
        },
        "number_of_shards": 1,
        "number_of_replicas": 1
    }

    mappings: Dict[str, Any] = {
        "properties": {
            "id": {"type": "keyword"},
            "source_id": {"type": "keyword"},
            "title": {
                "type": "text",
                "analyzer": "custom_russian",
                "fields": {
                    "english": {"type": "text", "analyzer": "custom_english"},
                    "ngram": {"type": "text", "analyzer": "ngram_analyzer"},
                    "keyword": {"type": "keyword"}
                }
            },
            "description": {
                "type": "text",
                "analyzer": "custom_russian",
                "fields": {
                    "english": {"type": "text", "analyzer": "custom_english"}
                }
            },
            "url": {"type": "keyword"},
            "content_type": {"type": "keyword"},
            "publication_date": {"type": "date"},
            "added_date": {"type": "date"},
            "avg_rating": {"type": "float"},
            "is_verified": {"type": "boolean"},
            "is_recommended": {"type": "boolean"},
            "tags": {
                "type": "text",
                "analyzer": "custom_russian",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "tag_ids": {"type": "keyword"},
            "interests": {
                "type": "text",
                "analyzer": "custom_russian",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "interest_ids": {"type": "keyword"},
            "added_by_username": {"type": "keyword"},
            "thumbnail_url": {"type": "keyword"},
            "popularity_score": {"type": "float"},
            "relevance_score": {"type": "float"},
            "full_text": {
                "type": "text",
                "analyzer": "custom_russian",
                "fields": {
                    "english": {"type": "text", "analyzer": "custom_english"}
                }
            }
        }
    }


class SuggestionDocument(BaseModel):
    """
    Модель документа поисковой подсказки для индексации в Elasticsearch.
    """
    id: str  # UUID в виде строки для ES
    text: str
    type: str
    source_id: Optional[str] = None
    weight: float = 1.0
    usage_count: int = 0


class SuggestionIndex(ElasticsearchIndex):
    """
    Схема для индекса поисковых подсказок в Elasticsearch.
    """
    index_name: str = "suggestions"

    settings: Dict[str, Any] = {
        "analysis": {
            "analyzer": {
                "completion_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase"]
                },
                "edge_ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "edge_ngram_filter"]
                }
            },
            "filter": {
                "edge_ngram_filter": {
                    "type": "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 20
                }
            }
        },
        "number_of_shards": 1,
        "number_of_replicas": 1
    }

    mappings: Dict[str, Any] = {
        "properties": {
            "id": {"type": "keyword"},
            "text": {
                "type": "text",
                "analyzer": "completion_analyzer",
                "fields": {
                    "ngram": {"type": "text", "analyzer": "edge_ngram_analyzer"},
                    "keyword": {"type": "keyword"}
                }
            },
            "suggest": {
                "type": "completion",
                "contexts": [
                    {
                        "name": "type",
                        "type": "category"
                    }
                ]
            },
            "type": {"type": "keyword"},
            "source_id": {"type": "keyword"},
            "weight": {"type": "float"},
            "usage_count": {"type": "integer"}
        }
    }


class ElasticsearchQuery(BaseModel):
    """
    Модель для формирования поисковых запросов к Elasticsearch.
    """
    index: str
    query: Dict[str, Any]
    size: int = 10
    from_: int = Field(0, alias="from")
    sort: Optional[List[Dict[str, Any]]] = None
    aggs: Optional[Dict[str, Any]] = None
    highlight: Optional[Dict[str, Any]] = None

    class Config:
        allow_population_by_field_name = True


class ElasticsearchResponse(BaseModel):
    """
    Модель для парсинга ответов от Elasticsearch.
    """
    took: int
    timed_out: bool
    hits: Dict[str, Any]
    aggregations: Optional[Dict[str, Any]] = None

    class Config:
        extra = "allow"