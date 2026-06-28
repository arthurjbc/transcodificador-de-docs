function SuccessMessage() {
  return (
    <div style={styles.box}>
      <div>
        <strong style={styles.title}>Transcodificação Concluída!</strong>
        <p style={styles.text}>
          O arquivo HTML foi processado e baixado automaticamente no seu disco.
        </p>
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
    backgroundColor: "#e6f4ea",
    border: "1px solid #b7e1cd",
    borderRadius: "6px",
    color: "#137333",
    fontSize: "0.9rem",
    textAlign: "left",
  },
  title: { display: "block", fontWeight: "bold", marginBottom: "3px" },
  text: { margin: 0, color: "#137333" },
};

export default SuccessMessage;
