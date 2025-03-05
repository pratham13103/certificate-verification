import { useState } from "react";
import { verifyCertificate } from "./api";

const CertificateForm = () => {
    const [certNumber, setCertNumber] = useState("");
    const [certificate, setCertificate] = useState(null);
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        const data = await verifyCertificate(certNumber);
        if (data) {
            setCertificate(data);
        } else {
            setError("Invalid certificate number or no data found.");
        }
    };

    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            minHeight: "100vh",
            width: "100vw",
            backgroundColor: "#fff",
            padding: "16px"
        }}>
            <div style={{
                backgroundColor: "white",
                padding: "20px",
                borderRadius: "8px",
                boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
                textAlign: "center",
                width: "800px",
                maxWidth: "90vw"
            }}>
                <h1 style={{ fontSize: "24px", fontWeight: "bold", marginBottom: "16px" }}>
                    Enter Certificate Number
                </h1>
                <form onSubmit={handleSubmit} style={{ marginBottom: "16px" }}>
                    <div style={{ display: "flex", alignItems: "center", marginBottom: "8px" }}>
                        <label style={{ fontSize: "18px", marginRight: "8px", fontWeight: "bold" }}>
                            Certificate Number:
                        </label>
                        <input
                            type="text"
                            value={certNumber}
                            onChange={(e) => setCertNumber(e.target.value)}
                            required
                            style={{
                                flex: 1,
                                padding: "10px",
                                border: "1px solid #ccc",
                                borderRadius: "4px",
                                fontSize: "16px",
                                color: "black"
                            }}
                        />
                    </div>
                    <button 
                        type="submit" 
                        style={{
                            backgroundColor: "green",
                            color: "white",
                            padding: "10px 20px",
                            fontSize: "16px",
                            border: "none",
                            borderRadius: "4px",
                            cursor: "pointer",
                            width: "100%",
                            marginTop: "8px"
                        }}
                    >
                        Verify Certificate
                    </button>
                </form>

                {error && <p style={{ color: "red" }}>{error}</p>}

                {certificate && (
                    <div style={{ marginTop: "16px" }}>
                        <h2 style={{ fontSize: "20px", fontWeight: "bold" }}>Preview Certificate</h2>
                        <img 
                            src={`http://localhost:8000${certificate.image_url}`} 
                            alt="Certificate" 
                            width="800" 
                            height="500"
                            style={{ 
                                marginTop: "10px", 
                                border: "1px solid #ccc", 
                                borderRadius: "4px",
                                display: "block",
                                marginLeft: "auto",
                                marginRight: "auto"
                            }}
                        />
                        <div style={{ marginTop: "10px" }}>
                            <a 
                                href={`http://localhost:8000${certificate.image_url}`} 
                                download 
                                style={{ color: "blue", textDecoration: "underline" }}
                            >
                                Download Certificate
                            </a>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CertificateForm;
