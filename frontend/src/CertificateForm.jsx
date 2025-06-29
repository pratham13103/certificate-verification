import { useEffect, useState } from "react";
import { verifyCertificate, getCertificates } from "./api";

const CertificateForm = () => {
  const [certNumber, setCertNumber] = useState("");
  const [certificate, setCertificate] = useState(null);
  const [error, setError] = useState("");
  const [certList, setCertList] = useState([]);

  // Fetch list of certificates for sidebar
  useEffect(() => {
    const fetchCerts = async () => {
      const certs = await getCertificates();
      setCertList(certs);
    };
    fetchCerts();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const data = await verifyCertificate(certNumber);
    if (data) {
      setCertificate(data);
    } else {
      setCertificate(null);
      setError("Invalid certificate number or no data found.");
    }
  };

  const handleCertClick = (number) => {
    setCertNumber(number);
    setCertificate(null); // Clear previous preview
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", width: "100vw" }}>
      {/* Sidebar */}
      <div
        style={{
          width: "300px",
          backgroundColor: "#f5f5f5",
          padding: "20px",
          borderRight: "1px solid #ccc",
          overflowY: "auto",
        }}
      >
        <h2 style={{ fontSize: "35px", marginBottom: "16px", color: "#222" }}>
          Certificates List
        </h2>
        <ul style={{ listStyle: "none", padding: 0 }}>
          {certList.map((cert) => (
            <li
              key={cert.cert_number}
              onClick={() => handleCertClick(cert.cert_number)}
              style={{
                backgroundColor: "#fff",
                padding: "10px",
                borderRadius: "8px",
                boxShadow: "0px 1px 4px rgba(0, 0, 0, 0.1)",
                marginBottom: "12px",
                cursor: "pointer",
              }}
            >
              <strong>{cert.name}</strong>
              <br />
              <span
                style={{ fontSize: "18px", fontWeight: "bold", color: "black" }}
              >
                {cert.cert_number} {cert.name}
              </span>
            </li>
          ))}
        </ul>
      </div>

      {/* Main Form */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          backgroundColor: "#fff",
          padding: "32px",
        }}
      >
        <div
          style={{
            backgroundColor: "white",
            padding: "32px",
            borderRadius: "12px",
            boxShadow: "0px 8px 12px rgba(0, 0, 0, 0.15)",
            textAlign: "center",
            width: "1000px",
            maxWidth: "95vw",
          }}
        >
          <h1
            style={{
              fontSize: "32px",
              fontWeight: "bold",
              marginBottom: "24px",
              color: "black",
            }}
          >
            Enter Certificate Number
          </h1>
          <form onSubmit={handleSubmit} style={{ marginBottom: "24px" }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                marginBottom: "12px",
              }}
            >
              <label
                style={{
                  fontSize: "20px",
                  marginRight: "10px",
                  fontWeight: "bold",
                  color: "black",
                  minWidth: "200px",
                  textAlign: "right",
                }}
              >
                Certificate Number:
              </label>
              <input
                type="text"
                value={certNumber}
                onChange={(e) => setCertNumber(e.target.value)}
                required
                style={{
                  flex: 1,
                  padding: "14px",
                  border: "2px solid #ccc",
                  borderRadius: "6px",
                  fontSize: "18px",
                  color: "black",
                  backgroundColor: "white",
                  width: "100%",
                }}
              />
            </div>
            <button
              type="submit"
              style={{
                backgroundColor: "green",
                color: "white",
                padding: "14px 24px",
                fontSize: "18px",
                border: "none",
                borderRadius: "6px",
                cursor: "pointer",
                width: "100%",
                marginTop: "12px",
              }}
            >
              Verify Certificate
            </button>
          </form>

          {error && <p style={{ color: "red", fontSize: "18px" }}>{error}</p>}

          {certificate && (
            <div style={{ marginTop: "24px" }}>
              <h2
                style={{
                  fontSize: "24px",
                  fontWeight: "bold",
                  marginBottom: "16px",
                }}
              >
                Preview Certificate
              </h2>
              <img
                src={`http://localhost:8000${certificate.image_url}`}
                alt="Certificate"
                width="1000"
                height="600"
                style={{
                  marginTop: "20px",
                  border: "2px solid #ccc",
                  borderRadius: "6px",
                  display: "block",
                  marginLeft: "auto",
                  marginRight: "auto",
                }}
              />
              <div style={{ marginTop: "16px" }}>
                <a
                  href={`http://localhost:8000/download/${certificate.image_url.replace(
                    "/modified_certs/",
                    ""
                  )}`}
                  style={{
                    color: "blue",
                    textDecoration: "underline",
                    fontSize: "18px",
                  }}
                >
                  Download Certificate
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CertificateForm;
