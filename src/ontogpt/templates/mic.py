from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'mic',
     'default_range': 'string',
     'description': 'A template for micronutrient information from text, including '
                    'its participation in biochemical pathways and relationships '
                    'to genes and diseases. Intended for use with the '
                    'Micronutrient Information Center, a resource curated and '
                    'managed by the Linus Pauling Institute at Oregon State '
                    'University.',
     'id': 'http://w3id.org/ontogpt/mic',
     'imports': ['linkml:types', 'core'],
     'license': 'https://creativecommons.org/publicdomain/zero/1.0/',
     'name': 'mic',
     'prefixes': {'GO': {'prefix_prefix': 'GO',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/GO_'},
                  'chebi': {'prefix_prefix': 'chebi',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/CHEBI_'},
                  'foodon': {'prefix_prefix': 'foodon',
                             'prefix_reference': 'http://purl.obolibrary.org/obo/foodon_'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'mic': {'prefix_prefix': 'mic',
                          'prefix_reference': 'http://w3id.org/ontogpt/mic'},
                  'rdf': {'prefix_prefix': 'rdf',
                          'prefix_reference': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}},
     'source_file': 'src/ontogpt/templates/mic.yaml',
     'title': 'Micronutrient Information Extraction Template'} )

class NullDataOptions(str, Enum):
    UNSPECIFIED_METHOD_OF_ADMINISTRATION = "UNSPECIFIED_METHOD_OF_ADMINISTRATION"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NOT_MENTIONED = "NOT_MENTIONED"


class GOBiologicalProcessType(str):
    pass



class ExtractionResult(ConfiguredBaseModel):
    """
    A result of extracting knowledge on text
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/core'})

    input_id: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'input_id', 'domain_of': ['ExtractionResult']} })
    input_title: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'input_title', 'domain_of': ['ExtractionResult']} })
    input_text: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'input_text', 'domain_of': ['ExtractionResult']} })
    raw_completion_output: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'raw_completion_output', 'domain_of': ['ExtractionResult']} })
    prompt: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'prompt', 'domain_of': ['ExtractionResult']} })
    extracted_object: Optional[Any] = Field(None, description="""The complex objects extracted from the text""", json_schema_extra = { "linkml_meta": {'alias': 'extracted_object', 'domain_of': ['ExtractionResult']} })
    named_entities: Optional[List[Any]] = Field(None, description="""Named entities extracted from the text""", json_schema_extra = { "linkml_meta": {'alias': 'named_entities', 'domain_of': ['ExtractionResult']} })


class NamedEntity(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'http://w3id.org/ontogpt/core'})

    id: str = Field(..., description="""A unique identifier for the named entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['this is populated during the grounding and normalization step'],
         'domain_of': ['NamedEntity', 'Publication']} })
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'aliases': ['name'],
         'annotations': {'owl': {'tag': 'owl',
                                 'value': 'AnnotationProperty, AnnotationAssertion'}},
         'domain_of': ['NamedEntity'],
         'slot_uri': 'rdfs:label'} })
    original_spans: Optional[List[str]] = Field(None, description="""The coordinates of the original text span from which the named entity was extracted, inclusive. For example, \"10:25\" means the span starting from the 10th character and ending with the 25th character. The first character in the text has index 0. Newlines are treated as single characters. Multivalued as there may be multiple spans for a single text.""", json_schema_extra = { "linkml_meta": {'alias': 'original_spans',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['This is determined during grounding and normalization',
                      'But is based on the full input text'],
         'domain_of': ['NamedEntity']} })

    @field_validator('original_spans')
    def pattern_original_spans(cls, v):
        pattern=re.compile(r"^\d+:\d+$")
        if isinstance(v,list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid original_spans format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid original_spans format: {v}")
        return v


class CompoundExpression(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'http://w3id.org/ontogpt/core'})

    pass


class Triple(CompoundExpression):
    """
    Abstract parent for Relation Extraction tasks
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'http://w3id.org/ontogpt/core'})

    subject: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'subject', 'domain_of': ['Triple']} })
    predicate: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'predicate', 'domain_of': ['Triple']} })
    object: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'object', 'domain_of': ['Triple']} })
    qualifier: Optional[str] = Field(None, description="""A qualifier for the statements, e.g. \"NOT\" for negation""", json_schema_extra = { "linkml_meta": {'alias': 'qualifier', 'domain_of': ['Triple']} })
    subject_qualifier: Optional[str] = Field(None, description="""An optional qualifier or modifier for the subject of the statement, e.g. \"high dose\" or \"intravenously administered\"""", json_schema_extra = { "linkml_meta": {'alias': 'subject_qualifier', 'domain_of': ['Triple']} })
    object_qualifier: Optional[str] = Field(None, description="""An optional qualifier or modifier for the object of the statement, e.g. \"severe\" or \"with additional complications\"""", json_schema_extra = { "linkml_meta": {'alias': 'object_qualifier', 'domain_of': ['Triple']} })


class TextWithTriples(ConfiguredBaseModel):
    """
    A text containing one or more relations of the Triple type.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/core'})

    publication: Optional[Publication] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'publication',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'domain_of': ['TextWithTriples', 'TextWithEntity']} })
    triples: Optional[List[Triple]] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'triples', 'domain_of': ['TextWithTriples']} })


class TextWithEntity(ConfiguredBaseModel):
    """
    A text containing one or more instances of a single type of entity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/core'})

    publication: Optional[Publication] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'publication',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'domain_of': ['TextWithTriples', 'TextWithEntity']} })
    entities: Optional[List[str]] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'entities', 'domain_of': ['TextWithEntity']} })


class RelationshipType(NamedEntity):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/core',
         'id_prefixes': ['RO', 'biolink']})

    id: str = Field(..., description="""A unique identifier for the named entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['this is populated during the grounding and normalization step'],
         'domain_of': ['NamedEntity', 'Publication']} })
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'aliases': ['name'],
         'annotations': {'owl': {'tag': 'owl',
                                 'value': 'AnnotationProperty, AnnotationAssertion'}},
         'domain_of': ['NamedEntity'],
         'slot_uri': 'rdfs:label'} })
    original_spans: Optional[List[str]] = Field(None, description="""The coordinates of the original text span from which the named entity was extracted, inclusive. For example, \"10:25\" means the span starting from the 10th character and ending with the 25th character. The first character in the text has index 0. Newlines are treated as single characters. Multivalued as there may be multiple spans for a single text.""", json_schema_extra = { "linkml_meta": {'alias': 'original_spans',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['This is determined during grounding and normalization',
                      'But is based on the full input text'],
         'domain_of': ['NamedEntity']} })

    @field_validator('original_spans')
    def pattern_original_spans(cls, v):
        pattern=re.compile(r"^\d+:\d+$")
        if isinstance(v,list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid original_spans format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid original_spans format: {v}")
        return v


class Publication(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/core'})

    id: Optional[str] = Field(None, description="""The publication identifier""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['NamedEntity', 'Publication']} })
    title: Optional[str] = Field(None, description="""The title of the publication""", json_schema_extra = { "linkml_meta": {'alias': 'title', 'domain_of': ['Publication']} })
    abstract: Optional[str] = Field(None, description="""The abstract of the publication""", json_schema_extra = { "linkml_meta": {'alias': 'abstract', 'domain_of': ['Publication']} })
    combined_text: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'combined_text', 'domain_of': ['Publication']} })
    full_text: Optional[str] = Field(None, description="""The full text of the publication""", json_schema_extra = { "linkml_meta": {'alias': 'full_text', 'domain_of': ['Publication']} })


class AnnotatorResult(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/core'})

    subject_text: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'subject_text', 'domain_of': ['AnnotatorResult']} })
    object_id: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'object_id', 'domain_of': ['AnnotatorResult']} })
    object_text: Optional[str] = Field(None, json_schema_extra = { "linkml_meta": {'alias': 'object_text', 'domain_of': ['AnnotatorResult']} })


class Document(NamedEntity):
    """
    A document that contains information about micronutrients, including vitamins and minerals.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/mic', 'tree_root': True})

    nutrient_to_disease_relationships: Optional[List[NutrientToDiseaseRelationship]] = Field(None, description="""A list of relationships between nutrients and biochemical diseases.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient_to_disease_relationships',
         'annotations': {'prompt': {'tag': 'prompt',
                                    'value': 'A semicolon-separated list of '
                                             'relationships between a single nutrient '
                                             '(including vitamins, minerals, and '
                                             'micronutrients) and a single disease, '
                                             'with a type of relationship connecting '
                                             'them both. A disease is any abnormal '
                                             "health condition (e.g., Alzheimer's "
                                             'disease, systemic lupus erythematosus, '
                                             'rheumatoid arthritis, sickle cell '
                                             'anemia, Barth syndrome). Represent the '
                                             'relationship as triples, e.g., "Nutrient '
                                             'HAS RELATIONSHIP WITH Disease". '
                                             'Relationships may include TREATS, '
                                             'PREVENTS, INCREASES RISK OF, DECREASES '
                                             'RISK OF, or others. For each '
                                             'relationship, include the number of the '
                                             'corresponding reference(s) in '
                                             'parentheses after the relationship; '
                                             'e.g., if the text indicates a reference '
                                             'of (3), include it after the object in '
                                             'the relationship, e.g., "Subject HAS '
                                             'RELATIONSHIP WITH Object (3)". Delimit '
                                             'multiple references with commas, e.g., '
                                             '"(3, 4)". Do not include newlines.'}},
         'domain_of': ['Document']} })
    nutrient_to_phenotype_relationships: Optional[List[NutrientToPhenotypeRelationship]] = Field(None, description="""A list of relationships between nutrients and biological phenotypes.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient_to_phenotype_relationships',
         'annotations': {'prompt': {'tag': 'prompt',
                                    'value': 'A semicolon-separated list of '
                                             'relationships between a single nutrient '
                                             '(including vitamins, minerals, and '
                                             'micronutrients) and a single biological '
                                             'phenotype, with a type of relationship '
                                             'connecting them both. A phenotype is an '
                                             'observable physical or behavioral trait '
                                             'or symptom (e.g., fever, headache, short '
                                             'attention span, petechiae, '
                                             'telangiectasia). It may or may not be '
                                             'associated with a disease. Phenotypes do '
                                             'NOT include high-level biological '
                                             'processes such as "Insulin signaling" or '
                                             '"lipid metabolism", developmental '
                                             'processes such as "limb development", or '
                                             'health states such as "healthy teeth". '
                                             'Represent the relationship as triples, '
                                             'e.g., "Nutrient HAS RELATIONSHIP WITH '
                                             'Phenotype". Relationships may include '
                                             'TREATS, PREVENTS, or others. For each '
                                             'relationship, include the number of the '
                                             'corresponding reference(s) in '
                                             'parentheses after the relationship; '
                                             'e.g., if the text indicates a reference '
                                             'of (3), include it after the object in '
                                             'the relationship, e.g., "Subject HAS '
                                             'RELATIONSHIP WITH Object (3)". Delimit '
                                             'multiple references with commas, e.g., '
                                             '"(3, 4)". Do not include newlines.'}},
         'domain_of': ['Document']} })
    nutrient_to_biological_process_relationships: Optional[List[NutrientToBiologicalProcessRelationship]] = Field(None, description="""A list of relationships between nutrients and biological processes.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient_to_biological_process_relationships',
         'annotations': {'prompt': {'tag': 'prompt',
                                    'value': 'A semicolon-separated list of '
                                             'relationships between a single nutrient '
                                             '(including vitamins, minerals, and '
                                             'micronutrients) and a single biological '
                                             'process, with a type of relationship '
                                             'connecting them both. A biological '
                                             'process is an activity or series of '
                                             'activities that occur in a cell or '
                                             'organism, such as "nuclear axial '
                                             'expansion", "intracellular transport", '
                                             '"ribosomal subunit export from nucleus", '
                                             '"insulin signaling", or "DNA repair". '
                                             'Biological processes do NOT include '
                                             'health states such as "healthy teeth" or '
                                             'proteins such as "retinoic acid '
                                             'receptor". Represent the relationship as '
                                             'triples, e.g., "Nutrient HAS '
                                             'RELATIONSHIP WITH Process". '
                                             'Relationships may include REGULATES, '
                                             'PARTICIPATES IN, or others. For each '
                                             'relationship, include the number of the '
                                             'corresponding reference(s) in '
                                             'parentheses after the relationship; '
                                             'e.g., if the text indicates a reference '
                                             'of (3), include it after the object in '
                                             'the relationship, e.g., "Subject HAS '
                                             'RELATIONSHIP WITH Object (3)". Delimit '
                                             'multiple references with commas, e.g., '
                                             '"(3, 4)". Do not include newlines.'}},
         'domain_of': ['Document']} })
    nutrient_to_health_status_relationships: Optional[List[NutrientToHealthStatusRelationship]] = Field(None, description="""A list of relationships between nutrients and health of a specific part or system of the human body.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient_to_health_status_relationships',
         'annotations': {'prompt': {'tag': 'prompt',
                                    'value': 'A semicolon-separated list of '
                                             'relationships between a single nutrient '
                                             '(including vitamins, minerals, and '
                                             'micronutrients) and a single part or '
                                             'system of the body, with a type of '
                                             'relationship connecting them both. '
                                             'Example parts or systems include '
                                             '"teeth", "skin", "cardiovascular '
                                             'system", "digestive system", or "liver". '
                                             'Transform names of processes to their '
                                             'respective anatomy, e.g., "thyroid '
                                             'function" or "thyroid health" should be '
                                             'changed to "thyroid"; "digestion" should '
                                             'be changed to "digestive system". '
                                             'Represent the relationship as triples, '
                                             'e.g., "Nutrient HAS RELATIONSHIP WITH '
                                             'Part". Relationships should be SUPPORTS '
                                             'HEALTH OF. For each relationship, '
                                             'include the number of the corresponding '
                                             'reference(s) in parentheses after the '
                                             'relationship; e.g., if the text '
                                             'indicates a reference of (3), include it '
                                             'after the object in the relationship, '
                                             'e.g., "Subject HAS RELATIONSHIP WITH '
                                             'Object (3)". Delimit multiple references '
                                             'with commas, e.g., "(3, 4)". Do not '
                                             'include newlines.'}},
         'domain_of': ['Document']} })
    nutrient_to_source_relationships: Optional[List[NutrientToSourceRelationship]] = Field(None, description="""A list of relationships between nutrients and their sources in food or supplements.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient_to_source_relationships',
         'annotations': {'prompt': {'tag': 'prompt',
                                    'value': 'A semicolon-separated list of '
                                             'relationships between a single nutrient '
                                             '(including vitamins, minerals, and '
                                             'micronutrients) and a single food or '
                                             'supplement, with a type of relationship '
                                             'connecting them both. Example foods '
                                             'include "butter", "apple", "watermelon", '
                                             '"beef", or "breakfast cereal". Represent '
                                             'the relationship as triples, e.g., '
                                             '"Nutrient HAS RELATIONSHIP WITH Source". '
                                             'Relationships should be PROVIDED BY. For '
                                             'each relationship, include the number of '
                                             'the corresponding reference(s) in '
                                             'parentheses after the relationship; '
                                             'e.g., if the text indicates a reference '
                                             'of (3), include it after the object in '
                                             'the relationship, e.g., "Subject HAS '
                                             'RELATIONSHIP WITH Object (3)". Delimit '
                                             'multiple references with commas, e.g., '
                                             '"(3, 4)". Do not include newlines.'}},
         'domain_of': ['Document']} })
    nutrient_to_nutrient_relationships: Optional[List[NutrientToNutrientRelationship]] = Field(None, description="""A list of relationships between nutrients and other nutrients.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient_to_nutrient_relationships',
         'annotations': {'prompt': {'tag': 'prompt',
                                    'value': 'A semicolon-separated list of '
                                             'relationships between a single nutrient '
                                             '(including vitamins, minerals, and '
                                             'micronutrients) and another single '
                                             'nutrient, with a type of relationship '
                                             'connecting them both. This does not '
                                             'include relationships between nutrients '
                                             'and proteins (e.g., a nutrient and its '
                                             'receptor protein). Represent the '
                                             'relationship as triples, e.g., "Nutrient '
                                             'INTERACTS WITH Nutrient". For each '
                                             'relationship, include the number of the '
                                             'corresponding reference(s) in '
                                             'parentheses after the relationship; '
                                             'e.g., if the text indicates a reference '
                                             'of (3), include it after the object in '
                                             'the relationship, e.g., "Subject HAS '
                                             'RELATIONSHIP WITH Object (3)". Delimit '
                                             'multiple references with commas, e.g., '
                                             '"(3, 4)". Do not include newlines.'}},
         'domain_of': ['Document']} })
    id: str = Field(..., description="""A unique identifier for the named entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['this is populated during the grounding and normalization step'],
         'domain_of': ['NamedEntity', 'Publication']} })
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'aliases': ['name'],
         'annotations': {'owl': {'tag': 'owl',
                                 'value': 'AnnotationProperty, AnnotationAssertion'}},
         'domain_of': ['NamedEntity'],
         'slot_uri': 'rdfs:label'} })
    original_spans: Optional[List[str]] = Field(None, description="""The coordinates of the original text span from which the named entity was extracted, inclusive. For example, \"10:25\" means the span starting from the 10th character and ending with the 25th character. The first character in the text has index 0. Newlines are treated as single characters. Multivalued as there may be multiple spans for a single text.""", json_schema_extra = { "linkml_meta": {'alias': 'original_spans',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['This is determined during grounding and normalization',
                      'But is based on the full input text'],
         'domain_of': ['NamedEntity']} })

    @field_validator('original_spans')
    def pattern_original_spans(cls, v):
        pattern=re.compile(r"^\d+:\d+$")
        if isinstance(v,list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid original_spans format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid original_spans format: {v}")
        return v


class Nutrient(NamedEntity):
    """
    The name of a nutrient, including vitamins and minerals.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'annotators': {'tag': 'annotators',
                                        'value': 'sqlite:obo:chebi'},
                         'prompt': {'tag': 'prompt',
                                    'value': 'The name of a nutrient, including '
                                             'vitamins and minerals.'}},
         'from_schema': 'http://w3id.org/ontogpt/mic',
         'id_prefixes': ['CHEBI']})

    id: str = Field(..., description="""A unique identifier for the named entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['this is populated during the grounding and normalization step'],
         'domain_of': ['NamedEntity', 'Publication']} })
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'aliases': ['name'],
         'annotations': {'owl': {'tag': 'owl',
                                 'value': 'AnnotationProperty, AnnotationAssertion'}},
         'domain_of': ['NamedEntity'],
         'slot_uri': 'rdfs:label'} })
    original_spans: Optional[List[str]] = Field(None, description="""The coordinates of the original text span from which the named entity was extracted, inclusive. For example, \"10:25\" means the span starting from the 10th character and ending with the 25th character. The first character in the text has index 0. Newlines are treated as single characters. Multivalued as there may be multiple spans for a single text.""", json_schema_extra = { "linkml_meta": {'alias': 'original_spans',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['This is determined during grounding and normalization',
                      'But is based on the full input text'],
         'domain_of': ['NamedEntity']} })

    @field_validator('original_spans')
    def pattern_original_spans(cls, v):
        pattern=re.compile(r"^\d+:\d+$")
        if isinstance(v,list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid original_spans format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid original_spans format: {v}")
        return v


class Disease(NamedEntity):
    """
    The name of a disease.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'annotators': {'tag': 'annotators',
                                        'value': 'sqlite:obo:mondo'},
                         'prompt': {'tag': 'prompt',
                                    'value': 'The name of a disease.'}},
         'from_schema': 'http://w3id.org/ontogpt/mic',
         'id_prefixes': ['MONDO']})

    id: str = Field(..., description="""A unique identifier for the named entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['this is populated during the grounding and normalization step'],
         'domain_of': ['NamedEntity', 'Publication']} })
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'aliases': ['name'],
         'annotations': {'owl': {'tag': 'owl',
                                 'value': 'AnnotationProperty, AnnotationAssertion'}},
         'domain_of': ['NamedEntity'],
         'slot_uri': 'rdfs:label'} })
    original_spans: Optional[List[str]] = Field(None, description="""The coordinates of the original text span from which the named entity was extracted, inclusive. For example, \"10:25\" means the span starting from the 10th character and ending with the 25th character. The first character in the text has index 0. Newlines are treated as single characters. Multivalued as there may be multiple spans for a single text.""", json_schema_extra = { "linkml_meta": {'alias': 'original_spans',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['This is determined during grounding and normalization',
                      'But is based on the full input text'],
         'domain_of': ['NamedEntity']} })

    @field_validator('original_spans')
    def pattern_original_spans(cls, v):
        pattern=re.compile(r"^\d+:\d+$")
        if isinstance(v,list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid original_spans format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid original_spans format: {v}")
        return v


class Phenotype(NamedEntity):
    """
    The name of a phenotype.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'annotators': {'tag': 'annotators', 'value': 'sqlite:obo:hp'},
                         'prompt': {'tag': 'prompt',
                                    'value': 'The name of a phenotype.'}},
         'from_schema': 'http://w3id.org/ontogpt/mic',
         'id_prefixes': ['HP']})

    id: str = Field(..., description="""A unique identifier for the named entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['this is populated during the grounding and normalization step'],
         'domain_of': ['NamedEntity', 'Publication']} })
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'aliases': ['name'],
         'annotations': {'owl': {'tag': 'owl',
                                 'value': 'AnnotationProperty, AnnotationAssertion'}},
         'domain_of': ['NamedEntity'],
         'slot_uri': 'rdfs:label'} })
    original_spans: Optional[List[str]] = Field(None, description="""The coordinates of the original text span from which the named entity was extracted, inclusive. For example, \"10:25\" means the span starting from the 10th character and ending with the 25th character. The first character in the text has index 0. Newlines are treated as single characters. Multivalued as there may be multiple spans for a single text.""", json_schema_extra = { "linkml_meta": {'alias': 'original_spans',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['This is determined during grounding and normalization',
                      'But is based on the full input text'],
         'domain_of': ['NamedEntity']} })

    @field_validator('original_spans')
    def pattern_original_spans(cls, v):
        pattern=re.compile(r"^\d+:\d+$")
        if isinstance(v,list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid original_spans format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid original_spans format: {v}")
        return v


class BiologicalProcess(NamedEntity):
    """
    The name of a biological process.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'annotators': {'tag': 'annotators', 'value': 'sqlite:obo:go'},
                         'prompt': {'tag': 'prompt',
                                    'value': 'The name of a biological process.'}},
         'from_schema': 'http://w3id.org/ontogpt/mic',
         'id_prefixes': ['GO'],
         'slot_usage': {'id': {'name': 'id',
                               'values_from': ['GOBiologicalProcessType']}}})

    id: str = Field(..., description="""A unique identifier for the named entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['this is populated during the grounding and normalization step'],
         'domain_of': ['NamedEntity', 'Publication'],
         'values_from': ['GOBiologicalProcessType']} })
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'aliases': ['name'],
         'annotations': {'owl': {'tag': 'owl',
                                 'value': 'AnnotationProperty, AnnotationAssertion'}},
         'domain_of': ['NamedEntity'],
         'slot_uri': 'rdfs:label'} })
    original_spans: Optional[List[str]] = Field(None, description="""The coordinates of the original text span from which the named entity was extracted, inclusive. For example, \"10:25\" means the span starting from the 10th character and ending with the 25th character. The first character in the text has index 0. Newlines are treated as single characters. Multivalued as there may be multiple spans for a single text.""", json_schema_extra = { "linkml_meta": {'alias': 'original_spans',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['This is determined during grounding and normalization',
                      'But is based on the full input text'],
         'domain_of': ['NamedEntity']} })

    @field_validator('original_spans')
    def pattern_original_spans(cls, v):
        pattern=re.compile(r"^\d+:\d+$")
        if isinstance(v,list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid original_spans format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid original_spans format: {v}")
        return v


class Anatomy(NamedEntity):
    """
    The name of an anatomical part or system.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'annotators': {'tag': 'annotators',
                                        'value': 'sqlite:obo:uberon'},
                         'prompt': {'tag': 'prompt',
                                    'value': 'The name of an anatomical part or '
                                             'system.'}},
         'from_schema': 'http://w3id.org/ontogpt/mic',
         'id_prefixes': ['UBERON']})

    id: str = Field(..., description="""A unique identifier for the named entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['this is populated during the grounding and normalization step'],
         'domain_of': ['NamedEntity', 'Publication']} })
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'aliases': ['name'],
         'annotations': {'owl': {'tag': 'owl',
                                 'value': 'AnnotationProperty, AnnotationAssertion'}},
         'domain_of': ['NamedEntity'],
         'slot_uri': 'rdfs:label'} })
    original_spans: Optional[List[str]] = Field(None, description="""The coordinates of the original text span from which the named entity was extracted, inclusive. For example, \"10:25\" means the span starting from the 10th character and ending with the 25th character. The first character in the text has index 0. Newlines are treated as single characters. Multivalued as there may be multiple spans for a single text.""", json_schema_extra = { "linkml_meta": {'alias': 'original_spans',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['This is determined during grounding and normalization',
                      'But is based on the full input text'],
         'domain_of': ['NamedEntity']} })

    @field_validator('original_spans')
    def pattern_original_spans(cls, v):
        pattern=re.compile(r"^\d+:\d+$")
        if isinstance(v,list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid original_spans format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid original_spans format: {v}")
        return v


class FoodOrSupplement(NamedEntity):
    """
    The name of a food or supplement.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'annotators': {'tag': 'annotators',
                                        'value': 'sqlite:obo:foodon'},
                         'prompt': {'tag': 'prompt',
                                    'value': 'The name of a food or supplement.'}},
         'from_schema': 'http://w3id.org/ontogpt/mic',
         'id_prefixes': ['FOODON']})

    id: str = Field(..., description="""A unique identifier for the named entity""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['this is populated during the grounding and normalization step'],
         'domain_of': ['NamedEntity', 'Publication']} })
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'aliases': ['name'],
         'annotations': {'owl': {'tag': 'owl',
                                 'value': 'AnnotationProperty, AnnotationAssertion'}},
         'domain_of': ['NamedEntity'],
         'slot_uri': 'rdfs:label'} })
    original_spans: Optional[List[str]] = Field(None, description="""The coordinates of the original text span from which the named entity was extracted, inclusive. For example, \"10:25\" means the span starting from the 10th character and ending with the 25th character. The first character in the text has index 0. Newlines are treated as single characters. Multivalued as there may be multiple spans for a single text.""", json_schema_extra = { "linkml_meta": {'alias': 'original_spans',
         'annotations': {'prompt.skip': {'tag': 'prompt.skip', 'value': 'true'}},
         'comments': ['This is determined during grounding and normalization',
                      'But is based on the full input text'],
         'domain_of': ['NamedEntity']} })

    @field_validator('original_spans')
    def pattern_original_spans(cls, v):
        pattern=re.compile(r"^\d+:\d+$")
        if isinstance(v,list):
            for element in v:
                if isinstance(v, str) and not pattern.match(element):
                    raise ValueError(f"Invalid original_spans format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid original_spans format: {v}")
        return v


class ScientificClaim(CompoundExpression):
    """
    A scientific claim made in the input text, structured as a relationship between entities.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/mic'})

    references: Optional[List[str]] = Field(None, description="""A semi-colon separated list of references supporting the claim, identified by number only.""", json_schema_extra = { "linkml_meta": {'alias': 'references', 'domain_of': ['ScientificClaim']} })


class NutrientToDiseaseRelationship(ScientificClaim):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['a Chemical to Disease relationship'],
         'from_schema': 'http://w3id.org/ontogpt/mic'})

    nutrient: Optional[str] = Field(None, description="""The name of the nutrient defined in the triple, including vitamins and minerals.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    relationship: Optional[str] = Field(None, description="""The name of a type of relationship between the nutrient and the disease.""", json_schema_extra = { "linkml_meta": {'alias': 'relationship',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToNutrientRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    disease: Optional[str] = Field(None, description="""The name of the disease defined in the triple.""", json_schema_extra = { "linkml_meta": {'alias': 'disease', 'domain_of': ['NutrientToDiseaseRelationship']} })
    references: Optional[List[str]] = Field(None, description="""A semi-colon separated list of references supporting the claim, identified by number only.""", json_schema_extra = { "linkml_meta": {'alias': 'references', 'domain_of': ['ScientificClaim']} })


class NutrientToPhenotypeRelationship(ScientificClaim):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['a Chemical to Phenotype relationship'],
         'from_schema': 'http://w3id.org/ontogpt/mic'})

    nutrient: Optional[str] = Field(None, description="""The name of the nutrient defined in the triple, including vitamins and minerals.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    relationship: Optional[str] = Field(None, description="""The name of a type of relationship between the nutrient and the phenotype.""", json_schema_extra = { "linkml_meta": {'alias': 'relationship',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToNutrientRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    phenotype: Optional[str] = Field(None, description="""The name of the phenotype defined in the triple.""", json_schema_extra = { "linkml_meta": {'alias': 'phenotype', 'domain_of': ['NutrientToPhenotypeRelationship']} })
    references: Optional[List[str]] = Field(None, description="""A semi-colon separated list of references supporting the claim, identified by number only.""", json_schema_extra = { "linkml_meta": {'alias': 'references', 'domain_of': ['ScientificClaim']} })


class NutrientToBiologicalProcessRelationship(ScientificClaim):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/mic'})

    nutrient: Optional[str] = Field(None, description="""The name of the nutrient defined in the triple, including vitamins and minerals.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    relationship: Optional[str] = Field(None, description="""The name of a type of relationship between the nutrient and the biological process.""", json_schema_extra = { "linkml_meta": {'alias': 'relationship',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToNutrientRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    process: Optional[str] = Field(None, description="""The name of the biological process defined in the triple.""", json_schema_extra = { "linkml_meta": {'alias': 'process', 'domain_of': ['NutrientToBiologicalProcessRelationship']} })
    references: Optional[List[str]] = Field(None, description="""A semi-colon separated list of references supporting the claim, identified by number only.""", json_schema_extra = { "linkml_meta": {'alias': 'references', 'domain_of': ['ScientificClaim']} })


class NutrientToNutrientRelationship(ScientificClaim):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['a Chemical to Chemical relationship'],
         'from_schema': 'http://w3id.org/ontogpt/mic'})

    nutrient_subject: Optional[str] = Field(None, description="""The name of a nutrient defined in the triple, including vitamins and minerals.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient_subject', 'domain_of': ['NutrientToNutrientRelationship']} })
    relationship: Optional[str] = Field(None, description="""The name of a type of relationship between the nutrient_subject and nutrient_object.""", json_schema_extra = { "linkml_meta": {'alias': 'relationship',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToNutrientRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    nutrient_object: Optional[str] = Field(None, description="""The name of a nutrient defined in the triple, including vitamins and minerals.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient_object', 'domain_of': ['NutrientToNutrientRelationship']} })
    references: Optional[List[str]] = Field(None, description="""A semi-colon separated list of references supporting the claim, identified by number only.""", json_schema_extra = { "linkml_meta": {'alias': 'references', 'domain_of': ['ScientificClaim']} })


class NutrientToHealthStatusRelationship(ScientificClaim):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/mic'})

    nutrient: Optional[str] = Field(None, description="""The name of the nutrient defined in the triple, including vitamins and minerals.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    relationship: Optional[str] = Field(None, description="""The name of a type of relationship between the nutrient and the anatomical part or system.""", json_schema_extra = { "linkml_meta": {'alias': 'relationship',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToNutrientRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    anatomy: Optional[str] = Field(None, description="""The name of the anatomical part or system defined in the triple.""", json_schema_extra = { "linkml_meta": {'alias': 'anatomy', 'domain_of': ['NutrientToHealthStatusRelationship']} })
    references: Optional[List[str]] = Field(None, description="""A semi-colon separated list of references supporting the claim, identified by number only.""", json_schema_extra = { "linkml_meta": {'alias': 'references', 'domain_of': ['ScientificClaim']} })


class NutrientToSourceRelationship(ScientificClaim):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontogpt/mic'})

    nutrient: Optional[str] = Field(None, description="""The name of the nutrient defined in the triple, including vitamins and minerals.""", json_schema_extra = { "linkml_meta": {'alias': 'nutrient',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    relationship: Optional[str] = Field(None, description="""The name of a type of relationship between the nutrient and the food or supplement.""", json_schema_extra = { "linkml_meta": {'alias': 'relationship',
         'domain_of': ['NutrientToDiseaseRelationship',
                       'NutrientToPhenotypeRelationship',
                       'NutrientToBiologicalProcessRelationship',
                       'NutrientToNutrientRelationship',
                       'NutrientToHealthStatusRelationship',
                       'NutrientToSourceRelationship']} })
    source: Optional[str] = Field(None, description="""The name of the food or supplement defined in the triple.""", json_schema_extra = { "linkml_meta": {'alias': 'source', 'domain_of': ['NutrientToSourceRelationship']} })
    references: Optional[List[str]] = Field(None, description="""A semi-colon separated list of references supporting the claim, identified by number only.""", json_schema_extra = { "linkml_meta": {'alias': 'references', 'domain_of': ['ScientificClaim']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
ExtractionResult.model_rebuild()
NamedEntity.model_rebuild()
CompoundExpression.model_rebuild()
Triple.model_rebuild()
TextWithTriples.model_rebuild()
TextWithEntity.model_rebuild()
RelationshipType.model_rebuild()
Publication.model_rebuild()
AnnotatorResult.model_rebuild()
Document.model_rebuild()
Nutrient.model_rebuild()
Disease.model_rebuild()
Phenotype.model_rebuild()
BiologicalProcess.model_rebuild()
Anatomy.model_rebuild()
FoodOrSupplement.model_rebuild()
ScientificClaim.model_rebuild()
NutrientToDiseaseRelationship.model_rebuild()
NutrientToPhenotypeRelationship.model_rebuild()
NutrientToBiologicalProcessRelationship.model_rebuild()
NutrientToNutrientRelationship.model_rebuild()
NutrientToHealthStatusRelationship.model_rebuild()
NutrientToSourceRelationship.model_rebuild()
