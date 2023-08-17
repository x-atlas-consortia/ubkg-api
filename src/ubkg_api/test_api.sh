#!/bin/bash
set -e
set -u

INGESTAPI_URL_PROD=https://ingest.api.hubmapconsortium.org
INGESTAPI_URL_DEV=https://ingest-api.dev.hubmapconsortium.org
INGESTAPI_URL_TEST=https://ingest-api.test.hubmapconsortium.org
INGESTAPI_URL_LOCAL=http://localhost:8484
INGESTAPI_URL=$INGESTAPI_URL_DEV

UBKG_URL_PROD=https://ontology.api.hubmapconsortium.org
UBKG_URL_DEV=https://ontology-api.dev.hubmapconsortium.org
UBKG_URL_LOCAL=http://127.0.0.1:5002
UBKG_URL=$UBKG_URL_LOCAL

SEARCH_URL_DEV=https://search-api.dev.hubmapconsortium.org
SEARCH_URL_TEST=https://search-api.test.hubmapconsortium.org
SEARCH_URL=$SEARCH_URL_DEV

UUID_URL_DEV=https://uuid-api.dev.hubmapconsortium.org
UUID_URL=$UUID_URL_DEV


# To get the BEARER_TOKEN, login through the UI (https://ingest.hubmapconsortium.org/) to get the credentials...
# In Firefox open 'Tools > Browser Tools > Web Developer Tools'.
# Click on "Storage" then the dropdown for "Local Storage" and then the url,
# Applications use the "groups_token" from the returned information.
# UI times-out in 15 min so close the browser window, and the token will last for a day or so.
#
# Run this with....
# export TOKEN="xxx"; ./src/ubkg_api/test_api.sh

echo "assayname_POST..."
curl --request POST \
 --url "${UBKG_URL}/assayname" \
 --header "Content-Type: application/json" \
 --header "Authorization: Bearer ${TOKEN}" \
 --data '{"name": "bulk-RNA"}'
echo

echo "assaytype GET"
curl --request GET \
 --url "${UBKG_URL}/assaytype?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "assaytype/<name> GET"
curl --request GET \
 --url "${UBKG_URL}/assaytype/bulk-RNA?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "codes/<code_id>/codes GET"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%20254837009/codes?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "codes/<code_id>/concepts GET"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%20254837009/concepts?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "concepts/<concept_id>/codes GET"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/codes?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "concepts/<concept_id>/concepts GET"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/concepts?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "concepts/<concept_id>/definitions GET"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/definitions?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "concepts/<concept_id>/semantics GET"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/semantics?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "concepts/expand POST..."
curl --request POST \
 --url "${UBKG_URL}/concepts/expand" \
 --header "Content-Type: application/json" \
 --header "Authorization: Bearer ${TOKEN}" \
 --data '{"query_concept_id": "C2720507", "sab": ["SNOMEDCT_US", "HGNC"], "rel": ["isa", "isa"], "depth": 2}'
echo

echo "concepts/paths POST..."
curl --request POST \
 --url "${UBKG_URL}/concepts/paths" \
 --header "Content-Type: application/json" \
 --header "Authorization: Bearer ${TOKEN}" \
 --data '{"query_concept_id": "C2720507", "sab": ["SNOMEDCT_US", "HGNC"], "rel": ["isa", "isa"]}'
echo

echo "concepts/shortestpaths POST..."
curl --request POST \
 --url "${UBKG_URL}/concepts/shortestpaths" \
 --header "Content-Type: application/json" \
 --header "Authorization: Bearer ${TOKEN}" \
 --data '{"query_concept_id": "C2720507", "target_concept_id": "C1272753", "sab": ["SNOMEDCT_US", "HGNC"], "rel": ["isa", "part_of"]}'
echo

echo "concepts/trees POST..."
curl --request POST \
 --url "${UBKG_URL}/concepts/trees" \
 --header "Content-Type: application/json" \
 --header "Authorization: Bearer ${TOKEN}" \
 --data '{"query_concept_id": "C2720507", "sab": ["SNOMEDCT_US", "HGNC"], "rel": ["isa", "isa"], "depth": 2}'
echo

echo "semantics/<semantic_id>/semantics GET"
curl --request GET \
 --url "${UBKG_URL}/semantics/Physical%20Object/semantics?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "terms/<term_id>/codes GET"
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/codes?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "terms/<term_id>/concepts GET"
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/concepts?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "terms/<term_id>/concepts/terms GET"
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/concepts/terms?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo

echo "tui/<tui_id>/semantics GET"
curl --request GET \
 --url "${UBKG_URL}/tui/T200/semantics?application_context=HUBMAP" \
 --header "Accept: application/json" \
 --header "Authorization: Bearer ${TOKEN}"
echo
