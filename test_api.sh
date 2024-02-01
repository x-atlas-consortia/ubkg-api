#!/bin/bash
set -e
set -u

UBKG_URL_PROD=https://ontology.api.hubmapconsortium.org
UBKG_URL_DEV=https://ontology-api.dev.hubmapconsortium.org
UBKG_URL_TEST=https://ontology-api.test.hubmapconsortium.org
UBKG_URL_LOCAL=http://127.0.0.1:5002

UBKG_URL=$UBKG_URL_LOCAL
echo "Using UBKG at: ${UBKG_URL}"

echo "TESTS FOR: codes/<code_id/codes GET"
echo "1. codes/<code_id>/codes GET with invalid parameter; should return custom 400"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3C254837009/codes?test=test" \
 --header "Accept: application/json"

echo "2. codes/<code_id>/codes GET with non-existent sab; should return custom 404"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3C254837009/codes?sab=999" \
 --header "Accept: application/json"
echo

echo "3. codes/<code_id>/codes GET with non-existent code; should return custom 404"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3C254837009X/codes" \
 --header "Accept: application/json"
echo

echo "4. codes/<code_id>/codes GET with sab as comma-delimited list of existing SABs; should return 200"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3C254837009/codes?sab=CHV,DOID" \
 --header "Accept: application/json"
echo

echo "5. codes/<code_id>/codes GET with individual sabs; should return 200"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3C254837009/codes?sab=CHV&sab=DOID" \
 --header "Accept: application/json"
echo

echo "TESTS FOR: codes/<code_id>/concepts"
echo "1. codes/<code_id/concepts GET with invalid code; should return custom 404"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%20254837009X/concepts" \
 --header "Accept: application/json"
echo

echo "2. codes/<code_id/concepts GET with valid code; should return 200"
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%20254837009/concepts" \
 --header "Accept: application/json"
echo

echo "TESTS FOR: concepts/<concept_id>/codes"
echo "1. concepts/<concept_id>/codes GET with invalid parameter; should return custom 400"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/codes?application_context=HUBMAP" \
 --header "Accept: application/json"
echo
echo "2. concepts/<concept_id>/codes GET with invalid concept; should return custom 404"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222x/codes" \
 --header "Accept: application/json"
echo
echo "3. concepts/<concept_id>/codes GET with valid concept; should return 200"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/codes" \
 --header "Accept: application/json"
echo

echo "TESTS FOR: concepts/<concept_id>/concepts GET"
echo "1. concepts/<concept_id>/concepts GET with invalid concept; should return custom 404"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222X/concepts" \
 --header "Accept: application/json"
echo
echo "2. concepts/<concept_id>/concepts GET with valid concept; should return 200"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/concepts" \
 --header "Accept: application/json"
echo

echo "TESTS FOR:  concepts/<concept_id>/definitions"
echo "1. concepts/<concept_id>/definitions GET with invalid concept; should return custom 404"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222x/definitions" \
 --header "Accept: application/json"
echo
echo "2. concepts/<concept_id>/definitions GET with valid concept; should return 200"
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/definitions" \
 --header "Accept: application/json"
echo

echo "TESTS FOR: concepts/<concept_id>/expand GET"
echo "1. concepts/<concept_id>/expand GET with missing required parameters; should return custom 400"
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/expand" \
 --header "Accept: application/json"
echo

echo "2. concepts/<concept_id>/expand GET with invalid parameter name; should return custom 400"
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/expand?sab=SNOMEDCT_US&rel=isa&depth2=2" \
 --header "Accept: application/json"
echo

echo "3. concepts/<concept_id>/expand GET with invalid concept id; should return custom 404"
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507Z/expand?sab=SNOMEDCT_US&rel=isa&depth=2" \
 --header "Accept: application/json"
echo
echo "4. concepts/<concept_id>/expand GET with valid parameters; should return 200"
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/expand?sab=SNOMEDCT_US&rel=isa&depth=2" \
 --header "Accept: application/json"
echo

echo "TESTS FOR: concepts/<concept_id>/paths GET "
echo "1. concepts/paths GET with missing parameters; should return custom 400"
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths" \
 --header "Accept: application/json"
echo

echo "2. concepts/paths GET with invalid parameter name; should return custom 400"
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths?sab=SNOMEDCT_US&rel2=isa" \
 --header "Accept: application/json"
echo
echo "3. concepts/paths GET with invalid concept_id; should return custom 404"
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507z/paths?sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json"
echo
echo "4. concepts/paths GET with valid parameters; should return 200"
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths?sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json"
echo

echo "TESTS FOR: concepts/<concept_id>/shortestpaths POST"
echo "concepts/shortestpaths POST..."
curl --request POST \
 --url "${UBKG_URL}/concepts/shortestpaths" \
 --header "Content-Type: application/json" \
 --data '{"query_concept_id": "C2720507", "target_concept_id": "C1272753", "sab": ["SNOMEDCT_US", "HGNC"], "rel": ["isa", "part_of"]}'
echo

echo "concepts/trees POST..."
curl --request POST \
 --url "${UBKG_URL}/concepts/trees" \
 --header "Content-Type: application/json" \
 --data '{"query_concept_id": "C2720507", "sab": ["SNOMEDCT_US", "HGNC"], "rel": ["isa", "isa"], "depth": 2}'
echo

echo "semantics/<semantic_id>/semantics GET"
curl --request GET \
 --url "${UBKG_URL}/semantics/Physical%20Object/semantics?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "terms/<term_id>/codes GET"
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/codes?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "terms/<term_id>/concepts GET"
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/concepts?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "terms/<term_id>/concepts/terms GET"
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/concepts/terms?application_context=HUBMAP" \
 --header "Accept: application/json"
echo

echo "tui/<tui_id>/semantics GET"
curl --request GET \
 --url "${UBKG_URL}/tui/T200/semantics?application_context=HUBMAP" \
 --header "Accept: application/json"
echo
