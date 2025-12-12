#!/bin/bash
set -e

# Colors
GREEN="\033[0;32m"
BLUE="\033[0;34m"
RED="\033[0;31m"
NC="\033[0m" # Reset

#########################################
# FUNCTIONS
#########################################

start_local() {
  echo -e "${GREEN}🚀 Starting LOCAL development environment...${NC}"
  echo ""

  # ----------------------------------------------
  # Redis + NGINX in Docker
  # ----------------------------------------------
  echo -e "${BLUE}🐳 Starting Redis + NGINX in Docker...${NC}"
  docker compose up -d redis nginx

  # ----------------------------------------------
  # exposed_or_not_api (port 5000)
  # ----------------------------------------------
  echo -e "${BLUE}➡️ Starting exposed_or_not_api (uvicorn:5000)...${NC}"
  (cd exposed_or_not && uvicorn main:app --reload --host 0.0.0.0 --port 5000) &

  # ----------------------------------------------
  # api_gateway (port 8000)
  # ----------------------------------------------
  echo -e "${BLUE}➡️ Starting api_gateway (uvicorn:8000)...${NC}"
  (cd api_gateway && uvicorn main:app --reload --host 0.0.0.0 --port 8000) &

  # ----------------------------------------------
  # Frontend (Vite)
  # ----------------------------------------------
  echo -e "${BLUE}➡️ Starting frontend dev server (Vite:5173)...${NC}"
  (cd frontend_cyber && npm run dev) &

  echo ""
  echo -e "${GREEN}🔥 LOCAL DEV environment running!${NC}"
  echo "-------------------------------------------"
  echo "Frontend:            http://localhost:5173"
  echo "API Gateway:         http://localhost:8000"
  echo "Microservice:        http://localhost:5000"
  echo "NGINX Proxy:         http://localhost/api"
  echo ""
}

start_docker() {
  echo -e "${GREEN}🐳 Starting FULL DOCKER environment...${NC}"
  docker compose up -d --build
  echo ""
  echo -e "${GREEN}🔥 Full Docker environment running!${NC}"
  echo ""
}

stop_all() {
  echo -e "${RED}🛑 Stopping local processes + Docker services...${NC}"

  # Kill Python + Node local dev processes
  pkill -f "uvicorn main:app" 2>/dev/null || true
  pkill -f "npm run dev" 2>/dev/null || true

  docker compose stop

  echo -e "${GREEN}✔ Everything stopped.${NC}"
}

clean_all() {
  echo -e "${RED}🧹 Cleaning EVERYTHING...${NC}"

  pkill -f "uvicorn main:app" 2>/dev/null || true
  pkill -f "npm run dev" 2>/dev/null || true

  docker compose down --remove-orphans --volumes

  echo -e "${GREEN}✔ Clean done.${NC}"
}

#########################################
# MENU
#########################################

while true; do
  echo ""
  echo "==============================="
  echo "   🛠  Development Launcher"
  echo "==============================="
  echo "1) Run LOCAL development mode"
  echo "2) Run FULL DOCKER mode"
  echo "3) Stop everything"
  echo "4) Clean everything"
  echo "5) Exit"
  echo "==============================="
  read -p "Choose an option: " OPTION

  case $OPTION in
    1) start_local ;;
    2) start_docker ;;
    3) stop_all ;;
    4) clean_all ;;
    5) exit 0 ;;
    *) echo -e "${RED}Invalid choice!${NC}" ;;
  esac
done
