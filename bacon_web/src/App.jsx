import { useState } from 'react'
import './App.css'

function App() {
  const [source, setSource] = useState("");
  const [target, setTarget] = useState("");
  const [message, setMessage] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    const response = await fetch(`http://localhost:5000/get_bacon_distance/${source}/${target}`);
    const data = await response.json();
    console.log(data)
    if (response.status == 400) {
      setMessage(`${data.error}: ${data.message}`)
    }
    else if (response.status == 200) {
      setMessage("Bacon distance: " + data.distance)
    }
    else {
      setMessage("Some error occurred")
    }
  };

  return (
      <form onSubmit={handleSubmit}>
          <label>Actors Bacon Distance Calculator</label>
          <input
            type="text"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="Type first actor..."
          />
          <input
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="Type second actor..."
          />
        <button type="submit">
          Submit
        </button>
        <label>{message}</label>
      </form>
    )
}

export default App
