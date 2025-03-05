import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export const verifyCertificate = async (certNumber) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/verify/${certNumber}`);
        return response.data;
    } catch (error) {
        console.error("Error verifying certificate", error);
        return null;
    }
};
