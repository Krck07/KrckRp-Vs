/**
 * KrckRP Frontend API Service
 * Handles all HTTP/WebSocket communication with the FastAPI backend
 */
class ApiService {
  constructor() {
    // Base URL - in production this would be configured from environment variables
    this.baseUrl = 'http://localhost:8000';
  }

  /**
   * Fetches data using GET request
   */
  async get(endpoint) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Posts data using POST request
   */
  async post(endpoint, data) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Patches data using PUT request
   */
  async put(endpoint, data) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Deletes data using DELETE request
   */
  async delete(endpoint) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  // Campaign and World related methods
  async getWorlds() {
    return this.get('/worlds');
  }

  async createWorld(worldData) {
    return this.post('/worlds', worldData);
  }

  async getWorld(id) {
    return this.get(`/worlds/${id}`);
  }

  async getCampaigns(worldId) {
    return this.get(`/worlds/${worldId}/campaigns`);
  }

  async createCampaign(campaignData) {
    return this.post('/campaigns', campaignData);
  }

  // Character related methods
  async getCharacters() {
    return this.get('/characters');
  }

  async createCharacter(characterData) {
    return this.post('/characters', characterData);
  }

  // Game play methods
  async getPlayerTurn(turnInput) {
    return this.post('/turns', turnInput);
  }

  async getGameHistory(campaignId, limit = 20) {
    return this.get(`/campaigns/${campaignId}/history?limit=${limit}`);
  }

  async undoTurn(campaignId, turnId) {
    return this.post(`/campaigns/${campaignId}/undo`, { turn_id: turnId });
  }

  // Correction tools
  async correctGameState(correctionData) {
    return this.post('/corrections', correctionData);
  }
}

// Create singleton instance
const apiService = new ApiService();

export default apiService;