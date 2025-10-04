# The Price is Bot - Complete System

A modernized AI-powered grocery shopping challenge that showcases Elastic's Agent Builder capabilities at conferences and demos.

## 🏗️ Architecture Overview

This system consists of four main components:

```
┌─────────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   Data Generator    │    │   Agent Builder      │    │   Game Frontend     │
│                     │    │   Integration        │    │                     │
│  • Grocery items    │    │                      │    │  • Next.js 14       │
│  • Store locations  │    │  • 8 Specialized     │    │  • Agent chat       │
│  • Inventory        │    │    tools             │    │  • Shopping cart    │
│  • Promotions       │    │  • 5 Unique agents   │    │  • Leaderboard      │
│  • Nutrition data   │    │  • ES|QL queries     │    │  • Admin panel      │
└─────────────────────┘    └──────────────────────┘    └─────────────────────┘
           │                           │                           │
           │                           │                           │
           ▼                           ▼                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Elasticsearch Cluster                            │
│                                                                             │
│  • grocery_items          • store_inventory        • game_sessions         │
│  • store_locations        • seasonal_availability  • access_codes          │
│  • nutrition_facts        • promotional_offers     • leaderboard_*         │
└─────────────────────────────────────────────────────────────────────────────┘
           ▲
           │
┌─────────────────────┐
│  Leaderboard API    │
│                     │
│  • FastAPI service  │
│  • Access codes     │
│  • Session mgmt     │
│  • Scoring system   │
└─────────────────────┘
```

## 🚀 Quick Start

### 1. Generate Data
```bash
cd grocery-data-generator
pip install -r requirements.txt
python control.py --es-url YOUR_ES_URL --es-api-key YOUR_KEY --generate-all
```

### 2. Start Leaderboard API
```bash
cd leaderboard-api
pip install -r requirements.txt
export ELASTICSEARCH_URL=YOUR_ES_URL
export ELASTICSEARCH_API_KEY=YOUR_KEY
python main.py
```

### 3. Launch Game UI
```bash
cd game-ui
npm install
npm run dev
```

### 4. Create Agent Builder Components
```bash
cd agent-builder-service
# Use the provided API client to create agents/tools per session
```

## 📦 Components

### [Grocery Data Generator](./grocery-data-generator/)
- **50,000 grocery items** with realistic names, brands, pricing
- **20 Las Vegas stores** with fun themed names
- **300,000 inventory records** with dynamic pricing
- **Seasonal availability** and **promotional offers**
- **Nutrition data** and **recipe combinations**

**Key Features:**
- LLM-powered data generation (Claude 3.5 Sonnet)
- Configurable dataset sizes
- JSON file output for repeatability
- ES|QL-ready index mappings

### [Agent Builder Integration](./agent-builder-service/)
- **8 Specialized tools** for grocery shopping
- **5 Unique agent personalities** 
- **Session-based isolation** (no cross-user contamination)
- **Dynamic agent/tool creation** via Kibana APIs

**Agents:**
- 💰 **Budget Master** - Price optimization expert
- 🥗 **Health Guru** - Nutrition and dietary focus
- 👨‍🍳 **Gourmet Chef** - Recipe and ingredient pairing
- ⚡ **Speed Shopper** - Quick decision specialist
- 🎰 **Vegas Local Expert** - Las Vegas store insider

### [Game Frontend](./game-ui/)
- **Next.js 14** with modern React patterns
- **Framer Motion** animations and transitions
- **Zustand** state management
- **Tailwind CSS** with Vegas + Elastic theming

**Features:**
- Responsive mobile-first design
- Real-time agent chat interface
- Interactive shopping cart with budget tracking
- Live leaderboard with confetti celebrations

### [Leaderboard API](./leaderboard-api/)
- **FastAPI** service for session management
- **Access code system** with QR code generation
- **Rolling leaderboards** by date
- **Scoring algorithm** (price accuracy + speed)

## 🎯 Game Mechanics

### Objective
Build a grocery cart as close to **$100** as possible without going over.

### Scoring System
- **Price Accuracy (70 points max):** Closer to $100 = higher score
- **Speed Bonus (30 points max):** Faster completion = more points
- **Over Budget:** Automatic score of 0

### Fair Play
- All agents available to all players
- Different tools per agent for strategic variety
- Equal opportunity for prizes (conference legal requirement)

## 🏢 Conference Setup

### For AWS re:Invent
- **Instruqt Integration:** Each player gets isolated ES cluster
- **QR Code Access:** Print cards with unique access codes
- **Large Leaderboard Display:** Live updates during event
- **Agent Builder Showcase:** Users see tools/agents in Kibana first

### Booth Experience
1. **QR Code Scan** → Access code entry
2. **Agent Builder Tour** → 2-minute Kibana walkthrough
3. **Agent Selection** → Choose shopping personality
4. **5-Minute Game** → Build perfect $100 cart
5. **Leaderboard** → Compete for prizes

## 🛠️ Development Status

### ✅ Completed
- Grocery data generator with LLM integration
- Agent Builder API client with 8 tools + 5 agents
- External leaderboard API with access codes
- Modern game UI with all core components
- Admin panel for code generation

### 🚧 Next Steps
- Instruqt track development
- Agent Builder → Game UI integration
- Observability and monitoring
- Load testing and optimization
- K8s deployment configurations

## 🎨 Design Philosophy

### Vegas Theme
- Fun, engaging casino-inspired elements
- Gold and red color palette
- Playful store names (Dice Mart, Jackpot Grocers)
- Celebration animations and sound effects

### Elastic Branding
- Professional blue and teal gradients
- "Powered by Elastic Agent Builder" messaging
- Search and analytics focus
- Clean, modern interface design

## 📊 Technical Highlights

### Data Architecture
- **Multi-index design** for complex joins
- **Semantic search** with ELSER embeddings
- **Real-time inventory** updates
- **Historical session** tracking

### Agent Intelligence
- **ES|QL queries** for data retrieval
- **Context-aware responses** based on user requests
- **Tool selection logic** per agent personality
- **Session memory** for conversation continuity

### Performance
- **Lazy loading** of UI components
- **Optimized ES queries** with proper indexing
- **Caching strategies** for repeated data
- **Responsive design** for all devices

## 🔧 Configuration

All components support extensive configuration:
- Dataset sizes and content types
- Game duration and target prices
- Agent personalities and available tools
- UI themes and branding elements

## 📝 License

MIT License - See individual component LICENSE files for details.

---

Built with ❤️ by the Elastic team for showcasing the power of Agent Builder and Elasticsearch at conferences worldwide.