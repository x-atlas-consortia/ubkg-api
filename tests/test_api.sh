#!/bin/bash
set -e
set -u

###########
# Help function
##########
Help()
{
   # Display Help
   echo ""
   echo "****************************************"
   echo "HELP: UBKG API test script"
   echo | tee
   echo "Syntax: ./test_api.sh [-option]..."
   echo "option" | tee
   echo "-v     test environment: l (local), d (DEV), or p (PROD)"
   echo "NOTE: This script writes output to a file named test.out."
}

#####
# Get options
while getopts ":hv:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      v) # environment
         env=$OPTARG;;
      \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done


UBKG_URL_PROD=https://ontology.api.hubmapconsortium.org
UBKG_URL_DEV=https://ontology-api.dev.hubmapconsortium.org
UBKG_URL_TEST=https://ontology-api.test.hubmapconsortium.org
UBKG_URL_LOCAL=http://127.0.0.1:5002

# Map to selected API environment.
case "$env" in
  l) # local
    UBKG_URL="${UBKG_URL:-$UBKG_URL_LOCAL}";;
  d) # DEV
    UBKG_URL="${UBKG_URL:-$UBKG_URL_DEV}";;
  p) # PROD
    UBKG_URL="${UBKG_URL:-$UBKG_URL_PROD}";;
  \?) # default to local machine
    UBKG_URL="${UBKG_URL:-$UBKG_URL_LOCAL}";;

esac

UBKG_URL=$UBKG_URL_LOCAL
echo "Using UBKG at: ${UBKG_URL}" | tee test.out
echo "Only the first 60 characters of output from HTTP 200 returns displayed."

#--------------------------------------------
echo "TESTS FOR: codes/<code_id/codes GET" | tee -a test.out
echo "1. /codes/SNOMEDCT_US%3A254837009/codes?test=test =>invalid parameter; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/codes?test=test" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. codes/SNOMEDCT_US%3A254837009/codes?sab=999 =>non-existent sab; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/codes?sab=999" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "3. codes/SNOMEDCT_US%3A254837009X/codes => non-existent code; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009X/codes" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "4. codes/SNOMEDCT_US%3A254837009/codes?sab=CHV,DOID => with sab as comma-delimited list of existing SABs; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/codes?sab=CHV,DOID" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "5. /codes/SNOMEDCT_US%3A254837009/codes?sab=CHV&sab=DOID => with individual sabs; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/codes?sab=CHV&sab=DOID" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: codes/<code_id>/concepts" | tee -a test.out
echo "1. codes/SNOMEDCT_US%3A254837009X/concepts => with invalid code; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009X/concepts" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out

echo "2. /codes/SNOMEDCT_US%3A254837009/concepts => valid code; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/codes/SNOMEDCT_US%3A254837009/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

echo "TESTS FOR: concepts/<concept_id>/codes GET" | tee -a test.out
echo "1. concepts/C0678222/codes?test=x => invalid parameter; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/codes?test=x" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C0678222x/codes => invalid concept; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222x/codes" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. concepts/C0678222/codes => valid concept; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/codes" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/<concept_id>/concepts GET" | tee -a test.out
echo "1. concepts/C0678222X/concepts => invalid concept; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222X/concepts" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C0678222/concepts => valid concept; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR:  concepts/<concept_id>/definitions" | tee -a test.out
echo "1. concepts/C0678222x/definitions => invalid concept; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222x/definitions" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C0678222/definitions => valid concept; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C0678222/definitions" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/subgraph"
echo "1. concepts/subgraph?sab=SNOMEDCT_US&rel=isaz=> invalid parameter value: should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/subgraph?sab=SNOMEDCT_US&rel=isaz" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/subgraph?sab=SNOMEDCT_US&rel=isa&limit=-1 => negative parameter: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/subgraph?sab=SNOMEDCT_US&rel=isa&skip=0&limit=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. concepts/subgraph?sab=SNOMEDCT_US&rel=isa&skip=0&limit=10 => valid parameters: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/subgraph?sab=SNOMEDCT_US&rel=isa&skip=0&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/<identifier>/nodes GET" | tee -a test.out
echo "1. concepts/Cellsz/nodes => invalid search term; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/Cellsz/nodes" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/Cells/nodes => valid search term; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/Cells/nodes" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/<concept_id>/paths/expand GET" | tee -a test.out
echo "1. concepts/C2720507/paths/expand => missing required parameters; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth2=2&maxdepth=3 => invalid parameter name; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth2=2&maxdepth=3" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. concepts/C2720507Z/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3 => invalid concept id; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507Z/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "4. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=z&maxdepth=3 => non-numeric depth; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=z&maxdepth=3" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "5. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=3&maxdepth=2 => parameter order invalid; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=3&maxdepth=2" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "6. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10 => long query; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out
echo "7. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=-1 => negative parameter value; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out
echo "8. concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&skip=0&limit=10 => valid parameters; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/<concept_id>/paths/trees GET" | tee -a test.out
echo "1. concepts/C2720507/paths/trees => missing parameters: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C2720507/paths/trees?sab2=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3 => invalid parameter: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab2=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=z&maxdepth=3 => non-numeric depth: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&depth=z" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "4. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=3&maxdepth=2 => invalid parameter order: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&depth=3" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "5. concepts/C2720507Z/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3 => invalid concept_id: should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507Z/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "6. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&skip=-1 => negative value: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&skip=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "6. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&limit=10 => invalid mindepth: should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=2&maxdepth=3&limit=10" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "7. concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=0&maxdepth=3&limit=10 => valid parameters: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/paths/trees?sab=SNOMEDCT_US&rel=isa&mindepth=0&maxdepth=3&limit=10" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: concepts/<origin_concept_id>/<terminus_concept_id>/shortestpath GET" | tee -a test.out
echo "1. concepts/C2720507/C1272753/shortestpath => missing parameters; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/C1272753/shortestpath" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. concepts/C2720507/C1272753/shortestpath?sab=SNOMEDCT_US&rel2=isa => invalid parameter name; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/C1272753/shortestpath?sab=SNOMEDCT_US&rel2=isa" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. concepts/C2720507Z/C1272753/shortestpath?sab=SNOMEDCT_US&rel=isa => invalid concept_id; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507Z/C1272753/shortestpath?sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "4. concepts/C2720507/C1272753/shortestpath?sab=SNOMEDCT_US&rel=isa => valid parameters; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/concepts/C2720507/C1272753/shortestpath?sab=SNOMEDCT_US&rel=isa" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: node_types/counts GET" | tee -a test.out
echo "1. node_types/counts GET => no match; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/counts/Codez" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. node_types/counts GET => valid; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/counts/Code" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: node_types/counts_by_sab GET" | tee -a test.out
echo "1. node_types/counts_by_sab GET => blocked because of likely timeout; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/counts_by_sab?test=test" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. node_types/counts_by_sab/Codez GET => invalid parameter; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/counts_by_sab/Codez" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. node_types/counts_by_sab/Code GET => valid; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/counts_by_sab/Code" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out
echo "3. node_types/counts_by_sab/Code?sab=NCI GET => valid parameter; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/node_types/counts_by_sab/Code?sab=NCI" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: property_types GET" | tee -a test.out
echo "1. property_types GET => valid; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/property_types" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: relationship_types GET" | tee -a test.out
echo "1. relationship_types GET => valid; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/relationship_types" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: semantics/semantic_types GET" | tee -a test.out
echo "1. semantics/semantic_types => should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_types" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out
echo "2. semantics/semantic_types?type=Anatomical%20Structurez => invalid semantic type; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_types?type=Anatomical%20Structurez" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. semantics/semantic_types?type=Anatomical%20Structure => valid semantic type; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_types?type=Anatomical%20Structure" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: semantics/semantic_subtypes GET" | tee -a test.out
echo "1. semantics/semantic_subtypes/Anatomical%20Structurez => invalid semantic type; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_subtypes/Anatomical%20Structurez" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. semantics/semantic_subtypes/Anatomical%20Structure&skip=-1 => invalid skip; should return custom 400" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_subtypes/Anatomical%20Structure&skip=-1" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "3. semantics/semantic_subtypes/Anatomical%20Structure => valid parameters; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/semantics/semantic_subtypes/Anatomical%20Structure" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: terms/<term_id>/codes GET" | tee -a test.out
echo "1. terms/Breast%20cancerz/codes => no match; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancerz/codes" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. terms/Breast%20cancer/codes GET with match: should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/codes" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out

#--------------------------------------------
echo "TESTS FOR: terms/<term_id>concepts GET" | tee -a test.out
echo "1. terms/Breast%20cancerz/concepts GET with no match; should return custom 404" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancerz/concepts" \
 --header "Accept: application/json" | tee -a test.out
echo | tee -a test.out
echo "2. terms/Breast%20cancer/concepts GET with match; should return 200" | tee -a test.out
curl --request GET \
 --url "${UBKG_URL}/terms/Breast%20cancer/concepts" \
 --header "Accept: application/json" | cut -c1-60 | tee -a test.out
echo | tee -a test.out