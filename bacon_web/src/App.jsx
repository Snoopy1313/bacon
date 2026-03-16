import { useState } from 'react'
import './App.css'

function App() {
  const [source, setSource] = useState("");
  const [target, setTarget] = useState("");
  const [distance, setDistance] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    let myObject = await fetch(`http://localhost:5000/get_bacon_distance/${source}/${target}`);
    let myText = await myObject.text();
    setDistance(myText)
  };

  return (
      <form onSubmit={handleSubmit}>
          <label>Actors ID</label>
          <input
            type="text"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="Type something..."
          />
          <input
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="Type something..."
          />
        <button type="submit">
          Submit
        </button>
        <label>Bacon distance: {distance}</label>
      </form>
    )
}

export default App
