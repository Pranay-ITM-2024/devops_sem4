const axios = require('axios');

// Point this to your FastAPI backend url
const API_BASE_URL = process.env.API_URL || 'http://localhost:8000/api';

describe('SOC Platform API Endpoints', () => {
    
    // Test the health endpoint
    test('GET /health should return status healthy', async () => {
        const response = await axios.get(`${API_BASE_URL}/health`);
        expect(response.status).toBe(200);
        expect(response.data.status).toBe('healthy');
    });

    // Test creating an alert
    let createdAlertId;

    test('POST /alerts should create a new alert', async () => {
        const newAlert = {
            title: "Jest Test Alert",
            description: "Testing API from Jest",
            severity: "low",
            source_ip: "192.168.1.1",
            dest_ip: "10.0.0.5",
            alert_type: "test"
        };

        const response = await axios.post(`${API_BASE_URL}/alerts`, newAlert);
        expect(response.status).toBe(201);
        expect(response.data.title).toBe("Jest Test Alert");
        expect(response.data.id).toBeDefined();
        
        // Save ID for the next test
        createdAlertId = response.data.id;
    });

    // Test getting alerts
    test('GET /alerts should return list of alerts', async () => {
        const response = await axios.get(`${API_BASE_URL}/alerts`);
        expect(response.status).toBe(200);
        expect(Array.isArray(response.data)).toBe(true);
        expect(response.data.length).toBeGreaterThan(0);
    });

    // Test executing a playbook
    test('POST /alerts/:id/respond should run a playbook successfully', async () => {
        expect(createdAlertId).toBeDefined();

        const payload = {
            action: "block_ip"
        };

        const response = await axios.post(`${API_BASE_URL}/alerts/${createdAlertId}/respond`, payload);
        expect(response.status).toBe(200);
        expect(response.data.status).toBe("success");
        expect(response.data.action).toBe("block_ip");
    });
});
