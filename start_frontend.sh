#!/bin/bash

# Start Frontend Server
cd "$(dirname "$0")/frontend"
npm install
npm run dev

