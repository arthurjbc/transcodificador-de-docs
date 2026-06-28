function FileSelector({ file, onFileChange, onUpload, status }) {
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.name.endsWith(".md")) {
      onFileChange(selectedFile);
    } else {
      alert("Por favor, selecione apenas arquivos Markdown (.md)");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.iconContainer}>
        <svg
          width="64"
          height="64"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#900020"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="17 8 12 3 7 8" />
          <line x1="12" y1="3" x2="12" y2="15" />
        </svg>
      </div>
      <label
        style={{
          ...styles.buttonSecondary,
          opacity: status === "uploading" ? 0.6 : 1,
        }}
      >
        Selecionar Arquivo Markdown (.md)
        <input
          type="file"
          accept=".md"
          onChange={handleFileChange}
          disabled={status === "uploading"}
          style={{ display: "none" }}
        />
      </label>

      {file && (
        <div style={styles.fileBox}>
          <span style={styles.fileName}>{file.name}</span>
        </div>
      )}

      <div style={styles.actionGroup}>
        <button
          onClick={onUpload}
          disabled={!file || status === "uploading"}
          style={{
            ...styles.buttonPrimary,
            backgroundColor:
              !file || status === "uploading" ? "#cca3aa" : "#900020",
          }}
        >
          {status === "uploading" ? "Processando Stream..." : "Transcodificar"}
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: "100%",
  },
  iconContainer: {
    marginBottom: "20px",
  },
  buttonSecondary: {
    padding: "12px 24px",
    backgroundColor: "#fff",
    color: "#900020",
    border: "2px solid #900020",
    borderRadius: "6px",
    fontWeight: "bold",
    cursor: "pointer",
    transition: "all 0.2s ease",
    textAlign: "center",
    boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
  },
  fileBox: {
    display: "flex",
    alignItems: "center",
    marginTop: "15px",
    padding: "10px 16px",
    backgroundColor: "#f8f9fa",
    border: "1px solid #e9ecef",
    borderRadius: "6px",
    width: "80%",
    maxWidth: "400px",
  },
  fileName: {
    fontSize: "0.9rem",
    color: "#495057",
    wordBreak: "break-all",
  },
  actionGroup: {
    marginTop: "25px",
    width: "100%",
    display: "flex",
    justifyContent: "center",
  },
  buttonPrimary: {
    padding: "14px 40px",
    color: "#white",
    border: "none",
    borderRadius: "6px",
    fontWeight: "bold",
    fontSize: "1rem",
    cursor: "pointer",
    boxShadow: "0 4px 6px rgba(144, 0, 32, 0.2)",
    transition: "background-color 0.2s ease",
  },
};

export default FileSelector;
