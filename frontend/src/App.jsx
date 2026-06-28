import { useState, useEffect } from "react";
import FileSelector from "./components/FileSelector";
import ProgressBar from "./components/ProgressBar";
import SuccessMessage from "./components/SuccessMessage";
import ErrorMessage from "./components/ErrorMessage";

function App() {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const [serverStats, setServerStats] = useState({
    active: 0,
    peak: 0,
    total: 0,
    failed: 0,
  });

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:5000/api/stats");

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (!data.error) {
        setServerStats(data);
      }
    };

    return () => eventSource.close();
  }, []);

  const handleFileChange = (selectedFile) => {
    setFile(selectedFile);
    setStatus("idle");
    setProgress(0);
    setErrorMessage("");
  };

  const handleRealUpload = () => {
    if (!file) return;

    setStatus("uploading");
    setProgress(0);

    const formData = new FormData();
    formData.append("file", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:5000/api/transcode");

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percent = Math.round((event.loaded / event.total) * 100);
        setProgress(percent);
      }
    };

    xhr.onload = () => {
      setProgress(100);

      let data;
      try {
        data = JSON.parse(xhr.responseText);
      } catch {
        setStatus("error");
        setErrorMessage("Resposta inválida do servidor.");
        return;
      }

      if (xhr.status < 200 || xhr.status >= 300) {
        setStatus("error");
        setErrorMessage(data.error_message || "Erro inesperado na conversão.");
        return;
      }

      setStatus("success");

      const blob = new Blob([data.content], { type: "text/html" });
      const url = URL.createObjectURL(blob);
      const downloadLink = document.createElement("a");
      downloadLink.href = url;
      downloadLink.download = data.filename;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
      URL.revokeObjectURL(url);
    };

    xhr.onerror = () => {
      setStatus("error");
      setErrorMessage("Falha de comunicação com o servidor. Verifique se o BFF está ativo.");
    };

    xhr.send(formData);
  };

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.title}>Centro de Informática - UFPE</h1>
          <p style={styles.subtitle}>
            Servidor de Transcodificação de Documentos | Equipe 05
          </p>
        </div>
      </header>

      <section style={styles.statsPanel}>
        <div style={styles.statBox}>
          <strong>Ativas:</strong> {serverStats.active}
        </div>
        <div style={styles.statBox}>
          <strong>Pico:</strong> {serverStats.peak}
        </div>
        <div style={styles.statBox}>
          <strong>Sucessos:</strong> {serverStats.total}
        </div>
        <div style={styles.statBox}>
          <strong>Falhas:</strong> {serverStats.failed}
        </div>
      </section>

      <main style={styles.mainCard}>
        <h3 style={styles.cardTitle}>Transcodificador Markdown para HTML</h3>

        <FileSelector
          file={file}
          onFileChange={handleFileChange}
          onUpload={handleRealUpload}
          status={status}
        />

        {status === "uploading" && <ProgressBar progress={progress} />}
        {status === "success" && <SuccessMessage />}
        {status === "error" && <ErrorMessage message={errorMessage} />}
      </main>
    </div>
  );
}

const styles = {
  page: {
    backgroundColor: "#fdfdfd",
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    fontFamily: "-apple-system, BlinkMacSystemFont, sans-serif",
    margin: 0,
    padding: 0,
  },
  header: {
    backgroundColor: "#900020",
    color: "#ffffff",
    padding: "24px 16px",
    textAlign: "center",
    boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
  },
  headerContent: { maxWidth: "800px", margin: "0 auto" },
  title: {
    margin: 0,
    fontSize: "1.6rem",
    fontWeight: "700",
    letterSpacing: "0.5px",
  },
  subtitle: { margin: "6px 0 0 0", fontSize: "0.95rem", opacity: 0.85 },
  statsPanel: {
    display: "flex",
    justifyContent: "center",
    gap: "15px",
    margin: "25px auto 0 auto",
    maxWidth: "550px",
    width: "90%",
  },
  statBox: {
    backgroundColor: "#f8f9fa",
    padding: "10px 18px",
    borderRadius: "6px",
    fontSize: "0.85rem",
    color: "#495057",
    border: "1px solid #e9ecef",
    fontWeight: "500",
    boxShadow: "0 2px 4px rgba(0,0,0,0.02)",
  },
  mainCard: {
    backgroundColor: "#ffffff",
    maxWidth: "550px",
    width: "90%",
    margin: "30px auto",
    padding: "35px",
    borderRadius: "12px",
    boxShadow: "0 4px 25px rgba(0, 0, 0, 0.05)",
    border: "1px solid #f1f3f5",
    textAlign: "center",
  },
  cardTitle: { margin: "0 0 8px 0", color: "#212529", fontSize: "1.3rem" },
};

export default App;
