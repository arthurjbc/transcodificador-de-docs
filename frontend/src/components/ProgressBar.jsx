function ProgressBar({ progress }) {
  return (
    <div style={styles.container}>
      <div style={styles.labelRow}>
        <span style={styles.labelText}>Progresso do Upload (gRPC Stream)</span>
        <span style={styles.percentage}>{progress}%</span>
      </div>
      <div style={styles.track}>
        <div style={{ ...styles.bar, width: `${progress}%` }} />
      </div>
    </div>
  );
}

const styles = {
  container: { width: "100%", maxWidth: "450px", margin: "20px auto 0 auto" },
  labelRow: {
    display: "flex",
    justifycontent: "space-between",
    justifyContent: "space-between",
    marginBottom: "8px",
    fontSize: "0.85rem",
    color: "#6c757d",
    fontWeight: "500",
  },
  track: {
    width: "100%",
    backgroundColor: "#e9ecef",
    height: "10px",
    borderRadius: "5px",
    overflow: "hidden",
  },
  bar: {
    height: "100%",
    backgroundColor: "#900020",
    backgroundImage: "linear-gradient(90deg, #900020 0%, #e60026 100%)",
    borderRadius: "5px",
    transition: "width 0.3s ease-out",
  },
};

export default ProgressBar;
