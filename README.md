AI Video Engineer - Backend

Automated video generation system using AI. Converts text scripts into professional videos with AI presenters.

Project Structure

ai-video-engineer-backend/
- app/ (main Flask application)
- scripts/ (AI processing: OpenAI, ElevenLabs, HeyGen, FFmpeg, Wasabi, Bubble)
- config/ (settings and configuration)
- cron_job.py (cleanup tasks)
- requirements.txt (Python packages)
- Procfile (deployment)
- .env.example (sample environment variables)
- README.md (this file)

Quick Start - Local Testing (No API Keys Needed!)

Step 1: Clone Repository
  git clone https://github.com/princeflexzy0/ai-video-engineer-backend.git
  cd ai-video-engineer-backend

Step 2: Setup Python Environment
  python3 -m venv venv
  source venv/bin/activate

Step 3: Install Dependencies
  pip install -r requirements.txt

Step 4: Setup Environment Variables
  cp .env.example .env
  echo "MOCK_MODE=True" > .env

Step 5: Run the Server
  python app/main.py

Server starts at: http://localhost:10000

Test the API

Test 1: Health Check
  curl http://localhost:10000/health

Test 2: Generate Video
  curl -X POST http://localhost:10000/generate-video -H "Content-Type: application/json" -d '{"script":"Amazon rainforest test","template":"presenter1","userId":"test@example.com"}'

Test 3: Check Status
  curl http://localhost:10000/video-status/YOUR-VIDEO-ID

API Endpoints

GET /           - API info
GET /health     - Health check
POST /generate-video - Start video generation
GET /video-status/ID - Check video status

Configuration

Mock Mode (Testing - No API Keys): MOCK_MODE=True
Production Mode (Real Videos): MOCK_MODE=False + add all API keys

Deploy to Render.com

1. Connect GitHub repository
2. Build Command: pip install -r requirements.txt
3. Start Command: gunicorn --bind 0.0.0.0:$PORT app.main:app
4. Add environment variables from .env.example
5. Deploy!

Tech Stack

Flask, Socket.io, OpenAI GPT-4, ElevenLabs, HeyGen, FFmpeg, Wasabi S3, Bubble.io

Related Projects

Frontend: https://github.com/princeflexzy0/ai-video-engineer-frontend

Built with love by AI Video Engineer Team
