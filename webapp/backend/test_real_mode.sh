#!/bin/bash
# Test script for real OpenOA mode
# Make sure the API server is running on port 8000

echo "Testing Real OpenOA Integration"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Check health endpoint
echo -e "${BLUE}1. Testing Health Endpoint${NC}"
curl -s http://localhost:8000/health | jq '.'
echo -e "\n"

# 2. Check info endpoint (should show OpenOA version)
echo -e "${BLUE}2. Testing Info Endpoint (should show OpenOA version)${NC}"
curl -s http://localhost:8000/api/v1/info | jq '.'
echo -e "\n"

# 3. Get sample data summary
echo -e "${BLUE}3. Testing Sample Data Summary${NC}"
curl -s http://localhost:8000/api/v1/data/sample-data/summary | jq '.'
echo -e "\n"

# 4. Get plant metadata
echo -e "${BLUE}4. Testing Plant Metadata${NC}"
curl -s http://localhost:8000/api/v1/data/sample-data/metadata | jq '.'
echo -e "\n"

# 5. Run AEP analysis with default iterations (should use real OpenOA)
echo -e "${BLUE}5. Testing AEP Analysis with Real OpenOA (1000 iterations)${NC}"
echo "This may take a few seconds..."
curl -s -X POST http://localhost:8000/api/v1/analysis/aep \
  -H "Content-Type: application/json" \
  -d '{"iterations": 1000}' | jq '.'
echo -e "\n"

# 6. Run AEP analysis with more iterations
echo -e "${BLUE}6. Testing AEP Analysis with 5000 iterations${NC}"
echo "This will take longer..."
curl -s -X POST http://localhost:8000/api/v1/analysis/aep \
  -H "Content-Type: application/json" \
  -d '{"iterations": 5000}' | jq '.'
echo -e "\n"

echo -e "${GREEN}✓ All tests completed!${NC}"
echo ""
echo "Check the results above:"
echo "- analysis_type should say 'real' (not 'mock')"
echo "- notes should NOT mention 'USE_MOCK_DATA=True'"
echo "- results should vary between runs (not deterministic)"
