function ErrorMessage({ message }) {
  return (
    <div style={styles.box}>
      <span style={styles.icon}>⚠️</span>
      <div>
        <strong style={styles.title}>Falha no Processamento</strong>
        <p style={styles.text}>{message}</p>
      </div>
    </div>
  );
}

const styles = {
  box: {
    display: "flex",
    alignItems: "flex-start",
    marginTop: "25px",
    padding: "15px",
    backgroundColor: "#fce8e6",
    border: "1px solid #fad2cf",
    borderRadius: "6px",
    color: "#c5221f",
    fontSize: "0.9rem",
    textAlign: "left",
  },
  icon: { fontSize: "1.5rem", marginRight: "12px" },
  title: { display: "block", fontWeight: "bold", marginBottom: "3px" },
  text: { margin: 0, color: "#a51d1a" },
};

export default ErrorMessage;
