// Used by the sources endpoint.
// Returns information on sources--i.e., nodes in the UBKGSOURCE ontology.

// Get the source nodes, which are children of the "Source" node.
// Filter by UBKG context in the calling function.
CALL
{
	MATCH (t:Term)<-[r:PT]-(c:Code)<-[:CODE]-(p:Concept)-[:isa]->(pParent:Concept),(p:Concept)-[:in_ubkg_context]->(pContext:Concept)-[:CODE]->(cContext:Code)-[rContext:PT]-(tContext:Term)
	WHERE pParent.CUI = 'UBKGSOURCE:C000001 CUI'
	AND r.CUI=p.CUI
	$contextfilter
	RETURN DISTINCT p.CUI as CUISource, c.CodeID As CodeIDSource, t.name AS nameSource
}
// SAB
// Filter by SAB in the calling function.
CALL
{
	WITH CUISource
	MATCH (pSource:Concept)-[:has_sab]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	$sabfilter
	AND r.CUI = p.CUI
	RETURN t.name AS sab
}
// Source name
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:has_name]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	AND r.CUI = p.CUI
	RETURN t.name AS source_name
}
// Source description
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:has_description]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	AND r.CUI = p.CUI
	RETURN DISTINCT t.name AS source_description
}
// home urls
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:has_home_url]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	AND r.CUI = p.CUI
	RETURN COLLECT(t.name) AS home_urls
}
// source dictionary url
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:has_source_dictionary_url]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	AND r.CUI = p.CUI
	RETURN t.name AS source_dictionary_url
}
// citations as both PMID and URL
CALL
{
	WITH CUISource
	MATCH (pSource:Concept)-[:has_citation]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	AND r.CUI = p.CUI
	RETURN COLLECT({pmid:CASE WHEN split(t.name,':')[0]='PMID' THEN split(t.name,':')[1] END,
	url:CASE WHEN split(t.name,':')[0]<>'PMID' THEN t.name ELSE 'https://pubmed.ncbi.nlm.nih.gov/'+split(t.name,':')[1] END}) AS citations
}

// ETL command
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:has_etl_command]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	AND r.CUI = p.CUI
	RETURN t.name AS source_etl_command
}
// ETL OWL
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:has_etl_owl]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	AND r.CUI = p.CUI
	RETURN t.name AS source_etl_owl
}
// source_version
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:has_source_version]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	AND r.CUI = p.CUI
	RETURN t.name AS source_version
}
// source_type, translated
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:has_source_type]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	AND r.CUI = p.CUI
	RETURN split(t.name,'source_type_')[1] AS source_type
}
// download_date
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:has_download_date]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	AND r.CUI = p.CUI
	RETURN t.name AS source_download_date
}
// license
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:has_license]->(pLicense:Concept)
	WHERE pSource.CUI = CUISource
	RETURN pLicense.CUI AS CUILicense
}
// license type
CALL
{
	WITH CUILicense
	OPTIONAL MATCH (pLicense:Concept)-[:has_license_type]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pLicense.CUI=CUILicense
	RETURN t.name AS license_type, p.CUI AS CUILicenseType
}
// license definition, which is linked to the license type
CALL
{
	WITH CUILicenseType
	OPTIONAL MATCH (pLicense:Concept)-[:DEF]->(d:Definition)
	WHERE pLicense.CUI=CUILicenseType
	RETURN d.DEF AS license_definition
}
// license subtype
CALL
{
	WITH CUILicense
	OPTIONAL MATCH (pLicense:Concept)-[:has_license_subtype]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pLicense.CUI=CUILicense
	RETURN t.name AS license_subtype
}
// license version
CALL
{
	WITH CUILicense
	OPTIONAL MATCH (pLicense:Concept)-[:has_license_version]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pLicense.CUI=CUILicense
	RETURN t.name AS license_version
}
// ubkg context
CALL
{
	WITH CUISource
	OPTIONAL MATCH (pSource:Concept)-[:in_ubkg_context]->(p:Concept)-[:CODE]->(c:Code)-[r:PT]->(t:Term)
	WHERE pSource.CUI=CUISource
	RETURN t.name AS context
}

WITH CUISource,sab,source_name,source_description, source_dictionary_url,home_urls, citations,
CASE WHEN source_etl_command IS NULL THEN source_etl_owl ELSE source_etl_command END as source_etl,
source_version, source_type,source_download_date, COLLECT(DISTINCT CASE WHEN license_type is NULL THEN NULL ELSE {type: CASE WHEN license_definition IS NULL THEN license_type ELSE license_definition END,subtype:license_subtype,version:license_version} END) AS licenses, COLLECT(DISTINCT context) AS contexts
WITH {sab:sab,name:source_name,description:source_description,home_urls:home_urls,source_dictionary_url:source_dictionary_url,citations:citations,source_etl:source_etl,source_version:source_version, source_type:source_type, download_date:source_download_date,licenses:licenses,contexts:contexts} AS source
WITH COLLECT(source) AS sources
RETURN {sources:sources} AS response