import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  // Обработка перетаскивания файла
  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    setFile(droppedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };
  // Отправка файла на Flask API
  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:5050/predict",
        formData
      );
      setResult(response.data.style);
    } catch (error) {
      console.error("Ошибка при отправке:", error);
      alert("Flask-сервер не ответил. Проверь порт и CORS.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>🧠 Super Genius Web Art-Style</h1>
      <div
        className="drop-area"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        {file ? (
          <img
            src={URL.createObjectURL(file)}
            alt="preview"
            className="preview"
          />
        ) : (
          <p>Перетащи сюда картину или кликни ниже чтобы выбрать</p>
        )}
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="file-input"
        />
      </div>
      <button onClick={handleUpload} className="btn" disabled={loading}>
        {loading ? "Предсказываю..." : "Предсказать стиль"}
      </button>
      {result && <h2>🎨 Результат: {result}</h2>}
    </div>
  );
}

export default App;
